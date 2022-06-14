from typing import Tuple, Optional

from django.conf import settings

from keras.metrics import Precision, Recall
from keras.optimizer_v2.adam import Adam
from keras.models import Model, load_model
from keras.preprocessing.image import ImageDataGenerator, DirectoryIterator


class UserModel:

    def __init__(self, base_model_path, train_path, validate_path, save_path):
        self.model: Model = load_model(base_model_path)
        self.save_path = save_path
        self.train_ds, self.validation_ds = self.load_datasets(train_path, validate_path)

        # Callbacks
        self.callbacks = []

    def train(self):
        print('train: Training...')
        self.lock(num_layers=4)

        self.model.compile(
            optimizer=Adam(),
            loss='categorical_crossentropy',
            metrics=['accuracy', Precision(), Recall()]
        )

        self.model.fit(
            self.train_ds,
            epochs=settings.USER_CLASSIFIER_MODEL['TRAINING_EPOCHS'],
            validation_data=self.validation_ds,
            callbacks=self.callbacks,
        )

    def fine_tune(self):
        print('fine_tune: Fine-Tuning...')
        self.unlock()
        self.model.compile(
            optimizer=Adam(1e-5),  # Very low learning rate
            loss='categorical_crossentropy',
            metrics=['accuracy', Precision(), Recall()]
        )

        self.model.fit(
            self.train_ds,
            epochs=settings.USER_CLASSIFIER_MODEL['FINE_TUNING_EPOCHS'],
            callbacks=self.callbacks,
            validation_data=self.validation_ds,
        )

    def save(self):
        print('save: Saving...')
        self.model.save(self.save_path)

    def lock(self, num_layers: Optional[int] = None):
        print('lock: Locking...')
        if num_layers is not None:
            index = len(self.model.layers) - num_layers

            for layer in self.model.layers[:index]:
                layer.trainable = False
            for layer in self.model.layers[index:]:
                layer.trainable = True
        else:
            for layer in self.model.layers:
                layer.trainable = False

    def unlock(self):
        print('unlock: Unlocking...')
        for layer in self.model.layers:
            layer.trainable = True

    def load_datasets(self, train_path, validate_path) -> Tuple[DirectoryIterator, DirectoryIterator]:
        print(f'load_datasets: Loading normal from {train_path}')
        train_datagen = ImageDataGenerator(
            rotation_range=12.,
            width_shift_range=0.2,
            height_shift_range=0.2,
            zoom_range=0.15,
            shear_range=0.2,
            brightness_range=(0.5, 1.0),
            horizontal_flip=True,
        )
        validate_datagen = ImageDataGenerator(
        )

        train_ds = train_datagen.flow_from_directory(
            train_path,
            target_size=settings.USER_CLASSIFIER_MODEL['IMAGE_SIZE'],
            batch_size=settings.USER_CLASSIFIER_MODEL['TRAINING_NBATCH'],
            classes=settings.USER_CLASSIFIER_MODEL['CLASSES'],
        )
        validate_ds = validate_datagen.flow_from_directory(
            validate_path,
            target_size=settings.USER_CLASSIFIER_MODEL['IMAGE_SIZE'],
            batch_size=settings.USER_CLASSIFIER_MODEL['VALIDATION_NBATCH'],
            classes=settings.USER_CLASSIFIER_MODEL['CLASSES'],
            shuffle=False,
        )

        return train_ds, validate_ds
