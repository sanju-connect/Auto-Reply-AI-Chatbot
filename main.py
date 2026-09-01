import time

import pyautogui
import pyperclip
from openai import OpenAI

from config import API_KEY


# ============================================================
# API CONFIGURATION
# ============================================================

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY,
)

MODEL = "openrouter/free"


# ============================================================
# AI ROLE / INSTRUCTIONS
# ============================================================

AI_ROLE = """
You are a WhatsApp chat assistant.

Your job is to analyze the conversation provided by the user
and generate the best possible reply to the latest WhatsApp message.

Rules:
- Understand the conversation context before replying.
- Make the reply natural and relevant.
- Match the tone of the conversation.
- Keep the reply concise unless a longer response is necessary.
- Do not mention that you are an AI.
- Do not explain your reasoning.
- Return only the message that should be sent on WhatsApp.
"""


# ============================================================
# WHATSAPP FUNCTIONS
# ============================================================

def open_chat():
    """Open WhatsApp and enter the chat."""
    pyautogui.click(1561, 1045)
    time.sleep(5)

    pyautogui.click(358, 407)
    time.sleep(5)


def copy_chat():
    """Select and copy the current WhatsApp conversation."""
    pyautogui.click(1770, 265)
    time.sleep(1)

    pyautogui.moveTo(1770, 265)
    pyautogui.dragTo(
        1781,
        904,
        duration=1.0,
        button="left"
    )

    pyautogui.hotkey("ctrl", "c")

    # Click the message input area again
    pyautogui.click(854, 975)
    time.sleep(1)

    return pyperclip.paste()


def send_message(message):
    """Paste and send the AI-generated WhatsApp message."""
    pyperclip.copy(message)

    pyautogui.click(854, 975)
    time.sleep(1)

    pyautogui.hotkey("ctrl", "v")
    time.sleep(1)

    pyautogui.press("enter")


# ============================================================
# AI FUNCTION
# ============================================================

def generate_reply(chat):
    """Send the chat conversation to the AI and return its reply."""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": AI_ROLE,
            },
            {
                "role": "user",
                "content": chat,
            },
        ],
        extra_body={
            "reasoning": {
                "enabled": True
            }
        }
    )

    return response.choices[0].message.content


# ============================================================
# MAIN LOOP
# ============================================================

open_chat()

# Store the current conversation.
# This prevents the bot from replying to the existing message
# when the program starts.
previous_chat = copy_chat()

print("Bot started.")
print("Waiting for a new WhatsApp message...")


while True:

    # --------------------------------------------------------
    # Get current conversation
    # --------------------------------------------------------

    current_chat = copy_chat()

    print("\nChecking for new message...")

    # --------------------------------------------------------
    # Check whether the conversation changed
    # --------------------------------------------------------

    if current_chat == previous_chat:
        print("No new message.")
        time.sleep(2)
        continue

    # --------------------------------------------------------
    # A new message/change was detected
    # --------------------------------------------------------

    print("New message detected!")

    print("\nCurrent chat:")
    print(current_chat)

    # Update previous chat before processing.
    previous_chat = current_chat

    # --------------------------------------------------------
    # Generate AI reply
    # --------------------------------------------------------

    ai_reply = generate_reply(current_chat)

    print("\nAI WhatsApp Reply:")
    print(ai_reply)

    # --------------------------------------------------------
    # Send AI reply
    # --------------------------------------------------------

    send_message(ai_reply)

    print("Reply sent.")

    # --------------------------------------------------------
    # IMPORTANT:
    # The WhatsApp conversation has now changed because
    # the bot itself sent a message.
    #
    # Capture the updated conversation and make it the new
    # baseline so the bot doesn't reply to its own message.
    # --------------------------------------------------------

    time.sleep(2)

    previous_chat = copy_chat()

    print("Waiting for another new message...")
