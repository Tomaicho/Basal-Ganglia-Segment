""""""

import os
import argparse

from methods import *


parser = argparse.ArgumentParser(
                    description='Performs segmentation of the STN, RN and SN of subject given its T1w and T2w brain MRI scans.')

parser.add_argument('-t1', required=True, help='Path to the T1-weighted MRI image of the subject.')
parser.add_argument('-t2', required=True, help='Path to the T2-weighted MRI image of the subject.')
parser.add_argument('-m', required=True, choices=['I', 'II'], help='Method to be used on the segmentation (I -> MNI, II -> native).')

args = parser.parse_args()

t1_image = args.t1
t2_image = args.t2
method = args.m

# Assert that the input images are .nii.gz files
assert t1_image.endswith('.nii.gz'), "Input T1 image must be a .nii.gz file."
assert t2_image.endswith('.nii.gz'), "Input T2 image must be a .nii.gz file."

# Create the tmp folder if it does not exist
if not os.path.exists("tmp"):
    os.makedirs("tmp")

if method == 'I':
    method_I_segment(t1_image, t2_image)
elif method == 'II':
    method_II_segment(t1_image, t2_image)
else:
    raise ValueError("Method not recognized. Please choose between 'I' and 'II'.")