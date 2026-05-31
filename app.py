
import streamlit as st
import PyPDF2
import re
import nltk
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('stopwords', quiet=True)
from nltk.corpus import stopwords

st.set_page_config(page_title="AI Resume Screener", page_icon="📄", layout="wide")

st.markdown("""
    <style>
    .score-box {
        padding: 20px; border-radius: 12px;
        text-align: center; font-size: 48px;
        font-weight: bold; margin: 20px 0;
    }
    .high   { background-color: #d4edda; color: #155724; }
    .medium { background-color: #fff3cd; color: #856404; }
    .low    { background-color: #f8d7da; color: #721c24; }
    .keyword-box {
        display: inline-block; padding: 4px 12px;
        margin: 4px; border-radius: 20px; font-size: 14px;
    }
    .found   { background-color: #d4edda; color: #155724; }
    .missing { background-color: #f8d7da; color: #721c24; }
    </style>
""", unsafe_allow_html=True)


def extract_text_from_pdf(uploaded_file):
    text = ""
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    return text

def clean_text(text):
    text = text.lower()
    text = re.sub(r"\n", " ", text)
    text = text.translate(str.maketrans("", "", string.punctuation))
    stop_words = set(stopwords.words("english"))
    tokens = [t for t in text.split() if t not in stop_words and len(t) > 2]
    return " ".join(tokens)

def get_match_score(resume_text, jd_text):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([resume_text, jd_text])
    score = cosine_similarity(vectors[0], vectors[1])[0][0]
    return round(score * 100, 2)

def extract_keywords(text, top_n=30):
    vectorizer = TfidfVectorizer(max_features=top_n, stop_words="english")
    vectorizer.fit_transform([text])
    return set(vectorizer.get_feature_names_out())

def get_missing_keywords(resume_text, jd_text):
    jd_keywords    = extract_keywords(jd_text, top_n=30)
    resume_words   = set(resume_text.lower().split())
    found_keywords   = {kw for kw in jd_keywords if kw in resume_words}
    missing_keywords = jd_keywords - found_keywords
    return found_keywords, missing_keywords

def score_label(score):
    if score >= 70:
        return "high",   "Strong Match"
    elif score >= 45:
        return "medium", "Moderate Match"
    else:
        return "low",    "Weak Match"


st.title("📄 AI Resume Screener")
st.markdown("Upload your resume and paste a job description to get an instant match score.")
st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    st.subheader("📎 Upload Resume (PDF)")
    uploaded_resume = st.file_uploader("Upload resume", type=["pdf"], label_visibility="collapsed")
with col2:
    st.subheader("📋 Paste Job Description")
    job_description = st.text_area("Job description", height=250,
                                   placeholder="Paste the full job description here...",
                                   label_visibility="collapsed")

st.markdown("---")

if st.button("🔍 Analyze Resume", use_container_width=True):
    if not uploaded_resume:
        st.error("Please upload your resume PDF.")
    elif not job_description.strip():
        st.error("Please paste a job description.")
    else:
        with st.spinner("Analyzing..."):
            raw_resume   = extract_text_from_pdf(uploaded_resume)
            clean_resume = clean_text(raw_resume)
            clean_jd     = clean_text(job_description)
            score        = get_match_score(clean_resume, clean_jd)
            css_class, label = score_label(score)
            found_kw, missing_kw = get_missing_keywords(clean_resume, clean_jd)

        st.markdown("## 📊 Results")
        r1, r2, r3 = st.columns(3)
        with r1:
            st.markdown(f"""
                <div class="score-box {css_class}">
                    {score}%<br>
                    <span style="font-size:18px">{label}</span>
                </div>""", unsafe_allow_html=True)
        with r2:
            st.metric("✅ Matched Keywords", len(found_kw))
        with r3:
            st.metric("❌ Missing Keywords", len(missing_kw))

        st.markdown("---")
        st.markdown("## 🔑 Keyword Analysis")
        k1, k2 = st.columns(2)
        with k1:
            st.markdown("### ✅ Found in Resume")
            if found_kw:
                st.markdown("".join([f'<span class="keyword-box found">{kw}</span>' for kw in sorted(found_kw)]),
                            unsafe_allow_html=True)
            else:
                st.info("No matching keywords found.")
        with k2:
            st.markdown("### ❌ Missing From Resume")
            if missing_kw:
                st.markdown("".join([f'<span class="keyword-box missing">{kw}</span>' for kw in sorted(missing_kw)]),
                            unsafe_allow_html=True)
            else:
                st.success("No important keywords missing!")

        st.markdown("---")
        st.markdown("## 💡 Suggestions")
        if score >= 70:
            st.success("Strong match! Focus on tailoring your summary and cover letter.")
        elif score >= 45:
            st.warning("Moderate match. Add missing keywords to your Skills or Projects sections.")
        else:
            st.error("Low match. Rework your resume to align with this job description.")

        if missing_kw:
            st.markdown("**Add these keywords to your resume where relevant:**")
            st.code(", ".join(sorted(missing_kw)))

        with st.expander("📄 View Extracted Resume Text"):
            st.text(raw_resume[:3000] + ("..." if len(raw_resume) > 3000 else ""))
