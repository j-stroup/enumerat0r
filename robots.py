import requests
import os


target = input('Target domain: ')

if not os.path.exists(target):
    os.makedirs(target)

output_file = target + '_robots.txt'

headers = {
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
          }

url = f'https://{target}/robots.txt'

r = requests.get(url, headers=headers)

for line in r.text.splitlines():
    if line.startswith('Allow'):
        line = line.strip('Allow: ')
        line = f'{url}{line}'
        with open(os.path.join(target, output_file), 'a', encoding="utf-8") as output:
            output.write(f'\n{line}')
            output.close()
    elif line.startswith('Disallow'):
        line = line.strip('Disallow: ')
        line = f'{url}{line}'
        with open(os.path.join(target, output_file), 'a', encoding="utf-8") as output:
            output.write(f'\n{line}')
            output.close()
