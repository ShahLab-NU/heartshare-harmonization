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
mkdir -p heartshare-analysis-v0.2.0-schema12-r3
cp heartshare-harmonization/notebooks/*.ipynb heartshare-analysis-v0.2.0-schema12-r3/
git -C heartshare-harmonization rev-parse HEAD > heartshare-analysis-v0.2.0-schema12-r3/notebook_commit.txt
cp heartshare-harmonization/notebook_compatibility.json heartshare-analysis-v0.2.0-schema12-r3/
```

Open the notebooks in `heartshare-analysis-v0.2.0-schema12-r3/` and edit those
copies. Keep the repository checkout clean so updates do not conflict with your
settings or saved notebook outputs. Save your working notebooks and provenance
with your results before ending the Data Studio analysis.

## Select the matching release

This notebook set was tested with the **v0.2.0 schema12_r3 candidate**. Its
runtime SHA-256 is recorded in [notebook_compatibility.json](notebook_compatibility.json).
The matching release must be uploaded under:

```text
/sbgenomics/project-files/x01_harmonization/v0.2.0/
```

In the harmonization notebook's first configuration cell, set:

```python
RELEASE_ROOT = "/sbgenomics/project-files/x01_harmonization"
RELEASE_VERSION = "v0.2.0"
```

Select the release explicitly instead of leaving the notebook default at
`"latest"`. Both notebooks accept runtime output schemas 1.1 and 1.2, but the
updated Table One additionally requires the `table_one/analysis/1` capability.
The earlier schema12_r2 runtime does not provide it. Keep the checksum checks
intact; install the matching release rather than bypassing a compatibility error.

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
