import requests
import time
import random
import sys
import os


def scan(target):
    speed = input('How fast? S_low/M_edium/F_ast: ').lower()
    list_length = input('Use S_hort/M_edium/L_ong list: ').lower()
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
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
            }
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
                r = requests.get(item, headers=headers)
                response = str(r)
                response = response.strip('<Response []>')
                item_response = response + ' | ' + item
                sys.stdout.write('                                                                      \r')
                sys.stdout.write(item_response + '\r')
                sys.stdout.flush()
                # Log subdomains
                with open(os.path.join(path, output_file), 'a', encoding="utf-8") as output:
                    output.write(f'\n{item}')
                    output.close()
            except:
                error = 'Error | ' + item
                sys.stdout.write('                                                                      \r')
                sys.stdout.write(error + '\r')
                sys.stdout.flush()
        sys.stdout.write('                                                                              \r')
        sys.stdout.write('Complete')
        sys.stdout.flush()
        print('\n')
    print(f'Results saved in: {output_file}')
    return output_file


if __name__ == "__main__":
    target = input('Target domain: https://')
    scan(target)
