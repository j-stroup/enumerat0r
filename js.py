import re
import requests
import sys
from urllib.parse import urlparse
import os
import crawler


# === Regex Patterns ===
url_regex = re.compile(r"https?://[^\s\"'<>]+")
api_key_regex = re.compile(r"(?i)(api_key|apikey|api-key|x-api-key)[\"'\s:]*[=:\s\"']+([A-Za-z0-9_\-]{16,})")
credential_regex = re.compile(r"(?i)(token|password|secret|access_token|auth)[\"'\s:]*[=:\s\"']+([A-Za-z0-9_\-]{8,})")

def fetch_js_content(target, jsfile):
    """Fetch JS content from URL or file"""
    if jsfile.startswith("http://") or jsfile.startswith("https://"):
        try:
            response = requests.get(jsfile, timeout=10)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"[!] Failed to fetch {jsfile}: {e}")
            return ""
    elif os.path.isfile(jsfile):
        try:
            with open(jsfile, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        except Exception as e:
            print(f"[!] Failed to read file {jsfile}: {e}")
            return ""
    else:
        print("[!] Invalid input: must be a URL or a local file path.")
        return ""

def scan_js(target, jsfile):
    """Scan JavaScript content for sensitive data"""
    found_urls = set(url_regex.findall(jsfile))
    found_api_keys = api_key_regex.findall(jsfile)
    found_credentials = credential_regex.findall(jsfile)

    for url in sorted(found_urls):
        crawler.add_url_to_visit(target, url)
        print("\n[+] Discovered URLs:")
        print("   -", url, "\n")

    for key in found_api_keys:
        print("\n[+] Possible API Keys:")
        file = f'{target}_treasure.txt'
        path = f'{target}/{file}'
        with open(path, 'a') as f:
            f.write(f'\n{jsfile}   - {key[0]}: {key[1]}')
            f.close()
        print(f"\nAPI KEYS ({jsfile})   - {key[0]}: {key[1]}\n")

    for cred in found_credentials:
        print("\n[+] Possible Credentials/Secrets:")
        file = f'{target}_treasure.txt'
        path = f'{target}/{file}'
        with open(path, 'a') as f:
            f.write(f'\n{jsfile}   - {cred[0]}: {cred[1]}')
            f.close()
        print(f"\nCREDENTIALS ({jsfile})  - {cred[0]}: {cred[1]}\n")


if __name__ == '__main__':
    scan_js(js_content)





"""
Fix out of scope logging of js files.
Are js files found in js files being scanned?
Log none js file urls that are found in js files.
"""
