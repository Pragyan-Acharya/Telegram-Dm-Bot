# Telegram-Dm-Bot
A high-performance, asynchronous Telegram bot that serves as a direct messaging bridge. It automatically forwards messages from users to an administrator and allows the admin to securely reply directly to users from their own chat.

Built with Python and `python-telegram-bot`, it utilizes `asyncio` for non-blocking operations and `python-dotenv` for secure environment variable management.

---

## ✨ Features

* **Two-Way Messaging:** Seamlessly forwards user messages to the admin and routes admin replies back to the specific user.
* **Fully Asynchronous:** Uses `asyncio` and `nest_asyncio` for fast, non-blocking message handling capable of handling multiple users simultaneously.
* **Secure Configuration:** Keeps sensitive tokens out of the source code using a local `credentials.txt` file.
* **Lightweight:** Minimal dependencies and easy to deploy on any server or cloud platform.

---

## 🛠️ Tech Stack

* **Language:** Python 3.8+
* **Core Framework:** `python-telegram-bot` (v20+)
* **Asynchronous Execution:** `asyncio`, `nest_asyncio`
* **Environment Management:** `python-dotenv`, `os`

---

## 📂 Folder Structure

```text
telegram-dm-bot/
│
├── bot.py             # Main bot script containing handlers and async logic
├── credentials.txt    # Configuration file for tokens and IDs (DO NOT COMMIT)
└── README.md          # Project documentation
```

---

# 🚀 Setup & Installation

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/Pragyan-Acharya/Telegram-Dm-Bot.git
cd telegram-dm-bot
```

## 2️⃣ Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

If you don't have a `requirements.txt` yet:

```bash
pip install python-telegram-bot python-dotenv nest-asyncio
```

---

## 4️⃣ Configure Credentials

Create a `credentials.txt` file:

```txt
BOT_TOKEN=your_bot_token_here
ADMIN_ID=your_telegram_user_id
```



---

# 💻 Running Locally

Start the bot with:

```bash
python bot.py
```

If everything is configured correctly, your bot should now be online and forwarding messages.

---

# ☁️ Deployment Guide

## 🚀 Deploy on Railway

1. Push your project to GitHub
2. Create an account on Railway
3. Create a new project and connect your repository
4. Add environment variables:

   * `BOT_TOKEN`
   * `ADMIN_ID`
5. Deploy the project

---

## 🟣 Deploy on Render

1. Push code to GitHub
2. Create a new **Background Worker**
3. Connect your repository
4. Set build command:

```bash
pip install -r requirements.txt
```

5. Set start command:

```bash
python bot.py
```

6. Add environment variables and deploy

---

## 🐳 Deploy with Docker

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "bot.py"]
```

### Build & Run

```bash
docker build -t telegram-dm-bot .
docker run -d telegram-dm-bot
```

---

# 🔒 Security Notes

* Never expose your bot token publicly
* Always use environment variables or private config files
* Add sensitive files to `.gitignore`
* Regenerate your bot token immediately if leaked

---

# 📜 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

Developed with ❤️ using Python and Telegram Bot API.

