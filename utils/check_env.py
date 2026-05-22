import sys
import torch
import platform

print("=" * 55)
print("  Verificação do Ambiente — Pipeline Ruminação")
print("=" * 55)

# Sistema operacional
print(f"\n  Sistema     : {platform.system()} {platform.release()}")
print(f"  Python      : {sys.version.split()[0]}")
print(f"  PyTorch     : {torch.__version__}")

# GPU
print("\n" + "─" * 55)
print("  STATUS DA GPU")
print("─" * 55)

if torch.cuda.is_available():
    n_gpus = torch.cuda.device_count()
    print(f"\n  Backend     : CUDA (NVIDIA)")
    print(f"  CUDA versão : {torch.version.cuda}")
    print(f"  GPUs visíveis: {n_gpus}")
    for i in range(n_gpus):
        nome = torch.cuda.get_device_name(i)
        mem  = torch.cuda.get_device_properties(i).total_memory / 1024**3
        cc   = torch.cuda.get_device_capability(i)
        print(f"\n    GPU {i}: {nome}")
        print(f"      VRAM               : {mem:.1f} GB")
        print(f"      Compute Capability : {cc[0]}.{cc[1]}")
    device = torch.device("cuda:0")

elif hasattr(torch, "version") and hasattr(torch.version, "hip") and torch.version.hip:
    print(f"\n  Backend     : ROCm (AMD)")
    print(f"  ROCm versão : {torch.version.hip}")
    if torch.cuda.is_available():  # ROCm usa a API CUDA
        n_gpus = torch.cuda.device_count()
        print(f"  GPUs visíveis: {n_gpus}")
        for i in range(n_gpus):
            nome = torch.cuda.get_device_name(i)
            mem  = torch.cuda.get_device_properties(i).total_memory / 1024**3
            print(f"\n    GPU {i}: {nome}")
            print(f"      VRAM : {mem:.1f} GB")
    device = torch.device("cuda:0")

else:
    print("\n  [AVISO] Nenhuma GPU detectada — rodando em CPU.")
    print("  Verifique se os drivers e o PyTorch correto estão instalados.")
    device = torch.device("cpu")

# Teste de operação na GPU
print("\n" + "─" * 55)
print("  TESTE DE OPERAÇÃO")
print("─" * 55)

try:
    # Simula um batch do pipeline (8 janelas, 3 eixos, 900 amostras)
    tensor = torch.randn(8, 3, 900, device=device)
    resultado = tensor.mean()
    print(f"\n  Tensor criado em : {tensor.device}")
    print(f"  Operação (mean)  : {resultado.item():.6f}  ✅")
    print(f"\n  [OK] GPU funcionando corretamente para o pipeline!")
except Exception as e:
    print(f"\n  [ERRO] Falha ao operar na GPU: {e}")

# Bibliotecas do pipeline
print("\n" + "─" * 55)
print("  BIBLIOTECAS DO PIPELINE")
print("─" * 55)

libs = {
    "pandas"       : "pandas",
    "numpy"        : "numpy",
    "scikit-learn" : "sklearn",
    "matplotlib"   : "matplotlib",
    "seaborn"      : "seaborn",
    "tqdm"         : "tqdm",
}

todas_ok = True
for nome, modulo in libs.items():
    try:
        m = __import__(modulo)
        versao = getattr(m, "__version__", "ok")
        print(f"  {'✅'} {nome:15s}: {versao}")
    except ImportError:
        print(f"  {'❌'} {nome:15s}: NÃO ENCONTRADO")
        todas_ok = False

print("\n" + "=" * 55)
if todas_ok:
    print("  Ambiente pronto!")
else:
    print("  [ATENÇÃO] Algumas bibliotecas estão faltando.")
    print("  Ative o ambiente correto e tente novamente.")
print("=" * 55)
