# cellduet — project context

The strategic background behind this project: why it exists, how the dataset and methodology choices were made, what the short- and long-term goals are, and how it connects to prior work. Companion to `README.md` (public-facing research framing) and `CLAUDE.md` (coding-context for Claude Code sessions).

## Why this project exists

This project is part of a deliberate portfolio strategy by **Patrick J. Reed, Ph.D.** (computational biologist, 15+ years; most recently Principal Scientist at Bristol Myers Squibb). Patrick's industry track record sits at the intersection of single-cell transcriptomics, foundation-model machine learning, and neurodegenerative-disease drug discovery. The job market in 2026 has converged on a hot subfield Patrick has not yet shipped a public artifact in: **multimodal perturbation analysis with foundation models**.

The project was selected through a structured gap analysis. Two phases:

- **2026-04-15 portfolio brainstorm** (`~/NewRoleEfforts/docs/portfolio_project_brainstorm.md`) tabulated skill signals across 72 senior-IC AI-bio job postings. Top gaps: generative models (39%), LLMs/agents (36%), protein language models (25%), GNNs (19%). Three projects were considered: an LLM agent for single-cell analysis (CellAgent), a domain-specific BioRAG, and a fine-tuned single-cell QA model.
- **2026-05-05 field pulse** refreshed the analysis with the more recent JD corpus and surfaced two new threads that hadn't been salient in April: **virtual cell foundation models / perturb-seq at scale** (Arc Institute Virtual Cell Initiative, Tahoe-100M, STATE, TranscriptFormer; Xaira, Recursion, Insitro) and **MCP servers / Claude agents for life sciences** (Anthropic's Claude for Life Sciences launch, HHMI + Allen Institute partnerships, the live Applied AI Engineer Life Sciences role).

`cellduet` and a sibling project (`cellagent`, an LLM agent for single-cell analysis) were chosen as the two highest-leverage builds. cellduet specifically closes three credentialing gaps simultaneously: **perturb-seq specificity**, **image-based CRISPR perturbation**, and **multimodal foundation-model integration**.

## Why these datasets

### Tahoe-100M (transcriptomic readout)

- **Canonical drug-perturbation single-cell atlas.** Released 2025 on the Arc Virtual Cell Atlas as the inaugural Atlas contribution by Vevo Therapeutics. Tahoe is a small-molecule screen, not a CRISPR screen: 379 unique drugs (across ~1,100 drug-by-dose conditions) profiled in pooled "cell village" wells over 50 cancer cell lines, with ~95.6M scRNA-seq cells passing QC. Vehicle controls are DMSO. The dataset is CC0-1.0.
- **Training/reference data for the major virtual-cell architectures** the field is converging on (STATE, Tahoe-x1, TranscriptFormer).
- **Active ecosystem.** The Tahoe + Arc + Biohub partnership announced in January 2026 is generating ~120M new perturbation data points across 225K drug-patient interactions; cellduet's analytical methods are designed to extend cleanly to that next-generation dataset.
- **Plugs into the Arc Virtual Cell Challenge.** Submitting to the next iteration is a v1 stretch.

### Cell Painting on the morphological side: a three-arm design

The morphological side of v0 uses **three Cell Painting datasets**, each playing a distinct role in the cross-modal test:

- **JUMP-Cell Painting Consortium cpg0016 ("JUMP main", primary)**. The largest publicly available compound Cell Painting dataset: 115,795 unique compounds across 803,853 wells, U2OS osteosarcoma, harmony-corrected 737-d CellProfiler features released CC0-1.0 on the Cell Painting Gallery. **228 compounds intersect with Tahoe-100M's drug list** by full InChIKey. Headline statistical test for v0.
- **Recursion rxrx3-core (robustness arm)**. 735 named CRISPR-KO genes plus a curated compound subset in HUVEC primary endothelial cells, with three pre-computed deep-encoder embedding products (OpenPhenom 384-d, Phenom-1 1024-d, Phenom-2 1664-d). 145 compounds overlap with Tahoe under skeleton-InChIKey matching. Tests whether the cross-modal concordance pattern survives both an encoder change (Phenom vs CellProfiler) and a cell-context change (HUVEC vs U2OS).
- **CPJUMP1 cpg0000-jump-pilot (same-cell sanity check)**. The JUMP consortium's pilot dataset, 302 compounds in A549 and U2OS, CellProfiler features only. **A549 is the one cell line shared with Tahoe-100M**, so subsetting Tahoe to A549 cells gives a 14-compound (11 treatment + 3 positive-control) same-cell-same-perturbation comparison. Small N but uniquely interpretable.

**Direct connection to Patrick's prior work.** At BMS, Patrick built a multi-task foundation-model proof-of-concept for the Neurobot HTS platform (Cerberus-inspired ResNet34 shared encoder, three task heads on the Broad NeuroPainting Cell Painting dataset). cellduet is methodology continuation on a different cell line and a different perturbation modality, with no encoder retraining; the encoders are public OpenPhenom and CellProfiler / cpcnn artifacts.

### Why drug-vs-drug, and why three arms

Most published virtual-cell work focuses on a single readout modality. The open question, *do transcriptomic and morphological drug phenotypes agree, and where they diverge, what does the discordance tell us about off-target activity, polypharmacology, or cell-context-dependence?*, has been touched by prior L1000-vs-Cell-Painting work (Subramanian et al. 2017 Connectivity Map) and by Recursion's internal benchmarks, but has not been answered using the most current 2025–2026 perturbation-atlas stack (Tahoe-100M scRNA-seq + JUMP cpg0016 / Phenom Cell Painting). The three-arm design lets the v0 result claim more than agreement-vs-disagreement on a single dataset pair: it tests the same question across encoders, across cell contexts, and at one same-cell-line slice. cellduet adds a sixth orthogonal evidence stream to Patrick's BMS-era 5-stream target-prioritization framework (compositional, GWAS-conditioned, trajectory, regulatory, ligand-receptor), namely directly-measured cross-modal drug phenotype concordance.

A v1 follow-up extends the same framework to **gene-perturbation cross-modality** (Replogle 2022 Perturb-seq × CRISPR-KO Cell Painting from JUMP / PERISCOPE), which addresses the original CRISPR-vs-CRISPR framing now that the v0 drug-vs-drug analysis is shipped.

## Strategic positioning

The artifact is built to support applications to the following role classes:

- **Anthropic Applied AI Engineer, Life Sciences** (Beneficial Deployments) — live posting; the JD explicitly asks for builders who can ship MCP servers and agent skills for genomics platforms. cellduet demonstrates the builder credibility on a non-trivial bio analysis.
- **Anthropic Research Scientist, Life Sciences** — was posted with a January 5 2026 deadline; reposts are likely. cellduet is publishable-aspiring research that maps to "fundamental biological discoveries" framing.
- **Xaira Therapeutics** — already received a tailored application from Patrick. The Xaira application honest-framed scRNA-seq-readout Perturb-seq as a near-adjacency rather than direct experience. cellduet turns that adjacency into a shipped artifact for any follow-up conversation or future re-application.
- **Recursion, Insitro, Iambic Therapeutics, Arc-adjacent academic appointments** — image-based CRISPR perturbation experience is a stated must-have or strong preference at all of these. The RxRx3 analytical work in cellduet maps directly.
- **General "perturb-seq + multimodal foundation model" credentialing** for any frontier-lab bio-AI role that surfaces.

## Connection to prior work

- **NeuroPainting multi-task foundation model** (BMS, 2025): Cerberus-inspired ResNet34 with three task heads. Same authoring scientist, same modality (Cell Painting imaging), same multi-task framing. cellduet extends the single-modality framing to an explicit two-modality concordance question.
- **12-million-nuclei NeuroPsych single-cell atlas** (BMS, 2026): atlas-scale snRNA-seq data engineering; same author. cellduet's transcriptomic side leverages the same toolchain (Scanpy, scVI-tools, Harmony).
- **6-phase deep phenotyping pipeline + 5-stream convergent target prioritization** (BMS, 2026): the analytical framework Patrick describes in interviews (e.g., the Valo Health Q3 100-target prioritization answer). cellduet is the public artifact of a 6th stream extending that framework to multimodal evidence.
- **scGPT and Geneformer fine-tuning on AMP-PD snRNA-seq** (BMS, 2025-2026): foundation-model fine-tuning experience that translates directly to Tahoe-100M / TranscriptFormer adaptation in v1.

## Short-term goals (v0, ~4–6 weeks evening work)

1. Verify the InChIKey compound intersections that drive each arm of the B3 design (target: 228 / 145 / 14) and produce per-arm replicate-count diagnostics.
2. Aggregate pre-computed embeddings to per-compound phenotype vectors in each modality (Tahoe pseudobulk for transcriptomic; JUMP cpg0016 harmony features, rxrx3-core OpenPhenom, CPJUMP1 CellProfiler features for morphological).
3. Compute within-modality pairwise distance matrices on each shared-compound set.
4. Cross-modality concordance test per arm: Mantel correlation, RV coefficient, per-compound neighborhood Jaccard with permutation null. Sensitivity of the headline (B3b) Mantel-r to Tahoe-pooled vs Tahoe-A549 transcriptomic vectors.
5. Discordance interpretation against drug-target annotations and known polypharmacology, with a worked focal-compound family vignette (likely EGFR inhibitors, ~12 Tahoe-overlap drugs).
6. Polished public repo: clean notebooks, figures, paper-style writeup, two HF dataset pushes (CC0 stack: B3b + B3c outputs; rxrx3-EULA-respecting separate dataset for B3a outputs).

## Long-term goals (v1+, opportunistic)

- **Gene-perturbation cross-modality extension**, the v0 framework rerun on Replogle 2022 K562 Perturb-seq paired with CRISPR-KO Cell Painting from JUMP / PERISCOPE. Addresses the original CRISPR-vs-CRISPR question once drug-vs-drug is shipped. Dossier already drafted at `docs/datasets/replogle.md`.
- **Shared-latent contrastive model** aligning the two compound-embedding spaces; HF model checkpoint at `patrickjreed/cellduet-shared-latent`.
- **Multi-task probing** comparing modality-specific vs shared signal per drug class / target class.
- **HF Spaces Gradio demo**: enter a compound or gene, see its transcriptomic and morphological neighbors with concordance score. Live portfolio surface.
- **Arc Virtual Cell Challenge submission** if calendar aligns. Community-recognized benchmark credential.
- **Preprint or conference workshop submission** if v1 results justify it. Genuine publication, not just a portfolio piece.

## Honest gaps acknowledged

These are intentionally surfaced, not buried:

- Patrick has not previously published on perturb-seq or virtual cell modeling specifically. cellduet is an *extension* of established methodology to a new application area, not a claim of prior expertise. The README's "Related work" section cites the field's recent benchmarks and platforms so readers can locate cellduet in the active literature.
- v0 deliberately does not retrain encoders. This is a scope-discipline choice driven by Colab Free tier compute budget, not a methodology limitation. The question of whether transcriptomic and morphological readouts agree is well-posed in the embedding space alone. v1 may add encoder-side work if results justify it.
- **The morphological readouts come from multiple publicly released encoders** (CellProfiler hand-engineered features, cpcnn EfficientNet-B0, Recursion's OpenPhenom and Phenom-1/2). Each encoder reflects its own choices about what is informative. The three-arm v0 design is specifically structured so that cross-encoder agreement (B3b CellProfiler vs B3a Phenom) is itself one of the things being tested, not assumed.
- **Cell-context mismatch is the central caveat in the v0 primary arm.** Tahoe's 50 cancer cell lines are pooled per drug on the transcriptomic side; JUMP cpg0016 is U2OS-only on the morphological side. The B3a robustness arm (Tahoe vs HUVEC) widens this gap further; the B3c sanity arm (Tahoe-A549 × CPJUMP1-A549) collapses it. The three arms together make the cell-context question empirical rather than rhetorical.
- **Drug-target annotations on Tahoe-100M are GPT-4o-derived** and validated against MedChemExpress, not curated by domain experts. For the writeup's interpretive layer (target-deconvolution / polypharmacology framing), individual claims about specific drugs need DrugBank / ChEMBL cross-checks before publication.
- **Drug-phenotype cross-modality concordance has prior work** (Subramanian et al. 2017 L1000 vs Cell Painting, Recursion's internal benchmarks). cellduet's novelty is in the dataset stack (Tahoe-100M scRNA-seq + JUMP cpg0016 / Phenom Cell Painting are 2025–2026 releases), the three-arm probing design, and the discordance-as-signal framing rather than agreement-only.
- **Recursion rxrx3-core ships under a bespoke EULA with a hard neuroscience carve-out**, so the v0 writeup cannot be framed as neuroscience research. Disease anchor is oncology, by composition (Tahoe is a cancer-line panel) and by license-policy compatibility.

## Source documents

For Claude Code instances and future-Patrick alike, the strategic reasoning behind this project is grounded in these documents (paths assume the standard `~/Sandbox` and `~/NewRoleEfforts` layout):

- `~/NewRoleEfforts/docs/portfolio_project_brainstorm.md` — original 2026-04-15 portfolio gap analysis (72 postings)
- `~/NewRoleEfforts/PatrickReed_Master_Resume.md` — gold-standard claims source for any prose about Patrick's prior work
- `~/NewRoleEfforts/PatrickReed_Accomplishments_Bank.md` — extended detail on BMS, Ionis, DNAtrix, Salk projects
- `~/NewRoleEfforts/PatrickReed_Claims_Audit.md` — claims flagged for revision (consult before writing about prior work)
- `~/NewRoleEfforts/PatrickReed_Writing_Style.md` — voice rules (no em-dashes, banned cliches, signature-phrase rotation)
- `~/NewRoleEfforts/cover_letter/evidence_bank.yaml` — reusable project vignettes (NeuroPainting, AMP-PD scGPT, ALS T-cell atlas, etc.)
