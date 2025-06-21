from src.utils.utils_agents import setup_agents, runner


def main():
    inires_flock = setup_agents()
    result = runner(inires_flock, "")
    return result


if __name__ == "__main__":
    main()
