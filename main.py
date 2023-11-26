import robots
import subbrute
import crawler
import os


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
    master = f'{target}/{target}_master.txt'

    # Add all subdomains to master list of URLs to be crawled
    if os.path.exists(subs):
        with open(subs, 'r') as f:
            Lines = [line for line in f.readlines() if line.strip()]
            for line in Lines:
                if line not in master_list:
                    master_list.append(line)
            f.close()

    # Add all endpoints discovered in robots.txt to master list of URLs to be crawled
    if os.path.exists(bots):
        with open(bots, 'r') as f:
            Lines = [line for line in f.readlines() if line.strip()]
            for line in Lines:
                if line not in master_list:
                    master_list.append(line)
            f.close()

    # Combine lists and write to new file
    with open(master, 'a') as f:
        for item in master_list:
            item.strip()
            f.write(item)
        f.close()

    # Start crawler
    crawler.check_for_list(target, speed)


if __name__ == "__main__":
    main()
