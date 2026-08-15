# control s

## 소개
이 프로젝트는 서버컴을 제어하고 (control s) 자신의 폴더를 저장하는 (ctrl s) 편의성을 제공하기 위한 프로젝트 입니다.

## 문제점
1. 저장 공간의 부족
2. 누가 무슨 작업 중인지 알 수 없음
3. cpu, ram 제한을 좀 더 쉽게 다룰 수 있으면 좋겠음

## 지원 기능
☑ cpu, ram 제한 기능 (toml 파일 수정을 통한 지원)

☑ 현재 무슨 작업 중인지 한 번에 확인 (status로 확인)

☑ toml 파일을 통한 쉬운 관리 

☐ 저장 공간 절약 (현재 clean 명령어 지원 x -> 문제가 생길 가능성이 높음)

## 설치
```
uv tool install git+https://github.com/jeehoo0507/ctrls.git
```

## 명령어 지원
| 명령어 | 설명 |
|---|---|
| `cvz init` | 현재 폴더 등록 (cvz.toml 생성) |
| `cvz limits` | RAM / CPU 제한 설정 |
| `cvz uv run x.py` | 제한 걸고 실행 + 기록 |
| `cvz status` | 누가 뭘 돌리는지 확인 |

## 설정 파일

`cvz init`이 만드는 `cvz.toml`을 직접 수정해도 됩니다.

```toml
[project]
owner = "cjh"
repo = "https://github.com/..."
task = "dLLM 병렬 생성 실험"

[limits]
ram = 32     # GB, 0이면 제한 없음
cpu = 8      # 코어, 0이면 제한 없음
```

## 지원 예정 명령어
cvz clean. cvz arxiv, cvz sleep

작동 방식
저장소가 등록되었는가?
-> no : github 저장소 입력
-> yes :
git push -> 커밋 번호 저장 -> 해당 폴더 cvz.toml를 제외한 파일 삭제

---
cvz unarxiv, cvz wake

작동 방식
cvz clean 을 통해 저장된 커밋 번호를 통해 파일들이 가지고 온다.


