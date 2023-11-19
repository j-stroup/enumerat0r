import requests
import os


def check_for_list(target):
    path = f'{target}/{target}_subs.txt'
    if not os.path.exists(path):
        get_robots(target)
    else:
        with open(path, 'r') as f:
            Lines = [line for line in f.readlines() if line.strip()]
            for line in Lines:
                get_robots(line)

def get_robots(target):
    print(f'Checking for {target}/robots.txt')

    headers = {
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
              }

    url = f'https://{target}/robots.txt'

    r = requests.get(url, headers=headers)

    if str(r) == '<Response [200]>':
        # Create directory and text file to hold list of endpoints
        if not os.path.exists(target):
            os.makedirs(target)

        output_file = target + '_robots.txt'

        # Loop through each line in robots.txt
        for line in r.text.splitlines():
            if line.startswith('Allow'):
                line = line.strip('Allow: ')
                line = f'https://{target}{line}'
                with open(os.path.join(target, output_file), 'a', encoding="utf-8") as output:
                    output.write(f'\n{line}')
                    output.close()
            elif line.startswith('Disallow'):
                line = line.strip('Disallow: ')
                line = f'https://{target}{line}'
                with open(os.path.join(target, output_file), 'a', encoding="utf-8") as output:
                    output.write(f'\n{line}')
                    output.close()

    print('Finished')


if __name__ == "__main__":
    target = input('Target domain: https://')
    check_for_list(target)
