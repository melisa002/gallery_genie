import os

MODEL_TARGET=os.environ.get("MODEL_TARGET")
PROJECT_NAME = os.environ.get("PROJECT_NAME")
BUCKET_NAME=os.environ.get("BUCKET_NAME")
BQ_REGION = os.environ.get("BQ_REGION")
PROJECT_REGION=os.environ.get("PROJECT_REGION")
TABLE1_NAME=os.environ.get("TABLE1_NAME")
NODE_NAME = os.environ.get("NODE_NAME")
REPO_NAME=os.environ.get("REPO_NAME")
GOOGLE_APPLICATION_CREDENTIALS=os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
IMG_HEIGHT=int(os.environ.get("IMG_HEIGHT"))
IMG_WIDTH=int(os.environ.get("IMG_WIDTH"))
BATCH_SIZE=int(os.environ.get("BATCH_SIZE"))
DATASET_DIR=os.environ.get("DATASET_DIR")
LOCAL_DATA_PATH = os.environ.get("LOCAL_DATA_PATH")
MODEL_REGISTRY =  os.environ.get("MODEL_REGISTRY")
COMET_WORKSPACE_NAME=os.environ.get("COMET_WORKSPACE_NAME")
COMET_MODEL_NAME=os.environ.get("MODEL_REGISTRY")
COMET_PROJECT_NAME=os.environ.get("COMET_PROJECT_NAME")
COMET_API_KEY = os.environ.get("COMET_API_KEY")


COLUMN_NAMES= [
    'author_name', 'painting_name', 'image_url', 'Genre', 'Style', 'Nationality',
    'Painting School', 'Art Movement', 'Field', 'Date', 'Influenced by', 'Media',
    'Influenced on', 'Family and Relatives', 'Tag', 'Pupils', 'Location',
    'Original Title', 'Dimensions', 'Series', 'Teachers', 'Friends and Co-workers',
    'Art institution', 'Period', 'Theme', 'Path'
    ]

DROPPED_COLUMNS= [
            'Theme', 'Period', 'Family and Relatives', 'Series', 'Pupils', 'Teachers',
            'Original Title', 'Dimensions', 'Friends and Co-workers',
            'Influenced by', 'Influenced on'
            ]
