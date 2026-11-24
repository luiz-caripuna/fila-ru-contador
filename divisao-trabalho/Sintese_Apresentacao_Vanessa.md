# Síntese da Apresentação — Vanessa
**Tópicos:** Simulação de Eventos Discretos (DES), Validação do Modelo, Cenários *What-If* e Deslocamento de Gargalo  
**Slides:** 13, 14 e 15 de `Afericao_Filas_RU_Seminario.pptx`  
**Tempo Estimado de Fala:** ~3,5 a 4,0 minutos  
**Transição:** Recebe a palavra de **Otávio** (Modelagem Teórica) e devolve para **Adriana** (Conclusão e Recomendações).

---

## 1. Mapa Rápido dos Slides de Vanessa

```
┌───────────────────────────────────────────────────────────────────────────────────┐
│ SLIDE 13: Simulação por Eventos Discretos (DES) & Calibração de Baseline          │
│ • Motor de Simulação em Node.js guiado por traço real (Trace-Driven DES)          │
│ • Entrada: os 1.074 eventos de 04/11 com timestamps em milissegundos              │
│ • Preservação da dinâmica empírica: rajadas reais de chegada mantidas intactas    │
│ • Desacoplamento do tempo de serviço puro (duração líquida no posto sem espera)   │
│ • Validação do Baseline com precisão cirúrgica:                                   │
│   Fila 1 Real: 131,5 s  vs.  Simulado: 131,9 s  ===>  ERRO DE APENAS 0,27%!       │
│   Fila 2 Real: 142,1 s  vs.  Simulado: 163,8 s  ===>  Divergência de 15,3%        │
├───────────────────────────────────────────────────────────────────────────────────┤
│ SLIDE 14: Análise Comparativa de Cenários Contrafatuais (What-If)                 │
│ • Tabela com Baseline, Cenário 1 (2 Catracas), Cenário 2 (2 Catracas + 2 Buffets)  │
│   e Cenário 3 (Buffet Otimizado -20% no atendimento)                              │
│ • Cenário 1 (c1=2, c2=1): Wq1 cai de 131,9s para 55,2s (-58%), MAS Wq2 no buffet  │
│   explode de 163,8s para 238,1s (+45,4%) e fila máxima salta de 25 para 48 alunos! │
│ • Cenário 2 (c1=2, c2=2): Wq1 = 55,2s (-58%) e Wq2 = 60,2s (-63,2%). Trânsito cai │
│   de 295,7s para 106,7s (economia de 3,15 minutos por estudante!).                │
│ • Ocupação das mesas no Cenário 2: pico de 98 cadeiras (45,4% de 216) — sem lotar!│
├───────────────────────────────────────────────────────────────────────────────────┤
│ SLIDE 15: O Fenômeno de Deslocamento de Gargalo (Bottle-neck Shifting)            │
│ • Prova visual e empírica da armadilha de intervir em apenas uma etapa:           │
│   Ao dobrar a catraca sem mexer no buffet, a taxa de injeção salta para 6,6 p/min │
│   contra uma vazão de buffet de apenas 3,72 p/min.                                │
│ • O gargalo NÃO desaparece: ele é transferido da calçada externa para dentro do    │
│   corredor fechado de bandejas do salão!                                          │
│ • Recomendação técnica: intervenção combinada ou escalonada no pico.              │
└───────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Conceitos e Fundamentos Essenciais (Colar na Ponta da Língua)

* **O que é Simulação Trace-Driven (Guiada por Traço)?**  
  Em vez de sortear números pseudoaleatórios a partir de distribuições teóricas simplistas, o motor de eventos discretos lê o arquivo real `eventos.jsonl`. O instante exato em que cada um dos 192 alunos chegou à calçada é preservado com precisão de milissegundos. Isso captura perfeitamente as rajadas de turmas saindo das aulas sem distorções artificiais.
* **Desacoplamento de Serviço Puro:**  
  O simulador separa o tempo em que o aluno ficou aguardando na fila ($W_q$) do tempo em que ele efetivamente passou o cartão na catraca ou se serviu no balcão ($S$). Para cada aluno, seu tempo de serviço real medido em campo é atribuído ao próximo servidor livre na simulação.
* **Modelagem Multi-Servidor ($M/G/c$):**  
  Nos cenários com dois servidores ($c = 2$), a fila física permanece única (fila única com múltiplos caixas). O primeiro estudante da fila é atendido pelo primeiro servidor que se tornar ocioso (`findAvailableServer`), garantindo balanceamento dinâmico ótimo de carga.
* **Efeito de Bloqueio (*Service Blocking*):**  
  O simulador monitora a capacidade do Salão de Mesas ($K = 216$). Se o número de estudantes em refeição atingisse 216, o buffet seria obrigado a interromper o fluxo para evitar superlotação física. A simulação provou que o salão suporta o fluxo sem bloqueio.

---

## 3. Os Números de Vanessa (Memorizar para Citar no Palco)

### Calibração do Modelo Baseline (Simulador vs. Realidade em Campo)
* **Tempo de Espera na Catraca ($W_{q1}$):**
  * Observado Real: **131,5 segundos**
  * Simulado no Modelo: **131,9 segundos**
  * **Erro de Calibração: $\mathbf{\Delta = 0,27\%}$** (validação estatística quase perfeita!).
* **Tempo de Espera no Buffet ($W_{q2}$):**
  * Observado Real: **142,1 segundos**
  * Simulado no Modelo: **163,8 segundos** (divergência de 15,3%, decorrente da acomodação do acoplamento atômico).

### Resultados Numéricos dos Cenários Contrafatuais (*What-If*)

| Métrica Avaliada | Baseline ($c_1=1, c_2=1$) | Cenário 1 ($c_1=2, c_2=1$) | Cenário 2 ($c_1=2, c_2=2$) | Cenário 3 (Buffet -20%) |
| :--- | :---: | :---: | :---: | :---: |
| **Espera Fila 1 ($W_{q1}$)** | 131,9 s (2,2 min) | **55,2 s (0,9 min)** [$\mathbf{-58\%}$] | **55,2 s (0,9 min)** [$\mathbf{-58\%}$] | 131,9 s (2,2 min) |
| **Fila Máxima Fila 1** | 51 alunos | **22 alunos** [$\mathbf{-57\%}$] | **22 alunos** [$\mathbf{-57\%}$] | 51 alunos |
| **Espera Fila 2 ($W_{q2}$)** | 163,8 s (2,7 min) | **238,1 s (4,0 min)** [$\mathbf{+45,4\%}$] | **60,2 s (1,0 min)** [$\mathbf{-63,2\%}$] | **104,2 s (1,7 min)** [$\mathbf{-36\%}$] |
| **Fila Máxima Fila 2** | 25 alunos | **48 alunos** [$\mathbf{+92\%}$] ⚠️ | **12 alunos** [$\mathbf{-52\%}$] | 17 alunos [$\mathbf{-32\%}$] |
| **Tempo de Trânsito Total** | 295,7 s (4,9 min) | 293,3 s (4,9 min) [0%] | **106,7 s (1,8 min)** [$\mathbf{-64\%}$] | 236,1 s (3,9 min) [$-20\%$] |
| **Pico de Mesas Ocupadas** | 116 cadeiras (53,7%) | 118 cadeiras (54,6%) | **98 cadeiras (45,4%)** | 116 cadeiras (53,7%) |

---

## 4. O Ponto Alto de Vanessa: O Deslocamento de Gargalo (*Bottle-neck Shifting*)

O momento mais marcante e tecnicamente brilhante da apresentação de Vanessa está no **Slide 15**:

> *"Se a administração do RU disser: 'A fila da calçada está feia, vamos colocar uma segunda catraca', nós temos a prova computacional de que isso é um erro operacional gravíssimo!"*

### A Mecânica do Desastre do Cenário 1:
1. Ao adicionar uma 2ª catraca ($c_1 = 2$), a capacidade de escoamento da entrada salta de $3,32\text{ p/min}$ para **$6,64\text{ p/min}$**.
2. A fila externa sob o sol realmente diminui de 51 para 22 alunos, e a espera cai 58%.
3. **Porém**, o balcão de buffet continua com capacidade de apenas **$3,72\text{ p/min}$**.
4. Como a entrada agora injeta quase o dobro da capacidade do buffet, o acúmulo é transferido instantaneamente:
   * A espera no buffet sobe de 2,7 minutos para **4,0 minutos (+45%)**.
   * A fila interna salta de 25 para **48 estudantes aglomerados** no corredor interno.
5. O tempo total de trânsito até sentar à mesa praticamente **não muda** (caiu meros 2 segundos: de 295,7s para 293,3s). O aluno apenas trocou o calor da calçada pelo aperto dentro do refeitório!
6. **A Solução Sistêmica Real (Cenário 2):** Duplicar simultaneamente a catraca e o balcão de refeições ($c_1 = 2, c_2 = 2$). O trânsito despenca de 5 minutos para 1,8 minutos, e o salão de 216 mesas absorve com folga (pico de apenas 98 lugares ocupados).

---

## 5. Roteiro de Fala Direto (O que Falar no Palco)

### 🟢 Início da Fala (Recebendo de Otávio):
> *"Obrigada, Otávio. Boa tarde a todos. O Otávio nos mostrou a elegância matemática das Cadeias de Markov e da Lei de Little. Porém, no mundo real da gestão do campus, a direção do RU não quer apenas equações analíticas; ela quer saber: 'E se nós contratarmos mais um atendente? E se instalarmos uma segunda catraca na entrada? Qual será o impacto real nas filas?'. Para responder a essas perguntas com precisão de engenharia, nós implementamos um motor de Simulação por Eventos Discretos guiado por traço, cujos resultados apresento agora."*

### 🟢 Slide 13: Simulação de Eventos Discretos & Calibração Baseline:
> *"No Slide 13, apresentamos a arquitetura do nosso simulador. Ele é do tipo Trace-Driven: nós injetamos no motor os 1.074 eventos reais gravados no dia 4 de novembro. Com isso, preservamos exatamente a ordem temporal em milissegundos e as rajadas naturais de chegada dos alunos. Nós desacoplamos o tempo de espera do tempo de serviço puro de cada estudante. Antes de simular cenários futuros, submetemos o motor ao teste de validação cruzada do cenário Baseline. E o resultado foi impressionante: o tempo de espera médio real na Fila 1 foi de 131,5 segundos, e a nossa simulação registrou 131,9 segundos. Uma margem de erro de apenas 0,27%! Essa calibração quase cirúrgica nos dá total autoridade científica para rodar cenários 'What-If'."*

### 🟢 Slide 14: Comparativo de Cenários Contrafatuais (What-If):
> *"No Slide 14, avaliamos três cenários contrafatuais. No Cenário 1, simulamos a instalação de uma 2ª catraca na entrada. O tempo de espera na Fila 1 despenca 58%, caindo para 55 segundos. Porém, observem o que acontece com a Fila 2, o buffet: o tempo de espera dispara para quase 4 minutos (+45%) e a fila interna salta de 25 para 48 alunos! No Cenário 2, onde duplicamos simultaneamente a catraca e a linha de buffet, o sistema atinge o seu melhor desempenho: a espera na entrada cai 58%, a espera no buffet despenca 63%, e o tempo total de trânsito até a mesa cai de quase 5 minutos para apenas 1 minuto e 46 segundos — uma economia de mais de 3 minutos por estudante! E o salão de refeições suporta perfeitamente, com pico de 98 lugares ocupados de 216 disponíveis, provando que não há risco de bloqueio das mesas."*

### 🟢 Slide 15: O Fenômeno de Deslocamento de Gargalo (Bottle-neck Shifting):
> *"No Slide 15, detalhamos o achado conceitual mais importante da nossa simulação: o fenômeno do Deslocamento de Gargalo, ou Bottle-neck Shifting. Em redes de filas em série, intervir de forma isolada em um único elo da cadeia não resolve o problema do usuário final; apenas empurra o gargalo para a etapa seguinte. Ao dobrar a catraca sozinha no Cenário 1, ela passa a injetar 6,6 alunos por minuto em um buffet que só consegue escoar 3,7. O estudante sai mais rápido da calçada, mas fica preso no corredor interno do restaurante, e o tempo total de trânsito permanece praticamente idêntico. A simulação prova matematicamente que qualquer intervenção física deve ser casada ou focada no pico. Para consolidar as conclusões executivas do nosso trabalho, devolvo a palavra para a Adriana."*

---

## 6. Possíveis Perguntas da Banca e Respostas Rápidas

* **P1: "Por que vocês usaram simulação guiada por traço (Trace-Driven) em vez de distribuições estatísticas teóricas com números aleatórios?"**
  * *Resposta de Vanessa:* "A simulação trace-driven tem a enorme vantagem de reproduzir com fidelidade absoluta as correlações temporais reais da coleta — como rajadas pontuais de dezenas de estudantes que saem juntos de aulas que terminam às 11h50. Se usássemos geradores teóricos de Poisson clássicos, perderíamos essa memória estocástica de rajada, o que subestimaria o tamanho dos picos de fila."
* **P2: "Nos cenários com dois servidores, como o simulador distribui os alunos?"**
  * *Resposta de Vanessa:* "Nós adotamos o modelo clássico de fila única com múltiplos atendentes ($M/G/c$), que é comprovadamente superior a filas paralelas individuais. O primeiro aluno da fila é direcionado imediatamente ao primeiro servidor que ficar ocioso. Isso evita ociosidade espúria e maximiza a taxa de utilização combinada dos dois postos."
* **P3: "O salão de mesas não correria o risco de superlotar no Cenário 2, já que o fluxo de entrada dobrou?"**
  * *Resposta de Vanessa:* "Não. Nós testamos exatamente essa restrição rígida ($K = 216$). Como o tempo médio de refeição é de cerca de 23 minutos, a rápida injeção de alunos gerou um pico máximo simulado de 98 assentos ocupados, o que representa apenas 45,4% da capacidade total do salão. As 216 cadeiras instaladas oferecem margem de segurança de mais de 50%, sem nenhum bloqueio de serviço (*blocking*) no buffet."
