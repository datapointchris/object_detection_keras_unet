import keras
from keras.layers import Conv2D, Conv2DTranspose, Dropout, MaxPooling2D, concatenate


def make_model(inputs: keras.layers.Input, name: str = None) -> keras.models.Model:

    common_params = dict(activation='elu', kernel_initializer='he_normal', padding='same')

    c1 = Conv2D(16, (3, 3), input_shape=inputs.shape[1:], **common_params)(inputs)
    c1 = Dropout(0.1)(c1)
    c1 = Conv2D(16, (3, 3), **common_params)(c1)
    p1 = MaxPooling2D((2, 2))(c1)

    c2 = Conv2D(32, (3, 3), **common_params)(p1)
    c2 = Dropout(0.1)(c2)
    c2 = Conv2D(32, (3, 3), **common_params)(c2)
    p2 = MaxPooling2D((2, 2))(c2)

    c3 = Conv2D(64, (3, 3), **common_params)(p2)
    c3 = Dropout(0.2)(c3)
    c3 = Conv2D(64, (3, 3), **common_params)(c3)
    p3 = MaxPooling2D((2, 2))(c3)

    c4 = Conv2D(128, (3, 3), **common_params)(p3)
    c4 = Dropout(0.2)(c4)
    c4 = Conv2D(128, (3, 3), **common_params)(c4)
    p4 = MaxPooling2D(pool_size=(2, 2))(c4)

    c5 = Conv2D(256, (3, 3), **common_params)(p4)
    c5 = Dropout(0.3)(c5)
    c5 = Conv2D(256, (3, 3), **common_params)(c5)

    u6 = Conv2DTranspose(128, (2, 2), strides=(2, 2), padding='same')(c5)
    u6 = concatenate([u6, c4])
    c6 = Conv2D(128, (3, 3), **common_params)(u6)
    c6 = Dropout(0.2)(c6)
    c6 = Conv2D(128, (3, 3), **common_params)(c6)

    u7 = Conv2DTranspose(64, (2, 2), strides=(2, 2), padding='same')(c6)
    u7 = concatenate([u7, c3])
    c7 = Conv2D(64, (3, 3), **common_params)(u7)
    c7 = Dropout(0.2)(c7)
    c7 = Conv2D(64, (3, 3), **common_params)(c7)

    u8 = Conv2DTranspose(32, (2, 2), strides=(2, 2), padding='same')(c7)
    u8 = concatenate([u8, c2])
    c8 = Conv2D(32, (3, 3), **common_params)(u8)
    c8 = Dropout(0.1)(c8)
    c8 = Conv2D(32, (3, 3), **common_params)(c8)

    u9 = Conv2DTranspose(16, (2, 2), strides=(2, 2), padding='same')(c8)
    u9 = concatenate([u9, c1], axis=3)
    c9 = Conv2D(16, (3, 3), **common_params)(u9)
    c9 = Dropout(0.1)(c9)
    c9 = Conv2D(16, (3, 3), **common_params)(c9)

    outputs = Conv2D(1, (1, 1), activation='sigmoid')(c9)

    return keras.models.Model(name=name, inputs=inputs, outputs=outputs)
