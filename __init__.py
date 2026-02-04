"""
jak ukladat tracks a obecne nested dicts aby to bylo prenositelne?
pipreqs neni dostatecne rekurzivni a nevidi dost daleko...

select_three_frames vraci cely df pro ty 3 radky? minimalne jeste obervation_id a frame_id
- TAKY ASI VYBER N ROVNOMERNE, TO VEZME JAKOU FAZI EXTRA A POKUD CHYBI TAK SAHNE VEDLE?

ZKUSIT KONTROLNI OBRAZKY, JESTLI FUNGUJI
"""

# Create requirements.txt by following these steps:
#
# 1) Generate requirements.in by scanning actual imports in the code:
#    pipreqs . --force --encoding=utf-8 --ignore figures,log,OpenPBS,python_compiled --savepath requirements.in
#
# 2) Manually fix any incorrect entries in requirements.in:
#    - Replace placeholder versions like `==0.0`
#    - Fix names like:
#        skimage → scikit-image
#        cv2     → opencv-python
#        PIL     → Pillow
#        yaml    → PyYAML
#
# 3) Generate the final, pinned requirements.txt:
#    pip-compile --output-file=requirements.txt requirements.in

"""
1) celkovy tok v oblasti okolo nove vznikele pory
    - kolik je potreba na vytvoreni?
    - v nejake cele oblasti okolo ni, ne jen uvnitr kontury
2) podminky na casove trvani nove pory
    - minimalne existuje min_time cca 3 snimky
    - uvolnit oblast, pokud se tam nic nevyskytuje alespon max_time cca 10 snimku
"""

import os

# Filter out TensorFlow warnings
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

# Disable GPUs to avoid CUDA-related issues
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

# Extend PATH to include LaTeX binaries
os.environ["PATH"] += os.pathsep + "/usr/bin:/usr/share/texlive/bin"
