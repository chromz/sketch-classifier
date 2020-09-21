# Rodrigo Custodio

from tensorflow import keras
from sklearn import preprocessing

import os
import pprint
import sklearn.model_selection as sk
import numpy as np
import tensorflow as tf
import joblib

class Trainer(object):
    """CNN Train class"""
    CLASS_SIZE = 7200
    DATA_FILE = "data.joblib"
    LABEL_FILE = "labels.joblib"
    CLASSES_FILE = "classes.joblib"
    def __init__(self):
        super(Trainer, self).__init__()

    def _get_dataset(self, dir_path):
        data = np.array([]).reshape(0, 28, 28, 1)
        labels = np.array([])
        data_name = f"{self.DATA_FILE}"
        labels_name = f"{self.LABEL_FILE}"
        if os.path.exists(data_name) and os.path.exists(labels_name):
            print("LOADING Dataset")
            data = joblib.load(data_name)
            labels = joblib.load(labels_name)
            return data, labels
        else:
            print("Preprocessing dataset")
        filelist = os.listdir(dir_path)
        np.random.seed(3123)
        np.random.shuffle(filelist)
        filelist = filelist[:20]
        pp = pprint.PrettyPrinter(indent=2)
        print("Valid classes")
        pp.pprint(filelist)
        for i, f in enumerate(filelist):
            if f.endswith(".npy"):
                sketches = np.load(f"{dir_path}/{f}")
                np.random.shuffle(sketches)
                label = os.path.splitext(f)[0]
                sketches = sketches[:self.CLASS_SIZE] / 255
                sketches_labels = np.full((sketches.shape[0],),
                                          label)
                print(f"Adding label {label} ({i}/{len(filelist)})", end="\r")
                sketches = sketches.reshape(len(sketches), 28, 28, 1)
                data = np.concatenate((data, sketches))
                labels = np.concatenate((labels, sketches_labels))
        print("")
        print("Dumping dataset")
        joblib.dump(data, data_name)
        joblib.dump(labels, labels_name)
        return data, labels

    def _get_model(self, train_images, test_images, train_labels, test_labels,
                   classes):
        num_classes = len(classes)
        model = keras.Sequential([
            keras.layers.Conv2D(64, (2, 2), strides=(1, 1), activation='relu',
                                input_shape=(28, 28, 1)),
            keras.layers.MaxPooling2D((2, 2)),
            keras.layers.Conv2D(64, (2, 2), strides=(1, 1), activation='relu'),
            keras.layers.Conv2D(128, (2, 2), activation='relu'),
            keras.layers.MaxPooling2D((2, 2)),
            keras.layers.Flatten(),
            keras.layers.Dense(256, activation='relu'),
            keras.layers.Dropout(.50),
            keras.layers.Dense(512, activation='relu'),
            keras.layers.Dropout(.50),
            keras.layers.Dense(num_classes, activation='softmax'),
        ])
        model.summary()
        model.compile(optimizer='adam', loss='sparse_categorical_crossentropy',
                      metrics=['accuracy'])
        model.fit(train_images, train_labels, epochs=10)
        _, test_acc = model.evaluate(test_images, test_labels)
        return model, test_acc

    def _get_full_model(self, train_images, train_labels, classes):
        num_classes = len(classes)
        model = keras.Sequential([
            keras.layers.Conv2D(64, (2, 2), strides=(1, 1), activation='relu',
                                input_shape=(28, 28, 1)),
            keras.layers.MaxPooling2D((2, 2)),
            keras.layers.Conv2D(64, (2, 2), strides=(1, 1), activation='relu'),
            keras.layers.Conv2D(128, (2, 2), activation='relu'),
            keras.layers.MaxPooling2D((2, 2)),
            keras.layers.Flatten(),
            keras.layers.Dense(256, activation='relu'),
            keras.layers.Dropout(.50),
            keras.layers.Dense(512, activation='relu'),
            keras.layers.Dropout(.50),
            keras.layers.Dense(num_classes, activation='softmax'),
        ])
        model.summary()
        model.compile(optimizer='adam', loss='sparse_categorical_crossentropy',
                      metrics=['accuracy'])
        model.fit(train_images, train_labels, epochs=10)
        return model



    def train(self, dir_path='data/'):
        data, labels = self._get_dataset(dir_path)
        label_encoder = preprocessing.LabelEncoder()
        labels = label_encoder.fit_transform(labels)
#          train_images, test_images, train_labels, test_labels = \
                #  sk.train_test_split(data, labels, test_size=0.2,
                                    #  random_state=42)

#          model, acc = self._get_model(train_images, test_images,
                                     #  train_labels, test_labels,
                                     #  label_encoder.classes_)
        # Full training
        model = self._get_full_model(data, labels, label_encoder.classes_)

        model.save("sketcher.ckpt")
        joblib.dump(label_encoder.classes_, self.CLASSES_FILE)


