import tensorflow
import keras
from keras.models import Model
from keras.callbacks import ReduceLROnPlateau
import Loader
from keras.models import Sequential

epochs = 10
batch_size = 20
max_size = 800

Loader.pickle()

X_train, Y_train, X_test, Y_test = Loader.unpickle('Pickles/pickle.pkl')

print(X_train.shape)
print(X_train.ndim)
input = keras.layers.Input(X_train.shape[:])
print(input.shape)

model = Sequential()
model.add(keras.layers.Dropout(0.5, input_shape=(max_size, max_size, 3)))
model.add(keras.layers.Conv2D(10, 10, strides=(2, 2), input_shape=(max_size,max_size,3), data_format='channels_last',  padding='same'))
model.add(keras.layers.Activation('relu'))
model.add(keras.layers.MaxPooling2D(pool_size=5, strides=1, padding='same'))
model.add(keras.layers.Dropout(0.5))
model.add(keras.layers.Conv2D(20, 8, strides=(2, 2), padding='same'))
model.add(keras.layers.Activation('relu'))
model.add(keras.layers.MaxPooling2D(pool_size=5, strides=1, padding='same'))

model.add(keras.layers.Dropout(0.5))
model.add(keras.layers.Conv2D(30,6, strides=(2,2), padding='same'))
model.add(keras.layers.Activation('relu'))


model.add(keras.layers.GlobalAveragePooling2D())
model.add(keras.layers.Dropout(0.5))

model.add(keras.layers.Dense(Y_train.shape[1], activation='softmax'))
optimizer = keras.optimizers.Adam(lr=0.0005)
best_model = keras.callbacks.ModelCheckpoint('modellen' + '.h5', monitor='val_loss',
                                                          save_best_only=True)

model.summary()
model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])

hist = model.fit(X_train, Y_train, batch_size=batch_size, epochs=epochs, verbose=1, validation_data=(X_test, Y_test))