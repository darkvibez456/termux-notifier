# termux-notifier

![Platform](https://img.shields.io/badge/Platform-Termux-black?style=for-the-badge&logo=android&logoColor=white)
![Language](https://img.shields.io/badge/Language-Python%203-blue?style=for-the-badge&logo=python&logoColor=white)
![Developer](https://img.shields.io/badge/Developer-%40darkvibez456-cyan?style=for-the-badge&logo=github&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)

> **Pipe any terminal output — nmap scans, tool logs, recon results — directly to your Telegram or Discord. No GUI. No bloat. Pure terminal.**

---

## ✦ What It Does

`termux-notifier` is a lightweight, pipe-friendly Python 3 script built for **Termux on Android**. It reads a message from a direct argument or from **stdin** (piped data) and forwards it to **Telegram** and/or **Discord** in real time.

Use it as the last stage of any automation pipeline to get instant alerts on your phone — no matter where you are.

---

## ✦ Key Features

| Feature | Detail |
|---|---|
| 📲 **Telegram Support** | Sends via Bot API (`TG_TOKEN` + `TG_CHAT_ID`) |
| 💬 **Discord Support** | Sends via Webhook URL (`DC_WEBHOOK`) |
| 🔀 **Dual Target** | Route to `tg`, `dc`, or `both` simultaneously |
| 🔗 **Pipe-Friendly** | Accepts stdin — chain with any CLI tool |
| 🔐 **Secure Credentials** | Loaded from `.env` or environment variables |
| 🎨 **Premium Banner** | ANSI colour terminal UI |
| 🤫 **Silent Mode** | `--quiet` flag for cron jobs and automation |
| ⚠️ **Error Handling** | Network timeouts, API errors, empty messages |

---

## ✦ Installation

### 1 — Update Termux & install dependencies

```bash
pkg update -y && pkg upgrade -y
pkg install python git nano -y
pip install requests
```

### 2 — Clone the repository

```bash
git clone https://github.com/darkvibez456/termux-notifier.git
cd termux-notifier
```

### 3 — Install Python requirements

```bash
pip install -r requirements.txt
```

### 4 — Create your credentials file

```bash
cp .env.example .env
nano .env
```

Fill in your credentials:

```env
TG_TOKEN=123456789:ABCDefghIJKlmnOPQRstUVwxyz
TG_CHAT_ID=987654321
DC_WEBHOOK=https://discord.com/api/webhooks/XXXXXXXXXX/YYYYYYYYYYYY
```

---

## ✦ Configuration

### Getting a Telegram Bot Token

1. Open Telegram → search **@BotFather**
2. Send `/newbot` and follow the prompts
3. Copy the token (format: `123456:ABC-...`)
4. Get your Chat ID: message **@userinfobot** or use `https://api.telegram.org/bot<TOKEN>/getUpdates`

### Getting a Discord Webhook

1. Open Discord → Server Settings → Integrations → Webhooks
2. Click **New Webhook** → choose channel → **Copy Webhook URL**

---

## ✦ Usage

### Basic syntax

```bash
python notifier.py [target] [message] [flags]
```

| Argument | Description |
|---|---|
| `tg` | Send to Telegram only |
| `dc` | Send to Discord only |
| `both` | Send to both simultaneously |
| `--no-banner` | Suppress ASCII banner |
| `--quiet` | Suppress all output (silent/cron mode) |
| `-h` / `--help` | Show the usage menu |

### Direct message

```bash
python notifier.py tg "Server is online."
python notifier.py dc "Recon phase complete."
python notifier.py both "Alert: new target found."
```

### Piped stdin

```bash
echo "ping result: host is up" | python notifier.py tg
cat /var/log/syslog | python notifier.py dc
```

---

## ✦ Ethical Hacking Pipeline Examples

> **All examples assume you have explicit written permission to test the target systems.**

### 🔍 nmap scan → Telegram

```bash
nmap -sV -O 192.168.1.0/24 | python notifier.py tg
```
Get your full nmap output delivered to Telegram the moment the scan finishes.

---

### 🌐 Subdomain enumeration → Discord

```bash
subfinder -d target.com -silent | python notifier.py dc
```

---

### 🕵️ Gobuster directory brute-force → both

```bash
gobuster dir -u http://target.com -w /usr/share/wordlists/dirb/common.txt \
  | python notifier.py both
```

---

### 📡 Nikto web scan → Telegram (silent mode)

```bash
nikto -h http://target.com | python notifier.py tg --no-banner
```

---

### 🔓 Hydra brute-force result → Telegram

```bash
hydra -l admin -P rockyou.txt ssh://192.168.1.100 \
  | grep "login:" \
  | python notifier.py tg --quiet
```

---

### 🗓️ Cron job — daily recon summary

```bash
# Run every day at 08:00 and send summary to Discord
0 8 * * * cd /data/data/com.termux/files/home/termux-notifier && \
  cat ~/recon/daily_summary.txt | python notifier.py dc --quiet
```

---

### ⛓️ Multi-tool chained pipeline

```bash
nmap -sV 10.0.0.1 -oG - \
  | grep "open" \
  | awk '{print $2, $5}' \
  | python notifier.py both
```

---

## ✦ File Structure

```
termux-notifier/
├── notifier.py        ← main script
├── .env               ← your credentials (git-ignored)
├── .env.example       ← credentials template
├── requirements.txt   ← Python dependencies
├── .gitignore         ← safety net
└── README.md          ← this file
```

---

## ✦ Security Notes

- **Never commit `.env`** — it is listed in `.gitignore`
- Telegram Bot Tokens and Discord Webhooks grant **send access** — treat them like passwords
- Rotate tokens/webhooks immediately if you suspect exposure
- Use environment variables (`export TG_TOKEN=...`) instead of `.env` in shared environments

---

## ✦ License

MIT License © 2026 **darkvibez456**  
See [LICENSE](./LICENSE) for full terms.

---

<div align="center">

**Built for the terminal. Built for Termux. Built by [@darkvibez456](https://github.com/darkvibez456)**

</div>
