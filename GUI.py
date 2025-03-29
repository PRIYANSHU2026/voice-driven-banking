# This MUST be the first Streamlit command
import streamlit as st

st.set_page_config(
    page_title="Voice-Driven Banking",
    page_icon="💰",
    layout="wide"
)

# Now import other modules
import speech_recognition as sr
from gtts import gTTS
import os
import time
import random
import numpy as np
from PIL import Image

# Fallback NLP processing
try:
    from transformers import pipeline

    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    st.warning("Transformers not available, using simple text processing")

# Mock user database
USER_DB = {
    "user123": {
        "name": "Priyanshu Tiwari",
        "balance": 1500.50,
        "transactions": [
            {"date": "2024-05-01", "description": "Salary Credit", "amount": 2000.00},
            {"date": "2024-05-03", "description": "Grocery Store", "amount": -150.75},
            {"date": "2024-05-05", "description": "Electricity Bill", "amount": -85.00}
        ]
    }
}


# Simplified NLP processing as fallback
def simple_intent_detection(text):
    text = text.lower()
    if "balance" in text:
        return "balance_inquiry"
    elif "transfer" in text or "send" in text:
        return "fund_transfer"
    return "unknown"


def simple_entity_extraction(text):
    words = text.split()
    amounts = [w for w in words if w.isdigit()]
    recipients = []
    for i, word in enumerate(words):
        if word in ["to", "for"] and i + 1 < len(words):
            recipients.append(words[i + 1])
    return amounts, recipients


# Initialize NLP pipeline with fallback
@st.cache_resource
def load_nlp_pipeline():
    if TRANSFORMERS_AVAILABLE:
        try:
            classifier = pipeline("text-classification", model="distilbert-base-uncased")
            ner = pipeline("ner", model="dslim/bert-base-NER")
            return classifier, ner
        except Exception as e:
            st.warning(f"Advanced NLP failed: {str(e)}, using simple processing")
            return None, None
    return None, None


classifier, ner = load_nlp_pipeline()


class BankOperations:
    def __init__(self):
        self.users = USER_DB

    def get_balance(self, user_id):
        return self.users.get(user_id, {}).get("balance", 0)

    def transfer_funds(self, from_user, to_user, amount):
        if from_user in self.users and self.users[from_user]["balance"] >= amount:
            self.users[from_user]["balance"] -= amount
            transaction = {
                "date": time.strftime("%Y-%m-%d"),
                "description": f"Transfer to {to_user}",
                "amount": -amount
            }
            self.users[from_user]["transactions"].append(transaction)
            return True, "Transfer successful"
        return False, "Insufficient funds"


bank = BankOperations()


def text_to_speech(text, lang='en'):
    try:
        tts = gTTS(text=text, lang=lang)
        tts.save("response.mp3")
        audio_file = open("response.mp3", "rb")
        audio_bytes = audio_file.read()
        audio_file.close()
        os.remove("response.mp3")
        return audio_bytes
    except Exception as e:
        st.error(f"Text-to-speech failed: {str(e)}")
        return None


def recognize_speech():
    try:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            st.info("Listening... Speak now (wait for 1 second after clicking)")
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source, timeout=5)
            try:
                return r.recognize_google(audio)
            except sr.UnknownValueError:
                return "Could not understand audio"
            except sr.RequestError as e:
                return f"API unavailable: {str(e)}"
    except Exception as e:
        return f"Microphone error: {str(e)}"


def process_command(text, user_id):
    if not text or text.startswith(("Could not", "API unavailable", "Microphone error")):
        return {
            "success": False,
            "response": text if text else "No command detected",
            "intent": "error"
        }

    if classifier and ner:
        try:
            intent_result = classifier(text)[0]
            intent = intent_result['label']
            entities = ner(text)
            amounts = [e['word'] for e in entities if e['entity'] == 'MONEY']
            recipients = [e['word'] for e in entities if e['entity'] in ['PER', 'ORG']]
        except:
            intent = simple_intent_detection(text)
            amounts, recipients = simple_entity_extraction(text)
    else:
        intent = simple_intent_detection(text)
        amounts, recipients = simple_entity_extraction(text)

    response = ""
    success = False

    if intent == "balance_inquiry":
        balance = bank.get_balance(user_id)
        response = f"Your current balance is {balance:.2f} rupees"
        success = True

    elif intent == "fund_transfer" and amounts and recipients:
        try:
            amount = float(amounts[0].replace(',', ''))
            recipient = recipients[0]
            success, msg = bank.transfer_funds(user_id, recipient, amount)
            response = msg
        except ValueError:
            response = "Invalid amount specified"
    else:
        response = "Sorry, I didn't understand that banking command. Please try again."

    return {
        "success": success,
        "response": response,
        "intent": intent,
        "amount": amounts[0] if amounts else None,
        "recipient": recipients[0] if recipients else None
    }


def main():
    st.title("Voice-Driven Banking Prototype")
    st.markdown("""
    <div style="background-color:#f0f2f6;padding:10px;border-radius:10px;margin-bottom:20px;">
    <h3 style="color:#2e4053;text-align:center;">Empowering Financial Inclusion Through Voice AI</h3>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("User Profile")
        user_id = st.selectbox("Select User", list(USER_DB.keys()))
        st.write(f"Welcome, {USER_DB[user_id]['name']}!")

    with col2:
        st.subheader("Voice Banking")
        st.write("""
        Try voice commands like:
        - "What's my balance?"
        - "Transfer 500 rupees to Priya"
        - "Send 1000 to mom"
        """)

        if st.button("Start Voice Command"):
            with st.spinner("Listening..."):
                command = recognize_speech()

            if command and not any(x in command for x in ["Could not", "unavailable", "error"]):
                result = process_command(command, user_id)

                st.subheader("Command Results")
                st.write(f"**You said:** {command}")

                if result['intent'] != "error":
                    st.write(f"**Detected intent:** {result['intent']}")
                    if result['amount']:
                        st.write(f"**Amount:** {result['amount']}")
                    if result['recipient']:
                        st.write(f"**Recipient:** {result['recipient']}")

                st.write(f"**Response:** {result['response']}")

                audio_bytes = text_to_speech(result['response'])
                if audio_bytes:
                    st.audio(audio_bytes, format='audio/mp3')

                if result['intent'] in ["balance_inquiry", "fund_transfer"]:
                    current_balance = bank.get_balance(user_id)
                    delta = None
                    if result['amount'] and result['intent'] == "fund_transfer":
                        try:
                            delta = -float(result['amount'].replace(',', ''))
                        except ValueError:
                            pass
                    st.metric("Current Balance",
                              f"{current_balance:.2f} INR",
                              delta=delta)
            else:
                st.error(f"Command failed: {command}")

    st.subheader("Recent Transactions")
    if user_id in USER_DB:
        transactions = sorted(USER_DB[user_id]["transactions"],
                              key=lambda x: x['date'],
                              reverse=True)

        for txn in transactions[:5]:
            amount = txn['amount']
            color = "green" if amount > 0 else "red"
            st.markdown(f"""
            <div style="padding:10px;margin:5px 0;border-left:4px solid {color};background-color:#f8f9fa;">
                <strong>{txn['date']}</strong>: {txn['description']}
                <span style="float:right;color:{color};font-weight:bold;">{amount:.2f} INR</span>
            </div>
            """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()