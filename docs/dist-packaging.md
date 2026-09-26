# Dist Packaging Rules

`dist/` contains distributable files generated from the versioned `work/`
directory. It is not a place for manual translation edits.

## Layout

```text
dist/
  Wargroove 2/
    1.2.x/
      YYYYMMDD/
        assets/
          config.dat
          ui.dat
        Wargroove2-ko-translate-1.2.x-YYYYMMDD.zip
```

The date is the modification date of the newest file under
`work/Wargroove 2/1.2.x/`. The ZIP contains exactly:

```text
assets/config.dat
assets/ui.dat
```

The generated DAT files are suitable for copying into the Windows game's
`assets/` directory after making a backup. The ZIP is the release artifact for
GitHub.

## Build

Run this command from the project root:

```sh
python3 tools/build_dist_package.py
```

The script:

1. Reads `work/Wargroove 2/1.2.x/config` and `ui`.
2. Packs them with `tools/config_workspace.py`.
3. Calculates the newest work-file date.
4. Writes the two DAT files under the dated `assets/` directory.
5. Creates `Wargroove2-ko-translate-1.2.x-YYYYMMDD.zip`.
6. Refuses to overwrite an existing release.

For a reproducible date or a temporary output directory:

```sh
python3 tools/build_dist_package.py \
  --date 20260927 \
  --dist-root /tmp/wargroove-dist
```

The script uses only Python's standard library and the project tools. No AI
tool or third-party package is required.

For a Wargroove 1 release, use the corresponding game directory and the
`Wargroove1-ko-translate-<version>-<date>.zip` naming pattern.
