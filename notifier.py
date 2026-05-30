#!/usr/bin/env python3
# ============================================================
#   termux-notifier — by @darkvibez456
#   Send Telegram & Discord alerts from the terminal / pipes
# ============================================================

import sys
import os
import argparse
import requests

# ── ANSI colour palette ─────────────────────────────────────
R  = "\033[0m"          # reset
B  = "\033[1m"          # bold
DIM= "\033[2m"          # dim
U  = "\033[4m"          # underline

BLK= "\033[30m"
RED= "\033[91m"
GRN= "\033[92m"
YLW= "\033[93m"
BLU= "\033[94m"
MGN= "\033[95m"
CYN= "\033[96m"
WHT= "\033[97m"

BBLK= "\033[40m"
BRED= "\033[41m"
BGRN= "\033[42m"
BYLW= "\033[43m"
BBLU= "\033[44m"
BMGN= "\033[45m"
BCYN= "\033[46m"
BWHT= "\033[47m"

# ── Banner ───────────────────────────────────────────────────
BANNER = f"""
{DIM}{CYN}╔══════════════════════════════════════════════════════════╗{R}
{DIM}{CYN}║{R}  {B}{WHT}  ████████╗███████╗██████╗ ███╗   ███╗██╗   ██╗██╗  ██╗{R}  {DIM}{CYN}║{R}
{DIM}{CYN}║{R}  {B}{WHT}  ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║   ██║╚██╗██╔╝{R}  {DIM}{CYN}║{R}
{DIM}{CYN}║{R}  {B}{CYN}     ██║   █████╗  ██████╔╝██╔████╔██║██║   ██║ ╚███╔╝ {R}  {DIM}{CYN}║{R}
{DIM}{CYN}║{R}  {B}{CYN}     ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║   ██║ ██╔██╗ {R}  {DIM}{CYN}║{R}
{DIM}{CYN}║{R}  {B}{MGN}     ██║   ███████╗██║  ██║██║ ╚═╝ ██║╚██████╔╝██╔╝ ██╗{R}  {DIM}{CYN}║{R}
{DIM}{CYN}║{R}  {B}{MGN}     ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═╝{R}  {DIM}{CYN}║{R}
{DIM}{CYN}║{R}                                                          {DIM}{CYN}║{R}
{DIM}{CYN}║{R}  {BBLU}{BLK}  N O T I F I E R  {R}   {DIM}{WHT}terminal → telegram / discord{R}       {DIM}{CYN}║{R}
{DIM}{CYN}║{R}                                                          {DIM}{CYN}║{R}
{DIM}{CYN}║{R}  {B}{GRN}  DEVELOPED BY{R} {B}{YLW}@darkvibez456{R}  {DIM}{WHT}│  github.com/darkvibez456{R}  {DIM}{CYN}║{R}
{DIM}{CYN}╚══════════════════════════════════════════════════════════╝{R}
"""

# ── Credential loading ───────────────────────────────────────
def load_env():
    """Load credentials from environment variables or a local .env file."""
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if os.path.isfile(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, _, val = line.partition("=")
                    os.environ.setdefault(key.strip(), val.strip())

    return {
        "tg_token"  : os.environ.get("TG_TOKEN", ""),
        "tg_chat_id": os.environ.get("TG_CHAT_ID", ""),
        "dc_webhook": os.environ.get("DC_WEBHOOK", ""),
    }

# ── Senders ──────────────────────────────────────────────────
def send_telegram(token: str, chat_id: str, message: str) -> bool:
    """POST a message to Telegram via Bot API."""
    if not token or not chat_id:
        print(f"{RED}[✗]{R} {B}TG_TOKEN{R} or {B}TG_CHAT_ID{R} is not set.")
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id"   : chat_id,
        "text"      : message,
        "parse_mode": "Markdown",
    }
    try:
        resp = requests.post(url, json=payload, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if data.get("ok"):
            print(f"{GRN}[✓]{R} Telegram — message delivered "
                  f"{DIM}(msg_id: {data['result']['message_id']}){R}")
            return True
        else:
            print(f"{RED}[✗]{R} Telegram API error: {data.get('description', 'unknown')}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"{RED}[✗]{R} Telegram — no network connection.")
    except requests.exceptions.Timeout:
        print(f"{RED}[✗]{R} Telegram — request timed out.")
    except requests.exceptions.HTTPError as e:
        print(f"{RED}[✗]{R} Telegram — HTTP {e.response.status_code}: {e.response.text[:120]}")
    except Exception as e:
        print(f"{RED}[✗]{R} Telegram — unexpected error: {e}")
    return False


def send_discord(webhook: str, message: str) -> bool:
    """POST a message to a Discord channel via Webhook."""
    if not webhook:
        print(f"{RED}[✗]{R} {B}DC_WEBHOOK{R} is not set.")
        return False

    payload = {"content": message}
    try:
        resp = requests.post(webhook, json=payload, timeout=10)
        if resp.status_code == 204:
            print(f"{GRN}[✓]{R} Discord — message delivered.")
            return True
        else:
            print(f"{RED}[✗]{R} Discord — HTTP {resp.status_code}: {resp.text[:120]}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"{RED}[✗]{R} Discord — no network connection.")
    except requests.exceptions.Timeout:
        print(f"{RED}[✗]{R} Discord — request timed out.")
    except Exception as e:
        print(f"{RED}[✗]{R} Discord — unexpected error: {e}")
    return False

# ── Usage / help ─────────────────────────────────────────────
def print_usage():
    print(f"""
{B}{CYN}┌─  USAGE ─────────────────────────────────────────────────┐{R}
{B}{CYN}│{R}                                                          {B}{CYN}│{R}
{B}{CYN}│{R}  {B}{WHT}Direct argument:{R}                                         {B}{CYN}│{R}
{B}{CYN}│{R}    {YLW}python notifier.py tg "your message"{R}                    {B}{CYN}│{R}
{B}{CYN}│{R}    {YLW}python notifier.py dc "your message"{R}                    {B}{CYN}│{R}
{B}{CYN}│{R}    {YLW}python notifier.py both "your message"{R}                  {B}{CYN}│{R}
{B}{CYN}│{R}                                                          {B}{CYN}│{R}
{B}{CYN}│{R}  {B}{WHT}Pipe / stdin:{R}                                            {B}{CYN}│{R}
{B}{CYN}│{R}    {YLW}echo "alert" | python notifier.py tg{R}                   {B}{CYN}│{R}
{B}{CYN}│{R}    {YLW}nmap -sV 192.168.1.1 | python notifier.py dc{R}           {B}{CYN}│{R}
{B}{CYN}│{R}    {YLW}cat report.txt | python notifier.py both{R}               {B}{CYN}│{R}
{B}{CYN}│{R}                                                          {B}{CYN}│{R}
{B}{CYN}│{R}  {B}{WHT}Targets:{R}                                                 {B}{CYN}│{R}
{B}{CYN}│{R}    {GRN}tg{R}   → Telegram  (TG_TOKEN + TG_CHAT_ID)               {B}{CYN}│{R}
{B}{CYN}│{R}    {MGN}dc{R}   → Discord   (DC_WEBHOOK)                          {B}{CYN}│{R}
{B}{CYN}│{R}    {CYN}both{R} → Telegram + Discord simultaneously                {B}{CYN}│{R}
{B}{CYN}│{R}                                                          {B}{CYN}│{R}
{B}{CYN}│{R}  {B}{WHT}Flags:{R}                                                   {B}{CYN}│{R}
{B}{CYN}│{R}    {YLW}--no-banner{R}  suppress the ASCII banner (good for pipes) {B}{CYN}│{R}
{B}{CYN}│{R}    {YLW}--quiet{R}      suppress all output (silent mode)           {B}{CYN}│{R}
{B}{CYN}│{R}    {YLW}-h / --help{R}  show this menu                              {B}{CYN}│{R}
{B}{CYN}│{R}                                                          {B}{CYN}│{R}
{B}{CYN}│{R}  {DIM}Credentials loaded from .env or environment variables.{R}   {B}{CYN}│{R}
{B}{CYN}└──────────────────────────────────────────────────────────┘{R}
""")

# ── CLI ──────────────────────────────────────────────────────
def build_parser():
    parser = argparse.ArgumentParser(
        prog="notifier",
        description="termux-notifier — send alerts to Telegram and/or Discord",
        add_help=False,
    )
    parser.add_argument(
        "target",
        nargs="?",
        choices=["tg", "dc", "both"],
        help="Delivery target: tg | dc | both",
    )
    parser.add_argument(
        "message",
        nargs="?",
        default=None,
        help="Message text (omit to read from stdin)",
    )
    parser.add_argument("--no-banner", action="store_true", help="Suppress ASCII banner")
    parser.add_argument("--quiet",     action="store_true", help="Suppress all stdout")
    parser.add_argument("-h", "--help", action="store_true", help="Show usage")
    return parser

# ── Entry point ──────────────────────────────────────────────
def main():
    parser = build_parser()
    args   = parser.parse_args()

    # Redirect stdout if --quiet
    if args.quiet:
        sys.stdout = open(os.devnull, "w")

    # Banner
    if not args.no_banner and not args.quiet:
        print(BANNER)

    # Help / no target
    if args.help or not args.target:
        print_usage()
        sys.exit(0)

    # ── Collect message ──────────────────────────────────────
    message = ""
    if args.message:
        message = args.message
    elif not sys.stdin.isatty():
        # reading from a pipe
        message = sys.stdin.read().strip()
    else:
        print(f"{YLW}[?]{R} No message provided and no stdin detected.")
        print(f"    Usage: {B}python notifier.py {args.target} \"your message\"{R}")
        sys.exit(1)

    if not message:
        print(f"{RED}[✗]{R} Message is empty — nothing to send.")
        sys.exit(1)

    # ── Load credentials ─────────────────────────────────────
    creds = load_env()

    # ── Route ────────────────────────────────────────────────
    target  = args.target.lower()
    success = []

    print(f"{DIM}{CYN}─────────────────────────────────────────{R}")
    print(f"{B}{WHT}  TARGET  {R} {B}{YLW}{target.upper()}{R}")
    print(f"{B}{WHT}  LENGTH  {R} {len(message)} chars")
    print(f"{DIM}{CYN}─────────────────────────────────────────{R}\n")

    if target in ("tg", "both"):
        ok = send_telegram(creds["tg_token"], creds["tg_chat_id"], message)
        success.append(("Telegram", ok))

    if target in ("dc", "both"):
        ok = send_discord(creds["dc_webhook"], message)
        success.append(("Discord", ok))

    # ── Summary ──────────────────────────────────────────────
    print()
    all_ok = all(s for _, s in success)
    if all_ok:
        print(f"{BGRN}{BLK}  ✓ ALL NOTIFICATIONS SENT  {R}\n")
        sys.exit(0)
    else:
        failed = [n for n, s in success if not s]
        print(f"{BRED}{BLK}  ✗ FAILED: {', '.join(failed)}  {R}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()