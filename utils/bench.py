import torch
import time

# Tamanho das matrizes (Ajuste para mais se quiser estressar a placa)
size = 8000 

def benchmark(device_name):
    device = torch.device(device_name)
    # Criando matrizes aleatórias
    a = torch.randn(size, size, device=device)
    b = torch.randn(size, size, device=device)
    
    # Warm-up (essencial para GPU)
    _ = torch.matmul(a, b)
    torch.cuda.synchronize() if device_name == "cuda" else None
    
    start = time.time()
    # Operação principal
    result = torch.matmul(a, b)
    
    # Garante que o cálculo terminou antes de parar o cronômetro
    torch.cuda.synchronize() if device_name == "cuda" else None
    end = time.time()
    
    return end - start

print(f"Iniciando Benchmark (Matrizes {size}x{size})...")

t_cpu = benchmark("cpu")
print(f"Tempo na CPU (Ryzen 5800X3D): {t_cpu:.4f} segundos")

t_gpu = benchmark("cuda")
print(f"Tempo na GPU (RX 7800 XT): {t_gpu:.4f} segundos")

print(f"\nA GPU foi {t_cpu/t_gpu:.2f}x mais rápida que a CPU!")