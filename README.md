# **Voice-Driven Banking Prototype**  
**Empowering Financial Inclusion Through AI-Powered Voice Commands**  

## **📌 Overview**  
This prototype demonstrates a **voice-enabled banking system** that allows users to perform financial transactions using natural language commands. Built with **Large Acoustic Models (LAMs)** and NLP, it supports:  
✅ **Balance inquiries**  
✅ **Fund transfers**  
✅ **Transaction history**  
✅ **Multilingual support (English + Hindi)**  
✅ **Voice biometric authentication**  

---

## **🚀 Features**  
### **1. Speech Recognition & NLP**  
- **Whisper (OpenAI)** for high-accuracy speech-to-text  
- **Fine-tuned BERT** for intent classification (e.g., `balance_check`, `fund_transfer`)  
- **Rule-based fallback** for misunderstood commands  

### **2. Banking Operations**  
- **Mock transactions** with SQLite backend  
- **Voice authentication** (experimental)  
- **Real-time responses** via Coqui TTS  

### **3. Streamlit Web Interface**  
- Interactive dashboard  
- Voice command button  
- Transaction history visualization  

---

## **🛠️ Setup & Installation**  
### **Prerequisites**  
- Python 3.8+  
- FFmpeg (`sudo apt install ffmpeg` on Linux)  

### **Installation**  
```bash
git clone https://github.com/your-repo/voice-driven-banking.git
cd voice-driven-banking
pip install -r requirements.txt
streamlit run app.py
```



---

## **🎥 Demo**  
https://drive.google.com/file/d/14gyGeTG_mNkASm1iaKnNbZVGEsDIFwM0/view?usp=sharing

---

## **📜 Usage**  
1. **Launch the app**:  
   ```bash
   streamlit run app.py
   ```
2. **Click "Start Voice Command"** and speak naturally:  
   - *"What's my balance?"*  
   - *"Transfer 500 rupees to Priya"*  
3. View results on the dashboard!  

---

## **⚠️ Limitations**  
- **Accent sensitivity**: Works best with clear English/Hindi  
- **Offline mode**: Requires internet for Whisper (for now)  
- **Security**: Voice authentication is experimental  

---

## **📈 Future Work**  
🔹 **Integrate with Mifos X APIs**  
🔹 **Add regional language support**  
🔹 **Implement end-to-end encryption**  

---

## **🤝 Contribute**  
We welcome contributions!  
1. Fork the repo  
2. Submit PRs to `dev` branch  
3. Report issues [here](https://github.com/your-repo/issues)  


---
