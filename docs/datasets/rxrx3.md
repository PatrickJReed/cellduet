# RxRx3 and the Phenom embeddings

A dossier for the cellduet v0 analysis. Numbers are cited inline. Anything not on a primary source is marked as "not published" or as an empirical question.

## Origin and citation

RxRx3 is a phenomics dataset released by [Recursion Pharmaceuticals](https://www.recursion.com/) in early 2023 alongside a bioRxiv preprint, [Fay et al., "RxRx3: Phenomics Map of Biology," bioRxiv 2023.02.07.527350](https://www.biorxiv.org/content/10.1101/2023.02.07.527350v1) (posted February 8, 2023). It is the third entry in the RxRx series after RxRx1 (2019) and RxRx2 (2020), per the [rxrx.ai/datasets index](https://www.rxrx.ai/datasets).

Two distinct releases exist:

- **Full RxRx3.** A genome-scale CRISPR-Cas9 knockout screen plus a small-molecule arm. Embeddings and image data for the full release are gated behind Recursion's MolRec download portal at [rxrx.ai/rxrx3](https://www.rxrx.ai/rxrx3); the dataset card describes the full corpus as roughly 100 TB of imagery covering ~17,000 genes and 2.2 million wells. About 16,000 of the perturbed genes are anonymised in the public release ("gene0001" style labels), with only a subset of named genes exposed for benchmarking. Distribution is image- and embedding-only, no raw sgRNA-level data.

- **rxrx3-core.** A curated subset released in late 2024 to accompany the OpenPhenom-S/16 model and the [Kraus et al., arXiv:2503.20158, RxRx3-core: Benchmarking drug-target interactions in High-Content Microscopy](https://arxiv.org/abs/2503.20158) (LMRL Workshop at ICLR 2025) paper. Hosted on Hugging Face at [recursionpharma/rxrx3-core](https://huggingface.co/datasets/recursionpharma/rxrx3-core), 21.7 GB total on disk, 222,601 wells. The 736 genes here are the not-blinded subset of the full RxRx3 (i.e., gene symbols are exposed), drawn from the gene001-gene176 experiments per the [arxiv HTML](https://arxiv.org/html/2503.20158v2). Verified directly from the metadata CSV: 735 unique HGNC symbols plus one `EMPTY_control` label across 126,900 CRISPR wells (the abstract's "736" counts EMPTY_control).

Both releases ship under the [Recursion Commercial End User License Agreement](https://huggingface.co/datasets/recursionpharma/rxrx3-core/blob/main/LICENSE), which Recursion describes as "similar to CC BY-SA" but with a hard carve-out: the materials may not be used for any neuroscience research, target validation, AI-model training, or commercial program in the neuroscience field (Section 3, paragraphs (a)-(e)). Older Recursion press materials describe RxRx3 as "CC BY-NC-SA"; the actual file shipped with rxrx3-core is the bespoke EULA, not a Creative Commons license. Citing this dossier is fine; using the embeddings as inputs to a neuroscience-themed downstream pipeline is contractually disallowed.

OpenPhenom-S/16 model weights are publicly released on Hugging Face at [recursionpharma/OpenPhenom](https://huggingface.co/recursionpharma/OpenPhenom) (also under a Recursion non-commercial EULA). Phenom-1 and Phenom-2 weights are not released; only their pre-computed embeddings on rxrx3-core are.

## Biological scope

- **Perturbation type.** CRISPR-Cas9 knockouts in primary [HUVEC](https://en.wikipedia.org/wiki/Human_umbilical_vein_endothelial_cells) (human umbilical vein endothelial cells), per [Fay et al. 2023](https://www.biorxiv.org/content/10.1101/2023.02.07.527350v1). Not CRISPRi.
- **Library scale.** The bioRxiv abstract reports 17,063 genes profiled with 101,029 sgRNAs, typically 6 guides per gene with 24 replicates per guide. The cited well total is 2.2 million across both arms (CRISPR plus the small-molecule arm). The number of perturbations attempted vs passing QC is not broken out in the abstract; the QC details live in the methods of the preprint, which is the empirical thing to read for cellduet.
- **Compound arm.** 1,674 known small-molecule compounds at 8 concentrations each, also in HUVEC, per the [rxrx.ai/rxrx3](https://www.rxrx.ai/rxrx3) page. Irrelevant to cellduet's CRISPR-vs-CRISPRi comparison but it is half of the wells.
- **Cell Painting protocol.** 6 fluorescence channels: Hoechst (DNA), ConA (ER), Phalloidin (F-actin), Syto14 (nucleoli/RNA), MitoTracker (mitochondria), WGA (Golgi/membrane). Confirmed against the [rxrx.ai/rxrx3](https://www.rxrx.ai/rxrx3) listing. Magnification is not stated on the rxrx.ai page; the imaging field is 2048x2048x6 per well, with one site per well in 1536-well plates.
- **Plate structure.** 1536-well plates, 1 imaging site per well. The compound arm uses randomized layouts; the CRISPR arm uses gene-replicated layouts ([rxrx3-core paper, Section 3.1](https://arxiv.org/html/2503.20158v2)).
- **rxrx3-core specifically.** 222,601 wells (verified by `wc -l` on the metadata CSV); 126,900 CRISPR wells across 735 named genes plus 25,312 `EMPTY_control` wells; remainder are compound-arm wells. The image patches are 512x512x6 pixels (downsampled from full-resolution).

## Disease-gene coverage

This was checked directly against the rxrx3-core metadata CSV (`metadata_rxrx3_core.csv`, downloaded May 2026 from the HF resolve URL). Coverage in the **full RxRx3** is presumed yes for almost any human protein-coding gene, since the screen is genome-scale at 17,063 genes; however, the gene symbols of approximately 16,000 of those are blinded in the public release, so practical coverage of named disease genes through the public release is rxrx3-core only.

| Set | Gene | rxrx3-core (verified) | full RxRx3 (~17k genes) |
|---|---|---|---|
| Neuro | TARDBP | no | likely yes (blinded) |
| Neuro | FUS | no | likely yes (blinded) |
| Neuro | C9orf72 | no | likely yes (blinded) |
| Neuro | GRN | no | likely yes (blinded) |
| Neuro | MAPT | no | likely yes (blinded) |
| Neuro | SNCA | no | likely yes (blinded) |
| Neuro | LRRK2 | no | likely yes (blinded) |
| Neuro | APP | no | likely yes (blinded) |
| Neuro | PSEN1 | no | likely yes (blinded) |
| Neuro | PSEN2 | no | likely yes (blinded) |
| Neuro | SOD1 | no | likely yes (blinded) |
| Neuro | HTT | no | likely yes (blinded) |
| Neuro | ATXN1 | no | likely yes (blinded) |
| Neuro | ATXN2 | no | likely yes (blinded) |
| Neuro | ATXN3 | no | likely yes (blinded) |
| Neuro | PARK7 (DJ-1) | no | likely yes (blinded) |
| Neuro | PINK1 | no | likely yes (blinded) |
| Neuro | PRKN | no | likely yes (blinded) |
| Onco | TP53 | yes | yes |
| Onco | KRAS | no | likely yes (blinded) |
| Onco | BRAF | yes | yes |
| Onco | EGFR | yes | yes |
| Onco | MYC | no | likely yes (blinded) |
| Onco | PIK3CA | yes | yes |
| Onco | PTEN | no | likely yes (blinded) |
| Onco | RB1 | no | likely yes (blinded) |
| Onco | CDKN2A | no | likely yes (blinded) |
| Cardiac | MYH7 | no | likely yes (blinded) |
| Cardiac | TTN | no | likely yes (blinded) |
| Cardiac | LMNA | no | likely yes (blinded) |
| Cardiac | KCNQ1 | no | likely yes (blinded) |
| Cardiac | SCN5A | yes | yes |
| Metab | INSR | yes | yes |
| Metab | LEP | no | likely yes (blinded) |
| Metab | LEPR | no | likely yes (blinded) |
| Metab | MC4R | no | likely yes (blinded) |
| Metab | PCSK9 | no | likely yes (blinded) |
| Metab | LDLR | no | likely yes (blinded) |

Headline: zero of the 18 neuro genes are in rxrx3-core. The Recursion EULA bans neuroscience use anyway, which makes the absence non-actionable. Oncology is partial (4/9 named); cardiac and metabolic are sparse (1/5 and 1/6). The 735 named genes appear to bias toward broadly cytoprotective and metabolic enzyme classes (visible in the alphabetic head: ABCC1/4/8, ABCG2, ABL1, ACAA2, the ACAD-family, ACE, ACHE, ACLY, ACO2, ACTB...), consistent with a benchmark-friendly subset focused on well-annotated drug targets, not a disease-genetics panel.

The exhaustive list of named genes is in `metadata_rxrx3_core.csv` on Hugging Face; programmatic check is `set(df.loc[df.perturbation_type=='CRISPR','gene'].dropna().unique())`.

## Distribution and access

| Release | Host | Auth | Size on disk | Format |
|---|---|---|---|---|
| rxrx3-core (images + embeddings) | [HF: recursionpharma/rxrx3-core](https://huggingface.co/datasets/recursionpharma/rxrx3-core) | None for read; EULA binds use | 21.7 GB total | JP2 images in 35 sharded `data/train-*.parquet`; metadata CSV; 3 sibling embedding parquets |
| full RxRx3 (images + embeddings) | MolRec download portal at [rxrx.ai/rxrx3](https://www.rxrx.ai/rxrx3) | Recursion account, EULA accept | ~100 TB | not specified publicly |
| OpenPhenom-S/16 weights | [HF: recursionpharma/OpenPhenom](https://huggingface.co/recursionpharma/OpenPhenom) | None for read; EULA binds use | small (ViT-S/16, ~25M params) | safetensors |

For Colab, only rxrx3-core is realistic. The single 532 MB `OpenPhenom_rxrx3_core_embeddings.parquet` plus the 20 MB metadata CSV is the smallest useful slice. `huggingface_hub.hf_hub_download(..., repo_type="dataset")` streams to `/content` or to mounted Drive. No access tokens needed for the dataset itself.

The full RxRx3 distribution is not streaming-friendly for Colab on any reasonable timescale: 100 TB through MolRec is incompatible with the 12-hour session and 15 GB Drive ceiling. Even if the per-well embeddings were extracted at 1024-d float32, 17,063 genes x 6 guides x 24 replicates x 4096 bytes is ~10 GB just for the CRISPR arm, which is feasible in principle but is not how Recursion ships the full release.

## Pre-computed artifacts

rxrx3-core ships **three** parallel embedding parquets, all keyed on `well_id` (one row per well, total 222,601 rows each), verified by directly reading the parquet schemas:

| Encoder | Backbone | Params | Embedding dim | File size |
|---|---|---|---|---|
| OpenPhenom-S/16 (CA-MAE) | ViT-S/16 | ~25 M | **384** | 532 MB |
| Phenom-1 (RPI-93M) | ViT-L/8 | ~307 M | **1024** | 1.4 GB |
| Phenom-2 (PP-16M trimmed) | ViT-G/8 | ~1.86 B | **1664** | 2.3 GB |

Encoder lineage: OpenPhenom-S/16 is the channel-agnostic MAE described in [Kraus et al., arXiv:2404.10242 (CVPR 2024), "Masked Autoencoders for Microscopy are Scalable Learners of Cellular Biology"](https://arxiv.org/abs/2404.10242) and shipped publicly. Phenom-1 and Phenom-2 are larger ViT-L/8 and ViT-G/8 MAEs trained on Recursion's internal RPI-93M and PP-16M corpora respectively; their embeddings on rxrx3-core are released, but the encoder weights themselves are not, per the [rxrx3-core paper, Section 3](https://arxiv.org/html/2503.20158v2) and the OpenPhenom HF model card.

OpenPhenom's published recipe (from the [HF model card](https://huggingface.co/recursionpharma/OpenPhenom)) takes a 256x256x6 image and emits a 384-d vector. The rxrx3-core paper describes the per-well aggregation: "the four tiled embeddings from every 256x256x6 crop of each 512x512x6 microscopy image are mean-aggregated," followed by PCA-CenterScale batch alignment ([arXiv:2503.20158](https://arxiv.org/html/2503.20158v2)). So one `well_id` row in the released parquet is the per-well mean across 4 tile embeddings, post-PCA-CS.

**Per-gene embeddings are not pre-computed.** Aggregation level on the wire is per-well. The cellduet v0 pipeline must aggregate per-well -> per-gene itself. Default approach: arithmetic mean across the 4-6 sgRNA replicate wells per gene (or median for robustness against guide-off-target outliers). The rxrx3-core paper's downstream benchmarks aggregate by treatment (gene or compound at concentration) using `EFAAR_benchmarking` ([github.com/recursionpharma/EFAAR_benchmarking](https://github.com/recursionpharma/EFAAR_benchmarking)), which centers on controls and applies typical-variation normalization (TVN) before averaging; reuse of that recipe is the natural choice.

## Compute footprint for v0

Working with rxrx3-core under Colab Free constraints is comfortable.

- **OpenPhenom 384-d embeddings.** 222,601 wells x 384 floats x 4 bytes = 342 MB in float32, ~170 MB in float16. The parquet on disk is 532 MB. Loads in seconds; fits in RAM with all of pandas around it; per-gene aggregation across 735 genes drops it to a 735 x 384 matrix (1.1 MB).
- **Phenom-1 1024-d embeddings.** 222,601 x 1024 x 4 = 911 MB (1.4 GB on disk as parquet). Borderline on the 12 GB Colab RAM if anything else is loaded, but a streaming read of `pyarrow.dataset` keeps it manageable.
- **Phenom-2 1664-d embeddings.** 222,601 x 1664 x 4 = 1.48 GB (2.3 GB on disk). Still loadable but the pareto trade-off vs Phenom-1 is unclear without benchmarking.
- **Per-gene aggregated arrays for the v0 pipeline.** 735 x 1664 x 4 = 4.9 MB. Distance matrix 735 x 735 x 4 = 2.2 MB. Negligible.

The full RxRx3 is **not tractable** on Colab Free. Use rxrx3-core. The 735-gene panel is the operating gene set; intersection with Replogle K562 GW (~9,866 genes) is the binding constraint.

T4 VRAM is a non-issue because no encoder is being run; cellduet only loads pre-computed embeddings.

## Known caveats

- **Not biological semantics.** The MAE encoders are trained as visual reconstruction objectives. The [arXiv:2404.10242](https://arxiv.org/abs/2404.10242) paper claims downstream biological signal (gene-gene relationship recovery on JUMP-CP, etc.), but the embedding space is a function of pixel statistics first and biology second. Batch effects, plate effects, and channel-intensity drift sit in the same dimensions as the biology unless explicitly subtracted. Recursion's own recommended fix on the OpenPhenom card is "Typical Variation Normalization": fit PCA on the EMPTY_control wells per batch, then standardize. Applying this inside the cellduet pipeline is mandatory, not optional.
- **Plate / batch effects.** rxrx3-core spans gene experiments (the gene001-gene176 series in the original RxRx3) and compound experiments. Each sub-experiment has its own plates, day-of-imaging effects, and edge-well artifacts. The released embeddings have already been PCA-CS aligned per the paper, but residual structure persists; the rxrx3-core benchmarks themselves use TVN on top.
- **Cell-type confound.** RxRx3 is HUVEC: primary endothelial cells from umbilical vein, post-mitotic cultures, cytoskeletal and adhesion biology dominant. K562 (Replogle) is a chronic myeloid leukemia suspension line, immortalized, hematopoietic lineage. They share core housekeeping biology but diverge on cell-type-specific signaling, lineage transcription factors, adhesion machinery, and stress response. This is the first-order limitation on cross-modal correlation and is discussed at length in section 8.
- **Single imaging site per well.** No within-well technical replication; biological replication only via the 6 sgRNAs x 24 wells per gene in the full RxRx3. In rxrx3-core the per-gene replicate count varies (curated subset) and should be checked empirically.
- **Anonymized genes.** The full RxRx3 hides ~16,000 gene names. cellduet does not need them, since rxrx3-core exposes the full 735 named genes used in benchmarks; just be aware that the full RxRx3 download is mostly opaque.
- **Encoder choice is unsettled.** OpenPhenom-S/16 is the only released model with weights, so it is the only Phenom-family encoder anyone outside Recursion can run on new data. Phenom-1 and Phenom-2 embeddings on rxrx3-core are larger and probably more expressive; the [rxrx3-core paper Table 1/2](https://arxiv.org/html/2503.20158v2) shows Phenom-2 winning most benchmarks but by modest margins. For v0, OpenPhenom-384d is the simplest baseline; switching to Phenom-1/1024d is an A/B knob.

## Joint-with-Replogle-K562 considerations

The binding gene set is rxrx3-core's 735 named CRISPR genes. Replogle K562 GW covers roughly 9,866 perturbed genes per the cellduet replogle dossier; the full Replogle GW manifest is essentially every expressed protein-coding gene in K562. The expected overlap is therefore very close to **735 - (a small number of K562-non-expressed genes)**, i.e., on the order of **600-720 genes** survive the intersection. This is a back-of-envelope estimate; the precise count is an empirical question for notebook 01 (load both manifests, intersect, drop duplicates from synonyms).

This 600-720-gene panel is the operating sample size for the cross-modal correlation. It is acceptable for a Mantel-style or RV-coefficient cross-distance-matrix test (n > 100 is fine for power); it is small for any per-gene per-modality regression that needs degrees of freedom.

**Gene-symbol convention.**
- rxrx3-core uses HGNC-style symbols (verified: 'TP53', 'EGFR', 'BRAF', 'PIK3CA', 'INSR' all present; the alphabetic head is ABCC1, ABCC4, ABCC8, ABCG2, ABL1, ACAA2... which are HGNC). One sentinel label `EMPTY_control` for the no-guide control wells.
- Replogle h5ad typically stores Ensembl gene IDs in `var_names` and HGNC symbols in `var['gene_symbol']` (or similar). Harmonization is a left-join on HGNC symbol with a fallback to Ensembl-ID lookup via [mygene.info](https://mygene.info/) or a static mapping. Watch for: pseudogenes with overlapping symbols, sex-chromosome paralogs, and recently-renamed symbols (e.g., FAM-family rename events post-2020). HUVEC and K562 share standard human reference, no species drift.

**Cell-type mismatch is the central caveat.** This dossier flags it explicitly because a strong null would be expected if the two cell types disagreed on every gene. The reasonable v0 hypothesis is that the cross-modal Mantel correlation is positive but modest (e.g., r in 0.05-0.3 range), driven by housekeeping biology that is shared, with most cell-type-specific signaling and tissue-context biology orthogonal between K562 and HUVEC. If the v0 correlation is notably positive, that is a finding; if it is near zero, that is also a finding ("phenotype concordance is cell-type-bound"). The dossier's framing should not pretend HUVEC + K562 is a fair test of the same biology.

## Open questions

These cannot be answered without actually running the load step.

1. **Per-gene replicate count in rxrx3-core.** The full RxRx3 had 6 guides x 24 replicates per gene; rxrx3-core is curated, so the per-gene well count varies. Need to compute `metadata.groupby('gene').size()`.
2. **Exact gene-set overlap with Replogle K562 GW.** Estimate above is 600-720; empirical answer requires loading both manifests.
3. **Within-modality embedding stability.** Variance of per-gene mean embedding across guides within rxrx3-core is unknown until measured. If guide-level variance is comparable to gene-level variance, the per-gene aggregate is noisy and the cross-modal correlation will be attenuated.
4. **Whether to use OpenPhenom-384d vs Phenom-1-1024d vs Phenom-2-1664d.** Pick one for the v0 baseline; an ablation is feasible since all three parquets are released. The rxrx3-core paper's benchmark numbers do not directly translate to gene-gene cross-modal correlation against Perturb-seq; this has to be measured.
5. **Whether TVN / PCA-CS suffices, or whether additional batch correction is needed before cross-modal correlation.** The released embeddings are already PCA-CS aligned, but residual plate effects may still inflate gene-gene similarity within a plate. A simple plate-residual regression on the per-well embedding before averaging is the safe first move.
6. **Practical I/O cost on Colab.** Reading 532 MB OpenPhenom parquet + 20 MB metadata is fast; reading 2.3 GB Phenom-2 parquet via `huggingface_hub` from a cold session needs to be timed once, not assumed. Drive caching is the planned mitigation.
7. **Whether Recursion's `EFAAR_benchmarking` library is reusable as-is for the per-gene aggregation step.** Worth a 30-minute read of the repo before re-implementing the same TVN-and-mean recipe by hand.
