# HeartShare Harmonization

Notebooks and instructions for running HeartShare data harmonization on
[BioData Catalyst powered by Seven Bridges](https://platform.sb.biodatacatalyst.nhlbi.nih.gov/)
(BDC).

This repository contains only the runner notebooks and these instructions.
The harmonization release itself — mapping files, standards library, catalog,
and runtime — lives in your BDC project's **Project Files** under
`x01_harmonization/`, alongside the study data. Nothing in this repository
contains study data.

> **Status:** evaluation. Harmonized outputs are candidate data for testing
> and feedback; verification of the release is ongoing. Please do not
> publish results derived from these outputs.

## Prerequisites

- Membership in the HeartShare X01 harmonization BDC project (the notebooks
  read the release and study files from that project's Project Files).
- A BDC Data Studio instance (Jupyter, any standard Python image).

## Getting the notebooks into Data Studio

1. Open your BDC project and start (or open) a **Data Studio** analysis.
2. In the JupyterLab launcher, open a **Terminal**.
3. Clone this repository:

   ```bash
   git clone https://github.com/ShahLab-NU/heartshare-harmonization.git
   ```

4. The notebooks appear in the file browser under
   `heartshare-harmonization/notebooks/`. Open them from there.

To update to the latest version later, run `git pull` from the
`heartshare-harmonization` directory in the same terminal.

## Running

### 1. Harmonize — `notebooks/heartshare_harmonize_bdc.ipynb`

Open the notebook and run it top to bottom. The configuration cell at the
top points at the release root (`/sbgenomics/project-files/x01_harmonization`)
and defaults to the latest release version found there; you can select
studies, variables, and timepoints in the same cell. Outputs (CSV + Parquet,
with a manifest, data dictionary, and lineage) are written under
`/sbgenomics/workspace/output-files/` — use "Save to Project Files" in Data
Studio if you want to keep them.

### 2. Table One — `notebooks/heartshare_table_one_bdc.ipynb`

Run after a harmonization run; point its configuration cell at the
harmonized output directory. It produces a baseline characteristics table
(median [IQR], n (%)) with CSV/Excel/Word/HTML exports.

## Questions and problems

Contact Ryan Sisk (r-sisk@northwestern.edu) or open an issue on this
repository. When reporting a problem, please include the release version the
notebook printed, the study/variable involved, and the notebook cell output
(with any participant-level values removed).
