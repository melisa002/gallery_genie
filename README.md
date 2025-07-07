# 🎨 Gallery Genie - AI Art Classifier & Recommendation System

An intelligent art classification and recommendation system that combines computer vision and similarity search to help users discover artworks. Built with a fine-tuned VGG16 model and FAISS vector search on a massive 500k artwork dataset.

## Features

### Art Classification
- **Style Recognition**: Classifies artwork into different artistic styles and movements
- **Top-5 Predictions**: Returns the 5 most likely style classifications with confidence scores
- **Real-time Processing**: Fast inference using optimized YOLO and VGG models

### Smart Recommendations
- **Visual Similarity**: Finds artworks visually similar to uploaded images
- **Feature Extraction**: Uses VGG16 block5_pool features with Global Average Pooling
- **FAISS Search**: Lightning-fast similarity search across 500k+ artworks
- **Style Filtering**: Recommends artworks from similar artistic styles

### Performance
- **Scalable**: Handles large-scale artwork databases efficiently
- **Fast API**: RESTful API built with FastAPI for production deployment
- **Optimized Models**: Custom VGG16 architecture fine-tuned for art classification

## Architecture

### Models Used
- **Classification**: Custom YOLO model fine-tuned on artwork dataset
- **Feature Extraction**: Modified VGG16 with Global Average Pooling
- **Similarity Search**: FAISS index for efficient nearest neighbor search

### Data Pipeline
1. **Image Upload**: Users upload artwork images via API
2. **Classification**: YOLO model predicts artistic style
3. **Feature Extraction**: VGG16 extracts visual features
4. **Similarity Search**: FAISS finds most similar artworks
5. **Recommendations**: Returns curated list of similar artworks

## Installation

### Requirements
- Python 3.8+
- FastAPI
- TensorFlow/Keras
- OpenCV
- FAISS
- Ultralytics YOLO
- pandas, numpy

### Setup
Install required packages and download the pre-trained models:
- YOLO classification model: best-87810.pt
- VGG16 feature extractor: models_20240613-101029.keras
- FAISS similarity index: faiss_index.bin
- Metadata: meta.csv

## API Endpoints
- Used OpenAI api to fetch information about all of the art pieces, year of creation, author, and meaning behind.
- Used Streamlit API to host the website.

### POST /upload_image
Upload an artwork image for classification and recommendations.

**Request**: Multipart form data with image file

**Response**:
- pred_label: Primary style classification
- top_5_names: Top 5 style predictions
- most_similar: List of similar artworks with metadata and distances

### GET /
Health check endpoint returning system status.

## Dataset

Trained on a comprehensive 500k artwork dataset featuring:
- Multiple artistic styles and movements
- Diverse time periods and cultural backgrounds
- High-quality artwork images
- Rich metadata including artist, style, and period information

## Technical Details

### Feature Extraction
- Uses VGG16 block5_pool layer output
- Global Average Pooling for dimensionality reduction
- 512-dimensional feature vectors

### Similarity Search
- FAISS index for efficient nearest neighbor search
- Cosine similarity for artwork comparison
- Top-k retrieval with configurable k value

### Model Architecture
- Fine-tuned VGG16 backbone
- Custom classification head for art styles
- Optimized for both accuracy and inference speed

## Use Cases

- **Art Discovery**: Help users find new artworks similar to their preferences
- **Style Analysis**: Classify and categorize artwork collections
- **Museum Applications**: Digital art recommendation systems
- **Art Education**: Learn about different artistic styles and movements
- **Collection Management**: Organize and search large art databases

## Deployment

The system is production-ready with:
- FastAPI backend with CORS support
- Async image processing
- Scalable architecture
- RESTful API design

## Performance Metrics

- **Classification Accuracy**: High accuracy on art style recognition
- **Search Speed**: Sub-second similarity search on 500k+ database
- **Scalability**: Handles concurrent requests efficiently
- **Model Size**: Optimized for production deployment
