import streamlit as st
import time
from typing import Optional

from voicebank.storage.inmemory import BankOperations
from voicebank.nlu.rule_based import detect_intent, extract_entities
from voicebank.tts.gtts_engine import synthesize_speech

st.set_page_config(page_title="Voice-Driven Banking", page_icon="💰", layout="wide")

bank = BankOperations()


def process_text_command(text: str, user_id: str):
    intent = detect_intent(text)
    amounts, recipients = extract_entities(text)
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
        "recipient": recipients[0] if recipients else None,
    }


def main():
    st.title("Voice-Driven Banking (Modular UI)")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("User Profile")
        user_id = st.selectbox("Select User", list(bank.users.keys()))
        st.write(f"Welcome, {bank.users[user_id]['name']}!")

    with col2:
        st.subheader("Text/Voice Banking")
        st.write("Try commands like: 'What's my balance?' or 'Transfer 500 rupees to Priya'")

        text_input = st.text_input("Type a command (mic integration can be added)")
        if st.button("Run Command") and text_input:
            with st.spinner("Processing..."):
                result = process_text_command(text_input, user_id)

            st.subheader("Command Results")
            st.write(f"**You said:** {text_input}")
            if result['intent'] != "error":
                st.write(f"**Detected intent:** {result['intent']}")
                if result['amount']:
                    st.write(f"**Amount:** {result['amount']}")
                if result['recipient']:
                    st.write(f"**Recipient:** {result['recipient']}")
            st.write(f"**Response:** {result['response']}")

            audio_bytes = synthesize_speech(result['response'])
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
                st.metric("Current Balance", f"{current_balance:.2f} INR", delta=delta)

    st.subheader("Recent Transactions")
    if user_id in bank.users:
        transactions = sorted(bank.users[user_id]["transactions"], key=lambda x: x['date'], reverse=True)
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
