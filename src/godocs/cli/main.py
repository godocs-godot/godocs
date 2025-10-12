from godocs.cli.command.app_command import AppCommand
from godocs import plugin


def main():
    """
    Entrypoint for the `godocs` CLI application.
    """

    app = AppCommand()

    plugins = plugin.load()

    # TODO: make register_plugin work with Plugin instances, besides the already accepted scripts
    # (but make the scripts require Plugin implementations as well), calling their register method passing the app
    for p in plugins:
        app.register_plugin(p)

    app.main()


if __name__ == "__main__":
    main()
