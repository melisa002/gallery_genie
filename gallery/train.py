from gallery.registry import save_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.utils import image_dataset_from_directory
from tensorflow.keras.applications import VGG16
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from gallery.params import *


def image_gen(dataset_dir,batch_size,img_height,img_width):

# Create an instance of the ImageDataGenerator and define any desired transformations
    datagen = ImageDataGenerator(
        rescale=1./255,             # Optional: Scale pixel values to [0, 1]
        rotation_range=20,          # Optional: Random rotation in the range of [-20, 20] degrees
        width_shift_range=0.2,      # Optional: Random horizontal shift by 20% of the image width
        height_shift_range=0.2,     # Optional: Random vertical shift by 20% of the image height
        horizontal_flip=True        # Optional: Randomly flip images horizontally
    )


    # Use the ImageDataGenerator to load and augment the dataset
    dataset = image_dataset_from_directory(
        dataset_dir,
        batch_size=batch_size,
        image_size=(img_height, img_width),
        validation_split=0.2,      # Optional: Split the dataset into train and validation sets
        subset='training',         # Optional: Specify 'training' or 'validation' subset
        seed=123,                  # Optional: Set a seed for shuffling
        labels='inferred',         # Optional: Infer class labels automatically from subdirectories
        label_mode='categorical',  # Optional: Set label mode, e.g., 'binary', 'categorical', 'sparse'
        interpolation='bilinear',  # Optional: Specify the interpolation method for resizing images

    )
    return dataset

def create_model():
    base_model = VGG16(weights='imagenet', include_top=False, input_shape=(IMG_HEIGHT,IMG_WIDTH,3))
    # Freeze the layers of the base model
    for layer in base_model.layers:
        layer.trainable = False
    # Create a sequential model and add the VGG16 model
    model = Sequential()
    model.add(base_model)
    # Add the custom layers on top
    model.add(Flatten())
    model.add(Dense(16, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(8, activation='relu'))
    # Output layer for count prediction
    # TODO pick top 30 to classify based on , increase sample samplesize.
    """, """
    model.add(Dense(30, activation='softmax'))  # Single neuron for regression output
    return model

def compile_model(model):
    model.compile(optimizer='adam', loss='mae')
    return model

def train_model(model,dataset,dataset_val):
    train_dataset = dataset.batch(BATCH_SIZE)
    validation_dataset = dataset_val.batch(BATCH_SIZE)
    model.fit(train_dataset,validation_data=validation_dataset, epochs=3)
    save_model(model)
    return model
