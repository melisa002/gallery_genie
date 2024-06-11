<<<<<<< HEAD
#FROM python:3.10-buster
FROM ultralytics/ultralytics:latest
=======
FROM python:3.10-buster
>>>>>>> 05dbe082355522629d90ee34174ac562cc96976f
COPY setup.py setup.py
COPY requirements.txt requirements.txt
RUN apt-get update && apt-get install -y libhdf5-dev
#RUN pip install --no-binary h5py h5py
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install -e .
COPY data data
COPY gallery gallery/
COPY gcp gcp/
CMD python gallery/main.py
