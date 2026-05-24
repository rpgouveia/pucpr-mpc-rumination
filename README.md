# Monitoramento Automatizado da Ruminação em Vacas Leiteiras via Sensores e IoT

Disciplina: Métodos de Pesquisa Científica  
Curso: Ciência da Computação — Pontifícia Universidade Católica do Paraná  
Ano: 2026

---

## Autores

- Angelo Piovezan Jorgeto
- Ian Carlo Araújo Braz
- Jafte Carneiro Fagundes da Silva
- Nicolas Felix Hrescak
- Renato Pestana de Gouveia

---

## Pergunta de Pesquisa

Qual modelo de aprendizagem de máquina é mais eficaz na identificação da ruminação de vacas leiteiras?

---

## Descrição

Este repositório contém o experimento desenvolvido como atividade avaliativa da disciplina de Métodos de Pesquisa Científica. O experimento compara dois paradigmas de aprendizagem de máquina — aprendizado profundo (CNN 1D) e aprendizado clássico (Random Forest) — quanto à capacidade de classificar automaticamente comportamentos de bovinos leiteiros a partir de dados de acelerômetro triaxial coletados por sensores IoT em colares de pescoço.

O dataset utilizado é público e foi disponibilizado por Pavlovic et al. (2021) no repositório Zenodo. Ele contém 3.460 horas de dados sincronizados de acelerômetro e halter de pressão de 18 bovinos monitorados em três fazendas no Reino Unido entre 2015 e 2016. Os três comportamentos classificados são: Ruminação, Comendo e Outro.

---

## Estrutura do Repositório

```
pucpr-mpc-rumination/
│
├── dataset/                        # CSVs do dataset (não versionados — baixar via Zenodo)
│
├── docs/
│   ├── proposta-projeto-pesquisa.docx   # Proposta acadêmica (ABNT)
│   └── relatorio_modelo1.md             # Relatório de resultados — CNN 1D
│
├── notebooks/
│   ├── model1.ipynb                # Experimento Modelo 1: CNN 1D (baseline)
│   └── model2.ipynb                # Experimento Modelo 2: Random Forest
│
├── results/
│   ├── checkpoints/                # Pesos dos modelos (não versionados)
│   ├── figures/                    # Gráficos gerados pelos experimentos
│   └── metrics/                    # Métricas e histórico de treinamento (JSON, CSV)
│
├── utils/
│   ├── verificar_gpu.py            # Verificação do ambiente e GPU
│   ├── gpu.py                      # Monitoramento de VRAM em tempo real
│   ├── bench.py                    # Benchmark CPU vs GPU
│   ├── test.py                     # Smoke test básico do PyTorch
│   └── amd-rocm.md                 # Referências de instalação ROCm
│
├── rumination-env-linux-amd.yml    # Ambiente conda — Linux com GPU AMD (ROCm 7.2)
├── rumination-env-windows-nvidia.yml  # Ambiente conda — Windows com GPU NVIDIA (CUDA 12.6)
├── .gitignore
└── README.md
```

---

## Configuração do Ambiente

O projeto requer Python 3.11 e PyTorch 2.11.0. Dois ambientes conda estão disponíveis conforme a plataforma.

### Linux com GPU AMD (ROCm 7.2)

```bash
conda env create -f rumination-env-linux-amd.yml
conda activate rumination
```

### Windows com GPU NVIDIA (CUDA 12.6)

```bash
conda env create -f rumination-env-windows-nvidia.yml
conda activate rumination
```

Após criar o ambiente, execute o script de verificação para confirmar que a GPU está sendo reconhecida corretamente:

```bash
python utils/verificar_gpu.py
```

---

## Dataset

O dataset não está incluído neste repositório devido ao seu tamanho. Para reproduzir o experimento, faça o download dos arquivos CSV diretamente do Zenodo e coloque-os na pasta `dataset/`:

- Fonte: https://doi.org/10.5281/zenodo.4064801
- Arquivos necessários: `accel-01.csv` a `accel-18.csv` e `halter-01.csv` a `halter-18.csv`

---

## Execução

Os experimentos são conduzidos via notebooks Jupyter. Com o ambiente conda ativado, escolha uma das opções abaixo:

### Jupyter Lab (navegador)

```bash
jupyter lab
```

### VS Code

Abra a pasta do projeto no VS Code, instale a extensão **Jupyter** (Microsoft) caso ainda não esteja instalada, e selecione o kernel `rumination` no canto superior direito do notebook antes de executar.

Execute os notebooks na seguinte ordem:

1. `notebooks/model1.ipynb` — CNN 1D (baseline)
2. `notebooks/model2.ipynb` — Random Forest

Cada notebook é independente e cobre o pipeline completo: carregamento, pré-processamento, treinamento, validação cruzada e avaliação no conjunto de teste. Os resultados são salvos automaticamente em `results/`.

---

## Pipeline Experimental

O pré-processamento aplicado a ambos os modelos segue o protocolo de Pavlovic et al. (2021):

1. Fusão dos arquivos de acelerômetro e halter por timestamp (arredondamento para 100 ms para alinhamento dos sensores)
2. Diferença discreta em cada eixo: `Δs[t] = s[t] - s[t-1]`
3. Segmentação em janelas de 90 s (900 amostras a 10 Hz) com rótulo por votação majoritária
4. Balanceamento por undersampling por animal
5. Divisão treino/teste: animais 04, 10 e 11 reservados para teste (um por farm trial); 15 restantes para treino com validação cruzada GroupKFold (5 folds por animal)

---

## Resultados Parciais

### Modelo 1 — CNN 1D

Replicação do baseline de Pavlovic et al. (2021).

| Métrica | Resultado | Referência (artigo) |
|---------|-----------|---------------------|
| F1 médio (validação cruzada) | 0,8285 +/- 0,0319 | 0,82 +/- ~0,03 |
| F1 macro (teste) | 0,786 | 0,82 |
| F1 weighted (teste) | 0,840 | 0,82 |
| Accuracy (teste) | 0,827 | ~0,82 |

Relatório completo: `docs/relatorio_modelo1.md`

### Modelo 2 — Random Forest

Em desenvolvimento. Resultados serão adicionados após a conclusão do `notebooks/model2.ipynb`.

---

## Referências

PAVLOVIC, D. et al. Classification of Cattle Behaviours Using Neck-Mounted Accelerometer-Equipped Collars and Convolutional Neural Networks. *Sensors*, v. 21, n. 12, p. 4050, 2021a.

PAVLOVIC, D. et al. *Precision Beef — Animal Behaviour Classification*. Zenodo, 2021b. DOI: 10.5281/zenodo.4064801. Disponível em: https://doi.org/10.5281/zenodo.4064801.

BEAUCHEMIN, K. A. Invited review: Current perspectives on eating and rumination activity in dairy cows. *Journal of Dairy Science*, v. 101, n. 6, p. 4762-4784, 2018.

KAPUSNIAKOVÁ, M. et al. Nutrition, rumination and heat stress as influential factors in dairy cows production: A review. *Acta fytotechnica et zootechnica*, v. 26, n. 2, p. 131-137, 2023.

TANGORRA, F. M. et al. Internet of Things (IoT): Sensors Application in Dairy Cattle Farming. *Animals*, v. 14, n. 21, p. 3071, 2024.