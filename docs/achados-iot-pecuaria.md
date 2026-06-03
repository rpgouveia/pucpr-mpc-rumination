# Discussão dos Achados: IoT e Pecuária de Precisão

| | |
|---|---|
| **Disciplina** | Métodos de Pesquisa Científica — PUCPR 2026 |
| **Grupo** | Ângelo Piovezan Jorgeto, Ian Carlo Araújo Braz, Jafte Carneiro Fagundes da Silva, Nicolas Felix Hrescak, Renato Pestana de Gouveia |
| **Data** | Junho 2026 |

## 1. Introdução e Contexto da IoT na Pecuária de Precisão
A pecuária de precisão visa individualizar a gestão e maximizar a eficiência produtiva através do monitoramento contínuo da saúde metabólica do rebanho. O presente documento conecta os resultados computacionais obtidos da comparação entre os modelos de classificação (**CNN 1D** e **Random Forest**) à infraestrutura física de **Internet das Coisas (IoT)**, consolidando os achados da pesquisa e validando a viabilidade técnica e prática da solução de monitoramento automatizado da ruminação em vacas leiteiras.

## 2. Viabilidade do Acelerômetro de Colar como Sensor Definitivo
De acordo com a literatura (Pavlovic et al., 2021), o uso de **halters sensíveis à pressão** é considerado o padrão-ouro laboratorial para detecção de ruminação. Contudo, halters são intrusivos, propensos a falhas em campo e pouco viáveis economicamente para adoção em escala comercial em fazendas leiteiras. Nossos achados experimentais comprovam que **acelerômetros triaxiais**, embarcados em colares de pescoço, constituem hardwares IoT altamente competentes para substituir o halter.

A ressalva fundamental encontrada, no entanto, é que o sensor captura a movimentação mecânica de maneira ruidosa. Logo, o sucesso da IoT não reside exclusivamente no hardware, mas é altamente dependente do algoritmo de retaguarda responsável por interpretar esse sinal ruidoso.

## 3. A Riqueza Temporal dos Dados IoT vs. Limitação da Extração Manual
A instrumentação operando a uma frequência de **10 Hz** gera uma massa de dados sequenciais e contínuos (900 leituras espaciais a cada janela de 90 segundos). A implementação do modelo de **Random Forest** evidenciou as limitações estruturais da extração de características (*Feature Engineering*) manuais em cenários de IoT.

Ao reduzir os 900 registros brutos para um vetor de apenas 15 atributos estatísticos globais (como média e amplitude), houve um achatamento irreversível da assinatura temporal do sensor, suprimindo o ritmo característico da mastigação. A eficiência superior da **CNN 1D** comprova que o valor intrínseco de um dispositivo IoT biomecânico está preservado na fidelidade de sua sequência bruta de tempo real.

## 4. O Trade-off Arquitetural IoT: Nuvem (Cloud) versus Borda (Edge)
A análise comparativa entre as duas abordagens revela um dilema clássico na engenharia de arquiteturas IoT:

- **Arquitetura Centralizada em Nuvem (Cloud):** A CNN 1D exige o tráfego contínuo dos dados brutos para alcançar sua precisão superior (F1=0.786). No campo, transmitir milhares de leituras por minuto via redes sem fio para a nuvem cria gargalos de banda e acelera significativamente a degradação da bateria dos colares.

- **Processamento na Borda com Modelos Clássicos (Edge/RF):** O Random Forest possui baixa complexidade computacional para inferência. É altamente viável processar as características estatísticas localmente no microcontrolador do colar e enviar apenas alertas simplificados (ex: via LoRaWAN). Todavia, há penalidade na taxa de acerto (F1=0.731 e altas taxas de falsos positivos na classe de alimentação).

### 4.1 A Perspectiva do "Edge AI"
Como proposta arquitetural definitiva, os resultados direcionam para a adoção de metodologias de **TinyML / Edge AI**. O futuro dessa instrumentação reside em embarcar processadores otimizados (como **microcontroladores ARM Cortex-M**) capazes de executar versões compactadas da CNN 1D fisicamente no colar da vaca, equilibrando alta acurácia com máxima eficiência energética na transmissão.

## 5. Impacto Prático na Pecuária e no Bem-Estar Animal
A confusão entre "Ruminação" e "Comendo", presente em ambos os modelos (taxa de erro de 22% a 24%), reflete o limite fisiológico e de captação atual. Contudo, ao estabilizar o F1-Score da CNN em patamares próximos ao estado-da-arte, o sistema prova-se comercialmente viável como ferramenta de diagnóstico preventivo.

A detecção de uma queda brusca no tempo de ruminação via relatórios automatizados de IoT fornece ao produtor um indicativo precoce de distúrbios como a **acidose ruminal subclínica**, possibilitando intervenções nutricionais rápidas que minimizam custos veterinários e asseguram o bem-estar do rebanho.
