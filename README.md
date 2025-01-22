# Basal-Ganglia-Segment
A repository containing two automatic segmentation methods of basal ganglia nuclei in MRI data. The methods trained for 7T and 3T field intensities are described in [.........] and perform segmentation of the Subthalamic Nucleus (STN), Substantia Nigra (SN) and Red Nucleus (RN).

## Installation
After forking this repository to a folder at your own choice, open a terminal in that folder and run the following commands:
export nnUNet_results="nnunet/models"
add 100_epochs_No_Mirroring to lib

## Usage
python basal_ganglia_segment.py -t1 path/to/t1/image.nii.gz -t2 path/to/t2/image.nii.gz -m [I, II]

## Dependencies
Synthstrip - FreeSurfer
Elastix
Torch
Torchio
nnUNetv2
SimpleITK
