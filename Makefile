create_data_folder:
	@mkdir ~/data/data

run_all:
	python -c 'from gallery.main import run; run()'
