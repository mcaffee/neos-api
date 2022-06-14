import tensorflow as tf


class ModelConverter:

    def __init__(self, model_path, save_path):
        self.converter = tf.lite.TFLiteConverter.from_saved_model(str(model_path))
        self.converter.optimizations = [tf.lite.Optimize.DEFAULT]
        self.save_path = save_path

    def convert(self):
        tflite_model = self.converter.convert()

        with open(self.save_path, 'wb') as outfile:
            outfile.write(tflite_model)
