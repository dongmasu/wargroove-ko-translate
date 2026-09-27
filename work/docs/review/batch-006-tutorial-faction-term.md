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
`verified-ko-KR.json`. Because the source name is ambiguous in this Faahri
context, the final wording is the shared unit class `병사`, rather than the
specific names `소드맨` or `듀얼리스트`.

## Follow-up Finding

The recruit dialogue is stored in the separate
`ko-KR_wargroove2_dev.json` resource, not in the campaign tutorial resource.
The following three keys also referred to `Swordsman` even though this
Faahri scenario only offers `Duelist`:

- `E1M1_recruitUI_Lytra_01`
- `E1M1_recruitUI_Pistil_02`
- `E1M1_recruitUI_Pistil_fail_01`

All three were updated to `병사` and recorded in
`work/Wargroove 2/1.2.x/translation-exceptions.tsv`.

## Runtime Label Note

The deployed unit in the Tutorial 4 Faahri Barracks is confirmed to be
`Duelist`, while the codex class is `병사` (`Soldier`) for both `Duelist` and
`Swordsman`. Therefore the ambiguous tutorial references use `병사`; they must
not be forced to either specific unit name. If the deployed unit's dialogue
label still appears as `소드맨`, that displayed value may come from embedded
tutorial or unit data in the program rather than the translated dialogue
string. This is a runtime-data investigation item, not a translation change.
