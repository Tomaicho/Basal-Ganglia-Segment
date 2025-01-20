"""Performs the segmentation when input T1 and T2 images of one subject.

Makes use of the functions in the utils.py file to pre-process the input images, perform the segmentation using the trained models that require T1 and T2 images of a subject, and post-process the output masks.
"""

import os
import argparse

from Image_processing.utils import *

MNI_TEMPLATE = "data/templates/mni_icbm152_t1_tal_nlin_asym_09c.nii.gz"
ATLAS_ROI = "data/templates/ROI_CIT168_atlas.nii.gz"

parser = argparse.ArgumentParser(
                    description='Performs segmentation of the STN, RN and SN of subject given its T1w and T2w brain MRI scans.')

parser.add_argument('-t1', required=True, help='Path to the T1-weighted MRI image of the subject.')
parser.add_argument('-t2', required=True, help='Path to the T2-weighted MRI image of the subject.')

args = parser.parse_args()

t1_image = args.t1
t2_image = args.t2

# Assert that the input images are .nii.gz files
assert t1_image.endswith('.nii.gz'), "Input T1 image must be a .nii.gz file."
assert t2_image.endswith('.nii.gz'), "Input T2 image must be a .nii.gz file."

# Skull-strip the input images
skull_strip(t1_image, t1=True)
skull_strip(t2_image, t1=False)

t1_ss_path = os.path.join("tmp", "t1_ss.nii.gz")
t2_ss_path = os.path.join("tmp", "t2_ss.nii.gz")

# Compute transformation of the MNI (data/templates/mni_icbm...) template to the skull-stripped T1 image
register_images(fixed_image=t1_ss_path, moving_image=MNI_TEMPLATE)

parameters_file_folder = os.path.join('tmp', 'MNI_to_t1_transform', 'TransformParameters.0.for_labels.txt')
change_parameters_file_for_labels(parameters_file_folder)

# Apply the transformation stored in tmp/MNI_to_t1_transform to the ROI atlas
roi_mask_path = os.path.join("tmp", "MNI_to_t1_transform", "roi_mask.nii.gz")
apply_transform_to_image(input_image=ATLAS_ROI, transform=os.path.join('tmp', 'MNI_to_t1_transform', 'TransformParameters.0.for_labels.txt'), output_image=roi_mask_path)

# Preprocess and use the transformed atlas ROI to crop T1 and T2 images
transform_path = os.path.join(parameters_file_folder, 'TransformParameters.0.for_labels.txt')
crop_and_preprocess_images(t1_ss_path, t2_ss_path, roi_mask_path, transform_path)

# Perform the segmentation of the images stored in the folder /nnunet/raw/Dataset002_LOCALIZER
# Output is stored in /results
os.system('nnUNet_predict -i tmp/preprocessed/ -o /results/ -d 001 -c 3d_fullres -f 5 --save_probabilities -tr nnUNetTrainer_100epochs_NoMirroring -p nnUNetResEncUNetLPlans')

