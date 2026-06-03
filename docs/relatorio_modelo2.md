# Relatório de Experimento — Modelo 2: Random Forest

**Disciplina:** Métodos de Pesquisa Científica — PUCPR 2026  
**Grupo:** Ângelo Piovezan Jorgeto, Ian Carlo Araújo Braz, Jafte Carneiro Fagundes da Silva, Nicolas Felix Hrescak, Renato Pestana de Gouveia  
**Pergunta de pesquisa:** Qual modelo de aprendizagem de máquina é mais eficaz na identificação da ruminação de vacas leiteiras?  
**Data:** Junho 2026

---

## 1. Objetivo

O presente relatório documenta o treinamento e a avaliação do Modelo 2 — Random Forest — para comparação direta com o Modelo 1 (CNN 1D). O Random Forest representa o paradigma de aprendizado de máquina clássico e opera sobre features estatísticas extraídas manualmente das janelas temporais, em contraste com a CNN 1D, que aprende representações automaticamente a partir dos dados brutos.

---

## 2. Dataset

| Atributo | Valor |
|----------|-------|
| Fonte | Zenodo — DOI: 10.5281/zenodo.4064801 |
| Referência | Pavlovic et al. (2021b) |
| Animais | 18 bovinos Limousin Cross |
| Farm Trials | 3 (Reino Unido, 2015–2016) |
| Sensores | Colar Afimilk (acelerômetro) + Halter Rumiwatch (pressão) |
| Frequência | 10 Hz |
| Total de horas | 3.460 h |
| Classes | Outro (0), Ruminação (1), Comendo (2) |

---

## 3. Pipeline de Pré-processamento

### 3.1 Fusão dos dados

Os arquivos `accel-XX.csv` (features) e `halter-XX.csv` (rótulos) de cada animal foram unidos pelo timestamp por meio de um *inner join*. Os sensores operam a 10 Hz com timestamps ligeiramente desalinhados — o colar apresenta deriva de clock com timestamps irregulares, enquanto o halter grava em intervalos exatos de 100 ms. O alinhamento foi realizado por meio do arredondamento de ambos os fluxos de dados para a precisão de 100 ms antes da fusão.

### 3.2 Diferença discreta

Aplicada em cada eixo do acelerômetro para eliminar vieses estáticos de orientação do colar:

$$\Delta s[t] = s[t] - s[t-1], \quad \forall s \in \{x, y, z\}$$

### 3.3 Janelamento

| Parâmetro | Valor |
|-----------|-------|
| Tamanho da janela | 90 s |
| Amostras por janela | 900 (90 s × 10 Hz) |
| Rótulo da janela | Votação majoritária dos rótulos do halter |

### 3.4 Engenharia de features

O Random Forest não opera sobre dados brutos. Para cada janela de 90 s, foram extraídos atributos estatísticos por eixo do acelerômetro, resultando em um vetor de 15 features:

| Feature | Eixos |
|---------|-------|
| Média | x, y, z |
| Desvio padrão | x, y, z |
| Mínimo | x, y, z |
| Máximo | x, y, z |
| Amplitude (Max - Min) | x, y, z |

### 3.5 Balanceamento

Aplicou-se *undersampling* por animal para igualar a representação das três classes no conjunto de treino.

### 3.6 Divisão treino / teste

| Conjunto | Animais | Janelas |
|----------|---------|---------|
| Treino/Validação | 01–03, 05–09, 12–18 (15 animais) | 65.496 (balanceado) |
| Teste | 04, 10, 11 (1 por farm trial) | 18.828 (distribuição natural) |

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

## 4. Configuração do Modelo

O Random Forest foi instanciado com os parâmetros padrão da biblioteca `scikit-learn`, utilizando 100 estimadores (`n_estimators=100`) e critério de divisão baseado na impureza de Gini. A profundidade máxima das árvores não foi restrita (`max_depth=None`), o que permite que os nós se expandam até que todas as folhas sejam puras, justificando o *overfitting* absoluto na base de treino. Por ser um algoritmo base que cria árvores até a pureza máxima dadas essas configurações, o treinamento é concluído em uma única etapa, sem *early stopping*.

---

## 5. Protocolo de Validação

Validação cruzada GroupKFold com 5 folds agrupados por animal — cada animal aparece exatamente uma vez no conjunto de validação. O modelo com maior F1 de validação é selecionado para avaliação no conjunto de teste.

| Fold | Animais na validação | F1 treino | F1 validação |
|------|----------------------|-----------|-------------|
| 1 | 06, 12 | 1,0000 | 0,7809 |
| 2 | 01, 18 | 1,0000 | **0,8050** |
| 3 | 02, 03, 17 | 1,0000 | 0,7914 |
| 4 | 07, 14, 15, 16 | 1,0000 | 0,7513 |
| 5 | 05, 08, 09, 13 | 1,0000 | 0,7542 |
| **Média** | | **1,0000** | **0,7766 ± 0,0209** |

O F1 igual a 1,000 no conjunto de treino em todos os folds indica overfitting estrutural. O Fold 2 produziu o melhor modelo de validação (F1 = 0,8050) e foi selecionado para avaliação no conjunto de teste.

---

## 6. Resultados no Conjunto de Teste

### 6.1 Métricas gerais

| Métrica | Resultado | Artigo (referência — CNN) |
|---------|-----------|--------------------------|
| Accuracy | 0,764 | ~0,82 |
| Precision (macro) | 0,744 | 0,84 |
| Recall (macro) | 0,783 | 0,82 |
| **F1-score (macro)** | **0,731** | **0,82** |

### 6.2 Métricas por classe

| Classe | Precision | Recall | F1 | Support |
|--------|-----------|--------|-----|---------|
| Outro | 0,92 | 0,79 | 0,85 | 9.246 |
| Ruminação | 0,88 | 0,69 | 0,78 | 6.870 |
| Comendo | 0,42 | 0,87 | 0,57 | 2.712 |

---

## 7. Análise dos Resultados

### 7.1 Overfitting estrutural

O padrão de F1=1,000 no treino e F1≈0,78 na validação em todos os folds evidencia o *overfitting* do modelo, decorrente do hiperparâmetro de profundidade livre nas árvores. O modelo memorizou as combinações de features estatísticas específicas dos animais de treino, mas não construiu representações suficientemente generalizadas para novos indivíduos com padrões de aceleração distintos.

### 7.2 Desempenho por classe

A classe **Comendo** apresenta o menor F1 (0,57), com Precision de apenas 0,42 — o modelo tende a prever "Comendo" com muita frequência, incorrendo em uma alta taxa de Falsos Positivos. Isso ocorre porque as features estatísticas puras de aceleração (média, desvio padrão, min/max e amplitude) extraídas de janelas longas (90s) perdem a riqueza do domínio temporal, não conseguindo distinguir com precisão os padrões de alimentação de novos animais em relação aos demais comportamentos.

### 7.3 Padrão de erro

Conforme evidenciado pela matriz de confusão gerada para o conjunto de teste, o principal padrão de erro recai sobre instâncias reais de **Ruminação** sendo classificadas incorretamente como **Comendo**, atingindo uma taxa expressiva de **24% (0.24)**. Este comportamento não apenas aproxima-se dos padrões de erro observados na CNN 1D, como também corrobora os achados do artigo original (PAVLOVIC et al., 2021a), que atribui essa dificuldade classificatória à forte similaridade biomecânica dos movimentos mandibulares cíclicos presentes durante ambos os comportamentos.

### 7.4 Variabilidade entre folds

O desvio padrão do F1 de validação (0,0209) é menor que o da CNN 1D, porém isso não indica melhor generalização. O F1 absoluto do RF é sistematicamente mais baixo e a menor variância decorre simplesmente da estabilidade da "memorização" (árvores expandidas até a pureza) nos dados de treino, gerando tetos de validação limitados e consistentes, mas não robustos frente a novos animais.

---

## 8. Artefatos Gerados

| Arquivo | Localização | Conteúdo |
|---------|-------------|----------|
| `resultados_rf.json` | `results/metrics/` | Métricas, preds, labels, f1_folds |
| `historico_rf.csv` | `results/metrics/` | F1 treino e validação por fold |
| `desempenho_folds_rf.png` | `results/figures/` | F1 treino vs. validação por fold |
| `matriz_confusao_rf.png` | `results/figures/` | Matriz de confusão no conjunto de teste |

---

## 9. Continuidade do Experimento

Os resultados do Modelo 2 são consolidados com os do Modelo 1 no relatório comparativo (`docs/relatorio_comparativo.md`), onde a análise quantitativa e qualitativa das diferenças entre os dois paradigmas é apresentada de forma sistemática.

---

## Referências

PAVLOVIC, D. et al. Classification of Cattle Behaviours Using Neck-Mounted Accelerometer-Equipped Collars and Convolutional Neural Networks. *Sensors*, v. 21, n. 12, p. 4050, 2021a.

PAVLOVIC, D. et al. *Precision Beef — Animal Behaviour Classification*. Zenodo, 2021b. DOI: 10.5281/zenodo.4064801. Disponível em: https://doi.org/10.5281/zenodo.4064801.
