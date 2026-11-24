# Síntese da Apresentação — Lucas
**Tópicos:** Método de Aferição, Engenharia de Software, Arquitetura Offline-First e Coleta Mobile  
**Slides:** 5 e 6 de `Afericao_Filas_RU_Seminario.pptx`  
**Tempo Estimado de Fala:** ~3,0 minutos  
**Transição:** Recebe a palavra de **Adriana** (Contexto e Campo) e passa para **Jaiane** (Resultados).

---

## 1. Mapa Rápido dos Slides de Lucas

```
┌───────────────────────────────────────────────────────────────────────────────────┐
│ SLIDE 5: Método & Arquitetura Web (Solução Autônoma e Offline-First)              │
│ • Zero Dependência de Nuvem: Hotspot Wi-Fi local emitido pelo notebook            │
│ • Celulares dos operadores conectam pelo navegador sem gastar 4G/5G               │
│ • Event Sourcing Append-Only: log imutável de eventos ordenados em `eventos.jsonl`│
│ • Tolerância a quedas de rede: fila offline no localStorage (flag `tardio: true`) │
│ • Proteção de concorrência: autenticação por PIN de 4 dígitos e idempotência      │
├───────────────────────────────────────────────────────────────────────────────────┤
│ SLIDE 6: Operação de Campo & Encadeamento Atômico                                 │
│ • Interface Mobile (celular.html): botões gigantes projetados para toque com 1 mão│
│ • Perfis especializados: quem fica na entrada só vê "CHEGADA", na catraca só      │
│   vê "ATENDIDO" com o ID do próximo aluno                                         │
│ • Tolerância a erros: botões "Reverter Último" e "Anular (×)"                     │
│ • Encadeamento Atômico (1 > 2 e 2 > 3): a saída da catraca gera entrada imediata  │
│   no buffet mantendo o mesmo número e timestamp em milissegundos                  │
└───────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Conceitos e Fundamentos Essenciais (Colar na Ponta da Língua)

* **Arquitetura Zero-Cloud / Hotspot Local:** O notebook do coordenador funcionou como servidor central e ponto de acesso Wi-Fi local (`192.168.137.1:3000`). Os smartphones acessaram via navegador web sem necessidade de internet, instalador ou custos de nuvem.
* **Event Sourcing Puro:** Em vez de registrar tabelas com o "estado atual da fila", o sistema grava cada toque do operador como um evento imutável com timestamp em milissegundos. O estado em qualquer instante $t$ é calculado pela função determinística:
  $$\text{Estado}(t) = \text{derivarEstado}(\text{Eventos}, t)$$
  Isso possibilita o recurso de **Replay Temporal** (reproduzir o segundo exato da fila em 1x, 5x, 10x ou 60x).
* **Encadeamento Atômico (Chaining):** Mecanismo de software que transforma a saída de uma fila na entrada da próxima no mesmo evento do servidor:
  $$\text{Saída}(\text{F1}, \text{Pessoa } k, t) \implies \text{Entrada}(\text{F2}, \text{Pessoa } k, t)$$
* **Idempotência e Concorrência:** Cada clique gera um `clientEventId` único. Se dois operadores tocarem no mesmo botão simultaneamente, o servidor valida o primeiro e responde ao segundo com `JA_ATENDIDO`, impedindo contagens duplicadas.

---

## 3. Os Números de Lucas (Dados Reais de Engenharia de Software)

* **Eventos Gravados:** 1.074 eventos gravados sequencialmente em `eventos.jsonl` (tamanho: 75,5 KB).
* **Conexões Registradas:** 74 eventos de conexão e reconexão monitorados no log `conexoes.jsonl`.
* **Latência Média na Rede Local:** Inferior a 100 milissegundos via WebSockets nativos.
* **Perdas de Pacotes ou Dados:** **Zero perdas** — 192 chegadas = 192 atendimentos processados com 10 anulações de desistência registradas e 2 reversões de toque.

---

## 4. O Ponto Alto de Lucas: O Encadeamento Atômico que Viabilizou a Coleta com 4 Pessoas

O grande trunfo técnico de Lucas é demonstrar como a engenharia de software contornou a escassez de pessoas em campo:
> *Se a medição fosse manual com pranchetas, seriam necessárias pelo menos 6 pessoas (2 para marcar entrada e saída da F1, 2 para entrada e saída da F2, e 2 para mesas/saída), correndo alto risco de perder a identidade de quem é quem.*
> 
> *Com o **Encadeamento Atômico**, 4 operadores cobriram perfeitamente as 3 filas: o operador da catraca, ao clicar em "ATENDIDO", liberava o aluno da Fila 1 e inseria o mesmíssimo estudante na Fila 2 de forma automática e atômica. Isso garantiu o cálculo exato do tempo de trânsito individual ($W_{q1} + W_{q2}$) sem margem de erro.*

---

## 5. Roteiro de Fala Direto (O que Falar no Palco)

### 🎙️ Slide 5: Método e Arquitetura Web — ~1,5 min:
> *"Obrigado, Adriana. Boa tarde a todos. Um dos maiores desafios práticos de engenharia ao medir o Restaurante Universitário é que os refeitórios costumam ter paredes grossas de concreto, onde o sinal 4G e 5G é fraco ou simplesmente não funciona. Métodos antigos com cronômetros e pranchetas geram erros humanos de sincronismo e perda de dados.*
> 
> *Para resolver isso com tecnologia de ponta, nós desenvolvemos a aplicação web **Fila RU**, com arquitetura autônoma e 'offline-first'. O notebook da coordenação atuou como um servidor local nativo em Node.js emitindo sua própria rede Wi-Fi. Os smartphones dos operadores conectaram diretamente pelo navegador web via WebSockets, sem consumir internet, sem instalar aplicativo e com custo zero de nuvem.*
> 
> *Adotamos o padrão arquitetural de **Event Sourcing**: cada toque do operador gerou um evento imutável com carimbo de data e hora em milissegundos gravado sequencialmente em arquivo jsonl. O estado da fila em qualquer instante é derivado por função pura, o que nos permitiu criar um player de Replay temporal completo. E se algum operador se afastasse do Wi-Fi, os toques ficavam salvos na memória do próprio celular e eram sincronizados automaticamente ao reconectar, sem perda de dados."*

### 🎙️ Slide 6: Coleta em Campo e Encadeamento Atômico — ~1,5 min:
> *"No Slide 6, vemos como isso funcionou na prática nas mãos dos operadores. A interface móvel foi desenhada com princípios de ergonomia: botões táteis gigantes na tela, permitindo que a gente marcasse as pessoas com apenas um polegar, sem precisar tirar os olhos da fila física. Criamos perfis dedicados: quem ficava na entrada só via o botão de 'CHEGADA'; quem operava na catraca via o botão 'PASSOU NA CATRACA' com o número da próxima pessoa da fila.*
> 
> *Implementamos mecanismos de segurança como o botão 'Reverter', caso o operador tocasse por engano antes do aluno passar, e o botão 'Anular', para desistências reais.*
> 
> *Mas o grande diferencial técnico que permitiu que apenas quatro pessoas medissem três filas com precisão cirúrgica foi o **Encadeamento Atômico**: quando a Adriana confirmava a passagem na catraca, o sistema encerrava a Fila 1 e, no mesmo milissegundo, gerava a entrada daquele mesmo estudante na Fila 2, preservando o número do aluno e a linha do tempo. E quando a Jaiane confirmava a entrega da bandeja, o aluno passava a ocupar uma cadeira no salão.*
> 
> *Isso nos deu rastreabilidade contínua de ponta a ponta. Passo a palavra para a Jaiane, que apresentará os dados consolidados que o nosso sistema registrou."*

---

## 6. Três Perguntas Prováveis da Banca para Lucas

1. **"Por que vocês não usaram um banco de dados tradicional como MySQL ou MongoDB em vez de Event Sourcing com JSONL?"**  
   * **Resposta:** *"Porque em coletas móveis de alta velocidade em tempo real, escritas append-only em arquivo sequencial (`eventos.jsonl`) têm latência próxima de zero e são imutáveis à prova de corrupção. Além disso, o Event Sourcing preserva a história completa segundo a segundo, permitindo rebobinar e reproduzir o replay exato de toda a operação."*
2. **"O que acontecia se dois operadores clicassem no botão ao mesmo tempo?"**  
   * **Resposta:** *"O servidor Node.js opera com um event loop centralizado e validação atômica de concorrência com chave `clientEventId`. Se dois operadores tentassem atender a mesma pessoa simultaneamente, o servidor processava o primeiro e rejeitava o segundo com a mensagem `JA_ATENDIDO`, garantindo consistência estrita."*
3. **"Essa aplicação consegue rodar em qualquer universidade ou restaurante comercial?"**  
   * **Resposta:** *"Sim. Como foi construída em Vanilla JavaScript e Node.js nativo sem frameworks pesados nem dependência de internet externa, qualquer pessoa com um notebook e alguns celulares consegue iniciar a coleta em 30 segundos usando apenas um comando `npm start` ou executando o arquivo `iniciar.bat`."*
