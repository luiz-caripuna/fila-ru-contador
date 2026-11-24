# Relatório Técnico: Aferição, Modelagem e Simulação das Filas do Restaurante Universitário

**Disciplina:** Avaliação de Desempenho de Sistemas  
**Tema:** Aferição em Campo, Modelagem Estocástica ($M/M/c$) e Simulação Discreta Guiada por Traço (*Trace-Driven DES*) das Filas do Restaurante Universitário (RU Central)  
**Data da Coleta Definitiva:** 04 de Novembro de 2026 (Duração observada: 65,34 minutos)  
**Equipe Responsável:**
* **Adriana** — Introdução, Contextualização Operacional, Relato de Campo e Conclusão Geral
* **Lucas** — Aferição (Método, Engenharia de Software e Operação de Coleta Móvel)
* **Jaiane** — Aferição (Resultados Empíricos, Análise Calma vs. Pico e Dispersão Estatística)
* **Otávio** — Modelagem Teórica (Espaço de Estados, Cadeias de Markov, Matriz P e Lei de Little)
* **Vanessa** — Simulação Computacional (Motor DES, Validação de Baseline e Cenários *What-If*)

---

## Resumo Executivo

Este trabalho apresenta um estudo experimental e analítico completo sobre o comportamento das filas de atendimento do Restaurante Universitário (RU Central), integrando aferição empírica em tempo real, modelagem matemática fundamentada na Teoria das Filas e simulação de eventos discretos (*Discrete Event Simulation - DES*).

A investigação monitorou o fluxo contínuo dos estudantes ao longo de três filas sequenciais: **Fila 1 (Entrada → Catraca)**, **Fila 2 (Catraca → Buffet de Atendimento)** e **Fila 3 / Salão (Mesas de Refeição → Saída)**. A coleta foi realizada com auxílio do sistema autônomo **Fila RU**, uma aplicação web *offline-first* desenvolvida pela equipe em JavaScript nativo sobre rede Wi-Fi local própria, eliminando a dependência de internet e mitigando erros de anotação manual.

Em 65,34 minutos de observação contínua, foram catalogados **1.074 eventos pontuais** e **192 estudantes atendidos**. O estudo comprovou que a sobrecarga do sistema concentra-se no intervalo de pico entre os minutos 30 e 50 da coleta, momento em que a taxa de chegada ($\lambda \approx 3,80\text{ pessoas/min}$) superou a capacidade de serviço da catraca de entrada ($\mu \approx 3,32\text{ pessoas/min}$), elevando o fator de utilização para $\rho > 1,12$ e gerando uma fila de até 51 alunos na calçada com espera de 90º percentil superior a 9 minutos.

A modelagem estocástica validou com alta precisão a **Lei de Little** na Fila 2, exibindo divergência de apenas **3,48%** ($L_q^{\text{obs}} = 6,72$ vs $\lambda W_q = 6,96$), e explicou analiticamente o transitório inicial da Fila 1. Por fim, o motor de simulação por eventos discretos guiado por traço histórico (calibrado com aderência de **0,27%** no baseline) comprovou o fenômeno do **Deslocamento de Gargalo (*Bottle-neck Shifting*)**: a instalação isolada de uma 2ª catraca reduz o tempo na entrada em 58%, mas transfere a retenção para o buffet, cuja espera sobe 45% (pico de 48 alunos no corredor). A solução ótima comprovada consiste na ativação simultânea da **2ª catraca combinada a uma 2ª linha de buffet**, o que reduz o tempo médio de retenção até as mesas em **63%** (de quase 5 minutos para 1,7 minuto), sendo perfeitamente suportada pela capacidade física do salão (216 cadeiras).

---

## 1. Introdução, Contextualização Operacional e Relato de Campo
*(Responsável: Adriana)*

### 1.1 O Desafio Operacional do Restaurante Universitário
O Restaurante Universitário desempenha papel crucial na permanência estudantil, fornecendo refeições balanceadas para milhares de discentes, docentes e servidores técnicos. No entanto, a alta concentração de demanda nos horários de intervalo de aulas (especialmente entre 11h45 e 12h30) impõe severo estresse sobre a infraestrutura de atendimento.

A formação de longas filas na entrada não decorre apenas de lentidão na catraca, mas sim da interação dinâmica entre múltiplos subsistemas interligados em série. Uma abordagem simplista de gestão costuma propor soluções isoladas (como "abrir mais uma catraca") sem compreender o efeito sistêmico no restante do refeitório. O propósito deste projeto é transformar a observação empírica em evidência quantitativa de engenharia, respondendo com rigor às perguntas: **Quando o sistema satura? Quanto tempo o aluno perde na fila? E Por Quê o gargalo se forma?**

### 1.2 Topologia Física das Três Filas e o Salão de Mesas
O fluxo de atendimento do RU Central foi modelado a partir de três zonas funcionais sequenciais com encadeamento contínuo:

```
[Chegada na Calçada]
         │
         ▼
 ┌───────────────┐
 │    FILA 1     │   Identificação / Validação na Catraca (Vermelha)
 └───────┬───────┘
         │ Encadeamento Atômico (1 > 2)
         ▼
 ┌───────────────┐
 │    FILA 2     │   Linha de Servir / Buffet e Bandejas (Verde)
 └───────┬───────┘
         │ Encadeamento Atômico (2 > 3)
         ▼
 ┌───────────────┐
 │ SALÃO & MESAS │   Capacidade Nominal: 216 cadeiras (36 mesas x 6 cadeiras)
 └───────┬───────┘
         │ Fluxo Contínuo de Descarte de Bandejas
         ▼
 ┌───────────────┐
 │    FILA 3     │   Porta de Saída do Restaurante (Rosa)
 └───────────────┘
```

1. **Fila 1 (Entrada → Catraca):** Zona externa de espera física na calçada. Modela o tempo despendido até a identificação na catraca eletrônica / guichê. Cor de controle: **Vermelha**.
2. **Fila 2 (Catraca → Atendimento/Buffet):** Zona interna ao longo do corredor de distribuição. O estudante pega a bandeja, prato, talheres e se serve no balcão térmico. Cor de controle: **Verde**.
3. **Salão de Mesas:** Área de refeição com capacidade nominal catalogada de **216 cadeiras**, dispostas em **4 fileiras de 9 mesas**, sendo **6 cadeiras por mesa (36 mesas no total)**.
4. **Fila 3 / Saída (Mesas → Porta Externa):** Modela o efluxo contínuo dos alunos que encerram a refeição, depositam as bandejas nos carrinhos de descarte e deixam o prédio. Cor de controle: **Rosa**.

### 1.3 Relato de Campo e Diário de Bordo da Equipe
Para cumprir a exigência do plano de trabalho e a diretriz pedagógica do docente de realizar a aferição durante uma janela representativa de 1 hora, a equipe organizou duas expedições de campo:

* **Primeira Expedição (21/10/2026):**
  A equipe compareceu ao RU no horário do almoço. Contudo, coincidiu de estar ocorrendo um grande evento acadêmico integrado no campus universitário, o que atraiu visitantes externos e alterou os horários usuais das turmas. A fila apresentou oscilações anômalas não representativas da rotina normal. Constatou-se também que os operadores precisavam de melhorias de ergonomia nos botões móveis para evitar cliques duplos acidentais na tela sob sol intenso. A equipe decidiu abortar aquela medição e dedicar a semana seguinte a aprimoramentos técnicos de software.
* **Segunda Expedição e Coleta Definitiva (04/11/2026):**
  Após validação das novas versões do software e testes de bancada, a equipe retornou ao RU Central em 04/11/2026 às 11h20. Montou-se a central com o notebook do coordenador no salão e os operadores conectaram-se ao hotspot Wi-Fi local. Como quatro membros puderam estar presentes em campo no momento, a distribuição física dos postos operacionais foi estruturada da seguinte forma:
  * **Operador 1 (Lucas):** Posicionado na cauda da Fila 1 (calçada externa), registrando cada estudante que chegava para entrar na fila.
  * **Operador 2 (Adriana):** Posicionada imediatamente ao lado da catraca de entrada, registrando o instante exato em que o estudante liberava o giro da catraca.
  * **Operador 3 (Jaiane):** Posicionada ao final do balcão do buffet, marcando o instante em que o estudante pegava o prato com a refeição e caminhava em direção às mesas.
  * **Operador 4 (Vanessa):** Posicionada na área de descarte de bandejas / porta de saída, marcando a saída definitiva de cada usuário do RU.
  *(Otávio atuou no suporte à infraestrutura da rede de dados e preparação do modelo matemático).*

A coleta teve início às 11h30 (timestamp `1793823918492` ms) e encerrou-se após 65,34 minutos de monitoramento ininterrupto (`1793827838878` ms), totalizando **1.074 eventos gravados** e capturando com absoluta fidelidade a transição entre o início calmo, o pico estrangulante e o início do esvaziamento.

---

## 2. Método de Aferição e Engenharia de Software
*(Responsável: Lucas)*

### 2.1 Arquitetura Tecnológica Autônoma (*Offline-First*)
A coleta de dados em ambientes universitários frequentemente falha devido à instabilidade do sinal de internet móvel (4G/5G) dentro de refeitórios de concreto e alvenaria densa. Para eliminar completamente esse risco, foi projetada uma arquitetura computacional *zero-cloud* e *offline-first*:

* **Servidor Central no Notebook:** Implementado em **Node.js nativo (ES Modules)**, utilizando apenas a biblioteca de baixo nível `ws` para comunicação via WebSockets e gerador de QR Code no terminal. O notebook acionou o Hotspot móvel local do sistema operacional Windows no IP `192.168.137.1:3000`.
* **Sem Necessidade de Internet Externa:** Todo o tráfego de dados trafegou exclusivamente na rede Wi-Fi local sem fio entre os smartphones e o notebook.
* **Paradigma de Event Sourcing Append-Only:** O sistema não salva estados estáticos mutáveis. Cada interação do operador gera um evento atômico imutável persistido sequencialmente em `dados/.../eventos.jsonl`. O estado do sistema em qualquer milissegundo $t$ é formalmente derivado por função pura:
  $$\text{Estado}(t) = \text{derivarEstado}(\text{Eventos}, t)$$
  Esse desenho permitiu implementar um reprodutor temporal (*Replay*) completo com avanços em 1x, 5x, 10x e 60x no painel de análise.

### 2.2 Coletor Mobile Ergonômico (`celular.html` / `celular.js`)
A interface dos smartphones foi desenvolvida com foco estrito na ergonomia do operador sob estresse em campo:

1. **Botões Táteis Gigantes:** Ocupando mais de 60% da tela do aparelho, permitindo toque preciso com apenas um dos polegares, sem que o pesquisador precisasse tirar os olhos da fila física para olhar para o teclado.
2. **Perfis Especializados por Posto:**
   - *Somente Chegadas:* Apresenta unicamente o botão vermelho "CHEGADA".
   - *Somente Atendimentos:* Apresenta o botão "PASSOU NA CATRACA" indicando em tempo real o ID da próxima pessoa a ser atendida.
3. **Mecanismos de Salvaguarda e Tolerância a Falhas:**
   - *Reverter Último:* Caso o operador clicasse por engano na catraca antes do aluno passar, um clique no botão de reversão recolocava imediatamente o estudante na cabeça da fila, emitindo o evento de compensação no log.
   - *Anulação ($\times$):* Caso um estudante desistisse da fila e fosse embora, o operador anulava aquela posição sem corromper as contagens de serviço.
   - *Fila Offline no LocalStorage:* Caso o operador se afastasse temporariamente do alcance do rádio Wi-Fi, o script armazenava os eventos localmente no navegador e os transmitia em rajada ao reconectar com a flag `tardio: true`, preservando os timestamps cronológicos originais.
   - *PIN de Proteção e Idempotência:* Autenticação por PIN de 4 dígitos gerado no início da sessão e rejeição de comandos repetidos duplicados via `clientEventId`.

### 2.3 Encadeamento Atômico Multi-Filas
Para garantir que a passagem por uma etapa gerasse a entrada imediata na seguinte sem necessidade de re-digitação, o servidor implementou o **Encadeamento Atômico**:

$$\text{Saída}(\text{Fila}_1, \text{Pessoa } k, t) \implies \text{Entrada}(\text{Fila}_2, \text{Pessoa } k, t)$$
$$\text{Saída}(\text{Fila}_2, \text{Pessoa } k, t) \implies \text{Entrada}(\text{Salão/Fila}_3, \text{Pessoa } k, t)$$

A mesma numeração de identificação da pessoa ($k$) e o mesmo instante de relógio ($t$) foram preservados ao longo de todo o percurso. Isso tornou possível calcular não apenas as esperas locais de cada fila isolada, mas também os indicadores combinados executivos:
* $T_{\text{trânsito, mesas}}$: Tempo decorrido desde a chegada na calçada externa até sentar à mesa com a comida ($W_{q1} + W_{q2}$).
* $T_{\text{permanência, total}}$: Tempo integral gasto no campus do RU, da calçada até a porta de saída.

---

## 3. Resultados Experimentais e Análise de Tráfego
*(Responsável: Jaiane)*

### 3.1 Tabulação Consolidada das Filas
A sessão de coleta teve duração observada efetiva de **65,34 minutos** (1,089 horas). A Tabela 1 consolida os indicadores globais extraídos do log de eventos:

**Tabela 1: Resumo Experimental Consolidado da Sessão de 04/11/2026**

| Indicador Operacional | Fila 1 (Entrada → Catraca) | Fila 2 (Buffet / Serviço) | Fila 3 (Salão / Saída) | Unidade |
| :--- | :---: | :---: | :---: | :---: |
| **Entradas Efetivas ($n_e$)** | 192 (202 c/ anuladas) | 192 | 185 | pessoas |
| **Saídas Efetivas ($n_s$)** | 192 | 185 | 95 | pessoas |
| **Alunos Anulados (Desistências)** | 10 | 0 | 0 | pessoas |
| **Pessoas Remanescentes ao Final** | 0 | 7 | 90 (almoçando) | pessoas |
| **Taxa Média de Chegadas ($\lambda$)** | **2,94** | **2,94** | **2,83** | pessoas/min |
| **Capacidade de Atendimento ($\mu$)** | **3,32** | **3,72** | **2,13** | pessoas/min |
| **Vazão Operacional Real** | 3,30 | 3,72 | 2,13 | pessoas/min |
| **Fator de Utilização ($\rho$)** | **0,886 (88,6%)** | **0,791 (79,1%)** | **1,328 (132,8%)** | — |
| **Espera Média na Fila ($W_q$)** | **131,5 s (2m 11s)** | **142,1 s (2m 22s)** | **1.391,9 s (23m 12s)**| segundos |
| **Mediana da Espera** | 27,4 s (0m 27s) | 132,9 s (2m 13s) | 1.421,9 s (23m 42s)| segundos |
| **Desvio Padrão Amostral ($DP$)** | 225,3 s (3m 45s) | 74,3 s (1m 14s) | 352,5 s (5m 52s) | segundos |
| **90º Percentil (P90)** | **542,0 s (9m 02s)** | **236,4 s (3m 56s)** | **1.802,0 s (30m 02s)**| segundos |
| **95º Percentil (P95)** | **664,4 s (11m 04s)**| **260,1 s (4m 20s)** | **1.920,0 s (32m 00s)**| segundos |
| **Pior Espera Observada (Máx)** | **978,0 s (16m 18s)**| **421,4 s (7m 01s)** | **2.215,0 s (36m 55s)**| segundos |
| **Comprimento Médio da Fila ($L_q$)** | **12,65** | **6,72** | — (fluxo contínuo) | pessoas |
| **Pico Físico da Fila** | **51 pessoas** | **19 pessoas** | — | pessoas |

### 3.2 Separação Metodológica entre Calma e Pico pelas Chegadas
Conforme exigido pelo checklist metodológico da disciplina, **a separação entre o regime de calma e o regime de pico deve ser estabelecida pela taxa de chegadas por minuto ($\lambda$), e jamais pelas ondas visuais da fila**. A análise puramente visual da fila pode iludir o pesquisador, pois a fila física pode continuar grande mesmo quando as chegadas cessam (devido à lentidão de serviço ou represamentos anteriores).

Para analisar o fluxo, a sessão foi segmentada em blocos discretos de 5 minutos, conforme sintetizado na Tabela 2:

**Tabela 2: Série Temporal por Blocos de 5 Minutos (Fila 1 - Entrada)**

| Bloco | Janela Temporal | Chegadas no Bloco | Taxa $\lambda$ (p/min) | Atendimentos Catraca | Regime Identificado |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **B1** | 00:00 – 05:00 | 4 | 0,80 | 0 | **Calma Inicial** |
| **B2** | 05:00 – 10:00 | 2 | 0,40 | 0 | **Calma Inicial** |
| **B3** | 10:00 – 15:00 | 12 | 2,40 | 12 | Regime Moderado |
| **B4** | 15:00 – 20:00 | 8 | 1,60 | 28 (desafogo) | Regime Moderado |
| **B5** | 20:00 – 25:00 | 9 | 1,80 | 29 (desafogo) | Regime Moderado |
| **B6** | 25:00 – 30:00 | 11 | 2,20 | 6 | Regime Moderado |
| **B7** | 30:00 – 35:00 | 17 | 3,40 | 20 | **Pico Central ($\lambda > \mu$)** |
| **B8** | 35:00 – 40:00 | 19 | **3,80** | 18 | **Pico Central ($\lambda > \mu$)** |
| **B9** | 40:00 – 45:00 | 19 | **3,80** | 19 | **Pico Central ($\lambda > \mu$)** |
| **B10**| 45:00 – 50:00 | 19 | **3,80** | 18 | **Pico Central ($\lambda > \mu$)** |
| **B11**| 50:00 – 55:00 | 11 | 2,20 | 13 | Calmaria Intermediária |
| **B12**| 55:00 – 60:00 | 15 | 3,00 | 14 | Repique de Pico |
| **B13**| 60:00 – 65:00 | 19 | **3,80** | 15 | **Pico Final ($\lambda > \mu$)** |
| **B14**| 65:00 – 65:20 | 2 | — | 2 | Fechamento |

**Diagnóstico Quantitativo das Fases:**
1. **Regime de Calma (Minutos 0 a 10):** Chegaram apenas 6 alunos em 10 minutos ($\lambda_{\text{calma}} = 0,60\text{ p/min}$). A catraca operou com folga ociosa extrema ($\rho \approx 0,18$).
2. **Regime de Pico (Minutos 30 a 50 e Bloco B13):** As chegadas estabilizaram no patamar contínuo de 19 alunos a cada 5 minutos ($\lambda_{\text{pico}} = 3,80\text{ p/min}$).
   Como a capacidade técnica da catraca é de $\mu = 3,32\text{ p/min}$, ocorreu a inversão estocástica crítica:
   $$\lambda_{\text{pico}} > \mu \implies \rho = \frac{3,80}{3,32} = 1,145 > 1,0$$
   Nesta condição de superutilização temporária, o sistema tornou-se não estacionário e a fila acumulou deterministicamente, gerando o pico de 51 pessoas na calçada.

### 3.3 Dinâmica das Mesas e Tempo de Refeição
Ao contrário do que se supunha antes da medição, o salão de mesas não se tornou o gargalo limitante durante o período aferido:
* Capacidade física total: **216 cadeiras** (36 mesas $\times$ 6 assentos).
* Pico máximo de assentos ocupados simultaneamente: **116 cadeiras** (53,7% da lotação máxima, status *Moderado*).
* Média ponderada de ocupação: **53,2 cadeiras** (24,6% de ocupação média).
* Tempo médio de permanência nas mesas (almoço e conversa): **23 minutos e 12 segundos** ($1.391,9\text{ s}$, com mediana de $1.421,9\text{ s}$).
* Ao encerramento da sessão de 65 minutos, 90 estudantes ainda permaneciam sentados almoçando, o que explica por que a Fila 3 registrou 185 entradas mas apenas 95 saídas no intervalo de 1 hora.

---

## 4. Modelagem Matemática e Teoria das Filas
*(Responsável: Otávio)*

### 4.1 Definição do Espaço de Estados e do Processo
Para analisar o comportamento sob a ótica analítica clássica da Pesquisa Operacional, cada fila foi modelada como um processo estocástico em tempo contínuo:
* **Espaço de Estados:** O estado $N(t) \in \{0, 1, 2, \dots, K\}$ representa a quantidade de estudantes no subsistema no instante $t$ (incluindo o que está sendo atendido).
* **Taxa de Chegada ($\lambda$):** Processo pontual com chegadas a taxa média $\lambda$, modelado sob hipótese poissoniana de intervalos exponenciais.
* **Taxa de Atendimento ($\mu$):** Capacidade de processamento do posto por minuto ($\mu = 1 / \bar{t}_{\text{serviço}}$).
* **Capacidade $K$:** Para a Fila 1 e Fila 2, considerou-se $K = \infty$ (espaço de calçada e corredor amplo). Para as Mesas, capacidade finita $K = 216$.

### 4.2 Matriz de Transição Estocástica $P$
Discretizando o tempo por um incremento infinitesimal $\Delta t$ tal que $(\lambda + \mu)\Delta t < 1$, o sistema é governado por uma Cadeia de Markov de Nascimento e Morte. A Matriz de Transição de Probabilidades $P$ possui estrutura tridiagonal:

$$P = \begin{pmatrix}
1 - \lambda \Delta t & \lambda \Delta t & 0 & 0 & \dots & 0 \\
\mu \Delta t & 1 - (\lambda + \mu)\Delta t & \lambda \Delta t & 0 & \dots & 0 \\
0 & \mu \Delta t & 1 - (\lambda + \mu)\Delta t & \lambda \Delta t & \dots & 0 \\
0 & 0 & \ddots & \ddots & \ddots & \vdots \\
0 & 0 & \dots & \mu \Delta t & 1 - (\lambda + \mu)\Delta t & \lambda \Delta t \\
0 & 0 & \dots & 0 & \mu \Delta t & 1 - \mu \Delta t
\end{pmatrix}$$

As equações de balanço de fluxo para cada estado $n$ no regime estacionário impõem que o fluxo de entrada deve ser igual ao fluxo de saída do corte:
$$\lambda P_n = \mu P_{n+1} \implies P_{n+1} = \left(\frac{\lambda}{\mu}\right) P_n = \rho P_n$$

Aplicando a condição de normalização $\sum_{n=0}^{\infty} P_n = 1$ para $\rho < 1$:
$$P_0 = 1 - \rho \quad \text{e} \quad P_n = (1 - \rho)\rho^n$$

### 4.3 Fórmulas Analíticas do Modelo $M/M/1$
A partir da distribuição $P_n$, derivam-se as equações teóricas de desempenho:
1. **Fator de Utilização:** $\rho = \frac{\lambda}{\mu}$
2. **Número Médio no Sistema:** $L = \sum_{n=0}^{\infty} n P_n = \frac{\rho}{1 - \rho} = \frac{\lambda}{\mu - \lambda}$
3. **Número Médio na Fila de Espera:** $L_q = \sum_{n=1}^{\infty} (n - 1) P_n = \frac{\rho^2}{1 - \rho} = \frac{\lambda^2}{\mu(\mu - \lambda)}$
4. **Tempo Médio de Espera na Fila:** $W_q = \frac{L_q}{\lambda} = \frac{\rho}{\mu - \lambda}$
5. **Tempo Médio Total no Sistema:** $W = W_q + \frac{1}{\mu} = \frac{1}{\mu - \lambda}$

**Aplicação aos Parâmetros Médios da Fila 1:**
Com $\lambda = 2,938\text{ p/min}$ e $\mu = 3,317\text{ p/min}$ ($\rho = 0,886$):
* $P_0 = 1 - 0,886 = 0,114$ (Probabilidade de catraca vazia = 11,4%)
* $L_q^{\text{teórico}} = \frac{0,886^2}{1 - 0,886} = 6,88\text{ pessoas}$
* $W_q^{\text{teórico}} = \frac{6,88}{2,938} = 2,34\text{ min} = 140,56\text{ segundos}$
* $L^{\text{teórico}} = 7,77\text{ pessoas}$
* $W^{\text{teórico}} = 158,65\text{ segundos}$

### 4.4 Verificação Experimental Formal via Lei de Little
A **Lei de Little** ($L = \lambda W$ e $L_q = \lambda W_q$) é um dos teoremas mais fundamentais da engenharia de tráfego, sendo válida para qualquer disciplina de atendimento e qualquer distribuição estocástica, desde que o sistema atinja o regime estacionário.

O confronto entre a métrica observada em campo (calculada por integração ponderada no tempo $L_q = \frac{1}{T}\int_0^T n(t)dt$) e o produto analítico $(\lambda \cdot W_q)$ revelou resultados altamente esclarecedores:

**Tabela 3: Verificação Experimental da Lei de Little**

| Fila Aferida | $L_q$ Observado (Integração) | $\lambda$ Empírico | $W_q$ Médio Real | $\lambda \cdot W_q$ Calculado | Divergência Relativa ($\Delta\%$) | Avaliação de Consistência |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Fila 2 (Buffet / Serviço)** | **6,72 alunos** | 2,938 p/min | 2,369 min (142,1s) | **6,96 alunos** | **3,48%** | **Altamente Consistente ($\le 5\%$)** |
| **Fila 1 (Entrada / Catraca)** | **12,65 alunos** | 2,938 p/min | 2,192 min (131,5s) | **6,44 alunos** | **49,08%** | Divergência por Transitório Inicial |

**Justificativa Teórica da Divergência na Fila 1:**
A divergência de 49% na Fila 1 decorre diretamente do fenômeno do **Regime Transitório Inicial**. Conforme anotado no log do coletor, às 11h30 já havia 27 alunos acumulados em pé na calçada aguardando a abertura da catraca. 
A integral de $L_q$ acumula a área sob essa curva elevada desde o segundo zero. Contudo, a Lei de Little assume que o sistema opera em regime estacionário onde as condições iniciais foram esquecidas. Quando a equipe calcula a Lei de Little isolando a janela de operação contínua após a dissipação do bloco inicial, o desvio decai para patamares inferiores a 8%, confirmando a validade das formulações.

---

## 5. Simulação de Eventos Discretos (*Trace-Driven DES*) e Análise de Cenários *What-If*
*(Responsável: Vanessa)*

### 5.1 Concepção do Simulador de Eventos Discretos
Para responder aos questionamentos de dimensionamento operacional levantados pela comunidade acadêmica, foi desenvolvido o motor de simulação contido em `shared/simulador.js`.

Ao invés de adotar uma simulação puramente sintética baseada em geradores pseudoaleatórios com parâmetros genéricos, o sistema implementa uma **Simulação Guiada por Traço Histórico (*Trace-Driven Simulation*)**:
1. **Preservação Integral das Chegadas:** O vetor exato de timestamps em que cada um dos 192 alunos chegou na Fila 1 em 04/11/2026 é injetado diretamente na simulação. As ondas e pausas reais são mantidas inalteradas.
2. **Desacoplamento do Tempo Puro de Atendimento:** O simulador isola a duração intrínseca que a catraca levou para validar cada cartão e que o buffet levou para servir cada prato (descontando o tempo de fila anterior).
3. **Fila Única Compartilhada ($M/G/c$):** Quando 2 ou mais servidores são configurados, os alunos aguardam em fila única central e avançam imediatamente para a primeira posição desocupada.
4. **Bloqueio de Serviço (*Service Blocking*):** Caso o salão atinja a capacidade nominal configurada ($C_{\text{mesas}} = 216$), o atendimento na Fila 2 é compulsoriamente bloqueado até que uma cadeira seja liberada.

### 5.2 Verificação e Validação do Simulador (Calibração do Baseline)
Antes de testar hipóteses, o simulador foi submetido ao teste de calibração contra o próprio cenário real observado ($c_1 = 1$, $c_2 = 1$ e $C_{\text{mesas}} = 216$):
* **Espera Média Real na Fila 1 ($W_{q1}^{\text{real}}$):** $131,52\text{ segundos}$
* **Espera Média Simulada no Baseline ($W_{q1}^{\text{sim}}$):** $131,88\text{ segundos}$
* **Erro Relativo de Calibração ($\Delta_{\text{calibração}}$):**
  $$\Delta = \frac{|131,88 - 131,52|}{131,52} \times 100 = \mathbf{0,27\%}$$

O desvio de apenas 0,27% atesta nível de calibração excepcional (critério de aceitação de literatura: $\Delta \le 5\%$), assegurando que o motor reproduz com precisão matemática a física real do restaurante.

### 5.3 Comparação Experimental de Cenários *What-If* (Regra: Uma Variável por Vez)
Seguindo o preceito fundamental da disciplina de Avaliação de Desempenho de variar rigorosamente uma dimensão de cada vez para isolar causalidades, três cenários foram simulados e comparados contra o baseline:

**Tabela 4: Matriz Comparativa de Cenários de Simulação**

| Parâmetro Operacional | Baseline (Real) | Cenário 1 (2 Catracas) | Cenário 2 (2 Catracas + 2 Buffets) | Cenário 3 (2 Cat + 2 Buf + Mesas -4m) |
| :--- | :---: | :---: | :---: | :---: |
| **Catracas na Entrada ($c_1$)** | 1 | **2 (+100%)** | **2 (+100%)** | **2 (+100%)** |
| **Linhas de Buffet ($c_2$)** | 1 | 1 | **2 (+100%)** | **2 (+100%)** |
| **Capacidade do Salão** | 216 cadeiras | 216 cadeiras | 216 cadeiras | 216 cadeiras |
| **Tempo de Refeição** | Observado (23 min) | Observado (23 min) | Observado (23 min) | **-4 minutos (rotatividade)** |
| **Espera Fila 1 ($W_{q1}$)** | 131,9 s | **55,2 s (-58,1%)** | **55,2 s (-58,1%)** | **55,2 s (-58,1%)** |
| **P90 de Espera Fila 1** | 543,5 s | **175,4 s (-67,7%)** | **175,4 s (-67,7%)** | **175,4 s (-67,7%)** |
| **Fila Média Fila 1 ($L_{q1}$)**| 8,96 alunos | **6,36 alunos** | **6,44 alunos** | **6,74 alunos** |
| **Espera Fila 2 ($W_{q2}$)** | 163,8 s | **238,1 s (+45,4%) ⚠️** | **60,2 s (-63,2%) ✅** | **60,2 s (-63,2%) ✅** |
| **Pico de Alunos no Buffet** | 25 alunos | **48 alunos (+92,0%) ⚠️** | **36 alunos** | **36 alunos** |
| **Trânsito até as Mesas** | **289,8 s (~4,8 min)** | **289,3 s (~4,8 min)** | **106,7 s (~1,7 min) ✅** | **106,7 s (~1,7 min) ✅** |
| **Pico de Assentos Ocupados** | 115 / 216 | 114 / 216 | 98 / 216 | 81 / 216 |
| **Alunos Bloqueados por Falta de Mesa** | 0 | 0 | 0 | 0 |
| **Diagnóstico Executivo** | Saturado no Pico | **Deslocamento de Gargalo** | **Solução Ótima Recomendada** | Folga Estrutural Máxima |

### 5.4 O Fenômeno do Deslocamento de Gargalo (*Bottle-neck Shifting*)
A análise do **Cenário 1** expõe o maior erro de intuição gerencial em restaurantes universitários:
* Ao duplicar as catracas ($c_1 = 2$), a fila externa de fato despencou: o tempo médio caiu de 131,9s para 55,2s (**redução de 58%**) e o 90º percentil caiu de 9 minutos para menos de 3 minutos.
* **No entanto, o tempo total de trânsito até as mesas permaneceu inalterado (289,3s vs 289,8s)!**
* **Por quê?** Porque o buffet continuou operando com apenas 1 servidor ($\mu \approx 3,72\text{ p/min}$). A aceleração da entrada despejou uma onda imediata de alunos no corredor interno, elevando a espera no buffet em **45,4%** (de 163,8s para 238,1s) e dobrando a fila interna de 25 para **48 estudantes aglomerados**.
* Houve um **deslocamento puro de gargalo**: tirou-se o aluno do sol na calçada e colocou-se ele espremido no corredor do buffet.

A verdadeira solução sistêmica surge apenas no **Cenário 2**:
* Ao emparelhar 2 catracas e 2 linhas de buffet, a Fila 1 estabiliza em 55,2s e a Fila 2 cai para **60,2s** (queda de 63,2% no buffet).
* O estudante leva apenas **1 minuto e 46 segundos** (106,7s) desde o momento em que chega na calçada até estar sentado com o prato na mesa.
* Como o pico de ocupação atinge no máximo 98 assentos (45,4% da capacidade física de 216), comprova-se que as mesas absorvem o fluxo acelerado com total segurança, sem necessidade de obras físicas de ampliação predial.

---

## 6. Conclusão e Diagnóstico Operacional: Quando, Quanto e Por Quê
*(Responsável: Adriana)*

Sintetizando as descobertas da aferição, da modelagem estocástica e da simulação computacional, a equipe responde conclusivamente aos três questionamentos centrais da Avaliação de Desempenho:

### 6.1 Quando?
O estrangulamento do Restaurante Universitário **não ocorre ao longo de todo o período de funcionamento**, mas sim em uma janela concentrada de **20 minutos no miolo do almoço (entre os minutos 30 e 50 da coleta, aproximadamente das 12h00 às 12h20)**, com um breve repique de fechamento após o minuto 55. Nos primeiros 10 minutos da abertura e nos períodos intermediários, o sistema opera com ampla ociosidade ($\rho < 0,20$).

### 6.2 Quanto?
Durante a janela de pico:
* A taxa de chegadas atinge **3,80 alunos por minuto** (19 alunos a cada 5 minutos).
* A fila externa na calçada acumulou até **51 estudantes simultâneos**.
* **10% dos estudantes enfrentaram mais de 9 minutos de espera (P90 = 542 segundos)** na Fila 1, chegando a extremos de 16 minutos no pior caso registrado.
* O tempo total médio de trânsito até sentar na mesa foi de **~5 minutos**, e a permanência completa no restaurante foi de **~29 minutos** (somando a espera, serviço e refeição média de 23 minutos).

### 6.3 Por Quê?
O gargalo se estabelece por uma incompatibilidade estocástica evidente:
1. **Déficit de Capacidade no Pico:** Uma única catraca possui capacidade técnica de $\mu = 3,32\text{ pessoas/min}$. Quando a demanda sobe para $\lambda = 3,80\text{ pessoas/min}$, a taxa de utilização ultrapassa a unidade ($\rho = 1,14 > 1,0$). Pela teoria fundamental das filas, qualquer sistema com $\rho > 1$ acumula fila que cresce de forma contínua enquanto durar o pico.
2. **Acoplamento em Cascata:** As três filas são mutuamente dependentes. A catraca funciona hoje como uma "válvula de retenção involuntária" que protege o buffet de colapsar. Se a administração simplesmente instalar uma catraca eletrônica mais rápida sem expandir o balcão de serviço, gerará tumulto interno no corredor de pratos.

### 6.4 Recomendações Práticas para a Gestão do RU
Com base nas simulações validadas, recomenda-se à Diretoria do Restaurante Universitário:
1. **Operação Flexível em Dupla Linha no Pico:** Não é necessário manter múltiplos funcionários ociosos durante todo o dia. Deve-se instituir a escala de reforço exclusivamente entre **11h45 e 12h30**, ativando simultaneamente a **2ª catraca e uma 2ª pista de buffet/distribuição**.
2. **Suficiência do Salão Atual:** Não há necessidade de investimento orçamentário em ampliação do espaço físico ou compra de mesas: as 216 cadeiras existentes operam hoje com folga confortável (54% no pico atual e 45% com fluxo acelerado).
3. **Comunicação Ativa de Rotatividade:** Campanhas educativas que incentivem a liberação ágil das mesas após a refeição (Cenário 3) reduzem o pico para apenas 81 assentos ocupados, criando margem para absorver o crescimento futuro da universidade nos próximos anos.

---

## 7. Referências e Créditos Técnicos

1. **HILLIER, Frederick S.; LIEBERMAN, Gerald J.** *Introdução à Pesquisa Operacional*. 9. ed. Porto Alegre: McGraw-Hill / Bookman, 2013. (Capítulo sobre Teoria das Filas e Modelos de Poisson).
2. **JAIN, Raj.** *The Art of Computer Systems Performance Analysis: Techniques for Experimental Design, Measurement, Simulation, and Modeling*. New York: John Wiley & Sons, 1991.
3. **LITTLE, John D. C.** A Proof for the Queuing Formula: $L = \lambda W$. *Operations Research*, v. 9, n. 3, p. 383–387, 1961.
4. **BANKS, Jerry; CARSON, John S.; NELSON, Barry L.; NICOL, David M.** *Discrete-Event System Simulation*. 5. ed. Upper Saddle River: Prentice Hall, 2010.
5. **Código-Fonte e Dados do Projeto Fila RU:** Módulos isomórficos `shared/metricas.js`, `shared/simulador.js`, `shared/estado.js` e bateria com 203 testes automatizados contidos no repositório local.
