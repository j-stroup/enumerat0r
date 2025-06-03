import re
import math
import requests
import random
import os
from datetime import datetime
from urllib.parse import urlparse

from user_agents import agents
import crawler


def calculate_shannon_entropy(data):
    if not data:
        return 0
    entropy = 0
    length = len(data)
    for x in set(data):
        p_x = data.count(x) / length
        entropy -= p_x * math.log2(p_x)
    return entropy

def find_high_entropy_strings(js_code, threshold=4.5, min_length=20):
    string_literals = re.findall(r'["\']([a-zA-Z0-9+/=]{%d,})["\']' % min_length, js_code)
    high_entropy = []
    for s in string_literals:
        entropy = calculate_shannon_entropy(s)
        if entropy >= threshold:
            high_entropy.append((s, round(entropy, 2)))
    return high_entropy

def scan_javascript(js_code):
    patterns = {
        "URLs": r'https?://[^\s\'"]+',
        "Relative Endpoints": r'["\'](/[^"\']+)[\'"]',
        "API Keys": r'(?:api[_-]?key|token|access[_-]?token)[\'"\s:=]+[\'"]?[a-zA-Z0-9_\-]{16,}',
        "Hardcoded Credentials": r'(username|user|email|password|passwd|pwd|secret)[\'"\s:=]+[\'"]?[^\s\'"]+',
    }

    findings = {}

    for label, pattern in patterns.items():
        matches = re.findall(pattern, js_code, re.IGNORECASE)
        if matches:
            findings[label] = list(set(matches))

    entropy_hits = find_high_entropy_strings(js_code)
    if entropy_hits:
        findings["High Entropy Strings"] = [f"{s} (Entropy: {e})" for s, e in entropy_hits]

    return findings

def sanitize_filename(jsfile):
    parsed = urlparse(jsfile)
    base = os.path.basename(parsed.path)
    if not base:
        base = "downloaded_script.js"
    return re.sub(r'[^\w\-_.]', '_', base)

def log_findings(target, results, jsfile):
    filename = f"{target}/{target}_js-treasure.txt"
    with open(filename, 'a') as f:
        f.write(f"\n\n**********************************************************************************\nURL: {jsfile}\nGenerated: {datetime.now()}\n\n")
        if not results:
            print("✅ No sensitive content found.\n")
        else:
            for category, items in results.items():
                f.write(f"--- {category} ---\n")
                for item in items:
                    f.write(f"{item}\n")
                f.write("\n")
    return filename

def fetch_javascript(jsfile):
    try:
        agent = random.choice(agents)
        headers = {
                'User-Agent': agent
                }
        response = requests.get(jsfile, headers=headers, timeout=10)
        response.raise_for_status()
        if 'javascript' not in response.headers.get('Content-Type', ''):
            print("[!] Warning: Content doesn't appear to be JavaScript.")
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"[!] Failed to fetch URL: {e}")
        return None

def js_scan(target, jsfile):
    print(f"📥 Fetching: {jsfile}")
    js_code = fetch_javascript(jsfile)
    if not js_code:
        return

    print("🔍 Scanning JavaScript content...")
    results = scan_javascript(js_code)

    report_file = log_findings(target, results, jsfile)
    print(f"✅ Scan complete. Results saved to: {report_file}")


if __name__ == "__main__":
    import sys

    js_scan()
