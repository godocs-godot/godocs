from godocs.cli.command.app_command import AppCommand


def main():
    """
    Entrypoint for the `godocs` CLI application.
    """

    app = AppCommand()

    app.main()


if __name__ == "__main__":
    main()
