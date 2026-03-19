import typer
from flowproxy.core.config_loader import ConfigLoader

app = typer.Typer(help = "Flowproxy CLI")

@app.command()
def up(config_path = "flowproxy.yml"):
    try:
        print('Flow proxy is up')
        config = ConfigLoader.load_config(config_path)
        typer.echo("✅ Config loaded successfully!")
        typer.echo(config.model_dump_json(indent=2))

    except Exception as e:
        typer.echo(f"❌ Error: {e}")
        raise typer.Exit(code=1)

@app.command()
def down():
    """
    Shut down the FlowProxy service.
    """
    typer.echo("🛑 App is shut down")

def main():
    app()

if __name__ == "__main__":
    main()