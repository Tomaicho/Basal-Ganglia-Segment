import os
import sys
from nnunetv2.model_sharing.model_import import install_model_from_zip_file

pwd = os.path.dirname(os.path.abspath(__file__))

# Define nnUNet paths
os.environ['nnUNet_raw'] = os.path.join(pwd, "nnunet", "raw")
os.environ['nnUNet_preprocessed'] = os.path.join(pwd, "nnunet", "preprocessed")
os.environ['nnUNet_results'] = os.path.join(pwd, "nnunet", "models")

if len(sys.argv) != 2:
    print("Usage: python install_model.py /path/to/model.zip")
    sys.exit(1)

zip_file_path = sys.argv[1]
install_model_from_zip_file(zip_file_path)