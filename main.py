import robots
import subbrute
import crawler
import os
import os.path

import cms_scan
import parse_endpoints as end


master_list = []

def main():
    # Select target
    target = input('Target domain: https://')

    # Select speed
    speed = input('How fast? S_low/M_edium/F_ast: ').lower()

    # Select tools

    # Custom user agent

    # Select list lengths
    list_length = input('Use S_hort/M_edium/L_ong fuzzing list: ').lower()

    # Start subdomain fuzzing
    subbrute.scan(target, speed, list_length)

    # Grab robots.txt
    robots.check_for_list(target)

    subs = f'{target}/{target}_subs.txt'
    bots = f'{target}/{target}_robots.txt'

    try:
        if os.path.isfile(subs):
            with open(subs, 'r') as f:
                Lines = [line for line in f.readlines() if line.strip()]
                for line in Lines:
                    if line != '':
                        target_url = line.strip()
                        if target_url.endswith('200'):
                            target_url = target_url.replace(' | 200', '')
                            # Fingerprint CMS
                            cms_scan.fingerprint(target, target_url, speed)
                # Add subdomain to crawl list
                for line in Lines:
                    if line != '':
                        target_url = line.strip()
                        if target_url.endswith('200'):
                            target_url = target_url.replace(' | 200', '')
                            crawler.add_url_to_visit(target, target_url, speed)
            crawler.start(target, target_url, speed)
    except Exception:
        print('No subdomains found')
        crawler.start(target, target, speed)

if __name__ == "__main__":
    main()


'''
Simplify for line loops into one
'''
