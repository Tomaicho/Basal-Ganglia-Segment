import os
import subprocess

pwd = os.path.dirname(os.path.abspath(__file__))

subprocess.run(f'echo export nnUNet_raw="{os.path.join(pwd, "nnunet")}"', shell=True)
subprocess.run(f'echo export nnUNet_preprocessed="{os.path.join(pwd, "nnunet")}"', shell=True)
subprocess.run(f'echo export nnUNet_results="{os.path.join(pwd, "nnunet", "models")}"', shell=True)