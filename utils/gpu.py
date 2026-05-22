import torch

def print_gpu_stats():
    if torch.cuda.is_available():
        # Memória total e reservada
        total_mem = torch.cuda.get_device_properties(0).total_memory / 1e9
        reserved_mem = torch.cuda.memory_reserved(0) / 1e9
        allocated_mem = torch.cuda.memory_allocated(0) / 1e9
        
        print(f"GPU: {torch.cuda.get_device_name(0)}")
        print(f"VRAM Total: {total_mem:.2f} GB")
        print(f"VRAM Reservada: {reserved_mem:.2f} GB")
        print(f"VRAM em uso: {allocated_mem:.2f} GB")
    else:
        print("GPU não disponível.")

print_gpu_stats()