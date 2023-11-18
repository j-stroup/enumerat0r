import robots
import subbrute


def main(target):
    # Select speed

    # Select list lengths

    # Select tools to run
    robots.get_robots(target)
    subbrute.scan(target)


if __name__ == "__main__":
    target = input('Target domain: https://')
    main(target)
