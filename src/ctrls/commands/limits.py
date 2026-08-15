from pathlib import Path

import tomlkit
import typer

config = "cvz.toml"

def main():
    path = Path.cwd() / config

    if not path.exists():
        print(f"{config} not found. run 'cvz init' first")
        raise typer.Exit(1)

    doc = tomlkit.parse(path.read_text())

    # 없으면 생성하기 필수임
    
    if "limits" not in doc:
        doc["limits"] = tomlkit.table()
    limits = doc["limits"]

    print("0 : unlimited")

    ram = typer.prompt(
        "RAM",
        default=limits.get("ram", 0),
        type=int
    )

    cpu = typer.prompt(
        "CPU",
        default=limits.get("cpu", 0),
        type=int
    )

    limits["ram"] = ram    
    limits["cpu"] = cpu

    path.write_text(tomlkit.dumps(doc))

    print(f"save! ram {ram} / cpu {cpu}")

