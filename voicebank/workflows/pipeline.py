from typing import Dict, Any
from voicebank.storage.inmemory import BankOperations
from voicebank.nlu.rule_based import detect_intent, extract_entities
from voicebank.models import CommandResult


bank = BankOperations()


def process_command_text(text: str, user_id: str) -> Dict[str, Any]:
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
