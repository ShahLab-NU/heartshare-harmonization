# HeartShare Harmonization

Personal runner notebooks for HeartShare harmonization on BioData Catalyst
(BDC), powered by Seven Bridges. Each user runs their own notebook copies in
their own Data Studio analysis workspace. Shared Project Files hold the release
and study data; do not edit or run the shared archived notebook copies there.

> **Status: evaluation.** Harmonized outputs remain candidate data for testing
> and feedback. Please do not publish results derived from these outputs.

## Get your own notebooks

Start your own BDC Data Studio analysis and open a JupyterLab terminal:

```bash
cd /sbgenomics/workspace
git clone https://github.com/ShahLab-NU/heartshare-harmonization.git
mkdir -p heartshare-analysis-v0.1.3-runtime-r4-coverage-1
cp heartshare-harmonization/notebooks/*.ipynb heartshare-analysis-v0.1.3-runtime-r4-coverage-1/
git -C heartshare-harmonization rev-parse HEAD > heartshare-analysis-v0.1.3-runtime-r4-coverage-1/notebook_commit.txt
cp heartshare-harmonization/notebook_compatibility.json heartshare-analysis-v0.1.3-runtime-r4-coverage-1/
```

Open the notebooks in `heartshare-analysis-v0.1.3-runtime-r4-coverage-1/` and edit those
copies. Keep the repository checkout clean so updates do not conflict with your
settings or saved notebook outputs. Save your working notebooks and provenance
with your results before ending the Data Studio analysis.

## Select the matching release

This notebook set was tested with the **v0.1.3 runtime_r4 bundle**. Its
runtime SHA-256 is recorded in [notebook_compatibility.json](notebook_compatibility.json).
The matching release must be uploaded under:

```text
/sbgenomics/project-files/x01_harmonization/v0.1.3/
```

In the harmonization notebook's first configuration cell, set:

```python
RELEASE_ROOT = "/sbgenomics/project-files/x01_harmonization"
RELEASE_VERSION = "v0.1.3"
```

The harmonization notebook defaults to `"v0.1.3"`. Keep that explicit version
for this bundle; changing it selects a different release. Both notebooks accept
runtime output schemas 1.1 and 1.2, but Table One additionally requires the `table_one/analysis/1` capability.
The earlier schema12_r2 runtime does not provide it. Keep the checksum checks
intact; install the matching release rather than bypassing a compatibility error.

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
