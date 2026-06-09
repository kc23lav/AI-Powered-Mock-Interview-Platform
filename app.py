import streamlit as st
from resume_parser import extract_resume_text
from jd_analyser import calculate_match
from interview_engine import generate_questions
from voice_generator import generate_voice
from answer_evaluator import evaluate_answer
from report_generator import generate_final_report
from pdf_generator import generate_pdf
from score_praser import extract_scores
from ats_analyser import calculate_ats_score
from metric_parser import extract_metrics
from semantic_matcher import semantic_match_score
from database import *
from datetime import datetime
from resume_optimizer import *
from streamlit_mic_recorder import mic_recorder
from transcriber import *
import tempfile
import pandas as pd
import matplotlib.pyplot as plt

st.markdown("""
<style>

/* ==========================
   APP BACKGROUND
========================== */

.stApp {

    background:
    linear-gradient(
        -45deg,
        #050816,
        #0b1023,
        #151d4f,
        #28114f,
        #09111f
    );

    background-size: 400% 400%;

    animation: gradientMove 12s ease infinite;
}

@keyframes gradientMove {

    0% {
        background-position: 0% 50%;
    }

    50% {
        background-position: 100% 50%;
    }

    100% {
        background-position: 0% 50%;
    }
}


/* ==========================
   SIDEBAR
========================== */

[data-testid="stSidebar"] {

    background:
    linear-gradient(
        180deg,
        rgba(15,18,40,0.95),
        rgba(8,10,25,0.98)
    );

    border-right:
    1px solid rgba(255,255,255,0.08);
}


/* ==========================
   HERO SECTION
========================== */

.hero {

    padding:40px;

    border-radius:24px;

    background:
    linear-gradient(
        135deg,
        rgba(255,255,255,0.06),
        rgba(255,255,255,0.02)
    );

    border:
    1px solid rgba(255,255,255,0.08);

    backdrop-filter: blur(12px);

    box-shadow:
    0 8px 40px rgba(255,105,180,0.08);
}

.hero h3 {

    color:#ff7ac8;

    font-weight:500;

    margin-bottom:10px;
}

.hero h1 {

    color:white;

    font-size:64px;

    font-weight:800;

    margin-top:0;

    margin-bottom:15px;
}

.hero p {

    color:#b8c0d4;

    font-size:20px;

    line-height:1.7;
}


/* ==========================
   FEATURE CARD
========================== */

.feature-card {

    padding:30px;

    border-radius:24px;

    background:
    linear-gradient(
        145deg,
        rgba(255,255,255,0.05),
        rgba(255,255,255,0.02)
    );

    border:
    1px solid rgba(255,255,255,0.08);

    backdrop-filter: blur(10px);

    transition: all 0.3s ease;
}

.feature-card:hover {

    transform: translateY(-4px);

    border-color: rgba(255,122,200,0.4);

    box-shadow:
    0 10px 30px rgba(255,105,180,0.15);
}


/* ==========================
   KPI CARDS
========================== */

.kpi-card {

    background:
    linear-gradient(
        145deg,
        rgba(30,41,59,0.85),
        rgba(15,23,42,0.95)
    );

    border-radius:24px;

    padding:30px;

    text-align:center;

    border:
    1px solid rgba(255,255,255,0.08);

    backdrop-filter: blur(14px);

    transition: all 0.3s ease;

    overflow:visible;
}

.kpi-card:hover {

    transform:
    translateY(-8px)
    scale(1.03);

    box-shadow:
    0 15px 40px
    rgba(255,105,180,0.25);
}
.kpi-icon {

    font-size:42px;

    margin-bottom:15px;
}

.kpi-value {

    color:white;

    font-size:46px;

    font-weight:800;
}

.kpi-title {

    color:white;

    font-size:18px;

    margin-top:10px;
}

.kpi-subtitle {

    color:#aab3c7;

    margin-top:10px;

    font-size:14px;
}


/* ==========================
   BUTTONS
========================== */

.stButton > button {

    border-radius:12px;

    border:none;

    background:
    linear-gradient(
        135deg,
        #ff5fb2,
        #ff7ac8
    );

    color:white;

    font-weight:600;

    transition: all 0.3s ease;
}

.stButton > button:hover {

    transform: translateY(-2px);

    box-shadow:
    0 8px 20px rgba(255,105,180,0.25);
}


/* ==========================
   FILE UPLOADER
========================== */

[data-testid="stFileUploader"] {

    border-radius:18px;

    border:
    1px solid rgba(255,255,255,0.08);

    background:
    rgba(255,255,255,0.03);
}


/* ==========================
   SCROLLBAR
========================== */

::-webkit-scrollbar {

    width:8px;
}

::-webkit-scrollbar-thumb {

    background:#ff7ac8;

    border-radius:20px;
}

::-webkit-scrollbar-track {

    background:#0b1023;
}

section[data-testid="stSidebar"] label {

    transition: all 0.3s ease;
}

section[data-testid="stSidebar"] label:hover {

    transform: translateX(6px);

    color: #ff7ac8;
}

.skill-pill {

    display:inline-block;

    padding:10px 16px;

    margin:6px;

    border-radius:25px;

    font-weight:600;

    font-size:15px;
}

.skill-match {

    background:rgba(0,255,100,0.15);

    color:#6eff9d;

    border:1px solid rgba(0,255,100,0.25);
}

.skill-missing {

    background:rgba(255,0,80,0.12);

    color:#ff7b9c;

    border:1px solid rgba(255,0,80,0.25);
}

textarea {

    border-radius:20px !important;

    border:1px solid rgba(255,102,196,0.35) !important;

    background:
    linear-gradient(
        145deg,
        rgba(255,255,255,0.04),
        rgba(255,255,255,0.02)
    ) !important;

    color:white !important;

    font-size:18px !important;

    padding:20px !important;

    line-height:1.7 !important;
}

textarea:focus {

    border:1px solid #ff66c4 !important;

    box-shadow:
    0 0 20px rgba(255,102,196,0.35) !important;
}

</style>
""",
unsafe_allow_html=True)
# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="AI Interview Platform",
    page_icon="🎤",
    layout="wide"
)

create_database()

# ---------------- SESSION STATE ---------------- #

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_id" not in st.session_state:
    st.session_state.user_id = None
    
if "user_name" not in st.session_state:
    st.session_state.user_name = ""

if "user_email" not in st.session_state:
    st.session_state.user_email = ""
    
if "questions" not in st.session_state:
    st.session_state.questions = []

if "current_question" not in st.session_state:
    st.session_state.current_question = 0
    
if "scores" not in st.session_state:
    st.session_state.scores = []
    
if"all_scores" not in st.session_state:
    st.session_state.all_scores = []
    
if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

if "jd_text" not in st.session_state:
    st.session_state.jd_text = ""

if "ats_result" not in st.session_state:
    st.session_state.ats_result = None

if "semantic_score" not in st.session_state:
    st.session_state.semantic_score = 0

if "final_report" not in st.session_state:
    st.session_state.final_report = ""

if "final_score" not in st.session_state:
    st.session_state.final_score = 0

if "final_decision" not in st.session_state:
    st.session_state.final_decision = ""
    
if "menu" not in st.session_state:
    st.session_state.menu = "📊 Dashboard"
    
if "saved_result" not in st.session_state:
    st.session_state.saved_result = False

# ---------------- LOGIN / REGISTER ---------------- #

if not st.session_state.logged_in:

    st.title("🎤 AI-Powered Mock Interview Platform")

    option = st.sidebar.selectbox(
        "Choose",
        ["Login", "Register"]
    )

    if option == "Register":

     st.subheader("Create Account")

    name = st.text_input(
        "Full Name",
        key="register_user"
    )

    email = st.text_input(
        "Email",
        key="register_email"
    )

    password = st.text_input(
        "Password",
        type="password",
        key="register_password"
    )

    if st.button("Register"):

        if not name.strip():

            st.error(
                "Please enter name."
            )

        elif not email.strip():

            st.error(
                "Please enter email."
            )

        elif not password.strip():

            st.error(
                "Please enter password."
            )

        else:

            success = register_user(
                name,
                email,
                password
            )

            if success:

                st.success(
                    "Registration successful! Please login."
                )

            else:

                st.error(
                    "Email already exists."
                )

    else:

     st.subheader("Login")

     email = st.text_input(
        "Email",
        key="login_email"
     )

     password = st.text_input(
        "Password",
        type="password",
        key="login_password"
     )

     if st.button("Login"):

        user = login_user(
            email,
            password
        )

        if user:

            st.session_state.logged_in = True

            st.session_state.user_id = user[0]
            st.session_state.user_name = user[1]
            st.session_state.user_email = user[2]

            st.success(
                f"Welcome {user[1]}!"
            )

            st.rerun()

        else:

            st.error(
                "Invalid Email or Password"
            )



else:

    st.title("🎤 AI-Powered Mock Interview Platform")
    

    #---------------Navigation----------------#
    with st.sidebar:

      st.markdown(f"""
            <div style="
               padding:20px;
               border-radius:20px;
               background:linear-gradient(135deg,#1e293b,#0f172a);
               border:1px solid rgba(255,255,255,0.08);
               text-align:center;
               margin-bottom:15px;">

              <h2 style="margin:0;">👋 {st.session_state.user_name}</h2>

              <p style="
              color:#b8c0d4;
              margin-top:10px;">
              {st.session_state.user_email}
              </p>

            </div>
            """, unsafe_allow_html=True)
      if st.button("🔒 Logout"):
        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.user_name = ""
        st.session_state.user_email = ""
        st.rerun()

    st.sidebar.divider()
    
    pages = [
    "📊 Dashboard",
    "📄 Resume Analysis",
    "🎤 Interview",
    "📈 Results",
    "📚 History"
]

    menu = st.sidebar.radio(
    "",
    pages,
    index=pages.index(
        st.session_state.menu
    )
)

    st.session_state.menu = menu
    
    #---------------- DASHBOARD ---------------- #
    
    if menu == "📊 Dashboard":
     st.markdown(f"""
      <div class="feature-card">

      <h2>🚀 Career Readiness Hub</h2>

      <p>
      Track ATS compatibility,
      Interview Performance,
      Semantic Match Score,
      and Hiring Decisions
      all from one dashboard.
      </p>

      </div>
      """,
      unsafe_allow_html=True)
     st.markdown(
     f"""
      <div class="hero">

        <h3>Welcome back,</h3>

        <h1>
           {st.session_state.user_name} 👋
        </h1>

        <p>
           Let's crack your dream job together! 🚀
        </p>

      </div>
      """,
      unsafe_allow_html=True
)
     st.markdown("""
           <div class="metric-card">

            ### 🚀 AI Interview Platform

            Prepare smarter with AI-powered resume analysis,
            interview simulation, and hiring readiness insights.

            </div>
            """,
            unsafe_allow_html=True)
    
     st.divider()
     
     history = get_user_history(st.session_state.user_id)
     
     if history:

       df = pd.DataFrame(
           history,
           columns=[
            "ID",
            "Date",
            "ATS Score",
            "Semantic Score",
            "Interview Score",
            "Hiring Decision"
           ]
        )

       total_interviews = len(df)

       avg_ats = round(
          df["ATS Score"].mean(),
          1
        )

       avg_interview = round(
          df["Interview Score"].mean(),
          1
       )

       best_score = round(
          df["Interview Score"].max(),
          1
        )

     else:

        total_interviews = 0
        avg_ats = 0
        avg_interview = 0
        best_score = 0


     col1, col2, col3, col4 = st.columns(4)

     with col1:

        st.markdown(f"""
       <div class="kpi-card">

          <div class="kpi-icon">📊</div>

          <div class="kpi-value">
            {total_interviews}
          </div>

          <div class="kpi-title">
            Total Interviews
          </div>

          <div class="kpi-subtitle">
            Attempts Made
          </div>

       </div>
       """,
       unsafe_allow_html=True)

     with col2:

        st.markdown(f"""
        <div class="kpi-card">

          <div class="kpi-icon">🎯</div>

          <div class="kpi-value">
            {avg_ats}%
          </div>

          <div class="kpi-title">
            Avg ATS Score
          </div>

          <div class="kpi-subtitle">
            Resume Match
          </div>

        </div>
        """,
        unsafe_allow_html=True)

     with col3:

        st.markdown(f"""
        <div class="kpi-card">

          <div class="kpi-icon">🧠</div>

          <div class="kpi-value">
            {avg_interview}
          </div>

          <div class="kpi-title">
            Avg Interview Score
          </div>

          <div class="kpi-subtitle">
            Performance Score
          </div>

        </div>
        """,
        unsafe_allow_html=True)

     with col4:

        st.markdown(f"""
        <div class="kpi-card">

          <div class="kpi-icon">🏆</div>

          <div class="kpi-value">
            {best_score}
          </div>

          <div class="kpi-title">
            Best Score
          </div>

          <div class="kpi-subtitle">
            Highest Achieved
          </div>

        </div>
        """,
        unsafe_allow_html=True)
        
    
     st.markdown("## ⚡ Quick Actions")

     col1,col2,col3 = st.columns(3)
     
     with col1:
      if st.button(
        "📄 Resume Analysis\nAnalyze ATS Compatibility",
        use_container_width=True
    ):
        st.session_state.menu = "📄 Resume Analysis"
        st.rerun()
        
     with col2:
      if st.button(
        "🎤 Start Interview\nGenerate AI Questions",
        use_container_width=True
    ):
        st.session_state.menu = "🎤 Interview"
        st.rerun()
        
     with col3:
      if st.button(
        "📈 View Results\nCheck Hiring Readiness",
        use_container_width=True
    ):
        st.session_state.menu = "📈 Results"
        st.rerun()
        
     st.markdown("## 🎯 Hiring Readiness")
     readiness = round(
    (avg_ats + avg_interview) / 2
    )
     
     st.progress(
    readiness / 100
    )

     st.metric(
    "Readiness Score",
    f"{readiness}%"
    )
     
     
    #---------------- RESUME ANALYSIS ---------------- #            
     
    elif menu == "📄 Resume Analysis":
     st.title("📄 Resume Analysis")
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
            st.session_state.resume_text = resume_text

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
            
            st.session_state.jd_text = jd_text

            if jd_text:

                st.success(
                    "Job Description Added Successfully!"
                )

                score, matched_skills, missing_skills, recommendations = calculate_match(
                    resume_text,
                    jd_text
                )
                
                ats_result = calculate_ats_score(
                    resume_text,
                    jd_text
                )
                
                semantic_score = semantic_match_score(
                    resume_text,
                    jd_text
                )
                
                st.session_state.ats_result = ats_result
                st.session_state.semantic_score = semantic_score

                st.subheader(
                    "🤖 ATS Compatibility Score"
                )

                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric(
                        "ATS Match Score",
                        f"{ats_result['score']}%"
                    )
                    
                with col2:
                    st.metric(
                        "Semantic Match Score",
                        f"{semantic_score:.2f}%"
                    )
                    
                st.progress(score / 100)
                
                if score >= 80:
                 st.success("🟢 Excellent Match")

                elif score >= 60:
                 st.warning("🟡 Moderate Match")

                else:
                 st.error("🔴 Needs Improvement")
                
                    
                
                st.subheader("📋 ATS Analysis"
                )
                
                matched_html = ""

                for skill in ats_result["matched"][:10]:

                    matched_html += f"""
                    <span class="skill-pill skill-match">
                    ✅ {skill}
                    </span>
                    """

                st.markdown(
                   matched_html,
                   unsafe_allow_html=True
                )
                    
                    
                st.subheader("📋 ATS Missing Skills"
                )

                missing_html = ""

                for skill in ats_result["missing"][:10]:

                  missing_html += f"""
                  <span class="skill-pill skill-missing">
                  ❌ {skill}
                  </span>
                  """

                st.markdown(
                 missing_html,
                 unsafe_allow_html=True
                )
                
                    
                

                # ---------------- ANALYSIS ---------------- #
                    
                st.subheader(
                       "✨ AI Resume Improvement Suggestions"
                )

                if st.button(
                      "Generate Resume Suggestions"
                ):

                        suggestions = improve_resume(
                             resume_text
                        )

                        st.text_area(
                           "Improved Resume",
                            suggestions,
                            height=400
                        )
                st.divider()

                st.markdown("""
                   <div class="feature-card">

                    <h2>🎤 Ready for Your Interview?</h2>

                    <p>
                     Your resume analysis is complete.
                     Now test your skills with an AI-powered mock interview.
                   </p>

                  </div>
                  """,
                  unsafe_allow_html=True)

                if st.button(
                "🚀 Start Interview",
                   use_container_width=True
                ):
                 st.session_state.menu = "🎤 Interview"
                 st.rerun()

        except Exception as e:

         st.error(
                f"Error reading resume: {e}"
            )
        
#---------------- INTERVIEW ---------------- #
    elif menu == "🎤 Interview":
     st.title("🎤 Interview")
     st.divider()

     if st.button(
         "🎯 Generate Interview Questions"
     ):

        with st.spinner(
            "Generating Questions..."
        ):

             st.session_state.questions = (
                 generate_questions(
                  st.session_state.resume_text,
                  st.session_state.jd_text
                )
            )

             st.session_state.current_question = 0
     if st.session_state.questions:

                     st.subheader(
                         "🎤 Interview Mode"
                        )

                     interview_mode = st.radio(
                         "",
                        [
                         "📝 Text Interview",
                         "🎙 Voice Interview"
                        ],
                         horizontal=True
                      )

                    
                     current = st.session_state.current_question

                     total = len(st.session_state.questions)
                     
                     question_display=min(current+1,total)
                     st.markdown(
                     f"### 🎯 Question {question_display} of {total}"
                    )
                     
                     progress_value = min(
                           (current + 1) /
                           len(st.session_state.questions),
                             1.0
                          )

                     st.progress(progress_value)
                    

                     if current < len(st.session_state.questions):


                        st.markdown(
                          f"""
                          <div class="feature-card">

                          <h3>🤖 Interview Question</h3>

                          <p style="
                          font-size:22px;
                          line-height:1.8;
                          color:white;
                          ">
                          {st.session_state.questions[current]}
                          </p>

                          </div>
                          """,
                          unsafe_allow_html=True
                        )
                    
                        if interview_mode == "🎙 Voice Interview":
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
                         
                        answer = ""
                         
                        if interview_mode == "📝 Text Interview":
                   
                         answer = st.text_area(
                            "💬 Your Answer",
                             placeholder="""
                             Start typing your response here...

                             Structure:
                             1. Situation / Context
                             2. Technical Approach
                             3. Challenges Faced
                             4. Outcome / Impact
                             """,
                             key=f"answer_{current}",
                             height=250
                           )
                         
                        else:
                            audio=mic_recorder(
                                start_prompt="🎙 Start Answer",
                                stop_prompt="⏹ Stop Answer",
                                key=f"voice_{current}"
                            )
                            
                            if "voice_answer" not in st.session_state:
                               st.session_state.voice_answer = ""
                               answer = st.session_state.voice_answer
                            
                            if audio:
                             st.success("Voice recorded successfully!")
                            
                             with tempfile.NamedTemporaryFile(
                                delete=False,
                                suffix=".wav"
                            ) as temp_audio:

                                temp_audio.write(
                                    audio["bytes"]
                                )

                                temp_path = temp_audio.name
                                
                                answer = transcribe_audio(
                                    temp_path
                                )
                                
                                st.success("Answer transcribed successfully!")
                                st.text_area(
                                    "Transcribed Answer",
                                    answer,
                                    height=200
                                )
                                st.session_state.voice_answer = answer
                                
                                
                        if st.button("✅ Submit Answer"):
                            
                            if not answer.strip():
                                st.error(
                                    "Please provide an answer before submitting."
                                )
                                st.stop()
                            
                            if interview_mode == "Voice Interview":
                               answer = st.session_state.voice_answer
                                
                            
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

                            metrics = extract_metrics(
                               result
                            )
                            
                            if metrics:
                                st.subheader(
                                    "📈 Evaluation Metrics")
                                
                                overall_score = metrics["Overall Score"]

                                st.markdown(
                                    f"""
                                    <div class="hero">

                                    <h3>🎯 Overall Interview Score</h3>

                                    <h1>{overall_score:.1f}/100</h1>

                                    <p>AI Evaluation Result</p>

                                    </div>
                                    """,
                                    unsafe_allow_html=True
                                 )
                                st.session_state.all_scores.append(overall_score)
                                
                                if overall_score >= 85:
                                    hiring_recommendation = "Strong Hire"
                                    st.success(
                                         "🟢 Strong Hire"
                                    )
                                    
                                elif overall_score >= 70:
                                    hiring_recommendation = "Consider with Reservations"
                                    st.warning(
                                         "🟡 Consider with Reservations"
                                    )
                                    
                                else:
                                    hiring_recommendation = "Not Recommended"
                                    st.error(
                                         "🔴 Not Recommended"
                                    )
                                
                                st.markdown("""
                                <div class="feature-card">

                                <h3>📊 Interview Evaluation Breakdown</h3>

                                </div>
                                """, unsafe_allow_html=True)

                                st.write("🧠 Technical Accuracy")
                                st.progress(metrics["Technical Accuracy"] / 100)
                                st.caption(f"{metrics['Technical Accuracy']:.0f}/100")

                                st.write("💬 Communication")
                                st.progress(metrics["Communication"] / 100)
                                st.caption(f"{metrics['Communication']:.0f}/100")

                                st.write("🧩 Problem Solving")
                                st.progress(metrics["Problem Solving"] / 100)
                                st.caption(f"{metrics['Problem Solving']:.0f}/100")

                                st.write("🔥 Confidence")
                                st.progress(metrics["Confidence"] / 100)
                                st.caption(f"{metrics['Confidence']:.0f}/100")
                                
                    
                        if st.button("➡ Next Question"):
                            
                         if st.session_state.current_question < len(st.session_state.questions)-1:

                          st.session_state.current_question += 1
                          st.session_state.voice_answer = ""
                         else :
                          st.session_state.current_question=len(st.session_state.questions)
                          st.session_state.voice_answer = ""

                         st.rerun()

                     else:
                        st.success(
                            "🎉 Interview Completed!"
                        )

                        st.balloons()

                        st.write(
                            "Thank you for taking the interview."
                        )

                        st.write(
                            "Your final report will be generated shortly and you can see your repost navigating to the Results section."
                        )
                        
                        if st.button("📊 View Results") :
                            st.session_state.menu="📈 Results"
                            st.rerun()

#----------------- RESULTS ---------------- #
    elif menu == "📈 Results":
     st.title("📈 Results")
     
     if not st.session_state.all_scores:

      st.warning(
        "Complete an interview first."
      )

      st.stop()
     final_report = generate_final_report(
                            "\n".join(
                                st.session_state.scores
                                )
                        )
     
                       
     scores = st.session_state.all_scores
                        
                       
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
                               sum(st.session_state.all_scores)
                               /
                               len(st.session_state.all_scores)
                           )
                       
                       
     final_interview_score = (
                           sum(st.session_state.all_scores) / len(st.session_state.all_scores)
                       )
                       
     if final_interview_score >= 85:
                            final_decision = "Strong Hire"
                            
     elif final_interview_score >= 70:
                           final_decision = "Consider with Reservations"
                       
     else:
                           final_decision = "Not Recommended"
                           
     st.session_state.final_report = final_report
     st.session_state.final_score = final_interview_score
     st.session_state.final_decision = final_decision
     
     if "saved_result" not in st.session_state:
         st.session_state.saved_result=False
         
     if not st.session_state.saved_result:
                        
      save_interview(
       st.session_state.user_id,
       datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
       st.session_state.ats_result["score"],
       st.session_state.semantic_score,
       final_interview_score,
       final_decision
  )
     st.session_state.saved_result=True

     st.markdown(f"""
     <div class="hero">
     <h3>🎯 Final Interview Score</h3>
     <h1>{average_score:.1f}/100</h1>
     <p>{final_decision}</p>
     </div>
     """,unsafe_allow_html=True)
     
     col1,col2,col3 =st.columns(3)
     
     with col1:
         st.metric(
             "ATS Score",
              f"{st.session_state.ats_result['score']}%"
         )
     with col2:
         st.metric(
             "Semantic Ma",
              f"{st.session_state.semantic_score:.1f}%"
         )
         
     with col3:
         st.metric(
             "Questions Answered",
               len(st.session_state.all_scores)
         )
         
                       
     st.subheader(
                                "📈 Question-wise Score Analysis"
                        )

     fig, ax = plt.subplots(
      figsize=(8,4))
     
     fig.patch.set_facecolor("#151d4f")
     ax.set_facecolor("#151d4f")

     bars=ax.bar(
                         df["Question"],
                         df["Score"]
                        )

     ax.set_xlabel(
                         "Questions",
                          color="white"
                      )

     ax.set_ylabel(
                         "Score (/10)",
                         color="white"
                       )

     ax.set_title(
                         "Interview Performance",
                          color="white",
                          fontsize=16,
                          fontweight="bold"
                        )
     ax.tick_params(
          colors="white"
     )
     
     for spine in ax.spines.values():
         spine.set_color("white")
         
     plt.tight_layout()
                       
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

     st.markdown(f"""
     <div class="hero">
     
     <h3>🤖 AI Final Assessment</h3>
     
     <p style="
     font-size:18px;
     line-height:1.8;
     color:white;
     ">
     {final_report.replace(chr(10), "<br>")}
     </p>
     
     </div>
      """,
     unsafe_allow_html=True)              
                       
     pdf_file = generate_pdf(
                           report_text=final_report,
                            chart_file=chart_file,
                            avg_score=average_score,
                            question_scores=st.session_state.all_scores,
                            recommendation=final_decision
                        )

     st.markdown("""
     <div class="feature-card">
     <h2>📄 Professional Interview Report</h2>
     
     <p>
     Download your complete interview assessment report including performance analytics ,AI feedback,recommendations and hiring readiness insights.
     </p>
     
     </div>
     """,
     unsafe_allow_html=True)
     
     with open(
            pdf_file,
            "rb"
     )as file:
            st.download_button(
                label="⬇ Download Professional PDF Report",
                data=file,
                file_name="Interview Report.pdf",
                mime="application/pdf",
                use_container_width=True
            )

     st.success(
                     "🎉 Interview Completed!"
                    )

     st.balloons()

     st.write(
                    "Thank you for taking the interview."
                    )

     if st.button(
                         "🔄 Start New Interview"
                    ):

                        st.session_state.current_question = 0
                        
                        st.session_state.scores = []

                        st.session_state.questions = []
                        
                        st.session_state.final_report=""
                        
                        st.session_state.final_score=0
                        
                        st.session_state.final_decision=""
                        
                        st.session_state.saved_result=False

                        st.rerun()
                        
   #----------History------------------------#

    elif menu == "📚 History":
     st.title("📚 History")
      
     history=get_user_history(st.session_state.user_id)  #Fetch interview history from database for logged in user
    
     if history:
        st.subheader(
            "📊 Interview History"
        )

        df_history = pd.DataFrame(
            history,
            columns=[
                "ID",
                "Date",
                "ATS Score",
                "Semantic Score",
                "Interview Score",
                "Hiring Decision"
            ]
        )

        col1, col2,col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Total Interviews",
                len(df_history)
            )
        with col2:
            st.metric(
                "Average ATS Score",
                f"{df_history['ATS Score'].mean():.2f}%"
            )
            
        with col3:
            st.metric(
                "Average Interview Score",
                f"{df_history['Interview Score'].mean():.2f}/100"
            )
            
        st.subheader(
            "📈 Interview Performance"
        )
        
        chart_df=df_history.sort_values("ID")
        
        st.line_chart(
            chart_df["Interview Score"]
        )
        
        st.subheader(
            "📋 Detailed History")
        
        st.dataframe(
            df_history,
            use_container_width=True
        )   
     else:
        st.info(
            "No interview history found. Start your first interview!"
        )