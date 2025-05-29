import requests
import os
import random

from user_agents import agents


def check_for_list(target):
    path = f'{target}/{target}_subs.txt'
    if not os.path.exists(path):
        target = ''
        get_robots(target)
    else:
        with open(path, 'r') as f:
            Lines = [line for line in f.readlines() if line.strip()]
            for line in Lines:
                if line != '':
                    url = line.strip()
                    get_robots(url)

def get_robots(target):
    print(f'Checking for {target}/robots.txt')

    agent = random.choice(agents)
    headers = {
            'User-Agent': agent
            }

    robot = f'{url}/robots.txt'
    print(robot)
    try:
        r = requests.get(robot, headers=headers)
    except:
        print(f'Error: Could not get {url}/robots.txt')
        r = 'error'

    if str(r) == '<Response [200]>':
        # Create directory and text file to hold list of endpoints
        if not os.path.exists(target):
            os.makedirs(target)

        output_file = target + '_robots.txt'

        # Loop through each line in robots.txt
        for line in r.text.splitlines():
            if line.endswith('*'):
                line = line.strip('*')
            if line.startswith('Allow'):
                line = line.strip('Allow: ')
                line = f'{url}{line}'
                with open(os.path.join(target, output_file), 'a', encoding="utf-8") as output:
                    output.write(f'{line}\n')
                    output.close()
            elif line.startswith('Disallow'):
                line = line.strip('Disallow: ')
                line = f'{url}{line}'
                with open(os.path.join(target, output_file), 'a', encoding="utf-8") as output:
                    output.write(f'{line}\n')
                    output.close()


if __name__ == "__main__":
    target = input('Target domain: https://')
    url = f'https://{target}'
    get_robots(target, url)




"""
Check add formatting for robots urls like https://
Remove *
"""
