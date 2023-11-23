import logging
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import time
import os


logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO)

urls_to_visit = []
visited_urls = []
known_folders = []

# Log JavaScript file locations
def js_folders(folder):
    if folder not in known_folders:
        known_folders.append(folder)
        path = 'scan_results/java_script'
        if not os.path.exists(path):
            os.makedirs(path)
        with open(os.path.join(path, 'js_locations.txt'), 'a') as f:
            f.write(f'\n{folder}/')
            f.close()

# Parse HTML
def get_linked_urls(url, html):
    soup = BeautifulSoup(html, 'html.parser')

    # Find linked urls
    for link in soup.find_all('a'):
        path = link.get('href')
        if path and path.startswith('/'):
            path = urljoin(url, path)
        yield path

    # Find JavaScript file locations
    for file in soup.find_all('script'):
        path = file.get('src')
        if path and path.endswith('.js'):
            print(path)
            time.sleep(4)
            if path.startswith('/'):
                path = urljoin(url, path)
            js_url = url.split('/')
            js_url.pop(-1)
            f = '/'.join(js_url)
            print(f)
            time.sleep(4)
            js_folders(f)

# Add discovered url to list if not already crawled
def add_url_to_visit(target_domain, url):
    if str(target_domain) not in str(url):
        pass
    elif url not in visited_urls and url not in urls_to_visit:
        urls_to_visit.append(url)

def crawl(target_domain, url):
    html = requests.get(url).text
    for url in get_linked_urls(url, html):
        add_url_to_visit(target_domain, url)

# Main function
def run(target_domain, file, speed):
    if speed == 's':
        speed = 3
    elif speed == 'm':
        speed = .5
    elif speed == 'f':
        speed = 0
    while urls_to_visit:
        url = urls_to_visit.pop(0)
        logging.info(f'Crawling: {url}')
        try:
            crawl(target_domain, url)
        except Exception:
            logging.exception(f'Failed to crawl: {url}')
        finally:
            visited_urls.append(url)
            path = 'scan_results'
            if not os.path.exists(path):
                os.makedirs(path)
            with open(os.path.join(path, file), 'a') as f:
                f.write(f'\n{url}')
                f.close()
            time.sleep(speed)

# Select target
def start(target_domain, speed):
    urls_to_visit.append(target_domain)
    file = target_domain.replace('https://', '')
    file = file.replace('.', '_') + '.txt'
    run(target_domain, file, speed)


if __name__ == '__main__':
    global target_domain
    target_domain = input('Domain: https://')
    target_domain = 'https://' + target_domain
    speed = input('How fast? S_low/M_edium/F_ast: ').lower()
    start(target_domain, speed)
