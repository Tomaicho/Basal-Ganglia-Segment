import os
import sys
import zipfile
import nnunetv2
#from nnunetv2.model_sharing.model_import import install_model_from_zip_file

pwd = os.path.dirname(os.path.abspath(__file__))

# Define nnUNet paths
os.environ['nnUNet_raw'] = os.path.join(pwd, "nnunet", "raw")
os.environ['nnUNet_preprocessed'] = os.path.join(pwd, "nnunet", "preprocessed")
os.environ['nnUNet_results'] = os.path.join(pwd, "nnunet", "models")

if len(sys.argv) != 2:
    print("Usage: python install_model.py /path/to/model.zip")
    sys.exit(1)

zip_file_path = sys.argv[1]

with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(os.path.join(pwd, "nnunet", "models"))

new_class = """
class nnUNetTrainer_100epochs_NoMirroring(nnUNetTrainer):
    def __init__(self, plans: dict, configuration: str, fold: int, dataset_json: dict, unpack_dataset: bool = True,
                 device: torch.device = torch.device('cuda')):
        super().__init__(plans, configuration, fold, dataset_json, unpack_dataset, device)
        self.num_epochs = 8000

    def configure_rotation_dummyDA_mirroring_and_inital_patch_size(self):
        rotation_for_DA, do_dummy_2d_data_aug, initial_patch_size, mirror_axes = \
            super().configure_rotation_dummyDA_mirroring_and_inital_patch_size()
        mirror_axes = None
        self.inference_allowed_mirroring_axes = None
        return rotation_for_DA, do_dummy_2d_data_aug, initial_patch_size, mirror_axes"""

try:
    with open(os.path.join(nnunetv2.__path__[0], "training", "nnUNetTrainer", "variants", "training_length", "nnUNetTrainer_Xepochs_NoMirroring.py"), 'a') as f:
        f.write(new_class)
except Exception as e:
    print(f"Error adding trainer class: {e}")