from importlib.metadata import entry_points
from typing import Any


def load() -> list[Any]:
    plugins: list[Any] = []

    # Get all registered entry points for "godocs.plugins"
    for ep in entry_points(group="godocs.plugins"):
        plugin_class = ep.load()  # Import the class or function
        plugins.append(plugin_class())

    print(plugins)

    return plugins
