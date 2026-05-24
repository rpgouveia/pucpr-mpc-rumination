# Relatório de Experimento — Modelo 1: CNN 1D (Baseline)

**Disciplina:** Métodos de Pesquisa Científica — PUCPR 2026  
**Grupo:** Ângelo Piovezan Jorgeto, Ian Carlo Araújo Braz, Jafte Carneiro Fagundes da Silva, Nicolas Felix Hrescak, Renato Pestana de Gouveia  
**Pergunta de pesquisa:** Qual modelo de aprendizagem de máquina é mais eficaz na identificação da ruminação de vacas leiteiras?  
**Data:** Maio 2026

---

## 1. Objetivo

O presente relatório documenta a replicação do experimento de Pavlovic et al. (2021) utilizando uma Rede Neural Convolucional unidimensional (CNN 1D) como **baseline**, cujos resultados serão utilizados para comparação sistemática com o Modelo 2 (Random Forest) na etapa subsequente do experimento.

---

## 2. Dataset

| Atributo | Valor |
|----------|-------|
| Fonte | Zenodo — DOI: 10.5281/zenodo.4064801 |
| Referência | Pavlovic et al. (2021). *Sensors*, 21, 4050 |
| Animais | 18 bovinos Limousin Cross |
| Farm Trials | 3 (Reino Unido, 2015–2016) |
| Sensores | Colar Afimilk (acelerômetro) + Halter Rumiwatch (pressão) |
| Frequência | 10 Hz |
| Total de horas | 3.460 h |
| Classes | Outro (0), Ruminação (1), Comendo (2) |

---

## 3. Pipeline de Pré-processamento

### 3.1 Fusão dos dados

Os arquivos `accel-XX.csv` (features) e `halter-XX.csv` (rótulos) de cada animal foram unidos pelo timestamp por meio de um *inner join*. Verificou-se que os dois sensores, embora operem a 10 Hz, apresentam timestamps ligeiramente desalinhados: o colar exibe deriva de clock com timestamps irregulares, enquanto o halter registra em intervalos exatos de 100 ms. O alinhamento foi realizado por meio do arredondamento de ambos os fluxos de dados para a precisão de 100 ms antes da fusão.

### 3.2 Diferença discreta

Aplicada em cada eixo do acelerômetro para eliminar vieses estáticos de orientação do colar:

$$\Delta s[t] = s[t] - s[t-1], \quad \forall s \in \{x, y, z\}$$

### 3.3 Janelamento

| Parâmetro | Valor |
|-----------|-------|
| Tamanho da janela | 90 s |
| Amostras por janela | 900 (90 s × 10 Hz) |
| Rótulo da janela | Votação majoritária dos rótulos do halter |

### 3.4 Balanceamento

Aplicou-se *undersampling* por animal para igualar a representação das três classes no conjunto de treino, evitando que o modelo favoreça classes majoritárias durante o aprendizado.

### 3.5 Divisão treino / teste

| Conjunto | Animais | Janelas |
|----------|---------|---------|
| Treino/Validação | 01–03, 05–09, 12–18 (15 animais) | 65.496 |
| Teste | 04, 10, 11 (1 por farm trial) | 18.828 |

**Distribuição do conjunto de treino (após balanceamento):**

| Classe | Janelas | Proporção |
|--------|---------|-----------|
| Outro | 21.832 | 33,3% |
| Ruminação | 21.832 | 33,3% |
| Comendo | 21.832 | 33,3% |

**Distribuição do conjunto de teste (distribuição natural):**

| Classe | Janelas | Proporção |
|--------|---------|-----------|
| Outro | 9.246 | 49,1% |
| Ruminação | 6.870 | 36,5% |
| Comendo | 2.712 | 14,4% |

---

## 4. Arquitetura do Modelo

CNN 1D conforme Pavlovic et al. (2021) — Figura 5.

| Componente | Especificação |
|-----------|---------------|
| Entrada | (batch, 3, 900) — 3 eixos × 900 amostras |
| Bloco 1 | Conv1D(3→64, kernel=16, stride=1) + Dropout + BatchNorm + ReLU |
| Bloco 2 | Conv1D(64→64, kernel=16, stride=2) + Dropout + BatchNorm + ReLU |
| Bloco 3 | Conv1D(64→64, kernel=16, stride=2) + Dropout + BatchNorm + ReLU |
| Bloco 4 | Conv1D(64→512, kernel=1, stride=1) + Dropout + BatchNorm + ReLU |
| Pooling | AdaptiveAvgPool1D(1) |
| Cabeça | Linear(512→3) |
| Saída | (batch, 3) — logits para 3 classes |
| Parâmetros | 170.563 |

**Hiperparâmetros de treinamento:**

| Parâmetro | Valor |
|-----------|-------|
| Otimizador | AdamW |
| Learning rate | 1×10⁻⁴ |
| Weight decay | 0,01 |
| Batch size | 256 |
| Épocas máx. | 50 |
| Early stopping patience | 15 |
| Early stopping delta | 0,01 |

---

## 5. Protocolo de Validação

Validação cruzada GroupKFold com 5 folds agrupados por animal — cada animal aparece exatamente uma vez no conjunto de validação. O modelo com menor loss de validação dentro de cada fold é salvo via early stopping.

| Fold | Animais na validação | F1 validação |
|------|----------------------|-------------|
| 1 | 06, 16 | 0,8257 |
| 2 | 01, 12 | 0,8778 |
| 3 | 03, 15, 18 | 0,8258 |
| 4 | 02, 09, 14, 17 | 0,8355 |
| 5 | 05, 07, 08, 13 | 0,7776 |
| **Média** | | **0,8285 ± 0,0319** |
| Referência (artigo) | | 0,82 ± ~0,03 |

O Fold 2 produziu o melhor modelo de validação (F1 = 0,8778) e foi selecionado para avaliação no conjunto de teste.

---

## 6. Resultados no Conjunto de Teste

### 6.1 Métricas gerais

| Métrica | Resultado | Artigo (referência) |
|---------|-----------|---------------------|
| Accuracy | 0,827 | ~0,82 |
| Precision (macro) | 0,792 | 0,84 |
| Recall (macro) | 0,822 | 0,82 |
| **F1-score (macro)** | **0,786** | **0,82** |
| F1-score (weighted) | 0,840 | 0,82 |

### 6.2 Métricas por classe

| Classe | Precision | Recall | F1 | Support |
|--------|-----------|--------|-----|---------|
| Outro | 0,92 | 0,90 | 0,91 | 9.246 |
| Ruminação | 0,96 | 0,73 | 0,83 | 6.870 |
| Comendo | 0,49 | 0,84 | 0,62 | 2.712 |

### 6.3 Matriz de Confusão (normalizada)

|  | Previsto: Outro | Previsto: Ruminação | Previsto: Comendo |
|--|:-:|:-:|:-:|
| **Real: Outro** | **0,90** | 0,01 | 0,09 |
| **Real: Ruminação** | 0,05 | **0,73** | 0,22 |
| **Real: Comendo** | 0,13 | 0,03 | **0,84** |

---

## 7. Análise dos Resultados

### 7.1 Replicação do baseline

A média de F1 na validação cruzada (0,8285 ± 0,0319) replica com fidelidade o resultado reportado por Pavlovic et al. (F1 = 0,82 ± ~0,03), confirmando a corretude do pipeline de pré-processamento, da arquitetura e do protocolo de avaliação.

### 7.2 Diferença macro vs. weighted

O F1 macro (0,786) é inferior ao F1 weighted (0,840) porque penaliza igualmente as três classes, incluindo **Comendo** — a classe minoritária no teste (14,4%) com Precision de apenas 0,49. O artigo reporta o resultado weighted, o que explica a aparente diferença.

### 7.3 Principal padrão de erro

A maior fonte de erro identificada é a **confusão entre Ruminação e Comendo (22%)**, fenômeno documentado pelo artigo original, que atribui tal ocorrência à semelhança entre os movimentos mandibulares dos dois comportamentos (PAVLOVIC et al., 2021a). Esse padrão deverá ser observado comparativamente nos resultados do Modelo 2.

### 7.4 Variabilidade entre folds

O Fold 5, composto por quatro animais na validação, apresentou maior ruído nas curvas de aprendizado e o menor F1 (0,7776). Tal resultado evidencia que a **variabilidade inter-animal** constitui o principal desafio do problema, visto que cada animal expressa padrões comportamentais ligeiramente distintos.

---

## 8. Artefatos Gerados

| Arquivo | Localização | Conteúdo |
|---------|-------------|----------|
| `resultados_cnn.json` | `results/metrics/` | Métricas, preds, labels, f1_folds |
| `historico_cnn.csv` | `results/metrics/` | Loss e F1 por época e fold |
| `curvas_aprendizado_cnn.png` | `results/figures/` | Loss e F1 de validação por fold |
| `matriz_confusao_cnn.png` | `results/figures/` | Matriz de confusão normalizada |
| `modelo_fold1-5.pt` | `results/checkpoints/` | Pesos dos modelos por fold |

---

## 9. Continuidade do Experimento

A etapa subsequente compreende o treinamento e a avaliação do **Modelo 2 — Random Forest** (`notebooks/model2.ipynb`), com features estatísticas extraídas das mesmas janelas de 90 s, sobre o mesmo conjunto de treino e teste utilizado no presente experimento, possibilitando a comparação direta entre os dois paradigmas de aprendizagem de máquina.

---

## Referências

PAVLOVIC, D. et al. Classification of Cattle Behaviours Using Neck-Mounted Accelerometer-Equipped Collars and Convolutional Neural Networks. *Sensors*, v. 21, n. 12, p. 4050, 2021a.

PAVLOVIC, D. et al. *Precision Beef — Animal Behaviour Classification*. Zenodo, 2021b. DOI: 10.5281/zenodo.4064801.