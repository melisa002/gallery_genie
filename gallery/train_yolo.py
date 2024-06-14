from ultralytics import YOLO
import os
import comet_ml
from comet_ml import API

# FIXME Change the import to gallery!
from gallery.params import *


def train_model(epochs: int = 10, img_size: int = 256):
    # Initialize Comet ML API connection
    # FIXME inster the api key
    comet_ml.init(api_key=COMET_API_KEY)
    api = API(api_key=COMET_API_KEY)

    model = None
    weights_path = os.path.join(LOCAL_DATA_PATH, "weights", "best.pt")

    # Try to use pretrained weights if available
    try:
        # Fetching the model from Comet ML
        models = api.get_model(
            workspace=COMET_WORKSPACE_NAME, model_name=COMET_MODEL_NAME
        )
        # Get production model weights
        model_versions = models.find_versions(status="Production")
        latest_production_weights = model_versions[0]

        # Downloading the weights
        os.makedirs(os.path.dirname(weights_path), exist_ok=True)
        models.download(
            version=latest_production_weights,
            output_folder=os.path.dirname(weights_path),
            expand=True,
        )

        # Load the model with the downloaded weights
        model = YOLO(weights_path)
        print("✅ Loaded weights from Comet ML")
    except Exception as error:
        print(f"❌ Could not load weights: {error}")

    # If loading pretrained weights fails, initialize a new model
    if not model:
        model = YOLO("yolov8n-cls.pt")
        print("🆕 Starting training with new model")

    # Train the model
    model.train(
        batch= BATCH_SIZE,
        data=LOCAL_DATA_PATH,
        epochs=epochs,
        imgsz=IMG_HEIGHT,
        patience=20,
        #device='mps' #
    )

    # Save the trained model weights to Comet ML
    experiments = api.get(
        workspace=COMET_WORKSPACE_NAME, project_name=COMET_PROJECT_NAME
    )
    current_experiment = experiments[-1]._name
    experiment = api.get(
        workspace=COMET_WORKSPACE_NAME,
        project_name=COMET_PROJECT_NAME,
        experiment=current_experiment,
    )

    # Sort list of experiments by one of the metrics to find the best one
    experiments.sort(
        key=lambda each_experiment: (
            float(each_experiment.get_metrics_summary("metrics/accuracy")["valueMax"])
            if isinstance(each_experiment.get_metrics_summary("metrics/accuracy"), dict)
            else 0
        )
    )

    # Get best experiment
    best_experiment_so_far = experiments[-1]._name

    # If current one is the best, move this model to production
    if current_experiment == best_experiment_so_far:
        experiment.register_model(COMET_MODEL_NAME, status="Production")
        print("✅ Registered current model as Production")
    else:
        experiment.register_model(COMET_MODEL_NAME)
        print("🖌️ Registered current model as history")


# Main execution
if __name__ == "__main__":
    train_model(epochs=100)
