import subprocess # 터미널 명령 실행
from pathlib import Path # 파일 경로 

import tomlkit # toml 파일 만들기
import typer # CLI 프로그램 만들기

config = "cvz.toml"

# 깃헙 저장소 가져오기 
# 깃헙 저장소로 등록되어있는지 확인하고 가져오면 됨 (try-except 사용하기!)

#string으로 반환
def check_repo() -> str:
    try: 
        r = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True, # 출력 결과 파이썬으로 가져오기
            text=True, # 문자열로 다루기
            timeout=3,
        )
        if r.returncode == 0: # 0이면 명령어 실행 성공
            return r.stdout.strip()
        else:
            return ""
        
    except Exception:
        return ""



def main():
    path = Path.cwd() / config # Path.cwd 현재 위치

    if path.exists(): # path가 이미 존재하는가?

        #typer.confirm : y/n 입력 받기
        reset = typer.confirm(f"{config}가 이미 존재합니다. 초기화하시겠습니까?") 

        if not reset:
            raise typer.Exit() # 종료


    owner = typer.prompt(
        "사용자명",
        # default=os.environ.get("USER", "")
        show_default=False,
        default = "?"
    )

    repo = typer.prompt(
        "github url",
        show_default=False,
        default = check_repo()
    )

    task = typer.prompt(
        "작업 내용",
        show_default=False,
        default = "?"
    )

    ram = 0
    cpu = 0

    #TOML 만들기
    doc = tomlkit.document() # 빈 문서(doc) 만들기

    # 상단 주석 추가
    doc.add(
        tomlkit.comment("cvz setting") 
    )

    project = tomlkit.table() # project 묶음 만들기
    project["owner"] = owner
    project["repo"] = repo
    project["task"] = task

    doc["project"] = project # doc에 project 추가

    limits = tomlkit.table() # limits 묶음 만들기
    limits["ram"] = ram
    limits["cpu"] = cpu

    doc["limits"] = limits # doc에 limits 추가


    path.write_text(tomlkit.dumps(doc)) # doc -> toml -> 재작성
    print("make it")