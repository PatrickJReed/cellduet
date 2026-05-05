# cellduet

> Cross-modality concordance analysis of CRISPR perturbations across single-cell transcriptomic and morphological readouts.

## Research question

For genes perturbed in *both* large-scale transcriptomic Perturb-seq and image-based Cell Painting datasets, do the two readouts converge on the same biological program — or do they capture distinct, modality-specific information about perturbation phenotype?

The answer matters for target prioritization: if transcriptomic and morphological evidence agree, a perturbation hit gets stronger weight; if they disagree, the discordance is itself a mechanistic signal.

## Approach (v0)

Compute pairwise perturbation distances within each modality from publicly available pre-computed embeddings, then test for cross-modality concordance on the gene overlap.

| Stream | Source | Modality |
|---|---|---|
| Transcriptomic | [Tahoe-100M](https://arcinstitute.org/tools/virtualcellatlas) (Arc Virtual Cell Atlas) | Pooled CRISPR + scRNA-seq |
| Morphological | [Recursion RxRx3](https://www.rxrx.ai/rxrx3) + Phenom embeddings | CRISPR + Cell Painting imaging |

Analyses planned for v0:

- Identify the gene-perturbation overlap between Tahoe-100M and RxRx3
- Build a per-gene transcriptomic phenotype embedding (from Tahoe perturbation effects) and a per-gene morphological phenotype embedding (from RxRx3 Phenom features)
- Pairwise distance matrices within each modality → cross-modality correlation analysis
- Identify "convergent perturbations" (agreed-on phenotype across modalities) vs modality-specific signals
- Worked-through cases with biological interpretation

Stretch (v1):

- Shared-latent contrastive model aligning the two embedding spaces
- Multi-task probing comparing modality-specific vs shared signal per gene class
- Submission to the [Arc Virtual Cell Challenge](https://arcinstitute.org/news/virtual-cell-challenge-2025-wrap-up) if calendar aligns

## Scope discipline

This project deliberately uses **pre-computed embeddings** and does not retrain encoders from raw images or raw counts. The interesting research question lives in the embedding-space comparison, not in the encoders. This keeps v0 shippable on a single workstation; full encoder training is out of scope.

## Related work

- Tegtmeyer et al., *Nature Communications* (2025). NeuroPainting + transcriptomics for the 22q11.2 deletion. ([10.1038/s41467-025-61547-x](https://doi.org/10.1038/s41467-025-61547-x))
- Sun et al., *Cell* (2025). Perturb-Multimodal: pooled genetic screens with imaging and sequencing in intact tissue.
- Tahoe-100M and the Tahoe + Arc + Biohub partnership announcement (Jan 2026)
- Arc Institute Virtual Cell Initiative (STATE, Tahoe-x1, TranscriptFormer)
- Cui et al., *Nature Methods* (2024). scGPT foundation model for single-cell.
- Theodoris et al., *Nature* (2023). Geneformer.
- ESM3 (EvolutionaryScale, 2025). Joint sequence + structure + function reasoning.

## Author

Patrick J. Reed, Ph.D. ([LinkedIn](https://linkedin.com/in/patrickjenningsreed))

This project extends a multi-stream target-prioritization framework built at Bristol Myers Squibb (12M-nuclei NeuroPsych atlas, 6-phase deep-phenotyping pipeline, scGPT/Geneformer fine-tuning on AMP-PD snRNA-seq) to multimodal perturbation evidence — adding a sixth orthogonal stream (morphological perturbation phenotype) to the convergent-evidence ranking workflow.

## License

MIT — see [LICENSE](LICENSE).
