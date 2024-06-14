from gallery.params import *
import numpy as np
from PIL import Image
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances
from keras.models import load_model

def fetch_paths():
    paths_to_images = []
    base_path = PATH_TO_TRAIN
    for folder in os.listdir(base_path):
        for image_ in os.listdir(os.path.join(base_path, folder)):
            paths_to_images.append(os.path.join(base_path, folder, image_))
    return paths_to_images



def extract_features(img_array, model):
    print("Start extracting")
    #features_list = []
    #for img_array in img_list:

    features = model(img_array)
    #features_list.append(features.flatten())
    return features

def compute_similarity_new_image(features_dataset, features_new_image):
    breakpoint()

    # Convert to numpy arrays for similarity computation
    features_dataset_numpy = features_dataset.vector.to_numpy()
    features_new_image = features_new_image.numpy()

    # Compute cosine similarity
    similarity_scores = cosine_similarity(features_dataset_numpy, features_new_image)
    return similarity_scores

def find_most_similar_new_image(similarity_scores, top_n=5):
    most_similar_indices = np.argsort(similarity_scores[:, 0])[::-1][:top_n]
    return most_similar_indices

def compare_images(im_arr,df,model):

    features1 = extract_features(im_arr, model)[0]
    # cosines = []
    # euclids = []


    # for vec in df['vector']:
    #     cosine_sim = cosine_similarity([features1], [vec])[0][0]
    #     euclidean_dist = euclidean_distances([features1], [vec])[0][0]
    #     cosines.append(cosine_sim)
    #     euclids.append(euclidean_dist)

    # df['cosine_similarity'] = cosines
    # df['euclidean_distance'] = euclids
    similarity_scores = compute_similarity_new_image(df, features1)

    top_images = find_most_similar_new_image(similarity_scores, top_n=5)

    return top_images

def find_most_similar_image(target_img_path, df, model):

    comparison_df = compare_images(target_img_path, df, model)
    most_similar_cosine = comparison_df.loc[comparison_df['cosine_similarity'].idxmax()]

    return most_similar_cosine['path']
