# 🛡️ PhishGuard AI - Fraud & Prompt Injection Security Agent
**ForgeHacks Online 2026 Submission | Track: AI + Cybersecurity**

PhishGuard AI is an ultra-fast, real-time threat evaluation agent designed to analyze and mitigate modern digital security risks—ranging from standard phishing scams to LLM prompt injection attacks, malicious hardware/microcontroller serial payloads, and executive security incident reporting.

---

## 🚀 Features
- **Multi-Vector Threat Analysis:** Evaluates email/SMS scams, AI prompt injections, and hardware serial logs.
- **Instant Risk Scoring:** Provides a percentage-based risk score along with threat severity levels (SAFE, SUSPICIOUS, DANGEROUS, CRITICAL).
- **Executive Security Incident Reporting (via ProjectAAL):** Seamlessly generates enterprise-ready executive incident response reports using the ProjectAAL API powered by DeepSeek-v3.
- **Vulnerability Breakdown:** Gives clear, technical explanations of potential vectors and security flaws.
- **Actionable Guidance:** Provides immediate mitigation steps for end-users or sysadmins.
- **Low Latency:** Powered by Groq's high-speed AI inference engine for sub-second analysis.

---

## 🛠️ Tech Stack
- **Frontend:** Streamlit
- **Threat Engine:** Groq API (openai/gpt-oss-20b)
- **Executive Report Engine:** ProjectAAL API (featherless/deepseek-v3)
- **Language:** Python 3.10+
- **Environment Management:** python-dotenv

---

## ⚙️ Setup & Installation Instructions

### 1. Clone the Repository
git clone https://github.com/umeshianjana/PhishGuard-AI.git
cd PhishGuard-AI

### 2. Install Dependencies
pip install -r requirements.txt

### 3. Configure Environment Variables
Create a .env file in the root directory and add your API keys:
GROQ_API_KEY=your_groq_api_key_here
PROJECTAAL_API_KEY=your_projectaal_api_key_here

### 4. Run the Application
streamlit run app.py

---

## 📄 Output
- **Real-Time Threat Analysis Dashboard**
- **Downloadable Executive Incident Reports (.md)**
