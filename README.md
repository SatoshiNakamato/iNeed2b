# 🔒 XSS Scanner for Zora.co

A Python-based scanner to detect XSS vulnerabilities in form fields on Zora.co. Built for bounty hunters, researchers, and hackers testing Zora's inputs.

## 🚀 Features

- Scans all forms on a given page
- Submits a list of customizable XSS payloads
- Detects if payloads are reflected in the response
- Designed specifically for Zora.co

## 🛠️ Setup (Termux / Linux)

```bash
pkg update && pkg install python git -y
pip install requests beautifulsoup4
git clone https://github.com/SatoshiNakamato/iNeed2b
cd iNeed2b
python xss_scanner.py
