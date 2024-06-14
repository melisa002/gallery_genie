create_data_folder:
	@mkdir ~/data/data

run_all:
	python -c 'from gallery.main import run; run()'


load:
	python -c 'from gallery.main import load_model_weights; load_model_weights()'
