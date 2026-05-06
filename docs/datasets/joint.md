# Joint dataset picture

What the cellduet v0 cross-modal analysis actually has to work with, after pairing **Replogle K562 genome-wide CRISPRi Perturb-seq** with **Recursion rxrx3-core CRISPR-KO Cell Painting (Phenom embeddings)**. Companion to `tahoe-100m.md`, `replogle.md`, `rxrx3.md` in this directory. The two single-dataset dossiers cover origin, biology, and feasibility per modality; this file covers everything that depends on having both at once.

## Headline numbers

| Property | Replogle K562 GW (transcriptomic) | rxrx3-core (morphological) |
|---|---|---|
| Perturbation modality | CRISPRi knockdown (dCas9-KRAB) | CRISPR-Cas9 knockout |
| Cell context | K562 (BCR-ABL+ CML, suspension, TP53-mutant) | HUVEC (primary umbilical vein endothelial, adherent) |
| Perturbed genes (named) | 9,866 | 735 (+ `EMPTY_control`) |
| Pre-computed per-gene aggregate | Yes (Z-normalized pseudobulk h5ad, 375 MB) | No (per-well embeddings, must aggregate) |
| Embedding dimensionality | ~8,000 measured genes (LFC-like Z-scores) | 384 (OpenPhenom), 1024 (Phenom-1), 1664 (Phenom-2) |
| License | CC BY 4.0 (Figshare+) | Recursion bespoke EULA (CC-BY-SA-like, **neuroscience carve-out**) |
| Total v0 download | ~470 MB (bulk h5ad + RPE1 sanity check) | ~550 MB (OpenPhenom parquet + metadata) or ~2.3 GB (Phenom-2) |

**The expected named-gene intersection is approximately 600–720 genes**, i.e., 735 minus K562-non-expressed members of the rxrx3-core panel. This clears the 500-gene feasibility gate by a comfortable margin and is the operating sample size for the cross-modal correlation. The exact count is the first empirical computation in `notebooks/01_data_exploration.ipynb`.

## What the v0 question actually tests

With these two datasets paired, the cross-modal concordance question is **not** "do CRISPR perturbations of gene X look the same in both modalities?" Different cell types and different perturbation chemistries (knockdown vs knockout) make that test ill-posed. What the pairing *does* support is a **relative-phenotype** test: do two genes that look similar in K562 transcriptomic space also look similar in HUVEC morphological space?

The natural test statistic is therefore a Mantel correlation (or RV coefficient) between the two `n × n` gene-gene distance matrices on the overlapping gene set, where `n ≈ 600–720`. A positive correlation says the two modalities agree on which genes group together; a near-zero correlation says agreement does not survive the cell-type and perturbation-chemistry shift. Both outcomes are findings, not failures.

This framing also clarifies what counts as a per-gene "convergent" or "divergent" call: a gene is **agreeing** if its near-neighbor sets in the two modalities have a Jaccard overlap above what a permutation null predicts; it is **divergent** if its neighborhoods are uncorrelated or anticorrelated. The v0 writeup names cases on both ends.

## Disease anchor decision

The original brainstorm assumed neurodegeneration as the natural anchor (TARDBP, FUS, MAPT, SNCA, LRRK2, and friends). That option is closed for this dataset pair, for two reinforcing reasons:

1. **rxrx3-core has zero of the 18 neurodegeneration core genes** in its 735-named-gene panel (verified directly against the metadata CSV; see `rxrx3.md` Section 3).
2. **The Recursion EULA forbids neuroscience research** as a use case for the data and embeddings (Section 3 of the EULA shipped with rxrx3-core). Even if the genes were present, the contractual carve-out would block the writeup.

**The anchor is oncology**, by elimination. Coverage in the joint set:

| Driver | rxrx3-core | Replogle K562 GW (prior) | Joint |
|---|---|---|---|
| TP53 | yes | yes (mutant in K562, but expressed) | yes |
| BRAF | yes | likely yes | yes |
| EGFR | yes | likely yes | yes |
| PIK3CA | yes | likely yes | yes |
| KRAS | no | likely yes | rxrx3-blocked |
| MYC | no | likely yes | rxrx3-blocked |
| PTEN | no | likely yes | rxrx3-blocked |
| RB1 | no | likely yes | rxrx3-blocked |
| CDKN2A | no | possibly deleted in K562 | both-blocked |

Four drivers (TP53, BRAF, EGFR, PIK3CA) are confirmed in rxrx3-core and almost certainly present in Replogle K562 GW. Empirical confirmation goes in notebook 01 by intersecting with the loaded `K562_gwps_normalized_bulk_01.h5ad` `.obs` perturbation list. **One worked oncology vignette is the v0 disease-anchored example**, with TP53 the most likely focal gene given how thoroughly characterized it is in K562 (mutant-loss-of-function baseline state, multiple known transcriptional and morphological consequences).

Cardiac (1/5 in rxrx3-core: SCN5A) and metabolic (1/6 in rxrx3-core: INSR) anchors are too thin to support a vignette and are dropped from v0 scope.

## Symbol harmonization plan

- **rxrx3-core** uses HGNC-style symbols (verified: TP53, EGFR, BRAF, PIK3CA, INSR all present as such).
- **Replogle h5ad** uses Ensembl gene IDs in `var_names` with HGNC symbols typically in `var['gene_symbol']` or analogous; the `.obs.gene` (perturbed gene) field is HGNC.

Plan: left-join on HGNC symbol, fall back to Ensembl-ID lookup via `mygene.info` (or a static GTF-derived mapping pinned to GRCh38 / GENCODE 44 for reproducibility). Pre-flight check in notebook 01: count unmapped symbols in each direction and inspect the unmapped list for systematic causes (recently-renamed FAM-family genes, pseudogenes, alias mismatches).

## License joint

The artifact pair has heterogeneous licenses; this matters for what cellduet can publish.

- **Replogle processed h5ad: CC BY 4.0** (Figshare+). Permissive for portfolio publication, attribution required.
- **Recursion rxrx3-core: bespoke EULA**. Recursion describes it as "CC BY-SA-like" but the actual file shipped on Hugging Face has hard carve-outs: no neuroscience research, no target validation as a commercial program, no use for AI-model training in the neuroscience field. Attribution and share-alike are still required for derivative works.

What this means concretely for cellduet:

- The repo and writeup can publish derivative analyses, figures, and per-gene aggregated embeddings under a permissive license **as long as** the writeup does not frame the work as neuroscience research and does not claim target validation.
- The oncology anchor is on-policy.
- Any v1 plan to fine-tune a model "trained on rxrx3-core for neurological disease prediction" is contractually disallowed and must not appear in the writeup, even as a stretch.
- HF dataset names should not contain "neuroscience" branding.

## Joint compute plan

Both files are small enough that the v0 cross-modal pipeline fits comfortably in one Colab Free session:

1. **Download once, cache to Drive.** `K562_gwps_normalized_bulk_01.h5ad` (375 MB) + `rpe1_normalized_bulk_01.h5ad` (95 MB, sanity check) + `OpenPhenom_rxrx3_core_embeddings.parquet` (532 MB) + `metadata_rxrx3_core.csv` (~20 MB). Total ~1 GB. Easily fits in 15 GB Drive.
2. **Per-modality per-gene aggregation.** Replogle: row-mean Z-scores within each perturbation across `gemgroup`. Output: 9,866 × ~8,000 (perturbed × measured) at float32 ≈ 315 MB. RxRx3: `EFAAR_benchmarking`-style TVN on EMPTY_control wells, then per-gene mean across replicate wells. Output: 735 × 384 ≈ 1.1 MB.
3. **Symbol harmonization + intersection.** Reduces to ≈600–720 genes on both sides.
4. **Per-modality pairwise distance matrices.** ~720 × 720 cosine. <1 MB each.
5. **Cross-modal Mantel + RV-coefficient + per-gene neighborhood Jaccard.** Trivial compute.
6. **Persist.** Push the joint per-gene embeddings + distance matrices to a Hugging Face dataset (`patrickjreed/cellduet-joint-pergene` or similar). Total artifact ~50 MB.

Bottom line: the entire v0 numerical pipeline fits in one ~3-hour Colab Free session, well under the 12-hour ceiling, with no model inference required. Switching the morphology side to Phenom-1 (1024-d) or Phenom-2 (1664-d) is a parquet swap with no other changes.

## Joint risks

In rough order of how badly each can compromise v0:

1. **Cell-type mismatch (K562 leukemia × HUVEC endothelial) is the dominant biological caveat.** A weak Mantel correlation may reflect cell-type-bound biology rather than modality difference. The writeup must frame the test honestly: this is a *gene-intrinsic perturbation phenotype* test, asking which gene effects survive the cell-type shift, not a clean same-context comparison. A permutation null built from gene-set-stratified shuffles helps, but the caveat is structural, not statistical.
2. **CRISPRi knockdown vs CRISPR knockout chemistry.** Replogle is partial knockdown (median KD efficiency 85.5% in K562); RxRx3 is null-allele knockout. For genes with strong dose-dependence or haploinsufficiency, the two perturbations can produce qualitatively different phenotypes. Less severe than (1) but real.
3. **Per-gene aggregation noise on the morphology side.** rxrx3-core has variable per-gene replicate counts; some genes may have 1–2 wells after curation. Mean-aggregation noise inflates cross-modal disagreement. Notebook 01 must report a per-gene replicate count histogram and either weight or drop low-count genes.
4. **TVN / PCA-CS sufficiency.** The released Phenom embeddings are PCA-CenterScale aligned, but residual plate effects can inflate within-plate gene-gene similarity. A second-pass plate-residual regression on per-well embeddings before averaging is a hedge. If unresolved, plate structure can leak into the morphology distance matrix and create false agreement.
5. **Symbol harmonization gotchas.** Recently-renamed FAM-family genes, sex-chromosome paralogs, pseudogene aliases. Manageable, but worth a careful first pass.
6. **License heterogeneity in derivatives.** Mixing CC BY 4.0 (Replogle) and the Recursion EULA (rxrx3-core) in one published artifact requires careful per-file licensing notes in the HF dataset README. Not a blocker, but a documentation chore.
7. **Effect-size detectability on the Replogle side.** Per Nadig 2024/2025, only ~36% of K562 GW perturbations show FDR-significant transcriptome-wide effects. cellduet uses Z-scored vectors directly (not significance-thresholded), so this is mitigated, but for genes with very small true effects the embedding is dominated by noise and contributes nothing to the correlation.

## Joint open questions for notebook 01

- Exact gene-set overlap after symbol harmonization. Estimate 600–720; verify.
- Per-gene replicate-count distribution in rxrx3-core for the overlap gene set.
- Are the four oncology drivers (TP53, BRAF, EGFR, PIK3CA) all present in `K562_gwps_normalized_bulk_01.h5ad` `.obs`?
- Does the per-modality variance structure (e.g., effective rank of the gene-gene distance matrix) suggest enough signal-to-noise for a Mantel test to have power, or does one modality dominate?
- Does cross-screen Replogle agreement (K562_gwps × RPE1 essential) on shared genes correlate with cross-modal Replogle × rxrx3-core agreement on the same genes? If the two transcriptomic screens disagree on a gene, expecting cross-modal agreement is unreasonable.
- Sensitivity of the cross-modal correlation to embedding choice (OpenPhenom-384 vs Phenom-1-1024 vs Phenom-2-1664). One ablation table.

## Summary verdict

The Replogle K562 GW × rxrx3-core pairing is **feasible, ethical (within EULA), and Colab-Free-tractable**. The 600–720-gene overlap clears the v0 feasibility gate. Oncology is the disease anchor; neurodegeneration is closed for this dataset pair. The cell-type mismatch is the single biggest caveat for biological interpretation and must be named openly in the writeup. Tahoe-100M moves to v1 as the drug-target-inference extension once v0 ships.
