# streamlit.py

# Import libraries
import streamlit as st
from app.config.dbconfig import SessionLocal
from app.utils.modelImpl import predict


def main():
    st.markdown("# Job Matching Application")
    st.sidebar.title("Job Matching Dashboard")

    html_temp = """
    <div style="background-color: #0B4F6C; padding:10px">
    <h2 style="color:white; text-align:center;">Job Matching Application</h2>
    </div>
    """
    st.markdown(html_temp, unsafe_allow_html=True)

    uploaded_resume = st.sidebar.file_uploader("Upload your resume", type=['txt'], key="resumeUploader")
    if uploaded_resume is not None:
        resume_text = uploaded_resume.read().decode('utf-8')
    else:
        resume_text = st.text_area("Paste your resume text here:", height=200)

    if st.button("Match Jobs"):
        with SessionLocal() as session:
            result_data = predict(session, resume_text)

            if result_data.empty:
                st.warning("No matching jobs found.")
            else:
                st.success("Matching jobs found!")
                st.table(result_data)


if __name__ == "__main__":
    main()
