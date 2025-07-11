# 🧠 AI-Powered Advanced Fake News Detection Chrome Extension

A real-time, multi-modal fake news detection system that combines **Natural Language Processing (BERT)** and **Computer Vision (ResNet50)** to classify misinformation from both **text** and **image** sources. The backend is built with **FastAPI**, and the interface is delivered via a **Chrome extension**, enabling users to detect and classify content while browsing.

---

## 🚀 Key Features

- 🔍 **Multimodal Detection**: Combines image and text analysis for more reliable detection.
- 🧠 **Custom-Trained Model**: Built on 50K+ curated samples from the Fakeddit dataset.
- ⚙️ **FastAPI Backend**: Lightweight and efficient REST API for inference.
- 🌐 **Chrome Extension**: Seamlessly integrated user interface for live misinformation detection.
- 📊 **6-Way Classification**: Detects not only fake or real but also various types of misleading content.

---

## 📦 Dataset: Fakeddit

> A fine-grained, multi-modal dataset designed to support the classification of misleading online content across text and image modalities.

### 🎯 Classification Labels
1. ✅ True / Authentic
2. 🎭 Satire / Parody
3. 🔗 False Connection
4. 🕵️ Imposter Content
5. ✂️ Manipulated Content
6. 🎯 Misleading Content

Only the 6-way classification was used; 2-way and 3-way labels were excluded.

---

## 🧠 Model Architecture

### 📝 Text Model — BERT
- Model: `bert-base-uncased`
- Pretrained on: Wikipedia + Toronto Book Corpus
- Used to extract contextual embeddings from headlines and post text.

### 🖼️ Image Model — ResNet50
- Pretrained on ImageNet
- Used for extracting deep image features and identifying visual misinformation cues.

---

## 🧹 Data Preprocessing

- Removed irrelevant columns from the dataset (2-way and 3-way labels).
- Used cleaned, lowercased titles for BERT tokenizer compatibility.
- Applied `train_test_split()` with stratification for class balance.
- Filtered out missing or broken image URLs using `urllib` and pandas.
- Replaced NaN values and ensured a clean, consistent dataset for training.

---

## 🧪 Training Highlights

- Operated on 10% of the full dataset (700K+ → ~50K entries).
- Trained image and text models separately and then combined.
- Utilized TPU and T4 GPU accelerators for faster training cycles.
- Optimized loss functions for balanced multi-class classification.

---

## 🧩 Tech Stack

| Component        | Technology           |
|------------------|----------------------|
| Text Model       | BERT (`bert-base-uncased`) |
| Image Model      | ResNet50             |
| Backend API      | FastAPI              |
| Frontend         | Chrome Extension (JS)|
| Dataset          | Fakeddit             |
| Deployment       | Localhost (dev)      |

---

## 🛠️ How to Run

### 1️⃣ Start FastAPI Backend
```bash
cd backend/app
uvicorn main:app --reload
