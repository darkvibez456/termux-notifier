# termux-notifier — Complete Repository & Termux Setup Guide
### For @darkvibez456 | github.com/darkvibez456

---

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 1 — GITHUB REPOSITORY FILES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

All 5 repository files are production-ready in the following paths:

  termux-notifier/
  ├── notifier.py        ← main script (below)
  ├── README.md          ← professional docs with badges
  ├── requirements.txt   ← requests>=2.31.0,<3.0.0
  ├── .gitignore         ← blocks .env, __pycache__, venv, etc.
  ├── .env.example       ← credential template (safe to commit)
  └── LICENSE            ← MIT 2026 © darkvibez456

---

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 2 — TERMUX LOCAL CREATION & SETUP GUIDE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## ┌─ PHASE 1: Prepare Termux ───────────────────────────────┐

### Step 1 — Update all packages
```
pkg update -y && pkg upgrade -y
```
Wait for this to finish. It will update Termux's package index
and upgrade any outdated core packages.

### Step 2 — Grant Android storage permission
```
termux-setup-storage
```
A system dialog will appear — tap ALLOW.
This lets Termux read/write to your Android storage (/sdcard).

### Step 3 — Install required tools
```
pkg install python git nano -y
```
  • python  → runs notifier.py
  • git     → clones/pushes to GitHub
  • nano    → text editor for creating/editing files

### Step 4 — Install the requests Python library
```
pip install requests
```

---

## ┌─ PHASE 2: Create the Project Locally ──────────────────┐

### Step 5 — Create and enter the project folder
```
mkdir -p ~/termux-notifier
cd ~/termux-notifier
```

### Step 6 — Open notifier.py in nano
```
nano notifier.py
```
The nano editor will open with an empty file.

### Step 7 — Paste the code
Tap and hold inside the Termux terminal to bring up the
paste option. Select PASTE to insert the full notifier.py
source code (copy it from the GitHub repo or this guide).

The file starts with:
    #!/usr/bin/env python3
    # ============================================================
    #   termux-notifier — by @darkvibez456
    ...

### Step 8 — Save and exit nano
  Ctrl + O    →  Write/save the file
  Enter       →  Confirm the filename (notifier.py)
  Ctrl + X    →  Exit nano

You will be back at the terminal prompt.

---

## ┌─ PHASE 3: Configure Credentials ──────────────────────┐

### Step 9 — Create your .env credentials file
```
nano .env
```

### Step 10 — Add your credentials inside nano
Type or paste exactly:

    TG_TOKEN=123456789:ABCDefghIJKlmnOPQRstUVwxyz
    TG_CHAT_ID=987654321
    DC_WEBHOOK=https://discord.com/api/webhooks/XXXXX/YYYYY

Replace the placeholder values with your REAL tokens.

  → Get TG_TOKEN from @BotFather on Telegram
  → Get TG_CHAT_ID from @userinfobot on Telegram
  → Get DC_WEBHOOK from Discord Server Settings → Integrations

### Step 11 — Save and exit nano
  Ctrl + O  →  save
  Enter     →  confirm
  Ctrl + X  →  exit

---

## ┌─ PHASE 4: Set Permissions & Test ─────────────────────┐

### Step 12 — Make notifier.py directly executable
```
chmod +x notifier.py
```
Now you can call it as ./notifier.py instead of python notifier.py.

### Step 13 — Verify the help menu loads
```
python notifier.py --help
```
Expected: the ANSI banner + usage table prints cleanly.

### Step 14 — Test Telegram alert
```
python notifier.py tg "Hello from Termux — Telegram test by @darkvibez456"
```
Expected output:
    ─────────────────────────────────────────
      TARGET   TG
      LENGTH   xx chars
    ─────────────────────────────────────────

    [✓] Telegram — message delivered (msg_id: 123)

    ██  ✓ ALL NOTIFICATIONS SENT  ██

Check your Telegram chat — the message should appear instantly.

### Step 15 — Test Discord alert
```
python notifier.py dc "Hello from Termux — Discord test by @darkvibez456"
```
Expected output:
    [✓] Discord — message delivered.
    ██  ✓ ALL NOTIFICATIONS SENT  ██

Check your Discord channel — message should appear instantly.

### Step 16 — Test BOTH targets simultaneously
```
python notifier.py both "Dual alert test — @darkvibez456 termux-notifier online."
```
Expected output:
    [✓] Telegram — message delivered (msg_id: ...)
    [✓] Discord  — message delivered.
    ██  ✓ ALL NOTIFICATIONS SENT  ██

### Step 17 — Test piped stdin (the real power)
```
echo "Pipe test: system is alive." | python notifier.py tg
```
```
uname -a | python notifier.py both
```
```
ls -la | python notifier.py dc --no-banner
```

---

## ┌─ PHASE 5: Push to GitHub ───────────────────────────────┐

### Step 18 — Initialise the git repo
```
cd ~/termux-notifier
git init
git branch -M main
```

### Step 19 — Create all remaining files
```
# requirements.txt
echo "requests>=2.31.0,<3.0.0" > requirements.txt

# .gitignore  (paste the full .gitignore content here)
nano .gitignore

# .env.example  (safe template — no real tokens)
nano .env.example

# LICENSE  (paste the MIT license text here)
nano LICENSE

# README.md  (paste the full README here)
nano README.md
```

### Step 20 — Stage and commit
```
git add notifier.py README.md requirements.txt .gitignore .env.example LICENSE
git commit -m "feat: initial release — termux-notifier by @darkvibez456"
```

### Step 21 — Add remote and push
```
git remote add origin https://github.com/darkvibez456/termux-notifier.git
git push -u origin main
```
Enter your GitHub username and a Personal Access Token (PAT)
when prompted. Generate a PAT at:
  github.com → Settings → Developer settings → Personal access tokens

---

## ┌─ QUICK REFERENCE CHEATSHEET ───────────────────────────┐

  COMMAND                                          RESULT
  ──────────────────────────────────────────────────────────
  python notifier.py tg "msg"                   → Telegram
  python notifier.py dc "msg"                   → Discord
  python notifier.py both "msg"                 → Both
  echo "x" | python notifier.py tg              → Pipe→TG
  nmap host | python notifier.py dc             → Pipe→DC
  cat file | python notifier.py both --quiet    → Silent
  python notifier.py --help                     → Help menu
  ──────────────────────────────────────────────────────────

  NANO SHORTCUTS
  ──────────────────────────────────────────────────────────
  Ctrl + O  →  Write (save) file
  Enter     →  Confirm filename
  Ctrl + X  →  Exit nano
  Ctrl + K  →  Cut current line
  Ctrl + U  →  Paste cut line
  Ctrl + W  →  Search in file
  ──────────────────────────────────────────────────────────

---

Built exclusively for @darkvibez456 | MIT © 2026
