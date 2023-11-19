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
js_files = []

# Log JavaScript file locations
def list_js_files(target, js_file):
    if js_file not in js_files:
        js_files.append(js_file)
        path = target.strip('https://')
        path = f'{path}'
        if not os.path.exists(path):
            os.makedirs(path)
        with open(os.path.join(path, 'js_files.txt'), 'a') as f:
            f.write(f'\n{js_file}')
            f.close()

# Parse HTML
def get_linked_urls(target, url, html):
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
            if path.startswith('/'):
                path = urljoin(url, path)
            list_js_files(target, path)

# Add discovered url to list if not already crawled
def add_url_to_visit(target, url):
    if str(target) not in str(url):
        pass
    elif url not in visited_urls and url not in urls_to_visit:
        urls_to_visit.append(url)

def crawl(target, url):
    html = requests.get(url).text
    for url in get_linked_urls(target, url, html):
        add_url_to_visit(target, url)

# Main function
def run(target, file, speed):
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
            crawl(target, url)
        except Exception:
            logging.exception(f'Failed to crawl: {url}')
        finally:
            visited_urls.append(url)
            path = target.strip('https://')
            if not os.path.exists(path):
                os.makedirs(path)
            with open(os.path.join(path, file), 'a') as f:
                f.write(f'\n{url}')
                f.close()
            time.sleep(speed)

# Select target
def start(target, speed):
    target = 'https://' + target
    urls_to_visit.append(target)
    file = target.replace('https://', '')
    file = file + '_endpoints.txt'
    run(target, file, speed)


if __name__ == '__main__':
    global target
    target = input('Domain: https://')
    speed = input('How fast? S_low/M_edium/F_ast: ').lower()
    start(target, speed)
