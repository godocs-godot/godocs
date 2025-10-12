from godocs.cli.command import AppCommand
from godocs import plugin


def main():
    """
    Entrypoint for the `godocs` CLI application.
    """

    # Loads plugins
    plugins = plugin.load()

    # Instantiates main app
    app = AppCommand()

    # Registers the loaded plugins
    for p in plugins:
        app.register_plugin(p)

    app.main()


if __name__ == "__main__":
    main()
