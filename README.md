# Solar Feature Contour Tracking

A Python framework for tracking, segmenting, and analysing evolving solar
features (sunspots, pores) using contour-based methods.

The code is designed for scientific workflows where reproducibility,
clear separation of concerns, and publication-quality visualisation
are required.

---

## Features

- Contour-based tracking of evolving solar features
- Phase segmentation (forming / stable / decaying)
- Statistical analysis of physical quantities
- Modular plotting pipelines (snapshots, PDFs, animations)

---

## Repository structure

scr/
  geometry/      contour extraction, geometry utilities
  pipelines/     tracking, statistics, and plotting pipelines
  plotting/      plotting helpers and animations
  stats/         statistical analysis and segmentation
  io/            FITS and data I/O
  utils/         small reusable utilities

scripts/
  run_tracking.py
  recompute_statistics.py
  make_animation.py

---

## Installation

Clone the repository:

git clone https://github.com/Sirrah91/solar-feature-tracking.git
cd solar-feature-tracking

Create and activate a conda environment (recommended):

conda create -n contour python=3.11
conda activate contour

Install dependencies:

pip install -r requirements.txt

---

## Quick start

Run contour tracking:

python scripts/run_tracking.py

Recompute statistics:

python scripts/recompute_statistics.py

Create animations:

python scripts/make_animation.py

---

## Dependencies

- numpy
- pandas
- scipy
- matplotlib
- scikit-image
- astropy
- sunpy
- shapely
- pwlf

See requirements.txt for exact versions.

---

## Citation

If you use this code in scientific work, please cite:

Korda et al., "Title of the paper", Journal, Year.

---

## License

This project is licensed under the MIT License.
