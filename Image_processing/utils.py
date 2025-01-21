"""File containing utility functions for image processing.

Skull-stripping function requires FreeSurfer to be installed on the system as it makes use of Synthstrip.
Image registration functions require elastix to be installed on the system.

This file can also be imported as a module and contains the following functions:

"""

import os
import subprocess
import re
import torchio as tio

ROI_MNI = "data/templates/combined_ROI_MNI.nii.gz"

def skull_strip(input_image, t1):
    """Function to skull-strip an image using FreeSurfer's Synthstrip.

    Parameters
    ----------
    input_image : str
        Path to the input image.

    T1 : bool
        Whether the input image is a T1-weighted image.

    Returns
    -------
    None

    """
    if not os.path.exists(input_image):
        raise FileNotFoundError(f"Input image {input_image} not found.")
    # save the output image in the tmp folder
    if t1:
        output_image = os.path.join("tmp", "t1_ss.nii.gz")
    else:
        output_image = os.path.join("tmp", "t2_ss.nii.gz")
    cmd = f"mri_synthstrip -i {input_image} -o {output_image}"
    subprocess.run(cmd, shell=True)


def register_images(fixed_image, moving_image, output_dir):
    """Function to register two images using elastix.

    Parameters
    ----------
    fixed_image : str
        Path to the fixed image.
    moving_image : str
        Path to the moving image.
    output_dir : str
        Path to save the output image.

    Returns
    -------
    None

    """
    if not os.path.exists(fixed_image):
        raise FileNotFoundError(f"Fixed image {fixed_image} not found.")
    if not os.path.exists(moving_image):
        raise FileNotFoundError(f"Moving image {moving_image} not found.")
    # save the output in a folder in the tmp folder
    os.makedirs(output_dir)
    cmd = f"elastix -f {fixed_image} -m {moving_image} -out {output_dir} -p parameters.txt"
    subprocess.run(cmd, shell=True)


def apply_transform_to_image(input_image, transform, output_image):
    """Function to apply a transformation to an image using transformix.

    Parameters
    ----------
    input_image : str
        Path to the input image.
    transform : str
        Path to the transformation file.
    output_image : str
        Path to save the output image.

    Returns
    -------
    None

    """
    if not os.path.exists(input_image):
        raise FileNotFoundError(f"Input image {input_image} not found.")
    if not os.path.exists(transform):
        raise FileNotFoundError(f"Transform file {transform} not found.")
    # save the output in a folder in the tmp folder
    cmd = f"transformix -in {input_image} -out {output_image} -tp {transform}"
    subprocess.run(cmd, shell=True)

def change_parameters_file_for_labels(path_to_parameters_file_folder):
    """"Function to change the Interpolation Order parameter of the elastix parameters file to 0 to make it aplicable to binary label images.

    Parameters
    ----------
    path_to_parameters_file_folder : str
        Path to the folder containing the elastix parameters file.
    
    Returns
    -------
    None

    """
    parameters_file = os.path.join(path_to_parameters_file_folder, 'TransformParameters.0.txt')
    with open(parameters_file, 'r') as param_file:
        params = param_file.read()

        params = re.sub('(FinalBSplineInterpolationOrder 3)', 'FinalBSplineInterpolationOrder 0', params)
        # save the modified parameters
        new_parameters_file = os.path.join(path_to_parameters_file_folder, 'TransformParameters.0.for_labels.txt')
        with open(new_parameters_file, 'w') as param_file:
            param_file.write(params)

def crop_and_preprocess_images_method_II(t1_ss_path, t2_ss_path, roi_mask_path):
    """Function to crop and preprocess the input T1 and T2 images using the transformed atlas ROI for method II input.

    Parameters
    ----------
    t1_ss_path : str
        Path to the skull-stripped T1-weighted image.
    t2_ss_path : str
        Path to the skull-stripped T2-weighted image.
    roi_mask_path : str
        Path to the transformed atlas ROI mask.

    Returns
    -------
    None

    """
    # Define the transformations to apply to the images
    transforms_preprocess = tio.Compose([
        tio.ToCanonical(),
        tio.Resample('t2', image_interpolation='bspline'),
        tio.CropOrPad(mask_name='roi_mask'),
        tio.HistogramStandardization('normalization_landmarks.pth'),
        tio.CropOrPad((90, 80, 60)),
    ])

    # Define the tio.Subject object
    subject = tio.Subject(
        t1=tio.ScalarImage(t1_ss_path),
        t2=tio.ScalarImage(t2_ss_path),
        roi_mask=tio.LabelMap(roi_mask_path),
    )

    # Apply the preprocessing transformations to t1 and t2
    preprocessed = transforms_preprocess(subject)

    # Save the preprocessed images in the preprocessed folder in the tmp folder
    os.makedirs(os.path.join('tmp', 'preprocessed_method_II'), exist_ok=True)
    preprocessed.t1.save(os.path.join('tmp', 'preprocessed_method_II', 'LOCALIZER_001_0000.nii.gz'))
    preprocessed.t2.save(os.path.join('tmp', 'preprocessed_method_II', 'LOCALIZER_001_0000.nii.gz'))


def crop_and_preprocess_images_method_I(t1_ss_path, t2_ss_path):
    """Function to crop and preprocess the input T1 and T2 images for method I input.

    Parameters
    ----------
    t1_ss_path : str
        Path to the skull-stripped T1-weighted image.
    t2_ss_path : str
        Path to the skull-stripped T2-weighted image.
    roi_mask_path : str
        Path to the transformed atlas ROI mask.

    Returns
    -------
    None

    """
    # Define the transformations to apply to the images
    transforms_preprocess = tio.Compose([
        tio.CropOrPad(mask_name='roi_mask'),
        tio.ZNormalization(),
        tio.HistogramStandardization('normalization_landmarks.pth'),
    ])

    # Define the tio.Subject object
    subject = tio.Subject(
        t1=tio.ScalarImage(t1_ss_path),
        t2=tio.ScalarImage(t2_ss_path),
        roi_mask=tio.LabelMap(ROI_MNI),
    )

    # Apply the preprocessing transformations to t1 and t2
    preprocessed = transforms_preprocess(subject)

    # Save the preprocessed images in the preprocessed folder in the tmp folder
    os.makedirs(os.path.join('tmp', 'preprocessed_method_I'), exist_ok=True)
    preprocessed.t1.save(os.path.join('tmp', 'preprocessed_method_I', '0.5_MNI_001_0000.nii.gz'))
    preprocessed.t2.save(os.path.join('tmp', 'preprocessed_method_I', '0.5_MNI_001_0001.nii.gz'))

