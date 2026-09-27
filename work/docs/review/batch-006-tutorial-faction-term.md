# Batch 006: Tutorial Faction Term

## Finding

In Tutorial 4, the player commands the Faahri faction, whose Barracks
recruits the `Duelist`. The source tutorial text still says `Swordsman`,
which belongs to the Cherrystone faction. This made the Korean tutorial
tell the player to recruit a unit that was not available.

## Change

Updated both Tutorial 4 strings below from `소드맨` to `듀얼리스트`:

- `wg2_tut_4_escape_from_memorial_isle_trigger_tutorial_barracks_pt_2_action_000_002`
- `wg2_tut_4_escape_from_memorial_isle_trigger_tutorial_barracks_pt_2_action_001_005`

The change was applied to the per-file Korean resource and the aggregate
`verified-ko-KR.json`.

## Follow-up Finding

The recruit dialogue is stored in the separate
`ko-KR_wargroove2_dev.json` resource, not in the campaign tutorial resource.
The following three keys also referred to `Swordsman` even though this
Faahri scenario only offers `Duelist`:

- `E1M1_recruitUI_Lytra_01`
- `E1M1_recruitUI_Pistil_02`
- `E1M1_recruitUI_Pistil_fail_01`

All three were updated to `듀얼리스트` and recorded in
`work/Wargroove 2/1.2.x/translation-exceptions.tsv`.
