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

- **Canonical perturbation-rich single-cell dataset.** Released 2025 on the Arc Virtual Cell Atlas; 250,000+ downloads as of early 2026.
- **Training/reference data for the major virtual-cell architectures** the field is converging on (STATE, Tahoe-x1, TranscriptFormer).
- **Active ecosystem.** The Tahoe + Arc + Biohub partnership announced in January 2026 is generating ~120M new perturbation data points across 225K drug-patient interactions; cellduet's analytical methods are designed to extend cleanly to that next-generation dataset.
- **Plugs into the Arc Virtual Cell Challenge.** Submitting to the next iteration is a v1 stretch.

### Recursion RxRx3 (morphological readout)

- **Canonical image-based CRISPR perturbation dataset.** Cell Painting fluorescence imaging across ~17K perturbed genes × multiple cell types.
- **Pre-computed Phenom embeddings publicly released** by Recursion on Hugging Face. This is what makes v0 tractable on Colab Free tier — the analytical question lives in the embedding space, not in retraining encoders.
- **Direct connection to Patrick's prior work.** At BMS, Patrick built a multi-task foundation-model proof-of-concept for the Neurobot HTS platform (Cerberus-inspired ResNet34 shared encoder, three task heads on the Broad NeuroPainting dataset) and drew on RxRx3 as a reference for image-based CRISPR perturbation modeling. cellduet is methodology continuation, not a new domain.

### Why both, and why concordance

Most published virtual-cell work focuses on transcriptomic-only readouts. The open question — *do transcriptomic and morphological perturbation phenotypes converge on the same biological program, and where do they diverge?* — has not been answered systematically at scale. It is also the natural extension of the **5-stream convergent-evidence target prioritization framework** Patrick has described in industry interviews (compositional, GWAS-conditioned, trajectory, regulatory, ligand-receptor): adding a sixth orthogonal stream of evidence, morphological perturbation phenotype, that is directly measured rather than inferred.

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

1. Establish the Tahoe-100M ↔ RxRx3 gene-perturbation overlap and confirm v0 is feasible (need ≥ ~500 overlapping genes).
2. Aggregate pre-computed embeddings to per-gene phenotype vectors in each modality.
3. Compute pairwise distance matrices within each modality.
4. Cross-modality concordance analysis (Mantel test, scatter, identification of concordant + discordant cases).
5. Worked-through biological interpretation of top concordant + top discordant gene clusters.
6. Polished public repo: clean notebooks, figures, paper-style writeup, HF datasets pushed for the per-gene embeddings.

## Long-term goals (v1+, opportunistic)

- **Shared-latent contrastive model** aligning the two embedding spaces; HF model checkpoint at `patrickjreed/cellduet-shared-latent`.
- **Multi-task probing** comparing modality-specific vs shared signal per gene class.
- **HF Spaces Gradio demo**: enter a gene, see its transcriptomic and morphological neighbors with concordance score. Live portfolio surface.
- **Arc Virtual Cell Challenge submission** if calendar aligns. Community-recognized benchmark credential.
- **Preprint or conference workshop submission** if v1 results justify it. Genuine publication, not just a portfolio piece.

## Honest gaps acknowledged

These are intentionally surfaced, not buried:

- Patrick has not previously published on perturb-seq or virtual cell modeling specifically. cellduet is an *extension* of established methodology to a new application area, not a claim of prior expertise. The README's "Related work" section cites the field's recent benchmarks and platforms (Perturb-Multimodal Cell 2025, Tahoe-100M, STATE) so readers can locate cellduet in the active literature.
- v0 deliberately does not retrain encoders. This is a scope-discipline choice driven by Colab Free tier compute budget, not by limitation of methodology — the question of whether transcriptomic and morphological readouts agree is well-posed in the embedding space alone. v1 may add encoder-side work if results justify it.
- The "morphological readout" comes from a publicly released embedding (Recursion's Phenom features) and reflects the encoder's choices about what is informative. Conclusions about cross-modality concordance depend on the quality of those features. This caveat is named explicitly in the writeup.

## Source documents

For Claude Code instances and future-Patrick alike, the strategic reasoning behind this project is grounded in these documents (paths assume the standard `~/Sandbox` and `~/NewRoleEfforts` layout):

- `~/NewRoleEfforts/docs/portfolio_project_brainstorm.md` — original 2026-04-15 portfolio gap analysis (72 postings)
- `~/NewRoleEfforts/PatrickReed_Master_Resume.md` — gold-standard claims source for any prose about Patrick's prior work
- `~/NewRoleEfforts/PatrickReed_Accomplishments_Bank.md` — extended detail on BMS, Ionis, DNAtrix, Salk projects
- `~/NewRoleEfforts/PatrickReed_Claims_Audit.md` — claims flagged for revision (consult before writing about prior work)
- `~/NewRoleEfforts/PatrickReed_Writing_Style.md` — voice rules (no em-dashes, banned cliches, signature-phrase rotation)
- `~/NewRoleEfforts/cover_letter/evidence_bank.yaml` — reusable project vignettes (NeuroPainting, AMP-PD scGPT, ALS T-cell atlas, etc.)
