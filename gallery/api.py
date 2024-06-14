from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from ultralytics import YOLO
import numpy as np
import cv2
from gallery.params import *
from gallery.stuff import find_most_similar_image
from tensorflow.keras.layers import GlobalAveragePooling2D
from tensorflow.keras.models import load_model, Model

import pandas as pd
import faiss
import numpy as np


def load_faiss_index(index_path):
    index = faiss.read_index(index_path)
    return index


# Path to the FAISS index file
index_path = "gallery/faiss_index.bin"
model_path = "gallery/models_20240613-101029.keras"
meta_path = "gallery/meta.csv"

new_model = load_model(model_path)
vgg16 = new_model.get_layer("vgg16")
input_layer = vgg16.input
block5 = vgg16.get_layer("block5_pool").output
pooled_output = GlobalAveragePooling2D()(block5)


app = FastAPI()
app.state.model = YOLO("gallery/best-87810.pt")
app.state.francisco_model = Model(inputs=input_layer, outputs=pooled_output)
app.state.faiss_index = load_faiss_index(index_path)
app.state.meta = pd.read_csv(meta_path)


def extract_single_image_feature(image_array, feature_extractor):
    try:
        img_array = np.expand_dims(image_array, axis=0)
        feature = feature_extractor.predict(img_array, verbose=0)
        return feature.flatten()
    except Exception as e:
        print(f"Error extracting features: {e}")
        return None


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def index():
    return {"status": "ok"}


@app.post("/upload_image")
async def receive_image(img: UploadFile = File(...)):
    contents = await img.read()

    nparr = np.fromstring(contents, np.uint8)
    cv2_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    model = app.state.model
    prediction = model(cv2_img, imgsz=512)
    class_label = prediction[0].probs.top1
    names = prediction[0].names
    pred_label = names[class_label]
    class_labels = prediction[0].probs.top5
    top_5_names = [names[each] for each in class_labels]

    # Recommendation
    francisco_model = app.state.francisco_model
    cv2_256 = cv2.resize(cv2_img, (256, 256))

    user_image_features = extract_single_image_feature(cv2_256, francisco_model)
    user_image_features = np.expand_dims(user_image_features, axis=0)
    faiss_index = app.state.faiss_index
    k = 50
    distances, indices = faiss_index.search(user_image_features, k)
    print(indices)
    # Unpack recommendations
    meta_df = app.state.meta

    top_images = meta_df.loc[meta_df.index.isin(indices[0])]
    top_images["distances"] = distances[0]

    #top_images = top_images.loc[top_images["style"].isin(top_5_names)].head()

    return {
        "pred_label": pred_label,
        "top_5_names": top_5_names,
        "most_similar": top_images.to_dict(orient="records"),
    }
