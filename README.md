\# ❤️ Cardiovascular Disease \& ECG Analysis System



\## 📌 Project Overview



This project is an AI-powered healthcare system designed to predict cardiovascular disease risk and analyze ECG signals. It combines machine learning and deep learning techniques to provide accurate and efficient heart condition assessment.



The system supports:



\* Clinical data-based cardiovascular prediction

\* ECG image-based disease classification



\---



\## 🚀 Features



\* ❤️ Cardiovascular Disease Prediction using clinical data

\* 🫀 ECG Image Analysis and Signal Processing

\* 📊 Dimensionality Reduction using PCA

\* 🤖 Machine Learning Models: Random Forest, XGBoost, KNN

\* 🧠 Deep Learning Model: ResNet50 for ECG image classification

\* 🌐 Interactive UI built using Streamlit



\---



\## 🛠️ Technologies Used



\* Python

\* Streamlit

\* Scikit-learn

\* NumPy, Pandas

\* Matplotlib

\* Scikit-image

\* Joblib



\---



\## 🧠 Machine Learning Workflow



1\. ECG Image Upload

2\. Image Preprocessing (Grayscale, Thresholding)

3\. Lead Segmentation (12-lead ECG extraction)

4\. Signal Extraction \& Scaling

5\. Feature Reduction using PCA

6\. Prediction using trained ML models



\---



\## 📂 Project Structure



```

Cardio-Project/

│

├── ML/                          # ML model logic

├── model\_pkl/                   # Saved ML models

├── PCA\_ECG (1).pkl             # PCA model

├── Heart\_Disease\_Prediction... # Trained classifier

├── Ecg.py                      # ECG processing module

├── cardio\_prediction.py        # Cardio prediction logic

├── app.py                      # Main Streamlit app

├── README.md

└── requirements.txt

```



\---



\## ▶️ How to Run the Project



\### 1️⃣ Clone the repository



```

git clone https://github.com/yourusername/Cardio-Project.git

cd Cardio-Project

```



\### 2️⃣ Install dependencies



```

pip install -r requirements.txt

```



\### 3️⃣ Run the application



```

streamlit run app.py

```



\---



\## 📊 Dataset



The dataset used for training is not included in this repository due to size limitations.



👉 You can use:



\* Public cardiovascular datasets (Kaggle/UCI)

\* ECG image datasets for training



\---



\## 📸 Output



\* Displays ECG preprocessing steps

\* Shows extracted signal data

\* Predicts heart condition:



&#x20; \* Normal

&#x20; \* Abnormal Heartbeat

&#x20; \* Myocardial Infarction



\---



\## ⚠️ Limitations



\* Depends on quality of ECG image

\* Dataset not included

\* Not a replacement for medical diagnosis



\---



\## 🔮 Future Enhancements



\* Real-time ECG monitoring

\* Cloud deployment

\* Integration with wearable devices

\* Improved deep learning models



\---



\## 👨‍💻 Author



Nabil



\---



\## 📢 Disclaimer



This project is for educational and research purposes only. It should not be used for real medical diagnosis without professional consultation.



