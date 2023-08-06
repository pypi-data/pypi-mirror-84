# Copyright 2020-present, Mayo Clinic Department of Neurology - Laboratory of Bioelectronics Neurophysiology and Engineering
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

__version__ = '0.1.3'



import os
# Check windows or linux and sets separator
if os.name == 'nt': DELIMITER = '\\'
else: DELIMITER = '/'


import AISC.FeatureExtractor
import AISC.WaveDetector
import AISC.models
import AISC.modules
import AISC.utils




