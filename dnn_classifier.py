import numpy as np
import os
import tensorflow as tf

INPUT_TENSOR_NAME = 'inputs'


def estimator_fn(run_config, params):
    feature_columns = [tf.feature_column.numeric_column(INPUT_TENSOR_NAME, shape=[29])]
    return tf.estimator.DNNClassifier(feature_columns=feature_columns, hidden_units=[10, 20, 10], n_classes=2, config=run_config)


def serving_input_fn(params):
    feature_spec = {INPUT_TENSOR_NAME: tf.FixedLenFeature(dtype=tf.float32, shape=[29])}
    return tf.estimator.export.build_parsing_serving_input_receiver_fn(feature_spec)()


def train_input_fn(training_dir, params):
    """Input function that would feed the model during training"""
    return _generate_input_fn(training_dir, 'train.csv')


def eval_input_fn(training_dir, params):
    """Input function that would feed the model during evaluation"""
    return _generate_input_fn(training_dir, 'test.csv')


def _generate_input_fn(training_dir, training_filename):
    training_set = tf.contrib.learn.datasets.base.load_csv_without_header(
        filename=os.path.join(training_dir, training_filename),
        target_dtype=np.int,
        features_dtype=np.float32)

    return tf.estimator.inputs.numpy_input_fn(
        x={INPUT_TENSOR_NAME: np.array(training_set.data)},
        y=np.array(training_set.target),
        num_epochs=None,
        shuffle=True)()
