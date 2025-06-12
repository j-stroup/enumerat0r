import requests
from bs4 import BeautifulSoup

def check_open_directory(url):
    try:
        if not url.startswith("http"):
            url = "http://" + url
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.title.string.strip() if soup.title else ""
            if "Index of /" in title:
                print(f"[+] Open directory found: {url}")
                return True
            # Heuristic: look for links that indicate a listing
            links = soup.find_all('a')
            if any(link.get('href') and ("../" in link.get('href') or "/?" in link.get('href')) for link in links):
                print(f"[+] Possible open directory: {url}")
                return True
        else:
            print(f"[-] Unable to access {url} (status code {response.status_code})")
    except requests.RequestException as e:
        print(f"[-] Error accessing {url}: {e}")
    return False

# List of target URLs (only root or sub-paths likely to have directory listing)
targets = [
    "example.com/",
    "testphp.vulnweb.com/",
    "example.com/uploads/",
    "example.com/files/"
]

if __name__ == "__main__":
    for target in targets:
        check_open_directory(target)
