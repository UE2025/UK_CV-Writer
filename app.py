import streamlit as st
from openai import OpenAI

# Set up OpenAI client using Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="AI Resume Writer", page_icon="🧠", layout="centered")
st.title("📄 AI Resume & Cover Letter Generator")

st.markdown("""
Paste your current CV and the job advert below. The app will rewrite your CV to match the job,
and generate a tailored cover letter — all optimised for ATS (Applicant Tracking Systems).
""")

# --- User Inputs ---
cv_text = st.text_area("📋 Paste Your Current CV:", height=300, placeholder="e.g. Work history, skills, education...")
job_ad = st.text_area("📌 Paste the Job Description:", height=300, placeholder="e.g. Responsibilities, skills required...")

if st.button("🚀 Generate CV & Cover Letter") and cv_text and job_ad:
    with st.spinner("Working on your CV and cover letter..."):
        prompt = f"""
You are an expert UK-based career consultant.

The user wants to apply for the job below:

Job Description:
{job_ad}

Their current CV:
{cv_text}

Tasks:
1. Rewrite the CV to highlight matching experience and skills using ATS-friendly formatting.
2. Write a custom cover letter tailored to the job.

Respond in two sections:
## Rewritten CV
...

## Cover Letter
...
"""
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a professional CV and cover letter writer."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1800
            )

            output = response.choices[0].message.content
            st.success("✅ Done! See your results below.")
            st.markdown(output)

            st.download_button(
                label="💾 Download as TXT",
                data=output,
                file_name="cv_and_cover_letter.txt",
                mime="text/plain"
            )

        except Exception as e:
            st.error(f"❌ Error: {e}")
else:
    st.info("Enter both your CV and the job ad to begin.")
