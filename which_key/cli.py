from pathlib import Path
from typing import Optional

import typer

from which_key.popup import WhichKeyDialog

app = typer.Typer(add_completion=False)


def locate_config_file(config_file: Optional[str]) -> Path:
    if config_file is not None:
        path = Path(config_file).expanduser().resolve().absolute()
        if path.exists():
            return path
        else:
            typer.echo(f"No such file: {path}")
            raise typer.Exit(code=1)
    else:
        locations = [
            Path(loc).expanduser().resolve().absolute()
            for loc in ["~/.config/which-key/which-key.toml", "which-key.toml"]
        ]
        for path in locations:
            if path.exists():
                return path
        else:
            typer.echo(
                f"Could not find default config file. Please save one as {locations[0]}."
            )
            raise typer.Exit(code=1)


@app.command()
def main(
    config_file: Optional[str] = typer.Option(None, help="Path to config file"),
    prefix: str = typer.Option("", help="Show commands under a certain key prefix"),
):
    dialog = WhichKeyDialog(locate_config_file(config_file), prefix=prefix)
    dialog.run()


if __name__ == "__main__":
    app()
