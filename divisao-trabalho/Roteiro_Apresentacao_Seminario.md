# Roteiro de Apresentação do Seminário: Filas do RU

**Disciplina:** Avaliação de Desempenho de Sistemas  
**Tema:** Aferição, Modelagem e Simulação das Filas do Restaurante Universitário  
**Tempo Total Planejado:** 18 a 20 minutos (aprox. 3,5 a 4 minutos por integrante)  
**Arquivo de Slides:** `Afericao_Filas_RU_Seminario.pptx` (17 slides em formato widescreen 16:9)

---

## 1. Visão Geral da Escala de Apresentação

| Bloco | Slides | Integrante | Tópico Principal | Tempo Estimado |
| :---: | :---: | :--- | :--- | :---: |
| **I** | 1, 2, 3 e 4 | **Adriana** | Abertura, Contextualização do RU e Relato de Campo | ~3,5 min |
| **II** | 5 e 6 | **Lucas** | Método de Aferição, Arquitetura Web e Coleta Mobile | ~3,0 min |
| **III** | 7, 8 e 9 | **Jaiane** | Resultados Empíricos, Calma vs. Pico e Dispersão $W_q$ | ~4,0 min |
| **IV** | 10, 11 e 12 | **Otávio** | Modelagem Teórica, Matriz P, $M/M/1$ e Lei de Little | ~4,0 min |
| **V** | 13, 14 e 15 | **Vanessa** | Simulação *Trace-Driven DES*, Baseline e Cenários *What-If* | ~4,0 min |
| **VI** | 16 e 17 | **Adriana** | Conclusão (Quando, Quanto e Por Quê) e Encerramento | ~2,5 min |

---

## 2. Roteiro Fala a Fala (Slide a Slide)

### 🎙️ BLOCO I: ABERTURA E CONTEXTO (Adriana)

#### Slide 1: Capa
* **Tempo:** 30 segundos
* **O que falar:**
  > "Boa tarde a todos, professor e colegas. Nosso grupo é composto por mim, Adriana, e pelos colegas Jaiane, Lucas, Otávio e Vanessa. Hoje vamos apresentar o trabalho final da disciplina de Avaliação de Desempenho de Sistemas, com foco na aferição experimental, modelagem analítica e simulação computacional das filas do nosso Restaurante Universitário Central."

#### Slide 2: Visão Geral e Agenda
* **Tempo:** 45 segundos
* **O que falar:**
  > "Nosso objetivo é transformar observação empírica de campo em evidência quantitativa de engenharia. Para isso, estruturamos a apresentação em cinco etapas lógicas: eu inicio contextualizando o problema e relatando nossa experiência de campo; o Lucas apresenta o método e a ferramenta web que desenvolvemos; a Jaiane traz os dados da coleta, diferenciando calma e pico; o Otávio formaliza o modelo matemático de filas e a Lei de Little; a Vanessa demonstra o simulador de eventos discretos e compara os cenários de melhoria; e, ao final, retorno com as conclusões práticas respondendo: quando, quanto e por quê."

#### Slide 3: Contexto Operacional e as Três Filas
* **Tempo:** 1 minuto
* **O que falar:**
  > "O Restaurante Universitário enfrenta um desafio clássico de picos de demanda no horário de almoço. Para entender o sistema, nós modelamos o restaurante não como uma fila isolada, mas como um fluxo contínuo em série com três etapas: a Fila 1, em vermelho, que é a fila externa na calçada até a catraca de identificação; a Fila 2, em verde, que contorna o corredor até o buffet onde o aluno pega a bandeja com a refeição; e o Salão de Refeições com a Fila 3, em rosa, que compreende as mesas com capacidade nominal de 216 cadeiras e a saída final. A pergunta que guiou nosso projeto foi: onde realmente está o gargalo e qual intervenção de capacidade produz o melhor retorno para o estudante?"

#### Slide 4: Relato de Campo e Organização da Equipe
* **Tempo:** 1 minuto e 15 segundos
* **O que falar:**
  > "Nossa equipe se organizou inicialmente para ir ao RU no dia 21 de outubro. No entanto, naquele dia estava ocorrendo um evento na universidade que alterou totalmente a rotina do restaurante, dificultando uma aferição padrão. Além disso, percebemos que o sistema precisava de melhorias nos botões de coleta para evitar cliques acidentais. Replanejamos nossa ida para o dia 04 de novembro de 2026. Chegamos cedo para montar a infraestrutura e, como nem todos puderam estar no local, quatro pessoas ficaram responsáveis pela operação durante 1 hora exata, como solicitado pelo professor. Ficamos organizados assim: dois operadores ficaram dedicados à Fila 1 (um na entrada marcando chegadas e outro na catraca), uma pessoa na Fila 2 ao final do atendimento e uma pessoa registrando a saída final após as mesas. Passo agora a palavra ao Lucas, que explicará o método e o sistema que construímos para viabilizar essa coleta."

---

### 🎙️ BLOCO II: MÉTODO E ENGENHARIA DE SOFTWARE (Lucas)

#### Slide 5: Método & Arquitetura Web (*Offline-First*)
* **Tempo:** 1 minuto e 30 segundos
* **O que falar:**
  > "Obrigado, Adriana. Um dos grandes desafios em medições de campo no RU é que os refeitórios costumam ter paredes espessas e sinal 4G/5G instável. O uso de cronômetros manuais e pranchetas introduz erros humanos graves de sincronismo. Por isso, desenvolvemos o sistema web Fila RU com uma arquitetura autônoma e 'offline-first'. O notebook da coordenação emitiu um Hotspot Wi-Fi local próprio. Nossos celulares conectaram diretamente a ele pelo navegador via WebSockets locais, sem consumir internet e sem precisar instalar nenhum aplicativo. A solução foi desenhada em Node.js nativo com o padrão Event Sourcing: cada toque gerou um evento imutável com carimbo de tempo em milissegundos gravado em arquivo jsonl. Mesmo que o sinal Wi-Fi oscilasse, os toques eram salvos no localStorage do celular e descarregados em ordem ao reconectar, garantindo auditoria completa e replay temporal."

#### Slide 6: Coleta em Campo e Encadeamento Atômico
* **Tempo:** 1 minuto e 30 segundos
* **O que falar:**
  > "Na interface dos celulares, desenhamos botões táteis gigantes para que o operador pudesse registrar os eventos com uma mão só, sem tirar os olhos da fila. Criamos travas como o botão 'Reverter', caso alguém tocasse por engano, e o botão 'Anular', para desistências reais. Mas o diferencial técnico do método foi o Encadeamento Atômico: quando a Adriana confirmava no celular que o aluno passou na catraca, o sistema registrava a saída da Fila 1 e, no mesmíssimo milissegundo, gerava a entrada daquela mesma pessoa na Fila 2. E quando o aluno pegava a bandeja na Fila 2, ele passava automaticamente a ocupar uma cadeira no salão. Isso nos deu rastreabilidade contínua de ponta a ponta, permitindo calcular o tempo de trânsito integral de cada estudante. Agora, a Jaiane apresentará os resultados que essa ferramenta coletou."

---

### 🎙️ BLOCO III: RESULTADOS EXPERIMENTAIS (Jaiane)

#### Slide 7: Resultados Globais das Três Filas
* **Tempo:** 1 minuto e 15 segundos
* **O que falar:**
  > "Obrigada, Lucas. Durante os 65,34 minutos de coleta contínua, registramos 1.074 eventos e 192 estudantes que completaram a Fila 1 e Fila 2. Conforme vemos na tabela, a taxa média de chegadas foi de 2,94 pessoas por minuto. A capacidade da catraca foi de 3,32 pessoas por minuto, o que resultou em um fator de utilização global de 88,6% na Fila 1. Na Fila 2 (o buffet), a capacidade foi ligeiramente maior, de 3,72 pessoas por minuto, com utilização de 79,1%. O tempo médio de espera foi de 2 minutos e 11 segundos na entrada e 2 minutos e 22 segundos no buffet. Já na Fila 3, observamos uma utilização aparente de 132%, porque os alunos passam em média 23 minutos almoçando nas mesas; logo, dos 185 que entraram, 95 saíram durante a nossa hora de coleta e 90 ainda estavam terminando a refeição."

#### Slide 8: Separação Rigorosa: Calma vs. Pico
* **Tempo:** 1 minuto e 30 segundos
* **O que falar:**
  > "Seguindo com rigor o checklist da disciplina, fizemos a separação entre calma e pico pelas chegadas por minuto, e não pelas ondas visuais da fila. Se olhássemos só o tamanho da fila, seríamos enganados. Ao tabularmos os blocos de 5 minutos, constatamos duas fases nítidas: nos primeiros 10 minutos (Regime de Calma), chegaram apenas 6 alunos no total, uma taxa de apenas 0,60 pessoas por minuto. A catraca operou com utilização de 18%, praticamente vazia. Porém, a partir do minuto 30 e até o minuto 50, entramos no Regime de Pico: a demanda saltou para 19 chegadas a cada 5 minutos, ou seja, 3,80 pessoas por minuto. Como a capacidade máxima da catraca é de 3,32 pessoas por minuto, ocorreu a inversão estocástica: lambda superou mi. Com rho maior que 1, a fila explodiu, atingindo o pico físico de 51 pessoas acumuladas na calçada."

#### Slide 9: Distribuição de Espera (Wq) e Dispersão
* **Tempo:** 1 minuto e 15 segundos
* **O que falar:**
  > "A análise das medidas de dispersão revela a desigualdade enfrentada pelos alunos dependendo do horário de chegada. Na Fila 1, a média foi de 2 minutos e 11 segundos, mas a mediana foi de apenas 27 segundos! Ou seja, metade dos alunos passou quase direto. Por outro lado, o Percentil 90 foi de 9 minutos e 2 segundos, e o pior caso registrado esperou 16 minutos e 18 segundos na calçada sob o sol. Na Fila 2, o tempo foi mais previsível, com desvio padrão menor. No percurso total até as mesas, 10% dos estudantes perderam mais de 13 minutos e meio na soma das filas. As mesas, contudo, atingiram pico de 116 cadeiras ocupadas de 216 disponíveis, operando em nível moderado. Agora, o Otávio mostrará como modelamos esses dados matematicamente."

---

### 🎙️ BLOCO IV: MODELAGEM TEÓRICA (Otávio)

#### Slide 10: Modelagem: Espaço de Estados e Parâmetros
* **Tempo:** 1 minuto e 15 segundos
* **O que falar:**
  > "Obrigado, Jaiane. Para modelar o sistema formalmente, definimos o estado N(t) como o número discreto de pessoas presentes em cada subsistema no instante t. As transições ocorrem por eventos pontuais de nascimento (chegadas a uma taxa lambda) e morte (atendimentos a uma taxa mi). Utilizamos o passo analítico de 5 minutos para confrontação de blocos e representamos a restrição física das mesas com capacidade K igual a 216 assentos. A partir dessa formulação, estabelecemos as equações de probabilidades de estado P_n, que nos permitem deduzir a probabilidade de fila vazia e o comportamento assintótico."

#### Slide 11: Matriz de Transição P e Equações M/M/1
* **Tempo:** 1 minuto e 15 segundos
* **O que falar:**
  > "Para um intervalo infinitesimal delta t, o processo é governado pela Matriz de Transição estocástica P, que tem formato tridiagonal clássico de cadeias de nascimento e morte. Aplicando o balanço de fluxo nos cortes estacionários, temos que a taxa de saída de um estado deve igualar a taxa de entrada, resultando em P_n igual a (1 - rho) vezes rho elevado a n. A partir dessa distribuição deduzimos as fórmulas clássicas de M/M/1 apresentadas no slide: o número médio na fila Lq igual a rho ao quadrado sobre (1 - rho), e o tempo médio de espera Wq dado por rho sobre (mi - lambda). Aplicando os parâmetros médios da Fila 1, o modelo teórico M/M/1 prevê uma espera média de 140 segundos e probabilidade de sistema vazio de 11,4%."

#### Slide 12: Verificação Experimental da Lei de Little
* **Tempo:** 1 minuto e 30 segundos
* **O que falar:**
  > "Para verificar a consistência matemática do nosso estudo, confrontamos os dados com a célebre Lei de Little: Lq deve ser igual a lambda vezes Wq. O resultado na Fila 2 (o buffet) foi extraordinário: o Lq medido diretamente pela integral temporal foi de 6,72 alunos, enquanto o produto lambda vezes Wq resultou em 6,96 alunos. Isso representa uma divergência de apenas 3,48%, comprovando com rigor experimental a consistência teórica da nossa medição. Já na Fila 1, encontramos uma divergência de 49%. E por que isso aconteceu? A teoria de Little pressupõe regime permanente estável; porém, como o Lucas e a Adriana registraram, a coleta começou com 27 alunos já acumulados antes da catraca abrir. Esse regime transitório inicial elevou a média de Lq. Quando isolamos a operação contínua após a abertura, o desvio cai abaixo de 10%. Passo agora à Vanessa para apresentar a simulação computacional."

---

### 🎙️ BLOCO V: SIMULAÇÃO COMPUTACIONAL (Vanessa)

#### Slide 13: Simulador DES Guiado por Traço Histórico
* **Tempo:** 1 minuto e 15 segundos
* **O que falar:**
  > "Obrigada, Otávio. Para responder a perguntas do tipo 'o que aconteceria se...', construímos o módulo de simulação por eventos discretos do Fila RU. Nosso diferencial foi utilizar uma Simulação Guiada por Traço Histórico (Trace-Driven DES). Em vez de inventar números aleatórios com distribuições teóricas que não refletem a universidade, o simulador utilizou o traço real dos horários exatos em que cada um dos 192 alunos chegou. O motor desacoplou o tempo de serviço puro observado na catraca e no buffet, simulou a fila única compartilhada para múltiplos servidores e implementou a lógica de Service Blocking para caso as mesas atingissem 100% de ocupação."

#### Slide 14: Verificação e Validação: Baseline
* **Tempo:** 1 minuto e 15 segundos
* **O que falar:**
  > "Antes de simular novos cenários, validamos o simulador rodando o cenário de referência (baseline com 1 catraca e 1 buffet). O resultado de calibração foi excelente: o tempo médio de espera real na Fila 1 foi de 131,52 segundos, e o simulador gerou 131,88 segundos. Isso representa um erro relativo de apenas 0,27%, muito abaixo do limite de tolerância de 5% preconizado na literatura de avaliação de desempenho. Todas as 192 chegadas e atendimentos foram conservados sem perdas, garantindo que o simulador estava verificado, validado e pronto para os testes de cenários."

#### Slide 15: Comparação de Cenários What-If e Deslocamento de Gargalo
* **Tempo:** 1 minuto e 30 segundos
* **O que falar:**
  > "Seguindo a regra de ouro da avaliação de desempenho, variamos exatamente uma dimensão operacional por vez. No Cenário 1, simulamos a adição de uma segunda catraca na entrada (c1 = 2). O resultado foi revelador: a espera na Fila 1 caiu 58%, de 131 para 55 segundos. Porém, o tempo de trânsito até a mesa não mudou! Por quê? Porque o buffet continuava com 1 atendente. A entrada rápida despejou uma onda de alunos no corredor interno: a espera no buffet subiu 45% (de 163 para 238 segundos) e o pico de alunos na fila interna pulou de 25 para 48 pessoas! Nós comprovamos computacionalmente o fenômeno do Deslocamento de Gargalo (Bottle-neck Shifting): apenas tirou-se o aluno do sol na calçada e colocou-se ele espremido no corredor do prato. A solução real surgiu no Cenário 2, onde duplicamos a catraca E o buffet simultaneamente: a espera no buffet caiu para 60 segundos e o tempo total de trânsito despencou 63%, de quase 5 minutos para apenas 1,7 minuto. E o salão de 216 mesas suportou com folga, atingindo pico de 98 lugares. Retorno agora à Adriana para as conclusões finais."

---

### 🎙️ BLOCO VI: CONCLUSÃO E RECOMENDAÇÕES (Adriana)

#### Slide 16: Diagnóstico Final: Quando, Quanto e Por Quê
* **Tempo:** 1 minuto e 45 segundos
* **O que falar:**
  > "Obrigada, Vanessa. Concluímos nosso trabalho respondendo de forma objetiva às três perguntas fundamentais da avaliação:
  > Primeiro: QUANDO ocorre o gargalo? O problema não existe o tempo todo. Ele se concentra em uma janela de 20 minutos no miolo do almoço, entre os minutos 30 e 50 da operação (aproximadamente 12h00 às 12h20).
  > Segundo: QUANTO é o impacto? No pico, a fila externa acumula até 51 pessoas simultâneas, com 10% dos estudantes esperando mais de 9 minutos só na entrada, e permanência média total de 29 minutos no RU.
  > Terceiro: POR QUÊ ocorre? Porque a taxa de chegada no pico (3,80 p/min) é maior que a capacidade de 1 catraca (3,32 p/min), gerando utilização de 114%. Além disso, como as filas são encadeadas, mexer apenas na catraca empurra o represamento para o buffet.
  > Como recomendação prática para a administração do RU: não é necessário contratar funcionários para o dia inteiro, nem ampliar o salão de mesas. Basta adotar uma escala flexível de reforço entre 11h45 e 12h30, ativando simultaneamente a segunda catraca e uma segunda pista de buffet, reduzindo o tempo de retenção do estudante em 63%."

#### Slide 17: Encerramento e Perguntas
* **Tempo:** 30 segundos
* **O que falar:**
  > "Finalizamos agradecendo ao professor e a todos pela atenção. Todo o código do Fila RU, os dados brutos e os testes automatizados estão documentados e disponíveis no repositório do projeto. Estamos à disposição para perguntas e comentários da banca. Muito obrigada!"

---

## 3. Dicas Práticas para o Ensaio da Equipe

1. **Cronômetro Ligado:** Durante o ensaio, um integrante (sugestão: Otávio ou Lucas) deve cronometrar a fala de cada um para garantir que ninguém ultrapasse 4 minutos.
2. **Passagem do Bastão Clara:** Cada integrante deve finalizar chamando o próximo pelo nome com uma frase de conexão (ex: *"Passo agora a palavra ao Otávio..."*).
3. **Não Ler os Textos dos Slides:** Os slides foram montados com cartões executivos e dados-chave. O apresentador deve olhar para a turma/banca e explicar os conceitos com suas próprias palavras, usando os números do slide apenas como âncora visual.
4. **Demonstração Rápida da Ferramenta (se houver tempo):** Lucas pode deixar uma aba aberta com `historico.html` e a barra de replay pronta para mostrar ao professor em caso de pergunta sobre a coleta.
