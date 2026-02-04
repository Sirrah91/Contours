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

import os

# Filter out TensorFlow warnings
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

# Disable GPUs to avoid CUDA-related issues
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

# Extend PATH to include LaTeX binaries
os.environ["PATH"] += os.pathsep + "/usr/bin:/usr/share/texlive/bin"

