# 📄 AI Resume Screener

An NLP-powered web application that analyzes resumes against job descriptions and provides a resume match score, keyword gap analysis, and personalized improvement suggestions to help candidates optimize their resumes for better job alignment.

---

## 🚀 Live Demo
🔗 Try the App:  
https://ai-resume-screener-vqixiclo6mltx36gyvse3k.streamlit.app/

---

## ✨ Features

✅ Upload and parse resumes in PDF format  
✅ Compare resumes with Job Descriptions (JD)  
✅ Generate Resume Match Score using NLP  
✅ Identify Matched & Missing Keywords  
✅ Display color-coded keyword analysis  
✅ Provide actionable recommendations to improve ATS compatibility  

---

## 🛠️ Tech Stack

| Category | Technologies |
|----------|-------------|
| Language | Python |
| Frontend | Streamlit |
| PDF Processing | PyPDF2 |
| NLP | NLTK |
| ML | Scikit-learn |
| Similarity | TF-IDF + Cosine Similarity |

---

## ⚙️ How It Works

1. Upload your resume (PDF)  
2. Paste the job description  
3. Extract text from resume  
4. Convert text into vectors using TF-IDF  
5. Calculate similarity using Cosine Similarity  
6. Generate:
   - Match Score
   - Keyword Analysis
   - Improvement Suggestions

---

## 📂 Project Structure

bash AI-Resume-Screener/ │ ├── app.py ├── requirements.txt ├── README.md ├── utils/ ├── sample_resume.pdf └── screenshots/ 

---

## 📸 Preview
<img width="1252" height="609" alt="reume" src="https://github.com/user-attachments/assets/c565f20a-fc98-4032-a05b-0eb14feee9d5" />

<img width="1280" height="604" alt="resume result" src="https://github.com/user-attachments/assets/f67feac7-9352-4789-8a03-e1807755a1b7" />

---

## 🎯 Future Improvements

- Resume ATS Score Visualization  
- Multiple Resume Comparison  
- Export Analysis Report (PDF)  
- Job Recommendation Engine  
- AI-powered Resume Optimizatio
