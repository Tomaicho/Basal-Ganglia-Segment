# Basal-Ganglia-Segment
A repository containing two automatic segmentation methods of basal ganglia nuclei in MRI data. The methods trained for 7T and 3T field intensities are described in [.........] and perform segmentation of the Subthalamic Nucleus (STN), Substantia Nigra (SN) and Red Nucleus (RN).

**Method I** performs the segmentation by relying on the MNI152 brain template to spatially normalize the images. The segmentation is performed in the template space, and the output masks are transformed back to the native space.

![alt text](https://github.com/Tomaicho/Basal-Ganglia-Segment/blob/main/documentation/Method_I_pipeline.png?raw=true)

**Method II** performs the segmentation directly on the native space of the image. For this, the CIT168 atlas is used to create a region of interest in every new subject.

![alt text](https://github.com/Tomaicho/Basal-Ganglia-Segment/blob/main/documentation/Method_II_pipeline.png?raw=true)

## Prerequisites
You need to have a machine with Python > 3.8 and any Bash based shell installed.

## Dependencies
### Pip installations:
    - Torch
    - Torchio
    - nnUNetv2
    - nipreps-synthstrip

### Downloadable packages:
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
7. Download the nnUNet models: [method I](https://campuscvut-my.sharepoint.com/:u:/g/personal/limatom1_cvut_cz/ETUBoVLkScxCpll3rY8cH9EBRx4rpId15ncHspdSQw3Feg?e=aPP7DO) and [method II](https://campuscvut-my.sharepoint.com/:u:/g/personal/limatom1_cvut_cz/EdqE2SUC-9lJl9q_-LeWSmYBG4SCQytict7hffJ6YK2P4A?e=kRHeMe) to a specified folder.
8. Open a terminal in the folder with the cloned Basal-Ganglia-Segment repository and run the following bash commands:
    ```
    $ python install_model.py /path/to/downloaded/models/folder/method_I.zip
    $ python install_model.py /path/to/downloaded/models/folder/method_II.zip

    ```

## Usage
Open a terminal in this project folder and run the following command:

```$ python basal_ganglia_segment.py -t1 path/to/t1/image.nii.gz -t2 path/to/t2/image.nii.gz -m [I, II]```

where the -t1 and -t2 arguments must be the absolute paths to the T1 and T2 images, respectively, and -m must be the method selected for the segmentation task, either I or II.

```
$ python basal_ganglia_segment.py -h
usage: basal_ganglia_segment.py [-h] -t1 T1 -t2 T2 -m {I,II}

Performs segmentation of the STN, RN and SN of subject given its T1w and T2w brain MRI scans.

options:
  -h, --help  show this help message and exit
  -t1 T1      Path to the T1-weighted MRI image of the subject.
  -t2 T2      Path to the T2-weighted MRI image of the subject.
  -m {I,II}   Method to be used on the segmentation (I -> MNI, II -> native).
```

The segmentation results are stored in the results/ folder as **method_I_output_in_native.nii.gz** and **method_II_output_in_native.nii.gz** for methods I and II, respectively. The segmentation of method I in the MNI space is also provided as **method_I_output_in_MNI.nii.gz**. nnUNet raw output is stored in the tmp/results/ folder.


## References

[1] Brett, Matthew, Ingrid S. Johnsrude, and Adrian M. Owen. "The problem of functional localization in the human brain." Nature reviews neuroscience 3.3 (2002): 243-249.

[2] Pauli, Wolfgang M., Amanda N. Nili, and J. Michael Tyszka. "A high-resolution probabilistic in vivo atlas of human subcortical brain nuclei." Scientific data 5.1 (2018): 1-13.

[3] Klein, Stefan, et al. "Elastix: a toolbox for intensity-based medical image registration." IEEE transactions on medical imaging 29.1 (2009): 196-205.

[4] Hoopes, Andrew, et al. "SynthStrip: skull-stripping for any brain image." NeuroImage 260 (2022): 119474.