from google.cloud import bigquery
import pandas as pd
import os
from PIL import Image
from io import BytesIO
import requests
from gallery.params import *

def fetching_data():
    client = bigquery.Client(project=PROJECT_NAME)
    full_table_name = f"{PROJECT_NAME}.{NODE_NAME}.{TABLE1_NAME}"
    query = f"SELECT * FROM {full_table_name} WHERE LOWER(Field) LIKE '%painting%'"
    response = client.query(query)
    uncleaned_data = response.result().to_dataframe()
    return uncleaned_data

def drop_nulls(uncleaned_data):
    uncleaned_data.dropna(subset=['Genre'], inplace=True)
    uncleaned_data.drop(DROPPED_COLUMNS,axis=1,inplace=True)
    return uncleaned_data

def filter_data(data):
    value_counts = data['Style'].value_counts()
    mask = value_counts < 100
    filtered_movements = value_counts[mask].index.tolist()

    filtered_data = data[data['Style'].isin(filtered_movements)]
    filtered_data = data[~data['Style'].isin(filtered_movements)]

    movements = filtered_data['Style'].value_counts().index.tolist()
    movements = [movement for movement in movements if ',' not in movement]

    return filtered_data, movements

def sample_images(filtered_data, movements):
    imp_list = []
    movements = movements[:30]
    for movement in movements:
        if ',' not in movement:
            imp = filtered_data[filtered_data['Style']== movement]
            imp_sampled = imp.sample(n=100, random_state=1)
            imp_list.append(imp_sampled)
    full_df = pd.concat(imp_list, ignore_index=True)
    return full_df


def is_image_valid(image_path):
    try:
        img = Image.open(image_path)
        img.verify()  # Verify that it is an image
        img.close()   # Close the image to avoid resource leaks

        # Reopen the image to ensure it can be read
        img = Image.open(image_path)
        img.load()    # Ensure the image can be fully loaded
        img.close()
        return True
    except (IOError, SyntaxError, OSError) as e:
        return False

def check_and_remove_invalid_images(base_dir):
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            file_path = os.path.join(root, file)
            if not is_image_valid(file_path):
                print(f"Removing invalid image: {file_path}")
                os.remove(file_path)


def save_to_dir(full_df):
    try:
        movement = full_df["Style"]
        url = full_df["image_url"]
        response = requests.get(url)
        if response.status_code == 200:
            save_dir = os.path.join(
                os.path.expanduser(LOCAL_DATA_PATH),
                "small_data",
                movement,
            )
            os.makedirs(save_dir, exist_ok=True)
            image_data = BytesIO(response.content)
            img = Image.open(image_data)
            img.save(os.path.join(save_dir, os.path.basename(url)))
    except Exception as e:
        print(f"Exception occurred while processing URL {url}: {e}")
