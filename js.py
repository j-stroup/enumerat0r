import re
import requests
import sys
from urllib.parse import urlparse
import os


# === Regex Patterns ===
url_regex = re.compile(r"https?://[^\s\"'<>]+")
api_key_regex = re.compile(r"(?i)(api_key|apikey|api-key|x-api-key)[\"'\s:]*[=:\s\"']+([A-Za-z0-9_\-]{16,})")
credential_regex = re.compile(r"(?i)(token|password|secret|access_token|auth)[\"'\s:]*[=:\s\"']+([A-Za-z0-9_\-]{8,})")


def scan_js(js_content):
    """Scan JavaScript content for sensitive data"""
    found_urls = set(url_regex.findall(js_content))
    found_api_keys = api_key_regex.findall(js_content)
    found_credentials = credential_regex.findall(js_content)

    print("\n[+] Discovered URLs:")
    for url in sorted(found_urls):
        # Add found URL to crawl list
        print("   -", url)

    print("\n[+] Possible API Keys:")
    for key in found_api_keys:
        file = f'{target}_treasure.txt'
        path = f'{target}/{file}'
        with open(path, 'a') as f:
            f.write(f'\n{js_content}   - {key[0]}: {key[1]}')
            f.close()
        print(f"   - {key[0]}: {key[1]}")

    print("\n[+] Possible Credentials/Secrets:")
    for cred in found_credentials:
        file = f'{target}_treasure.txt'
        path = f'{target}/{file}'
        with open(path, 'a') as f:
            f.write(f'\n{js_content}   - {cred[0]}: {cred[1]}')
            f.close()
        print(f"   - {cred[0]}: {cred[1]}")


if __name__ == '__main__':
    scan_js(js_content)
