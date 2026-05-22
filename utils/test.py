# ROCm installation instructions: https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/quick-start.html
# PyTorch installation instructions: https://pytorch.org/get-started/locally/
# to execute the Test: 
# source venv/bin/activate
# python test.py

import torch

x = torch.randn(3, 4)
print(x)

print("CUDA Available: ",torch.cuda.is_available())