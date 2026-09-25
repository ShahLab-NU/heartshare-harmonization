# Rerun an earlier analysis

Save your edited notebooks, notebook commit SHA, notebook_compatibility.json,
configuration, run manifest, source-data versions, and environment details with
each analysis. Reproducing the scripts alone does not reproduce changed data.

Use a separate checkout to retrieve a recorded revision:

```bash
cd /sbgenomics/workspace
git clone https://github.com/ShahLab-NU/heartshare-harmonization.git heartshare-rerun
git -C heartshare-rerun fetch --tags
# Replace NOTEBOOK_TAG_OR_COMMIT with the revision recorded for your analysis.
git -C heartshare-rerun checkout --detach NOTEBOOK_TAG_OR_COMMIT
```

Copy those notebooks into a new personal analysis folder. Set `RELEASE_VERSION`
to the exact historical version, use the preserved release folder and source
data, and start a fresh kernel. Write outputs to a new folder.

The archived pre-update public revision is
`763e45cc3ef4d0404aca12c7562acbd52ec30ae0` (schema 1.1 notebooks). This is not
proof that every older analysis used that commit; prefer its saved provenance.

New BDC release archives also contain notebook snapshots as a recovery option.
Copy them into your personal Data Studio workspace before editing or running.
The public notebook repository is the normal distribution channel; shared
Project Files are not a shared editable notebook workspace.

For exact historical Table One results, use the matching historical notebook
and runtime. Using a newer runtime override creates a new analysis; record its
checksum and keep its outputs separate.

## Maintainer contract

- Publish immutable notebook tags and record the exact commit SHA. Never move
  a published tag to newer code.
- Preserve each published BDC release's runtime, manifest, catalog, standards,
  and mappings. Never replace files behind a release used for saved runs.
- Keep notebook/runtime compatibility metadata and archived notebook copies.
- Test both notebooks against the packaged runtime, including exports and
  feature incompatibility failures, before publishing.
- Require a new release version when changing an already-used release. The
  current v0.2.0 candidate can be finalized as r3 because no saved runs used it.
