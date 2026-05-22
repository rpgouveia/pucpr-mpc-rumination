import platform
import subprocess
import torch


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


def get_backend() -> str:
    """Returns the active GPU backend: CUDA, ROCm or CPU."""
    if not torch.cuda.is_available():
        return "cpu"
    if torch.version.hip:
        return "rocm"
    return "cuda"


def print_system_stats():
    """Prints CPU and GPU stats dynamically, works on AMD (ROCm) and NVIDIA (CUDA)."""

    backend = get_backend()
    cpu_name = get_cpu_name()

    print("=" * 50)
    print("  System Stats")
    print("=" * 50)

    # CPU
    print(f"\n  CPU : {cpu_name}")

    # GPU
    if backend == "cpu":
        print("\n  GPU : Not available — running on CPU only.")
        print("=" * 50)
        return

    n_gpus = torch.cuda.device_count()
    backend_label = f"ROCm {torch.version.hip}" if backend == "rocm" else f"CUDA {torch.version.cuda}"

    print(f"  GPU backend : {backend_label}")
    print(f"  GPUs found  : {n_gpus}")

    for i in range(n_gpus):
        props       = torch.cuda.get_device_properties(i)
        total_mem   = props.total_memory / 1e9
        reserved    = torch.cuda.memory_reserved(i) / 1e9
        allocated   = torch.cuda.memory_allocated(i) / 1e9
        free        = total_mem - reserved

        print(f"\n  [{i}] {props.name}")
        print(f"      VRAM Total     : {total_mem:.2f} GB")
        print(f"      VRAM Reserved  : {reserved:.2f} GB")
        print(f"      VRAM Allocated : {allocated:.2f} GB")
        print(f"      VRAM Free      : {free:.2f} GB")

    print("=" * 50)


if __name__ == "__main__":
    print_system_stats()