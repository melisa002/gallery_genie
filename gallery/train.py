from gallery.registry import save_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.utils import image_dataset_from_directory
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from gallery.params import *
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.models import Model
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances
import os



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
    model.add(Dense(30, activation='softmax'))  # Single neuron for regression output
    return model

def compile_model(model):
    model.compile(optimizer='adam', loss='mae')
    return model

def train_model(model,dataset,dataset_val):
    train_dataset = dataset.batch(BATCH_SIZE)
    validation_dataset = dataset_val.batch(BATCH_SIZE)
    model.fit(train_dataset,validation_data=validation_dataset, epochs=1)
    save_model(model)
    return model

def extract_features(img_array, model):
    features = model.predict(img_array)
    return features

base_model = VGG16(weights='imagenet')
model = Model(inputs=base_model.input, outputs=base_model.get_layer('fc1').output)

#model predict the layer - output is vector
#vector vs vector
#save vectors into df , compare df.apply
#df['embedding'] = [model.predict()]
# we get class impres
# similiraity_to_each_image_in_df = df.loc[df.category== 'impres']['embedding'].apply(lambda x: x @ embedded_input_from_user)
# we want to get the first one which has sim <0.8


def compare_images(img_path1, img_path2, model):
    features1 = extract_features(img_path1, model)
    features2 = extract_features(img_path2, model)

    cosine_sim = cosine_similarity(features1, features2)[0][0]
    euclidean_dist = euclidean_distances(features1, features2)[0][0]

    return cosine_sim, euclidean_dist

def find_most_similar_image(imagearr, folder_path, model):
    target_features = extract_features(imagearr, model)
    most_similar_img = None
    highest_cosine_similarity = -1
    lowest_euclidean_distance = float('inf')

    for img_name in os.listdir(folder_path):
        img_path = os.path.join(folder_path, img_name)
        if os.path.isfile(img_path):
            features = extract_features(img_path, model)

            cosine_sim = cosine_similarity(target_features, features)[0][0]
            euclidean_dist = euclidean_distances(target_features, features)[0][0]

            if cosine_sim > highest_cosine_similarity:
                highest_cosine_similarity = cosine_sim
                most_similar_img = img_path

            if euclidean_dist < lowest_euclidean_distance:
                lowest_euclidean_distance = euclidean_dist
                most_similar_img = img_path

    return most_similar_img, highest_cosine_similarity, lowest_euclidean_distance

img_path1 = '/Users/poloniki/code/melisa_project/gallery_genie/data/data/art/train/abstract_expressionism/10stones19891jpglarge.jpg'
img_path2 = '/Users/poloniki/code/melisa_project/gallery_genie/data/data/art/train/abstract_expressionism/11stones19891.jpg'

cosine_sim, euclidean_dist = compare_images(img_path1, img_path2, model)
