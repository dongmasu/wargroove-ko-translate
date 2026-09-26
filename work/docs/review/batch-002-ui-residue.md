# Translation Batch 002: UI Residue

Date: 2026-09-26

Scope: obvious untranslated or mismatched UI/operator strings found by
comparing NSW Wargroove 2 English and Korean resources.

The following values are applied by
`tools/build_translation_batch.py` and are included in the regenerated
direct-replacement resources:

| Key | English | Previous Korean | Proposed Korean |
| --- | --- | --- | --- |
| `operator_different` | `not` | `not` | `아님` |
| `operator_greater` | `more than` | `more than` | `초과` |
| `operator_less` | `less than` | `less than` | `미만` |
| `turn_n` | `TURN {0}` | `TURN {0}` | `턴 {0}` |
| `ui_map_day` | `Turn {0}` | `Turn {0}` | `턴 {0}` |
| `ui_cutscene_emote_cat` | `Enid Lying Down` | `Enid Lying Down` | `에니드 눕기` |
| `ui_cutscene_emote_catappears` | `Enid Appears` | `Enid Grooming` | `에니드 등장` |
| `ui_cutscene_emote_catsit` | `Enid Sitting` | `Enid Sitting` | `에니드 앉기` |
| `ui_cutscene_emote_catstop` | `Enid Stops Grooming` | `Enid Stops Grooming` | `에니드 그루밍 종료` |
| `ui_cutscene_emote_pet` | `Pet` | `Enid Being Pet` | `쓰다듬기` |
| `ui_cutscene_sfx_family_leaving_bushes` | `Wulfar and the Twins leaving the bushes.` | same | `울파와 쌍둥이가 수풀을 빠져나감` |
| `ui_cutscene_sfx_family_leaving_cactus` | `Wulfar and the Twins leaving the cactii.` | same | `울파와 쌍둥이가 선인장을 빠져나감` |
| `ui_cutscene_sfx_treasure_stolen` | `Gold Being Stolen` | same | `골드 도난` |

These are content/UI labels, not narrative dialogue. Placeholder and control
code checks are required before packaging.
