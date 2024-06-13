import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.layers import Input, BatchNormalization, Reshape, Dense, LeakyReLU, Conv2DTranspose
from tensorflow.keras.models import Model
import os
from datetime import datetime


def make_generator_model():
    input_1 = Input(shape=(100, ), name="Input_image")
    x = Dense(25*25*256, use_bias=False)(input_1)
    x = BatchNormalization()(x)
    x = LeakyReLU()(x)
    x = Reshape((25, 25, 256))(x)
    x = Conv2DTranspose(256, (1, 1), strides=(
        1, 1), padding='same', use_bias=False)(x)
    x = BatchNormalization()(x)
    x = LeakyReLU()(x)
    x = Conv2DTranspose(128, (3, 3), strides=(
        2, 2), padding='same', use_bias=False)(x)
    x = BatchNormalization()(x)
    x = LeakyReLU()(x)
    x = Conv2DTranspose(64, (5, 5), strides=(
        2, 2), padding='same', use_bias=False)(x)
    x = BatchNormalization()(x)
    x = LeakyReLU()(x)
    x = Conv2DTranspose(32, (7, 7), strides=(
        2, 2), padding='same', use_bias=False)(x)
    x = BatchNormalization()(x)
    x = LeakyReLU()(x)
    x = Conv2DTranspose(16, (9, 9), strides=(
        2, 2), padding='same', use_bias=False)(x)
    x = BatchNormalization()(x)
    x = LeakyReLU()(x)
    x = Conv2DTranspose(1, (11, 11), strides=(
        2, 2), padding='same', use_bias=False, activation='tanh')(x)
    model = Model(inputs=input_1, outputs=x)

    return model


def generate_and_save_images():
    generator = make_generator_model()
    generator.load_weights('saved_weights/generator_weights.h5')

    input_image = tf.random.normal([1, 100])

    predictions = generator(input_image, training=False)
    plt.figure(figsize=(12, 12))
    plt.imshow(predictions[0, :, :, 0] * 127.5 + 127.5, cmap='gray')
    plt.axis('off')

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'static/generated_image_{timestamp}.png'

    os.makedirs(os.path.dirname(filename), exist_ok=True)
    plt.savefig(filename, bbox_inches='tight', pad_inches=0)
    plt.close()

    print(f"Image saved at: {filename}")

    return filename
