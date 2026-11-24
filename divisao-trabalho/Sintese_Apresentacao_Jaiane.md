# Síntese da Apresentação — Jaiane
**Tópicos:** Resultados Empíricos da Aferição, Separação Calma vs. Pico e Dispersão Estatística  
**Slides:** 7, 8 e 9 de `Afericao_Filas_RU_Seminario.pptx`  
**Tempo Estimado de Fala:** ~4,0 minutos  
**Transição:** Recebe a palavra de **Lucas** (Método) e passa para **Otávio** (Modelagem).

---

## 1. Mapa Rápido dos Slides de Jaiane

```
┌───────────────────────────────────────────────────────────────────────────────────┐
│ SLIDE 7: Resultados Globais das Três Filas (Sessão de 04/11/2026)                 │
│ • Tabela consolidada com Entradas, Saídas, λ, μ, ρ e Espera Média Wq              │
│ • Fila 1 (Entrada): λ = 2,94 p/min, μ = 3,32 p/min, ρ = 88,6%, Wq = 131,5 s      │
│ • Fila 2 (Buffet):  λ = 2,94 p/min, μ = 3,72 p/min, ρ = 79,1%, Wq = 142,1 s      │
│ • Fila 3 (Saída 1h): λ = 2,83 p/min, μ = 2,13 p/min, ρ = 132,8%, Wq = 23,2 min    │
│   (185 entraram no salão, 95 saíram e 90 ainda estavam almoçando)                │
├───────────────────────────────────────────────────────────────────────────────────┤
│ SLIDE 8: Separação Rigorosa: Regime de Calma vs. Regime de Pico                   │
│ • Exigência central da disciplina: separar por λ (chegadas/min), NÃO pela fila    │
│ • Calma (minutos 0 a 10): apenas 6 chegadas no total ==> λ = 0,60 p/min, ρ = 18%  │
│ • Pico (minutos 30 a 50): 19 chegadas a cada 5 min  ==> λ = 3,80 p/min, ρ = 114,5%│
│ • Inversão crítica: no pico, λ > μ (3,80 > 3,32), gerando fila física de 51 alunos│
├───────────────────────────────────────────────────────────────────────────────────┤
│ SLIDE 9: Distribuição dos Tempos de Espera (Wq) e Dispersão Amostral              │
│ • Grande disparidade entre média e mediana:                                       │
│   Fila 1: Mediana = 27,4 segundos (quase direto) vs P90 = 9 minutos e 2 segundos! │
│ • Pior caso registrado: 16 minutos e 18 segundos aguardando na calçada            │
│ • Salão de Mesas: tempo de refeição médio de 23m 12s, com pico de 116 cadeiras    │
│   ocupadas de 216 disponíveis (53,7% de ocupação — status Moderado, sem lotar)    │
└───────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Conceitos e Fundamentos Essenciais (Colar na Ponta da Língua)

* **Por que separar Calma e Pico pelas chegadas e não pela fila?**  
  A fila física é uma consequência atrasada no tempo. Se olhássemos apenas o tamanho da fila, poderíamos achar que às 11h35 havia "pico" quando na verdade eram apenas os 27 alunos acumulados antes da catraca abrir sendo atendidos. A verdadeira demanda externa do sistema é dada pela **taxa de chegadas por minuto ($\lambda$)**.
* **Condição de Sobrecarga Estocástica ($\lambda > \mu$):**  
  Quando a taxa de chegada supera a capacidade máxima de processamento do posto ($\lambda > \mu$, ou seja, $\rho > 1,0$), a teoria matemática prova que a fila não atinge equilíbrio e cresce de forma contínua enquanto durar a sobrecarga.
* **Média vs. Mediana e Percentis (P90 e P95):**  
  Em distribuições de filas fortemente assimétricas (com cauda longa), a média aritmética é puxada para cima pelos alunos do pico. A **mediana (27 s)** reflete a experiência de 50% dos alunos (quem chega na calma passa quase direto), enquanto o **P90 (9 min)** quantifica o sofrimento dos 10% que chegam no pior momento do dia.

---

## 3. Os Números de Jaiane (Memorizar para Citar no Palco)

* **Fila 1 (Entrada / Catraca):**
  * Entradas: 192 efetivas (+ 10 desistências/anulações).
  * Taxa de Chegada ($\lambda$): 2,94 pessoas/minuto (global) e **3,80 no pico**.
  * Capacidade da Catraca ($\mu$): 3,32 pessoas/minuto.
  * Utilização ($\rho$): **88,6%** na média e **114,5% no pico**.
  * Espera ($W_{q1}$): Média de **2m 11s** (131,5 s), Mediana de **27 s**, P90 de **9m 02s** (542 s), Máximo de **16m 18s**.
  * Tamanho da Fila ($L_{q1}$): Média de 12,65 alunos; **Pico de 51 alunos na calçada**.
* **Fila 2 (Buffet / Serviço de Alimentos):**
  * Taxa de Atendimento ($\mu_2$): 3,72 pessoas/minuto.
  * Utilização ($\rho_2$): **79,1%**.
  * Espera ($W_{q2}$): Média de **2m 22s** (142,1 s), Mediana de **2m 13s**, P90 de **3m 56s**.
  * Fila Média ($L_{q2}$): 6,72 alunos; Pico de 19 alunos no corredor.
* **Salão de Mesas:**
  * Capacidade Total: 216 assentos (36 mesas $\times$ 6 lugares).
  * Pico Ocupado: **116 cadeiras** (53,7% da capacidade — nível Moderado).
  * Tempo Médio de Refeição: **23 minutos e 12 segundos**.

---

## 4. O Ponto Alto de Jaiane: A Evidência de Calma vs. Pico e a Desigualdade do Aluno

O grande momento da fala de Jaiane ocorre na transição entre o **Slide 8** e o **Slide 9**:
> *"O nosso dado mais revelador foi tabular a taxa de chegadas em blocos de 5 minutos. Nós provamos numericamente o que o professor solicitou: quem chega entre 11h30 e 11h40 encontra o restaurante vazio e passa na catraca em 27 segundos. Mas quem chega entre 12h00 e 12h20 enfrenta uma taxa de 3,80 alunos por minuto, superior aos 3,32 que a catraca aguenta. A utilização vai a 114,5% e o tempo salta para mais de 9 minutos. A experiência do aluno muda radicalmente dependendo de um intervalo de apenas 20 minutos!"*

---

## 5. Roteiro de Fala Direto (O que Falar no Palco)

### 🎙️ Slide 7: Resultados Globais das Três Filas — ~1 min:
> *"Obrigada, Lucas. Boa tarde a todos. O sistema que o Lucas descreveu capturou 65,34 minutos ininterruptos de operação, totalizando 1.074 eventos. Na Tabela do Slide 7, vemos o resumo quantitativo consolidado das três filas.*
> 
> *A taxa média global de chegadas foi de 2,94 pessoas por minuto. A capacidade da catraca na Fila 1 foi de 3,32 pessoas por minuto, o que resultou em um fator de utilização de 88,6%. Na Fila 2, o buffet, a capacidade de atendimento foi ligeiramente superior, de 3,72 pessoas por minuto, operando com utilização de 79,1%.*
> 
> *A espera média foi de 2 minutos e 11 segundos na calçada e 2 minutos e 22 segundos no buffet. Já na Fila 3, vemos uma utilização aparente de 132%, porque os alunos levam em média 23 minutos almoçando nas mesas; por isso, dos 185 que entraram, 95 deixaram o refeitório dentro da nossa hora de coleta e 90 ainda estavam concluindo a refeição."*

### 🎙️ Slide 8: Separação Calma vs. Pico pelas Chegadas — ~1,5 min:
> *"Avançando para o Slide 8, cumprimos com rigor a diretriz da disciplina: a separação entre calma e pico deve ser feita pela taxa de chegadas por minuto ($\lambda$), e não pelas ondas visuais da fila.*
> 
> *Ao dividirmos os dados em blocos de 5 minutos, identificamos duas fases completamente distintas: nos primeiros 10 minutos (Regime de Calma), chegaram apenas 6 alunos no total, uma taxa de $\lambda = 0,60$ pessoas por minuto. A catraca operou com utilização de apenas 18%, praticamente vazia.*
> 
> *Porém, a partir do minuto 30 até o minuto 50, a demanda explodiu no Regime de Pico: foram 19 chegadas a cada 5 minutos, ou seja, $\lambda = 3,80$ pessoas por minuto. Como a capacidade máxima de uma catraca é de 3,32 pessoas por minuto, ocorreu a inversão estocástica crítica: $\lambda$ superou $\mu$. Com $\rho$ atingindo 114,5% (> 1,0), a fila acumulou e bateu o pico físico de 51 pessoas formadas na calçada."*

### 🎙️ Slide 9: Tempos de Espera Wq e Dispersão — ~1,5 min:
> *"No Slide 9, analisamos a dispersão estatística desses tempos de espera. A comparação entre a média e a mediana comprova uma enorme desigualdade de tratamento: na Fila 1, a média foi de 2m 11s, mas a mediana foi de apenas 27 segundos! Metade dos alunos passou praticamente direto.*
> 
> *Em compensação, o 90º percentil atingiu 9 minutos e 2 segundos, e o pior tempo registrado chegou a 16 minutos e 18 segundos. No percurso total até sentar à mesa com a comida, 10% dos estudantes perderam mais de 13 minutos e meio na soma das filas.*
> 
> *Já o Salão de Mesas operou com ampla folga: com 216 cadeiras instaladas, o pico máximo simultâneo foi de 116 alunos sentados (53,7% da capacidade), mantendo-se na faixa Moderada. Agora, o Otávio mostrará como formalizamos esses números através da Teoria das Filas e da Lei de Little."*

---

## 6. Três Perguntas Prováveis da Banca para Jaiane

1. **"Por que a Fila 3 teve utilização de 132% se as mesas não lotaram?"**  
   * **Resposta:** *"Porque a utilização $\rho$ compara chegadas e saídas dentro da janela de 65 minutos da coleta. Como a refeição dura 23 minutos em média, os alunos que entraram a partir dos 45 minutos ainda estavam comendo quando a coleta encerrou. O acúmulo ocorreu nas cadeiras do salão (que suportam 216 pessoas), e não em uma fila de corredor."*
2. **"O que explica o pico de 51 pessoas se a média de pessoas na fila foi de 12,6?"**  
   * **Resposta:** *"A média ponderada no tempo ($L_q = 12,65$) dilui todo o período de 65 minutos, incluindo os primeiros 15 minutos em que a fila esteve praticamente zerada. O pico de 51 alunos ocorreu pontualmente durante os 20 minutos de pico onde $\lambda > \mu$, mostrando por que a média isolada esconde gargalos severos de regime transiente."*
3. **"Por que a Fila 2 teve tempo médio maior que a Fila 1 (142s vs 131s) mesmo tendo menor utilização (79% vs 88%)?"**  
   * **Resposta:** *"Porque o atendimento no buffet é inerentemente mais lento por pessoa do que o giro da catraca: o aluno leva cerca de 16 a 20 segundos para pegar bandeja, prato, talheres e escolher a salada, enquanto o passe na catraca leva de 6 a 8 segundos. Por isso, a taxa de serviço individual determina tempos de residência maiores no balcão térmico."*
