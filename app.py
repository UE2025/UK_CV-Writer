import streamlit as st
from openai import OpenAI

# OpenAI API client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# App config
st.set_page_config(page_title="UK CV Writer", page_icon="📄", layout="centered")

# === HEADER / BANNER ===
st.markdown("""
# 🇬🇧 UK CV Writer
Create tailored, ATS-optimised CVs and cover letters with AI – for UK job roles.

""")

# === EXAMPLE INPUTS ===
example_cv = """John Smith
London, UK | john.smith@email.com | 07123 456789

Work Experience:
Delivery Driver – DPD UK (2020–2024)
- Delivered parcels efficiently across Greater London
- Maintained delivery records and vehicle logs

Education:
GCSEs – English (B), Maths (C), Science (C)

Skills:
Teamwork, Customer Service, Timekeeping
"""

example_job_ad = """Job Title: Warehouse Operative – Amazon Tilbury

We are looking for reliable individuals to join our logistics team. Must be able to work flexible shifts and operate safely in a fast-paced environment.

Key Responsibilities:
- Picking and packing items
- Operating pallet trucks and scanners
- Following health & safety protocols
"""

# === INPUT FIELDS ===
cv_text = st.text_area("📋 Paste or Edit Your CV:", value=example_cv, height=300)
job_ad = st.text_area("📌 Paste the Job Description:", value=example_job_ad, height=300)

# === BUTTON ===
if st.button("🚀 Generate My CV & Cover Letter") and cv_text and job_ad:
    with st.spinner("AI is writing your tailored CV and cover letter..."):
        prompt = f"""
You are a UK-based career expert.

Job Ad:
{job_ad}

Current CV:
{cv_text}

Rewrite the CV to match the job and create a new cover letter.

Respond in this format:
## Rewritten CV
...

## Cover Letter
...
"""
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a professional UK CV and cover letter writer."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1800
            )
            output = response.choices[0].message.content
            st.success("✅ Done! See your results below.")
            st.markdown(output)

            st.download_button(
                label="💾 Download as .txt file",
                data=output,
                file_name="uk_cv_and_cover_letter.txt",
                mime="text/plain"
            )

        except Exception as e:
            st.error(f"❌ Error: {e}")
else:
    st.info("Fill in both fields and click the button to generate your documents.")
