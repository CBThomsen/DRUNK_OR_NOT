import tensorflow
import keras
from keras.models import Model
from keras.callbacks import ReduceLROnPlateau
import Loader
from tensorflow.python.framework import graph_util
from PIL import Image
from keras.models import Sequential
import sklearn.metrics

epochs = 1
batch_size = 100
max_size = 100

Loader.pickle()

X_train, Y_train, X_test, Y_test = Loader.unpickle('Pickles/pickle.pkl')

print(X_train[0].shape)
img = Image.fromarray(X_train[0],'RGB')
img.save('test.png')
img.show()

model = Sequential()
model.add(keras.layers.Dropout(0.5, input_shape=(max_size, max_size, 3)))
model.add(keras.layers.Conv2D(16, 10, strides=(2, 2), input_shape=(max_size,max_size,3), data_format='channels_last',  padding='same'))
model.add(keras.layers.Activation('relu'))
model.add(keras.layers.MaxPooling2D(pool_size=5, strides=1, padding='same'))
model.add(keras.layers.Dropout(0.5))
model.add(keras.layers.Conv2D(32, 8, strides=(2, 2), padding='same'))
model.add(keras.layers.Activation('relu'))
model.add(keras.layers.MaxPooling2D(pool_size=5, strides=1, padding='same'))

model.add(keras.layers.Dropout(0.5))
model.add(keras.layers.Conv2D(64,6, strides=(2, 2), padding='same'))
model.add(keras.layers.Activation('relu'))

model.add(keras.layers.MaxPooling2D(pool_size=5, strides=1, padding='same'))

model.add(keras.layers.Dropout(0.5))
model.add(keras.layers.Conv2D(128,4, strides=(2, 2), padding='same'))
model.add(keras.layers.Activation('relu'))
model.add(keras.layers.MaxPooling2D(pool_size=5, strides=1, padding='same'))

model.add(keras.layers.GlobalAveragePooling2D())
model.add(keras.layers.Dropout(0.5))

model.add(keras.layers.Dense(Y_train.shape[1], activation='softmax'))
optimizer = keras.optimizers.Adam(lr=0.0005)
best_model = keras.callbacks.ModelCheckpoint('modellen' + '.h5', monitor='val_loss',
                                                          save_best_only=True)

model.summary()
model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])
session = keras.backend.get_session()
print(graph_util.convert_variables_to_constants(session, session.graph_def, [node.op.name for node in model.outputs]))


hist = model.fit(X_train, Y_train, batch_size=batch_size, epochs=epochs, verbose=1, validation_data=(X_test, Y_test))

model_json = model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
model.save_weights("model.h5")

