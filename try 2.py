import streamlit as st
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
import tempfile

# Theme toggle
theme = st.toggle("🌗 Dark Mode")

if theme:
    background = "linear-gradient(to right, #141E30, #243B55)"
    card_bg = "rgba(30,30,30,0.95)"
    text_color = "white"
else:
    background = "linear-gradient(to right, #1f4037, #99f2c8)"
    card_bg = "rgba(255,255,255,0.9)"
    text_color = "black"

st.set_page_config(page_title="Premium CGPA Calculator", layout="centered")

# ---------- Custom CSS ----------
st.markdown(f"""
<style>
.stApp {{
    background: {background};
}}
.main-card {{
    background-color: {card_bg};
    padding: 30px;
    border-radius: 15px;
    box-shadow: 0px 8px 20px rgba(0,0,0,0.2);
}}
h1 {{
    text-align: center;
    color: {text_color};
}}
.result-box {{
    background-color: #1f4037;
    padding: 15px;
    border-radius: 10px;
    color: white;
    font-size: 20px;
    text-align: center;
    margin-top: 20px;
}}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>🎓 Premium CGPA Calculator</h1>", unsafe_allow_html=True)

st.markdown('<div class="main-card">', unsafe_allow_html=True)

# Grade mapping
grade_dict = {
    "O": 10,
    "A+": 9,
    "A": 8,
    "B+": 7,
    "B": 6,
    "C": 5
}

# Session state
if "num_subjects" not in st.session_state:
    st.session_state.num_subjects = 1

col1, col2 = st.columns(2)

with col1:
    if st.button("➕ Add Subject"):
        st.session_state.num_subjects += 1

with col2:
    if st.button("➖ Remove Subject"):
        if st.session_state.num_subjects > 1:
            st.session_state.num_subjects -= 1

total_credits = 0
total_points = 0
grades_list = []

for i in range(st.session_state.num_subjects):
    st.subheader(f"Subject {i+1}")

    col1, col2 = st.columns(2)

    with col1:
        subject_type = st.selectbox(
            "Subject Type",
            ["Theory", "Laboratory"],
            key=f"type{i}"
        )

    with col2:
        grade = st.selectbox(
            "Grade",
            list(grade_dict.keys()),
            key=f"grade{i}"
        )

    credit = 3 if subject_type == "Theory" else 2

    total_credits += credit
    total_points += grade_dict[grade] * credit
    grades_list.append(grade_dict[grade])

if st.button("🚀 Calculate CGPA"):
    cgpa = total_points / total_credits
    percentage = cgpa * 9.5

    st.markdown(
        f"""
        <div class="result-box">
            🎯 CGPA: {round(cgpa,2)} <br>
            📊 Percentage: {round(percentage,2)} %
        </div>
        """,
        unsafe_allow_html=True
    )

    # Chart
    fig, ax = plt.subplots()
    ax.bar(range(1, len(grades_list)+1), grades_list)
    ax.set_xlabel("Subjects")
    ax.set_ylabel("Grade Points")
    ax.set_title("Grade Distribution")
    st.pyplot(fig)

    # PDF
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    doc = SimpleDocTemplate(temp_file.name, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("CGPA Report", styles["Title"]))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"CGPA: {round(cgpa,2)}", styles["Normal"]))
    elements.append(Paragraph(f"Percentage: {round(percentage,2)}%", styles["Normal"]))

    doc.build(elements)

    with open(temp_file.name, "rb") as f:
        st.download_button("💾 Download Report", f, file_name="CGPA_Report.pdf")

st.markdown('</div>', unsafe_allow_html=True)