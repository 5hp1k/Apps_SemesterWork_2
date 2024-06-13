import matplotlib.pyplot as plt
import tensorflow as tf
import tensorflow as tf
from tensorflow.keras.layers import Input, BatchNormalization, Reshape, Dense, LeakyReLU, Conv2DTranspose
from tensorflow.keras.models import Model


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


generator = make_generator_model()

generator.load_weights('saved_weights/generator_weights.h5')


def generate_and_save_images(model, test_input):
    predictions = model(test_input, training=False)
    plt.figure(figsize=(12, 12))
    plt.imshow(predictions[0, :, :, 0] * 127.5 + 127.5, cmap='gray')
    plt.axis('off')
    plt.savefig('results/generated_image.png',
                bbox_inches='tight', pad_inches=0)
    plt.show()


noise = tf.random.normal([1, 100])

generate_and_save_images(generator, noise)
