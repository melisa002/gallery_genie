from tensorflow import keras
import keras
import os
import time
from google.cloud import storage
from gallery.params import *

def save_model(model:keras.Model = None) -> None:
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    os.makedirs(os.path.join(MODEL_REGISTRY,'models'))

    model_path = os.path.join(MODEL_REGISTRY,'models',f"{timestamp}.h5")
    model.save_weights(model_path)

    if MODEL_TARGET == "gcs":
        model_filename = model_path.split("/")[-1]
        client = storage.Client()
        bucket = client.bucket(BUCKET_NAME)
        blob = bucket.blob(f"models/{model_filename}")
        blob.upload_from_filename(model_path)

        print("Model saved to GCS")
        return None
    return None

def load_model() -> keras.Model:

    print("\nLoad latest model GCS ...")
    client = storage.Client()
    blobs = list(client.get_bucket(BUCKET_NAME).list_blobs(prefix="model"))

    try:
        latest_blob = max(blobs, key=lambda x: x.updated)
        latest_model_path_to_save = os.path.join(MODEL_REGISTRY,latest_blob.name)
        latest_blob.download_to_filename(latest_model_path_to_save)

        latest_model = keras.models.load_model(latest_model_path_to_save)
        print("Latest model loaded")
        return latest_model
    except:
        print(f"\n No model found in GCS bucket {BUCKET_NAME} ")
        return None
