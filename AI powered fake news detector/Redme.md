# 🧠 AI-Powered Advanced Fake News Detection Chrome Extension

A **multi-modal fake news detection system** using BERT (NLP) and ResNet50 (Vision) deployed via a **FastAPI backend** and integrated into a **Chrome extension**.

---

## 🚀 Key Features
- MultiModal Classification (Text + Image)
- 6-class labeling using the Fakeddit dataset
- FastAPI backend with real-time detection
- Chrome extension frontend (vanilla JavaScript)
- Custom-trained model on 50K+ samples

---

## 📦 Dataset
- Fakeddit (6 classes): True, Satire, False Connection, Imposter, Manipulated, Misleading

---

## 🧠 Models
- BERT (`bert-base-uncased`) for text (pretrained on Wikipedia & Toronto Book Corpus)
- ResNet50 for image classification (pretrained on ImageNet)

---

## 🧹 Preprocessing
- Removed 2-way and 3-way labels
- Used cleaned lowercase titles
- Stratified train-test split on 700K+ samples (used 10%)
- Dropped missing image URLs and NaNs

---

## 📁 How to Run
### 1️⃣ Start Backend
```bash
cd backend/app
uvicorn main:app --reload
