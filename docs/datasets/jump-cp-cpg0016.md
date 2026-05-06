# JUMP-CP cpg0016 dossier

A primary-source rundown of `cpg0016-jump`, the compound arm of the JUMP-Cell Painting Consortium release. Written to drive v0 implementation planning for the Tahoe-100M × JUMP cross-modal concordance study (B3b plan in [`scan_b3_drug_overlap.md`](./scan_b3_drug_overlap.md)). Numbers were pulled and re-verified against the public AWS S3 bucket `s3://cellpainting-gallery/cpg0016-jump/` and `s3://cellpainting-gallery/cpg0016-jump-assembled/` directly during research; the parquet schemas, well counts, plate counts, and feature dimensionalities below are reproducible by an anonymous `pyarrow` open against those keys.

## Origin and citation

`cpg0016` is the principal dataset of the **JUMP-Cell Painting Consortium**, a public-private partnership of 10 pharmaceutical companies (AbbVie, Astellas, AstraZeneca, Bayer, BMS, Janssen, Merck KGaA, MSD, Pfizer, Servier, Takeda), 6 supporting technology companies, and 2 non-profit partners (Broad Institute, NIH). The project was led by Anne E. Carpenter and Shantanu Singh (Broad Institute), with Srinivas Niranj Chandrasekaran as first author on the dataset paper.

**Dataset paper.** Chandrasekaran et al., *"JUMP Cell Painting dataset: morphological impact of 136,000 chemical and genetic perturbations,"* bioRxiv [2023.03.23.534023](https://www.biorxiv.org/content/10.1101/2023.03.23.534023v2) (v2, posted March 2023; the same preprint is the canonical citation as of May 2026; bioRxiv returned 403 to direct fetch attempts during research, so version-specific deltas are unverified). The peer-reviewed JUMP follow-up that ships morphological maps of gene over-/under-expression is Chandrasekaran et al. 2025 in **Nature Methods** ([PMC12439680](https://pmc.ncbi.nlm.nih.gov/articles/PMC12439680/)), with the analysis repository at [`jump-cellpainting/2025_Chandrasekaran_NatureMethods_Morphmap`](https://github.com/jump-cellpainting/2025_Chandrasekaran_NatureMethods_Morphmap). The Cell Painting Gallery itself is described in Weisbart et al., *"Cell Painting Gallery: an open resource for image-based profiling,"* **Nature Methods** 2024, [PMC11466682](https://pmc.ncbi.nlm.nih.gov/articles/PMC11466682/) (preprint [arXiv:2402.02203](https://arxiv.org/abs/2402.02203)). The pilot dataset that preceded `cpg0016` and that motivates the cellduet same-cell sanity check is Chandrasekaran et al. 2024, *"Three million images and morphological profiles of cells treated with matched chemical and genetic perturbations,"* **Nature Methods** ([10.1038/s41592-024-02241-6](https://www.nature.com/articles/s41592-024-02241-6), [PMC11166567](https://pmc.ncbi.nlm.nih.gov/articles/PMC11166567/)); that is `cpg0000-jump-pilot` / CPJUMP1, covered by a separate dossier and out of scope here.

**License.** **CC0 1.0 Universal** for the entire Cell Painting Gallery, including `cpg0016-jump` ([Cell Painting Gallery README](https://github.com/broadinstitute/cellpainting-gallery), [AWS Open Data registry listing](https://registry.opendata.aws/cellpainting-gallery/)). The gallery README asks for citation of the Weisbart et al. paper plus the dataset's own paper as a courtesy, but there is no contractual restriction on use. This is the cleanest license stack available for any large-scale phenotypic perturbation atlas in 2026.

**Canonical hosting.** AWS S3 bucket `s3://cellpainting-gallery/cpg0016-jump/` (raw images, per-plate features, per-plate deep-learning embeddings) and `s3://cellpainting-gallery/cpg0016-jump-assembled/` (consortium-aggregated profile parquets). Both are public, no-sign-request, served via the AWS Open Data Program ([registry page](https://registry.opendata.aws/cellpainting-gallery/), [data structure docs](https://broadinstitute.github.io/cellpainting-gallery/data_structure.html)). Total Cell Painting Gallery size is **688 TB** as of the 2024 paper; `cpg0016-jump` accounts for **358.4 TB** of that. The compound metadata table is mirrored on GitHub at [`jump-cellpainting/datasets`](https://github.com/jump-cellpainting/datasets/blob/main/metadata/compound.csv.gz).

## Biological scope

**Perturbation type: small molecules** for the compound arm, plus matched ORF over-expression and CRISPR-Cas9 knockout arms for the gene arms. The cellduet B3b plan uses the compound arm only.

**Compound count.** **115,795 unique compounds** (verified locally during research by counting unique `Metadata_JCP2022` values in `s3://cellpainting-gallery/cpg0016-jump-assembled/source_all/workspace/profiles_assembled/COMPOUND/v1.0/profiles_var_mad_int_featselect_harmony.parquet`, which has 803,853 well-level rows and reports 115,795 distinct JCP2022 IDs). The same number drops out of `metadata/compound.csv.gz` on the GitHub mirror, which has 115,797 lines minus header minus 1 duplicate InChIKey. The widely cited "116,000 compounds" rounding ([JUMP Hub data description](https://github.com/broadinstitute/jump_hub/blob/main/explanations/data_description.md), [Cell Painting Gallery paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC11466682/)) and "116,750 unique compounds" figure are both consistent with this once you account for whether DMSO, replicate stocks, and JUMP-MOA / JUMP-Target positive controls are counted. The dossier uses **115,795** as the canonical compound count.

**Cell line.** **U2OS only.** Human osteosarcoma (CVCL_0042, ATCC HTB-96), chosen by the consortium during the pilot phase because "phenotypes are equally or more visible than" alternatives ([JUMP Hub data description](https://github.com/broadinstitute/jump_hub/blob/main/explanations/data_description.md)). The complementary CPJUMP1 pilot also profiled A549, but CPJUMP1 is `cpg0000`, not `cpg0016`. **There is no other cell line in `cpg0016-jump`'s compound arm.** This is the headline cellduet caveat: the morphological signal is in a single cellular context, and that context is osteosarcoma, not the lung/bowel/pancreas/skin cancer panel of Tahoe-100M.

**Plate, well, image structure.** Verified empirically:

- **1,713 unique plates** in the assembled COMPOUND profile (confirmed by counting distinct `Metadata_Plate` values).
- **803,853 wells** with CellProfiler profiles (compound + DMSO + control wells).
- **10 contributing data-generating sources** present in the assembled compound profile (sources 1, 2, 3, 5, 6, 7, 8, 9, 10, 11; counted from `Metadata_Source`). The full bucket lists 12 compound-eligible sources plus source_4 (ORF) and source_13 (CRISPR), but two of the 12 (sources 12 and 14) did not produce well-aggregated compound profiles that survived assembly QC, leaving 10 in the production-ready `profiles_assembled/COMPOUND/v1.0/`. Source contribution is unbalanced; source_9 alone contributes 160,194 wells (~20%), source_3 contributes 51,637 (~6%).
- **>8 million images** total ([Cell Painting Gallery paper Table 1](https://pmc.ncbi.nlm.nih.gov/articles/PMC11466682/)). At ~5 channels × ~6-9 sites per well × ~800k wells, this is consistent.
- **Replicate structure.** Each compound is profiled with **5 replicate wells**, distributed across **2-4 different sites** ([JUMP Hub data description](https://github.com/broadinstitute/jump_hub/blob/main/explanations/data_description.md)). Per-(compound, source) replication is 1-2 wells; per-compound across-source replication is 5. Wells per plate = 384 (CPJUMP-style).

**Cell Painting protocol.** Five fluorescence channels following the [Bray 2016 Nat Protoc](https://doi.org/10.1038/nprot.2016.105) optimized assay (refined in [Cimini 2023 Nat Protoc](https://doi.org/10.1038/s41596-023-00840-9)): **DNA (Hoechst), RNA / nucleoli (SYTO14), ER (concanavalin A), AGP (phalloidin + WGA), and mitochondria (MitoTracker)**. Magnification per the harmonized metadata `Objective_Magnification` column on S3 is **20x** with **NA 1.0** water-immersion. Imaging is multi-site per well (typically 6-9 sites/well, varies by source). The protocol is the same one CPJUMP1 used; consortium goal was procedural reproducibility across 12 different labs and microscopes.

**Controls and positive controls.** Each compound plate contains:

- **DMSO negative controls.** The canonical DMSO row in the metadata is `JCP2022_033924`. Plate-paired DMSO is the standard reference for normalization.
- **JUMP-MOA positive control set.** [`jump-cellpainting/JUMP-MOA`](https://github.com/jump-cellpainting/JUMP-MOA): **90 compounds across 47 mechanism-of-action classes**, 4 replicate wells per compound on a single 384-well plate, dosed at 3 µM, MoAs sourced from [clue.io/repurposing](https://clue.io/repurposing). Designed for replicate-retrieval benchmarking and within-plate batch-effect QC.
- **JUMP-Target-2 connectivity set.** [`jump-cellpainting/JUMP-Target`](https://github.com/jump-cellpainting/JUMP-Target): **301 compounds** targeting **160 genes**, with matched CRISPR and ORF perturbations on companion plates. Used to assess compound-vs-gene connectivity, not as a standard positive control. JUMP-Target-1 is the older variant used for the CPJUMP1 pilot; JUMP-Target-2 is the production layout aligned with `cpg0016`. License: MIT for the metadata.
- **Per-plate positive controls.** 8 positive control wells are placed on each compound sample plate ([JUMP Hub data description](https://github.com/broadinstitute/jump_hub/blob/main/explanations/data_description.md)), drawn from the JUMP-Target / JUMP-MOA pool.

## Chemical scope

**Identifier system.** The Broad's canonical join key is `Metadata_JCP2022`, an integer ID of the form `JCP2022_NNNNNN`. Every compound in the dataset has this ID, and the [`metadata/compound.csv.gz`](https://github.com/jump-cellpainting/datasets/blob/main/metadata/compound.csv.gz) file ships the schema:

```
Metadata_JCP2022,Metadata_InChIKey,Metadata_InChI,Metadata_SMILES
```

**InChIKey is the de facto interoperable join key** (115,795 unique non-DMSO entries, plus DMSO at `JCP2022_033924`). SMILES are also provided. PubChem CID is **not** native to the cpg0016 metadata; it has to be derived via RDKit roundtrip or an external lookup against PubChem.

**Distribution by chemotype / target class / library source.** The JUMP compound library was sourced from the [Broad Drug Repurposing Hub](https://www.broadinstitute.org/drug-repurposing-hub) plus consortium-member-contributed in-house compounds, plus a chemical-diversity backbone. The compound metadata file does not ship per-compound MoA or target annotations directly; those live in the [`jump-cellpainting/datasets`](https://github.com/jump-cellpainting/datasets) repository's `metadata/orf.csv.gz`, `metadata/crispr.csv.gz`, and (for the JUMP-Target subset) `metadata/JUMP-Target-2_compound_metadata.tsv`. For the cellduet question, the relevant chemotype facts are:

- The library is heavily oncology-skewed because the Drug Repurposing Hub pull was oncology-weighted. Kinase inhibitors, DNA-damage / topoisomerase inhibitors, HDAC inhibitors, proteasome inhibitors, and nuclear-hormone-receptor modulators are over-represented.
- The remainder is broad bioactive coverage: GPCR ligands, ion-channel modulators, metabolic enzymes, antimicrobials. Coverage of CNS / neuroscience targets is substantial because the Drug Repurposing Hub spans clinically used CNS drugs, but the cellular context (U2OS) is not neural, so neuroscience MoAs will not produce on-target morphology.
- The exact MoA distribution of the 115,795 compounds is not summarized in a single published table. The JUMPrr `compound_features.parquet` table on the Cell Painting Gallery is the closest published thing; for cellduet, MoA labels can be merged in from the Drug Repurposing Hub release or the Tahoe `drug_metadata.parquet` for the 228-compound joint slice.

**Tahoe ∩ JUMP overlap.** Per [`scan_b3_drug_overlap.md`](./scan_b3_drug_overlap.md), computed locally on the actual `metadata/compound.csv.gz`: **228 compounds match by full 27-character InChIKey**, **230 match by 14-character InChIKey skeleton** (the latter ignores stereochemistry and salt forms). The 2-compound delta is consistent with stereoisomer mismatches between Tahoe's curated SMILES and JUMP's InChIKey provenance. For v0 the conservative join is the 228 full-InChIKey set; for sensitivity analysis the 230 skeleton set can be added. The biological reason this number is high relative to RxRx3 (145) is that both Tahoe and JUMP-CP drew from the Broad Drug Repurposing Hub as their candidate pool. MoA breakdown of the 228 was not separately computed for this dossier; it should mirror the 145-compound RxRx3 breakdown in the scan, weighted toward kinase inhibitors and DNA-damage agents.

## Distribution and access

**Bucket structure.** Two top-level prefixes matter for cellduet:

| Prefix | Purpose | Where the cellduet pipeline reads |
|---|---|---|
| `s3://cellpainting-gallery/cpg0016-jump/source_<N>/` | Per-source raw outputs: images, CellProfiler well-level profiles, per-plate deep-learning embeddings | Per-plate parquets if you need plate-level granularity |
| `s3://cellpainting-gallery/cpg0016-jump-assembled/source_all/workspace/profiles_assembled/` | Consortium-aggregated, pipeline-processed profile parquets at multiple processing stages | Single COMPOUND parquet for v0 |

Per-source structure (verified by listing `source_4` as the canonical example): each source has `images/`, `workspace/`, and `workspace_dl/`. The `workspace/` tree contains `analysis/`, `backend/` (per-plate SQLite), `load_data_csv/`, `profiles/<batch>/<plate>/<plate>.parquet` (per-plate well-level CellProfiler profiles, one parquet per plate, **~13 MB each, 384 rows × 4,765 columns of which 4,762 are CellProfiler features**), plus `software/` and `structure/`. The `workspace_dl/` tree contains `embeddings/` (per-image deep-learning embeddings) and `profiles/<network>/<batch>/<plate>/<plate>.parquet` (per-plate well-aggregated DL profiles).

**Assembled compound parquet inventory.** The single most useful artifact for cellduet is in `cpg0016-jump-assembled/source_all/workspace/profiles_assembled/COMPOUND/v1.0/`. Sizes and shapes verified by anonymous `pyarrow` open against the bucket:

| File | Rows (wells) | Feature columns | Size |
|---|---|---|---|
| `profiles.parquet` | 804,844 | 3,673 | 9.91 GB |
| `profiles_var.parquet` | 803,853 | feature-selected | 8.76 GB |
| `profiles_var_mad.parquet` | 803,853 | 3,180 | 11.33 GB |
| `profiles_var_mad_int.parquet` | 803,853 | 3,180 | 11.28 GB |
| `profiles_var_mad_int_featselect.parquet` | 803,853 | 737 | **2.62 GB** |
| `profiles_var_mad_int_featselect_harmony.parquet` | 803,853 | 737 | **2.64 GB** |

All six files share the metadata schema `Metadata_Source, Metadata_Plate, Metadata_Well, Metadata_JCP2022`. Sister bundles `ORF/`, `CRISPR/`, and `ALL/` exist with the same naming pattern. **The harmony-corrected, feature-selected, batch-aware compound parquet is 2.64 GB and is the v0-ready turnkey artifact.** The raw 4,762-feature per-plate CellProfiler parquets are also available if a consumer needs them for a different aggregation rule, at ~13 MB per plate × 1,713 plates ≈ 22 GB total.

**Auth.** Public, no-sign-request, no requester-pays. All listings and ranged-byte fetches in this dossier were performed without credentials. Streaming via `boto3` / `s3fs` / `pyarrow.fs.S3FileSystem(anonymous=True)` works directly on Colab without any AWS account.

**Streaming-friendliness for Colab.** The 2.64 GB feature-selected harmony parquet fits trivially in Colab Free RAM if loaded with column selection or row filtering. Reading only the 228 Tahoe-overlap compounds is a `pyarrow.parquet.read_table(..., filters=[('Metadata_JCP2022', 'in', list_of_228_jcp_ids)])` call that returns a tiny dataframe (~5,000 rows × 737 features ≈ 14 MB).

## Pre-computed artifacts

This is the section that decides v0 feasibility. Empirical inventory from S3, May 2026:

**(a) CellProfiler hand-engineered features.** This is the canonical JUMP product.

- **Per-plate well-level profiles**: `s3://cellpainting-gallery/cpg0016-jump/source_<N>/workspace/profiles/<batch>/<plate>/<plate>.parquet`. Each plate parquet is 384 wells × 4,762 CellProfiler features (verified on `source_4/...BR00117035.parquet`). Approximately 13 MB per plate.
- **Assembled compound parquet**: 803,853 wells × 3,673 features (raw assembly) → 803,853 wells × **737 features** (after `var → mad → int → featselect → harmony` from [`broadinstitute/jump-profiling-recipe`](https://github.com/broadinstitute/jump-profiling-recipe)). Pipeline stages: variance threshold (`pycytominer.feature_select` variant filter), MAD normalization (`pycytominer.normalize`), rank inverse normal transform, correlation+blocklist feature selection, and Harmony batch correction via [`harmonypy`](https://github.com/slowkow/harmonypy). The recipe is BSD-3-Clause; the v1.0 release (the only published version) targets the consortium dataset directly.
- License: CC0-1.0 (inherited from the Cell Painting Gallery).

**(b) CellProfiler-CNN ("cpcnn") deep features.** Available across all 12 compound sources at `s3://cellpainting-gallery/cpg0016-jump/source_<N>/workspace_dl/profiles/cpcnn_zenodo_7114558/<batch>/<plate>/<plate>.parquet`. Verified empirically:

- Architecture: EfficientNet-B0 trained on Cell Painting single-cell images. Model: [`zenodo.7114558`](https://zenodo.org/records/7114558), Cell_Painting_CNN_v1, paper [Moshkov et al. 2024 *Nat Commun* "Learning representations for image-based profiling of perturbations"](https://doi.org/10.1101/2022.08.12.503783).
- **Embedding dimensionality: 672-d per well** (single concatenated `all_emb` array column; verified by reading row 0 of `BR00117035.parquet`).
- Aggregation level: per-well (mean of single-cell embeddings within the well).
- File size: ~1.6 MB per plate parquet × 1,713 plates ≈ 2.7 GB total across the compound arm.
- License: CC-BY-4.0 on the model; data layer inherits CC0 from the gallery.

**(c) EfficientNet-V2-S ImageNet-21k embeddings.** Also available across all 12 compound sources at `s3://cellpainting-gallery/cpg0016-jump/source_<N>/workspace_dl/profiles/efficientnet_v2_imagenet21k_s_feature_vector_2_0260bc96/<batch>/<plate>/<plate>.parquet`. Verified empirically:

- Architecture: EfficientNet-V2-S, the public ImageNet-21k checkpoint from TensorFlow Hub (`efficientnet_v2_imagenet21k_s_feature_vector/2`).
- **Embedding dimensionality: 5 channels × 1,280-d = 6,400-d per well**, stored as five list columns `agp_emb`, `dna_emb`, `er_emb`, `mito_emb`, `rna_emb` (each 1,280-d). Concatenation is the user's choice.
- Aggregation level: per-well.
- License: model is Apache-2.0 via TensorFlow Hub; data layer inherits CC0 from the gallery. **Important caveat**: this encoder was never trained on cell-painting imagery, so the features are general-purpose visual statistics, not phenotype-tuned. Useful as a baseline against cpcnn, not as the primary phenomic signal.

**(d) cpdistiller_mesmer (knowledge-distilled deep features).** Source 4 only at this time: `s3://cellpainting-gallery/cpg0016-jump/source_4/workspace_dl/profiles/cpdistiller_mesmer_s41467_025_62193_z/`. Tied to a [Nature Communications 2025 paper (s41467-025-62193-z)](https://doi.org/10.1038/s41467-025-62193-z) on knowledge distillation for cell-painting representations. Source coverage is incomplete; not the v0 default.

**(e) OpenPhenom / Phenom-1 / Phenom-2 / Cytoself / Cellomic foundation-model embeddings.** **Not present on the Cell Painting Gallery as of May 2026.** Despite the 2024 OpenPhenom-S/16 release ([Recursion press release](https://ir.recursion.com/news-releases/news-release-details/recursion-announces-release-openphenom-s16-google-clouds-model)), and despite published OpenPhenom benchmarks reporting higher StringDB recall on JUMP-CP cpg0016 than CellProfiler features ([benchmark blog](https://www.nature.com/articles/s41598-025-88825-4)), Recursion has not contributed pre-computed OpenPhenom embeddings of the JUMP imagery to the public gallery. Phenom-1 and Phenom-2 weights are proprietary; their embeddings on JUMP have not been released under any license. Cytoself, MAE-CellPaint, and Cell-DINO have published-paper-level evaluations on JUMP but not gallery-deposited artifacts. **The cellduet pipeline cannot use OpenPhenom embeddings on JUMP without running OpenPhenom inference itself**, which requires either (a) downloading the imagery (~358 TB; not feasible) or (b) running OpenPhenom on per-image patches the consortium provides via DeepCellProfiler-compatible single-cell crops (not currently available at scale on the gallery). For v0 the cpcnn 672-d profile is the best deep-feature artifact already on the gallery.

**(f) JUMPrr reference tables.** The [JUMP Hub](https://broadinstitute.github.io/jump_hub/) publishes per-treatment summary tables under the JUMPrr (JUMP Recipe-ready) brand: `compound_features.parquet` (top-feature-vs-DMSO ranking per perturbation), `compound_significance.parquet` (phenotypic-activity p-values per perturbation), `compound_gallery.parquet` (cropped image links). These are the per-treatment ("consensus") aggregated views, with one row per JCP2022 compound rather than one row per well. Hosted in the gallery but exact S3 paths are referenced through the JUMP Hub HTML docs rather than printed in the README. They are gigabyte-or-less and Colab-friendly. **For cellduet, these are an alternative starting point if a per-treatment endpoint is wanted directly**, skipping the well-level aggregation step that pycytominer would otherwise do.

**Recommended v0 artifact: `profiles_var_mad_int_featselect_harmony.parquet`** from `cpg0016-jump-assembled/source_all/workspace/profiles_assembled/COMPOUND/v1.0/`. Reasons: 737 features after the consortium's own batch-correction pipeline, 803,853 well-level rows, 2.64 GB total, CC0, single file. The 672-d cpcnn deep embedding is the secondary head-to-head artifact for the "do deep features track CellProfiler features?" sensitivity question, requiring per-source assembly (10 sources × 1,713 plates' worth of small parquets ≈ 2.7 GB).

## Compute footprint for v0

Colab Free is the binding constraint: **~12 GB RAM, 15 GB persistent Drive, T4 with ~15 GB VRAM, 12-hour session, ~90-min idle disconnect**.

**Smallest useful slice for cellduet.** The 228-compound Tahoe-overlap intersection, restricted to U2OS, with the harmony-corrected feature-selected CellProfiler parquet:

1. Stream-filter `profiles_var_mad_int_featselect_harmony.parquet` on `Metadata_JCP2022 IN <228 IDs>` via `pyarrow.parquet.read_table(..., filters=...)`. Expected output: ~228 compounds × 5 replicates × ~2 sources averaged = ~2,200-5,000 well rows × 737 features × float32 ≈ **15 MB**. Trivially in RAM.
2. Aggregate per-compound (mean across replicates and sources via `pycytominer.consensus` or a pandas groupby). Output: **228 compounds × 737 features × float32 ≈ 670 KB**.
3. Compute pairwise cosine distance matrix on the aggregate. **228 × 228 floats ≈ 200 KB.** Microseconds.
4. Mirror the same pipeline for the 672-d cpcnn embedding by concatenating per-source / per-plate cpcnn parquets, filtered to the 228 JCP2022 IDs. Per-plate parquets are 1.6 MB × ~50 plates that contain at least one of the 228 compounds (varies by plate layout; bounded above by 1,713 plates × 1.6 MB = 2.7 GB if all are streamed). The post-filter aggregate is **228 × 672 × float32 ≈ 615 KB**. Essentially identical compute footprint to the CellProfiler path.

**What does not fit.** The full ~358 TB image corpus, obviously. The whole well-level harmony parquet (2.64 GB) fits in RAM with margin, but loading it twice or holding intermediate copies would push toward the 12 GB ceiling; column-projection at read time is the safer pattern. The unprocessed 9.91 GB `profiles.parquet` should not be loaded whole; only chunk-streamed.

**Persistent caches.** Per `CLAUDE.md` execution model, the per-(compound, feature) aggregate (~670 KB) is small enough to push to a HuggingFace dataset (`patrickjreed/cellduet-jump-pertreatment` or similar). The per-well filtered slice (~15 MB) is too large to redownload per session without caching but small enough to keep on Drive at `/content/drive/MyDrive/cellduet/cache/`.

## Aggregation considerations

JUMP's data structure is (compound) → (5 replicate wells) → (2-4 sources / sites) → (8-9 imaging sites per well) → (5 channels). The CellProfiler well-level aggregation already collapses per-cell and per-site detail to a single row per well, so the v0 starting point is well-level, not single-cell. From there, two more aggregation steps are needed:

1. **Plate / batch normalization.** The harmony parquet has already been MAD-normalized per plate, INT-transformed, feature-selected, and Harmony-corrected at the source level. No additional per-plate normalization is required for v0.
2. **Replicate aggregation to per-(treatment) consensus.** For each compound, average the 737-d feature vector across the 5 replicate wells (typically ~10-15 wells when summed across sources). The community standard is the `pycytominer.consensus` function, which computes a median or mean of replicate well profiles per perturbation. The function is documented in [`pycytominer/README.md`](https://github.com/cytomining/pycytominer/blob/main/README.md), and the JUMPrr `compound_features.parquet` reference table is itself produced by this pipeline.

**Recommendation: use pycytominer's `consensus` function with median aggregation, as the consortium does.** It is one line of code, it handles the per-(JCP2022, source) groupby cleanly, and it matches the convention every downstream JUMP analysis paper uses, which keeps the cellduet methodology directly comparable to published phenotypic profiling. There is no payoff to implementing aggregation by hand: the median-of-wells reduction is trivial, but using pycytominer means future methods improvements (e.g. plate-position-aware aggregates) drop in for free. Install: `pip install pycytominer`.

## Known caveats

- **Plate / batch effects.** Cell Painting at this scale across 12 sites is *the* canonical batch-effects benchmark. The consortium's response is the harmony-corrected feature-selected parquet (the file the v0 plan recommends), but Harmony is a linear method that does not fully eliminate site-specific structure for compounds whose true phenotype lies near a site axis. The first-pass v0 sanity check is: per-(compound, source) feature vectors should be more similar to each other than to (different compound, same source) vectors. If that does not hold, the harmony step is under-correcting and a deeper batch-correction pass is warranted. The consortium [Morphmap repository](https://github.com/jump-cellpainting/2025_Chandrasekaran_NatureMethods_Morphmap) reports this kind of QC in its `00*` analysis notebooks.
- **U2OS context.** Osteosarcoma (P53-mutant, RB1-altered, near-tetraploid). It is not in the Tahoe panel of 50 cancer cell lines (which is dominated by lung, bowel, pancreas, skin); cell-line context mismatch is structural to the B3b plan. A "drug effect in U2OS" is a real morphological phenotype, but it is not the same biology as "drug effect in A549 lung adenocarcinoma." The cellduet writeup must frame the cross-modality concordance as gene-/MoA-intrinsic signal that survives across cancer-cell-line context, not as a same-cell-line comparison. This is the single most important caveat.
- **CellProfiler vs deep embedding.** CellProfiler features are interpretable, hand-engineered (areas, intensities, textures, neighbor relations), and well-validated, but they collapse spatial / morphological detail into hundreds of measurements that may be noise-dominated for subtle phenotypes. cpcnn features are learned from cell-painting imagery (positive: phenotype-tuned), but the encoder is small (EfficientNet-B0) and old (2022). Neither is strictly better; the v0 plan should report both as a sensitivity analysis. **OpenPhenom is the artifact the field would most want, but it is not in the gallery for JUMP**, so the cellduet writeup should explicitly note the OpenPhenom comparison as a v1 stretch goal, not v0 scope.
- **JUMP-MOA "ground truth" mechanism-of-action labels.** The 90-compound JUMP-MOA set has 47 hand-curated MoA classes. These are intended for replicate-retrieval and MoA-classification benchmarks within JUMP's own studies. **They do not extend to the full 115,795-compound library**, so they cannot serve as a dense MoA label vector for the joint Tahoe ∩ JUMP set. Of the 228 Tahoe-overlap compounds, only the small subset that is also in JUMP-MOA (likely <10) carries a JUMP-MOA label. For the cellduet 228-compound joint analysis, MoA annotations should come from the Tahoe `drug_metadata.moa-broad` / `moa-fine` columns, not from JUMP-MOA.
- **Replicate count is shallow per source.** 5 wells per compound, but typically 1-2 per source. Within-source statistical power for any single (compound, source) pair is bounded; aggregation across sources is required to get a stable per-compound estimate, and that aggregation makes the per-source contribution information implicit. For v0, the consortium-produced harmony-corrected parquet has already done this aggregation, so the issue is only relevant if the project re-aggregates from per-plate inputs.
- **Source distribution is unbalanced.** Source_9 contributes ~20% of well rows; source_3 contributes ~6%. A naïve per-source mean treats sources as if they were equal, which they are not; an unweighted across-source aggregation can mask source-specific effects. The harmony-corrected file is the safest starting point because it has already accounted for the unequal source contribution, but if the project recomputes consensus features from non-harmonized inputs, source-balanced sampling matters.
- **`profiles_var_mad_int_featselect_harmony.parquet` schema is sparse on metadata.** Only 4 metadata columns ship: `Metadata_Source, Metadata_Plate, Metadata_Well, Metadata_JCP2022`. To get InChIKey / SMILES / MoA, an additional left-join against `metadata/compound.csv.gz` from the GitHub mirror is required. This is a 30-second pandas merge, but it is a step the v0 notebook must include explicitly.

## Joint-with-Tahoe-100M considerations

**Compound overlap: 228 (full InChIKey) / 230 (skeleton).** Verified in [`scan_b3_drug_overlap.md`](./scan_b3_drug_overlap.md) by joining Tahoe's `drug_metadata.parquet` (`canonical_smiles` → RDKit-derived InChIKey) against JUMP's `metadata/compound.csv.gz` `Metadata_InChIKey`. Re-running this overlap is a 1-minute script and should be the first cell of `notebooks/01_data_exploration.ipynb`. The 2-compound spread between full and skeleton InChIKey is consistent with stereoisomer mismatches; for v0 the conservative choice is the 228-compound full-key intersection.

**Cell-line overlap: 0.** JUMP cpg0016 compounds are profiled in U2OS only. Tahoe's 50 cancer cell lines do not include U2OS (U2OS is not a Tahoe cell line per `cell_line_metadata.parquet`; verified in `scan_b3`). The cellduet B3b primary analysis is therefore a **cross-cell-context comparison**: 47 Tahoe cancer lines × U2OS via 228 shared compounds. A same-cell-line sanity check exists via the CPJUMP1 / `cpg0000` arm (A549 + ~15 shared compounds), covered in a separate dossier. There is no path to a same-cell-line comparison at scale on `cpg0016` alone.

**Gene-target rollup.** Tahoe's `drug_metadata.targets` column carries a GPT-4o-derived gene-target annotation for 264 of 379 drugs covering 280 unique target gene symbols. JUMP cpg0016 does not ship per-compound target annotations on the canonical compound metadata; targets are inferred either from the JUMP-Target-2 subset (160 genes, 301 compounds, hand-curated) or from external databases (DrugBank, ChEMBL, Drug Repurposing Hub). For the 228-compound joint set, the workable per-target rollup is:

1. Take the Tahoe `targets` column for the 228 shared compounds.
2. Group compounds by target gene; expect ~100-150 unique target genes covered with ≥2 compounds per target (empirical, but consistent with the 280-gene Tahoe ceiling restricted to a 228-compound subset).
3. Per target, average the per-compound aggregate transcriptomic phenotype (from Tahoe pseudobulk LFC, Section 6 of [`tahoe-100m.md`](./tahoe-100m.md)) and the per-compound aggregate morphological phenotype (737-d harmony or 672-d cpcnn from JUMP).
4. Compute target × target distance matrices in both modalities; correlate.

The target-rollup endpoint is a per-(target gene) cross-modality concordance score. It is the cellduet B3b headline figure. **The denominator is bounded by Tahoe's 280 target genes, not JUMP's full library**, because Tahoe is the side that ships the target annotation.

## Open questions

These cannot be answered without actually loading data on Colab. Notebook 01 should resolve them in this order:

1. **Re-verify the 228-compound overlap.** Run the InChIKey join end-to-end in a Colab cell. Confirm the 228 number, the 230 skeleton-key number, and the 2-compound stereo delta. If the number drifts (because either dataset is updated post-May-2026), update the dossier.
2. **Per-source distribution of the 228 compounds.** Some compounds may be in only one source's plates; that bounds the within-source replicate count for those compounds. Group the harmony parquet by `(Metadata_JCP2022, Metadata_Source)` for the 228-compound subset and inspect.
3. **Are CellProfiler harmony-corrected features and cpcnn features locally consistent on JUMP-MOA?** The 90-compound JUMP-MOA set has 47 known MoA labels. Within-MoA replicate retrieval should be high in both feature spaces; cross-MoA distance should be low. If cpcnn massively beats CellProfiler on this benchmark (likely), it argues for cpcnn as the primary v0 morphological feature; if they are comparable, CellProfiler is preferred for interpretability.
4. **Does the JUMPrr `compound_features.parquet` per-treatment table give cleaner phenotype vectors than running pycytominer.consensus on the harmony parquet?** Empirical; both are CC0; load both for a small subset and compare.
5. **Plate / source confound for the 228-compound subset.** If the 228 overlap concentrates in a small number of plates (e.g., a couple of compound libraries that the Drug Repurposing Hub ships together), the cross-cell-context concordance will be confounded with plate signal. The fix is to confirm the 228 compounds are spread across many plates (expected, given the 1,713-plate scale and randomized layouts) and to require ≥3 distinct plates per compound for inclusion.
6. **Should the v0 morphological feature dimension be 737 (CellProfiler-harmony), 672 (cpcnn), or something else?** Only one feature space is needed for the headline figure; the other is a sensitivity check. The decision is empirical, made after question 3.
7. **Whether OpenPhenom embedding on JUMP can be obtained without running pixel-level inference.** The Recursion / Broad collaboration may release these in the future; the JUMP Hub is the place to watch. If they appear during the project window, the cellduet pipeline should swap them in as the primary morphological feature, given OpenPhenom's published phenotype recall advantage on JUMP.
8. **MoA enrichment of the 228-compound joint set.** Compute the Tahoe `moa-broad` distribution restricted to the 228 compounds; report the top 10 MoA classes and whether kinase inhibitors / DNA-damage agents dominate as the rxrx3-core 145-compound joint set did. This is a one-cell pandas value_counts.
9. **Target gene coverage of the 228-compound joint set.** How many of Tahoe's 280 target genes survive when restricted to the 228 shared compounds? Likely ~100-200; this is the denominator for the target-rollup figure and bounds the statistical power of the headline concordance result.
