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
