import json
import time
from pathlib import Path

from rich.console import Console
from rich.table import Table

RUNS = Path.home() / "ctrls" / "runs"


def elapsed(start: float) -> str:
    sec = int(time.time() - start)
    h, m = sec // 3600, (sec % 3600) // 60
    if h:
        return f"{h}h {m}m"
    return f"{m}m"


def fmt_limits(d: dict) -> str:
    ram = d.get("ram", 0)
    cpu = d.get("cpu", 0)
    parts = []
    if ram:
        parts.append(f"{ram}G")
    if cpu:
        parts.append(f"{cpu}core")
    return " / ".join(parts) if parts else "-"


def main():
    # 작업 목록
    if not RUNS.exists():
        print("no running jobs")
        return

    table = Table()
    for col in ["PID", "OWNER", "TASK", "DIR", "ELAPSED", "LIMITS"]:
        table.add_column(col)

    rows = 0
    for f in sorted(RUNS.glob("*.json")):
        try:
            d = json.loads(f.read_text())
        except Exception:
            continue

        # 기록 삭제
        if not Path(f"/proc/{d['pid']}").exists():
            f.unlink(missing_ok=True)
            continue

        table.add_row(
            str(d["pid"]),
            d.get("owner", "-"),
            d.get("task") or "-",
            d.get("cwd", "-"),
            elapsed(d.get("start", time.time())),
            fmt_limits(d.get("limits", {})),
        )
        rows += 1

    if rows == 0:
        print("no running jobs")
    else:
        Console().print(table)