# cellduet — first-time setup

One-time setup for the three external services this project uses: GitHub (code), Hugging Face Hub (artifacts), Google Colab (compute).

After this is done once, see the "Per-session checklist" at the bottom for the day-to-day flow.

## Execution model

```
Edit locally (VS Code)
        │
        │  git push
        ▼
GitHub  ──────────────────►  Colab notebook
(cellduet repo)              (clones repo on each session)
                                       │
                                       │  push trained artifacts /
                                       │  derived datasets
                                       ▼
                              Hugging Face Hub
                              (datasets/, models/, spaces/)
```

Code is local. Execution is on Colab. Artifacts persist on Hugging Face. GitHub is the coordinator.

## 1. GitHub (code repository)

Assumed already done. The repo lives at `https://github.com/PatrickJReed/cellduet` (push when ready). Locally:

```bash
cd ~/Sandbox/cellduet
git remote -v   # should show origin pointing at github.com/PatrickJReed/cellduet
```

If not yet pushed:

```bash
gh repo create PatrickJReed/cellduet --public --source=. --remote=origin --push
```

## 2. Hugging Face Hub (artifact store)

### Create the account

1. Sign up at [huggingface.co/join](https://huggingface.co/join). Use `patrickjreed` (or similar) for parity with your GitHub identity.
2. Confirm email, fill out the profile (name, affiliation, links to GitHub + LinkedIn). The HF profile is part of your portfolio surface.

### Generate an access token

1. Go to [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens).
2. Click **"New token"**.
3. Name: `cellduet-laptop` (or `cellduet-colab` if you'd rather scope by venue).
4. Type: **Write** (you'll be uploading datasets and models, not just reading).
5. Copy the token (`hf_...`). You'll only see it once. Store it in a password manager.

### Local CLI auth

```bash
pip install --upgrade huggingface_hub
huggingface-cli login
# paste the hf_... token when prompted
huggingface-cli whoami   # confirms it cached correctly
```

The token is now in `~/.cache/huggingface/token`.

### Programmatic upload pattern (for reference, not needed yet)

```python
from huggingface_hub import HfApi

api = HfApi()
api.create_repo(repo_id="patrickjreed/cellduet-pergene-embeddings", repo_type="dataset")
api.upload_folder(
    folder_path="./local_artifacts/embeddings",
    repo_id="patrickjreed/cellduet-pergene-embeddings",
    repo_type="dataset",
)
```

## 3. Google Colab (compute runtime)

### First-time activation

1. Visit [colab.research.google.com](https://colab.research.google.com) and sign in with the Google account you want associated with this work. This account also gets ~15 GB of free Drive for persistent caching.
2. Open a blank notebook to seed your account.
3. **Verify GPU access**: `Runtime → Change runtime type → T4 GPU → Save`. In a code cell, run `!nvidia-smi`. You should see a Tesla T4 with ~15 GB VRAM. (Free-tier GPUs are quota-limited; if you don't get one, retry in a few hours.)
4. **Verify Drive mount**:

   ```python
   from google.colab import drive
   drive.mount('/content/drive')
   ```

   First run pops up an OAuth flow. Approve. After mount, `/content/drive/MyDrive/` is writable and persistent.

### Set up Colab secrets (for HF token)

So you don't paste the token into notebook source:

1. In any Colab notebook, click the **🔑 key icon** in the left sidebar.
2. **+ Add new secret**: name `HF_TOKEN`, value the `hf_...` token from step 2.
3. Toggle **Notebook access** on for the cellduet repo notebooks.

In notebook code:

```python
from google.colab import userdata
from huggingface_hub import login
login(token=userdata.get('HF_TOKEN'))
```

### Free tier constraints to remember

- **Session limit**: ~12 hours max, ~90 min idle disconnect. Save artifacts to Drive or HF before they evaporate.
- **GPU quota**: heavy use → throttled to CPU. Pace your work; don't run tight training loops back-to-back.
- **Disk**: `/content` is ~100 GB but ephemeral. `/content/drive/MyDrive/` is ~15 GB and persistent.
- **RAM**: ~12–13 GB. Watch out on Tahoe-100M loads; use chunked / per-gene aggregation, not whole-dataset RAM loads.

If v0 hits the free-tier wall: **Colab Pro at $10/mo** gives priority GPU and ~24-hr sessions. Worth flagging if you find yourself disconnecting mid-analysis.

## 4. VS Code workflow

The cleanest pattern for editing Python code locally and executing on Colab:

1. **Edit `src/cellduet/*.py` and notebooks in VS Code locally.** Use the Jupyter extension to scratch-test cells against a local kernel where it's lightweight.
2. **Commit and push to GitHub** (`git add ... && git commit && git push`).
3. **Open the notebook on Colab** via:

   ```
   https://colab.research.google.com/github/PatrickJReed/cellduet/blob/main/notebooks/00_environment_smoke.ipynb
   ```

   Or click the "Open in Colab" badge that lives at the top of each notebook in the repo (template in `notebooks/00_environment_smoke.ipynb`).
4. **Each Colab notebook starts by reinstalling cellduet from GitHub** so it always pulls the latest:

   ```python
   !pip install -q git+https://github.com/PatrickJReed/cellduet.git@main
   ```

5. **Notebook outputs / figures** that you want preserved go to Drive (`/content/drive/MyDrive/cellduet/`) or HF Hub. Don't rely on `/content/` surviving the session.

VS Code has a Colab-integration extension, but the GitHub-mediated flow above is more reliable than direct VS Code → Colab kernel connection.

## Per-session checklist

Once everything above is done, the per-session ritual is:

```
Local (VS Code):
  [ ] git pull          # in case Colab edits got pushed back
  [ ] edit code/notebook
  [ ] git add + commit + push

Colab:
  [ ] open notebook from github.com/PatrickJReed/cellduet
  [ ] Runtime → T4 GPU (if applicable)
  [ ] run notebook from top: install cell, HF login cell, Drive mount cell, work cells
  [ ] save artifacts to Drive AND/OR push to HF Hub before disconnect
```

## Known sharp edges

- **Colab and the VS Code Jupyter extension don't share kernel state.** Switching between local-VS-Code-execution and Colab-execution requires you to re-run setup cells. Keep heavy work on Colab; use local VS Code for light scratch only.
- **`pip install git+...` is slow** (~30–60 s per session). Acceptable; cache once per session.
- **HF Hub free tier** has a soft 100 GB total storage cap. v0 artifacts are MB-scale, so this is not a near-term issue. v1 contrastive-model checkpoints could push toward GB; still well under cap.
- **Drive's 15 GB free quota** can fill if you cache raw embeddings. Aggregate to per-gene level early; raw datasets stay on HF (streamed) or Arc Virtual Cell Atlas (web-pulled).
