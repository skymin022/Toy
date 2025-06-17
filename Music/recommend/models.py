from keras.models import Sequential
from keras.layers import LSTM, Conv1D, Dense, Flatten, Reshape, InputLayer

def generator_model(input_shape=(100, 1)):
    model = Sequential()
    model.add(InputLayer(input_shape=input_shape))
    model.add(Conv1D(64, kernel_size=3, activation='relu', padding='same'))
    model.add(LSTM(128, return_sequences=True))
    model.add(Flatten())
    model.add(Dense(256, activation='relu'))
    model.add(Dense(100 * 2, activation='sigmoid'))
    model.add(Reshape((100, 2)))
    return model
