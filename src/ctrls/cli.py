import typer

from ctrls.commands import init, limits, run, status

app = typer.Typer(help="kshs ctrls")

# cvz init
app.command("init")(init.main)

# cvz limits && limit
app.command("limits")(limits.main)
app.command("limit")(limits.main)

# cvz status
app.command("status")(status.main)

# cvz uv run
uv_app = typer.Typer()
app.add_typer(uv_app, name="uv")
uv_app.command(
    "run",
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True},
)(run.main)