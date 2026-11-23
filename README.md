# HeartShare Harmonization

Personal runner notebooks for HeartShare harmonization on BioData Catalyst
(BDC), powered by Seven Bridges. Each user runs their own notebook copies in
their own Data Studio analysis workspace. Shared Project Files hold the release
and study data; do not edit or run the shared archived notebook copies there.

> **Status: released for analysis (v0.1.6).** Use these outputs to explore the
> data and plan analyses. v1.0.0, the first release for publication, will
> follow. Manuscripts and abstracts should use v1.0.0 once it is available and
> follow the [HeartShare publications policy](https://amphf.org/for-scientists/publications/).
> Read the release notes first, especially the known limitations, and record
> the release version, runtime and notebook commit with your results.

## Read the release notes first

The release notes are in the release folder on BDC:

```text
/sbgenomics/project-files/x01_harmonization/v0.1.6/RELEASE_NOTES.md
```

They describe the 13 studies, the variables, the output table, what to know
before analyzing, and the known limitations. A few points change results if
missed:

- **Analyze one measurement context at a time.** Blood pressure (by position
  and timing), ejection fraction (by method), and some labs (local versus core
  laboratory) have more than one way of being measured. The
  `measurement_context` column tells them apart, and Table One gives each
  context its own row.
- **`hf_phenotype` is the cohort each study enrolled or assigned at baseline**,
  not a classification from measured ejection fraction. It is available for
  every study except CATHGEN. Each row's
  `measurement_context` names the `assignment_method`. Use measured ejection
  fraction when an analysis needs a specific threshold.
- **Race in HFN-IRONOUT and SCAN-MP comes from a two-way source grouping**
  (White vs Black/Other; Black vs Non-Black). Unknown means "reported as
  Black/Other" (IRONOUT) or "Non-Black or not reported" (SCAN-MP). Do not drop
  Unknown in these studies.
- **TOPCAT follow-up medications can be carried forward** from the last
  recorded visit; see [Carried-forward values](#carried-forward-values-output-schema-13).
- **Some probable recording errors are kept, with a flag.** For example, TOPCAT
  albumin values of 30 or more in a g/dL field are kept as recorded, and the
  lineage file marks them with a `VALUE FLAG:` note. These flags are not a
  complete plausibility screen; apply your own range checks.

## Get your own notebooks

Start your own BDC Data Studio analysis and open a JupyterLab terminal:

```bash
cd /sbgenomics/workspace
git clone https://github.com/ShahLab-NU/heartshare-harmonization.git
mkdir -p heartshare-analysis-v0.1.6-runtime-r1-1
cp heartshare-harmonization/notebooks/*.ipynb heartshare-analysis-v0.1.6-runtime-r1-1/
git -C heartshare-harmonization rev-parse HEAD > heartshare-analysis-v0.1.6-runtime-r1-1/notebook_commit.txt
cp heartshare-harmonization/notebook_compatibility.json heartshare-analysis-v0.1.6-runtime-r1-1/
```

Open the notebooks in `heartshare-analysis-v0.1.6-runtime-r1-1/` and edit those
copies. Keep the repository checkout clean so updates do not conflict with your
settings or saved notebook outputs. Save your working notebooks and provenance
with your results before ending the Data Studio analysis.

## Select the matching release

This notebook set was tested with the **v0.1.6 runtime r1 bundle** (`v0.1.6-runtime-r1`). Its
runtime SHA-256 is recorded in [notebook_compatibility.json](notebook_compatibility.json).
The matching release must be uploaded under:

```text
/sbgenomics/project-files/x01_harmonization/v0.1.6/
```

Releases published on BDC so far: v0.1.3, v0.1.5 and v0.1.6. (v0.1.4 was
prepared but never published.)

In the harmonization notebook's first configuration cell, set:

```python
RELEASE_ROOT = "/sbgenomics/project-files/x01_harmonization"
RELEASE_VERSION = "v0.1.6"
```

The harmonization notebook defaults to `"v0.1.6"`. Keep that explicit version
for this bundle; changing it selects a different release. Both notebooks accept
runtime output schemas 1.1, 1.2, and 1.3, but Table One additionally requires the `table_one/analysis/1` capability.
The earlier schema12_r2 runtime does not provide it. Keep the checksum checks
intact; install the matching release rather than bypassing a compatibility error.
Notebooks older than commit `e9c09bf` (including the v0.1.3 notebooks) accept only
1.1 and 1.2 and refuse this runtime with a schema mismatch; update your checkout
rather than editing the check.

## Carried-forward values (output schema 1.3)

Schema 1.3 adds one `value_origin` value, `carried_forward`, alongside
`source_reported` and `calculated`. It is used only for TOPCAT
medication use from form T007: when a follow-up visit records no medication
change, the most recent recorded value is carried to that visit. It is never
carried past a visit without a recorded medication list. The row's notes name
the source visit.

Baseline values are never carried forward. Table One does not filter on
`value_origin`, so follow-up and longitudinal TOPCAT medication summaries
include carried-forward values. To summarize recorded values only, remove rows
with `value_origin == "carried_forward"` from `harmonized_long.csv` before
building the table.

## New in v0.1.6

- **No change to the harmonized data.** Mappings and variable definitions are
  the same as in v0.1.5, and full runs produce the same rows.
- **Fixed: some HFN-EXACT echocardiography selections stopped the run.** In
  v0.1.5, selecting `lvef`, `lv_mass`, `lvedd`, `lvesd`,
  `interventricular_septum_thickness` or `lv_posterior_wall_thickness` without
  both `interventricular_septum_thickness` and `lvedd` failed with
  "source_condition variable 'ivsd' is not present in the source frame". These
  selections now run. The v0.1.5 workaround of adding those two variables is no
  longer needed.
- **New: compare two releases on BDC.** Run the harmonization notebook's setup
  cells with `RELEASE_VERSION = "v0.1.6"`, then add a cell:

  ```python
  from heartshare_harmonization.release_consistency import main as check_releases

  check_releases([
      "check", "--old", "v0.1.5", "--new", "v0.1.6", "--baseline-only",
      "--output-dir", "/sbgenomics/workspace/output-files/consistency_v0.1.5_v0.1.6",
  ])
  ```

  It reports, per study and variable, whether output changed and whether the
  release files explain the change. The report holds aggregate results only.
  Every study and variable should come back `same` between v0.1.5 and v0.1.6.
  The release notes describe the options.

### Coming from v0.1.3 notebooks

- HFN-EXACT, HFN-RELAX and SCAN-MP record atrial fibrillation and flutter
  together, so their history is in `afib_flutter_hx`, not `afib_hx`. Add
  `afib_flutter_hx` to saved `VARIABLES` lists that name `afib_hx`. HFN-FIGHT
  and HFN-NEAT record the two separately and export both.
- `pap_diastolic`, `pap_mean`, `pcwp` and `subcohort` are no longer in the
  release. Remove them from saved `VARIABLES` lists.

## Choose domains and individual variables

Step 4 combines both lists, without duplicates. For example:

```python
DOMAINS = ["demographics"]
VARIABLES = ["height", "weight", "bmi"]
```

This selects every demographic variable (including age and sex), plus height,
weight, and BMI. The notebook prints the combined selection before running.
Leave both lists empty to select all mapped variables. Domain names are the
category headings printed by Step 2; variable names must match that inventory.
Earlier notebooks ignored DOMAINS whenever VARIABLES was nonempty.

The default example includes height and weight alongside BMI so you can inspect
the component measurements with the calculated result.

Turning off BASELINE_ONLY includes baseline and follow-up visits. It does not
exclude baseline sex values; HFN-NEAT's sex mapping is baseline-only and is not
repeated at each follow-up visit. If sex is missing from the entire output,
check the manifest's selected_variables, variable_coverage, and dataset reports.

## Check dry-run coverage

Step 6 shows a variable/timepoint-by-study matrix and a gap-only summary with
which studies are affected and why. Missing source or mapping files show
**NOT READY**. When files exist but individual requested variables lack mappings,
the notebook shows **READY TO RUN, WITH VARIABLE COVERAGE GAPS**.

`mapping_missing` means no selected mapping exists; it does not establish that
the study never collected the data. `planned` confirms a mapping, with source
columns and usable values checked during the real run. Combinations without a
coverage record are labeled **Not assessed at this timepoint**. The complete
record is also saved in `variable_coverage.csv` and `variable_coverage.json`.

## Run

1. Open `heartshare_harmonize_bdc.ipynb`, select studies and variables, and run
   the dry run first. Resolve any reported missing files before setting
   `DRY_RUN = False`. Record the printed output folder.
2. Open `heartshare_table_one_bdc.ipynb`, set `RUN_DIR` to that output folder,
   and run its cells. It supports baseline summaries, cohort filters, subgroup
   comparisons, per-study longitudinal summaries, and configurable continuous
   summaries. It exports tables and figures plus analysis settings and
   participant selection counts.

Table One normally uses the exact runtime recorded by the harmonization run.
Use a fresh kernel when changing releases or runtimes. Results are written under
`/sbgenomics/workspace/output-files/`; use Data Studio's Save to Project Files
workflow to preserve the results and working notebook copies.

## Updates and historical reruns

Update the clean repository checkout with:

```bash
git -C /sbgenomics/workspace/heartshare-harmonization pull --ff-only
```

Copy the updated notebooks into a **new analysis folder**. Leave previous
working notebooks and results intact. For a historical run, retrieve the exact
recorded commit or release tag rather than pulling the latest scripts. See
[RERUNS.md](RERUNS.md) for the complete procedure.

## Questions and problems

Contact Ryan Sisk (r-sisk@northwestern.edu) or open an issue here. Include the
notebook commit, release/runtime version, study and variable, and relevant error
output, with participant-level values removed. This repository contains no
study data, mappings, standards library, or runtime archives.

## License

The code in this repository is released under the [MIT License](LICENSE). The
license does not cover study data or the release files on BDC.
