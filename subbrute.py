import requests
import time
import random
import sys
import os

from user_agents import agents


def scan(target, speed, list_length):
    print('\n')
    if speed == 's':
        speed = [2,3,4]
    elif speed == 'm':
        speed = [.5,1,2]
    elif speed == 'f':
        speed = [0,0]
    if list_length == 's':
        sub_list = 'lists/subs_short.txt'
    elif list_length == 'm':
        sub_list = 'lists/subs_medium.txt'
    elif list_length == 'l':
        sub_list = 'lists/subs_long.txt'
    elif list_length == 't':
        sub_list = 'lists/test.txt'
    output_file = target + '_subs.txt'

    with open(sub_list, 'r', encoding="utf-8") as file:
        print('Sit back and relax. This will take some time.\n')
        path = target
        if not os.path.exists(path):
            os.makedirs(path)
        for item in file:
            frequency = random.choice(speed)
            time.sleep(frequency)
            item = item.strip()
            item = 'https://' + item + '.' + target
            try:
                agent = random.choice(agents)
                headers = {
                        'User-Agent': agent
                        }
                r = requests.get(item, headers=headers)
                response = str(r)
                response = response.strip('<Response []>')
                if response != '200':
                    try:
                        item_http = item.replace('https:', 'http:')
                        r = requests.get(item_http, headers=headers)
                        response = str(r)
                        response = response.strip('<Response []>')
                        item_response = item + ' | ' + response
                        print(item_response)
                        # Log interesting responses
                        with open(os.path.join(path, output_file), 'a', encoding="utf-8") as output:
                            item_response = item_http + ' | ' + response
                            output.write(f'{item_response}\n')
                            output.close()
                    except:
                        error = 'Error | ' + item_http
                        print(error)
                item_response = item + ' | ' + response
                print(item_response)
                # Log subdomains
                with open(os.path.join(path, output_file), 'a', encoding="utf-8") as output:
                    output.write(f'{item_response}\n')
                    output.close()
            except:
                error = 'Error | ' + item
                print(error)
        print('Complete')
        print('\n')
    print(f'Results saved in: {output_file}')
    return output_file


if __name__ == "__main__":
    target = input('Target domain: https://')
    speed = input('How fast? S_low/M_edium/F_ast: ').lower()
    list_length = input('Use S_hort/M_edium/L_ong list: ').lower()
    scan(target, speed, list_length)
