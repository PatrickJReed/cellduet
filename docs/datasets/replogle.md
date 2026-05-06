# Replogle Perturb-seq dossier

A primary-source rundown of the Replogle et al. 2022 genome-scale Perturb-seq atlas, written to evaluate it as the v0 transcriptomic partner for Recursion RxRx3 / Phenom in cellduet. The dossier replaces Tahoe-100M's role on the transcriptomic side, because Tahoe is a small-molecule atlas and Replogle is a true CRISPR screen with single-gene perturbations and non-targeting-control sgRNAs as the matched baseline.

**Project-level finding up front.** Replogle is a clean fit for the v0 cross-modal comparison against RxRx3 (CRISPR-KO Cell Painting). The perturbation modality matches (CRISPRi knockdown vs CRISPR-KO; both are loss-of-function), the published per-gene Z-normalized pseudobulk files are small enough for Colab Free tier (a few hundred MB each), and the license on the processed data is CC BY 4.0 with no auth wall. The biggest live risk is biological: K562 is a BCR-ABL+ leukemia line and RPE1 is an epithelial line, so neurodegeneration genes (MAPT, SNCA, APP, LRRK2, PSEN1/2) and most cardiac genes are unlikely to clear the cell-type expression filter that defines what was perturbed. The 9,866-gene K562 genome-wide screen is the only sub-screen that gets close to "all expressed genes," and even there, lineage-restricted disease genes are out by construction. Section 9 has the explicit recommendation.

## Origin and citation

Replogle, Joseph M.; Saunders, Reuben A.; Pogson, Angela N.; Hussmann, Jeffrey A.; Lenail, Alexander; Guna, Alina; Mascibroda, Lauren; Wagner, Eric J.; Adelman, Karen; Lithwick-Yanai, Gila; Iremadze, Nika; Oberstrass, Florian; Lipson, Doron; Bonnar, Jessica L.; Jost, Marco; Norman, Thomas M.; Weissman, Jonathan S. *"Mapping information-rich genotype-phenotype landscapes with genome-scale Perturb-seq."* **Cell** 185(14):2559–2575.e28, 7 July 2022. DOI [10.1016/j.cell.2022.05.013](https://doi.org/10.1016/j.cell.2022.05.013) ([PMC9380471](https://pmc.ncbi.nlm.nih.gov/articles/PMC9380471/), [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0092867422005979)). Earlier preprint at bioRxiv 2021.12.16.473013.

**Canonical hosting.** The processed h5ad files live at Figshare+ DOI [10.25452/figshare.plus.20029387](https://doi.org/10.25452/figshare.plus.20029387) (license **CC BY 4.0**, total size 171.5 GB across 12 files). The cellranger MTX outputs are at [10.25452/figshare.plus.20127869](https://doi.org/10.25452/figshare.plus.20127869) (CC BY 4.0, 104 GB). Commonly requested supplemental tables (Anderson-Darling DE p-values, embedding coordinates, clustered mean expression) are at [10.25452/figshare.plus.21632564](https://doi.org/10.25452/figshare.plus.21632564) (license **CC0**). Raw fastq is on SRA under [BioProject PRJNA831566](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA831566). An interactive browser is at [gwps.wi.mit.edu](https://gwps.wi.mit.edu/) (loads via JS; the underlying data is the Figshare release). The K562-Essential subset is also mirrored on the [CZI Virtual Cells Platform](https://virtualcellmodels.cziscience.com/dataset/k562-essential-perturb-seq) under CC BY-NC-SA 4.0 (more restrictive than the Figshare original).

**Subsequent extensions.** Nadig, Replogle et al., *"Transcriptome-wide analysis of differential expression in perturbation atlases,"* **Nature Genetics** 2025, DOI [10.1038/s41588-025-02169-3](https://www.nature.com/articles/s41588-025-02169-3) (preprint [bioRxiv 2024.07.03.601903](https://www.biorxiv.org/content/10.1101/2024.07.03.601903v1)) introduces the TRADE statistical framework for noise-corrected transcriptome-wide effect size estimation and re-analyzes the original Replogle data; new sequencing runs are deposited at [GEO GSE264667](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE264667) under [BioProject PRJNA1100571](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1100571) ([Nadig et al., PMC11244993](https://pmc.ncbi.nlm.nih.gov/articles/PMC11244993/)). Nadig **complements** rather than supersedes Replogle 2022: the underlying screens are still the 2022 atlas, and TRADE's contribution is statistical post-processing (a noise-corrected effect size estimator that recovers more signal than per-gene FDR filtering, with the headline that 36% of K562-genome-wide transcriptome-wide impact is captured by FDR-significant calls). The "Replogle-Nadig" combined release is also one of the three training corpora cited for [Arc Institute's STATE model](https://arcinstitute.org/news/virtual-cell-model-state).

## Biological scope

Three sub-datasets in the original 2022 release. CRISPRi only (no CRISPRa, no KO). All loss-of-function via dCas9-KRAB transcriptional repression. Library is **multiplexed dual-sgRNA** (two distinct sgRNAs per gene packaged into a single lentiviral vector), with non-targeting control sgRNAs accounting for **~5% of the library** ([PMC9380471](https://pmc.ncbi.nlm.nih.gov/articles/PMC9380471/)). 10x Genomics droplet-based 3' scRNA-seq with direct sgRNA capture for perturbation calling.

| Sub-screen | Cell line | Day | Perturbed genes | Total cells | Median cells/perturbation | Median KD efficiency |
|---|---|---|---|---|---|---|
| K562 genome-wide (`K562_gwps`) | K562, dCas9-KRAB | 8 | **9,866** (all expressed genes) | ~2.5M (across all three screens) | >100 | 85.5% (K562) |
| K562 essential (`K562_essential`) | K562, dCas9-KRAB | 6 | **2,057** (common essentials) | included in 2.5M | >100 | 85.5% (K562) |
| RPE1 essential (`rpe1`) | RPE1, dCas9-ZIM3-KRAB | 7 | **2,393** (common essentials) | ~247,914 | >100 | 91.6% (RPE1) |

Sources: [Cell 2022 abstract / methods via PMC9380471](https://pmc.ncbi.nlm.nih.gov/articles/PMC9380471/), [Replogle Twitter thread for KD efficiency](https://x.com/josephmreplogle/status/1472244456917196814).

**K562** is a chronic myeloid leukemia (CML) line, BCR-ABL fusion positive, CML blast crisis. Highly aneuploid and one of the three tier-1 ENCODE lines ([PMC6396411](https://pmc.ncbi.nlm.nih.gov/articles/PMC6396411/)). **RPE1** (specifically hTERT-RPE1) is a karyotype-stable but hTERT-immortalized retinal pigment epithelial line; the Replogle version was further engineered with dCas9-ZIM3-KRAB, which gives stronger CRISPRi repression than the older dCas9-KRAB used in K562 ([eLife 2023, dual-sgRNA optimization paper](https://elifesciences.org/articles/81856)).

The K562 genome-wide arm targets "all expressed genes" defined by an internal expression filter, which is why 9,866 (not ~20,000) genes are screened. The two essential arms target the intersection of the genome-wide list with a common-essential gene set defined from previous DepMap-style fitness screens. Replicate structure is gemgroup-level rather than biological-replicate-level; the `gemgroup` field in `.obs` is the variance unit used for the Z-normalization in the published bulk files.

NTC structure: ~5% of the dual-sgRNA library is non-targeting, providing a within-experiment matched baseline for differential expression. This is exactly the control structure the v0 cross-modal comparison wants: a perturbed-vs-NTC contrast on the same plate, analogous to how RxRx3 has matched untreated wells for each gene.

## Disease-gene coverage

Genes are now directly perturbable since Replogle is a CRISPR screen, not a drug atlas. The right question is *which sub-screen contains each gene*, and the deciding filter is whether the gene was expressed in K562 or RPE1 above the screen's expression threshold. Without downloading the per-screen `.var` (or the published library annotation table), I cannot return a definitive yes/no for each gene. What I *can* return is well-grounded priors based on cell-line lineage. Treat the verdicts below as priors that should be refuted or confirmed by intersecting the loaded `K562_gwps` `.obs.gene` (or `.var.feature_id`) list with each disease gene set in `notebooks/01_data_exploration.ipynb`.

**Neurodegeneration core (TARDBP, FUS, C9orf72, GRN, MAPT, SNCA, LRRK2, APP, PSEN1, PSEN2, SOD1, HTT, ATXN1, ATXN2, ATXN3, PARK7/DJ-1, PINK1, PRKN).** Mostly **NO** in any sub-screen, mostly because of cell-line lineage. K562 (myeloid leukemia) and RPE1 (epithelial) are neither neuronal nor brain-derived; lineage-restricted genes (MAPT/Tau is neuron-restricted; SNCA is enriched in neurons; APP is broadly expressed including K562; LRRK2 is broadly low; HTT is broadly expressed; PSEN1/2 are broadly expressed) will mostly fall below the K562 expression filter that defined the 9,866-gene set. Some housekeeping-like neurodegeneration genes (SOD1, TARDBP, FUS, GRN, PARK7/DJ-1, PINK1, PRKN, ATXN1/2/3, HTT, APP) are likely **partially covered** in the K562 genome-wide screen because they are ubiquitously expressed. **MAPT, SNCA, LRRK2, PSEN1, PSEN2, C9orf72** are the most likely to be missing. Empirical confirmation needed; this is the single biggest open question for any neurodegeneration-flavored framing of the project.

**Common oncology drivers (TP53, KRAS, BRAF, EGFR, MYC, PIK3CA, PTEN, RB1, CDKN2A).** Mostly **YES** in K562 genome-wide, possibly some in K562 essential. K562 is a cancer line carrying loss-of-function or altered states for several of these (it is TP53-mutant, BCR-ABL+, with whole-genome characterizations available at [PMC6396411](https://pmc.ncbi.nlm.nih.gov/articles/PMC6396411/)). MYC, KRAS, PTEN, PIK3CA, EGFR are broadly expressed; TP53 expression in K562 is mutant but present; RB1, CDKN2A may be deleted or silenced (CDKN2A is famously deleted in many cancer lines). Anything not silenced in K562 is in the 9,866-gene list. Verdict: **expect the majority of this set to be perturbed in K562 genome-wide**; CDKN2A is the most likely miss because of K562-specific deletion status.

**Cardiac (MYH7, TTN, LMNA, KCNQ1, SCN5A).** Mostly **NO**. MYH7 (cardiac muscle myosin), TTN (titin, sarcomere), KCNQ1 (cardiac K+ channel), SCN5A (cardiac Na+ channel) are tissue-restricted to cardiomyocytes and not expressed in K562 or RPE1, so they will not be in the screened gene list. **LMNA** (lamin A/C) is broadly expressed and is the only likely **YES** in this set.

**Metabolic (INSR, LEP, LEPR, MC4R, PCSK9, LDLR).** Mixed. INSR is broadly expressed (likely yes). LDLR is broadly expressed (likely yes). PCSK9 is liver-restricted (likely no). LEP, LEPR, MC4R are adipose / hypothalamus-restricted (no in K562/RPE1).

**Practical implication for v0.** The gene-overlap denominator with RxRx3 must be computed against the actual `.var` of K562_gwps, not against the union of all human genes. Do not pre-commit to a neurodegeneration framing. Oncology-driver overlap is the cleanest story Replogle K562 can tell.

## Distribution and access

**Primary host: Figshare+** (the paid Figshare research data tier; free downloads, no auth wall, just `curl` against `ndownloader.figshare.com`). License **CC BY 4.0**. Total release across the three Figshare entries is ~276 GB, but for v0 only a small slice is needed (see Section 5).

The processed AnnData release at [DOI 10.25452/figshare.plus.20029387](https://doi.org/10.25452/figshare.plus.20029387) ships **four h5ad files per sub-screen**:
- `${pop}_raw_singlecell_01.h5ad`, single-cell raw counts, genes filtered to `>0.01 UMI/cell`.
- `${pop}_raw_bulk_01.h5ad`, pseudobulk raw counts (one row per perturbation × gemgroup or similar aggregation).
- `${pop}_normalized_singlecell_01.h5ad`, gemgroup Z-normalized single-cell expression.
- `${pop}_normalized_bulk_01.h5ad`, gemgroup Z-normalized pseudobulk expression. **This is the v0 turnkey product.**

File sizes from the Figshare API (`api.figshare.com/v2/articles/20029387`):

| File | Size |
|---|---|
| `K562_essential_normalized_bulk_01.h5ad` | 79.8 MB |
| `K562_essential_raw_bulk_01.h5ad` | 79.8 MB |
| `K562_essential_normalized_singlecell_01.h5ad` | 10.66 GB |
| `K562_essential_raw_singlecell_01.h5ad` | 10.66 GB |
| `K562_gwps_normalized_bulk_01.h5ad` | 374.6 MB |
| `K562_gwps_raw_bulk_01.h5ad` | 374.6 MB |
| `K562_gwps_normalized_singlecell_01.h5ad` | **65.83 GB** |
| `K562_gwps_raw_singlecell_01.h5ad` | **65.83 GB** |
| `rpe1_normalized_bulk_01.h5ad` | 95.4 MB |
| `rpe1_raw_bulk_01.h5ad` | 95.4 MB |
| `rpe1_normalized_singlecell_01.h5ad` | 8.70 GB |
| `rpe1_raw_singlecell_01.h5ad` | 8.70 GB |

Streaming friendliness: h5ad over HTTPS works fine on Colab via `urllib`/`requests` to local SSD. The bulk files fit in RAM trivially. The K562 essential and RPE1 single-cell files are downloadable to Drive (10 GB and 9 GB respectively, well under the 15 GB Drive quota, but they fill it). **K562 genome-wide single-cell at 65.8 GB will not fit on Colab Free**, full stop, in either RAM or Drive; use the bulk file instead.

Secondary mirrors: [scPerturb](http://projects.sanderlab.org/scperturb/) provides harmonized h5ad files; [Zenodo](https://zenodo.org/records/10044268) hosts the scPerturb release; the [pertpy](https://pertpy.readthedocs.io/en/stable/api/data/pertpy.data.replogle_2022_k562_gwps.html) Python package wraps the download. The CZI [Virtual Cells Platform K562-Essential mirror](https://virtualcellmodels.cziscience.com/dataset/k562-essential-perturb-seq) carries a more restrictive **CC BY-NC-SA 4.0** license; use the original Figshare CC BY 4.0 for portfolio publication safety.

## Pre-computed artifacts

**Pseudobulk effect-size vectors per perturbed gene: YES, native to the release.** The `${pop}_normalized_bulk_01.h5ad` files are exactly the turnkey product cellduet wants. Per the Figshare description, these contain "gemgroup Z-normalized pseudo-bulk expression data," which is the standard Perturb-seq formulation: each perturbation × gemgroup is one observation row, expression values are Z-scored relative to non-targeting controls in the same gemgroup, and the .X matrix is therefore an effect-size-like quantity in units of NTC standard deviations. The K562 GW bulk file is 374.6 MB (well under Colab RAM). The K562 essential and RPE1 bulk files are 80 and 95 MB respectively.

The exact `.obs` schema (whether each row is one (gene, gemgroup) pair, one (sgRNA, gemgroup) pair, or one gene aggregated across gemgroups) is not documented on the Figshare card and is best confirmed by loading and inspecting `.obs.columns` and `.obs.shape[0]`. The [scverse discourse thread](https://discourse.scverse.org/t/obs-perturbation-and-obs-gene-in-replogle-dataset/3933) flags some upstream metadata edge cases (NaN perturbation calls, complex perturbation strings); expect a brief data-cleaning pass.

**Anderson-Darling DE p-values** are released separately at [10.25452/figshare.plus.21632564](https://doi.org/10.25452/figshare.plus.21632564) under CC0, ~488 MB compressed. This is a perturbation × gene table of differential expression p-values, which is an alternative starting point if Z-normalized log fold-change is not the desired feature.

**Foundation-model embeddings.**
- **Arc Institute STATE** ([github.com/ArcInstitute/state](https://github.com/ArcInstitute/state)). Two interlocking modules, SE (State Embedding, ~600M params, [arcinstitute/SE-600M](https://huggingface.co/arcinstitute/SE-600M) on HuggingFace) and ST (State Transition, e.g. [arcinstitute/ST-Tahoe](https://huggingface.co/arcinstitute/ST-Tahoe), [arcinstitute/ST-Parse](https://huggingface.co/arcinstitute/ST-Parse)). Replogle-Nadig is one of the three training corpora cited in the [STATE announcement](https://arcinstitute.org/news/virtual-cell-model-state) (Tahoe-100M, Parse-PBMC, Replogle-Nadig). Code is CC BY-NC-SA 4.0; **model weights and outputs are under the Arc Research Institute State Model Non-Commercial License** with a separate Acceptable Use Policy. The non-commercial restriction is a downstream license blocker for any commercial republication of derived embeddings, but for a portfolio research artifact published under a non-commercial framing it is acceptable. Pre-computed per-gene embeddings for Replogle perturbations are not advertised as a separate downloadable artifact; using STATE means running inference, which is feasible on a T4 only for the ST module, not the SE-600M model. **Verdict for v0: STATE is overkill; the native pseudobulk file is sufficient.**
- **scGPT** ([github.com/bowang-lab/scGPT](https://github.com/bowang-lab/scGPT)). Trained across 33M cells. Gene-level embeddings can be extracted ([issue #132](https://github.com/bowang-lab/scGPT/issues/132)). No published per-gene Replogle-conditioned embedding hub release; would require running scGPT inference. T4-feasible but adds engineering scope.
- **Geneformer**, **UCE**, **scFoundation**, **SCimilarity** all train on observational atlases (CellxGene-style) without perturbation conditioning. Their gene-level embeddings encode "what is gene X" but not "what does perturbing gene X do," so they are the wrong product for a perturbation-phenotype concordance analysis. Skip.
- **GenePert** ([github.com/zou-group/GenePert](https://github.com/zou-group/GenePert)) wraps Geneformer and scGPT embeddings for perturbation prediction; it is a pipeline, not a pre-computed artifact, and not a useful drop-in.

**Recommendation: use the native `${pop}_normalized_bulk_01.h5ad` files.** They are the authors' own published per-gene effect-size product, the smallest artifacts (sub-GB), and the cleanest license (CC BY 4.0). Foundation-model embeddings add scope without obvious payoff for a pairwise gene-distance comparison.

## Compute footprint for v0

Colab Free constraints: T4 with ~15 GB VRAM, ~12 GB system RAM, ~15 GB persistent Drive, ~12-hr session, ~90-min idle disconnect.

**Per-gene aggregation tractability per sub-screen, using the bulk h5ad as the starting point:**

- **K562 essential (80 MB).** Trivially loads into RAM. Per-gene aggregation (mean Z-score across gemgroups for each perturbation) is a few seconds of pandas/numpy work. Output: a 2,057 × ~8,000-genes matrix at float32 ≈ 65 MB.
- **RPE1 essential (95 MB).** Same story. Output: 2,393 × ~8,000-genes matrix ≈ 76 MB.
- **K562 genome-wide (375 MB).** Loads into RAM with margin. Output: 9,866 × ~8,000-genes matrix at float32 ≈ 315 MB. Still comfortable.

**The realistic memory bottleneck is not the bulk file; it is anything that returns to single-cell.** If single-cell loading is required (e.g., to recompute pseudobulk with a different aggregation rule, or to inspect cell-level distributions), only the K562 essential (10.66 GB) and RPE1 (8.70 GB) single-cell files fit on Drive, and even those approach RAM limits when fully loaded as dense arrays. The K562 GW single-cell file (65.83 GB) is out of reach on Colab Free; would require either a Colab Pro+ session, Vertex AI, or chunked HDF5 reads from a local mount.

**Recommended aggregation strategy for v0.** Skip the single-cell files. Pull `K562_gwps_normalized_bulk_01.h5ad` (375 MB) from Figshare, mean-aggregate Z-scores across `gemgroup` (or whatever the replicate field turns out to be) to get one effect-size vector per perturbed gene, restrict the gene-axis (the .var, the *measured* genes) to the intersection with RxRx3's gene set, then compute the gene × gene cosine distance matrix. This is the cleanest, smallest-data path. Repeat in parallel with the RPE1 file (95 MB) as a cross-cell-line sanity check.

Persistence: the resulting per-gene embedding (~9,866 × 1,000 measured-gene-features at float32 ≈ 40 MB) is small enough to push to a HuggingFace dataset (`patrickjreed/cellduet-replogle-pergene` or similar) without size concerns.

## Known caveats

- **Cell-line confound.** K562 is BCR-ABL+ CML blast crisis, highly aneuploid, TP53-mutant, with substantial copy number changes ([PMC6396411](https://pmc.ncbi.nlm.nih.gov/articles/PMC6396411/)). Many oncology drivers will show baseline-state effects that complicate effect-size interpretation. RPE1 is karyotypically more stable but hTERT-immortalized and not "primary." Neither line resembles the cell types used in RxRx3 (HUVEC, Cell Painting on epithelial / fibroblast contexts), so any gene-pair distance match across modalities reflects a *gene-intrinsic* perturbation phenotype that survives across both contexts; this is a feature for portfolio framing but a caveat to state honestly.

- **CRISPRi knockdown variability.** Median KD is 85.5% (K562) and 91.6% (RPE1), but this is a median; some genes are poorly knocked down (notably genes with short or atypical 5' UTRs, lowly-expressed genes, or genes with poor sgRNA design at the TSS). The [poor-KD repo from the Weissman lab summer project](https://github.com/vyinkabanjo/CRISPRi_poorKD_genes) catalogs which genes have poor coverage. For genes near the bottom of the KD distribution, the perturbation phenotype is biologically attenuated and apparent "no effect" can be a false negative.

- **Effect-size detectability.** The original paper reported that only ~41% of perturbations show statistically significant transcriptome-wide effects under standard FDR analysis, and Nadig 2024/2025 (TRADE) reanalysis recovers that **only 36% of true K562-genome-wide transcriptome-wide impact is captured by FDR-significant calls** ([PMC11244993](https://pmc.ncbi.nlm.nih.gov/articles/PMC11244993/)). For v0, this means using Z-scored pseudobulk vectors directly (not significance-thresholded calls) is preferable: small effects are in the embedding even when they fail FDR.

- **Batch / gemgroup structure.** The Z-normalization is gemgroup-aware, so most large-batch confounding is already corrected. Residual batch effect across gemgroups within a sub-screen is the most likely remaining structure; check by computing perturbation-vs-NTC distance distributions per gemgroup before pooling.

- **K562 GW screened gene set is not "all human genes."** It is "all genes expressed in K562 above the screen's threshold," which is 9,866 genes. The `.var` of the K562 GW bulk file is the *measured* gene axis (similarly subsetted). RxRx3's gene set must be intersected with both axes.

- **Perturbation calling NaNs.** Some cells lack confident sgRNA assignment ([scverse discourse](https://discourse.scverse.org/t/obs-perturbation-and-obs-gene-in-replogle-dataset/3933) reports 1,527 NaN perturbation rows in one of the released subsets). Drop these in preprocessing.

- **Off-target and adjacent-gene effects.** CRISPRi at the TSS can affect bidirectional promoters and nearby genes. Replogle 2022 includes guide-level QC; the published library is the dual-sgRNA optimized version from [eLife 2023](https://elifesciences.org/articles/81856), so off-target rates are characterized but not zero.

## Open questions

- **Does the K562_gwps `.var` (measured gene axis) cover the genes RxRx3 perturbs?** This is the v0 feasibility-gate computation. Empirical: load `K562_gwps_normalized_bulk_01.h5ad`, take `adata.var_names`, intersect with the RxRx3 gene set; the count must clear ~500 to keep the project alive.
- **Does the K562_gwps `.obs` (perturbed gene axis) cover the genes RxRx3 perturbs?** Separate question, also empirical. The intersection of *perturbed* genes (rows) and *measured* genes (columns) bounds what's actually comparable.
- **Exact `.obs` row structure of the bulk files.** Is each row one (gene, gemgroup), one (sgRNA, gemgroup), or already aggregated to one row per gene? This determines whether v0 needs a second aggregation step.
- **NTC / control structure in the bulk file.** Are NTC rows already removed, kept in for the user to drop, or used as the Z-normalization reference (in which case they have effect size ~0 by construction)? Empirical.
- **Disease-gene coverage vs the K562 expression filter.** The Section 3 verdicts are priors; only inspecting `K562_gwps_normalized_bulk_01.h5ad`'s gene lists confirms which neurodegeneration / oncology / cardiac / metabolic genes survived. This is a 30-line notebook cell.
- **RPE1 vs K562 cross-screen reproducibility.** For genes in both essential screens, do their effect-size vectors agree? The cross-screen correlation is itself a methodological probe and a bonus figure for the writeup.
- **Match to the RxRx3 cell-line context.** RxRx3 morphology was generated in a different cellular context than K562 / RPE1; the cross-modality agreement figure is therefore a *gene-intrinsic-vs-context-specific* test, not a same-cell-type test. Frame this honestly.

## Recommendation

**Use Replogle K562 genome-wide (`K562_gwps`) as the primary v0 transcriptomic partner for RxRx3, with RPE1 essential as a cross-cell-line sanity check.**

Strongest single reason: the **9,866 perturbed genes in K562_gwps is the only published per-gene Perturb-seq aggregate large enough to clear the 500-gene overlap gate against RxRx3, ships pre-computed pseudobulk Z-normalized effect-size vectors at 375 MB (Colab-tractable), and lives under CC BY 4.0**. No alternative comes close on all three axes simultaneously:

- **K562 essential and RPE1 essential** (2,057 and 2,393 genes respectively) might still clear 500 overlap depending on RxRx3's gene list, but they target only common-essential genes, which is a biased and narrow biological denominator.
- **Frangieh 2021** ([Nat Genet 53:332-341](https://www.nature.com/articles/s41588-021-00779-1)) targets only ~248 immune-resistance genes, below the feasibility gate.
- **Norman 2019** is combinatorial (gene-pair) rather than single-gene; the cross-modal alignment story is harder to tell with combinations.
- **Adamson 2016** is ~80 genes (UPR), far below the gate.
- **Arc Virtual Cell Challenge perturbation training set** (primarily H1 hESC) is a different cell type and modality, but the H1 hESC context is even further from RxRx3 than K562 is. It is also less mature as a community benchmark and the per-gene aggregate format is less standardized. Worth a fast secondary check during v0 exploration but not the primary.
- **Replogle-Nadig (TRADE-reanalyzed)** is the same screens with a better statistical post-processing layer; useful as a v1 enhancement but not necessary for v0.

The recommended file to pull first: [`K562_gwps_normalized_bulk_01.h5ad`](https://ndownloader.figshare.com/files/35773217) (374.6 MB, CC BY 4.0). Drop into `notebooks/01_data_exploration.ipynb` and run the gene-overlap intersection against RxRx3 immediately. If the overlap clears 500, v0 is feasible. If it doesn't, fall back to combining K562_gwps with RPE1 essential (different `.obs` perturbed-gene sets, identical or near-identical `.var` measured-gene sets) before recommending a switch off Replogle.
