import robots
import subbrute
import crawler
import os

import cms_scan
import parse_endpoints as end


master_list = []

def main():
    # Select target
    target = input('Target domain: https://')

    # Select speed
    speed = input('How fast? S_low/M_edium/F_ast: ').lower()

    # Select list lengths
    list_length = input('Use S_hort/M_edium/L_ong fuzzing list: ').lower()

    # Start subdomain fuzzing
    subbrute.scan(target, speed, list_length)

    # Grab robots.txt
    robots.check_for_list(target)

    subs = f'{target}/{target}_subs.txt'
    bots = f'{target}/{target}_robots.txt'


    # Combine lists and write to new file
    try:
        with open(subs, 'r') as f:
            Lines = [line for line in f.readlines() if line.strip()]
            for line in Lines:
                if line != '':
                    target_url = line.strip()
                    # Fingerprint CMS
                    cms_scan.fingerprint(target, target_url, speed)
                    # Start crawler
            for line in Lines:
                if line != '':
                    target_url = line.strip()
                    crawler.start(target, target_url, speed)
    except Exception:
        print('No subdomains found')
        crawler.start(target, target, speed)

if __name__ == "__main__":
    main()
