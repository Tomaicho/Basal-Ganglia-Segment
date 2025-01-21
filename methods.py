"""Performs the segmentation when input T1 and T2 images of one subject.

Makes use of the functions in the utils.py file to pre-process the input images, perform the segmentation using the trained models that require T1 and T2 images of a subject, and post-process the output masks.
"""

import os
from Image_processing.utils import *

MNI_TEMPLATE = "data/templates/mni_icbm152_t1_tal_nlin_asym_09c_masked.nii.gz"
ATLAS_ROI = "data/templates/ROI_CIT168_atlas.nii.gz"

def method_II_segment(t1_image, t2_image):
    """Performs the segmentation of the STN, RN and SN of a subject using the method II.

    Parameters
    ----------
    t1_image : str
        Path to the T1-weighted MRI image of the subject.
    t2_image : str
        Path to the T2-weighted MRI image of the subject.

    Returns
    -------
    None

    """
    # Skull-strip the input images
    skull_strip(t1_image, t1=True)
    skull_strip(t2_image, t1=False)

    t1_ss_path = os.path.join("tmp", "t1_ss.nii.gz")
    t2_ss_path = os.path.join("tmp", "t2_ss.nii.gz")

    # Create the MNI_to_t1_transform folder if it does not exist
    if not os.path.exists(os.path.join("tmp", "MNI_to_t1_transform")):
        os.makedirs(os.path.join("tmp", "MNI_to_t1_transform"))

    # Compute transformation of the MNI (data/templates/mni_icbm...) template to the skull-stripped T1 image
    register_images(fixed_image=t1_ss_path, moving_image=MNI_TEMPLATE, output_dir=os.path.join("tmp", "MNI_to_t1_transform"), parameters_file="data/templates/Par0064_affine.txt")
    print("\nTransformation of MNI to native space computed.\n")

    parameters_file_folder = os.path.join('tmp', 'MNI_to_t1_transform')
    change_parameters_file_for_labels(parameters_file_folder)
    print("\nParameters file modified to be applicable for labels.\n")

    # Apply the transformation stored in tmp/MNI_to_t1_transform to the ROI atlas
    roi_mask_output_dir = os.path.join("tmp", "MNI_to_t1_transform")
    apply_transform_to_image(input_image=ATLAS_ROI, transform=os.path.join('tmp', 'MNI_to_t1_transform', 'TransformParameters.0.for_labels.txt'), output_dir=roi_mask_output_dir)
    print("\nROI mask transformed to native space.\n")

    # Preprocess and use the transformed atlas ROI to crop T1 and T2 images
    roi_mask_path = os.path.join("tmp", "MNI_to_t1_transform", "roi_mask.nii.gz")
    crop_and_preprocess_images_method_II(t1_ss_path, t2_ss_path, roi_mask_path)
    print("\nImages preprocessed and cropped using the transformed ROI mask.\n")

    # Perform the segmentation of the images stored in the folder preprocessed folder
    # Output is stored in /results
    os.system('nnUNetv2_predict -i tmp/preprocessed_method_II/ -o /results/ -d 002 -c 3d_fullres -f 5 --save_probabilities -tr nnUNetTrainer_100epochs_NoMirroring -p nnUNetResEncUNetLPlans')

    print("Segmentation completed and stored in /results folder as LOCALIZER_001.nii.gz")

def method_I_segment(t1_image, t2_image):
    """Performs the segmentation of the STN, RN and SN of a subject using the method I.

    Parameters
    ----------
    t1_image : str
        Path to the T1-weighted MRI image of the subject.
    t2_image : str
        Path to the T2-weighted MRI image of the subject.

    Returns
    -------
    None

    """
    # Skull-strip the input images
    skull_strip(t1_image, t1=True)
    skull_strip(t2_image, t1=False)

    t1_ss_path = os.path.join("tmp", "t1_ss.nii.gz")
    t2_ss_path = os.path.join("tmp", "t2_ss.nii.gz")

    # Create the t1_to_MNI_transform folder if it does not exist
    if not os.path.exists(os.path.join("tmp", "t1_to_MNI_transform")):
        os.makedirs(os.path.join("tmp", "t1_to_MNI_transform"))

    # Compute transformation of the skull-stripped T1 image to the MNI (data/templates/mni_icbm...) template
    register_images(fixed_image=MNI_TEMPLATE, moving_image=t1_ss_path, output_dir=os.path.join("tmp", "t1_to_MNI_transform"))

    # Apply the transformation stored in tmp/t1_to_MNI_transform to the T1_ss and T2_ss images
    transform_path = os.path.join('tmp', 't1_to_MNI_transform', 'TransformParameters.0.txt')
    apply_transform_to_image(input_image=t1_ss_path, transform=transform_path, output_image=os.path.join("tmp", "t1_ss_MNI.nii.gz"))
    apply_transform_to_image(input_image=t2_ss_path, transform=transform_path, output_image=os.path.join("tmp", "t2_ss_MNI.nii.gz"))

    # Preprocess T1 and T2 images
    crop_and_preprocess_images_method_I(t1_ss_path, t2_ss_path)

    # Perform the segmentation of the images stored in the folder preprocessed folder
    # Output is stored in /results
    os.system('nnUNetv2_predict -i tmp/preprocessed_method_I/ -o /results/ -d 003 -c 3d_fullres -f 5 --save_probabilities -tr nnUNetTrainer_100epochs_NoMirroring -p nnUNetResEncUNetLPlans')
    
    print("Segmentation completed and stored in /results folder as 0.5_MNI_001.nii.gz")