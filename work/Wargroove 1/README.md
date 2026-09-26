# Wargroove 1 작업 디렉터리

현재 Wargroove 1 번역 작업은 시작하지 않았습니다. 이 디렉터리는
의도적으로 비워 둡니다.

## 작업 시작

`src/Wargroove 1/2.1.x/`는 원본 `config.dat`와 `ui.dat`를 해독·압축 해제한
읽기 전용 기준본입니다. 작업을 시작할 때 기준본을 이 디렉터리로 복사합니다.

```sh
mkdir -p "work/Wargroove 1/2.1.x"
cp -R "src/Wargroove 1/2.1.x/config" "work/Wargroove 1/2.1.x/"
cp -R "src/Wargroove 1/2.1.x/ui" "work/Wargroove 1/2.1.x/"
```

`src/`의 파일은 직접 수정하지 않습니다. 번역 작업은 `work/`에서 진행하고,
패킹 결과는 `dist/`에 생성합니다.

```sh
python3 tools/config_workspace.py pack \
  "work/Wargroove 1/2.1.x/config" \
  "dist/Wargroove 1/2.1.x/YYYYMMDD/config.dat"
```

`ui.dat`를 수정한 경우에도 같은 방식으로 `ui` workspace를 패킹할 수
있습니다.
