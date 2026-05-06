# cellduet v0 — design spec

**Date**: 2026-05-06
**Author**: Patrick J. Reed (with Claude as planning collaborator)
**Status**: Design approved, ready for writing-plans handoff
**Companion documents**: `docs/datasets/joint.md` (dataset-stack reference), per-dataset dossiers in `docs/datasets/`

## Purpose

This spec captures the v0 design that emerged from the 2026-05-06 brainstorming session and the dossier-driven dataset feasibility pass. It is the input artifact for the writing-plans skill, which will convert it into an executable, milestone-by-milestone implementation plan.

## Research question

> Do drug-induced transcriptomic phenotypes (from Tahoe-100M, scRNA-seq across 50 cancer cell lines under 379 small-molecule perturbations) and drug-induced morphological phenotypes (from Cell Painting datasets in U2OS, HUVEC, and A549) agree on the same compounds, and where they disagree, does the discordance carry interpretable structure (off-target activity, polypharmacology, cell-context-dependence)?

The unit of analysis is the per-compound phenotype vector. The headline statistic is a Mantel correlation between the per-modality pairwise compound-compound distance matrices, restricted to the shared-compound set per arm. Per-compound neighborhood Jaccard quantifies which compounds agree. Discordance is characterized against drug-target annotations and prior polypharmacology.

## v0 scope (in)

- Pre-computed embeddings only. No image-from-pixels work, no encoder retraining, no foundation-model inference at the cell level.
- Three-arm cross-modal comparison (B3b primary, B3a robustness, B3c sanity), all joined on full InChIKey.
- One worked focal-compound-family vignette (default: EGFR inhibitors, ~12 Tahoe-overlap drugs).
- Discordance interpretation against Tahoe drug-target annotations.
- Two HF dataset publications (CC0 stack + rxrx3-EULA-respecting separate dataset).
- Paper-style writeup as a README extension or standalone blog post, plus cleaned notebooks rendered to HTML.

## v0 scope (out)

- Encoder retraining of any kind.
- Foundation-model inference (STATE / Tahoe-x1 / scGPT) on Tahoe; the native `pseudobulk_differential_expression` parquet is sufficient.
- Gene-perturbation cross-modal analysis (Replogle Perturb-seq × CRISPR-KO Cell Painting). Deferred to v1.
- Shared-latent contrastive model. Deferred to v1.
- HF Spaces Gradio demo. Deferred to v1.
- Disease anchors other than oncology (neurodegeneration is closed by Recursion EULA + composition; cardiac and metabolic are too sparse).
- Recomputing Tahoe pseudobulk DE from raw counts (use the published parquet unless notebook 02 surfaces a structural problem).

## Definition of "shipped v0"

v0 is shipped when **all** of the following hold:

1. The compound intersections are verified empirically: 228 ± 5 (B3b), 145 ± 10 (B3a), 14 (B3c).
2. Per-compound phenotype embeddings are produced for each arm, persisted to HF as named datasets (`patrickjreed/cellduet-tahoe-percompound`, `patrickjreed/cellduet-jump-percompound`, the rxrx3 + CPJUMP1 outputs), all with documented per-file licensing.
3. Mantel correlation, RV coefficient, and per-compound neighborhood Jaccard are computed and reported per arm.
4. The Tahoe-pooled vs Tahoe-A549 sensitivity comparison is reported on the B3b 228-compound set.
5. A worked focal-compound-family vignette (default EGFR family) is presented end-to-end with at least three named-compound cases (concordant, discordant-with-explanation, mixed).
6. Notebooks 00–08 are clean (cleared outputs) and render to HTML for portfolio display.
7. A README extension or blog post communicates the result, the framing, and the caveats (cell-context mismatch, encoder differences across arms, drug-target annotation noise) honestly.
8. The repo's `docs/CONTEXT.md`, `CLAUDE.md`, `README.md` reflect the as-shipped state.

The Mantel-r value itself is **not** an acceptance criterion. v0 ships whether the cross-modal correlation is high, low, or mixed. Both outcomes are findings, framed honestly.

## The three arms

Per `docs/datasets/joint.md`. Repeated here only at the level of role and gate-numbers; full detail lives in the dossier.

| Arm | Role | Compound count | Gate to clear |
|---|---|---|---|
| **B3b primary** Tahoe × JUMP-CP cpg0016 | Headline statistical test | 228 | ≥200 after empirical verification |
| **B3a robustness** Tahoe × rxrx3-core | Encoder + cell-type robustness | 145 | ≥100 after empirical verification |
| **B3c sanity** Tahoe-A549 × CPJUMP1-A549 | Same-cell direction-of-effect check | 14 | ≥10 after positive-control filtering |

## Notebook structure

Eight notebooks, each delivering one artifact and gating the next.

| # | Title | Inputs | Outputs | Gates |
|---|---|---|---|---|
| 00 | `00_environment_smoke.ipynb` | (none) | Confirmed Colab + HF + Drive runtime | T4 GPU available, HF login OK, Drive mounted |
| 01 | `01_intersections.ipynb` | Tahoe `drug_metadata`, JUMP cpg0016 metadata, rxrx3-core metadata, CPJUMP1 metadata | `compound_manifest.parquet`, replicate-count histograms per arm, HF push of compound manifest | All three intersection counts clear their gates |
| 02 | `02_tahoe_percompound.ipynb` | Tahoe `pseudobulk_differential_expression`, metadata parquets | `tahoe_pooled_per_compound.h5ad`, `tahoe_a549_per_compound.h5ad` | Per-compound vectors materialized for all 379 drugs (and all A549 drugs); HVG selection documented |
| 03 | `03_jump_percompound.ipynb` | JUMP cpg0016 harmony parquet | `jump_per_compound.parquet` (228 × 737-d), optional cpcnn ablation | All 228 B3b compounds aggregated; per-compound replicate-count documented |
| 04 | `04_rxrx3_percompound.ipynb` | rxrx3-core OpenPhenom parquet, metadata | `rxrx3_per_compound.parquet` (145 × 384-d), optional Phenom-1/2 ablation | TVN applied; all 145 B3a compounds aggregated |
| 05 | `05_cpjump1_percompound.ipynb` | CPJUMP1 CellProfiler features for relevant A549 plates | `cpjump1_a549_per_compound.parquet` (14 × ~4K) | Per-plate feature alignment done; all 14 B3c compounds aggregated |
| 06 | `06_concordance.ipynb` | All four per-compound artifacts + compound manifest | Per-arm distance matrices, Mantel-r, RV, neighborhood Jaccard, permutation null, sensitivity table | Headline numbers reported per arm |
| 07 | `07_interpretation.ipynb` | Per-arm concordance results + Tahoe drug-target annotations | Concordant/discordant compound clusters, EGFR-family worked vignette, figures | At least 3 named compounds worked through |
| 08 | `08_polish.ipynb` (or non-notebook task) | All prior notebooks | Cleaned notebooks rendered to HTML, README extension or blog post, HF dataset pushes | Repo passes `ruff check . && ruff format .` and notebook outputs are cleared |

## Milestone calendar (rough)

Working assumption: 4–6 weeks of evening work, ~10–15 hours/week. This is a target, not a contract. If reality forces a slip, the slip is documented honestly in CLAUDE.md status.

- **Week 1**: Notebooks 00, 01. Confirm runtime, verify intersections, push compound manifest. Goes/no-goes the rest of v0.
- **Week 2**: Notebook 02 (Tahoe per-compound). The most data-engineering-heavy notebook because of the streamed pseudobulk parquet.
- **Week 3**: Notebooks 03 + 04 (JUMP and rxrx3 per-compound). Both are smaller-data than 02; can be done in one week if 02 went well, or split into weeks 3-4 otherwise.
- **Week 4**: Notebook 05 (CPJUMP1) + Notebook 06 (concordance). Headline result lands here.
- **Week 5**: Notebook 07 (interpretation, EGFR vignette). Most prose-heavy.
- **Week 6**: Notebook 08 (polish, writeup, HF pushes). Buffer week.

If v0 over-runs into weeks 7–8, the most likely cause is notebook 02 (Tahoe scale) or notebook 06 (statistical interpretation). Both are surfaceable and can be discussed before sliding the milestone.

## Acceptance gates per arm

These are the empirical conditions that need to hold for each arm's result to be considered usable, beyond the size-of-overlap gates above.

- **B3b primary**: per-compound replicate count ≥3 wells for ≥80% of the 228 compounds (after harmony correction); CellProfiler-737 vs cpcnn-672 cross-encoder Mantel-r within 0.1 (otherwise treat encoder-choice as a finding, not a control).
- **B3a robustness**: per-compound replicate count ≥3 wells for ≥80% of the 145 compounds; PCA-CS + EFAAR TVN applied; no obvious per-plate residual structure dominating distances.
- **B3c sanity**: 11 non-control compounds with at least n=4 replicate wells per timepoint; sign agreement across modalities for a majority of the 11.

## Risk register

The seven risks documented in `docs/datasets/joint.md` § "Joint risks" plus three operational risks:

| Risk | Severity | Mitigation |
|---|---|---|
| Cell-line context mismatch on B3b primary | High | B3a + B3c probe it directly. Tahoe-pooled vs Tahoe-A549 sensitivity column. Honest framing in writeup. |
| Different morphology encoders across arms | Medium | Reframe as feature, not bug. Encoder-robust findings carry more weight. |
| Drug-target annotation noise (Tahoe GPT-4o) | Medium | Cross-check focal-vignette compounds against DrugBank / ChEMBL before publication. |
| Prior literature on drug-phenotype concordance | Medium | Frame novelty around (a) modern dataset stack, (b) three-arm structure, (c) discordance-as-signal. |
| Tahoe pseudobulk DE table provenance unclear | Medium | Read paper before trusting LFCs; consider single-cell sanity check on a small slice if structural issue surfaces. |
| Plate / batch effects on morphology side | Medium | Use harmony-corrected JUMP parquet, EFAAR TVN on rxrx3-core, per-plate alignment on CPJUMP1. |
| Compound replicate-count heterogeneity | Low | Notebook 01 reports histograms; downweight or drop low-count compounds. |
| Colab Free session disconnect mid-pipeline | Operational | Cache to Drive at every notebook boundary; HF push of compound manifest after notebook 01. |
| Computer-time / personal-time slippage | Operational | Weekly milestones; surface slippage to CLAUDE.md status; week 6 is buffer. |
| Scope creep into v1 territory | Operational | Spec is explicit about out-of-scope; reject foundation-model inference, encoder training, contrastive model in v0. |

## Reproducibility commitments

- Every notebook starts with `!pip install -q git+https://github.com/PatrickJReed/cellduet.git@main` to force the package to be self-contained.
- Notebooks commit with cleared outputs.
- Compound joining is on full InChIKey (B3b, B3c) or skeleton InChIKey (B3a only, documented as the looser join).
- All HF artifacts include a `dataset_card.md` with provenance, license, and reproduction instructions.
- The `cellduet` Python package keeps two-modality I/O helpers (Tahoe loader, JUMP loader, rxrx3 loader, CPJUMP1 loader) and one statistical-test helper (Mantel + RV + neighborhood Jaccard); module structure emerges from working code, not pre-designed.
- Random seeds documented per notebook for permutation nulls.

## Open decisions deferred to implementation

These are intentional unknowns to resolve in writing-plans / notebook execution, not to settle in this spec:

- **HVG selection on Tahoe**: 2,000 (STATE convention) or project-specific HVG list across the 47 lines? Default is 2,000; revisit if signal-to-noise looks poor in notebook 06.
- **JUMP encoder choice for B3b primary**: CellProfiler-737 (community standard) or cpcnn-672 (deep encoder, more recent). Default CellProfiler-737; report cpcnn as ablation.
- **rxrx3 encoder choice for B3a**: OpenPhenom-384 (smallest, fastest) primary, Phenom-1 + Phenom-2 as ablation table.
- **Aggregation rule for per-compound morphology**: arithmetic mean across replicate wells (default) or median (robust to outlier guides). Compare in notebook 03/04 if time permits.
- **Distance metric**: cosine (default) or Euclidean post z-scoring? Cosine is robust to magnitude differences in encoder outputs, but the choice can be revisited.
- **Permutation null structure**: simple compound shuffle, or compound-class-stratified shuffle? Default simple; stratified if compound classes show structure.

## Stretch / v1 backlog

In rough priority order. None of these are in v0 scope; they exist here so writing-plans does not pull them in by accident.

1. **Gene-perturbation cross-modal extension** (Replogle K562 GW × CRISPR-KO Cell Painting from JUMP / PERISCOPE). The original CRISPR-vs-CRISPR question, now answerable as a follow-up using the same v0 statistical machinery. Dossier already drafted at `docs/datasets/replogle.md`.
2. **Shared-latent contrastive model** aligning compound-embedding spaces (and gene-embedding spaces in a v1.5).
3. **HF Spaces Gradio demo**: enter a compound or gene, get its cross-modal neighbors with concordance score.
4. **Multi-task probing** comparing modality-specific vs shared signal per drug class / target class.
5. **Arc Virtual Cell Challenge submission** if calendar aligns.
6. **Preprint or workshop submission** if v1 results justify it.

## Handoff

Next step: invoke the writing-plans skill to convert this spec into an ordered, milestone-by-milestone implementation plan, with one TaskCreate-style task per notebook deliverable plus the polish work.
