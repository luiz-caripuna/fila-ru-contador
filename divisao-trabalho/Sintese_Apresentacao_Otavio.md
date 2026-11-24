# Síntese da Apresentação — Otávio
**Tópico:** Modelagem Teórica, Cadeias de Markov e Lei de Little  
**Slides:** 10, 11 e 12 de `Afericao_Filas_RU_Seminario.pptx`  
**Tempo Estimado de Fala:** ~3,5 a 4 minutos  
**Transição:** Recebe a palavra de **Jaiane** (Resultados) e passa para **Vanessa** (Simulação).

---

## 1. Mapa Rápido dos Slides de Otávio

```
┌───────────────────────────────────────────────────────────────────────────────────┐
│ SLIDE 10: Modelagem Estocástica (Espaço de Estados e Parâmetros)                  │
│ • Estado N(t): número de pessoas presentes (na fila + em atendimento)             │
│ • Passo temporal: contínuo com taxas médias e discretização em blocos de 5 min    │
│ • Probabilidades P_n: probabilidade de haver n pessoas no sistema                 │
│ • Capacidade K: K = 216 assentos nas mesas (restrição física do salão)            │
├───────────────────────────────────────────────────────────────────────────────────┤
│ SLIDE 11: Matriz de Transição P e Equações do Modelo M/M/1                        │
│ • Processo de Nascimento e Morte: chegadas λ e atendimentos μ                     │
│ • Matriz P tridiagonal (tempo discreto Δt infinitesimal)                          │
│ • Balanço de corte: λ·P_n = μ·P_(n+1)  ==>  P_n = (1 - ρ)·ρ^n                     │
│ • Fórmulas M/M/1: ρ = λ/μ, P_0 = 1 - ρ, L_q = ρ²/(1 - ρ), W_q = L_q/λ             │
├───────────────────────────────────────────────────────────────────────────────────┤
│ SLIDE 12: Verificação Experimental pela Lei de Little (L = λ·W)                   │
│ • Fila 2 (Buffet): L_q(obs) = 6,72 vs λ·W_q = 6,96  ==>  Diferença de APENAS 3,48%│
│ • Fila 1 (Catraca): Divergência de 49% explicada pelo Regime Transitório Inicial  │
│   (27 pessoas acumuladas na calçada antes da catraca abrir)                       │
└───────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Conceitos e Fórmulas Essenciais (Colar na Ponta da Língua)

### 2.1 Espaço de Estados e Processo de Nascimento e Morte
* **Definição de Estado $N(t)$:** Variável aleatória discreta $N(t) \in \{0, 1, 2, \dots, K\}$ representando a quantidade total de usuários no subsistema no instante $t$.
* **Taxas do Processo:**
  * Taxa de nascimento (chegada): $\lambda$ (Poisson).
  * Taxa de morte (serviço): $\mu$ (Exponencial).
* **Capacidade $K$:** 
  * Filas 1 e 2: modeladas como espaço infinito ($K = \infty$) na calçada e corredor.
  * Salão de Mesas: capacidade finita rígida $K = 216$ cadeiras (36 mesas $\times$ 6 lugares).

### 2.2 Matriz de Probabilidades de Transição $P$
Em um intervalo infinitesimal $\Delta t$ tal que $(\lambda + \mu)\Delta t < 1$:

$$P = \begin{pmatrix}
1 - \lambda \Delta t & \lambda \Delta t & 0 & 0 & \dots \\
\mu \Delta t & 1 - (\lambda + \mu)\Delta t & \lambda \Delta t & 0 & \dots \\
0 & \mu \Delta t & 1 - (\lambda + \mu)\Delta t & \lambda \Delta t & \dots \\
\vdots & \ddots & \ddots & \ddots & \vdots
\end{pmatrix}$$

### 2.3 Equações de Equilíbrio e Métricas do Modelo $M/M/1$
Condição de estabilidade estacionária: $\rho = \frac{\lambda}{\mu} < 1$.

| Métrica | Símbolo / Fórmula | Significado Físico no RU |
| :--- | :---: | :--- |
| **Fator de Utilização** | $\rho = \frac{\lambda}{\mu}$ | Fração de tempo em que o atendente/catraca está ocupado. |
| **Probabilidade de Vazio** | $P_0 = 1 - \rho$ | Chance de um aluno chegar e encontrar o posto livre. |
| **Probabilidade de Estado** | $P_n = (1 - \rho)\rho^n$ | Distribuição estacionária de encontrar $n$ pessoas. |
| **Fila Média (espera)** | $L_q = \frac{\rho^2}{1 - \rho} = \frac{\lambda^2}{\mu(\mu - \lambda)}$ | Quantidade média de pessoas esperando na fila física. |
| **Tempo Médio de Espera** | $W_q = \frac{L_q}{\lambda} = \frac{\rho}{\mu - \lambda}$ | Tempo médio que o estudante aguarda na fila. |
| **Número Médio no Sistema** | $L = \frac{\rho}{1 - \rho}$ | Pessoas na fila somadas à pessoa em atendimento. |
| **Tempo Total no Sistema** | $W = W_q + \frac{1}{\mu} = \frac{1}{\mu - \lambda}$ | Tempo total gasto desde a chegada até ser liberado. |

---

## 3. Os Números de Otávio (Dados Reais da Coleta de 04/11/2026)

### Aplicação Teórica na Fila 1 (Entrada / Catraca)
* $\lambda = 2,938\text{ pessoas/min}$
* $\mu = 3,317\text{ pessoas/min}$
* $\rho = \frac{2,938}{3,317} = \mathbf{0,886\text{ (88,6\%)}}$
* $P_0 = 1 - 0,886 = \mathbf{11,4\%}$ (catraca livre apenas 11,4% do tempo).
* $L_q^{\text{teórico}} = \frac{0,886^2}{1 - 0,886} = \mathbf{6,88\text{ pessoas}}$
* $W_q^{\text{teórico}} = \frac{6,88}{2,938} = 2,34\text{ min} = \mathbf{140,56\text{ segundos}}$ (bastante próximo da média observada de 131,5s).

---

## 4. O Ponto Alto: Verificação Experimental da Lei de Little ($L_q = \lambda \cdot W_q$)

A Lei de Little afirma que, em regime permanente estável:
$$L = \lambda \cdot W \quad \text{e} \quad L_q = \lambda \cdot W_q$$

### Comparação Experimental em Campo:

| Fila Aferida | $L_q$ Observado (Integral Temporal) | $\lambda$ Empírico | $W_q$ Médio Real | $\lambda \cdot W_q$ Calculado | Divergência ($\Delta\%$) | Conclusão Científica |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Fila 2 (Buffet)** | **6,72 pessoas** | 2,938 p/min | 2,369 min (142,1s) | **6,96 pessoas** | **3,48%** | **Perfeitamente Consistente ($\le 5\%$)** |
| **Fila 1 (Entrada)** | **12,65 pessoas** | 2,938 p/min | 2,192 min (131,5s) | **6,44 pessoas** | **49,08%** | **Efeito de Regime Transitório Inicial** |

### Como explicar a diferença de 49% na Fila 1 se o professor perguntar:
> *"A Lei de Little é um teorema assintótico que exige regime permanente estável (condições iniciais esquecidas). No dia da coleta, às 11h30 já havia 27 estudantes formados na calçada antes da catraca ser destravada. A integral no tempo de $L_q$ carregou essa área acumulada inicial. Já os tempos individuais de $W_q$ foram menores porque a catraca atendeu rápido após abrir. Quando calculamos a Lei de Little isolando a operação após a dissipação desse bloco inicial, a divergência decai para menos de 8%!"*

---

## 5. Roteiro de Fala Direto (O que Falar no Palco)

### 🟢 Início da Fala (Conectando com Jaiane):
> *"Obrigado, Jaiane. Boa tarde a todos. A Jaiane nos mostrou o comportamento empírico das três filas. O meu papel agora é traduzir esse comportamento para a linguagem matemática da Teoria das Filas, definindo o espaço de estados, deduzindo a matriz de transição e verificando a consistência analítica através da Lei de Little."*

### 🟢 Slide 10: Modelagem Estocástica e Espaço de Estados:
> *"No Slide 10, nós modelamos o sistema definindo o estado $N(t)$ como a quantidade discreta de estudantes presentes em cada etapa no instante $t$. Cada evento no RU altera esse estado pontualmente: uma chegada soma 1 (a uma taxa $\lambda$) e um atendimento subtrai 1 (a uma taxa $\mu$). Nós adotamos o passo analítico de 5 minutos para confrontar as séries temporais. E consideramos uma diferença fundamental de capacidade: enquanto a entrada e o corredor do buffet possuem espaço aberto na calçada ($K = \infty$), o Salão de Refeições possui uma restrição rígida de capacidade física: $K = 216$ cadeiras, distribuídas em 36 mesas de 6 lugares."*

### 🟢 Slide 11: Matriz de Transição P e Fórmulas M/M/1:
> *"Avançando para o Slide 11, para um intervalo infinitesimal $\Delta t$, o processo é governado por uma Cadeia de Markov de Nascimento e Morte com a Matriz de Transição $P$ tridiagonal exibida aqui. Aplicando o balanço de corte no regime estacionário — onde a taxa de saída de um estado deve igualar a de entrada —, deduzimos que a probabilidade $P_n$ é dada por $(1 - \rho)\rho^n$. A partir dessa distribuição, obtemos as métricas analíticas clássicas do modelo $M/M/1$: a utilização $\rho = \lambda / \mu$, a probabilidade de sistema vazio $P_0 = 1 - \rho$, o tamanho médio da fila $L_q = \rho^2 / (1 - \rho)$ e o tempo médio de espera $W_q = L_q / \lambda$. Aplicando os parâmetros médios da Fila 1, o modelo $M/M/1$ prevê uma espera média teórica de 140 segundos e probabilidade de catraca ociosa de 11,4%."*

### 🟢 Slide 12: Validação Formal pela Lei de Little:
> *"No Slide 12, submetemos a nossa medição ao teste mais rigoroso da engenharia de tráfego: a validação pela Lei de Little, que estabelece que $L_q$ deve ser igual a $\lambda$ vezes $W_q$. E o resultado na Fila 2, o buffet, foi fantástico: o $L_q$ observado diretamente pela integral temporal foi de 6,72 alunos, enquanto o produto $\lambda \cdot W_q$ resultou em 6,96 alunos. Isso representa uma divergência de apenas 3,48%, comprovando com rigor científico a consistência matemática da nossa aferição em campo! Na Fila 1, observamos uma divergência de 49% devido ao regime transitório inicial — pois já havia 27 alunos acumulados na calçada antes da catraca abrir, elevando a média temporal ponderada de $L_q$. Mas como podemos usar esses modelos para testar cenários futuros e saber o que acontece se colocarmos mais uma catraca? Para responder isso, passo a palavra para a Vanessa, que apresentará a simulação de eventos discretos."*

---

## 6. Possíveis Perguntas da Banca e Respostas Rápidas

* **P1: "Por que vocês usaram M/M/1 se os alunos chegam em turmas e não necessariamente por Poisson puro?"**
  * *Resposta de Otávio:* "O modelo $M/M/1$ serve como nosso referencial teórico analítico (*baseline* assintótico). Ele nos fornece a base de comparação clássica. Para capturar as nuances reais, como chegadas em rajadas de turmas e tempos de atendimento não estritamente exponenciais, nós construímos o simulador por eventos discretos que a Vanessa vai apresentar a seguir."
* **P2: "Por que a capacidade K foi modelada apenas nas mesas e não na Fila 1?"**
  * *Resposta de Otávio:* "Porque a Fila 1 se estende pela calçada aberta do campus, sem barreira física rígida que impeça a chegada de novos alunos (capacidade praticamente infinita). Já o salão de mesas tem limite físico estrito de 216 cadeiras instaladas; se lotar, causa bloqueio compulsório no buffet."
* **P3: "O que comprova que o sistema da Fila 2 estava em equilíbrio?"**
  * *Resposta de Otávio:* "A aderência quase perfeita à Lei de Little ($\Delta = 3,48\%$) e o fator de utilização $\rho = 0,791 < 1$. Em um sistema instável ou com perda severa de clientes, a Lei de Little entre $L_q$ observado e $\lambda W_q$ divergiria amplamente."
