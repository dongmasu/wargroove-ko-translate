# Wargroove 2 작업 디렉터리

Wargroove 2 번역 작업은 이 디렉터리에서 진행합니다.

AI 도구 없이도 작업할 수 있습니다. JSON 파일을 일반 텍스트 편집기로
수정하고, 프로젝트 루트에서 Python 도구를 실행하면 됩니다.

## 작업 시작

`src/Wargroove 2/1.2.x/`는 원본 `config.dat`와 `ui.dat`를 해독·압축 해제한
읽기 전용 기준본입니다. 작업을 시작할 때 기준본을 이 디렉터리로 복사합니다.

```sh
mkdir -p "work/Wargroove 2/1.2.x"
cp -R "src/Wargroove 2/1.2.x/config" "work/Wargroove 2/1.2.x/"
cp -R "src/Wargroove 2/1.2.x/ui" "work/Wargroove 2/1.2.x/"
```

`src/`의 파일은 직접 수정하지 않습니다. 번역 작업은 `work/`에서 진행하고,
패킹 결과는 `dist/`에 생성합니다.

## 번역 파일

문자열 번역 파일은 다음 위치에 있습니다.

```text
work/Wargroove 2/1.2.x/config/configFile/strings/
```

영어 원문은 `en-GB_*.json`, 일본어와 중국어는 `ja-JP_*.json`,
`zh-Hans_*.json`을 참고합니다. 한국어 파일은 `ko-KR_*.json`으로 만들거나
수정합니다. 파일 내부의 문자열 키는 변경하지 말고 값만 번역합니다.

예를 들어 다음 파일을 일반 편집기로 열어 번역합니다.

```text
work/Wargroove 2/1.2.x/config/configFile/strings/ko-KR_ui.json
```

한국어 파일을 새로 추가할 때에는 대응하는 영어 파일을 복사한 뒤 파일명과
내용을 한국어용으로 수정합니다.

이 버전에 적용되는 용어집은 다음 파일입니다.

```text
work/Wargroove 2/1.2.x/wg2-terminology.tsv
```

용어집은 게임 버전별로 달라질 수 있으므로 다른 버전의 작업 디렉터리와
공유하지 않습니다. 새 인명·지명·고유명사와 확정된 번역어는 이 파일에
기록합니다.

## 패킹

작업 결과는 새 파일로 생성되며 원본 `config.dat`는 수정되지 않습니다.
최종 배포 패키지는 작업 파일 중 가장 최근 수정일을 기준으로 한 날짜
디렉터리에 생성합니다. 자세한 규칙은
`docs/dist-packaging.md`를 참고합니다.

`config.dat`와 `ui.dat`를 패킹하고 ZIP까지 한 번에 만들려면 프로젝트 루트에서
다음 명령을 실행합니다.

```sh
python3 tools/build_dist_package.py
```

결과:

```text
dist/Wargroove 2/1.2.x/YYYYMMDD/assets/config.dat
dist/Wargroove 2/1.2.x/YYYYMMDD/assets/ui.dat
dist/Wargroove 2/1.2.x/YYYYMMDD/Wargroove2-ko-translate-1.2.x-YYYYMMDD.zip
```

```sh
python3 tools/config_workspace.py pack \
  "work/Wargroove 2/1.2.x/config" \
  "dist/Wargroove 2/1.2.x/YYYYMMDD/config.dat"
```

`ui.dat`를 수정한 경우에는 `ui` workspace를 별도로 패킹합니다.

```sh
python3 tools/config_workspace.py pack \
  "work/Wargroove 2/1.2.x/ui" \
  "dist/Wargroove 2/1.2.x/YYYYMMDD/ui.dat"
```

패킹 후 생성된 파일을 확인한 다음, Windows 게임 설치 폴더의
`assets/config.dat` 또는 `assets/ui.dat`를 백업하고 교체합니다.
`dist/` 파일은 바로 배포할 수 있는 결과물이며, 기존 게임 파일을 직접
수정하지 않는 것을 원칙으로 합니다.
