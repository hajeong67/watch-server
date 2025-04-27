import tensorflow as tf
import numpy as np

class PPGModel:
    """
    Class for performing predictions using a Keras .h5 model.
    """

    def __init__(self, model_path=None):
        """
        Initialize the PPGModel class.

        Args:
            model_path (str): Path to the .h5 model file.
        """
        self.model_path = model_path
        self.model = None

        if model_path:
            self.load_model()

    def load_model(self):
        """
        Load the .h5 model from the given path.
        """
        self.model = tf.keras.models.load_model(self.model_path)

    def get_input_shape(self):
        """
        Return the input shape expected by the model.
        """
        return self.model.input_shape

    def predict(self, ppg_signal):
        """
        Predict from a single PPG signal.

        Args:
            ppg_signal (list or np.ndarray): 1D list of PPG values.

        Returns:
            np.ndarray: Model prediction result.
        """
        input_data = np.array(ppg_signal, dtype=np.float32).reshape(1, -1, 1)
        return self.model.predict(input_data)
