# CLAUDE.md — context for Claude Code sessions in this repo

This file seeds the next Claude Code session with project context that isn't obvious from the code or README alone. Read this before doing meaningful work.

## What this repo is

`cellduet` is a portfolio research artifact authored by Patrick J. Reed, Ph.D. (computational biologist, 15+ years; recent Principal Scientist at Bristol Myers Squibb). The project tests whether perturbation phenotypes converge across **transcriptomic** (Tahoe-100M / Arc Virtual Cell Atlas) and **morphological** (Recursion RxRx3 / Phenom embeddings) readouts of the same gene-level CRISPR perturbations.

The artifact is positioned for senior IC roles at:
- **Anthropic** — Applied AI Engineer, Life Sciences (live JD); Research Scientist, Life Sciences (when reposted)
- **Xaira Therapeutics**, **Recursion**, **Insitro**, **Arc Institute** and adjacent academic / bio-AI startups
- General "perturb-seq + multimodal foundation model" credentialing

See `README.md` for the public-facing research framing.

## Hard scope discipline

These constraints exist because the project must be shippable in 4–6 weeks of evening work, on a single workstation, by one person. Violate them only after explicit user approval.

- **Use pre-computed embeddings.** Do NOT retrain encoders from raw images (RxRx3 ≈ 5–10 TB) or raw counts. Tahoe-100M and RxRx3 Phenom features are publicly available on the Arc Virtual Cell Atlas and HuggingFace respectively. The interesting research question lives in the embedding-space comparison, not in the encoders.
- **No encoder training in v0.** A v1 stretch may include a small shared-latent contrastive model on top of frozen embeddings; full encoder training is out of scope for the foreseeable future.
- **Lean module architecture.** Do not pre-create empty `data/`, `embeddings/`, `analysis/` Python packages until there is real code to put in them. Module structure should emerge from working code, not be designed up-front.

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
- Notebooks live in `notebooks/`, named with a `NN_short_description.ipynb` convention. Notebook outputs are gitignored; check in clean cells.
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

Rough order; revisit as work proceeds:

1. **Data exploration**: gene-perturbation overlap between Tahoe-100M and RxRx3. Notebook output drives whether v0 is feasible (need ≥ ~500 overlapping genes for meaningful concordance analysis).
2. **Per-gene transcriptomic phenotype embedding** from Tahoe-100M perturbation effects (pseudobulk DE or direct foundation-model embeddings).
3. **Per-gene morphological phenotype embedding** from RxRx3 Phenom features (gene-level aggregation across replicates and cell types).
4. **Pairwise distance matrices** within each modality.
5. **Cross-modality correlation analysis**: do transcriptomic distances correlate with morphological distances? Mantel test or similar.
6. **Convergent perturbation detection**: rank genes by cross-modality concordance; surface top concordant + top discordant cases with biological interpretation.
7. **Repo polish**: notebooks, figures, writeup. Ship.

Stretch (v1+):

- Shared-latent contrastive model aligning the two embedding spaces
- Multi-task probing comparing modality-specific vs shared signal per gene class
- Submit to next Arc Virtual Cell Challenge

## Status

Scaffold only. No code yet. README + pyproject + license + gitignore + version pin. Initial commit on `main`.
