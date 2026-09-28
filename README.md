# Wargroove 2 한글 번역 프로젝트

이 저장소는 Windows용 Wargroove 2의 한글 번역을 만드는 프로젝트입니다.
macOS용 게임은 지원하지 않습니다.

Wargroove 1에는 공식 한국어 번역이 있지만 Wargroove 2는 한국어를
지원하지 않습니다. Wargroove 1은 용어와 문체를 참고하는 기준으로
사용합니다.

번역 규칙과 문맥별 예외는
[`docs/translation-guide.md`](docs/translation-guide.md)에 기록합니다.
버전별 예외는 각 번역 workspace에 함께 기록합니다.

## 링크

- 공식 웹사이트: https://wargroove.com/
- Steam Wargroove 1: https://store.steampowered.com/app/607050/_/
- Steam Wargroove 2: https://store.steampowered.com/app/1346020/Wargroove_2/

## 폰트 방향

현재 폰트 방향은 Windows용 Wargroove 2의 UI를 순정 상태로 유지하고,
`Noto Serif`만 Google Noto Serif Korean으로 교체하는 것입니다.
`Sitka Text Bold Italic`과 그 밖의 UI 폰트 자산은 변경하지 않습니다.

순정 `Noto Serif`에는 한글 음절이 51자밖에 포함되어 있지 않아 스킬 및
그루브 효과 문장에서 일부 글리프가 표시되지 않을 수 있기 때문입니다.
전체 폰트 교체 절차와 변환 설정은
[`docs/font-editing-guide.md`](docs/font-editing-guide.md)에 기록되어
있습니다. 사용한 소스는 Google Noto Serif Korean이며 SIL Open Font
License 1.1에 따라 배포됩니다. 저작권 표시와 공식 링크도 해당 문서에
기록되어 있습니다.

설치 및 백업 방법은 [`INSTALL.md`](INSTALL.md)에 기록되어 있습니다.

## 원칙

- 특별한 이유가 없으면 원본 파일과 기존 번역을 보존합니다.
- 실제 대상 게임에 맞춰 소스와 번역 작업을 정리합니다.
- 인증 정보, 기기 비밀 정보, 외부 서비스 설정을 workspace에 넣지 않습니다.

## 디렉터리 구조

```text
src/
  Wargroove 1/2.1.x/    변경하지 않는 Wargroove 1 원본 스냅샷
  Wargroove 2/1.2.x/    변경하지 않는 Windows WG2 원본 스냅샷
tools/                  HALLEYPK parser 및 ConfigFile 도구
tests/                  회귀 테스트와 소규모 테스트 fixture
work/
  Wargroove 1/2.1.x/    Wargroove 1 작업 사본
  Wargroove 2/1.2.x/    WG2 번역 작업 파일
  docs/                  버전 관리되는 검수 기록; 로컬 분석은 무시됨
dist/                   게임에 복사할 날짜별 배포 파일
docs/                   안정적인 프로젝트 설계 및 작업 절차 문서
references/             로컬 원본 자료; Git에서 제외됨
```

`src/` 아래 파일은 변경하지 않는 읽기 전용 원본 스냅샷입니다. 버전이
관리되는 검수 및 진행 기록은 `work/docs/review/`에 저장하고, 재현 가능한
원시 payload와 중간 변환 결과는 Git에서 무시되는
`work/docs/analysis/`에 저장합니다. 번역 수정은 해당
`work/<game>/<version>/config/` 아래에서 진행합니다.
`dist/`의 날짜별 `config.dat`, `ui.dat`, ZIP이 배포 산출물입니다.

전체 DAT 및 ZIP 패키징 규칙은 [`docs/dist-packaging.md`](docs/dist-packaging.md)에
기록되어 있습니다. Wargroove 2 릴리스는 다음 명령으로 생성합니다.

```sh
python3 tools/build_dist_package.py
```

사용자용 설치 방법은 [`INSTALL.md`](INSTALL.md)에 있습니다.

번역 작업 절차는 [`docs/translation-process.md`](docs/translation-process.md)에
정의되어 있습니다. 관련 Wesnoth 번역 프로젝트에서 정한 검수자, 승인자,
편집자, 검증자, 배포자 역할 분리를 사용합니다.

---

# Wargroove Korean Translation

This repository is a project for creating a Korean translation for the Windows
version of Wargroove 2. macOS is not a supported platform for this project.

Wargroove 1 has an official Korean translation, while Wargroove 2 does not
support Korean. Wargroove 1 may be used as a terminology and style reference.

Translation rules and context-specific exceptions are documented in
[`docs/translation-guide.md`](docs/translation-guide.md). Version-specific
exceptions are recorded beside each translation workspace.

## Links

- Official website: https://wargroove.com/
- Wargroove 1 on Steam: https://store.steampowered.com/app/607050/_/
- Wargroove 2 on Steam: https://store.steampowered.com/app/1346020/Wargroove_2/

## Font Direction

The current font direction is to keep the Windows Wargroove 2 UI in its
original state and replace only `Noto Serif` with Google Noto Serif Korean.
`Sitka Text Bold Italic` and all other UI font assets remain unchanged.

The reason is that the original `Noto Serif` contains only 51 Hangul
syllables, which can cause missing glyphs in skill and groove-effect text.
The complete font replacement procedure and conversion settings are recorded
in [`docs/font-editing-guide.md`](docs/font-editing-guide.md).
The source is Google Noto Serif Korean, licensed under SIL Open Font License
1.1; attribution and the official links are recorded in the guide.

Installation and backup instructions are documented in
[`INSTALL.md`](INSTALL.md).

## Principles

- Preserve source files and existing translations by default.
- Keep source and translation work organized by the actual target game's needs.
- Keep credentials, machine secrets, and external services out of the
  workspace.

## Layout

```text
src/
  Wargroove 1/2.1.x/    Immutable Wargroove 1 source snapshot
  Wargroove 2/1.2.x/    Immutable Windows WG2 source snapshot
tools/                  HALLEYPK parser and ConfigFile tools
tests/                  Regression tests and small test fixtures
work/
  Wargroove 1/2.1.x/    Wargroove 1 working copy
  Wargroove 2/1.2.x/    WG2 translation working files
  docs/                  Versioned review records; local analysis is ignored
dist/                   Dated files ready to copy into the game
docs/                   Stable project design and process documents
references/             Local source material, excluded from Git
```

Files under `src/` are immutable, readable source snapshots. Versioned review
and progress records belong under `work/docs/review/`; reproducible raw
payloads and intermediate conversions belong under the ignored
`work/docs/analysis/`.
Translation edits belong under the matching `work/<game>/<version>/config/`
directory.
The dated `config.dat`, `ui.dat`, and ZIP under `dist/` are release artifacts.

The complete DAT-and-ZIP packaging rule is documented in
[`docs/dist-packaging.md`](docs/dist-packaging.md). Build a Wargroove 2
release with:

```sh
python3 tools/build_dist_package.py
```

Installation instructions for users are in
[`INSTALL.md`](INSTALL.md).

The translation workflow is defined in
[`docs/translation-process.md`](docs/translation-process.md).
It uses the reviewer, approver, editor, verifier, and publisher separation
established in the related Wesnoth translation project.
