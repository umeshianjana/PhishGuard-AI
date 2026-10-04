import os
import requests
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
PROJECTAAL_API_KEY = os.getenv("PROJECTAAL_API_KEY")

# Page Configuration
st.set_page_config(
    page_title="PhishGuard AI",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ PhishGuard AI - Fraud & Prompt Injection Security Agent")
st.markdown("Real-time threat evaluation agent for phishing, prompt injection, and hardware payloads.")

# Initialize Groq Client
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

# Helper function to generate incident report via ProjectAAL API
def generate_projectaal_report(threat_data):
    url = "https://fekvbeqwpqhlpimdemxo.supabase.co/functions/v1/v1-chat"
    headers = {
        "Authorization": f"Bearer {PROJECTAAL_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "featherless/deepseek-v3",
        "messages": [
            {
                "role": "system",
                "content": "You are an enterprise cybersecurity incident response manager. Generate a concise, formal Executive Security Incident Report in Markdown."
            },
            {
                "role": "user",
                "content": f"Generate an Incident Report based on this detected threat data:\n{threat_data}"
            }
        ],
        "stream": False
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=60)
        if response.status_code == 200:
            res_json = response.json()
            return res_json['choices'][0]['message']['content']
        else:
            return f"Error from ProjectAAL API: Status Code {response.status_code} - {response.text}"
    except Exception as e:
        return f"Failed to generate report via ProjectAAL: {str(e)}"
    payload = {
        "model": "deepseek/deepseek-chat",
        "messages": [
            {
                "role": "system",
                "content": "You are an enterprise cybersecurity incident response manager. Generate a concise, formal Executive Security Incident Report in Markdown."
            },
            {
                "role": "user",
                "content": f"Generate an Incident Report based on this detected threat data:\n{threat_data}"
            }
        ],
        "stream": False
    }
    
    try:
        # Timeout seconds 60 
        response = requests.post(url, json=payload, headers=headers, timeout=60)
        if response.status_code == 200:
            res_json = response.json()
            return res_json['choices'][0]['message']['content']
        else:
            return f"Error from ProjectAAL API: Status Code {response.status_code} - {response.text}"
    except Exception as e:
        return f"Failed to generate report via ProjectAAL: {str(e)}"

# Session state initialization
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

def get_threat_analysis(threat_type, content):
    if not client:
        st.error("Groq API Key missing. Please check your .env file.")
        return None
    
    prompt = f"""
    You are PhishGuard AI, an expert cybersecurity threat analysis agent.
    Analyze the following {threat_type}:
    
    CONTENT:
    "{content}"
    
    Provide the analysis in the following structured format:
    1. **Risk Score**: (0-100%)
    2. **Threat Level**: (SAFE / SUSPICIOUS / DANGEROUS / CRITICAL)
    3. **Vulnerability Breakdown**: Detailed technical explanation.
    4. **Actionable Mitigation Steps**: Step-by-step guidance for the user or sysadmin.
    """
    
    with st.spinner("Analyzing threat vector..."):
        try:
            response = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2
            )
            return response.choices[0].message.content
        except Exception as e:
            st.error(f"Error during analysis: {str(e)}")
            return None

# Tabs for Multi-Vector Threat Analysis
tab1, tab2, tab3 = st.tabs(["📧 Phishing / Fraud Analysis", "🤖 Prompt Injection Detection", "🔌 Hardware Payload Analysis"])

# Tab 1: Phishing
with tab1:
    st.subheader("Analyze Phishing Emails or SMS Messages")
    phish_input = st.text_area("Paste suspicious email header or body text here:", height=150)
    if st.button("Scan Email/SMS"):
        if phish_input.strip():
            st.session_state.analysis_result = get_threat_analysis("Phishing/SMS Scam", phish_input)
        else:
            st.warning("Please enter text to analyze.")

# Tab 2: Prompt Injection
with tab2:
    st.subheader("Analyze AI System Prompts for Exploits")
    prompt_input = st.text_area("Paste AI prompt or input payload here:", height=150)
    if st.button("Scan Prompt"):
        if prompt_input.strip():
            st.session_state.analysis_result = get_threat_analysis("Prompt Injection Attack", prompt_input)
        else:
            st.warning("Please enter a prompt to analyze.")

# Tab 3: Hardware Payload
with tab3:
    st.subheader("Analyze Microcontroller & Serial Stream Logs")
    hardware_input = st.text_area("Paste BadUSB / Serial communication logs here:", height=150)
    if st.button("Scan Hardware Log"):
        if hardware_input.strip():
            st.session_state.analysis_result = get_threat_analysis("Hardware Serial Payload", hardware_input)
        else:
            st.warning("Please enter hardware logs to analyze.")

# Display Results and ProjectAAL Report Button
if st.session_state.analysis_result:
    st.divider()
    st.markdown(st.session_state.analysis_result)
    st.divider()
    st.subheader("📄 ProjectAAL Security Incident Integration")
    if PROJECTAAL_API_KEY:
        if st.button("Generate Executive Incident Report (via ProjectAAL)"):
            with st.spinner("Generating formal incident report using ProjectAAL..."):
                report = generate_projectaal_report(st.session_state.analysis_result)
                st.success("Executive Incident Report Generated!")
                st.markdown(report)
                st.download_button(
                    label="📥 Download Incident Report (.md)",
                    data=report,
                    file_name="PhishGuard_Incident_Report.md",
                    mime="text/markdown"
                )
    else:
        st.info("Add PROJECTAAL_API_KEY to your .env to enable enterprise report generation.")
