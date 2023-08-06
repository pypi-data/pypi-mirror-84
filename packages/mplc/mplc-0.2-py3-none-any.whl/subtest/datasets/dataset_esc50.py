# -*- coding: utf-8 -*-
"""
ESC-50 dataset
More infos at https://github.com/karolpiczak/ESC-50
"""
import glob
import shutil
import zipfile
from pathlib import Path
from time import sleep
from urllib.error import HTTPError, URLError
from urllib.request import urlretrieve

import numpy as np
import pandas as pd
from keras.layers import Conv2D, GlobalAveragePooling2D, MaxPooling2D
from keras.layers import Dense, Dropout
from keras.losses import categorical_crossentropy
from keras.models import Sequential
from keras.utils import to_categorical
from librosa import load as wav_load
from librosa.feature import mfcc
from loguru import logger
from sklearn.model_selection import train_test_split

from . import dataset
from .. import constants

num_classes = 50
input_shape = (40, 431, 1)


# return a dataset object
def generate_new_dataset():
    # Load data
    (x_train, y_train), (x_test, y_test) = load_data()

    # Pre-process inputs
    logger.info('Preprocessing the raw audios')
    x_train = preprocess_dataset_inputs(x_train)
    x_test = preprocess_dataset_inputs(x_test)

    dataset_obj = dataset.Dataset(
        "esc50",
        x_train,
        x_test,
        y_train,
        y_test,
        input_shape,
        num_classes,
        preprocess_dataset_labels,
        generate_new_model_for_dataset,
        train_val_split_global,
        train_test_split_local,
        train_val_split_local
    )
    return dataset_obj


# Init dataset-specific functions

# Preprocess functions
def preprocess_dataset_labels(y):
    y = to_categorical(y, num_classes)

    return y


def preprocess_dataset_inputs(x):
    """
    Compute the Mel-Frequency Cepstral Coefficients
    :param x: iterator. Yield tuples, of audio and rate.
    :return: Array of mfcc images.
    """

    features_list = []
    for audio, rate in x:
        mfccs = mfcc(y=audio, sr=rate, n_mfcc=40)
        # mfccs_scaled = np.mean(mfccs.T, axis=0)
        features_list.append(mfccs)
    features = np.array(features_list)
    return features.reshape(((features.shape[0],) + input_shape))


# download train and test sets
def load_data():
    """
    load the dataset. Note that the x are iterators which need to be preprocess
    :return: (x_train, y_train), (x_test, y_test)
    """
    path = Path(__file__).resolve().parents[0]
    folder = path / 'local_data' / 'esc50'
    if not folder.is_dir():
        Path.mkdir(folder)
        logger.info('ESC-50 dataset not found.')
        _download_data(str(folder))
    else:
        logger.info('ESC-50 dataset found')

    esc50_df = pd.read_csv(folder / 'esc50.csv')
    train, test = train_test_split_global(esc50_df)
    y_train = train.target.to_numpy()
    y_test = test.target.to_numpy()
    x_train = (wav_load((folder / 'audio' / file_name).resolve(), sr=None)
               for file_name in train.filename.to_list())
    x_test = (wav_load((folder / 'audio' / file_name).resolve(), sr=None)
              for file_name in test.filename.to_list())

    return (x_train, y_train), (x_test, y_test)


def _download_data(path):
    """
    Download the dataset, and unzip it. The dataset will be stored in the datasets/local_data directory, which is
    gitignored

    :param path: provided by load_data.
                 Should be LOCAL_DIR/distributed-learning-contributivity/datasets/local_data/esc50
    :return: None
    """
    logger.info('Downloading it from https://github.com/karoldvl/ESC-50/')
    attempts = 0
    while True:
        try:
            urlretrieve('https://github.com/karoldvl/ESC-50/archive/master.zip', f'{path}/ESC-50.zip')
            break
        except (HTTPError, URLError) as e:
            if hasattr(e, 'code'):
                temp = e.code
            else:
                temp = e.errno
            logger.debug(
                f'URL fetch failure on '
                f'https://github.com/karoldvl/ESC-50/archive/master.zip : '
                f'{temp} -- {e.reason}')
            if attempts < constants.NUMBER_OF_DOWNLOAD_ATTEMPTS:
                sleep(2)
                attempts += 1
            else:
                raise
    logger.info('Extraction at distributed-learning-contributivity/datasets/local_data/esc50')
    with zipfile.ZipFile(f'{path}/ESC-50.zip') as package:
        package.extractall(f'{path}/')

    Path.unlink(Path(path) / 'ESC-50.zip')
    for src in glob.glob(f'{path}/ESC-50-master/audio'):
        shutil.move(src, f'{path}/{str(Path(src).name)}')
    shutil.move(f'{path}/ESC-50-master/meta/esc50.csv', f'{path}/esc50.csv')

    shutil.rmtree(f'{path}/ESC-50-master')


# Model structure and generation
def generate_new_model_for_dataset():
    # The model is adapted from https://github.com/mikesmales/Udacity-ML-Capstone
    # It was initially design to work on the URBANSOUND8K DATASET
    model = Sequential()
    model.add(Conv2D(filters=16, kernel_size=2, input_shape=input_shape, activation='relu'))
    model.add(MaxPooling2D(pool_size=2))
    model.add(Dropout(0.2))

    model.add(Conv2D(filters=32, kernel_size=2, activation='relu'))
    model.add(MaxPooling2D(pool_size=2))
    model.add(Dropout(0.2))

    model.add(Conv2D(filters=64, kernel_size=2, activation='relu'))
    model.add(MaxPooling2D(pool_size=2))
    model.add(Dropout(0.2))

    model.add(Conv2D(filters=128, kernel_size=2, activation='relu'))
    model.add(MaxPooling2D(pool_size=2))
    model.add(Dropout(0.2))
    model.add(GlobalAveragePooling2D())

    model.add(Dense(num_classes, activation='softmax'))
    model.compile(
        loss=categorical_crossentropy,
        optimizer="adam",
        metrics=["accuracy"],
    )
    return model


# train, test, val splits

def train_test_split_local(x, y):
    return x, np.array([]), y, np.array([])


def train_val_split_local(x, y):
    return x, np.array([]), y, np.array([])


def train_val_split_global(x, y):
    return train_test_split(x, y, test_size=0.1, random_state=42)


def train_test_split_global(data):
    return train_test_split(data, test_size=0.1, random_state=42)
