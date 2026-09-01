# WhatsApp AI Chat Assistant 🤖💬

A Python-based WhatsApp AI chat assistant that monitors a WhatsApp conversation, detects new messages, generates a contextual reply using an AI model through **OpenRouter**, and automatically sends the generated response.

The project uses **PyAutoGUI** to interact with the WhatsApp desktop/web interface and the **OpenAI Python SDK** to communicate with OpenRouter.

> ⚠️ **Important:** This project automates WhatsApp through screen/keyboard/mouse interaction. Coordinate-based automation depends on your screen resolution and WhatsApp layout, so you may need to adjust the coordinates for your system.

---

## ✨ Features

- 🤖 Automatically generates WhatsApp replies using AI
- 💬 Uses the existing conversation as context
- 🔄 Continuously monitors the conversation for changes
- 📋 Copies the WhatsApp conversation automatically
- 🖱️ Uses PyAutoGUI for WhatsApp interaction
- 📤 Automatically pastes and sends generated replies
- 🧠 Uses OpenRouter's model routing
- 🔐 Keeps the API key in a separate configuration file
- 🚫 Prevents the bot from replying to its own messages

---

## 🛠️ Technologies Used

- **Python**
- **PyAutoGUI** — mouse and keyboard automation
- **Pyperclip** — clipboard operations
- **OpenAI Python SDK** — AI API communication
- **OpenRouter** — access to AI models
- **WhatsApp Web/Desktop** — chat interface

---

## 📁 Project Structure

```text
whatsapp-ai-chat-assistant/
│
├── main.py
├── coordinates.py
├── config.py
├── requirements.txt
├── .gitignore
└── README.md
```

### `main.py`

The main application.

It:

1. Opens WhatsApp.
2. Opens the configured chat.
3. Copies the current conversation.
4. Detects changes in the conversation.
5. Sends the conversation to the AI.
6. Receives a generated reply.
7. Sends the reply to WhatsApp.
8. Updates the conversation baseline to prevent replying to its own message.

### `coordinates.py`

A small utility used to find mouse cursor coordinates.

Run it while moving your mouse around the screen to determine the coordinates needed by `main.py`.

### `config.py`

Stores your API key locally.

Example:

```python
API_KEY = "YOUR_OPENROUTER_API_KEY"
```

**Do not commit this file to Git.**

### `requirements.txt`

Contains the Python packages required by the project.

### `.gitignore`

Prevents sensitive/local files such as `config.py` from being uploaded to Git repositories.

---

# 🚀 Installation

## 1. Clone the project

```bash
git clone <your-repository-url>
cd whatsapp-ai-chat-assistant
```

Or simply download the project and open the project directory.

---

## 2. Create a virtual environment

It is recommended to use a virtual environment.

### Windows

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

### macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install dependencies

Run:

```bash
pip install -r requirements.txt
```

---

# 🔑 API Key Setup

This project uses **OpenRouter** for AI requests.

Create an OpenRouter API key and put it inside your local `config.py` file:

```python
API_KEY = "YOUR_OPENROUTER_API_KEY"
```

The project imports the key in `main.py`:

```python
from config import API_KEY
```

And uses it to initialize the OpenAI client:

```python
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY,
)
```

### 🔐 Security

Make sure `config.py` is included in `.gitignore`:

```gitignore
config.py
```

Never upload your API key to GitHub or share it publicly.

If an API key has already been exposed, **revoke it and create a new one**.

---

# 📱 WhatsApp Setup

Before starting the bot:

1. Open WhatsApp Web/Desktop.
2. Log in to your WhatsApp account.
3. Make sure the required conversation is accessible.
4. Keep the WhatsApp window visible.
5. Do not move or resize the window after configuring the coordinates.

The current implementation uses fixed screen coordinates such as:

```python
pyautogui.click(1561, 1045)
pyautogui.click(358, 407)
pyautogui.click(1770, 265)
pyautogui.click(854, 975)
```

These coordinates are specific to the screen layout used while developing the project.

You will probably need to change them for your own computer.

---

# 🖱️ Finding Coordinates

The project includes `coordinates.py` to help determine screen coordinates.

Run:

```bash
python coordinates.py
```

Then move your mouse around the WhatsApp window.

The program will continuously print the cursor position:

```text
Point(x=854, y=975)
Point(x=900, y=500)
Point(x=1200, y=700)
```

Use the coordinates to update the PyAutoGUI commands in `main.py`.

For example:

```python
pyautogui.click(854, 975)
```

means:

```text
X = 854
Y = 975
```

---

# ▶️ Running the Bot

Once everything is configured, run:

```bash
python main.py
```

You should see:

```text
Bot started.
Waiting for a new WhatsApp message...
```

The program will continuously monitor the conversation.

When it detects a change:

```text
Checking for new message...
New message detected!
```

It sends the conversation to the AI and generates a response.

Example:

```text
AI WhatsApp Reply:
Sure! I'll let you know when I'm available.
```

The bot then pastes the response into WhatsApp and sends it.

---

# 🧠 How It Works

The basic workflow is:

```text
             ┌──────────────────┐
             │     WhatsApp     │
             └────────┬─────────┘
                      │
                      ▼
             Copy conversation
                      │
                      ▼
             Detect conversation
                   change
                      │
             ┌────────┴────────┐
             │                 │
          No change          Changed
             │                 │
             ▼                 ▼
          Wait              Send chat
             │              to OpenRouter
             │                 │
             │                 ▼
             │             AI generates
             │               reply
             │                 │
             │                 ▼
             │          Paste reply into
             │             WhatsApp
             │                 │
             │                 ▼
             │              Send
             │                 │
             └───────◄─────────┘
```

---

# 🤖 AI Configuration

The assistant is configured with the following role:

```text
You are a WhatsApp chat assistant.

Your job is to analyze the conversation provided by the user
and generate the best possible reply to the latest WhatsApp message.
```

The instructions tell the AI to:

- Understand the conversation context
- Generate a natural response
- Match the conversation's tone
- Keep responses concise
- Avoid mentioning that it is an AI
- Return only the message intended for WhatsApp

You can customize the `AI_ROLE` variable in `main.py` to change the assistant's behavior.

---

# 🧩 Model

The project currently uses:

```python
MODEL = "openrouter/free"
```

This allows OpenRouter to route the request through its available free-model routing.

You can change the model if you want to use a specific model supported by your OpenRouter account.

---

# 🔄 Message Detection

The bot stores the current conversation:

```python
previous_chat = copy_chat()
```

It then repeatedly copies the conversation:

```python
current_chat = copy_chat()
```

And compares the two:

```python
if current_chat == previous_chat:
    print("No new message.")
```

If the conversation has changed, the bot generates a response.

After sending its own response, it captures the updated conversation:

```python
previous_chat = copy_chat()
```

This prevents the bot from continuously responding to its own messages.

---

# ⚙️ Configuration

The following parts may need customization depending on your computer:

### WhatsApp opening button

```python
pyautogui.click(1561, 1045)
```

### Chat selection

```python
pyautogui.click(358, 407)
```

### Conversation area

```python
pyautogui.click(1770, 265)

pyautogui.moveTo(1770, 265)
pyautogui.dragTo(
    1781,
    904,
    duration=1.0,
    button="left"
)
```

### Message input

```python
pyautogui.click(854, 975)
```

These values are based on screen coordinates and may be different on another computer.

---

# ⚠️ Limitations

Because the project uses coordinate-based automation, it has some limitations.

### 1. Screen resolution dependency

The coordinates may not work correctly on different screen resolutions.

### 2. Window position dependency

Moving or resizing the WhatsApp window can cause the automation to click the wrong location.

### 3. UI changes

If WhatsApp changes its interface, existing coordinates may stop working.

### 4. Timing dependency

The project uses `time.sleep()` to wait for WhatsApp actions.

For example:

```python
time.sleep(5)
```

A slower computer or internet connection may require longer delays.

### 5. Conversation detection

The current implementation detects changes by comparing the copied conversation text. Any change in the copied chat can potentially trigger processing.

---

# 🛡️ Safety & Privacy

Be careful when using an AI system with personal conversations.

The application sends the copied conversation to the configured AI service for generating a response.

Avoid using the bot with conversations containing sensitive information unless you understand and accept how the configured AI service processes that data.

Also:

- Never share your API key.
- Never commit `config.py`.
- Do not publish private conversations.
- Review AI-generated messages before using the project in important conversations.
- Keep your API key permissions and usage under control.

---

# 🐛 Troubleshooting

## `ModuleNotFoundError`

Install the dependencies:

```bash
pip install -r requirements.txt
```

---

## PyAutoGUI clicks the wrong location

Run:

```bash
python coordinates.py
```

Find the correct coordinates and update `main.py`.

---

## The bot doesn't detect messages

Check that:

- WhatsApp is open.
- The correct chat is selected.
- The conversation is being copied correctly.
- The coordinates are correct.
- WhatsApp is not minimized.
- The application has permission to control the mouse/keyboard.

---

## The AI request fails

Check:

- Your API key is valid.
- Your OpenRouter account has access to the selected model.
- Your internet connection is working.
- The OpenAI package is installed correctly.

You can reinstall the SDK with:

```bash
pip install -r requirements.txt
```

---

# 📌 Future Improvements

Some possible improvements for future versions:

- [ ] Replace fixed coordinates with image recognition
- [ ] Add configurable WhatsApp chat selection
- [ ] Use environment variables instead of `config.py`
- [ ] Add logging
- [ ] Add error handling
- [ ] Add configurable response delay
- [ ] Add a pause/resume feature
- [ ] Detect only incoming messages instead of any chat change
- [ ] Add a graphical user interface
- [ ] Add support for multiple conversations
- [ ] Add better message parsing
- [ ] Add configurable AI personality
- [ ] Add a dry-run/test mode before sending messages

---

# 📄 License

This project is provided for educational and personal-use purposes.

Make sure your use of WhatsApp automation complies with WhatsApp's applicable terms and policies.

---

# ⭐ Acknowledgements

This project uses:

- Python
- PyAutoGUI
- Pyperclip
- OpenAI Python SDK
- OpenRouter
- WhatsApp

---

## 👨‍💻 Author

**Sanju**

If you find this project useful, consider giving it a ⭐ on GitHub.
