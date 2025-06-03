import requests
import random
import time

from bs4 import BeautifulSoup


def detect_cms(target_url, speed):
    if speed == 's':
        speed = [2,3,4]
    elif speed == 'm':
        speed = [.5,1,2]
    elif speed == 'f':
        speed = [0,0]
    try:
        if not target_url.startswith(('http://', 'https://')):
            target_url = 'http://' + target_url

        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(target_url, headers=headers, timeout=10)
        content = response.text.lower()
        soup = BeautifulSoup(content, 'html.parser')

        # Meta generator tag
        generator = soup.find('meta', attrs={'name': 'generator'})
        if generator and 'content' in generator.attrs:
            gen_content = generator['content'].lower()
            if 'wordpress' in gen_content:
                return 'WordPress'
            elif 'joomla' in gen_content:
                return 'Joomla'
            elif 'drupal' in gen_content:
                return 'Drupal'

        # WordPress
        if '/wp-content/' in content or '/wp-includes/' in content:
            return 'WordPress'
        wp_login_check = requests.get(target_url.rstrip('/') + '/wp-login.php', headers=headers, timeout=5)
        if wp_login_check.status_code == 200 and 'wordpress' in wp_login_check.text.lower():
            return 'WordPress'

        # Joomla
        if 'content="joomla!' in content or 'com_content' in content:
            return 'Joomla'

        # Drupal
        if 'sites/all/' in content or 'drupal-settings-json' in content:
            return 'Drupal'

        # Shopify
        if 'cdn.shopify.com' in content or 'x-shopify-stage' in response.headers:
            return 'Shopify'

        # Wix
        if 'wix.com' in content or 'X-Wix-Request-Id' in response.headers:
            return 'Wix'

        # Squarespace
        if 'squarespace.com' in content or 'static.squarespace.com' in content:
            return 'Squarespace'

        # Check for endpoints for more accuate results

        return 'Unknown or Custom CMS'

    except requests.RequestException as e:
        print(f"Error accessing {target_url}: {e}")
        return 'Error'
    time.sleep(random.choice(speed))
    # Return results

def fingerprint(target, target_url, speed):
    cms = detect_cms(target_url, speed)
    file = f'{target}.txt'
    path = f'{target}/{file}'
    with open(path, 'a') as f:
        f.write(f'{target_url} is using: {cms}')
        f.close()
    print(f"{target_url} is using: {cms}")


if __name__ == "__main__":
    target_url = input("Enter a website URL: ")
    speed = 'm'
    cms = detect_cms(target_url, speed)
    print(f"{target_url} is using: {cms}")
