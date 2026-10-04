import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# Load Environment Variables
load_dotenv()

# Initialize Groq Client
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    st.error("GROQ_API_KEY not found! Please check your .env file.")
    st.stop()

client = Groq(api_key=api_key)

# Page Setup
st.set_page_config(page_title="PhishGuard AI", page_icon="🛡️", layout="wide")

st.title("🛡️ PhishGuard AI - Fraud & Prompt Injection Security Agent")
st.subheader("Detect Scams, AI Deepfake Messages, & Hardware Payload Attacks in Real-Time")

st.markdown("---")

# User Input Options
st.markdown("### 🔍 Input Data for Analysis")
input_type = st.radio("Select Input Category:", ["Email / SMS Scam", "AI Prompt Injection Payload", "Hardware / Microcontroller Serial Payload"])

input_text = st.text_area(
    "Enter Suspicious Content:",
    height=160,
    placeholder="Paste text, suspicious message, AI prompt, or hardware packet here..."
)

if st.button("🚨 Analyze Security Threat", type="primary", use_container_width=True):
    if not input_text.strip():
        st.warning("Please enter some content to analyze!")
    else:
        with st.spinner("Analyzing content with Groq AI Security Engine..."):
            prompt = f"""
            You are an elite Cybersecurity AI Agent evaluating potential fraud, deepfakes, and prompt injection attacks for ForgeHacks 2026.
            
            Input Category: {input_type}
            Content to analyze:
            "{input_text}"

            Perform a strict cybersecurity threat evaluation and output your findings in clear Markdown layout using section headers and bullet points (DO NOT use Markdown tables or HTML tags like <br>):

            ## 🛡️️ Threat Assessment Summary
            * **Risk Score:** [Specify 0% to 100%]
            * **Threat Level:** [SAFE / SUSPICIOUS / DANGEROUS / CRITICAL]
            * **Primary Threat Vector Identified:** [e.g., Phishing, SIM Swap/Impersonation, Prompt Injection, Buffer Overflow Logic, Malicious Payload]

            ### 🧐 Vulnerability Summary
            [Concise explanation of why this is dangerous or safe]

            ### 💡 Recommended Action Steps
            * [Step 1]
            * [Step 2]
            * [Step 3]
            """

            try:
                response = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="openai/gpt-oss-20b",
                    temperature=0.2
                )
                
                analysis = response.choices[0].message.content
                
                st.markdown("---")
                st.success("✅ Threat Assessment Complete!")

                # Quick Metric Cards Display
                col1, col2, col3 = st.columns(3)
                col1.metric("Status", "Completed", "Groq Powered")
                col2.metric("Category", input_type.split()[0])
                col3.metric("Response Latency", "< 1 Sec", "Real-time")

                st.markdown(analysis)

            except Exception as e:
                st.error(f"Error during analysis: {e}")