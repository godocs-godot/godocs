import typer

TRANSLATORS = ["rst"]

MODELS = ["rst"]

app = typer.Typer(help="Godot Docs generator CLI")

# Sub-app for "construct"
construct_app = typer.Typer(
    help="Construct documentation with a chosen backend"
)

# Add construct subcommand
app.add_typer(construct_app, name="construct")


@app.callback()
def main(
    translator: str = typer.Option(
        "rst",
        "-t",
        "--translator",
        help=f"Which translator to use. Can be one of {TRANSLATORS} or a path to a script that has a Translator implementation.",
    )
):
    """
    Main CLI entrypoint.
    """
    typer.echo(f"Using translator: {translator}")


# Add jinja subcommand to constructor
@construct_app.command("jinja")
def construct_jinja(
    model: str = typer.Option(
        "rst",
        "-m",
        "--model",
        help=f"Which model to use. Can be one of {MODELS} or a path to a model directory."
    ),
    templates: str = typer.Option(
        None,
        "-T",
        "--templates",
        help="Path to directory with Jinja templates."
    ),
    filters: str = typer.Option(
        None,
        "-F",
        "--filters",
        help="Path to script with Jinja filter functions."
    ),
    builders: str = typer.Option(
        None,
        "-B",
        "--builders",
        help="Path to script with builders dict."
    ),
    input_dir: str = typer.Argument(
        ...,
        help="Input directory with XML documentation files."
    ),
    output_dir: str = typer.Argument(
        ...,
        help="Output directory to save generated documentation."
    ),
):
    """
    Construct docs using the Jinja constructor.
    """
    typer.echo(f"[Jinja] Model: {model}")
    typer.echo(f"[Jinja] Templates: {templates}")
    typer.echo(f"[Jinja] Filters: {filters}")
    typer.echo(f"[Jinja] Builders: {builders}")
    typer.echo(f"[Jinja] In: {input_dir}, Out: {output_dir}")


# === FUTURE CONSTRUCTOR EXAMPLE ===
@construct_app.command("something-else")
def construct_other(
    config: str = typer.Option(
        ...,
        "--config",
        help="Path to config file"
    ),
    in_dir: str = typer.Argument(..., help="Input directory"),
    out_dir: str = typer.Argument(..., help="Output directory"),
):
    """
    Construct docs using a different constructor.
    """
    typer.echo(f"[Other] Config: {config}")
    typer.echo(f"[Other] In: {in_dir}, Out: {out_dir}")


if __name__ == "__main__":
    app()
