# Relatório de Experimento — Modelo 1: CNN 1D (Baseline)

**Disciplina:** Métodos de Pesquisa Científica — PUCPR 2026  
**Grupo:** Ângelo Piovezan Jorgeto, Ian Carlo Araújo Braz, Jafte Carneiro Fagundes da Silva, Nicolas Felix Hrescak, Renato Pestana de Gouveia  
**Pergunta de pesquisa:** Qual modelo de aprendizagem de máquina é mais eficaz na identificação da ruminação de vacas leiteiras?  
**Data:** Maio 2026

---

## 1. Objetivo

Replicar o experimento de Pavlovic et al. (2021) utilizando o modelo de treinamento Random Forest para comparação posterior com o Modelo 1 (CNN 1D).

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

Os arquivos `accel-XX.csv` (features) e `halter-XX.csv` (rótulos) de cada animal foram unidos pelo timestamp. Os sensores operam a 10 Hz com timestamps ligeiramente desalinhados — o colar apresenta deriva de clock com timestamps irregulares (ex: `.161041`, `.260490`), enquanto o halter grava em intervalos exatos de 100 ms. O alinhamento foi realizado arredondando ambos os streams para 100 ms antes do merge.


### 3.2 Diferença discreta

Aplicada em cada eixo do acelerômetro para eliminar vieses estáticos de orientação do colar:

$$\Delta s[t] = s[t] - s[t-1], \quad \forall s \in \{x, y, z\}$$

### 3.3 Janelamento

| Parâmetro | Valor |
|-----------|-------|
| Tamanho da janela | 90 s |
| Amostras por janela | 900 (90 s × 10 Hz) |
| Rótulo da janela | Votação majoritária dos rótulos do halter |

### 3.5 Divisão treino / teste

| Conjunto | Animais | Janelas |
|----------|---------|---------|
| Treino/Validação | 01–03, 05–09, 12–18 (15 animais) | 116.038 |
| Teste | 04, 10, 11 (1 por farm trial) | 23.207 |

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

## 4. Protocolo de Validação

Validação cruzada GroupKFold com 5 folds agrupados por animal — cada animal aparece exatamente uma vez no conjunto de validação. O modelo com menor loss de validação dentro de cada fold é salvo via early stopping.

── Fold 1/5  |  validação: ['06', '12'] ──
  Treino concluído | f1_tr: 1.0000 | f1_val: 0.7809
  → F1 (melhor modelo) fold 1: 0.7809

── Fold 2/5  |  validação: ['01', '18'] ──
  Treino concluído | f1_tr: 1.0000 | f1_val: 0.8050
  → F1 (melhor modelo) fold 2: 0.8050

── Fold 3/5  |  validação: ['02', '03', '17'] ──
  Treino concluído | f1_tr: 1.0000 | f1_val: 0.7914
  → F1 (melhor modelo) fold 3: 0.7914

── Fold 4/5  |  validação: ['07', '14', '15', '16'] ──
  Treino concluído | f1_tr: 1.0000 | f1_val: 0.7513
  → F1 (melhor modelo) fold 4: 0.7513

── Fold 5/5  |  validação: ['05', '08', '09', '13'] ──
  Treino concluído | f1_tr: 1.0000 | f1_val: 0.7542
  → F1 (melhor modelo) fold 5: 0.7542

  Média : 0.7766 ± 0.0209
  Referência (artigo) | | 0,82 ± ~0,03

  O Fold 2 produziu o melhor modelo de validação (F1 = 0,8050) e foi selecionado para avaliação no conjunto de teste.

---

## 6. Resultados no Conjunto de Teste

### 6.1 Métricas gerais

 Métricas no Conjunto de Teste (Random Forest - Melhor Fold) ══
  Accuracy  : 0.7642
  Precision : 0.7435
  Recall    : 0.7826
  F1 (macro): 0.7318
  (Artigo   : Precision=0.84 | Recall=0.82 | F1=0.82)

### 6.2 Métricas por classe
              precision    recall  f1-score   support

       Outro       0.92      0.79      0.85      9246
   Ruminação       0.88      0.69      0.78      6870
     Comendo       0.42      0.87      0.57      2712

## 7. Comparação com CNN 1D
O Modelo 1 (CNN 1D) superou o Modelo 2 (Random Forest). O gráfico de barras revelou que o Random Forest sofreu forte overfitting, atingindo F1=1.0 no treino, mas falhando em generalizar tão bem para novos animais (média em torno de 0.78). Isso prova que a CNN, por conseguir analisar o 'formato contínuo da onda' temporal (através das convoluções), extrai padrões de comportamento de forma muito mais genérica e robusta do que usar características estatísticas isoladas (média, variância) no Random Forest.