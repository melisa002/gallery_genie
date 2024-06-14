<<<<<<< HEAD
=======
#FROM python:3.10-buster
#FROM ultralytics/ultralytics:latest
#COPY setup.py setup.py
#COPY requirements.txt requirements.txt
#RUN apt-get update && apt-get install -y libhdf5-dev
#RUN pip install --no-binary h5py h5py
#RUN pip install --upgrade pip
#RUN pip install -r requirements.txt
#RUN pip install -e .
#COPY data data
#COPY gallery gallery/
#COPY gcp gcp/
#CMD python gallery/train_yolo.py

>>>>>>> 970cb2faf88be19f1a06c7b9f28ece8510709df7
FROM python:3.10
RUN apt-get update
RUN apt-get install \
  'ffmpeg'\
  'libsm6'\
  'libxext6'  -y
COPY gallery gallery
COPY data data
COPY gcp gcp
COPY requirements.ultralytics.txt requirements.txt
RUN pip install -U pip
RUN pip install -r requirements.txt
COPY setup.py setup.py
RUN pip install -e .
CMD python gallery/train_yolo.py
