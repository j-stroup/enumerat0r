import robots
import subbrute
import crawler


def main():
    # Select target
    target = input('Target domain: https://')

    # Select speed
    speed = input('How fast? S_low/M_edium/F_ast: ').lower()

    # Select list lengths
    list_length = input('Use S_hort/M_edium/L_ong fuzzing list: ').lower()

    # Select tools to run
    subbrute.scan(target, speed, list_length)
    robots.get_robots(target)
    crawler.start(target, speed)


if __name__ == "__main__":
    main()
