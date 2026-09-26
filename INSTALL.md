# Wargroove 2 한글 패치 설치

이 패치는 **Windows용 Wargroove 2**를 대상으로 합니다. macOS용 게임에는
적용할 수 없습니다.

## 1. 패치 다운로드

다음 중 한 가지 방법으로 ZIP 파일을 받습니다.

- GitHub Release의 Assets에서 `Wargroove2-ko-translate-<버전>-<수정일>.zip`
  다운로드
- 저장소의 `dist/Wargroove 2/<버전>/<수정일>/`에 있는 ZIP 사용

ZIP 내부에는 다음 두 파일만 있습니다.

```text
assets/config.dat
assets/ui.dat
```

## 2. 게임 설치 폴더 열기

Steam에서 다음 순서로 엽니다.

1. 라이브러리에서 **Wargroove 2**를 우클릭합니다.
2. **관리 → 로컬 파일 보기**를 선택합니다.
3. 열린 폴더 안의 `assets/` 폴더로 이동합니다.

일반적인 기본 설치 경로는 다음과 같습니다.

```text
C:\Program Files (x86)\Steam\steamapps\common\Wargroove 2\assets\
```

## 3. 원본 파일 백업

기존 파일을 삭제하거나 바로 덮어쓰지 말고, 먼저 이름을 바꿔 백업합니다.

```text
config.dat -> config.dat.wargroove-original
ui.dat     -> ui.dat.wargroove-original
```

Windows 탐색기에서 파일을 복사해 다른 폴더에 보관해도 됩니다.

## 4. 패치 파일 설치

ZIP 파일을 압축 해제한 뒤, ZIP 안의 `assets/config.dat`와 `assets/ui.dat`를
게임 설치 폴더의 `assets/`에 복사합니다.

최종 구조는 다음과 같아야 합니다.

```text
Wargroove 2/
  assets/
    config.dat
    ui.dat
```

`assets` 폴더가 중복되어 다음과 같은 구조가 되지 않도록 주의합니다.

```text
Wargroove 2/assets/assets/config.dat
```

## 5. 게임 실행

게임을 실행한 뒤 언어 설정에서 **한국어**를 선택합니다. 언어 목록에
한국어가 보이지 않으면 다음을 확인합니다.

- ZIP 안의 `assets/config.dat`를 게임 폴더에 복사했는지 확인
- Steam 게임 파일 무결성 검사를 실행하지 않았는지 확인
- 올바른 Wargroove 2 설치 폴더에 복사했는지 확인
- 기존 `config.dat`와 `ui.dat`를 백업한 뒤 교체했는지 확인

## 원상 복구

패치를 제거하려면 패치 파일을 삭제하는 대신 백업 파일을 복원합니다.

```text
config.dat.wargroove-original -> config.dat
ui.dat.wargroove-original     -> ui.dat
```

백업 파일이 없다면 Steam의 **게임 파일 무결성 확인**으로 원본 파일을
복구할 수 있습니다. 이후 한글 패치를 다시 적용하려면 ZIP을 다시
압축 해제해 복사합니다.

## 주의사항

- 패치 적용 전 원본 파일을 반드시 백업합니다.
- 게임 업데이트 후에는 `config.dat`와 `ui.dat`가 변경될 수 있으므로
  패치를 다시 적용해야 할 수 있습니다.
- 다른 버전의 패치 파일을 섞어 사용하지 않습니다.
