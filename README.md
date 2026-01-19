# **Voice-Driven Banking**
Empowering financial inclusion with voice-first banking for low-resource languages.

## **📌 Overview**
This project enables voice-driven banking so users can speak intents like balance checks and transfers without navigating complex UIs. The system targets rural and underserved communities and is being built to support regional languages and accents with secure voice biometrics.

- **Technical**: LAM/STT for regional languages, multilingual NLU, voice biometrics, modular backend.
- **Business**: Expanded access and lower service costs via automation.
- **Social**: Accessibility for non‑literate users and improved digital inclusion.

> Status: Modular Streamlit + FastAPI prototype with rule-based NLU, in‑memory banking ops, gTTS responses, and Selenium executor scaffolding. LAM/STT, biometrics, and core-banking integrations are planned next.

---

## **🚀 Capabilities**
- **Streamlit UI (modular)** and legacy prototype UI.
- **Rule-based NLU** for `balance_inquiry` and `fund_transfer`.
- **In‑memory banking store** with mock users and transactions.
- **Text-to-speech** via gTTS with audio playback in UI.
- **FastAPI** endpoint for text command processing.
- **Selenium executor** scaffold (headless, opt‑in).

### Roadmap (Planned)
- LAM/STT: Whisper (local/API) or Vosk/Coqui for low‑resource/offline.
- Intent with transformers/LLM, multilingual slot extraction.
- Voice biometrics (enrollment/verification) for secure auth.
- Real persistence (SQLite/Postgres) and Mifos X integration.
- Regional language packs and accessibility improvements.
- End‑to‑end encryption and compliance hardening.

---

## **🧱 Architecture & Structure**
```
.
├── app.py                       # Streamlit entrypoint (modular UI)
├── GUI.py                       # Legacy prototype UI
├── requirements.txt
├── ui/
│   └── streamlit_app.py         # Modular Streamlit page
└── voicebank/
    ├── api/
    │   └── server.py            # FastAPI app
    ├── actions/
    │   ├── base.py
    │   └── selenium_executor.py # Headless Selenium (opt-in)
    ├── biometrics/
    │   └── stub.py              # Voice auth placeholder
    ├── config.py                # Env configuration
    ├── models.py                # Pydantic models
    ├── nlu/
    │   └── rule_based.py        # Simple intent + entity extraction
    ├── storage/
    │   └── inmemory.py          # Mock user data
    ├── stt/
    │   └── base.py              # STT interface for LAMs/ASR
    ├── tts/
    │   └── gtts_engine.py       # TTS implementation (gTTS)
    └── workflows/
        └── pipeline.py          # Orchestration (text -> action)
```

Prototype data flow:
Speech/Text → NLU → Workflow → Banking store/Selenium → Response → TTS

---

## **🛠️ Setup & Installation**
### Prerequisites
- Python 3.8+
- Optional: Chrome (for Selenium)
- Optional: FFmpeg (useful for some STT/TTS; not required for gTTS)

### Installation
```bash
git clone https://github.com/your-repo/voice-driven-banking.git
cd voice-driven-banking
pip install -r requirements.txt
```

### Environment configuration
Create a `.env` (optional):
```bash
# Optional: for future LLM/STT integrations
OPENAI_API_KEY=sk-...

# Default language for prompts/tts
DEFAULT_LANGUAGE=en

# Enable headless Selenium flows (0/1)
ALLOW_SELENIUM=0
```
Note: `ALLOW_SELENIUM=1` requires Chrome installed.

---

## **📜 Usage**
### Streamlit UI (modular)
```bash
streamlit run app.py
```
Try commands like:
- "What's my balance?"
- "Transfer 500 rupees to Priya"

### Legacy prototype UI (mic input)
```bash
streamlit run GUI.py
```

### FastAPI backend
```bash
uvicorn voicebank.api.server:app --reload
```
Quick test:
```bash
curl -X POST http://127.0.0.1:8000/workflows/command \
  -H 'Content-Type: application/json' \
  -d '{"user_id":"user123","text":"transfer 500 to Priya"}'
```

### Optional: enable Selenium executor
```bash
export ALLOW_SELENIUM=1   # requires Chrome installed
```

---

## **🎥 Demo**
https://drive.google.com/file/d/14gyGeTG_mNkASm1iaKnNbZVGEsDIFwM0/view?usp=sharing

---

## **⚠️ Limitations**
- Modular UI uses text input; legacy UI uses mic with Google STT.
- Offline/on‑device STT (Whisper/Vosk) not yet integrated here.
- Voice biometrics is a placeholder and not production‑ready.
- Selenium flows are scaffolds and not wired to real banking portals.

---

## **📈 Future Work**
- Integrate with Mifos X APIs and real cores.
- Add regional/low‑resource language support (on‑device where possible).
- Implement end‑to‑end encryption + secret management.
- LAM/STT integration (Whisper local/API, Vosk/Coqui).
- Voice biometrics enrollment/verification.
- Replace in‑memory storage with SQLite/Postgres.
- Expand Selenium workflows (login, balance, transfer).
- Analytics dashboards for usage and model quality.

---

## **🔒 Security & Privacy**
- Do not store raw audio/biometrics without consent and compliance.
- Use HTTPS and environment variables for secrets.
- Keep a fallback authentication factor while biometrics are experimental.
- Follow local data protection regulations for deployment.

---

## **🤝 Contribute**
We welcome contributions!
1. Fork the repo
2. Submit PRs to `dev` branch
3. Report issues [here](https://github.com/your-repo/issues)

---
