# CLAUDE.md — context for Claude Code sessions in this repo

This file seeds the next Claude Code session with project context that isn't obvious from the code or README alone. Read this before doing meaningful work.

For the **strategic background** behind the project (why it exists, project-selection rationale, dataset rationale, role-class positioning, connection to prior work, short- and long-term goals, honestly-acknowledged gaps), read `docs/CONTEXT.md`. This file (`CLAUDE.md`) is for *how to work in the codebase*; `docs/CONTEXT.md` is for *why the codebase exists*.

## What this repo is

`cellduet` is a portfolio research artifact authored by Patrick J. Reed, Ph.D. (computational biologist, 15+ years; recent Principal Scientist at Bristol Myers Squibb). The project tests whether **small-molecule drug perturbation phenotypes** agree across transcriptomic (Tahoe-100M / Arc Virtual Cell Atlas) and morphological (JUMP-Cell Painting Consortium cpg0016 primary; Recursion rxrx3-core robustness arm with Phenom embeddings; CPJUMP1 same-cell-line sanity check) readouts. v0 is a three-arm design joined on full InChIKey: 228 shared compounds in B3b primary, 145 in B3a robustness, 14 in B3c sanity. v1 extends the framework to gene-perturbation cross-modality (Replogle 2022 Perturb-seq paired with CRISPR-KO Cell Painting from JUMP / PERISCOPE).

The artifact is positioned for senior IC roles at:
- **Anthropic** — Applied AI Engineer, Life Sciences (live JD); Research Scientist, Life Sciences (when reposted)
- **Xaira Therapeutics**, **Recursion**, **Insitro**, **Arc Institute** and adjacent academic / bio-AI startups
- General "perturb-seq + multimodal foundation model" credentialing

See `README.md` for the public-facing research framing.

## Execution model

This repo is **code-local, execution-Colab, artifacts-HF, coordination-GitHub**:

```
VS Code (local)  →  git push  →  GitHub  →  Colab notebooks (clone + execute)  →  HF Hub (artifacts)
```

- **Code lives locally** and is edited in VS Code (Patrick's editor).
- **Execution happens on Google Colab Free tier** (T4 GPU, ~12 GB RAM, ~12-hr session limit, ~15 GB Drive for persistent cache). Heavy compute does not run on the local machine.
- **Each Colab notebook reinstalls `cellduet` from GitHub** at the top: `!pip install -q git+https://github.com/PatrickJReed/cellduet.git@main`. This forces the Python package to be self-contained and installable; no ad-hoc local-path coupling.
- **Artifacts persist on Hugging Face Hub** (account: `patrickjreed`). Aggregated embeddings → HF datasets. Trained models (v1) → HF models. Optional Gradio demo → HF Spaces.
- **VS Code does not connect directly to Colab kernels.** The flow is GitHub-mediated: edit locally, push, open notebook on Colab, run.

Onboarding details: `docs/SETUP.md`.

## Hard scope discipline

These constraints exist because the project must be shippable in 4–6 weeks of evening work, on Colab Free tier, by one person. Violate them only after explicit user approval.

- **Use pre-computed embeddings and pseudobulk aggregates.** Do NOT retrain encoders from raw images (RxRx3 full release ~100 TB; JUMP-CP cpg0016 ~358 TB) or raw counts (Tahoe-100M ~337 GB). The morphology side ships pre-computed CellProfiler features (~737-d harmony-corrected, CC0), cpcnn EfficientNet-B0 features (672-d), and Phenom-family embeddings (OpenPhenom 384-d, Phenom-1 1024-d, Phenom-2 1664-d on rxrx3-core). The transcriptomic side ships streamable `pseudobulk_differential_expression` parquet plus drug/cell-line metadata. The interesting research question lives in the embedding-space comparison, not in the encoders.
- **No encoder training in v0.** A v1 stretch may include a small shared-latent contrastive model on top of frozen embeddings; full encoder training is out of scope for the foreseeable future.
- **Lean module architecture.** Do not pre-create empty `data/`, `embeddings/`, `analysis/` Python packages until there is real code to put in them. Module structure should emerge from working code, not be designed up-front.
- **Respect Colab Free tier constraints.** RAM (~12 GB), session length (~12 hr), idle disconnect (~90 min). Aggregate to per-compound level early; do not load full Tahoe-100M expression or full JUMP cpg0016 imagery. Stream the Tahoe pseudobulk parquet; pull only the harmony-corrected JUMP feature parquet (2.64 GB). Save intermediate artifacts to Drive (`/content/drive/MyDrive/cellduet/cache/`) AND/OR push to HF Hub before disconnect.
- **Don't run heavy compute locally.** If a notebook cell exceeds ~30 seconds or ~2 GB RAM on a laptop, that cell belongs on Colab. Local execution is for scratch + quick imports + iteration on logic.

## Voice and writing style

Patrick has explicit voice preferences captured at `/Users/patrickreed/NewRoleEfforts/PatrickReed_Writing_Style.md`. Read that file before writing any user-facing prose (README, blog posts, paper draft, commit messages). Highlights:

- **No em-dashes** as connectors. Use commas, parentheses, or sentence breaks.
- **No banned cliches**: "leverage", "robust", "seamless", "cutting-edge", "passionate about", "world-class", "state-of-the-art", "perfect fit", "I am writing to express", "Furthermore" / "Moreover" sentence openers.
- **Once-per-document rule** for signature phrases like "convergent" / "convergent evidence". Rotate to "concordant", "orthogonal lines of evidence", "multi-stream validation" if needed.
- **Demonstrate, don't state.** Specific numbers + named tools + concrete outcomes beat adjectives.
- **Honest framing.** Never invent metrics, never claim experience that doesn't exist. If a result is preliminary, say so. If a method has known caveats, name them.

## Coding conventions

- Python ≥ 3.10. Type hints encouraged but not enforced.
- Ruff for lint + format (`ruff check . && ruff format .`). Config in `pyproject.toml`.
- Build via `hatchling`. Editable install: `pip install -e ".[dev,torch]"`.
- Default to `numpy` + `pandas` + `scipy` + `scikit-learn` + `anndata` + `scanpy`. PyTorch only when there's actual model code (it's an optional extra).
- Notebooks live in `notebooks/`, named with a `NN_short_description.ipynb` convention. Each notebook starts with: (a) a markdown header with title + Open-In-Colab badge, (b) an `!pip install -q git+...cellduet.git@main` cell, (c) HF login cell (Colab Secret `HF_TOKEN`), (d) optional Drive mount cell, (e) work cells. Pattern is established in `notebooks/00_environment_smoke.ipynb` — copy that as the template.
- **Commit notebooks with cleared outputs** to keep diffs small and avoid leaking session-specific state. Use `Edit > Clear All Outputs` in Jupyter / VS Code, or `jupyter nbconvert --clear-output --inplace path/to/nb.ipynb` before commit.
- **Persistent caches** go to `/content/drive/MyDrive/cellduet/cache/` (Colab) or HF datasets, never to repo paths. Local development cache directory should be configurable, not hardcoded.
- One commit per coherent change; commit messages start with a short `scope:` prefix matching what's changing (e.g., `data:`, `analysis:`, `notebooks:`, `docs:`).

## What NOT to do

- Do **not** pre-architect a deep module hierarchy without code. Empty packages are technical debt.
- Do **not** add CI workflows, pre-commit hooks, or `tests/` scaffolding until there is something to test or run.
- Do **not** invent or estimate metrics. Every number in the README, paper draft, or blog must trace to an actual computation.
- Do **not** introduce a fifth dataset or scope expansion without surfacing the tradeoff to the user. v0 is four datasets: Tahoe-100M (transcriptomic backbone) plus JUMP-CP cpg0016 (morphological primary), rxrx3-core (robustness), and CPJUMP1 (same-cell sanity).
- Do **not** write multi-paragraph docstrings or extensive prose comments. One short line max.
- Do **not** create new top-level documentation files (`*.md`) without explicit ask. Edit `README.md` for public-facing changes; edit this file (`CLAUDE.md`) for Claude-context changes.
- Do **not** rewrite the README's "Author" or "Related work" sections without checking with Patrick first.

## Cross-references

- **Parent strategy doc**: `/Users/patrickreed/NewRoleEfforts/docs/portfolio_project_brainstorm.md` — original portfolio-project rationale (2026-04-15)
- **Voice rules**: `/Users/patrickreed/NewRoleEfforts/PatrickReed_Writing_Style.md`
- **Patrick's master resume**: `/Users/patrickreed/NewRoleEfforts/PatrickReed_Master_Resume.md` (gold-standard claims source)
- **Patrick's accomplishments bank**: `/Users/patrickreed/NewRoleEfforts/PatrickReed_Accomplishments_Bank.md` (extended detail)
- **Patrick's claims audit**: `/Users/patrickreed/NewRoleEfforts/PatrickReed_Claims_Audit.md` (flagged-for-revision claims; consult before writing about Patrick's prior work)

## v0 task list

Rough order; revisit as work proceeds. All compute steps run on Colab; results push to HF for persistence. The plan implements the **B3 three-arm design** documented in `docs/datasets/joint.md`. Compound-level joining throughout, on full InChIKey.

0. **Run `notebooks/00_environment_smoke.ipynb` on Colab** to confirm the runtime is good (GPU, HF login, Drive mount).
1. **Data exploration + intersection** (`notebooks/01_intersections.ipynb`): pull Tahoe drug list, JUMP cpg0016 compound metadata, rxrx3-core compound metadata, CPJUMP1 compound metadata. Compute and verify the InChIKey intersections (target: 228 / 145 / 14). Per-compound replicate-count histograms per arm. Push the joint compound manifest to HF as `patrickjreed/cellduet-compound-manifest`.
2. **Per-compound transcriptomic phenotype** (`notebooks/02_tahoe_percompound.ipynb`): stream Tahoe `pseudobulk_differential_expression`, plate-match to DMSO, aggregate to per-(drug, cell_line) LFC vectors over ~2,000 HVGs. Two products: `Tahoe-pooled` (379 × 2K) for B3b/B3a, and `Tahoe-A549` (~A549 drugs × 2K) for B3b cell-context probe + B3c. Push to HF dataset `patrickjreed/cellduet-tahoe-percompound`.
3. **Per-compound morphological phenotype, B3b primary** (`notebooks/03_jump_percompound.ipynb`): pull JUMP cpg0016 harmony-corrected feature parquet (2.64 GB). Filter to the 228 Tahoe-overlap InChIKeys. Aggregate per compound via pycytominer-style mean across replicates. Output: 228 × 737-d. Push to HF dataset `patrickjreed/cellduet-jump-percompound`. Optional cpcnn 672-d ablation.
4. **Per-compound morphological phenotype, B3a robustness** (`notebooks/04_rxrx3_percompound.ipynb`): pull rxrx3-core OpenPhenom-384 embeddings (532 MB). EFAAR-style TVN on EMPTY_control wells. Filter to 145 Tahoe-overlap (skeleton-InChIKey-matched) compounds. Per-compound mean. Output: 145 × 384-d. Optional Phenom-1/2 ablation.
5. **Per-compound morphological phenotype, B3c sanity** (`notebooks/05_cpjump1_percompound.ipynb`): pull CPJUMP1 CellProfiler features for the relevant A549 compound plates (~9 MB). Filter to compound-perturbation only (drop ORF/CRISPR), align per-plate feature schemas, aggregate per compound. Output: 14 × ~4,000 features. (No HF push for this small artifact unless useful.)
6. **Within-arm distance matrices + cross-modal concordance tests** (`notebooks/06_concordance.ipynb`): cosine distance per modality per arm. Mantel correlation, RV coefficient, per-compound neighborhood Jaccard with permutation null. B3b headline + B3a robustness + B3c direction-of-effect check. Tahoe-pooled vs Tahoe-A549 sensitivity column on B3b.
7. **Discordance interpretation + worked vignette** (`notebooks/07_interpretation.ipynb`): rank compounds by cross-modal concordance per arm; identify concordant + discordant clusters; characterize discordance against drug-target annotations and known polypharmacology; one focal compound family (likely EGFR inhibitors, ~12 Tahoe-overlap drugs) worked through end-to-end. Figures.
8. **Repo polish + writeup**: clean notebooks (cleared outputs), render to HTML for portfolio display, write a paper-style README extension or blog post. Ship.

Stretch (v1+):

- Extend to **gene-perturbation cross-modality** (Replogle 2022 K562 Perturb-seq × CRISPR-KO Cell Painting from JUMP / PERISCOPE); cellduet's CRISPR-vs-CRISPR sibling track. Dossier already drafted at `docs/datasets/replogle.md`.
- Shared-latent contrastive model aligning the two compound-embedding spaces; checkpoint to HF as `patrickjreed/cellduet-shared-latent`
- Multi-task probing comparing modality-specific vs shared signal per drug class / target class
- HF Spaces Gradio demo: enter a compound or gene, get its transcriptomic + morphological neighbors with concordance score
- Submit to next Arc Virtual Cell Challenge

## Status

Scaffold + planning artifacts. No analysis code yet. Files: `README.md`, `CLAUDE.md`, `pyproject.toml`, `LICENSE`, `.gitignore`, `src/cellduet/__init__.py`, `docs/SETUP.md`, `docs/CONTEXT.md`, `notebooks/00_environment_smoke.ipynb`, plus a full set of dataset dossiers and feasibility scans under `docs/datasets/` (Tahoe-100M, Replogle, rxrx3, JUMP cpg0016, CPJUMP1, joint B3 design, B2 + B3 scans). Multiple commits on `main` reflecting the dossier-driven pivot from a CRISPR-vs-CRISPR framing to the locked-in B3 drug-vs-drug three-arm design.
