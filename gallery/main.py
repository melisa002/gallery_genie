from gallery.data import fetching_data, drop_nulls,filter_data,sample_images,save_to_dir, check_and_remove_invalid_images
from gallery.train import image_gen, create_model, train_model
from gallery.params import *

def run():

    dataset_dir = os.path.join(os.path.expanduser(LOCAL_DATA_PATH), 'small_data')
    if not os.path.exists(dataset_dir):
        initial_data = fetching_data()
        no_null_data = drop_nulls(initial_data)
        filtered_data, movements = filter_data(no_null_data)
        sampled_images = sample_images(filtered_data,movements)
        sampled_images.apply(save_to_dir, axis=1)
        # Set the path to the directory containing your image dataset
    else:
        # Check and remove empty or invalid images
        check_and_remove_invalid_images(dataset_dir)
        dataset = image_gen(dataset_dir,BATCH_SIZE,IMG_HEIGHT,IMG_WIDTH)
        model = create_model()
        trained_model = train_model(model,dataset)
    return trained_model
