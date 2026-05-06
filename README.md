# cellduet

> Cross-modality phenotype concordance for small-molecule perturbations across single-cell transcriptomic and image-based morphological readouts.

## Research question

For small molecules profiled in *both* a large-scale transcriptomic perturbation atlas and an image-based Cell Painting dataset, do the two readouts converge on the same biological program, or do they capture distinct, modality-specific information about drug phenotype? Where they diverge, does the discordance carry interpretable mechanistic signal (off-target activity, polypharmacology, cell-type-restricted effects)?

The answer matters for target deconvolution and drug repurposing: if transcriptomic and morphological evidence agree, a compound's claimed mechanism gets stronger weight; if they disagree, the discordance is itself a flag for off-target structure or context-dependence.

## Approach (v0)

Compute pairwise per-compound distances within each modality from publicly available pre-computed embeddings, then test for cross-modality concordance on the shared-compound set. The v0 design uses a **three-arm structure**: one primary statistical test, one cross-encoder + cross-cell-type robustness arm, and one same-cell-line sanity check.

| Arm | Transcriptomic | Morphological | Cell context | Shared compounds |
|---|---|---|---|---|
| **Primary** | [Tahoe-100M](https://huggingface.co/datasets/tahoebio/Tahoe-100M) (Vevo / Arc Virtual Cell Atlas) | [JUMP-CP cpg0016](https://github.com/broadinstitute/cellpainting-gallery) (Cell Painting Consortium) | Tahoe 50 cancer lines × U2OS osteosarcoma | **228** |
| **Robustness** | Tahoe-100M | [Recursion rxrx3-core](https://huggingface.co/datasets/recursionpharma/rxrx3-core) (Phenom embeddings) | Tahoe 50 cancer lines × HUVEC primary endothelial | **145** |
| **Sanity** | Tahoe-100M (subset to A549) | [CPJUMP1 (cpg0000-jump-pilot)](https://github.com/broadinstitute/cellpainting-gallery) | A549 lung adenocarcinoma in both | **14** |

Analyses planned for v0:
- Build per-compound transcriptomic phenotype vectors from Tahoe pseudobulk drug effects
- Build per-compound morphological phenotype vectors from each morphology arm using publicly released embeddings (CellProfiler / cpcnn, OpenPhenom, Phenom-1/2)
- Compute within-modality pairwise compound-compound distance matrices
- Cross-modality concordance test per arm: Mantel correlation, RV coefficient, per-compound neighborhood Jaccard with permutation null
- Characterize discordant compounds against drug-target annotations and known polypharmacology
- Worked-through cases with biological interpretation, anchored on a focal compound family (likely EGFR inhibitors; ~12 Tahoe-overlap drugs)

Stretch (v1+):

- Extend the framework to **gene-perturbation cross-modality** (Replogle 2022 Perturb-seq × CRISPR-KO Cell Painting from JUMP-CP / PERISCOPE), now with same-perturbation-type matched
- Shared-latent contrastive model aligning the two embedding spaces; HF model checkpoint at `patrickjreed/cellduet-shared-latent`
- Multi-task probing comparing modality-specific vs shared signal per drug class / target class
- HF Spaces Gradio demo: enter a compound or gene, see its transcriptomic and morphological neighbors with concordance score
- Submission to the [Arc Virtual Cell Challenge](https://arcinstitute.org/news/virtual-cell-challenge-2025-wrap-up) if calendar aligns

## Scope discipline

This project deliberately uses **pre-computed embeddings and pseudobulk aggregates** and does not retrain encoders from raw images or raw counts. The interesting research question lives in the embedding-space comparison, not in the encoders. This keeps v0 shippable on Google Colab Free tier (T4 GPU, ~12 GB RAM, ~15 GB Drive); full encoder training is out of scope.

## Running cellduet

All analyses are designed to run on **Google Colab Free tier**. Code is developed locally; execution happens on Colab; artifacts persist on **Hugging Face Hub**.

| Notebook | Open on Colab |
|---|---|
| `00_environment_smoke` | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/PatrickJReed/cellduet/blob/main/notebooks/00_environment_smoke.ipynb) |

First-time setup (Hugging Face account, Colab activation, VS Code workflow): see [docs/SETUP.md](docs/SETUP.md). Per-dataset details (origin, license, distribution, compute footprint) live in [docs/datasets/](docs/datasets/).

## Related work

- Chandrasekaran et al. (2024). *Three million images and morphological profiles of cells treated with matched chemical and genetic perturbations.* The JUMP-Cell Painting Consortium primary paper. ([Nat Methods 21:1114-1121](https://doi.org/10.1038/s41592-024-02241-6))
- Fay et al. (2023). *RxRx3: Phenomics Map of Biology.* Recursion's CRISPR-KO Cell Painting atlas, plus Phenom embeddings. ([bioRxiv 2023.02.07.527350](https://doi.org/10.1101/2023.02.07.527350))
- Kraus et al. (2024). *Masked Autoencoders for Microscopy are Scalable Learners of Cellular Biology.* The OpenPhenom / Phenom-family encoder lineage. ([CVPR 2024, arXiv:2404.10242](https://arxiv.org/abs/2404.10242))
- Zhang et al. (2025). *Tahoe-100M: A Giga-Scale Single-Cell Perturbation Atlas for Context-Dependent Gene Function and Cellular Modeling.* ([bioRxiv 2025.02.20.639398](https://doi.org/10.1101/2025.02.20.639398))
- Subramanian et al. (2017). *A Next Generation Connectivity Map: L1000 Platform and the First 1,000,000 Profiles.* The reference prior work on transcriptomic-vs-imaging compound concordance. ([Cell 171:1437-1452](https://doi.org/10.1016/j.cell.2017.10.049))
- Replogle et al. (2022). *Mapping information-rich genotype-phenotype landscapes with genome-scale Perturb-seq.* The CRISPR-perturbation transcriptomic backbone for v1. ([Cell 185:2559-2575](https://doi.org/10.1016/j.cell.2022.05.013))
- Sun et al. (2025). *Perturb-Multimodal: pooled genetic screens with imaging and sequencing in intact tissue.*
- Cui et al. (2024). *scGPT: toward building a foundation model for single-cell multi-omics using generative AI.* ([Nat Methods](https://doi.org/10.1038/s41592-024-02201-0))
- Theodoris et al. (2023). *Transfer learning enables predictions in network biology.* Geneformer. ([Nature](https://doi.org/10.1038/s41586-023-06139-9))

## Author

Patrick J. Reed, Ph.D. ([LinkedIn](https://linkedin.com/in/patrickjenningsreed))

This project extends a multi-stream target-prioritization framework built at Bristol Myers Squibb (12M-nuclei NeuroPsych atlas, 6-phase deep-phenotyping pipeline, scGPT/Geneformer fine-tuning on AMP-PD snRNA-seq, Cerberus-inspired multi-task foundation-model proof-of-concept on the Broad NeuroPainting Cell Painting dataset) to multimodal compound evidence, adding a sixth orthogonal stream (image-based morphological perturbation phenotype) to the convergent-evidence ranking workflow.

## License

MIT — see [LICENSE](LICENSE).
