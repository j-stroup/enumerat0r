import requests
import os
import random

from user_agents import agents


robots_endpoints = []


def check_for_list(target):
    path = f'{target}/{target}_subs.txt'
    if not os.path.exists(path):
        url = f'https://{target}'
        get_robots(target, url)
    else:
        url = f'https://{target}'
        get_robots(target, url)
        with open(path, 'r') as f:
            Lines = [line for line in f.readlines() if line.strip()]
            for line in Lines:
                if line != '':
                    url = line.strip()
                    if url.endswith('200'):
                        url = url.replace(' | 200', '')                    
                    get_robots(target, url)

def get_robots(target, url):
    print(f'Checking for {url}/robots.txt')

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
            if line not in robots_endpoints:
                robots_endpoints.append(line)
                if line.endswith('*'):
                    line = line.strip('*')
                if line.startswith('Allow'):
                    line = line.replace('Allow: ', '')
                    line = f'{url}{line}'
                    with open(os.path.join(target, output_file), 'a', encoding="utf-8") as output:
                        output.write(f'{line}\n')
                        output.close()
                elif line.startswith('Disallow'):
                    line = line.replace('Disallow: ', '')
                    if line.strip() != '/':
                        line = f'{url}{line}'
                        with open(os.path.join(target, output_file), 'a', encoding="utf-8") as output:
                            output.write(f'{line}\n')
                            output.close()


if __name__ == "__main__":
    target = input('Target domain: https://')
    url = f'https://{target}'
    get_robots(target, url)
