import bmac_client
import env_parser


def main():
    env_parser.load_env()

    # Run these as scheduled tasks or upon a certain event.
    bmac_client.init_subscriptions()
    bmac_client.clear_expired_subscribers()
    # ###


if __name__ == "__main__":
    main()
