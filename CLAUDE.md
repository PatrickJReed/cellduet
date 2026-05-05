# CLAUDE.md — context for Claude Code sessions in this repo

This file seeds the next Claude Code session with project context that isn't obvious from the code or README alone. Read this before doing meaningful work.

For the **strategic background** behind the project (why it exists, project-selection rationale, dataset rationale, role-class positioning, connection to prior work, short- and long-term goals, honestly-acknowledged gaps), read `docs/CONTEXT.md`. This file (`CLAUDE.md`) is for *how to work in the codebase*; `docs/CONTEXT.md` is for *why the codebase exists*.

## What this repo is

`cellduet` is a portfolio research artifact authored by Patrick J. Reed, Ph.D. (computational biologist, 15+ years; recent Principal Scientist at Bristol Myers Squibb). The project tests whether perturbation phenotypes converge across **transcriptomic** (Tahoe-100M / Arc Virtual Cell Atlas) and **morphological** (Recursion RxRx3 / Phenom embeddings) readouts of the same gene-level CRISPR perturbations.

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

- **Use pre-computed embeddings.** Do NOT retrain encoders from raw images (RxRx3 ≈ 5–10 TB) or raw counts. Tahoe-100M and RxRx3 Phenom features are publicly available on the Arc Virtual Cell Atlas and HuggingFace respectively. The interesting research question lives in the embedding-space comparison, not in the encoders.
- **No encoder training in v0.** A v1 stretch may include a small shared-latent contrastive model on top of frozen embeddings; full encoder training is out of scope for the foreseeable future.
- **Lean module architecture.** Do not pre-create empty `data/`, `embeddings/`, `analysis/` Python packages until there is real code to put in them. Module structure should emerge from working code, not be designed up-front.
- **Respect Colab Free tier constraints.** RAM (~12 GB), session length (~12 hr), idle disconnect (~90 min). Aggregate to per-gene level early; never load whole Tahoe-100M into RAM. Save intermediate artifacts to Drive (`/content/drive/MyDrive/cellduet/cache/`) AND/OR push to HF Hub before disconnect.
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
- Do **not** introduce a third dataset or scope expansion without surfacing the tradeoff to the user. v0 is two datasets: Tahoe-100M and RxRx3.
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

Rough order; revisit as work proceeds. All compute steps run on Colab; results push to HF for persistence.

0. **Run `notebooks/00_environment_smoke.ipynb` on Colab** to confirm the runtime is good (GPU, HF login, Drive mount).
1. **Data exploration** (`notebooks/01_data_exploration.ipynb`): pull Tahoe-100M metadata + RxRx3 metadata, enumerate the gene-perturbation overlap. Notebook output drives whether v0 is feasible (need ≥ ~500 overlapping genes for meaningful concordance analysis). Push the gene-overlap table to HF as a small dataset for reuse across later notebooks.
2. **Per-gene transcriptomic phenotype embedding** (`notebooks/02_tahoe_pergene.ipynb`): from Tahoe-100M perturbation effects (pseudobulk DE or direct foundation-model embeddings). Push embeddings to HF dataset `patrickjreed/cellduet-tahoe-pergene`.
3. **Per-gene morphological phenotype embedding** (`notebooks/03_rxrx3_pergene.ipynb`): from RxRx3 Phenom features (gene-level aggregation across replicates and cell types). Push to HF dataset `patrickjreed/cellduet-rxrx3-pergene`.
4. **Pairwise distance matrices** within each modality (`notebooks/04_distances.ipynb`). Pull both embedding datasets from HF; produce two distance matrices on the overlapping gene set.
5. **Cross-modality correlation analysis** (`notebooks/05_concordance.ipynb`): Mantel test, scatter of transcriptomic vs morphological distances, identification of concordant + discordant cases.
6. **Convergent perturbation detection + biological interpretation** (`notebooks/06_convergent.ipynb`): rank genes by cross-modality concordance; manually annotate top concordant + top discordant gene clusters; figures.
7. **Repo polish + writeup**: clean notebooks, render to HTML for portfolio display, write a paper-style README extension or blog post. Ship.

Stretch (v1+):

- Shared-latent contrastive model aligning the two embedding spaces; checkpoint to HF as `patrickjreed/cellduet-shared-latent`
- Multi-task probing comparing modality-specific vs shared signal per gene class
- HF Spaces Gradio demo: enter a gene, get its transcriptomic + morphological neighbors with concordance score
- Submit to next Arc Virtual Cell Challenge

## Status

Scaffold only. No analysis code yet. Files: `README.md`, `CLAUDE.md`, `pyproject.toml`, `LICENSE`, `.gitignore`, `src/cellduet/__init__.py`, `docs/SETUP.md`, `notebooks/00_environment_smoke.ipynb`. Two initial commits on `main`.
