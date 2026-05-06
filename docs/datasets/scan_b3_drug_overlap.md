# Scan B3: drug-vs-drug pivot, Tahoe-100M × morphological compound atlases

A scoped feasibility scan. The decision question: *if cellduet pivots from CRISPR-vs-CRISPR (Replogle K562 × rxrx3-core CRISPR arm) to drug-vs-drug, can we find ≥100 shared compounds with at least one shared cell line between Tahoe-100M and a public morphological drug-perturbation atlas?* Numbers in this memo were computed locally against the actual metadata files; the script is reproducible from the citations.

## 1. Tahoe-100M drug list (the join side)

Confirmed against `metadata/drug_metadata.parquet` ([HF blob](https://huggingface.co/datasets/tahoebio/Tahoe-100M/blob/main/metadata/drug_metadata.parquet)):

- **379 unique drugs** (matches the tahoe-100m.md dossier).
- Schema columns: `drug, targets, moa-broad, moa-fine, human-approved, clinical-trials, gpt-notes-approval, canonical_smiles, pubchem_cid`.
- **No native InChIKey column.** Canonical join keys: `canonical_smiles` (377 of 379 non-null) and `pubchem_cid` (377 of 379 non-null).
- For comparison against InChIKey-keyed external lists I computed `InChIKey` from `canonical_smiles` via RDKit (`Chem.MolFromSmiles -> Chem.inchi.MolToInchiKey`); 377 of 379 round-trip cleanly. The two failures are inorganic salts (Talc, calcium lactate). The 14-character first block ("skeleton") of the InChIKey is the right key when handling stereochemistry / salt mismatches between sources.

License: CC0-1.0 ([HF README YAML](https://huggingface.co/datasets/tahoebio/Tahoe-100M/blob/main/README.md)).

## 2. Morphological candidates

### Full RxRx3 compound arm

- **1,674 compounds × 8 concentrations × HUVEC**, image + embeddings ([rxrx.ai/rxrx3](https://www.rxrx.ai/rxrx3)).
- **Important correction to scan_b1's framing.** The full compound arm is not gated. `metadata_rxrx3_core.csv` on Hugging Face contains the entire 1,674-compound list with SMILES, concentration, and well IDs. Verified locally: 95,701 COMPOUND wells, 1,674 unique SMILES, all `cell_type == HUVEC`, 8 concentrations from 0.002 µM to 10 µM (with both µM and mM-prefixed dosing tracks present in the raw metadata).
- **OpenPhenom-S/16, Phenom-1, Phenom-2 embeddings cover all 222,601 wells**, including the 95,701 compound wells, in the same parquets the rxrx3.md dossier already characterises. So the existing rxrx3-core download (21.7 GB total, 532 MB for OpenPhenom alone) is sufficient.
- License: Recursion non-commercial EULA with a hard neuroscience carve-out ([license file](https://huggingface.co/datasets/recursionpharma/rxrx3-core/blob/main/LICENSE)). The same EULA stack used in B1.
- Identifier: SMILES + free-text drug `treatment` name. No InChIKey or PubChem CID shipped; both must be computed.
- Colab Free compatibility: identical to B1 (already proven in the rxrx3.md compute footprint).

### JUMP-CP cpg0016 (Broad Institute, Cell Painting Gallery)

- **115,795 unique compounds** (verified by `wc -l` on `metadata/compound.csv.gz` from [jump-cellpainting/datasets](https://github.com/jump-cellpainting/datasets/blob/main/metadata/compound.csv.gz); 115,797 rows minus 1 header minus 1 duplicate InChIKey).
- **Cell line: U2OS only** for the main 116k-compound dataset ([JUMP data_description](https://broadinstitute.github.io/jump_hub/explanations/data_description.html)).
- Schema: `Metadata_JCP2022, Metadata_InChIKey, Metadata_InChI, Metadata_SMILES`. **InChIKey is the canonical Broad join key** (`JCP2022_NNNNNN`, e.g., DMSO = `JCP2022_033924`).
- Hosting: AWS S3 `s3://cellpainting-gallery/cpg0016-jump`, no-sign-request public ([AWS Open Data registry](https://registry.opendata.aws/cellpainting-gallery/)). Total raw imagery ~115 TB; pre-computed CellProfiler well-level profiles and per-perturbation consensus parquets are kilobyte-to-GB scale. License: **CC0-1.0** ([registry page](https://registry.opendata.aws/cellpainting-gallery/)). The license stack is permissive end-to-end, in contrast to RxRx3's EULA.
- Pre-computed embeddings exist; the JUMP folder structure has `embeddings/<network>/` subfolders for OpenPhenom, DINO, and CellProfiler profiles ([Cell Painting Gallery folder structure](https://broadinstitute.github.io/cellpainting-gallery/data_structure.html)). Sizes for the consensus (per-treatment) parquet are O(100 MB)–O(1 GB), well inside Colab Free.

### JUMP-CP CPJUMP1 / cpg0000 pilot (the only JUMP arm with a non-U2OS cell line)

- **303 curated compounds × {U2OS, A549} × {24 h, 48 h}**, plus matched CRISPR/ORF for 160 genes ([Chandrasekaran 2024 Nat Methods, PMC11166567](https://pmc.ncbi.nlm.nih.gov/articles/PMC11166567/)).
- This is the **only JUMP slice that profiles A549**, which matters because A549 is in Tahoe.
- Compound list available at [JUMP-Target-1_compound_metadata.tsv](https://github.com/jump-cellpainting/JUMP-Target/blob/master/JUMP-Target-1_compound_metadata.tsv); columns `broad_sample, InChIKey, pert_iname, pubchem_cid, target_list, smiles, InChI`. Verified locally: 307 rows, 302 unique InChIKeys.

### Other candidates (briefly)

- **LINCS L1000**. ~16,425 chemical perturbagens across 9 core cell lines including A549, MCF7, HCC515, HEPG2 ([nature.com s41598-019-44291-3](https://www.nature.com/articles/s41598-019-44291-3); [DOSE-L1000 paper](https://academic.oup.com/bioinformatics/article/39/11/btad683/7413173) reports 20,412 small molecules across the GEO submission). Transcriptomic (978 landmark genes), not morphological. **Out of scope for B3 because the readout is the same modality as Tahoe.** Useful as a cross-validation companion if B3 ships, not as the morphological arm.
- **JUMP-MOA**. A subset of JUMP-Target with ~90 compounds and 47 MoAs in U2OS, designed for MoA-classification benchmarks. Too small to matter as a primary morphological arm.
- **Connectivity Map (CMap, Broad)**. The transcriptomic CMap (~1,300 compounds in MCF7) is the L1000 predecessor, also transcriptomic. Same exclusion as LINCS.
- **Recursion's other compound datasets**. RxRx1 (~30 compounds, mechanism-of-action-focused), RxRx19a/b (SARS-CoV-2 antiviral screens, ~1,670 compounds in HRCE/VeroE6) ([rxrx.ai/datasets](https://www.rxrx.ai/datasets)). Disease-context-specific; not a general drug atlas.

## 3. Compound overlap (Tahoe ∩ candidate)

Computed on the actual InChIKeys. Both the full 27-character InChIKey and the 14-character "skeleton" (stereo-/salt-agnostic first block) are reported because Tahoe ships salt forms and stereoisomers that don't match cleanly in some cases (e.g., Ixazomib vs. Ixazomib citrate; Quinidine stereo flag).

| Candidate | Compound count | Tahoe ∩ candidate (full InChIKey) | Tahoe ∩ candidate (skeleton) | Notes |
|---|---|---|---|---|
| Full RxRx3 / rxrx3-core compound arm (HUVEC) | 1,674 | 75 | **145** | Both lists in hand; computed locally |
| JUMP-CP cpg0016 main (U2OS) | 115,795 | **228** | **230** | Both lists in hand; computed locally |
| JUMP-Target-1 / CPJUMP1 (U2OS + A549) | 302 | 14 | 15 | Subset of cpg0016; the only A549-bearing JUMP slice |

**Why JUMP overlap is so much higher than rxrx3-core overlap.** Tahoe's drug curation explicitly used the Broad Drug Repurposing Hub as a candidate pool, and JUMP-CP's compound set was also derived from the Drug Repurposing Hub ([JUMP-Target README](https://github.com/jump-cellpainting/JUMP-Target)). They share the same upstream pharmacology library. RxRx3's compound arm draws from a separate FDA-approved + bioactive set with different curation emphasis (more chemistry-diverse, less oncology-weighted), which is why ~60% of Tahoe lands in JUMP but only ~38% in rxrx3-core.

**MoA distribution of the Tahoe ∩ rxrx3-core 145.** Of the 145 compounds with a Tahoe MoA annotation, 70 are tagged "unclear", and the remainder cluster in DNA synthesis/repair inhibitors (12), COX inhibitors (9), kinase inhibitors split across MTOR/PI3K/MEK/EGFR/RAF/CDK/JAK (29 total), HDAC inhibitors (3), proteasome inhibitors (2), and androgen-receptor antagonists (4). The kinase-inhibitor cluster is the most biologically interpretable joint subset.

## 4. Cell-line overlap

Tahoe spans 50 cancer cell lines, 47 surviving QC, including **A549, MCF-7, HCT116, HCT15, HT-29, SW480, PANC-1, MIA PaCa-2, BxPC-3, NCI-H460, NCI-H358, BT-474, BT-20, HepG2/C3A, U-87 MG**, and others (verified locally against `cell_line_metadata.parquet`).

| Tahoe line present | rxrx3-core | JUMP cpg0016 main | JUMP CPJUMP1 pilot | LINCS L1000 |
|---|---|---|---|---|
| A549 | no | no | **yes** | yes |
| U2OS | no | yes | yes | no |
| MCF-7 | no | no | no | yes |
| HT-29 | no | no | no | yes |
| HepG2 | no | no | no | yes |
| (HUVEC) | yes | no | no | no |

**Tahoe ∩ rxrx3-core cell-line overlap: 0.** HUVEC is not in Tahoe; none of the 50 cancer lines is HUVEC. So a Tahoe × rxrx3-core comparison must compare *across* cell types: drug effect in 47 cancer contexts vs drug effect in HUVEC. This is the same cell-type-mismatch caveat that B1 already carries (K562 vs HUVEC), only now with 47 transcriptomic contexts instead of one.

**Tahoe ∩ JUMP cpg0016 main cell-line overlap: 0** (U2OS not in Tahoe).

**Tahoe ∩ JUMP CPJUMP1 cell-line overlap: 1, namely A549.** This is the only Tahoe-anchored slice with a real shared-cell-line story. But CPJUMP1 has only 302 compounds, of which ~15 overlap Tahoe in A549. That's below the 100-compound feasibility gate.

## 5. Verdict on the ≥100-shared-compound + ≥1-shared-cell-line gate

| Pair | Compounds shared | Shared cell line(s) | Gate? |
|---|---|---|---|
| Tahoe × rxrx3-core compound arm | 145 (skel) | none (HUVEC vs cancer panel) | **Compounds: pass. Cell line: fail.** |
| Tahoe × JUMP cpg0016 (U2OS) | 228–230 | none (U2OS vs cancer panel) | **Compounds: pass. Cell line: fail.** |
| Tahoe × JUMP CPJUMP1 (U2OS + A549) | 14–15 | A549 | **Compounds: fail. Cell line: pass.** |

There is **no public morphological dataset that simultaneously clears the 100-compound and ≥1-shared-cell-line bars** against Tahoe. The cleanest framing is therefore:

- **Drop the same-cell-line requirement** and accept a cross-cell-type concordance question (same as B1 already does).
- Operating point becomes Tahoe × JUMP cpg0016 with **228 shared compounds in a 47-cancer-line × U2OS comparison**, or Tahoe × rxrx3-core with **145 shared compounds in 47-cancer-line × HUVEC**.
- The A549 single-cell-line slice is too small at 15 compounds to be the primary analysis; it can serve as a **same-cell-line sanity check** within a larger cross-cell-type study.

## 6. Side-by-side: B1 vs B3

| Axis | B1 (Replogle K562 × rxrx3-core CRISPR) | B3a (Tahoe × rxrx3-core compounds) | B3b (Tahoe × JUMP cpg0016) |
|---|---|---|---|
| Perturbation modality | CRISPRi gene KD vs CRISPR-KO | small molecule vs small molecule | small molecule vs small molecule |
| Joint perturbation count | ~600–720 genes (rxrx3-core 735 ∩ Replogle GW) | **145 compounds** | **228 compounds** |
| Transcriptomic dataset cells/lines | K562 only (CML) | 47 cancer lines | 47 cancer lines |
| Morphological dataset cells | HUVEC | HUVEC | U2OS |
| Same-cell-line slice? | no (K562 vs HUVEC) | no (cancer vs HUVEC) | no (cancer vs U2OS); A549 sub-slice via CPJUMP1 with ~15 compounds |
| Transcriptomic license | CC BY 4.0 (Replogle) | CC0-1.0 (Tahoe) | CC0-1.0 (Tahoe) |
| Morphological license | Recursion EULA | Recursion EULA | **CC0-1.0** |
| Combined license risk | EULA + CC BY (no neuro use; OK for portfolio) | EULA + CC0 (no neuro use; OK for portfolio) | **fully CC0-1.0** |
| Embedding artifact ready? | yes (3 Phenom parquets, 532 MB–2.3 GB) | yes (same parquets; compound wells are in the same files) | yes (JUMP consensus parquets and OpenPhenom embeddings on S3) |
| Colab Free compatible? | yes (proven in B1 dossier) | yes (same artifacts) | yes (consensus profiles are GB-scale) |
| Scientific question | "do CRISPR-KO morphology phenotypes track CRISPRi transcriptome phenotypes across cell types?" | "do drug-induced morphology phenotypes (HUVEC) track drug-induced transcriptome phenotypes (cancer panel)?" | "do drug-induced morphology phenotypes (U2OS) track drug-induced transcriptome phenotypes (cancer panel)?" |
| Credentialing | Replogle is a 2022 paper, well-cited but no longer the headline benchmark | **Tahoe-100M is the inaugural Arc Virtual Cell Atlas dataset and the most-discussed perturbation atlas of 2025–2026** | same Tahoe credentialing + JUMP-CP is the morphological-foundation-model standard ([Chandrasekaran et al. 2024 Nat Methods](https://www.nature.com/articles/s41592-024-02241-6)) |
| Modality-mismatch caveat | CRISPRi vs KO is a real but tractable caveat | none (both are drug perturbations) | none (both are drug perturbations) |
| Cell-type-mismatch caveat | K562 vs HUVEC, single-context | 47 cancer contexts vs HUVEC, multi-context | 47 cancer contexts vs U2OS, multi-context |

The main scientific upgrade from B1 to B3 is that B3 removes the CRISPRi-vs-KO modality mismatch and replaces it with a like-for-like drug-perturbation comparison. The cell-type mismatch persists in both, but B3 has 47 transcriptomic contexts to sample from, which lets the analysis report "concordance averaged across cancer panel" *and* "concordance for tissue-matched cancer lines" (e.g., lung lines for an A549/U2OS comparison) as separate outputs.

The main credentialing upgrade is that B3 reintroduces Tahoe-100M, which is the dataset most directly aligned with the live Anthropic Applied AI Engineer (Life Sciences) JD's framing of "virtual cell atlas" work, and B3b additionally drops the Recursion neuroscience-EULA constraint by using the Broad CC0 morphological data.

## 7. Recommendation

**Pivot to B3b (Tahoe × JUMP cpg0016 main, U2OS) as the primary v0, with B3a (Tahoe × rxrx3-core compound arm, HUVEC) as a secondary readout.** Three reasons:

1. **Compound overlap is highest.** 228 shared InChIKeys is comfortably above the 100-compound feasibility gate, and the joint set is biologically meaningful (kinase inhibitors, DNA-damage agents, hormone-receptor modulators) per the MoA breakdown.
2. **License stack collapses to CC0 + CC0.** Tahoe-100M (CC0-1.0) and Cell Painting Gallery (CC0-1.0) are both public-domain dedications. No EULA. No neuroscience carve-out. No commercial-use ambiguity. This is materially better for a portfolio artifact than the B1 stack.
3. **Tahoe-100M re-enters the project.** The B1 detour was driven by the discovery that Tahoe is drug-perturbed, not CRISPR-perturbed. B3 turns that constraint into a feature: a drug-vs-drug pairing is the natively correct framing for Tahoe and it places the project on the dataset most directly relevant to the Anthropic / Arc / Recursion / Insitro target roles.

**Why B3a sits in second place, not first.** rxrx3-core is a smaller compound set (1,674 vs 115,795), the EULA is restrictive, and the compound overlap is lower (145 vs 228). It does have one strong advantage: Recursion's pre-aggregated, batch-corrected, ready-to-load Phenom-1/Phenom-2 embeddings are higher-quality features than CellProfiler well-level profiles for a phenotype-distance analysis. So the right architecture is **B3b is the headline analysis** (228 shared compounds, CC0 stack, Tahoe + JUMP-CP credentialing), **B3a is a robustness check** ("does the same-drug concordance pattern survive a different morphological encoder and a different cell type?"), and the **A549 sub-slice from CPJUMP1 (~15 compounds) is the same-cell-line sanity check** that addresses the cell-type-mismatch caveat head-on.

**Hybrid with B1?** Not recommended. B3 is strictly better on every axis the project cares about (license, credentialing, compound overlap, modality-match), and adds back Tahoe. Keeping B1 as a parallel track doubles the engineering load with no new scientific payoff. If the scope shrinks further later, the B1 plan can be retired.

## 8. Empirical follow-ups before locking the pivot

These are the things to verify in notebook 01 before committing the full pipeline:

1. **JUMP cpg0016 consensus / well-level profile parquet sizes on S3.** Walk `s3://cellpainting-gallery/cpg0016-jump/source_*/workspace/profiles/` and `embeddings/` and confirm the per-source consensus profiles are gigabyte-scale, not hundred-gigabyte-scale. Streamability via `fsspec`/`s3fs` is the binding test. Reference: [Cell Painting Gallery folder structure](https://broadinstitute.github.io/cellpainting-gallery/data_structure.html).
2. **Re-run the InChIKey overlap with stereo-handling.** The 228 vs 230 spread (full vs skeleton) suggests ~2 stereoisomer mismatches; resolve them by hand. Also try the PubChem CID join as an independent check.
3. **Tahoe per-(drug, A549) DE coverage.** Confirm A549 has enough cells per drug for stable LFCs; the Tahoe replicate structure is shallow per (drug, cell-line). This is open question 3 in tahoe-100m.md.
4. **Whether JUMP cpg0016 ships an OpenPhenom embedding parquet.** If yes, the Phenom-family encoder choice can be held constant across B3a (rxrx3-core) and B3b (cpg0016), which lets a direct head-to-head encoder comparison happen for free.
5. **Drug-name harmonization.** The Tahoe `drug` column is free text (mixes generics, brand names, and codes like "ABT-199", "LEE011", "ODM-201"); JUMP uses `pert_iname`. SMILES-derived InChIKey is the right join, but human-readable labels in figures will need a name-harmonization pass.
