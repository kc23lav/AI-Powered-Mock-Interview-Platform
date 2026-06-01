import streamlit as st
from resume_parser import extract_resume_text
from jd_analyser import calculate_match
from interview_engine import generate_questions
from voice_generator import generate_voice
from answer_evaluator import evaluate_answer
from report_generator import generate_final_report
from pdf_generator import generate_pdf
from score_praser import extract_scores
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="AI Interview Platform",
    page_icon="🎤",
    layout="wide"
)

# ---------------- SESSION STATE ---------------- #

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "questions" not in st.session_state:
    st.session_state.questions = []

if "current_question" not in st.session_state:
    st.session_state.current_question = 0
    
if "scores" not in st.session_state:
    st.session_state.scores = []

# ---------------- LOGIN / REGISTER ---------------- #

if not st.session_state.logged_in:

    st.title("🎤 AI-Powered Mock Interview Platform")

    option = st.sidebar.selectbox(
        "Choose",
        ["Login", "Register"]
    )

    if option == "Register":

        st.subheader("Create Account")

        name = st.text_input("Full Name")
        email = st.text_input("Email")
        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Register"):

            st.success(
                "Registration Successful! Please Login."
            )

    else:

        st.subheader("Login")

        email = st.text_input("Email")
        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Login"):

            st.session_state.logged_in = True
            st.rerun()

# ---------------- DASHBOARD ---------------- #

else:

    st.title("🏠 Candidate Dashboard")

    st.success("Login Successful!")

    st.write(
        "Welcome to the AI Interview Platform"
    )

    # ---------------- RESUME ---------------- #

    st.subheader("📄 Upload Resume")

    uploaded_resume = st.file_uploader(
        "Upload Resume (PDF)",
        type=["pdf"]
    )

    if uploaded_resume:

        st.success(
            "Resume Uploaded Successfully!"
        )

        try:

            resume_text = extract_resume_text(
                uploaded_resume
            )

            st.subheader(
                "📄 Resume Preview"
            )

            st.text_area(
                "Extracted Resume Text",
                resume_text,
                height=300
            )

            # ---------------- JD ---------------- #

            st.subheader(
                "💼 Job Description"
            )

            jd_text = st.text_area(
                "Paste Job Description",
                height=250
            )

            if jd_text:

                st.success(
                    "Job Description Added Successfully!"
                )

                score, matched_skills, missing_skills, recommendations = calculate_match(
                    resume_text,
                    jd_text
                )

                # ---------------- ANALYSIS ---------------- #

                st.subheader(
                    "📊 Resume Match Analysis"
                )

                st.metric(
                    "Match Score",
                    f"{score}%"
                )

                # ---------------- MATCHED ---------------- #

                st.write(
                    "### ✅ Matched Skills"
                )

                if matched_skills:

                    for skill in matched_skills:

                        st.write(
                            f"• {skill}"
                        )

                else:

                    st.write(
                        "No matching skills found."
                    )

                # ---------------- MISSING ---------------- #

                st.write(
                    "### ❌ Missing Skills"
                )

                if missing_skills:

                    for skill in missing_skills:

                        st.write(
                            f"• {skill}"
                        )

                else:

                    st.write(
                        "No missing skills."
                    )

                # ---------------- RECOMMENDATIONS ---------------- #

                st.write(
                    "### 💡 Recommendations"
                )

                for recommendation in recommendations:

                    st.write(
                        f"• {recommendation}"
                    )

                # ---------------- AI QUESTIONS ---------------- #

                st.divider()

                if st.button(
                    "🎯 Generate Interview Questions"
                ):

                    with st.spinner(
                        "Generating Questions..."
                    ):

                        st.session_state.questions = (
                            generate_questions(
                                resume_text,
                                jd_text
                            )
                        )

                        st.session_state.current_question = 0

                if st.session_state.questions:

                     current = st.session_state.current_question
                     
                     st.write("Current Question:", current)
                     st.write("Total Questions:", len(st.session_state.questions))

                     if current < len(st.session_state.questions):

                        st.subheader(
                         f"🤖 Question {current + 1}"
                    )

                        st.write(
                        st.session_state.questions[current]
                    )
                        audio_file = generate_voice(
                        st.session_state.questions[current]
                        )

                        audio_bytes = open(
                              audio_file,
                              "rb"
                        ).read()

                        st.audio(
                            audio_bytes,
                            format="audio/mp3"
                        )
                   
                        answer = st.text_area(
                        "✍ Your Answer",
                        key=f"answer_{current}",
                        height=200
                    )
                        if st.button("📤 Submit Answer"):
                            
                            #Evaluate answer and store score
                            result = evaluate_answer(
                                st.session_state.questions[current],
                                answer
                            )
                            
                            #Append result to session state 
                            st.session_state.scores.append(result)

                            st.success(
                            "Answer Submitted!"
                            )
                            
                            st.subheader(
                               "📊 AI Evaluation"
                            )

                            st.text_area(
                                "Evaluation",
                                result,
                                height=300
                           )
                        

                        if st.button("➡ Next Question"):

                         st.session_state.current_question += 1

                         st.rerun()

                     else:
                         
                       final_report = generate_final_report(
                            "\n".join(
                                st.session_state.scores
                                )
                        )
                       
                       scores = extract_scores(
                           st.session_state.scores
                        )
                       
                       df = pd.DataFrame({
                        "Question": [
                            f"Q{i+1}"
                            for i in range(len(scores))
                        ],
                        "Score": scores
                        })

                       st.subheader(
                          "📊 Question-wise Performance"
                        )

                       st.dataframe(
                           df,
                           use_container_width=True
                        )
                       
                       average_score = (
                           sum(scores) / len(scores)
                           if len(scores) > 0 else 0
                       )

                       st.metric(
                              "🎯 Average Interview Score",
                              f"{average_score:.1f}/10"
                        )
                       
                       st.subheader(
                                "📈 Question-wise Score Analysis"
                        )

                       fig, ax = plt.subplots()

                       ax.bar(
                         df["Question"],
                         df["Score"]
                        )

                       ax.set_xlabel(
                         "Questions"
                      )

                       ax.set_ylabel(
                         "Score (/10)"
                       )

                       ax.set_title(
                         "Interview Performance"
                        )
                       
                       chart_file = "performance_chart.png"

                       fig.savefig(
                              chart_file,
                              bbox_inches="tight"
                        )

                       st.pyplot(fig)
                         
                       for i ,score_text in enumerate(st.session_state.scores,1):
                            st.write(
                            f"### Question {i} Evaluation"
                        )

                            st.text_area(
                                f"Evaluation Result {i}",
                                score_text,
                                height=300,
                                key=f"evaluation_{i}"
                        )
                        
                        #After loop, show final report
                       st.subheader(
                            "📊 Final Interview Report"
                        )

                       st.text_area(
                               "Final Report",
                                final_report,
                                height=350,
                                key="final_report"
                    )
                       
                       pdf_file = generate_pdf(
                           final_report,
                            chart_file
                        )

                       with open(
                            pdf_file,
                            "rb"
                        ) as file:

                        st.download_button(
                            label="📄 Download PDF Report",
                            data=file,
                            file_name="Interview_Report.pdf",
                            mime="application/pdf"
                        )

                       st.success(
                     "🎉 Interview Completed!"
                    )

                       st.balloons()

                       st.write(
                    "Thank you for taking the interview."
                    )

                       st.write(
                    "Your final report will be generated shortly."
                    )

                       if st.button(
                         "🔄 Start New Interview"
                    ):

                        st.session_state.current_question = 0
                        
                        st.session_state.scores = []

                        st.session_state.questions = []

                        st.rerun()

        except Exception as e:

            st.error(
                f"Error reading resume: {e}"
            )

    # ---------------- LOGOUT ---------------- #

    if st.button("Logout"):

        st.session_state.logged_in = False
        st.rerun()