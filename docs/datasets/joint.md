# Joint dataset picture (B3 three-arm v0 design)

What the cellduet v0 cross-modal analysis actually has to work with, after pairing **Tahoe-100M** (transcriptomic, 379 small-molecule drugs across 50 cancer cell lines) with three morphological compound datasets in a complementary three-arm structure. Companion to the per-dataset dossiers in this directory: `tahoe-100m.md`, `jump-cp-cpg0016.md`, `cpjump1.md`, `rxrx3.md`. The Replogle dossier (`replogle.md`) and B2 same-cell scan (`scan_b2_same_cell.md`) document a CRISPR-vs-CRISPR alternative that was evaluated and dropped during planning; they remain useful as v1 reference material.

This file covers everything that depends on having all four datasets in view at once.

## v0 research question, restated for B3

> Do drug-induced transcriptomic phenotypes (Tahoe-100M) and drug-induced morphological phenotypes (JUMP-CP / rxrx3-core / CPJUMP1) agree on the same compounds, and where they disagree, does the discordance carry interpretable structure (off-target activity, polypharmacology, cell-type-restricted effects)?

The pairwise per-compound distance matrix on each modality is the unit of analysis. The headline statistic is a Mantel correlation (or RV coefficient) between the two distance matrices restricted to the shared-compound set. Per-compound neighborhood Jaccard quantifies which compounds agree. Discordant compounds are then characterized against drug-target annotations and known polypharmacology, which is the writeup's interpretive layer.

## The three arms

Three cross-modal comparisons, each with a distinct role. All three share the same Tahoe transcriptomic backbone, joined on full InChIKey.

| Arm | Role | Compounds (Tahoe ∩) | Cell context | Morphology embedding | License stack |
|---|---|---|---|---|---|
| **B3b primary** Tahoe × JUMP-CP cpg0016 | Headline statistical test | **228** | Tahoe-50-cancer × U2OS osteosarcoma | CellProfiler 737-d (harmony-corrected) and/or cpcnn 672-d | **CC0 + CC0** |
| **B3a robustness** Tahoe × rxrx3-core | Encoder + cell-type robustness | **145** | Tahoe-50-cancer × HUVEC primary endothelial | OpenPhenom 384-d, Phenom-1 1024-d, Phenom-2 1664-d | CC0 + Recursion EULA (CC-BY-SA-like; **neuroscience carve-out**) |
| **B3c sanity** Tahoe-A549 × CPJUMP1-A549 | Same-cell-line direction-of-effect check | **14** (3 positive controls + 11 treatments) | **A549 literal match** | CellProfiler features only | CC0 + CC0 |

The three-arm structure tests whether the cross-modal agreement pattern survives several confounds in succession: encoder change (Phenom vs CellProfiler/cpcnn), cell-type change (U2OS vs HUVEC), and same-cell-line collapse (A549 in both modalities). Each arm answers a question the other two cannot.

**Why all three matter together.**
- B3b is the headline because it has the largest N and the cleanest license stack.
- B3a tests whether B3b's signal is a U2OS / CellProfiler artifact or a real cross-encoder + cross-cell-context phenotype concordance.
- B3c is the smallest but the only arm where cell-line context is matched. If B3b shows agreement at scale and B3c shows the same direction-of-effect at small N with matched cells, the cross-cell-line caveat is empirically defused; if B3c sign-flips, the writeup has to discuss cell-context-dependence honestly.

## Compound identifier and joining

Tahoe ships canonical SMILES per drug in `drug_metadata.parquet`; the agent-verified intersections used **RDKit-derived full InChIKey** for B3b (228) and B3c (14), and **skeleton InChIKey** for B3a (145; the looser key was needed to bridge stereoisomer differences with rxrx3-core). The cellduet pipeline pins the join policy as:

1. Compute full InChIKey from canonical SMILES on the Tahoe side.
2. Match against pre-computed InChIKey columns on each morphology side (cpg0016 ships InChIKey + SMILES + JCP2022 IDs; CPJUMP1 ships InChIKey; rxrx3-core ships drug names that need mapping to InChIKey via PubChem or DrugBank).
3. Use full InChIKey for B3b and B3c. For B3a, fall back to skeleton InChIKey only if full-key match yields fewer than ~100 compounds; document the looser join in the writeup.

## Cell-context considerations

The three arms span four cell contexts on the morphology side and 50 cancer cell lines on the transcriptomic side. The interpretation matrix:

- **B3b** (Tahoe-pooled × JUMP-U2OS): Tahoe is pooled across its 50 cancer lines per drug to produce one transcriptomic vector; this collapses cell-context heterogeneity into the average drug response. JUMP is U2OS-only, an osteosarcoma adherent line. The cell-context mismatch in B3b is *real but bounded*: both sides are cancer biology; the difference is tumor type, not cancer-vs-normal.
- **B3a** (Tahoe-pooled × rxrx3-HUVEC): Tahoe is again pooled. RxRx3-core is HUVEC, a primary endothelial line, neither cancer nor adherent-fibroblast. Cancer × normal-endothelial is the largest cell-context jump in the v0 design. Concordance found here is the strongest claim of cell-context-invariant phenotype concordance.
- **B3c** (Tahoe-A549-only × CPJUMP1-A549): Tahoe is *subset to A549 cells* before per-drug aggregation, producing one A549-specific transcriptomic vector per drug. CPJUMP1 ships the same A549 lung adenocarcinoma line. This is the only arm where the cell context is literally identical. Limited to 14 compounds (11 once positive controls are excluded).

Optional v0 sub-analysis: for the 228 B3b compounds, also compute a Tahoe-A549-only transcriptomic vector and report how the cross-modal Mantel correlation changes between Tahoe-pooled and Tahoe-A549. This is one extra column in the headline table at trivial compute cost, and it directly probes how much of the B3b cell-context mismatch matters.

## Disease anchor

By composition, **oncology**. Tahoe is 50 cancer cell lines profiled with cancer-relevant compounds (kinase inhibitors, chemo agents, hormone-receptor modulators, epigenetic regulators). JUMP-CP cpg0016, CPJUMP1, and rxrx3-core all profile compounds in cancer or transformed lines. Tahoe ships GPT-4o-derived drug-target annotations covering ~280 unique target genes, with EGFR (12 drugs), KRAS, BRAF, PIK3CA, ALK, MET, FGFR1-4, HDAC1-11, mTOR, CDK4/6 as the densest targets. The writeup's worked vignette is a focal compound or compound family with multiple Tahoe-overlap hits — EGFR inhibitors are the most plausible (12 drugs, all on-target, multiple reach JUMP and rxrx3-core). TP53-stabilizers and KRAS inhibitors are alternative vignette candidates if the EGFR family delivers a degenerate result.

Neurodegeneration, cardiac, and metabolic anchors remain **out of scope**: Tahoe's drug list does not target these gene sets, and the rxrx3-core EULA forbids neuroscience framing.

## License joint

The artifact stack has heterogeneous licenses; this matters for what cellduet can publish.

- **B3b stack: fully CC0**. Tahoe-100M (CC0-1.0 on Hugging Face), JUMP-CP cpg0016 (CC0-1.0 on the Cell Painting Gallery), CellProfiler features (CC0), cpcnn weights and features (CC-BY-4.0 via Zenodo). The headline arm can be redistributed without restriction.
- **B3a stack: CC0 + Recursion EULA**. Tahoe is CC0; rxrx3-core ships under Recursion's bespoke EULA with hard carve-outs (no neuroscience research, no commercial target validation, no use as training data for AI in neuroscience). Derivative analysis is permitted; the writeup cannot be framed as neuroscience and per-file licensing must be documented in any HF dataset push.
- **B3c stack: fully CC0**. Tahoe is CC0; CPJUMP1 is CC0 on the Cell Painting Gallery.

The HF artifact released at the end of v0 (per-compound aggregated embeddings + distance matrices) should be published as **two separate datasets**: one CC0 dataset covering the B3b + B3c outputs, one Recursion-EULA-respecting dataset covering the B3a outputs. Mixing licenses in a single artifact is operationally messy.

## Joint compute plan

All three arms are Colab-Free-tractable. Total v0 download is approximately 5–6 GB once the Tahoe slice is restricted to a tractable per-drug aggregate (the full Tahoe atlas is 337 GB; the cellduet path uses the streamed `pseudobulk_differential_expression` parquet plus `drug_metadata`, totaling a few GB).

1. **Tahoe transcriptomic per-drug vectors.** Stream `pseudobulk_differential_expression` from HF. Filter to non-DMSO drugs, retain `(sample, gene_symbol, log_fold_change)`. Join `sample` to `(drug, cell_line, plate)` via metadata parquets. Two outputs: Tahoe-pooled per drug (`379 × 2,000-HVG` matrix), and Tahoe-A549-only per drug (`(379-or-fewer) × 2,000-HVG`). Plate-matched DMSO controls per the Tahoe HF README.
2. **JUMP cpg0016 per-compound vectors.** Pull `profiles_var_mad_int_featselect_harmony.parquet` (2.64 GB single file) from `s3://cellpainting-gallery/cpg0016-jump-assembled`. Filter wells to the 228 Tahoe-overlap InChIKeys. Aggregate per compound via pycytominer-style mean across replicates. Output: `228 × 737-d`.
3. **rxrx3-core per-compound vectors.** Pull `OpenPhenom_rxrx3_core_embeddings.parquet` (532 MB) and metadata CSV from HF. Filter to the 145 Tahoe-overlap InChIKey-skeleton-matched compounds. Apply EFAAR-style TVN on `EMPTY_control` wells, then per-compound mean across replicates. Output: `145 × 384-d` (OpenPhenom). Optional repeat with Phenom-1 (1024-d) and Phenom-2 (1664-d) parquets.
4. **CPJUMP1-A549 per-compound vectors.** Pull CellProfiler features for the relevant CPJUMP1 plates (~9 MB total slice for 14 compounds × ~4 replicate wells × ~2 timepoints). Filter to A549, compound-perturbation only (drop ORF/CRISPR plates), aggregate per compound. Output: `14 × ~4,000-CellProfiler-features` (the per-plate feature schema differs across plates; pre-aggregation alignment needed).
5. **Per-arm pairwise distance matrices.** Cosine distance is the default. B3b: `228 × 228`. B3a: `145 × 145`. B3c: `14 × 14`.
6. **Cross-modal tests per arm.** Mantel correlation, RV coefficient, per-compound neighborhood Jaccard with permutation null. B3c reports direction-of-effect rather than significance because of small N.
7. **Publish.** Push per-compound aggregated embeddings + distance matrices to two HF datasets: `patrickjreed/cellduet-b3-cc0` (B3b + B3c outputs) and `patrickjreed/cellduet-b3-rxrx3` (B3a outputs).

Total compute footprint per arm is small (sub-second to minutes for all numerical operations once embeddings are loaded). The dominating cost is download / first-load of the cpg0016 harmony parquet (2.64 GB) and the Phenom-2 parquet (2.3 GB) on cold Colab sessions. Drive caching mitigates.

## Joint risks

In rough order of how badly each can compromise v0:

1. **Cell-line context mismatch in the primary arm (B3b).** Tahoe-pooled (50 cancer lines) × U2OS osteosarcoma collapses cell-type heterogeneity on the Tahoe side and pins one cell type on the JUMP side. Concordance found here is *cell-context-averaged* on one side and *one-cell-context-specific* on the other. The Tahoe-A549-restricted alternative for B3b mitigates partially. B3c is the design-level answer: same cell line, smaller N, qualitative confirmation.
2. **Different morphology encoders across arms.** B3b uses CellProfiler / cpcnn, B3a uses Phenom-family, B3c uses CellProfiler only. A finding that holds across arms is encoder-robust; a finding that varies is encoder-specific. The writeup must frame this as a feature, not a bug, but it does mean per-arm headlines will differ in absolute Mantel-r and require careful comparison.
3. **Drug-target annotation noise (Tahoe).** The 280-gene drug-target column was generated by GPT-4o and validated against MedChemExpress. For the writeup's interpretive layer (target-deconvolution / polypharmacology framing), individual claims about specific drugs need DrugBank / ChEMBL cross-checks before publication.
4. **Pre-existing literature on drug-phenotype concordance.** The "do morphology and transcriptomics agree on drug effects" question has prior art via L1000 vs Cell Painting comparisons (e.g., the Subramanian-Way Connectivity Map work) and Recursion's internal benchmarks. The cellduet writeup needs a clear claim of novelty (likely: Tahoe-100M is new, the three-arm structure is new, the discordance-as-signal framing is more developed than prior comparison-only work).
5. **Tahoe pseudobulk DE table provenance.** The exact statistical method used to generate the `pseudobulk_differential_expression` parquet is not in the README schema. Pin it down by reading the paper before trusting the LFCs (per `tahoe-100m.md` Section 7).
6. **Plate / batch effects on the morphology side.** JUMP cpg0016's harmony-corrected parquet handles inter-source heterogeneity; rxrx3-core ships PCA-CenterScale-aligned embeddings with EFAAR TVN on top recommended; CPJUMP1's per-plate feature selection means feature-schema drift across plates and pre-aggregation alignment is mandatory.
7. **Compound replicate-count heterogeneity.** Each morphology dataset has different per-compound replicate density. Notebook 01 must report per-compound replicate-count histograms per arm and either weight or drop low-count compounds.

## Open questions for notebook 01

- Verify the exact 228-compound and 145-compound and 14-compound intersections after re-running the InChIKey joins on freshly-loaded data.
- Per-compound replicate-count distribution per arm. Drop or weight thin-replicate compounds.
- Tahoe-pooled vs Tahoe-A549 cross-modal Mantel-r delta on the B3b 228-compound set. How much of the cross-cell-context caveat is real?
- Sensitivity of B3b's headline Mantel-r to encoder choice (CellProfiler 737-d vs cpcnn 672-d). Pick one as primary.
- Sensitivity of B3a's Mantel-r to Phenom version (OpenPhenom 384 vs Phenom-1 1024 vs Phenom-2 1664). Reportable as an ablation table.
- B3c sign agreement: do the 11 non-control compounds show same-direction effect in transcriptomic and morphological space at A549?
- Drug-target annotation quality spot-check on the EGFR family (12 drugs). Do per-target predicted-MOA rollups make biological sense?

## Summary verdict

The B3 three-arm design is **feasible, ethical (within the rxrx3 EULA), and Colab-Free-tractable**. The 228-compound primary, 145-compound robustness arm, and 14-compound same-cell sanity check together provide three layers of evidence for the headline drug-phenotype concordance claim. Tahoe-100M is the transcriptomic backbone; JUMP-CP cpg0016 is the morphological primary; rxrx3-core and CPJUMP1 are robustness and sanity layers. Replogle moves to a v1 follow-up extending the framework to gene-perturbation phenotypes once v0 ships.
