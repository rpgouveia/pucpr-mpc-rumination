# Relatório Comparativo: CNN 1D vs. Random Forest

**Disciplina:** Métodos de Pesquisa Científica — PUCPR 2026  
**Grupo:** Ângelo Piovezan Jorgeto, Ian Carlo Araújo Braz, Jafte Carneiro Fagundes da Silva, Nicolas Felix Hrescak, Renato Pestana de Gouveia  
**Pergunta de pesquisa:** Qual modelo de aprendizagem de máquina é mais eficaz na identificação da ruminação de vacas leiteiras?  
**Data:** Junho 2026

---

## 1. Objetivo

Este documento apresenta a análise comparativa final entre o **Modelo 1 (CNN 1D)**, representando a abordagem de *Deep Learning* com aprendizado de representações a partir de dados brutos, e o **Modelo 2 (Random Forest)**, representando o paradigma clássico de *Machine Learning* apoiado em engenharia de atributos manuais. O intuito é responder à pergunta de pesquisa sobre a eficácia na classificação comportamental, especificamente a ruminação, utilizando o dataset de Pavlovic et al. (2021).

---

## 2. Diferenças Metodológicas

A principal distinção metodológica entre os dois modelos reside na etapa de pré-processamento e extração de características:

* **Modelo 1 (CNN 1D):** O modelo processou matrizes brutas derivadas das janelas temporais de 90 segundos do acelerômetro, com a arquitetura convolucional encarregada de aprender e abstrair os padrões temporais automaticamente.
* **Modelo 2 (Random Forest):** Incapaz de processar os dados temporais brutos, o modelo exigiu **Engenharia de Características (Feature Engineering)**. Para cada janela de 90s, extraiu-se 15 features estatísticas baseadas na aceleração (Média, Desvio Padrão, Mínimo, Máximo e Amplitude em x, y, z). Além disso, não utiliza o conceito de épocas (*epochs*), mas constrói árvores até a pureza das folhas.

---

## 3. Comparativo de Desempenho (Conjunto de Teste)

A tabela abaixo sintetiza os resultados globais no conjunto de dados não vistos durante o treinamento (animais 04, 10 e 11):

| Métrica Global | CNN 1D (Modelo 1) | Random Forest (Modelo 2) | Diferença Absoluta |
| :--- | :---: | :---: | :---: |
| **Accuracy** | **0,827** | 0,764 | + 0,063 (CNN) |
| **Precision (macro)** | **0,792** | 0,744 | + 0,048 (CNN) |
| **Recall (macro)** | **0,822** | 0,783 | + 0,039 (CNN) |
| **F1-Score (macro)** | **0,786** | 0,731 | + 0,055 (CNN) |

### 3.1. Desempenho por Classe (F1-Score)

| Classe | CNN 1D | Random Forest |
| :--- | :---: | :---: |
| **Outro** | 0,91 | 0,85 |
| **Ruminação** | 0,83 | 0,78 |
| **Comendo** | 0,62 | 0,57 |

**Análise:** A CNN 1D demonstrou superioridade consistente em todas as métricas gerais e por classe. O desempenho para a identificação específica da "Ruminação" atingiu F1=0,83 na CNN, superando o RF (F1=0,78).

---

## 4. Análise Crítica dos Resultados

### 4.1. Generalização vs. Overfitting

O Random Forest apresentou um padrão nítido de **overfitting estrutural**, marcando F1=1,000 no treino em todos os *folds*, porém com uma queda drástica na validação (F1 médio ≈0,77) e no teste (F1=0,731). A capacidade ilimitada da profundidade das árvores levou o modelo a memorizar os animais do treino em vez de generalizar os padrões de aceleração. Em contraponto, a CNN 1D generalizou melhor, aproximando-se do baseline do artigo de referência (F1=0,82).

### 4.2. Padrões de Erro e Confusão

Apesar das diferenças na eficácia, ambos os modelos compartilham a mesma vulnerabilidade principal: **a confusão entre as classes "Ruminação" e "Comendo"**.

* O Random Forest confundiu instâncias reais de Ruminação prevendo-as como Comendo em **24%** dos casos.
* A CNN 1D cometeu o mesmo tipo de erro em **22%** dos casos.

Esse padrão de erro alinha-se diretamente aos achados originais de Pavlovic et al. (2021), que documentaram a extrema dificuldade em distinguir essas classes devido à alta similaridade biomecânica dos movimentos mandibulares durante a ingestão e a ruminação.

### 4.3. Limitação da Engenharia de Features

A queda de performance do Random Forest, particularmente o baixo *Precision* na classe "Comendo" (0,42), ilustra a limitação das extrações manuais. Features estatísticas puras (como a média e amplitude) ao longo de uma janela extensa de 90 segundos achatam e suprimem a riqueza do domínio temporal, inviabilizando a identificação de micropadrões de alimentação em novos animais. A CNN, extraindo features espacialmente locais através de convoluções, superou essa limitação de forma eficiente.

---

## 5. Conclusão

Respondendo à pergunta de pesquisa proposta por este estudo, conclui-se que **a Rede Neural Convolucional 1D (CNN 1D) é significativamente mais eficaz** do que o Random Forest para a identificação da ruminação e classificação comportamental geral de vacas leiteiras baseada em dados de acelerômetros de pescoço.

A abordagem baseada em *Deep Learning* demonstrou maior resiliência na generalização para animais desconhecidos e conseguiu abstrair informações espaço-temporais críticas, comprovando que, para séries temporais densas originadas de sensores biomecânicos, a extração automática de atributos supera metodologias dependentes de características estatísticas manuais.
