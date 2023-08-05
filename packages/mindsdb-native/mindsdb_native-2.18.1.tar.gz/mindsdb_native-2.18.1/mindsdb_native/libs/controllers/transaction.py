from mindsdb_native.libs.constants.mindsdb import *
from mindsdb_native.libs.helpers.general_helpers import *
from mindsdb_native.libs.data_types.transaction_data import TransactionData
from mindsdb_native.libs.data_types.transaction_output_data import (
    PredictTransactionOutputData,
    TrainTransactionOutputData
)
from mindsdb_native.libs.data_types.mindsdb_logger import log
from mindsdb_native.config import CONFIG

import _thread
import traceback
import importlib
import datetime
import pickle
import dill
import sys
from copy import deepcopy
import pandas as pd
import numpy as np


class Transaction:
    def __init__(self,
                 session,
                 light_transaction_metadata,
                 heavy_transaction_metadata,
                 logger=log):
        """
        A transaction is the interface to start some MindsDB operation within a session

        :param session:
        :param transaction_metadata: dict
        :param heavy_transaction_metadata: dict
        """

        self.session = session
        self.lmd = light_transaction_metadata
        self.lmd['created_at'] = str(datetime.datetime.now())
        self.hmd = heavy_transaction_metadata

        # variables to de defined by setup
        self.error = None
        self.errorMsg = None

        self.input_data = TransactionData()
        self.output_data = TrainTransactionOutputData()

        # variables that can be persisted

        self.log = logger

        self.run()

    def load_metadata(self):
        try:
            import resource
            resource.setrlimit(resource.RLIMIT_STACK, [0x10000000, resource.RLIM_INFINITY])
            sys.setrecursionlimit(0x100000)
        except Exception:
            pass

        fn = os.path.join(CONFIG.MINDSDB_STORAGE_PATH, self.lmd['name'], 'light_model_metadata.pickle')
        try:
            self.lmd = load_lmd(fn)
        except Exception as e:
            self.log.error(e)
            self.log.error(f'Could not load mindsdb light metadata from the file: {fn}')

        fn = os.path.join(CONFIG.MINDSDB_STORAGE_PATH, self.hmd['name'], 'heavy_model_metadata.pickle')
        try:
            self.hmd = load_hmd(fn)
        except Exception as e:
            self.log.error(e)
            self.log.error(f'Could not load mindsdb heavy metadata in the file: {fn}')

        icp_fn = os.path.join(CONFIG.MINDSDB_STORAGE_PATH, self.hmd['name'], 'icp.pickle')
        try:
            with open(icp_fn, 'rb') as fp:
                self.hmd['icp'] = dill.load(fp)
                # restore MDB predictors in ICP objects
                # for col in self.lmd['predict_columns']:
                #     self.hmd['icp'][col].nc_function.model.model = self.session.transaction.model_backend.predictor
        except FileNotFoundError as e:
            self.hmd['icp'] = {'active': False}
            self.log.warning(f'Could not find mindsdb conformal predictor.')
        except Exception as e:
            self.log.error(e)
            self.log.error(f'Could not load mindsdb conformal predictor in the file: {icp_fn}')

    def save_metadata(self):
        Path(CONFIG.MINDSDB_STORAGE_PATH).joinpath(self.lmd['name']).mkdir(mode=0o777, exist_ok=True, parents=True)
        fn = os.path.join(CONFIG.MINDSDB_STORAGE_PATH, self.lmd['name'], 'light_model_metadata.pickle')
        self.lmd['updated_at'] = str(datetime.datetime.now())
        try:
            with open(fn, 'wb') as fp:
                pickle.dump(self.lmd, fp,protocol=pickle.HIGHEST_PROTOCOL)
        except Exception as e:
            self.log.error(traceback.print_exc())
            self.log.error(e)
            self.log.error(f'Could not save mindsdb light metadata in the file: {fn}')

        fn = os.path.join(CONFIG.MINDSDB_STORAGE_PATH, self.hmd['name'], 'heavy_model_metadata.pickle')
        save_hmd = {}
        null_out_fields = ['from_data', 'icp', 'breakpoint']
        for k in null_out_fields:
            save_hmd[k] = None

        for k in self.hmd:
            if k not in null_out_fields:
                save_hmd[k] = self.hmd[k]
            if k == 'model_backend' and not isinstance(self.hmd['model_backend'], str):
                save_hmd[k] = None

        try:
            with open(fn, 'wb') as fp:
                # Don't save data for now
                pickle.dump(save_hmd, fp, protocol=pickle.HIGHEST_PROTOCOL)
        except Exception as e:
            self.log.error(e)
            self.log.error(traceback.print_exc())
            self.log.error(f'Could not save mindsdb heavy metadata in the file: {fn}')

        if 'icp' in self.hmd.keys() and self.hmd['icp']['active']:
            icp_fn = os.path.join(CONFIG.MINDSDB_STORAGE_PATH, self.hmd['name'], 'icp.pickle')
            try:
                mdb_predictors = {}
                with open(icp_fn, 'wb') as fp:
                    # clear data cache
                    # TODO: restore model clearing as soon as we can access a loaded predictor from a session
                    for key in self.hmd['icp'].keys():
                        if key != 'active':
                            # mdb_predictors[key] = self.hmd['icp'][key].nc_function.model.model
                            # self.hmd['icp'][key].nc_function.model.model = None
                            self.hmd['icp'][key].nc_function.model.last_x = None
                            self.hmd['icp'][key].nc_function.model.last_y = None

                    dill.dump(self.hmd['icp'], fp, protocol=dill.HIGHEST_PROTOCOL)

                    # restore predictor
                    # for key in self.hmd['icp'].keys():
                    #     if key != 'active':
                    #         self.hmd['icp'][key].nc_function.model.model = mdb_predictors[key]

            except Exception as e:
                self.log.error(e)
                self.log.error(traceback.print_exc())
                self.log.error(f'Could not save mindsdb conformal predictor in the file: {icp_fn}')

    def _call_phase_module(self, module_name, **kwargs):
        """
        Loads the module and runs it
        """

        self.lmd['is_active'] = True
        self.lmd['phase'] = module_name
        module_path = convert_cammelcase_to_snake_string(module_name)
        module_full_path = f'mindsdb_native.libs.phases.{module_path}.{module_path}'
        try:
            main_module = importlib.import_module(module_full_path)
            module = getattr(main_module, module_name)
            return module(self.session, self)(**kwargs)
        except Exception:
            error = f'Could not load module {module_name}'
            self.log.error(error)
            raise
        finally:
            self.lmd['phase'] = module_name
            self.lmd['is_active'] = False

            if  self.hmd['breakpoint'] is not None:
                 if module_name in self.hmd['breakpoint']:
                     self.hmd['breakpoint'][module_name]()

    def run(self):
        pass


class LearnTransaction(Transaction):
    def _run(self):
        try:
            self.lmd['current_phase'] = MODEL_STATUS_PREPARING
            self.save_metadata()

            self._call_phase_module(module_name='DataExtractor')
            self.save_metadata()

            self._call_phase_module(module_name='DataCleaner')
            self.save_metadata()

            self._call_phase_module(module_name='TypeDeductor',
                                    input_data=self.input_data)
            self.save_metadata()

            #if not self.lmd['quick_learn']: <-- replace with histogram only if this ends up being heavily used
            self.lmd['current_phase'] = MODEL_STATUS_DATA_ANALYSIS
            self._call_phase_module(module_name='DataAnalyzer',
                                    input_data=self.input_data)
            self.save_metadata()

            self._call_phase_module(module_name='DataCleaner')
            self.save_metadata()

            self._call_phase_module(module_name='DataSplitter')
            self.save_metadata()

            self._call_phase_module(module_name='DataTransformer', input_data=self.input_data)
            self.lmd['current_phase'] = MODEL_STATUS_TRAINING
            self.save_metadata()
            self._call_phase_module(module_name='ModelInterface', mode='train')

            if not self.lmd['quick_learn']:
                self.lmd['current_phase'] = MODEL_STATUS_ANALYZING
                self.save_metadata()
                self._call_phase_module(module_name='ModelAnalyzer')

            self.lmd['current_phase'] = MODEL_STATUS_TRAINED
            self.save_metadata()
            return

        except Exception as e:
            self.lmd['is_active'] = False
            self.lmd['current_phase'] = MODEL_STATUS_ERROR
            self.lmd['error_msg'] = traceback.print_exc()
            self.log.error(str(e))
            raise e

    def run(self):
        if CONFIG.EXEC_LEARN_IN_THREAD == False:
            self._run()
        else:
            _thread.start_new_thread(self._run(), ())


class AnalyseTransaction(Transaction):
    def run(self):
        self._call_phase_module(module_name='DataExtractor')
        self._call_phase_module(module_name='DataCleaner')
        self._call_phase_module(module_name='TypeDeductor', input_data=self.input_data)
        self._call_phase_module(module_name='DataAnalyzer', input_data=self.input_data)
        self.lmd['current_phase'] = MODEL_STATUS_DONE


class PredictTransaction(Transaction):
    def run(self):
        old_lmd = {}
        for k in self.lmd: old_lmd[k] = self.lmd[k]

        old_hmd = {}
        for k in self.hmd: old_hmd[k] = self.hmd[k]
        self.load_metadata()

        for k in old_lmd:
            if old_lmd[k] is not None:
                self.lmd[k] = old_lmd[k]
            else:
                if k not in self.lmd:
                    self.lmd[k] = None

        for k in old_hmd:
            if old_hmd[k] is not None:
                self.hmd[k] = old_hmd[k]
            else:
                if k not in self.hmd:
                    self.hmd[k] = None

        if self.lmd is None:
            self.log.error('No metadata found for this model')
            return

        self._call_phase_module(module_name='DataExtractor')

        if self.input_data.data_frame.shape[0] <= 0:
            self.log.error('No input data provided !')
            return
        if self.lmd['tss']['is_timeseries']:
            self._call_phase_module(module_name='DataSplitter')

        if self.lmd['quick_predict']:
            self._call_phase_module(module_name='DataTransformer', input_data=self.input_data)
            self._call_phase_module(module_name='ModelInterface', mode='predict')
            self.output_data = self.hmd['predictions']
            return

        # @TODO Maybe move to a separate "PredictionAnalysis" phase ?
        if self.lmd['run_confidence_variation_analysis'] and not self.lmd['tss']['is_timeseries']:
            nulled_out_data = []
            nulled_out_columns = []
            for column in self.input_data.columns:
                # Only adapted for a single `when`
                if self.input_data.data_frame.iloc[0][column] is not None:
                    nulled_out_data.append(self.input_data.data_frame.iloc[0].copy())
                    nulled_out_data[-1][column] = None
                    nulled_out_columns.append(column)

            nulled_out_data = pd.DataFrame(nulled_out_data)

        for mode in ['predict', 'analyze_confidence']:
            if mode == 'analyze_confidence':
                if not self.lmd['run_confidence_variation_analysis'] or self.lmd['tss']['is_timeseries']:
                    continue
                else:
                    self.input_data.data_frame = nulled_out_data

            self._call_phase_module(module_name='DataTransformer', input_data=self.input_data)

            self._call_phase_module(module_name='ModelInterface', mode='predict')

            output_data = {col: [] for col in self.lmd['columns']}

            if 'make_predictions' in self.input_data.data_frame.columns:
                predictions_df = pd.DataFrame(self.input_data.data_frame[self.input_data.data_frame['make_predictions'] == True])
                del predictions_df['make_predictions']
            else:
                predictions_df = self.input_data.data_frame

            for column in self.input_data.columns:
                if column in self.lmd['predict_columns']:
                    output_data[f'__observed_{column}'] = list(predictions_df[column])
                else:
                    output_data[column] = list(predictions_df[column])

            for predicted_col in self.lmd['predict_columns']:
                output_data[predicted_col] = list(self.hmd['predictions'][predicted_col])
                for extra_column in [f'{predicted_col}_model_confidence', f'{predicted_col}_confidence_range']:
                    if extra_column in self.hmd['predictions']:
                        output_data[extra_column] = self.hmd['predictions'][extra_column]

                probabilistic_validator = unpickle_obj(self.hmd['probabilistic_validators'][predicted_col])
                output_data[f'{predicted_col}_confidence'] = [None] * len(output_data[predicted_col])

                output_data[f'model_{predicted_col}'] = deepcopy(output_data[predicted_col])
                for row_number, predicted_value in enumerate(output_data[predicted_col]):

                    # Compute the feature existance vector
                    input_columns = [col for col in self.input_data.columns if col not in self.lmd['predict_columns']]
                    features_existance_vector = [False if  str(output_data[col][row_number]) in ('None', 'nan', '', 'Nan', 'NAN', 'NaN') else True for col in input_columns if col not in self.lmd['columns_to_ignore']]

                    # Create the probabilsitic evaluation
                    probability_true_prediction = probabilistic_validator.evaluate_prediction_accuracy(features_existence=features_existance_vector, predicted_value=predicted_value)

                    output_data[f'{predicted_col}_confidence'][row_number] = probability_true_prediction

            # confidence estimation
            if self.hmd['icp']['active']:
                self.lmd['all_conformal_ranges'] = {}
                for predicted_col in self.lmd['predict_columns']:
                    X = deepcopy(predictions_df)
                    for col in self.lmd['columns_to_ignore'] + self.lmd['predict_columns']:
                        X.pop(col)

                    if self.lmd['stats_v2'][predicted_col]['typing']['data_type'] == DATA_TYPES.NUMERIC and not self.lmd['tss']['is_timeseries']:
                        tol_const = 2  # std devs
                        tolerance = self.lmd['stats_v2']['train_std_dev'][predicted_col] * tol_const
                        self.lmd['all_conformal_ranges'][predicted_col] = self.hmd['icp'][predicted_col].predict(X.values)
                        for sample_idx in range(self.lmd['all_conformal_ranges'][predicted_col].shape[0]):
                            sample = self.lmd['all_conformal_ranges'][predicted_col][sample_idx, :, :]
                            for idx in range(sample.shape[1]):
                                significance = (99 - idx) / 100
                                diff = sample[1, idx] - sample[0, idx]
                                if diff <= tolerance:
                                    output_data[f'{predicted_col}_confidence'][sample_idx] = significance
                                    output_data[f'{predicted_col}_confidence_range'][sample_idx] = list(sample[:, idx])
                                    break
                            else:
                                output_data[f'{predicted_col}_confidence'][sample_idx] = 0.9901  # default
                                bounds = sample[:, 0]
                                sigma = (bounds[1] - bounds[0]) / 2
                                output_data[f'{predicted_col}_confidence_range'][sample_idx] = [bounds[0] - sigma, bounds[1] + sigma]

                    elif self.lmd['stats_v2'][predicted_col]['typing']['data_type'] == DATA_TYPES.CATEGORICAL and not self.lmd['tss']['is_timeseries']:
                        if self.lmd['stats_v2'][predicted_col]['typing']['data_subtype'] != DATA_SUBTYPES.TAGS:
                            all_ranges = np.array([self.hmd['icp'][predicted_col].predict(X.values, significance=s / 100) for s in range(1, 100)])
                            self.lmd['all_conformal_ranges'][predicted_col] = np.swapaxes(np.swapaxes(all_ranges, 0, 2), 0, 1)
                            for sample_idx in range(self.lmd['all_conformal_ranges'][predicted_col].shape[0]):
                                sample = self.lmd['all_conformal_ranges'][predicted_col][sample_idx, :, :]
                                for idx in range(sample.shape[1]):
                                    significance = (99 - idx) / 100
                                    if np.sum(sample[:, idx]) == 1:
                                        output_data[f'{predicted_col}_confidence'][sample_idx] = significance
                                        break
                                else:
                                    output_data[f'{predicted_col}_confidence'][sample_idx] = 0.005

            if mode == 'predict':
                self.output_data = PredictTransactionOutputData(transaction=self, data=output_data)
            else:
                nulled_out_predictions = PredictTransactionOutputData(transaction=self, data=output_data)

        if self.lmd['run_confidence_variation_analysis'] and not self.lmd['tss']['is_timeseries']:
            input_confidence = {}
            extra_insights = {}

            for predicted_col in self.lmd['predict_columns']:
                input_confidence[predicted_col] = {}
                extra_insights[predicted_col] = {'if_missing':[]}

                actual_confidence = self.output_data[0].explanation[predicted_col]['confidence']

                for i, nulled_col_name in enumerate(nulled_out_columns):
                    nulled_out_predicted_value = nulled_out_predictions[i].explanation[predicted_col]['predicted_value']
                    nulled_confidence = nulled_out_predictions[i].explanation[predicted_col]['confidence']
                    confidence_variation = actual_confidence - nulled_confidence

                    input_confidence[predicted_col][nulled_col_name] = round(confidence_variation,3)
                    extra_insights[predicted_col]['if_missing'].append({nulled_col_name: nulled_out_predicted_value})

            self.output_data._input_confidence = input_confidence
            self.output_data._extra_insights = extra_insights


class BadTransaction(Transaction):
    def run(self):
        self.log.error(self.errorMsg)
        self.error = True
