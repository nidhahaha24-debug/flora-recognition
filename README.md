# 🌿 Flora Recognition

### AI-Powered Crop Leaf Disease Detection System

Flora Recognition is an AI-powered crop leaf disease detection system that uses deep learning and computer vision to identify crop types and detect common leaf diseases from leaf images.

The system allows users to upload a crop leaf image and receive an AI-generated prediction with confidence, plant health insights, symptoms, and recommended management actions.

---

## 🌱 Project Overview

Agricultural crop diseases can significantly affect crop productivity. Early identification of diseases can help farmers take appropriate preventive and management actions.

Flora Recognition provides a simple image-based approach where:

**Leaf Image → Image Processing → MobileNetV2 → Disease Prediction → Health Insights**

The system is designed with a farmer-friendly interface and supports multiple crop and disease categories.

---

## ✨ Features

- 🌿 Crop and disease recognition from leaf images
- 🤖 Deep learning-based image classification
- 📚 38 predefined crop/disease classes
- 📊 Prediction confidence score
- ❤️ Plant health indicator
- 🩺 Disease symptoms
- 🌱 Prevention and management guidance
- ⚡ Lightweight MobileNetV2 architecture
- 📱 Mobile-friendly Streamlit interface
- 🎨 Interactive and modern UI
- 🚀 Fast model inference

---

## 🧠 Machine Learning Model

The project uses **MobileNetV2**, a lightweight convolutional neural network architecture pretrained on ImageNet.

### Model Architecture

```text
Input Image
    ↓
224 × 224 × 3
    ↓
MobileNetV2
    ↓
Global Average Pooling
    ↓
Dropout
    ↓
Dense Layer
    ↓
Softmax
    ↓
38 Crop/Disease Classes





| Parameter      | Value                           |
| -------------- | ------------------------------- |
| Architecture   | MobileNetV2                     |
| Input Size     | 224 × 224                       |
| Output Classes | 38                              |
| Optimizer      | Adam                            |
| Loss Function  | Sparse Categorical Crossentropy |
| Activation     | Softmax                         |
| Batch Size     | 16                              |








📚 Dataset

The model was developed using the PlantVillage dataset, containing crop leaf images covering multiple crop species and disease categories.

The dataset used in this project contains:

54,304 images
38 crop/disease categories

The model was trained and evaluated using a stratified subset of the dataset.

Dataset Split
Dataset	Images
Training	12,000
Validation	3,000
Testing	3,000

The test images were kept separate from the training data and used to evaluate model performance.

📊 Model Performance

The trained model was evaluated on 3,000 unseen test images.

Metric	Result
Test Accuracy	91.53%
Weighted Precision	91.88%
Weighted Recall	91.53%
Weighted F1-Score	91.41%
Test Loss	0.3171
Average Model Inference Time	89.93 ms/image

A 38 × 38 confusion matrix was also generated to analyze classification performance across all classes.

Performance Interpretation

The strong concentration of predictions along the diagonal of the confusion matrix indicates that the model correctly classified a large proportion of the test images.

Some misclassifications occur between visually similar crop disease categories.

🌾 Supported Crop/Disease Categories

The model supports 38 predefined categories including:

Apple
Blueberry
Cherry
Corn
Grape
Orange
Peach
Pepper
Potato
Raspberry
Soybean
Squash
Strawberry
Tomato

The categories include both healthy and diseased leaf conditions.

🛠️ Technologies Used
Programming
Python
Machine Learning
TensorFlow
Keras
MobileNetV2
NumPy
Scikit-learn
Dataset
Hugging Face Datasets
PlantVillage dataset
Web Application
Streamlit
HTML
CSS
Development Environment
Google Colab
GitHub
Deployment
Streamlit Community Cloud
🔄 System Workflow
User
 │
 ▼
Upload / Capture Leaf Image
 │
 ▼
Image Preprocessing
 │
 ├── Convert to RGB
 ├── Resize to 224 × 224
 └── MobileNetV2 preprocessing
 │
 ▼
MobileNetV2 Model
 │
 ▼
38-Class Prediction
 │
 ▼
Crop + Disease + Confidence
 │
 ▼
Plant Health Insights
 │
 ▼
Farmer Action Plan
📓 Google Colab Notebook

The complete machine learning workflow, including dataset loading, preprocessing, model training, evaluation, testing, and prediction, is available in the notebook:

📓 View the Complete Colab Notebook

Open Directly in Google Colab

🌐 Live Application

Flora Recognition Web Application:

https://flora-recognition-nidha-hussain-naheen-tasmiya.streamlit.app/

The application provides an interactive interface where users can upload leaf images and obtain model predictions.

Note: The free Streamlit deployment may go to sleep after periods of inactivity. If this happens, use the wake-up option provided by Streamlit.

📁 Project Structure
flora-recognition/
│
├── app.py
├── agricare_model.keras
├── class_names.json
├── requirements.txt
├── AgriCare_AI_Model.ipynb
└── README.md


⚙️ Running the Project Locally
1. Clone the repository
git clone https://github.com/nidhahaha24-debug/flora-recognition.git
2. Open the project
cd flora-recognition
3. Install dependencies
pip install -r requirements.txt
4. Run the Streamlit application
streamlit run app.py

The application will then open in your browser.

⚠️ Important Note

Flora Recognition is an academic/student machine-learning project.

The model is trained and evaluated on PlantVillage-style leaf images. Real-world farm images can contain different lighting, backgrounds, camera conditions, leaf orientations, and disease appearances.

Therefore, predictions should be treated as AI-assisted identification, not as a replacement for professional agricultural diagnosis.

The health score displayed by the application is a presentation-oriented indicator and is not a scientifically validated measurement of actual plant disease severity.

🚀 Future Improvements

Possible future improvements include:

📸 Real-time camera-based detection
🌾 Additional crop and disease categories
🌍 Regional/local crop disease datasets
🔬 Larger and more diverse training datasets
📱 Dedicated Android/iOS application
🌐 Multi-language support for farmers
🗺️ Location-aware agricultural guidance
☁️ Cloud-based model optimization
📈 Disease monitoring over time
👩‍💻 Project Author

Nidha Hussain

B.E. Computer Science & Engineering
T. John Institute of Technology, Bengaluru

Expected Graduation: May 2027

📜 Disclaimer

This project is developed for educational and academic purposes.

The predictions generated by the system are based on a machine-learning classification model and should not be considered professional agricultural advice.
