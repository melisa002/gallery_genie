<<<<<<< HEAD
from gallery.data import fetching_data, drop_nulls,filter_data,sample_images,save_to_dir, check_and_remove_invalid_images, clean_faulty_images
from gallery.train import image_gen, create_model, train_model, compile_model
=======
from gallery.data import fetching_data, drop_nulls,filter_data,sample_images,save_to_dir, check_and_remove_invalid_images
from gallery.train import image_gen, create_model, train_model, compile_model, load_and_preprocess_image, extract_features, compare_images, find_most_similar_image
>>>>>>> 970cb2faf88be19f1a06c7b9f28ece8510709df7
from google.cloud import storage
from gallery.params import *
from gallery.registry import load_model

def run():
    dataset_dir = os.path.join(os.path.expanduser(LOCAL_DATA_PATH),'train')
    val_dir = os.path.join(os.path.expanduser(LOCAL_DATA_PATH),'validation')
    if not os.path.exists(dataset_dir):
        print("Started fetching the data")
        initial_data = fetching_data()
        no_null_data = drop_nulls(initial_data)
        filtered_data, movements = filter_data(no_null_data)
        sampled_images = sample_images(filtered_data,movements)
        sampled_images.apply(save_to_dir, axis=1)
        # Set the path to the directory containing your image dataset

        # Check and remove empty or invalid images
    check_and_remove_invalid_images(dataset_dir)
    check_and_remove_invalid_images(val_dir)
<<<<<<< HEAD
    clean_faulty_images()
=======

>>>>>>> 970cb2faf88be19f1a06c7b9f28ece8510709df7
    dataset = image_gen(dataset_dir,BATCH_SIZE,IMG_HEIGHT,IMG_WIDTH)
    val_dataset = image_gen(val_dir,BATCH_SIZE,IMG_HEIGHT,IMG_WIDTH)



    client = storage.Client(project=PROJECT_NAME)
    bucket = client.bucket(BUCKET_NAME)
    blobs = bucket.list_blobs(prefix="model")
    number=len([each for each in blobs if 'h5' in each.name])
    if number > 0:
        model = load_model()
        print("Model Loaded")
    else:
        model = create_model()
        print("Model Created")
    model = compile_model(model)
    trained_model = train_model(model,dataset,val_dataset)
    return trained_model

<<<<<<< HEAD
def load_model_weights():
    model = create_model()
    model1= compile_model(model)
    mod = model1.load_weights('/Users/franciscocarassus/code/melisa002/models/models_20240612-141510.weights.h5')
    return mod
=======
#def reccommend():
    #img_array = load_and_preprocess_image()

>>>>>>> 970cb2faf88be19f1a06c7b9f28ece8510709df7

if __name__ == '__main__':
    run()
