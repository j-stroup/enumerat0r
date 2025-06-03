import logging
from urllib.parse import urljoin
import requests
import random
from bs4 import BeautifulSoup
import time
import os
import js2

from user_agents import agents


logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO)

urls_to_visit = []
visited_urls = []
known_jsfiles = []
emails = []

not_crawl = ['jpeg', '.jpg', '.pdf', '.svg', '.png', '.gif', 'webp', 'tiff', '.mp3', '.mp4']

# Log JavaScript file locations
def js_files(target, jsfile):
    if jsfile not in known_jsfiles:
        if str(target) not in str(jsfile):
            pass
        else:
            logging.info(f'FOUND: {jsfile}')
            known_jsfiles.append(jsfile)
            js2.js_scan(target, jsfile)
            file = f'{target}_js-files.txt'
            path = f'{target}/{file}'
            with open(path, 'a') as f:
                f.write(f'{jsfile}\n')
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
            jsfile = path
            if jsfile.startswith('http'):
                pass
            else:
                jsfile = urljoin(url, path)
            js_files(target, jsfile)

# Add discovered url to list if not already crawled
def add_url_to_visit(target, url):
    # Check for email or phone links
    if url and url.startswith('http'):
        pass
    else:
        if url and url.startswith('/'):
            url = f'https://{target}{url}'
        elif url and url.startswith('mailto'):
            file = f'{target}_emails.txt'
            path = f'{target}/{file}'
            url = url.replace('mailto:', '')
            url = url.split('?')
            email = url[0]
            if email not in emails:
                emails.append(email)
                with open(path, 'a') as f:
                    f.write(f'{email}\n')
                    f.close()
        elif url and url.startswith('tel'):
            pass
        else:
            url = f'https://{target}/{url}'
    if str(target) not in str(url): # Keep it in scope
        pass
    elif str(url[-4:]) in not_crawl: # Discard images and videos
        pass
    elif url and url.endswith('.txt') or url.endswith('.md'):
        file = f'{target}_txts.txt'
        path = f'{target}/{file}'
        with open(path, 'a') as f:
            f.write(f'{url}\n')
            f.close()
    elif url not in visited_urls and url not in urls_to_visit:
        urls_to_visit.append(url)

def crawl(target, url):
    agent = random.choice(agents)
    headers = {
            'User-Agent': agent
            }
    try:
        r = requests.get(url, headers=headers)
    except:
        print(f'Error: Could not get {url}')
        r = 'error'
    if str(r).startswith('<Response [3'):
        file = f'{target}_300s.txt'
        path = f'{target}/{file}'
        with open(path, 'a') as f:
            f.write(f'{url}   - {r}\n')
            f.close()
    elif str(r).startswith('<Response [4'):
        file = f'{target}_400s.txt'
        path = f'{target}/{file}'
        with open(path, 'a') as f:
            f.write(f'{url}   - {r}\n')
            f.close()
    elif str(r).startswith('<Response [5'):
        file = f'{target}_500s.txt'
        path = f'{target}/{file}'
        with open(path, 'a') as f:
            f.write(f'{url}   - {r}\n')
            f.close()

    html = requests.get(url, headers=headers).text
    for url in get_linked_urls(target, url, html):
        add_url_to_visit(target, url)

# Main function
def run(target, target_url, file, speed):
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
            path = target + '/'
            if not os.path.exists(path):
                os.makedirs(path)
            with open(os.path.join(path, file), 'a') as f:
                f.write(f'{url}\n')
                f.close()
            time.sleep(speed)

# Select target
def start(target, target_url, speed):
    urls_to_visit.append(target_url)
    file = target + '_endpoints.txt'
    run(target, target_url, file, speed)


if __name__ == '__main__':
    global target_domain
    target = input('Domain: https://')
    target_domain = 'https://' + target
    speed = input('How fast? S_low/M_edium/F_ast: ').lower()
    start(target, target_domain, speed)



"""
Finding and logging duplicate js files under subdomains
"""
