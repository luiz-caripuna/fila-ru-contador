# Síntese da Apresentação — Adriana
**Tópicos:** Introdução, Contextualização Operacional, Relato de Campo e Conclusão Geral  
**Slides:** 1, 2, 3, 4 (Abertura e Contexto) e 16, 17 (Conclusão e Perguntas) de `Afericao_Filas_RU_Seminario.pptx`  
**Tempo Estimado de Fala:** ~5 a 6 minutos no total (divididos em ~3,5 min no Bloco I e ~2,5 min no Bloco VI)  
**Papel de Liderança:** Abre o seminário, contextualiza o problema, passa a palavra para **Lucas** (Método), reassume após **Vanessa** (Simulação) para concluir e encerra a sessão.

---

## 1. Mapa Rápido dos Slides de Adriana

```
┌───────────────────────────────────────────────────────────────────────────────────┐
│ SLIDE 1: Capa Oficial                                                             │
│ • Apresentação do tema: Avaliação de Desempenho das Filas do RU Central           │
│ • Menção aos 5 integrantes da equipe e data da coleta: 04/11/2026 (65,34 minutos) │
├───────────────────────────────────────────────────────────────────────────────────┤
│ SLIDE 2: Agenda e Estrutura do Seminário                                          │
│ • O percurso lógico: Contexto ➔ Método ➔ Resultados ➔ Modelagem ➔ Simulação      │
│ • Apresentação dos papéis de cada colega na condução do trabalho                  │
├───────────────────────────────────────────────────────────────────────────────────┤
│ SLIDE 3: Contexto Operacional e as Três Filas em Série                            │
│ • O desafio real do RU no horário de almoço (alta concentração e gargalos)        │
│ • As 3 etapas: Fila 1 (Entrada/Vermelha), Fila 2 (Buffet/Verde) e Salão (Rosa)    │
│ • Pergunta central: "Onde ocorre o gargalo e qual intervenção dá melhor retorno?" │
├───────────────────────────────────────────────────────────────────────────────────┤
│ SLIDE 4: Organização de Campo e Diário de Bordo da Equipe                         │
│ • 1ª ida (21/10): evento no campus inviabilizou a rotina padrão                   │
│ • Replanejamento: melhorias na interface web móvel e protocolo de equipe          │
│ • 2ª ida (04/11): 1 hora exata solicitada pelo professor com 4 membros em campo:  │
│   2 na Fila 1 (Entrada/Catraca), 1 na Fila 2 (Buffet) e 1 na Saída                │
├───────────────────────────────────────────────────────────────────────────────────┤
│ SLIDE 16: Conclusão Operacional: Quando, Quanto e Por Quê                        │
│ • QUANDO: janela central de pico de 20 minutos (minutos 30 a 50 do almoço)        │
│ • QUANTO: fila externa de até 51 alunos, P90 de 9 min, permanência total de 29 min│
│ • POR QUÊ: λ no pico (3,80 p/min) > μ da catraca (3,32 p/min) e filas acopladas   │
│ • RECOMENDAÇÃO: reforço flexível no pico (11h45–12h30) com 2ª catraca + 2º buffet │
├───────────────────────────────────────────────────────────────────────────────────┤
│ SLIDE 17: Encerramento e Agradecimentos                                           │
│ • Agradecimento à banca/professor e abertura para a sessão de perguntas           │
└───────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Conceitos e Fundamentos Essenciais (Colar na Ponta da Língua)

* **Visão Sistêmica de Filas em Série:** O restaurante não é uma fila única, mas uma rede em cascata (Entrada $\to$ Buffet $\to$ Mesas $\to$ Saída). O que acontece em uma etapa dita o ritmo da próxima.
* **A Regra de Ouro do Professor:** O objetivo não é apenas descrever números, mas **diagnosticar causas** e propor intervenções viáveis com base em dados (*Quando, Quanto e Por Quê*).
* **Capacidade Física do Salão:** O salão tem **216 cadeiras** (36 mesas $\times$ 6 lugares). Não há falta de espaço físico para sentar; o gargalo está nas transições de serviço.
* **Coordenação do Tempo:** Adriana é a guardiã do cronômetro. Se algum colega se estender, ela garante que as transições sejam ágeis para fechar o seminário dentro dos 18 a 20 minutos.

---

## 3. Os Números de Adriana (Dados Reais para Citar com Firmeza)

* **Duração da Coleta:** 65,34 minutos (1 hora solicitada pelo docente).
* **Volume Aferido:** 1.074 eventos gravados e 192 estudantes atendidos.
* **Pico Físico:** 51 pessoas acumuladas na calçada externa (Fila 1).
* **Tempo de Permanência Total:** Média de **29 minutos** no complexo do RU (espera na fila externa + espera no buffet + 23 minutos de refeição nas mesas).
* **Horário Crítico:** Janela das **12h00 às 12h20** (minutos 30 a 50 da coleta), onde $\lambda = 3,80\text{ p/min}$ e $\mu = 3,32\text{ p/min}$ ($\rho = 1,14 > 1,0$).

---

## 4. O Ponto Alto de Adriana: A Resposta Executiva (Quando, Quanto e Por Quê)

O momento mais forte da apresentação de Adriana é o **Slide 16**, onde ela sintetiza todo o trabalho em 3 respostas diretas e uma recomendação acionável:
1. **QUANDO?** O problema não dura o dia todo. Ocorre exclusivamente em uma janela de 20 minutos no miolo do almoço (minutos 30 a 50).
2. **QUANTO?** Filas de até 51 estudantes na calçada sob o sol, 10% dos alunos esperando mais de 9 minutos e permanência de quase meia hora.
3. **POR QUÊ?** Inversão estocástica ($\lambda_{\text{pico}} > \mu$) e acoplamento em série (se abrir apenas a catraca, o corredor interno do buffet colapsa).
4. **RECOMENDAÇÃO PRÁTICA:** Escala flexível de pico (11h45–12h30) com abertura casada de **2ª catraca + 2ª linha de buffet**, aproveitando as 216 mesas existentes que têm folga para absorver o fluxo.

---

## 5. Roteiro de Fala Direto (O que Falar no Palco)

### 🎙️ Abertura (Slides 1 e 2) — ~1 min:
> *"Boa tarde, professor e colegas. Nosso grupo é composto por mim, Adriana, e pelos colegas Jaiane, Lucas, Otávio e Vanessa. Hoje apresentamos o trabalho de Avaliação de Desempenho focado na aferição, modelagem analítica e simulação das filas do Restaurante Universitário Central.*
> 
> *Estruturamos nosso seminário em um percurso completo de engenharia: eu inicio contextualizando o RU e nossa experiência em campo; o Lucas apresenta a ferramenta web e o método de coleta; a Jaiane traz os dados da medição, separando calma e pico; o Otávio formaliza o modelo matemático de filas e a Lei de Little; a Vanessa demonstra a simulação de cenários e o deslocamento de gargalo; e, ao final, retorno com as respostas executivas: quando, quanto e por quê."*

### 🎙️ Contexto e Organização de Campo (Slides 3 e 4) — ~2,5 min:
> *"No Slide 3, vemos a topologia do RU. Para entender o sistema, nós o modelamos em três etapas sequenciais: a Fila 1, em vermelho, na calçada até a catraca; a Fila 2, em verde, que contorna a linha de buffet onde o aluno se serve; e o Salão de Mesas com a Fila 3, em rosa, que compreende as 216 cadeiras e a saída final. Nossa pergunta central foi: onde realmente está o gargalo e qual intervenção de capacidade produz o melhor retorno?*
> 
> *No Slide 4, compartilhamos nosso relato de campo. Nossa equipe se organizou inicialmente para ir ao RU no dia 21 de outubro. Porém, estava ocorrendo um evento na universidade que alterou totalmente o fluxo e dificultou a medição padrão. Além disso, identificamos que o sistema precisava de melhorias nos botões de coleta para evitar cliques duplos acidentais. Replanejamos nossa ida para o dia 04 de novembro de 2026. Chegamos cedo e, como nem todos conseguiram ir, quatro pessoas ficaram responsáveis pela operação durante 1 hora, como solicitado pelo professor: 2 pessoas ficaram na Fila 1 (uma marcando chegadas na calçada e outra na catraca), 1 pessoa na saída do buffet e 1 pessoa registrando a saída final após as mesas. Passo a palavra ao Lucas, que explicará o método e o sistema web desenvolvido."*

*(... Lucas, Jaiane, Otávio e Vanessa apresentam ...)*

### 🎙️ Conclusão e Recomendações (Slides 16 e 17) — ~2,5 min:
> *"Obrigada, Vanessa. Retomo agora para consolidar o diagnóstico operacional final respondendo às três perguntas essenciais da avaliação de desempenho:*
> 
> *Primeiro: QUANDO ocorre o gargalo? O problema não existe o tempo todo. Ele se concentra em uma janela de 20 minutos no miolo do almoço, entre os minutos 30 e 50 da coleta (aproximadamente 12h00 às 12h20).*
> 
> *Segundo: QUANTO é o impacto? No pico, a fila externa acumula até 51 pessoas na calçada, com 10% dos estudantes esperando mais de 9 minutos só na entrada e tempo total médio de 29 minutos no RU.*
> 
> *Terceiro: POR QUÊ ocorre? Porque a taxa de chegada de pico de 3,80 alunos por minuto supera a capacidade de 1 catraca (3,32 p/min), gerando utilização de 114%. Além disso, como as filas são encadeadas, abrir apenas a catraca transfere a fila para o buffet.*
> 
> *Nossa recomendação para a gestão do RU é clara: não é preciso obras nem compra de mesas. Basta instituir uma escala de reforço flexível entre 11h45 e 12h30 com ativação casada da 2ª catraca e de uma 2ª pista de buffet, reduzindo o tempo de retenção do estudante em 63%.*
> 
> *Finalizamos agradecendo ao professor e a todos pela atenção. Estamos à disposição para perguntas da banca!"*

---

## 6. Três Perguntas Prováveis da Banca para Adriana

1. **"Por que vocês não fizeram a coleta em um dia de evento para comparar?"**  
   * **Resposta:** *"A diretriz pedagógica da disciplina era capturar o comportamento operacional padrão do restaurante em regime regular. Um dia de evento universitário introduz ruídos externos atípicos (visitantes de fora, horários irregulares de ônibus) que mascaram o dimensionamento correto do dia a dia."*
2. **"Por que vocês recomendam reforço apenas entre 11h45 e 12h30?"**  
   * **Resposta:** *"Porque os dados demonstraram que nos primeiros 10 minutos e após o pico a utilização fica abaixo de 30% e a catraca opera ociosa. Manter servidores extras durante todo o dia geraria desperdício de custo operacional sem benefício real."*
3. **"Como vocês garantiram que as 4 pessoas em campo conseguiram cobrir as 3 filas?"**  
   * **Resposta:** *"Graças ao encadeamento atômico do software desenvolvido pelo Lucas. Como a saída da catraca gerava automaticamente a entrada no buffet, bastou colocar 1 pessoa na calçada, 1 na catraca, 1 no buffet e 1 na saída, cobrindo o percurso integral de ponta a ponta sem lacunas."*
