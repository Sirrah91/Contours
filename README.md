# Solar Feature Contour Tracking

A Python framework for tracking, segmenting, and analysing evolving solar
features (sunspots and pores) using contour-based methods.

The code is intended for **scientific workflows**, with an emphasis on

- reproducibility,
- clear separation of concerns, and
- publication-quality visualisation.

This repository accompanies ongoing research and is primarily designed for
expert users working with solar image data.

---

## Main features

- Contour-based tracking of evolving solar features
- Phase segmentation (forming / stable / decaying)
- Statistical analysis of physical and geometrical quantities
- Modular plotting pipelines:
  - snapshot figures,
  - PDFs,
  - animations

---

## Repository structure (overview)

```
src/
├─ geometry/     # contour extraction and geometry utilities
├─ pipelines/    # tracking, statistics, and plotting pipelines
├─ plotting/     # plotting helpers and animations
├─ stats/        # statistical analysis and phase segmentation
├─ io/           # FITS and data I/O
└─ utils/        # small reusable utilities

scripts/
├─ run_tracking.py
├─ recompute_statistics.py
└─ make_animation.py
```

Only the high-level structure is shown here; individual modules are documented
inline in the source code.

---

## Installation

### 1. Clone the repository

> **Note**  
> The repository is currently under active development.  
> Replace the URL below with the actual GitHub URL once the repository is public.

```bash
git clone https://github.com/<username>/<repository-name>.git
cd <repository-name>
```

---

### 2. Create a Python environment (recommended)

Using conda:

```bash
conda create -n contour python=3.11
conda activate contour
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

The `requirements.txt` file should list **exact package versions** to ensure
reproducibility.

---

## Required data and configuration

This code **does not download data automatically**.

You are expected to provide:

- calibrated solar image data (e.g. FITS files),
- metadata required for tracking and statistics,
- configuration paths inside the scripts or via a user-defined config file.

Please inspect the scripts in `scripts/` to adapt paths and parameters to your
local data layout.

---

## Quick start

Run contour tracking:

```bash
python scripts/run_tracking.py
```

Recompute statistics:

```bash
python scripts/recompute_statistics.py
```

Create animations:

```bash
python scripts/make_animation.py
```

Each script is intended to be **edited or wrapped** for specific datasets and
experiments.

---

## Dependencies

Core dependencies include:

- numpy
- pandas
- scipy
- matplotlib
- scikit-image
- astropy
- sunpy
- shapely
- pwlf

See `requirements.txt` for exact versions.

---

## Citation

If you use this code in scientific work, please cite:

> Korda et al.,  
> *Equipartition field strength on the sunspot boundary: A statistical study*,  
> Astronomy & Astrophysics, 2026.

---

## License

Specify the license here (e.g. MIT, BSD-3-Clause, GPL-3.0).
