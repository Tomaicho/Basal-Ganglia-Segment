import sys
from nnunetv2.model_sharing.model_import import install_model_from_zip_file

if len(sys.argv) != 2:
    print("Usage: python install_model.py /path/to/model.zip")
    sys.exit(1)

zip_file_path = sys.argv[1]
install_model_from_zip_file(zip_file_path)