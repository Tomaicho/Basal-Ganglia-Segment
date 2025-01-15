"""File containing utility functions for image processing.

Skull-stripping function requires FreeSurfer to be installed on the system as it makes use of Synthstrip.
Image registration functions require elastix to be installed on the system.

This file can also be imported as a module and contains the following functions:

"""

import os
import subprocess

def skull_strip(input_image, T1):
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
    if T1:
        output_image = os.path.join("tmp", "t1_ss.nii.gz")
    else:
        output_image = os.path.join("tmp", "t2_ss.nii.gz")
    cmd = f"SynthStrip -i {input_image} -o {output_image}"
    subprocess.run(cmd, shell=True)


def register_images(fixed_image, moving_image):
    """Function to register two images using elastix.

    Parameters
    ----------
    fixed_image : str
        Path to the fixed image.
    moving_image : str
        Path to the moving image.

    Returns
    -------
    None

    """
    if not os.path.exists(fixed_image):
        raise FileNotFoundError(f"Fixed image {fixed_image} not found.")
    if not os.path.exists(moving_image):
        raise FileNotFoundError(f"Moving image {moving_image} not found.")
    # save the output in a folder in the tmp folder
    output_dir = os.path.join("tmp", "MNI_to_t1_transform")
    os.makedirs(output_dir)
    cmd = f"elastix -f {fixed_image} -m {moving_image} -out {output_dir} -p parameters.txt"
    subprocess.run(cmd, shell=True)


def apply_transform_to_image(input_image, transform):
    """Function to apply a transformation to an image using transformix.

    Parameters
    ----------
    input_image : str
        Path to the input image.
    transform : str
        Path to the transformation file.

    Returns
    -------
    None

    """
    if not os.path.exists(input_image):
        raise FileNotFoundError(f"Input image {input_image} not found.")
    if not os.path.exists(transform):
        raise FileNotFoundError(f"Transform file {transform} not found.")
    # save the output in a folder in the tmp folder
    output_image = os.path.join("tmp", "Atlas_ROI_in_native")
    cmd = f"transformix -in {input_image} -out {output_image} -tp {transform}"
    subprocess.run(cmd, shell=True)

def change_parameters_file_for_labels(path_to_parameters_file_folder):
    
    parameters_file = os.path.join(path_to_parameters_file_folder, 'TransformParameters.0.txt')
    with open(parameters_file, 'r') as param_file:
        params = param_file.read()

        params = re.sub('(FinalBSplineInterpolationOrder 3)', 'FinalBSplineInterpolationOrder 0', params)
        # save the modified parameters
        new_parameters_file = os.path.join(path_to_parameters_file_folder, 'TransformParameters.0.for_labels.txt')
        with open(new_parameters_file, 'w') as param_file:
            param_file.write(params)