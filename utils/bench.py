import platform
import subprocess
import time

import torch


# Matrix size — increase to stress the GPU further
SIZE = 8000


def get_cpu_name() -> str:
    """Detects CPU name cross-platform without hardcoding."""
    system = platform.system()
    try:
        if system == "Linux":
            with open("/proc/cpuinfo") as f:
                for line in f:
                    if "model name" in line:
                        return line.split(":")[1].strip()
        elif system == "Windows":
            result = subprocess.check_output(
                ["wmic", "cpu", "get", "name"], text=True
            )
            lines = [l.strip() for l in result.splitlines() if l.strip()]
            return lines[1] if len(lines) > 1 else "Unknown CPU"
        elif system == "Darwin":
            result = subprocess.check_output(
                ["sysctl", "-n", "machdep.cpu.brand_string"], text=True
            )
            return result.strip()
    except Exception:
        pass
    return "Unknown CPU"


def get_gpu_name() -> str:
    """Returns GPU name if available, otherwise empty string."""
    if torch.cuda.is_available():
        return torch.cuda.get_device_name(0)
    return ""


def get_backend_label() -> str:
    """Returns a human-readable backend label (ROCm, CUDA or CPU)."""
    if not torch.cuda.is_available():
        return "CPU only"
    if torch.version.hip:
        return f"ROCm {torch.version.hip}"
    return f"CUDA {torch.version.cuda}"


def benchmark(device_name: str) -> float:
    """
    Runs a matrix multiplication benchmark on the given device.
    Returns elapsed time in seconds.
    """
    device = torch.device(device_name)
    a = torch.randn(SIZE, SIZE, device=device)
    b = torch.randn(SIZE, SIZE, device=device)

    # Warm-up — essential for GPU to avoid cold-start bias
    _ = torch.matmul(a, b)
    if torch.cuda.is_available():
        torch.cuda.synchronize()

    start = time.perf_counter()
    result = torch.matmul(a, b)
    if torch.cuda.is_available():
        torch.cuda.synchronize()
    end = time.perf_counter()

    return end - start


if __name__ == "__main__":
    cpu_name     = get_cpu_name()
    gpu_name     = get_gpu_name()
    backend      = get_backend_label()
    gpu_available = torch.cuda.is_available()

    print("=" * 55)
    print(f"  Matrix Benchmark ({SIZE}x{SIZE})")
    print("=" * 55)
    print(f"\n  CPU : {cpu_name}")
    print(f"  GPU : {gpu_name if gpu_available else 'Not available'}")
    print(f"  Backend : {backend}\n")
    print("─" * 55)

    t_cpu = benchmark("cpu")
    print(f"  CPU time : {t_cpu:.4f}s")

    if gpu_available:
        t_gpu = benchmark("cuda")
        print(f"  GPU time : {t_gpu:.4f}s")
        print("─" * 55)
        print(f"\n  GPU was {t_cpu / t_gpu:.1f}x faster than CPU!")
    else:
        print("\n  [INFO] No GPU detected — skipping GPU benchmark.")

    print("=" * 55)