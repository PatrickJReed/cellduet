# Scan B2: same-cell-line Perturb-seq + imaging pairings

A narrow feasibility scan, not a full dossier. Decision question: does a publicly-available Perturb-seq + imaging dataset pair sharing a cell line exist with **joint coverage ≥ 500 perturbed genes**, and is it Colab-Free-tractable? If yes, promote to full dossier; if no, stick with the cross-cell-line pairing in scan_b1 (Replogle K562 + RxRx3 HUVEC) or pivot.

The scan was time-boxed to ~45 minutes of search + primary-source page reads.

## Headline

The candidate that clears the gate cleanly is **PERISCOPE-A549 (Cell Painting, 20,393 genes) + a future A549 Perturb-seq, of which no public genome-scale release exists today**. The candidate that almost clears the gate from existing-data alone is **JUMP-CP-U2OS (Cell Painting, 7,975 CRISPR-KO genes) + Replogle's K562 GW (cross-cell)**, which is exactly the cross-cell pairing already used by [Celik et al. PLOS Comp Bio 2024](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1012463) and is **not** same-cell. The two same-cell candidates that *do* exist (Perturb-Multi mouse liver tissue; Labitigan U2OS optical pooled CRISPRi at 366 genes) both miss the 500-gene gate, the first by being mouse + tissue and the second by being below scale.

**Bottom line: no genome-scale same-cell Perturb-seq + imaging pair exists in the public domain as of May 2026.** The cleanest path forward is to keep the B1 cross-cell pairing (Replogle K562 + RxRx3 HUVEC) and frame the v0 result as a *gene-intrinsic* concordance test, OR pivot to cross-modal *within Cell Painting only* (PERISCOPE A549 vs JUMP-CP U2OS) which is two morphology screens, not the project's stated multimodal scope.

## Candidates evaluated

### 1. JUMP-CP CRISPR-KO arm (cpg0016-jump)

- **Cell line on the imaging side**: U2OS (osteosarcoma) only ([Chandrasekaran et al. bioRxiv 2023](https://www.biorxiv.org/content/10.1101/2023.03.23.534023v2.full); the [JUMP-CP results page](https://jump-cellpainting.broadinstitute.org/results) confirms U2OS is the single CRISPR-KO line; A549 was used only for pilot cpg0000 comparison). HUVEC is **not** in JUMP-CP.
- **CRISPR-KO gene count**: 7,975 unique genes, 4 sgRNAs/gene pool ([Chandrasekaran et al.](https://www.biorxiv.org/content/10.1101/2023.03.23.534023v2.full); [JUMP-CP press](https://jump-cellpainting.broadinstitute.org/news/data-release-manuscript-biorxiv)).
- **Perturb-seq counterpart in U2OS**: not found in this scan. No genome-scale U2OS Perturb-seq is published as a primary dataset; PerturBase indexes 19 cell lines covering THP1, K562, RPE1, HepG2, MCF10A but not U2OS at scale ([PerturBase, NAR 2025](https://academic.oup.com/nar/article/53/D1/D1099/7815638)).
- **Hosting / license**: Cell Painting Gallery on AWS S3, accession [cpg0016-jump](https://broadinstitute.github.io/cellpainting-gallery/), CC0; total >250 TB, but pre-computed gene-level Cell Profiler profiles are sub-GB.
- **Colab footprint**: gene-level profile parquets are tractable; raw images are not.
- **Verdict on ≥ 500-gene same-cell gate**: **NO same-cell pairing**. JUMP-CP-U2OS is a candidate *morphology partner*, but the matching transcriptomic side does not exist publicly in U2OS. Crossing JUMP-CP-U2OS with Replogle K562 GW would be a different cross-cell pairing than B1, not a same-cell rescue.

### 2. PERISCOPE (cpg0021-periscope)

- **Cell line on the imaging side**: A549 (lung) genome-wide; HeLa (cervical) genome-wide in two media conditions ([Ramezani et al. Nature Methods 2025](https://www.nature.com/articles/s41592-024-02537-7); [PERISCOPE GitHub](https://github.com/broadinstitute/2022_PERISCOPE)).
- **CRISPR-KO gene count**: 20,393 gene-level profiles in A549, average 460 cells/gene from 11.2M cells imaged ([Ramezani et al.](https://www.nature.com/articles/s41592-024-02537-7)). HeLa screen at similar scale.
- **Perturbation type**: optical pooled CRISPR-Cas9 KO (not CRISPRi). Profiles are Cell-Painting-derived CellProfiler features, not embeddings; OpenPhenom-style image embeddings are not pre-released for PERISCOPE.
- **Perturb-seq counterpart in A549 or HeLa**: **not found publicly at genome scale**. Targeted A549 CRISPRi-CROP-seq exists in scattered preprints ([Frontiers Bioinformatics 2024](https://www.frontiersin.org/journals/bioinformatics/articles/10.3389/fbinf.2024.1340339/full)) but at <100-gene scale. A focused-pathway A549 CRISPRi screen of 44–61 genes per pathway exists ([bioRxiv 2024](https://www.biorxiv.org/content/10.1101/2024.01.29.576933v2.full)) but does not clear the 500-gene gate. No HeLa genome-scale Perturb-seq surfaced.
- **Hosting / license**: cpg0021-periscope on AWS S3, BSD-3-Clause profile code, CC0 data; 56 TB total, of which 11 TB is profile data and the gene-level CSV is sub-GB ([cpg0021 listing](https://github.com/broadinstitute/cellpainting-gallery)).
- **Colab footprint**: gene-level profile CSVs at 20,393 × ~2,500 features is well under 1 GB, fully tractable.
- **Verdict on ≥ 500-gene same-cell gate**: **NO**, because the matching transcriptomic side is absent. If a 500+-gene A549 Perturb-seq drops in the next year, this becomes the strongest pairing on the table.

### 3. X-Atlas/Orion (Xaira Therapeutics, 2025)

- **Cell lines on the transcriptomic side**: HCT116 (colon) and HEK293T (embryonic kidney) ([Xaira preprint, bioRxiv 2025](https://www.biorxiv.org/content/10.1101/2025.06.11.659105v1.full); [HuggingFace dataset card](https://huggingface.co/datasets/Xaira-Therapeutics/X-Atlas-Orion)).
- **Perturbation type**: CRISPRi via the FiCS (Fix-Cryopreserve-ScRNAseq) platform.
- **Perturbed gene count**: 18,903 protein-coding genes per cell line, 8M cells total, median 140 cells/perturbation, on-target KD efficiency 75.4% (HCT116) and 51.5% (HEK293T).
- **Imaging counterpart in HCT116 or HEK293T**: **not found in JUMP-CP, PERISCOPE, or rxrx3-core**. HCT116 has small-molecule Cell Painting profiles ([PLOS One 2025](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0334025)) but no public genome-scale CRISPR Cell Painting in HCT116. HEK293T is rarely used for high-content imaging.
- **Hosting / license**: HuggingFace dataset (Parquet, 126 GB) + Figshare+ ([10.25452/figshare.plus.29190726](https://doi.org/10.25452/figshare.plus.29190726)) under **CC BY-NC-SA 4.0** (note: same restrictive non-commercial license as the CZI Replogle mirror, but acceptable for a non-commercial portfolio piece).
- **Colab footprint**: full release is 126 GB, out of reach on Colab Free Drive. Figshare also hosts processed pseudobulk-style h5ads (not directly verified in this scan; needs a 30-min check before commit).
- **Verdict on ≥ 500-gene same-cell gate**: **NO**, no matching imaging dataset in HCT116 or HEK293T at scale.

### 4. Perturb-Multimodal (Sun et al., Cell 2025)

- **Same-cell, same-tissue, same-experiment** by design: paired imaging (multiplexed protein/RNA + MERFISH) and scRNA-seq on the same perturbed cells ([Sun et al. Cell 2025](https://www.cell.com/cell/fulltext/S0092-8674(25)00572-0); [Nature Genetics commentary](https://www.nature.com/articles/s41588-025-02279-y)).
- **Catch**: the published application is **mouse liver tissue**, hundreds of perturbations, not a human cell-line system. Imaging modality is MERFISH/IF, not Cell Painting; readouts are tissue-context spatial measurements, not the high-content morphological embedding space that RxRx3 / OpenPhenom occupy.
- **Verdict on ≥ 500-gene same-cell gate**: **NO** for the cellduet question; the modality is a different kind of imaging and the species is mouse.

### 5. Labitigan et al. optical pooled CRISPRi in U2OS (eLife 2024)

- Pooled optical CRISPRi screen of **366 genes** in U2OS, with deep-learning morphological embedding ([Labitigan et al., eLife reviewed preprint 2024](https://elifesciences.org/reviewed-preprints/94964)).
- Same cell line as JUMP-CP-U2OS, so a cross-screen U2OS imaging-imaging comparison is possible, but **no transcriptomic counterpart** in U2OS.
- **Verdict**: 366 genes is **below the 500-gene gate** even before considering the transcriptomic gap. Skip.

### 6. CellPaint-POSH (Caicedo lab / Recursion-style pooled Cell Painting CRISPR)

- Pooled Cell Painting CRISPR screening platform; demonstrated on a druggable-genome library of low hundreds of genes ([Nat Commun 2025](https://www.nature.com/articles/s41467-025-66778-6)). Not at the 500-gene scale in a public release.

### 7. HUVEC Perturb-seq (to pair cleanly with rxrx3-core)

- No public genome-scale or even essential-gene-scale HUVEC Perturb-seq surfaced in the search ([scPerturb / PerturBase / PerturbDB](https://academic.oup.com/nar/article/53/D1/D1099/7815638) cover 19 cell lines with K562, RPE1, HepG2, THP1, MCF10A as the standards; HUVEC is not among them).
- **Verdict**: **NO**. The cleanest cell-line match for RxRx3 is contractually disallowed by absence of upstream data. This was the original motivation for the cross-cell K562↔HUVEC pairing in B1.

### 8. K562 / RPE1 Cell Painting (to pair cleanly with Replogle)

- K562 is a **suspension** line; standard Cell Painting expects adherent cells. K562 Cell Painting at scale is not a thing in the public catalogs ([Cell Painting Gallery dataset list](https://broadinstitute.github.io/cellpainting-gallery/)). Recent platform papers (e.g. [NK-mediated K562 CRISPR-screen, eLife 2019](https://elifesciences.org/articles/47362)) use functional assays, not morphology.
- RPE1 Cell Painting at genome scale is also not in the public catalogs; no cpg00xx dataset I could identify uses RPE1 as the CRISPR perturbation line at >500 genes.
- **Verdict**: **NO**. The transcriptomic-anchor side has no morphological counterpart in either Replogle line.

## Summary table

| Pairing | Same cell? | Transcriptomic side | Imaging side | Max joint genes | Colab Free? | License pair | ≥ 500-gene gate? |
|---|---|---|---|---|---|---|---|
| JUMP-CP U2OS + Perturb-seq U2OS | yes (U2OS) | none public | 7,975 CRISPR-KO ([JUMP](https://www.biorxiv.org/content/10.1101/2023.03.23.534023v2.full)) | **0** (no transcriptomic) | yes | CC0 / N/A | **NO** |
| PERISCOPE A549 + Perturb-seq A549 | yes (A549) | none public at scale | 20,393 KO ([PERISCOPE](https://www.nature.com/articles/s41592-024-02537-7)) | **<100** today | yes | CC0 / N/A | **NO** |
| PERISCOPE HeLa + Perturb-seq HeLa | yes (HeLa) | none public at scale | ~20,000 KO ([PERISCOPE](https://www.nature.com/articles/s41592-024-02537-7)) | **<100** today | yes | CC0 / N/A | **NO** |
| X-Atlas/Orion HCT116 + HCT116 imaging | yes (HCT116) | 18,903 CRISPRi ([Xaira](https://www.biorxiv.org/content/10.1101/2025.06.11.659105v1.full)) | none public at scale | **0** (no imaging) | borderline (126 GB) | CC BY-NC-SA / N/A | **NO** |
| X-Atlas/Orion HEK293T + HEK293T imaging | yes (HEK293T) | 18,903 CRISPRi | none public at scale | **0** | borderline | CC BY-NC-SA / N/A | **NO** |
| Replogle K562 GW + JUMP-CP U2OS | **no** (K562 vs U2OS) | 9,866 CRISPRi | 7,975 KO | ~3,000–5,000 (intersect) | yes | CC BY 4.0 / CC0 | yes, but not same-cell (= B1-equivalent) |
| Replogle K562 GW + PERISCOPE A549 | **no** (K562 vs A549) | 9,866 CRISPRi | 20,393 KO | ~7,000+ | yes | CC BY 4.0 / CC0 | yes, but not same-cell |
| Perturb-Multi (Sun 2025) | yes (mouse hepatocytes) | hundreds of genes ([Sun et al.](https://www.cell.com/cell/fulltext/S0092-8674(25)00572-0)) | hundreds | hundreds | yes (small) | unspecified | mouse + tissue, off-scope |
| Labitigan U2OS optical CRISPRi | yes (U2OS) | none paired | 366 genes ([eLife](https://elifesciences.org/reviewed-preprints/94964)) | 366 if paired | yes | CC BY 4.0 | **NO** (below gate) |

## Red flags

- **Cell-line monoculture in JUMP-CP** ([Chandrasekaran et al.](https://www.biorxiv.org/content/10.1101/2023.03.23.534023v2.full)). The CRISPR-KO arm of JUMP-CP locked in U2OS specifically because U2OS had a deeper prior literature for image-based profiling. The Perturb-seq community in parallel locked in K562 and RPE1 for orthogonal reasons (CRISPRi machinery efficiency, suspension-line scalability). The two communities do not share a primary cell line.
- **Imaging assays prefer adherent lines; Perturb-seq prefers suspension lines.** This is mechanical, not arbitrary: high-content imaging needs flat morphology and consistent focus, and Perturb-seq's droplet 10x workflow is easiest on dispersed suspension cells. Genome-scale matching is therefore biased *against* the same-cell convergence scan_b2 was looking for.
- **The two paper-level attempts to align transcriptional and morphological perturbation maps that I found ([Celik et al. PLOS Comp Bio 2024](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1012463) and the [Lazar 2024 / Recursion comparison line of work](https://arxiv.org/abs/2503.20158)) both make the cross-cell-line compromise explicitly.** This is now community practice, not a flaw unique to cellduet's planned approach.
- **PERISCOPE feature space is CellProfiler features, not foundation-model embeddings.** Switching to PERISCOPE on the morphology side would require either generating OpenPhenom-style embeddings on PERISCOPE images (out of scope on Colab Free; 56 TB) or accepting handcrafted morphological features instead. RxRx3-core ships pre-computed deep embeddings; PERISCOPE does not equivalent.
- **X-Atlas/Orion non-commercial license** ([CC BY-NC-SA 4.0](https://huggingface.co/datasets/Xaira-Therapeutics/X-Atlas-Orion)) is restrictive for any commercial-republication path. Acceptable for a portfolio research artifact, blocking for redistribution.

## Recommendation

**Do not pivot to a same-cell pairing for v0. Stay on B1 (Replogle K562 GW + rxrx3-core HUVEC).** No publicly-available genome-scale same-cell Perturb-seq + imaging pair exists today, and the gap is structural (cell-line-of-choice divergence between the two communities) rather than incidental. The honest framing of the v0 result is and remains *gene-intrinsic phenotype concordance across cell-type contexts*, which the cellduet README and the Replogle dossier both already acknowledge.

**Watch list for v1.** Two specific releases would change this calculus:
- A genome-scale **A549 Perturb-seq** would unlock PERISCOPE-A549 + A549 Perturb-seq as the strongest same-cell pairing (~20,000 genes on the morphology side, full intersection with whatever the Perturb-seq side measures). The Xaira FiCS platform makes new cell-line releases plausible on a 12–18 month horizon.
- A genome-scale **HUVEC Perturb-seq** would unlock RxRx3 + HUVEC Perturb-seq as the cleanest same-cell pairing on the existing morphology side. Less likely in the near term because HUVEC is a primary line with shorter passage limits.

**Optional secondary v0 ablation.** As a no-cost robustness check, add a *second* cross-cell pairing alongside B1: Replogle K562 GW + JUMP-CP U2OS CRISPR-KO ([cpg0016-jump](https://broadinstitute.github.io/cellpainting-gallery/)). Both sides are public, both are CC0-or-equivalent, and the K562↔U2OS combination is a different cross-cell pairing than K562↔HUVEC. If the K562↔HUVEC concordance result reproduces under K562↔U2OS, that is positive multi-cell-type evidence that the concordance is gene-intrinsic; if it does not reproduce, that is informative too. This is a one-notebook addition to v0, not a scope expansion.

**Promote to full dossier?** No new dossier needed. JUMP-CP-U2OS is worth ~30 minutes of additional verification (gene list intersection with Replogle K562 GW) inside `notebooks/01_data_exploration.ipynb`, but does not warrant a standalone `docs/datasets/jump_cp.md` for v0 unless the K562↔U2OS ablation becomes a headline figure.
