import json
import os
import joblib
import pickle
# import numpy as np
# import pandas as pd
import tensorflow as tf
# from channels.generic.websocket import AsyncWebsocketConsumer
# from channels.layers import get_channel_layer
# from django.core.cache import cache
import logging
# import requests
# import json

from preprocess.twelveSecFilter import preprocessing, GMM_model_twelve_sec
from preprocess.twelveSecPlot import PeakPredictor

logger = logging.getLogger('logger')

class PpgModelPredictor:
    def __init__(self, model_path, gmm_n_path, gmm_p_path, list_pickle_path, chunk_size, overlap):
        self.model_path = model_path
        self.gmm_n_path = gmm_n_path
        self.gmm_p_path = gmm_p_path
        self.list_pickle_path = list_pickle_path
        self.chunk_size = chunk_size
        self.overlap = overlap
        print("📍 Model path:", os.path.abspath(self.model_path))
        print("📍 GMM Negative path:", os.path.abspath(self.gmm_n_path))
        print("📍 GMM Positive path:", os.path.abspath(self.gmm_p_path))
        print("📍 Feature list path:", os.path.abspath(self.list_pickle_path))
        self.model = self.load_model()
        self.gmm_n, self.gmm_p, self.lab0_f, self.lab1_f, self.m_f, self.n_f = self.load_gmm_and_list()

    def load_model(self):
        logger.info("Loading TensorFlow model...")
        model = tf.keras.models.load_model(self.model_path)
        logger.info("TensorFlow model loaded successfully")
        return model

    def load_gmm_and_list(self):
        try:
            gmm_n_from_joblib = joblib.load(self.gmm_n_path)
            logger.debug("gmm_n loaded successfully")

            gmm_p_from_joblib = joblib.load(self.gmm_p_path)
            logger.debug("gmm_p loaded successfully")

            with open(self.list_pickle_path, "rb") as fi:
                test = pickle.load(fi)
            logger.debug("list.pickle loaded successfully")

            lab0_f = test[0]
            lab1_f = test[1]
            m_f = test[2]
            n_f = test[3]

            return gmm_n_from_joblib, gmm_p_from_joblib, lab0_f, lab1_f, m_f, n_f
        except Exception as e:
            logger.error(f"Error loading files: {e}")
            raise e

    def ppg_process_and_predict(self, ppg_data):
        try:
            ppg_data_list = [float(item) for item in ppg_data]
            if not ppg_data_list:
                logger.error('ppg_data_list is empty or invalid')
                return None, None, None, 'ppg_data_list is empty or invalid'

            test_data_list = [ppg_data_list]

            test_filtered = preprocessing(data=test_data_list, chunk_size=self.chunk_size, overlap=self.overlap)
            logger.debug(f"DEBUG: test_filtered = {test_filtered}")
            twelve_sec_filtered, twelve_sec_x, twelve_sec_y = test_filtered.dividing_and_extracting()

            if twelve_sec_filtered is None or twelve_sec_x is None or twelve_sec_y is None:
                logger.error('Testing preprocessing failed, resulting in None data.')
                return None, None, None, 'Testing preprocessing failed, resulting in None data.'

            model_for_twelve_sec = GMM_model_twelve_sec(twelve_sec_filtered, self.gmm_p, self.gmm_n,
                                                        self.lab0_f, self.lab1_f, self.m_f, self.n_f)
            x_test_twelve_sec, y_test_twelve_sec = model_for_twelve_sec.GMM_model()

            if x_test_twelve_sec is None or y_test_twelve_sec is None:
                logger.error('Modeling failed, resulting in None data.')
                return None, None, None, 'Modeling failed, resulting in None data.'

            predictor = PeakPredictor(self.model_path, x_test_twelve_sec)
            y_test_twelve_sec, state = predictor.predict_peaks()

            if not y_test_twelve_sec:
                logger.error('Prediction resulted in empty data.')
                return x_test_twelve_sec, None, state, 'Prediction resulted in empty data.'

            return x_test_twelve_sec, y_test_twelve_sec, state, None
        except Exception as e:
            logger.error(f"Exception: {str(e)}")
            return None, None, None, str(e)