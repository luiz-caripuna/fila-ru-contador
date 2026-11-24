# Modelagem Estocástica: Matriz de Probabilidade de Transição do Sistema (Cadeias de Markov)

**Disciplina:** Avaliação de Desempenho de Sistemas  
**Responsável:** Otávio (Modelagem Teórica)  
**Projeto:** Fila RU — Estudo de Caso no Restaurante Universitário Central  
**Data da Coleta Base:** 04 de Novembro de 2026 (Sessão de 65,34 minutos)

---

## 1. Fundamentação Teórica da Modelagem

O fluxo do Restaurante Universitário é modelado através da teoria dos **Processos Estocásticos de Nascimento e Morte** em tempo contínuo e em tempo discreto.

* **Definição de Estado $n \in \{0, 1, 2, \dots, K\}$:**  
  Representa o número total de pessoas no subsistema no instante $t$ (incluindo o aluno que está sendo atendido no posto e os alunos aguardando na fila).
* **Taxa de Chegadas ($\lambda$ — "Nascimento"):**  
  Número médio de chegadas por unidade de tempo (processo de Poisson).
* **Taxa de Atendimento ($\mu$ — "Morte"):**  
  Capacidade média de serviço do posto por unidade de tempo (tempos exponenciais).
* **Passo de Discretização ($\Delta t$):**  
  Intervalo de tempo suficientemente pequeno para garantir que ocorra no máximo **uma** transição (uma chegada ou uma saída), respeitando a condição:
  $$(\lambda + \mu)\Delta t < 1$$

---

## 2. Estrutura Algébrica da Matriz de Probabilidade de Transição ($\mathbf{P}$)

Para uma cadeia de Markov em tempo discreto com capacidade finita $K$, a **Matriz de Transição de Estados $\mathbf{P} = [p_{i,j}]$** possui dimensão $(K+1) \times (K+1)$ e formato tridiagonal:

$$\mathbf{P} = \begin{pmatrix}
1 - \lambda \Delta t & \lambda \Delta t & 0 & 0 & 0 & \dots & 0 \\
\mu \Delta t & 1 - (\lambda + \mu)\Delta t & \lambda \Delta t & 0 & 0 & \dots & 0 \\
0 & \mu \Delta t & 1 - (\lambda + \mu)\Delta t & \lambda \Delta t & 0 & \dots & 0 \\
0 & 0 & \mu \Delta t & 1 - (\lambda + \mu)\Delta t & \lambda \Delta t & \dots & 0 \\
\vdots & \vdots & \ddots & \ddots & \ddots & \ddots & \vdots \\
0 & 0 & \dots & 0 & \mu \Delta t & 1 - (\lambda + \mu)\Delta t & \lambda \Delta t \\
0 & 0 & \dots & 0 & 0 & \mu \Delta t & 1 - \mu \Delta t
\end{pmatrix}$$

### Regras dos Elementos da Matriz:
1. **Estado $i = 0$ (Sistema Vazio):**  
   Não pode haver saída quando não há ninguém no sistema ($\mu = 0$).  
   * $p_{0,1} = \lambda \Delta t$ (probabilidade de uma chegada ocorrer em $\Delta t$).
   * $p_{0,0} = 1 - \lambda \Delta t$ (probabilidade de permanecer vazio).
2. **Estados Intermediários $0 < i < K$:**  
   * $p_{i, i+1} = \lambda \Delta t$ (uma nova chegada, estado aumenta para $i+1$).
   * $p_{i, i-1} = \mu \Delta t$ (um atendimento concluído, estado reduz para $i-1$).
   * $p_{i, i} = 1 - (\lambda + \mu)\Delta t$ (nenhum evento conclui em $\Delta t$).
3. **Estado de Capacidade Máxima $i = K$ (Saturação):**  
   O sistema atinge o limite $K$; novas chegadas são bloqueadas/descartadas ($\lambda = 0$).  
   * $p_{K, K-1} = \mu \Delta t$ (um atendimento conclui).
   * $p_{K, K} = 1 - \mu \Delta t$ (permanece na capacidade máxima).
4. **Propriedade Estocástica Fundamental:**  
   A soma das probabilidades de qualquer linha $i$ é estritamente igual a 1:
   $$\sum_{j=0}^{K} p_{i,j} = 1, \quad \forall i$$

---

## 3. Matrizes Numéricas com os Dados Coletados em Campo

Com base na sessão real de **04/11/2026** no RU Central, foram extraídos os parâmetros operacionais de cada fila:

### 3.1 FILA 1: Entrada → Catraca (Fila Vermelha)
* **Taxa de Chegadas:** $\lambda_1 = 2,938\text{ pessoas/min} = 0,04897\text{ pessoas/s}$
* **Taxa de Serviço:** $\mu_1 = 3,317\text{ pessoas/min} = 0,05528\text{ pessoas/s}$
* **Fator de Utilização:** $\rho_1 = \frac{\lambda_1}{\mu_1} = \frac{2,938}{3,317} = \mathbf{0,8860\text{ (88,6\%)}}$
* **Passo Adotado:** $\Delta t = 1\text{ segundo} = \frac{1}{60}\text{ min}$

#### Probabilidades Elementares da Fila 1 ($\Delta t = 1\text{ s}$):
* $\lambda_1 \Delta t = 0,04897$ ($\mathbf{4,90\%}$ de chance de chegada em 1 segundo)
* $\mu_1 \Delta t = 0,05528$ ($\mathbf{5,53\%}$ de chance de atendimento em 1 segundo)
* $1 - (\lambda_1 + \mu_1)\Delta t = 1 - 0,10425 = \mathbf{0,89575}$ ($\mathbf{89,58\%}$ de chance de não mudar de estado)
* $p_{0,0} = 1 - \lambda_1 \Delta t = \mathbf{0,95103}$ ($\mathbf{95,10\%}$ quando o sistema está vazio)

#### Matriz Numérica $\mathbf{P}_1$ Truncada nos Primeiros 6 Estados ($0$ a $5$ pessoas):

$$\mathbf{P}_1 = \begin{pmatrix}
\mathbf{0,9510} & \mathbf{0,0490} & 0 & 0 & 0 & 0 & \dots \\
\mathbf{0,0553} & \mathbf{0,8958} & \mathbf{0,0490} & 0 & 0 & 0 & \dots \\
0 & \mathbf{0,0553} & \mathbf{0,8958} & \mathbf{0,0490} & 0 & 0 & \dots \\
0 & 0 & \mathbf{0,0553} & \mathbf{0,8958} & \mathbf{0,0490} & 0 & \dots \\
0 & 0 & 0 & \mathbf{0,0553} & \mathbf{0,8958} & \mathbf{0,0490} & \dots \\
0 & 0 & 0 & 0 & \mathbf{0,0553} & \mathbf{0,8958} & \dots \\
\vdots & \vdots & \vdots & \vdots & \vdots & \vdots & \ddots
\end{pmatrix}$$

---

### 3.2 FILA 2: Catraca → Buffet / Atendimento de Pratos (Fila Verde)
* **Taxa de Chegadas:** $\lambda_2 = 2,938\text{ pessoas/min} = 0,04897\text{ pessoas/s}$ (encadeada da Fila 1)
* **Taxa de Serviço:** $\mu_2 = 3,716\text{ pessoas/min} = 0,06193\text{ pessoas/s}$
* **Fator de Utilização:** $\rho_2 = \frac{\lambda_2}{\mu_2} = \frac{2,938}{3,716} = \mathbf{0,7908\text{ (79,1\%)}}$
* **Passo Adotado:** $\Delta t = 1\text{ segundo}$

#### Probabilidades Elementares da Fila 2 ($\Delta t = 1\text{ s}$):
* $\lambda_2 \Delta t = 0,04897$ ($\mathbf{4,90\%}$ de chegada em 1 segundo)
* $\mu_2 \Delta t = 0,06193$ ($\mathbf{6,19\%}$ de atendimento em 1 segundo)
* $1 - (\lambda_2 + \mu_2)\Delta t = 1 - 0,11090 = \mathbf{0,88910}$ ($\mathbf{88,91\%}$ de permanência)
* $p_{0,0} = 1 - \lambda_2 \Delta t = \mathbf{0,95103}$ ($\mathbf{95,10\%}$)

#### Matriz Numérica $\mathbf{P}_2$ Truncada nos Primeiros 6 Estados ($0$ a $5$ pessoas):

$$\mathbf{P}_2 = \begin{pmatrix}
\mathbf{0,9510} & \mathbf{0,0490} & 0 & 0 & 0 & 0 & \dots \\
\mathbf{0,0619} & \mathbf{0,8891} & \mathbf{0,0490} & 0 & 0 & 0 & \dots \\
0 & \mathbf{0,0619} & \mathbf{0,8891} & \mathbf{0,0490} & 0 & 0 & \dots \\
0 & 0 & \mathbf{0,0619} & \mathbf{0,8891} & \mathbf{0,0490} & 0 & \dots \\
0 & 0 & 0 & \mathbf{0,0619} & \mathbf{0,8891} & \mathbf{0,0490} & \dots \\
0 & 0 & 0 & 0 & \mathbf{0,0619} & \mathbf{0,8891} & \dots \\
\vdots & \vdots & \vdots & \vdots & \vdots & \vdots & \ddots
\end{pmatrix}$$

---

### 3.3 SALÃO DE MESAS (Capacidade Finita $K = 216$ Cadeiras)
Para o salão de refeições, o estado $n \in \{0, 1, 2, \dots, 216\}$ representa o número de cadeiras ocupadas.
* Capacidade Nominal Total: $K = 216$ cadeiras (36 mesas $\times$ 6 lugares).
* No estado $n = 216$, novas entradas são bloqueadas:
  $$p_{216, 215} = \mu_{\text{mesas}} \Delta t \quad \text{e} \quad p_{216, 216} = 1 - \mu_{\text{mesas}} \Delta t$$
* Caso uma pessoa tente sentar com $n = 216$, ocorre **Service Blocking**: ela permanece retida no final da Fila 2 segurando a bandeja.

---

## 4. Vetor de Probabilidades Estacionárias ($\boldsymbol{\pi}$)

O vetor estacionário de probabilidades $\boldsymbol{\pi} = [\pi_0, \pi_1, \pi_2, \dots]$ é o autovetor à esquerda da matriz $\mathbf{P}$ associado ao autovalor unitário:

$$\boldsymbol{\pi} \mathbf{P} = \boldsymbol{\pi} \quad \text{e} \quad \sum_{n=0}^{\infty} \pi_n = 1$$

Resolvendo o sistema de equações de balanço global de fluxo $\lambda \pi_n = \mu \pi_{n+1}$:

$$\pi_0 = 1 - \rho$$
$$\pi_n = (1 - \rho) \cdot \rho^n$$

### Comparação Numérica Teórica ($\boldsymbol{\pi}_n$) vs. Frequência Empírica Observada:

| Estado ($n$ pessoas) | Teórico Fila 1 ($\rho=0,886$) | Empírico Fila 1 (Observado em Campo) | Teórico Fila 2 ($\rho=0,791$) |
| :---: | :---: | :---: | :---: |
| **0 (vazio)** | **11,40%** | **25,97%** *(ocioso no início)* | **20,92%** |
| **1 pessoa** | **10,10%** | **13,93%** | **16,54%** |
| **2 pessoas** | **8,95%** | **12,18%** | **13,08%** |
| **3 pessoas** | **7,93%** | **4,87%** | **10,35%** |
| **4 pessoas** | **7,03%** | **3,33%** | **8,18%** |
| **5 pessoas** | **6,22%** | **1,31%** | **6,47%** |
| **6 pessoas** | **5,51%** | **0,58%** | **5,12%** |
| **7 pessoas** | **4,89%** | **1,20%** | **4,05%** |
| **8 pessoas** | **4,33%** | **1,95%** | **3,20%** |
| **9 pessoas** | **3,84%** | **1,12%** | **2,53%** |
| **$\ge 10$ pessoas** | **29,80%** | **13,54%** *(acumulado no pico)*| **8,56%** |

---

## 5. Matriz Geradora Infinitesimal em Tempo Contínuo ($\mathbf{Q}$)

Caso o professor solicite a representação por **Cadeia de Markov em Tempo Contínuo (CTMC)**, a matriz de taxas infinitesimais $\mathbf{Q} = [q_{i,j}]$ (onde $\sum_j q_{i,j} = 0$) é dada por:

$$\mathbf{Q} = \begin{pmatrix}
-\lambda & \lambda & 0 & 0 & \dots \\
\mu & -(\lambda + \mu) & \lambda & 0 & \dots \\
0 & \mu & -(\lambda + \mu) & \lambda & \dots \\
0 & 0 & \mu & -(\lambda + \mu) & \dots \\
\vdots & \vdots & \ddots & \ddots & \ddots
\end{pmatrix}$$

Substituindo os valores em **pessoas por minuto** da Fila 1 ($\lambda_1 = 2,938\text{ p/min}$ e $\mu_1 = 3,317\text{ p/min}$):

$$\mathbf{Q}_1 = \begin{pmatrix}
-2,938 & 2,938 & 0 & 0 & \dots \\
3,317 & -6,255 & 2,938 & 0 & \dots \\
0 & 3,317 & -6,255 & 2,938 & \dots \\
\vdots & \ddots & \ddots & \ddots & \ddots
\end{pmatrix}$$

---

## 6. Como Otávio deve Apresentar a Matriz no Seminário

1. **Explicar a lógica física:**  
   *"A matriz de probabilidades $P$ responde a uma pergunta simples: se agora há $i$ pessoas na fila, qual é a chance de haver $j$ pessoas no segundo seguinte? Como o passo $\Delta t = 1\text{ s}$ é muito curto, ou chega 1 pessoa (probabilidade de 4,9%), ou sai 1 pessoa (5,5%), ou a fila se mantém igual (89,6%)."*
2. **Destacar a tridiagonalidade:**  
   *"A matriz é tridiagonal porque num processo de nascimento e morte puro não ocorrem saltos múltiplos simultâneos em $\Delta t$."*
3. **Conectar com o vetor estacionário:**  
   *"Ao multiplicar $\boldsymbol{\pi} \mathbf{P} = \boldsymbol{\pi}$, deduzimos as probabilidades estacionárias $\pi_n = (1 - \rho)\rho^n$, comprovando que a catraca fica livre 11,4% do tempo e o buffet fica livre 20,9% do tempo."*
