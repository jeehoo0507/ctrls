import json
import os
import shutil
import subprocess
import time
from pathlib import Path

import tomlkit
import typer

config = "cvz.toml"
RUNS = Path.home() / "ctrls" / "runs"


def build_cmd(args: list[str], ram: int, cpu: int) -> list[str]:
    cmd = ["uv", "run"] + args

    if ram:
        cmd = ["systemd-run", "--user", "--scope", "--quiet",
            "-p", f"MemoryMax={ram}G",
            "-p", "MemorySwapMax=0"] + cmd

    if cpu:
        cmd = ["taskset", "-c", f"0-{cpu - 1}"] + cmd

    return cmd


def make_env(cpu: int) -> dict:
    env = os.environ.copy()
    if cpu:
        env["OMP_NUM_THREADS"] = str(cpu)
        env["MKL_NUM_THREADS"] = str(cpu)
        env["OPENBLAS_NUM_THREADS"] = str(cpu)
    return env


def main(
    ctx: typer.Context,
    m: str = typer.Option("", "-m", help="이번 실행의 작업 내용"),
):
    path = Path.cwd() / config

    if not path.exists():
        print(f"{config} not found. run 'cvz init' first")
        raise typer.Exit(1)

    args = ctx.args
    if not args:
        print("no command given")
        raise typer.Exit(1)

    doc = tomlkit.parse(path.read_text())
    project = doc["project"]
    limits = doc["limits"]

    # toml 설정 확인
    task = m or project.get("task", "")
    if not task:
        task = typer.prompt("task?")
        project["task"] = task
        path.write_text(tomlkit.dumps(doc))

    ram = limits.get("ram", 0)
    cpu = limits.get("cpu", 0)

    if ram and not shutil.which("systemd-run"):
        print("warning: systemd-run not found, RAM limit ignored")
        ram = 0

    if cpu and not shutil.which("taskset"):
        print("warning: taskset not found, CPU pinning ignored")
        cpu = 0

    cmd = build_cmd(args, ram, cpu)
    proc = subprocess.Popen(cmd, env=make_env(cpu))

    # RUNS 폴더 만들고 그 안에 json으로 기록하기
    RUNS.mkdir(parents=True, exist_ok=True)
    rec = RUNS / f"{proc.pid}.json"
    rec.write_text(json.dumps({
        "pid": proc.pid,
        "owner": project.get("owner") or os.environ.get("USER", ""),
        "cwd": str(Path.cwd()),
        "task": task,
        "cmd": cmd,
        "start": time.time(),
        "limits": {"ram": ram, "cpu": cpu},
    }, ensure_ascii=False))

    try:
        code = proc.wait()
    finally:
        rec.unlink(missing_ok=True)

    raise typer.Exit(code)