# Basal-Ganglia-Segment
A repository containing two automatic segmentation methods of basal ganglia nuclei in MRI data. The methods trained for 7T and 3T field intensities are described in [.........] and perform segmentation of the Subthalamic Nucleus (STN), Substantia Nigra (SN) and Red Nucleus (RN).

## Usage
python basal_ganglia_segment.py -t1 path/to/t1/image.nii.gz -t2 path/to/t2/image.nii.gz -m [I, II]

## Dependencies
### Pip installations:
    - Torch
    - Torchio
    - nnUNetv2
    - SimpleITK

### Downloadable packages:
    - Synthstrip 
    - FreeSurfer
    - Elastix

### Installation Guidelines
1. Create virtual environment.
2. Install the pip dependencies.
3. Download correct FreeSurfer release to a specified **folder** from https://surfer.nmr.mgh.harvard.edu/fswiki/rel7downloads and follow the Install and Setup guidelines.
4. Run the following bash commands:
    ```
    $ export FREESURFER_HOME=/path/to/folder/freesurfer
    $ source $FREESURFER_HOME/SetUpFreeSurfer.sh
    ```
5. Download elastix from https://github.com/SuperElastix/elastix/releases/tag/5.2.0 and unzip to a specified folder.
6. Run the following bash commands:
    ```
    $ export PATH=/path/to/folder/elastix/bin:$PATH
    $ export LD_LIBRARY_PATH=/path/to/folder/elastix/lib:$LD_LIBRARY_PATH
    $ chmod +x /path/to/folder/elastix/bin/elastix
    ```
7. Clone this repository to a specified folder and run this bash command:
    ```
    $ export nnUNet_results="/path/to/folder/Basal-Ganglia-Segment/nnunet/models"
    ```
9. Download the nnUNet models from https://campuscvut-my.sharepoint.com/:u:/g/personal/limatom1_cvut_cz/EU3QE9E1gIVFmWyLaOwOX0sB9_jRzA32GqJJ9Cl_FalVaw?e=SNG8au and https://campuscvut-my.sharepoint.com/:u:/g/personal/limatom1_cvut_cz/EZab_ICIPA1AgzYdkCiOgdUBAJtoo5-Cmqh6XhcyxpruJQ?e=84FQ3H to a specified folder.
10. Open a terminal in the folder with the cloned Basal-Ganglia-Segment repository and run the following bash commands:
    ```
    $ python install_model.py /path/to/downloaded/models/folder/method_I.zip
    $ python install_model.py /path/to/downloaded/models/folder/method_II.zip
    ```
