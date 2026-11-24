import json

# Carregar dados da coleta real para embutir no simulador
with open("fila-ru-contador/dados/sessao_2026-11-04T20-25-18-492Z_azuq2/eventos.jsonl") as f:
    events = [json.loads(l) for l in f if l.strip()]

with open("fila-ru-contador/dados/sessao_2026-11-04T20-25-18-492Z_azuq2/metadados.json") as f:
    meta = json.load(f)

t0 = meta["inicioMs"]

chegadas_f1 = []
pessoas = {}

for e in events:
    p = e.get("pessoa")
    t = round((e["t"] - t0) / 1000.0, 1)
    tipo = e.get("tipo")
    fila = e.get("fila")
    if p not in pessoas:
        pessoas[p] = {"p": p}
    
    if tipo == "chegada" and fila == 1 and not e.get("anulada"):
        pessoas[p]["chegada_f1"] = t
        chegadas_f1.append(t)
    elif tipo == "atendimento" and fila == 1:
        pessoas[p]["atend_f1"] = t
    elif tipo == "atendimento" and fila == 2:
        pessoas[p]["atend_f2"] = t
    elif tipo == "atendimento" and fila == 3:
        pessoas[p]["atend_f3"] = t

chegadas_f1.sort()

# Serviços puros observados
servicos_f1 = []
servicos_f2 = []
tempos_mesas = []

ult_f1 = 0
for p in sorted(pessoas.values(), key=lambda x: x.get("atend_f1", 999999)):
    if "atend_f1" in p and "chegada_f1" in p:
        ini = max(p["chegada_f1"], ult_f1)
        dur = p["atend_f1"] - ini
        if 0 < dur <= 45:
            servicos_f1.append(round(dur, 1))
        ult_f1 = p["atend_f1"]

ult_f2 = 0
for p in sorted(pessoas.values(), key=lambda x: x.get("atend_f2", 999999)):
    if "atend_f2" in p and "atend_f1" in p:
        ini = max(p["atend_f1"], ult_f2)
        dur = p["atend_f2"] - ini
        if 0 < dur <= 60:
            servicos_f2.append(round(dur, 1))
        ult_f2 = p["atend_f2"]

for p in pessoas.values():
    if "atend_f3" in p and "atend_f2" in p:
        dur = p["atend_f3"] - p["atend_f2"]
        if 300 <= dur <= 3600:
            tempos_mesas.append(round(dur, 1))

json_chegadas = json.dumps(chegadas_f1)
json_serv_f1 = json.dumps(servicos_f1)
json_serv_f2 = json.dumps(servicos_f2)
json_mesas = json.dumps(tempos_mesas)

html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Simulador Interativo 2D & Gráficos — Filas do Restaurante Universitário</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>
    :root {{
      --navy: #16263A;
      --blue: #2663B4;
      --red: #DC2626;
      --green: #16A34A;
      --pink: #EC4899;
      --orange: #EA580C;
      --bg: #0F172A;
      --card-bg: #1E293B;
      --card-border: #334155;
      --text: #F8FAFC;
      --text-muted: #94A3B8;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
      background: var(--bg);
      color: var(--text);
      padding: 16px;
      line-height: 1.4;
      overflow-x: hidden;
    }}
    .top-bar {{
      background: var(--navy);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 16px 24px;
      margin-bottom: 16px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
    }}
    .brand h1 {{ font-size: 20px; font-weight: 700; color: #fff; display: flex; align-items: center; gap: 8px; }}
    .brand p {{ font-size: 12px; color: var(--text-muted); }}
    
    .preset-btn-group {{
      display: flex; gap: 8px; flex-wrap: wrap;
    }}
    .preset-btn {{
      background: #334155; border: 1px solid #475569; color: #fff;
      padding: 6px 12px; border-radius: 6px; font-size: 11px; font-weight: 600; cursor: pointer;
      transition: all 0.2s;
    }}
    .preset-btn:hover {{ background: var(--blue); border-color: var(--blue); }}
    .preset-btn.active {{ background: var(--blue); border-color: #60A5FA; }}

    .main-layout {{
      display: grid;
      grid-template-columns: 320px 1fr 340px;
      gap: 16px;
      height: calc(100vh - 110px);
      min-height: 720px;
    }}
    @media (max-width: 1400px) {{
      .main-layout {{ grid-template-columns: 300px 1fr; height: auto; }}
      .right-panel {{ grid-column: 1 / -1; }}
    }}
    @media (max-width: 900px) {{
      .main-layout {{ grid-template-columns: 1fr; }}
    }}

    .card {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 10px;
      padding: 16px;
      overflow-y: auto;
    }}

    /* Painel de Controles */
    .controls-panel h3 {{ font-size: 14px; text-transform: uppercase; letter-spacing: 0.5px; color: #60A5FA; margin-bottom: 12px; display: flex; align-items: center; gap: 6px; }}
    .param-group {{ margin-bottom: 14px; background: rgba(0,0,0,0.2); padding: 10px; border-radius: 8px; border-left: 3px solid var(--card-border); }}
    .param-group.f1 {{ border-left-color: var(--red); }}
    .param-group.f2 {{ border-left-color: var(--green); }}
    .param-group.mesas {{ border-left-color: var(--pink); }}
    
    .param-title {{ font-size: 12px; font-weight: 700; display: flex; justify-content: space-between; margin-bottom: 4px; }}
    .param-val {{ font-size: 12px; font-weight: 800; color: #38BDF8; }}
    .param-slider {{ width: 100%; height: 6px; border-radius: 3px; accent-color: #38BDF8; cursor: pointer; }}
    .param-sub {{ font-size: 10px; color: var(--text-muted); }}

    /* Canvas Central de Animação */
    .center-panel {{
      display: flex;
      flex-direction: column;
      gap: 12px;
    }}
    .playback-bar {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 10px;
      padding: 10px 16px;
      display: flex;
      align-items: center;
      gap: 12px;
      flex-wrap: wrap;
    }}
    .play-btn {{
      background: var(--blue); color: white; border: none; padding: 8px 18px; border-radius: 6px;
      font-size: 13px; font-weight: 700; cursor: pointer; display: flex; align-items: center; gap: 6px;
      transition: background 0.2s;
    }}
    .play-btn:hover {{ background: #1D4ED8; }}
    .play-btn.paused {{ background: #EA580C; }}
    .reset-btn {{
      background: #475569; color: white; border: none; padding: 8px 14px; border-radius: 6px;
      font-size: 13px; font-weight: 600; cursor: pointer;
    }}
    .reset-btn:hover {{ background: #64748B; }}

    .speed-selector {{
      display: flex; gap: 4px; align-items: center; margin-left: auto;
    }}
    .speed-btn {{
      background: #334155; border: 1px solid #475569; color: #fff; padding: 4px 8px; border-radius: 4px;
      font-size: 11px; font-weight: 700; cursor: pointer;
    }}
    .speed-btn.active {{ background: #2563EB; border-color: #60A5FA; }}

    .time-indicator {{
      font-family: monospace; font-size: 16px; font-weight: 800; color: #38BDF8; min-width: 90px;
    }}

    .canvas-container {{
      flex: 1;
      background: #090D16;
      border: 1px solid var(--card-border);
      border-radius: 10px;
      position: relative;
      overflow: hidden;
      min-height: 440px;
    }}
    canvas#simCanvas {{
      width: 100%;
      height: 100%;
      display: block;
    }}

    /* Alerta de Service Blocking */
    .blocking-banner {{
      position: absolute;
      top: 12px;
      left: 50%;
      transform: translateX(-50%);
      background: rgba(220, 38, 38, 0.9);
      border: 2px solid #FCA5A5;
      color: white;
      padding: 6px 18px;
      border-radius: 20px;
      font-size: 12px;
      font-weight: 800;
      display: none;
      align-items: center;
      gap: 8px;
      box-shadow: 0 4px 15px rgba(220, 38, 38, 0.5);
      animation: pulse 1s infinite;
      z-index: 10;
    }}
    @keyframes pulse {{
      0% {{ transform: translateX(-50%) scale(1); }}
      50% {{ transform: translateX(-50%) scale(1.04); }}
      100% {{ transform: translateX(-50%) scale(1); }}
    }}

    /* Painel da Direita (Gráficos e KPIs) */
    .right-panel {{
      display: flex;
      flex-direction: column;
      gap: 12px;
      overflow-y: auto;
    }}
    .kpi-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
    }}
    .kpi-mini {{
      background: rgba(0,0,0,0.3);
      padding: 8px;
      border-radius: 6px;
      border-left: 2px solid var(--blue);
    }}
    .kpi-mini.f1 {{ border-left-color: var(--red); }}
    .kpi-mini.f2 {{ border-left-color: var(--green); }}
    .kpi-mini.f3 {{ border-left-color: var(--pink); }}
    .kpi-mini-tit {{ font-size: 10px; text-transform: uppercase; color: var(--text-muted); }}
    .kpi-mini-val {{ font-size: 18px; font-weight: 800; color: #fff; }}
    .kpi-mini-sub {{ font-size: 9px; color: var(--text-muted); }}

    .chart-box {{
      background: rgba(0,0,0,0.3);
      border: 1px solid var(--card-border);
      border-radius: 8px;
      padding: 10px;
      height: 180px;
      position: relative;
    }}
    .chart-box h4 {{
      font-size: 11px; font-weight: 700; text-transform: uppercase; color: #94A3B8; margin-bottom: 6px;
    }}
    .chart-inner {{
      position: relative;
      height: 140px;
      width: 100%;
    }}

    .delta-good {{ color: #4ADE80; font-weight: 700; }}
    .delta-bad {{ color: #F87171; font-weight: 700; }}
  </style>
</head>
<body>

  <!-- BARRA SUPERIOR -->
  <div class="top-bar">
    <div class="brand">
      <h1>🍽️ Simulador de Filas do RU — Visualização 2D & Gráficos ao Vivo</h1>
      <p>Simulação guiada por traço histórico (Trace-Driven DES) • Coleta de Campo: 04/11/2026</p>
    </div>
    <div class="preset-btn-group">
      <button class="preset-btn active" onclick="carregarPreset('baseline')">📌 Baseline Real (1 Cat, 1 Buf)</button>
      <button class="preset-btn" onclick="carregarPreset('c1')">🚀 Cenário 1: 2 Catracas</button>
      <button class="preset-btn" onclick="carregarPreset('c2')">⭐ Cenário 2: 2 Cat + 2 Buf</button>
      <button class="preset-btn" onclick="carregarPreset('estresse')">🔥 Estresse (+50% Demanda)</button>
    </div>
  </div>

  <div class="main-layout">

    <!-- COLUNA ESQUERDA: PARÂMETROS / MÉTRICAS AJUSTÁVEIS -->
    <div class="card controls-panel">
      <h3>⚙️ Parâmetros do Sistema</h3>

      <!-- Demanda / Chegadas -->
      <div class="param-group">
        <div class="param-title">
          <span>Multiplicador de Demanda (λ)</span>
          <span class="param-val" id="val-demanda">1.0×</span>
        </div>
        <input type="range" class="param-slider" id="slider-demanda" min="0.5" max="2.0" step="0.1" value="1.0" oninput="atualizarParametros()">
        <div class="param-sub">Ajusta o volume de alunos que chegam ao RU</div>
      </div>

      <!-- Fila 1: Entrada / Catraca -->
      <div class="param-group f1">
        <div class="param-title">
          <span>Catracas na Entrada (c₁)</span>
          <span class="param-val" id="val-c1">1</span>
        </div>
        <input type="range" class="param-slider" id="slider-c1" min="1" max="4" step="1" value="1" oninput="atualizarParametros()">
        
        <div class="param-title" style="margin-top:8px;">
          <span>Velocidade da Catraca (μ₁)</span>
          <span class="param-val" id="val-vel-f1">0% (Normal)</span>
        </div>
        <input type="range" class="param-slider" id="slider-vel-f1" min="-50" max="100" step="10" value="0" oninput="atualizarParametros()">
        <div class="param-sub">+100% reduz pela metade o tempo do cartão</div>
      </div>

      <!-- Fila 2: Buffet / Serviço -->
      <div class="param-group f2">
        <div class="param-title">
          <span>Linhas de Buffet (c₂)</span>
          <span class="param-val" id="val-c2">1</span>
        </div>
        <input type="range" class="param-slider" id="slider-c2" min="1" max="3" step="1" value="1" oninput="atualizarParametros()">

        <div class="param-title" style="margin-top:8px;">
          <span>Velocidade do Buffet (μ₂)</span>
          <span class="param-val" id="val-vel-f2">0% (Normal)</span>
        </div>
        <input type="range" class="param-slider" id="slider-vel-f2" min="-50" max="100" step="10" value="0" oninput="atualizarParametros()">
        <div class="param-sub">Agilidade na montagem e entrega dos pratos</div>
      </div>

      <!-- Salão de Mesas -->
      <div class="param-group mesas">
        <div class="param-title">
          <span>Capacidade do Salão (K)</span>
          <span class="param-val" id="val-mesas">216 cadeiras</span>
        </div>
        <input type="range" class="param-slider" id="slider-mesas" min="60" max="300" step="12" value="216" oninput="atualizarParametros()">

        <div class="param-title" style="margin-top:8px;">
          <span>Tempo de Refeição</span>
          <span class="param-val" id="val-refeicao">0 min (22 min)</span>
        </div>
        <input type="range" class="param-slider" id="slider-refeicao" min="-10" max="15" step="1" value="0" oninput="atualizarParametros()">
        <div class="param-sub">Variação no tempo que os alunos sentam à mesa</div>
      </div>

      <div style="font-size:11px; color:#94A3B8; margin-top:10px; line-height:1.3;">
        💡 <em>Dica:</em> Mude os controles e observe o reflexo imediato no fluxo de blocos 2D e nos gráficos à direita.
      </div>
    </div>

    <!-- COLUNA CENTRAL: CANVAS 2D E REPRODUTOR -->
    <div class="center-panel">
      <!-- Barra de Controle -->
      <div class="playback-bar">
        <button class="play-btn" id="btn-play" onclick="togglePlay()">
          <span id="play-icon">▶</span> <span id="play-text">Iniciar</span>
        </button>
        <button class="reset-btn" onclick="reiniciarSimulacao()">⏮ Reiniciar</button>

        <span class="time-indicator" id="clock-display">00:00:00</span>

        <input type="range" id="time-scrubber" min="0" max="3920" value="0" style="flex:1; accent-color:#38BDF8;" oninput="onScrub(this.value)">

        <div class="speed-selector">
          <button class="speed-btn active" onclick="setVelocidade(1, this)">1×</button>
          <button class="speed-btn" onclick="setVelocidade(5, this)">5×</button>
          <button class="speed-btn" onclick="setVelocidade(15, this)">15×</button>
          <button class="speed-btn" onclick="setVelocidade(60, this)">60×</button>
        </div>
      </div>

      <!-- Container do Canvas -->
      <div class="canvas-container" id="canvasContainer">
        <div class="blocking-banner" id="blockingBanner">
          ⚠️ SERVICE BLOCKING: MESAS LOTADAS! ALUNOS RETIDOS EM PÉ!
        </div>
        <canvas id="simCanvas"></canvas>
      </div>
    </div>

    <!-- COLUNA DIREITA: KPIs E GRÁFICOS EM TEMPO REAL -->
    <div class="card right-panel">
      <!-- Mini KPIs ao Vivo -->
      <div class="kpi-grid">
        <div class="kpi-mini f1">
          <div class="kpi-mini-tit">Fila Externa (F1)</div>
          <div class="kpi-mini-val" id="kpi-f1-now">0</div>
          <div class="kpi-mini-sub">Pico: <span id="kpi-f1-pico">0</span> alunos</div>
        </div>
        <div class="kpi-mini f2">
          <div class="kpi-mini-tit">Fila Buffet (F2)</div>
          <div class="kpi-mini-val" id="kpi-f2-now">0</div>
          <div class="kpi-mini-sub">Pico: <span id="kpi-f2-pico">0</span> alunos</div>
        </div>
        <div class="kpi-mini f3">
          <div class="kpi-mini-tit">Salão de Mesas</div>
          <div class="kpi-mini-val" id="kpi-mesas-now">0</div>
          <div class="kpi-mini-sub">Lotação: <span id="kpi-mesas-pct">0%</span></div>
        </div>
        <div class="kpi-mini">
          <div class="kpi-mini-tit">Total Atendidos</div>
          <div class="kpi-mini-val" id="kpi-atendidos-total">0</div>
          <div class="kpi-mini-sub">de 192 alunos</div>
        </div>
      </div>

      <!-- Card Desempenho / Deltas -->
      <div style="background:rgba(0,0,0,0.3); padding:10px; border-radius:6px; font-size:11px;">
        <div style="font-weight:700; color:#94A3B8; margin-bottom:4px; text-transform:uppercase;">Tempo Médio de Espera (vs. Real)</div>
        <div style="display:flex; justify-content:space-between; margin-bottom:3px;">
          <span>Espera F1 (Entrada):</span>
          <span id="delta-wq1" style="font-weight:700;">131,5 s</span>
        </div>
        <div style="display:flex; justify-content:space-between; margin-bottom:3px;">
          <span>Espera F2 (Buffet):</span>
          <span id="delta-wq2" style="font-weight:700;">142,1 s</span>
        </div>
        <div style="display:flex; justify-content:space-between;">
          <span>Trânsito até a Mesa:</span>
          <span id="delta-transito" style="font-weight:700; color:#38BDF8;">~5,0 min</span>
        </div>
      </div>

      <!-- Gráfico 1: Tamanho das Filas -->
      <div class="chart-box">
        <h4>Filas F1 e F2 no Tempo (Pessoas)</h4>
        <div class="chart-inner">
          <canvas id="chartFilas"></canvas>
        </div>
      </div>

      <!-- Gráfico 2: Ocupação das Mesas -->
      <div class="chart-box">
        <h4>Ocupação do Salão vs. Limite K</h4>
        <div class="chart-inner">
          <canvas id="chartMesas"></canvas>
        </div>
      </div>
    </div>

  </div>

  <script>
    // DADOS HISTÓRICOS EMBUTIDOS (04/11/2026)
    const DADOS_REAIS = {{
      chegadasF1: {json_chegadas},
      servicosF1: {json_serv_f1},
      servicosF2: {json_serv_f2},
      temposMesas: {json_mesas}
    }};

    // ESTADO DA SIMULAÇÃO
    const SimState = {{
      rodando: false,
      tempoAtual: 0,        // em segundos simulados (0 a 3920)
      velocidade: 5,        // multiplicador de velocidade (1x, 5x, 15x, 60x)
      ultimoFrameTimestamp: 0,
      
      // Parâmetros configuráveis
      demandaMult: 1.0,
      c1: 1,
      fatorVelF1: 0,
      c2: 1,
      fatorVelF2: 0,
      capacidadeMesas: 216,
      deltaRefeicaoMin: 0,

      // Entidades simuladas geradas a partir dos parâmetros
      alunos: [],           // lista de alunos simulados com timestamps
      fila1Espera: [],      // IDs dos alunos na fila 1
      catracasOcupadas: [], // estado de cada catraca
      fila2Espera: [],      // IDs dos alunos na fila 2
      buffetsOcupados: [],  // estado de cada buffet
      mesasOcupadas: [],    // IDs nas mesas
      alunosBloqueados: [], // alunos segurando bandeja esperando mesa
      saidasRU: [],

      // Séries históricas para gráficos (amostradas a cada 30 segundos)
      historicoTempo: [],
      historicoFila1: [],
      historicoFila2: [],
      historicoMesas: [],

      picoF1: 0,
      picoF2: 0,
      picoMesas: 0
    }};

    // Inicialização do Canvas
    const canvas = document.getElementById('simCanvas');
    const ctx = canvas.getContext('2d');
    let width = 800, height = 500;

    function resizeCanvas() {{
      const container = document.getElementById('canvasContainer');
      width = container.clientWidth;
      height = container.clientHeight;
      canvas.width = width;
      canvas.height = height;
    }}
    window.addEventListener('resize', resizeCanvas);
    resizeCanvas();

    // Setup dos Gráficos Chart.js
    let chartFilasInstance = null;
    let chartMesasInstance = null;

    function initCharts() {{
      const ctxFilas = document.getElementById('chartFilas').getContext('2d');
      chartFilasInstance = new Chart(ctxFilas, {{
        type: 'line',
        data: {{
          labels: [],
          datasets: [
            {{ label: 'F1 Entrada', data: [], borderColor: '#EF4444', borderWidth: 2, pointRadius: 0, tension: 0.2 }},
            {{ label: 'F2 Buffet', data: [], borderColor: '#22C55E', borderWidth: 2, pointRadius: 0, tension: 0.2 }}
          ]
        }},
        options: {{
          responsive: true, maintainAspectRatio: false,
          animation: false,
          scales: {{
            x: {{ display: true, ticks: {{ color: '#64748B', font: {{ size: 9 }}, maxTicksLimit: 6 }} }},
            y: {{ beginAtZero: true, max: 55, ticks: {{ color: '#64748B', font: {{ size: 9 }} }} }}
          }},
          plugins: {{ legend: {{ labels: {{ color: '#94A3B8', boxWidth: 10, font: {{ size: 9 }} }} }} }}
        }}
      }});

      const ctxMesas = document.getElementById('chartMesas').getContext('2d');
      chartMesasInstance = new Chart(ctxMesas, {{
        type: 'line',
        data: {{
          labels: [],
          datasets: [
            {{ label: 'Mesas Ocupadas', data: [], borderColor: '#EC4899', backgroundColor: 'rgba(236, 72, 153, 0.2)', fill: true, borderWidth: 2, pointRadius: 0, tension: 0.2 }},
            {{ label: 'Capacidade K', data: [], borderColor: '#DC2626', borderDash: [4, 4], borderWidth: 1.5, pointRadius: 0 }}
          ]
        }},
        options: {{
          responsive: true, maintainAspectRatio: false,
          animation: false,
          scales: {{
            x: {{ display: true, ticks: {{ color: '#64748B', font: {{ size: 9 }}, maxTicksLimit: 6 }} }},
            y: {{ beginAtZero: true, max: 240, ticks: {{ color: '#64748B', font: {{ size: 9 }} }} }}
          }},
          plugins: {{ legend: {{ labels: {{ color: '#94A3B8', boxWidth: 10, font: {{ size: 9 }} }} }} }}
        }}
      }});
    }}
    initCharts();

    // PREPARAÇÃO DO MODELO DE SIMULAÇÃO
    function reconstruirEventosSimulacao() {{
      const multTempoF1 = 1 / (1 + (SimState.fatorVelF1 / 100));
      const multTempoF2 = 1 / (1 + (SimState.fatorVelF2 / 100));
      const deltaMesasSeg = SimState.deltaRefeicaoMin * 60;

      // Gerar alunos a partir do traço real ajustado
      SimState.alunos = [];
      const totalAlunos = Math.round(DADOS_REAIS.chegadasF1.length * SimState.demandaMult);

      for (let i = 0; i < totalAlunos; i++) {{
        const baseIdx = Math.min(DADOS_REAIS.chegadasF1.length - 1, Math.floor(i / SimState.demandaMult));
        const tCheg = DADOS_REAIS.chegadasF1[baseIdx] * (i < DADOS_REAIS.chegadasF1.length ? 1.0 : (1.0 + (i % 3) * 0.05));
        
        const durServ1 = (DADOS_REAIS.servicosF1[i % DADOS_REAIS.servicosF1.length] || 6.0) * multTempoF1;
        const durServ2 = (DADOS_REAIS.servicosF2[i % DADOS_REAIS.servicosF2.length] || 11.0) * multTempoF2;
        const durMesas = Math.max(300, (DADOS_REAIS.temposMesas[i % DADOS_REAIS.temposMesas.length] || 1300) + deltaMesasSeg);

        SimState.alunos.push({{
          id: i + 1,
          tChegada: tCheg,
          durServ1: Math.max(1.5, durServ1),
          durServ2: Math.max(2.5, durServ2),
          durMesas: durMesas,
          
          // Marcos temporais simulados
          tIniCatraca: null,
          tFimCatraca: null,
          tIniBuffet: null,
          tFimBuffet: null,
          tEntrouMesa: null,
          tSaiuMesa: null,
          
          // Posições visuais para interpolação
          x: 0, y: 0, estadoVisual: 'espera1'
        }});
      }}

      // Pré-simulação determinística de eventos para garantir timeline 100% contínua
      resolverTimelineDiscreta();
    }}

    function resolverTimelineDiscreta() {{
      // Fila única compartilhada para c1 catracas
      const catracasLivreEm = Array(SimState.c1).fill(0);
      const buffetsLivreEm = Array(SimState.c2).fill(0);
      const mesasLiberacao = []; // lista de instantes de liberação de mesas

      for (const al of SimState.alunos) {{
        // 1. Catraca
        // Escolhe o primeiro servidor livre
        let melhorCatraca = 0;
        for (let c = 1; c < SimState.c1; c++) {{
          if (catracasLivreEm[c] < catracasLivreEm[melhorCatraca]) melhorCatraca = c;
        }}
        al.tIniCatraca = Math.max(al.tChegada, catracasLivreEm[melhorCatraca]);
        al.tFimCatraca = al.tIniCatraca + al.durServ1;
        catracasLivreEm[melhorCatraca] = al.tFimCatraca;

        // 2. Buffet (Fila 2)
        let melhorBuffet = 0;
        for (let b = 1; b < SimState.c2; b++) {{
          if (buffetsLivreEm[b] < buffetsLivreEm[melhorBuffet]) melhorBuffet = b;
        }}
        al.tIniBuffet = Math.max(al.tFimCatraca, buffetsLivreEm[melhorBuffet]);
        al.tFimBuffet = al.tIniBuffet + al.durServ2;
        buffetsLivreEm[melhorBuffet] = al.tFimBuffet;

        // 3. Mesas e Bloqueio (Service Blocking)
        let tMesaLivre = al.tFimBuffet;
        if (mesasLiberacao.length >= SimState.capacidadeMesas) {{
          mesasLiberacao.sort((a, b) => a - b);
          // O mais antigo a liberar mesa
          const maisAntigo = mesasLiberacao[0];
          if (maisAntigo > tMesaLivre) {{
            // Bloqueio! Teve que esperar em pé
            tMesaLivre = maisAntigo;
          }}
          mesasLiberacao.shift(); // remove a cadeira que desocupou
        }}

        al.tEntrouMesa = tMesaLivre;
        al.tSaiuMesa = al.tEntrouMesa + al.durMesas;
        mesasLiberacao.push(al.tSaiuMesa);
      }}

      // Calcular médias simuladas
      let somaEsperaF1 = 0, somaEsperaF2 = 0, countAtend = 0;
      for (const al of SimState.alunos) {{
        if (al.tIniCatraca !== null) {{
          somaEsperaF1 += (al.tIniCatraca - al.tChegada);
          somaEsperaF2 += (al.tIniBuffet - al.tFimCatraca);
          countAtend++;
        }}
      }}
      const mediaWq1 = countAtend > 0 ? (somaEsperaF1 / countAtend) : 0;
      const mediaWq2 = countAtend > 0 ? (somaEsperaF2 / countAtend) : 0;
      const transitoTotal = mediaWq1 + mediaWq2;

      document.getElementById('delta-wq1').textContent = mediaWq1.toFixed(1) + ' s';
      document.getElementById('delta-wq1').className = mediaWq1 < 125 ? 'delta-good' : (mediaWq1 > 140 ? 'delta-bad' : '');

      document.getElementById('delta-wq2').textContent = mediaWq2.toFixed(1) + ' s';
      document.getElementById('delta-wq2').className = mediaWq2 < 135 ? 'delta-good' : (mediaWq2 > 155 ? 'delta-bad' : '');

      document.getElementById('delta-transito').textContent = (transitoTotal / 60).toFixed(1) + ' min';
      document.getElementById('delta-transito').className = transitoTotal < 250 ? 'delta-good' : (transitoTotal > 320 ? 'delta-bad' : '');
    }}

    // REINICIALIZAR / RESET
    function reiniciarSimulacao() {{
      SimState.tempoAtual = 0;
      SimState.picoF1 = 0;
      SimState.picoF2 = 0;
      SimState.picoMesas = 0;
      SimState.historicoTempo = [];
      SimState.historicoFila1 = [];
      SimState.historicoFila2 = [];
      SimState.historicoMesas = [];
      document.getElementById('time-scrubber').value = 0;
      reconstruirEventosSimulacao();
      atualizarInterface();
    }}

    function togglePlay() {{
      SimState.rodando = !SimState.rodando;
      const btn = document.getElementById('btn-play');
      const icon = document.getElementById('play-icon');
      const text = document.getElementById('play-text');

      if (SimState.rodando) {{
        btn.classList.add('paused');
        icon.textContent = '⏸';
        text.textContent = 'Pausar';
        SimState.ultimoFrameTimestamp = performance.now();
        requestAnimationFrame(animarLoop);
      }} else {{
        btn.classList.remove('paused');
        icon.textContent = '▶';
        text.textContent = 'Continuar';
      }}
    }}

    function setVelocidade(v, el) {{
      SimState.velocidade = v;
      document.querySelectorAll('.speed-btn').forEach(b => b.classList.remove('active'));
      el.classList.add('active');
    }}

    function onScrub(val) {{
      SimState.tempoAtual = parseFloat(val);
      atualizarInterface();
    }}

    function carregarPreset(tipo) {{
      document.querySelectorAll('.preset-btn').forEach(b => b.classList.remove('active'));
      event.target.classList.add('active');

      if (tipo === 'baseline') {{
        document.getElementById('slider-demanda').value = 1.0;
        document.getElementById('slider-c1').value = 1;
        document.getElementById('slider-vel-f1').value = 0;
        document.getElementById('slider-c2').value = 1;
        document.getElementById('slider-vel-f2').value = 0;
        document.getElementById('slider-mesas').value = 216;
        document.getElementById('slider-refeicao').value = 0;
      }} else if (tipo === 'c1') {{
        // Cenário 1: 2 Catracas e 1 Buffet
        document.getElementById('slider-demanda').value = 1.0;
        document.getElementById('slider-c1').value = 2;
        document.getElementById('slider-vel-f1').value = 0;
        document.getElementById('slider-c2').value = 1;
        document.getElementById('slider-vel-f2').value = 0;
        document.getElementById('slider-mesas').value = 216;
        document.getElementById('slider-refeicao').value = 0;
      }} else if (tipo === 'c2') {{
        // Cenário 2: 2 Catracas + 2 Buffets
        document.getElementById('slider-demanda').value = 1.0;
        document.getElementById('slider-c1').value = 2;
        document.getElementById('slider-vel-f1').value = 0;
        document.getElementById('slider-c2').value = 2;
        document.getElementById('slider-vel-f2').value = 0;
        document.getElementById('slider-mesas').value = 216;
        document.getElementById('slider-refeicao').value = 0;
      }} else if (tipo === 'estresse') {{
        document.getElementById('slider-demanda').value = 1.5;
        document.getElementById('slider-c1').value = 1;
        document.getElementById('slider-vel-f1').value = -20;
        document.getElementById('slider-c2').value = 1;
        document.getElementById('slider-vel-f2').value = 0;
        document.getElementById('slider-mesas').value = 180;
        document.getElementById('slider-refeicao').value = 4;
      }}
      atualizarParametros();
      reiniciarSimulacao();
    }}

    function atualizarParametros() {{
      SimState.demandaMult = parseFloat(document.getElementById('slider-demanda').value);
      SimState.c1 = parseInt(document.getElementById('slider-c1').value);
      SimState.fatorVelF1 = parseInt(document.getElementById('slider-vel-f1').value);
      SimState.c2 = parseInt(document.getElementById('slider-c2').value);
      SimState.fatorVelF2 = parseInt(document.getElementById('slider-vel-f2').value);
      SimState.capacidadeMesas = parseInt(document.getElementById('slider-mesas').value);
      SimState.deltaRefeicaoMin = parseInt(document.getElementById('slider-refeicao').value);

      document.getElementById('val-demanda').textContent = SimState.demandaMult.toFixed(1) + '×';
      document.getElementById('val-c1').textContent = SimState.c1;
      document.getElementById('val-vel-f1').textContent = (SimState.fatorVelF1 > 0 ? '+' : '') + SimState.fatorVelF1 + '%';
      document.getElementById('val-c2').textContent = SimState.c2;
      document.getElementById('val-vel-f2').textContent = (SimState.fatorVelF2 > 0 ? '+' : '') + SimState.fatorVelF2 + '%';
      document.getElementById('val-mesas').textContent = SimState.capacidadeMesas + ' cadeiras';
      document.getElementById('val-refeicao').textContent = (SimState.deltaRefeicaoMin > 0 ? '+' : '') + SimState.deltaRefeicaoMin + ' min (' + (22 + SimState.deltaRefeicaoMin) + ' min)';

      reconstruirEventosSimulacao();
      atualizarInterface();
    }}

    // LOOP DE ANIMAÇÃO A 60 FPS
    function animarLoop(timestamp) {{
      if (!SimState.rodando) return;

      const deltaMs = timestamp - SimState.ultimoFrameTimestamp;
      SimState.ultimoFrameTimestamp = timestamp;

      // Avança o relógio da simulação proporcional à velocidade
      const deltaSegSimulado = (deltaMs / 1000.0) * SimState.velocidade;
      SimState.tempoAtual += deltaSegSimulado;

      if (SimState.tempoAtual >= 3920) {{
        SimState.tempoAtual = 3920;
        togglePlay();
      }}

      document.getElementById('time-scrubber').value = SimState.tempoAtual;

      atualizarInterface();
      renderizarCanvas();

      if (SimState.rodando) {{
        requestAnimationFrame(animarLoop);
      }}
    }}

    // ATUALIZAÇÃO DA INTERFACE, KPIS E GRÁFICOS
    function atualizarInterface() {{
      const t = SimState.tempoAtual;

      // Formatar relógio hh:mm:ss
      const h = Math.floor(t / 3600);
      const m = Math.floor((t % 3600) / 60);
      const s = Math.floor(t % 60);
      document.getElementById('clock-display').textContent = 
        String(h).padStart(2, '0') + ':' + String(m).padStart(2, '0') + ':' + String(s).padStart(2, '0');

      // Filtrar estado instantâneo das filas no tempo t
      let f1Count = 0;
      let f2Count = 0;
      let mesasCount = 0;
      let bloqueadosCount = 0;
      let atendidosCount = 0;

      for (const al of SimState.alunos) {{
        if (al.tChegada <= t) {{
          if (al.tIniCatraca === null || al.tIniCatraca > t) {{
            f1Count++;
          }} else if (al.tFimCatraca <= t) {{
            atendidosCount++;
            if (al.tIniBuffet === null || al.tIniBuffet > t) {{
              f2Count++;
            }} else if (al.tFimBuffet <= t) {{
              if (al.tEntrouMesa > t) {{
                // Bloqueado segurando bandeja!
                bloqueadosCount++;
              }} else if (al.tSaiuMesa > t) {{
                mesasCount++;
              }}
            }}
          }}
        }}
      }}

      // Alerta visual de blocking
      const banner = document.getElementById('blockingBanner');
      if (bloqueadosCount > 0) {{
        banner.style.display = 'flex';
        banner.textContent = `⚠️ SERVICE BLOCKING: ${{bloqueadosCount}} ALUNO(S) EM PÉ SEGURANDO BANDEJA!`;
      }} else {{
        banner.style.display = 'none';
      }}

      // Picos
      SimState.picoF1 = Math.max(SimState.picoF1, f1Count);
      SimState.picoF2 = Math.max(SimState.picoF2, f2Count);
      SimState.picoMesas = Math.max(SimState.picoMesas, mesasCount);

      document.getElementById('kpi-f1-now').textContent = f1Count;
      document.getElementById('kpi-f1-pico').textContent = SimState.picoF1;
      document.getElementById('kpi-f2-now').textContent = f2Count;
      document.getElementById('kpi-f2-pico').textContent = SimState.picoF2;
      document.getElementById('kpi-mesas-now').textContent = mesasCount;
      document.getElementById('kpi-mesas-pct').textContent = Math.round((mesasCount / SimState.capacidadeMesas) * 100) + '%';
      document.getElementById('kpi-atendidos-total').textContent = atendidosCount;

      // Amostragem nos Gráficos (a cada 30 segundos)
      const minutoAtual = Math.floor(t / 60);
      if (SimState.historicoTempo.length === 0 || t - SimState.historicoTempo[SimState.historicoTempo.length - 1] >= 25) {{
        SimState.historicoTempo.push(t);
        const rotuloMin = (t / 60).toFixed(0) + 'm';
        
        chartFilasInstance.data.labels.push(rotuloMin);
        chartFilasInstance.data.datasets[0].data.push(f1Count);
        chartFilasInstance.data.datasets[1].data.push(f2Count);
        chartFilasInstance.update('none');

        chartMesasInstance.data.labels.push(rotuloMin);
        chartMesasInstance.data.datasets[0].data.push(mesasCount);
        chartMesasInstance.data.datasets[1].data.push(SimState.capacidadeMesas);
        chartMesasInstance.update('none');
      }}
    }}

    // RENDERIZADOR 2D NO CANVAS
    function renderizarCanvas() {{
      const t = SimState.tempoAtual;
      ctx.clearRect(0, 0, width, height);

      // Fundo e Layout Arquitetural do RU
      // Escala e centralização
      const escalaX = width / 840;
      const escalaY = height / 520;
      const s = Math.min(escalaX, escalaY);

      ctx.save();
      ctx.scale(s, s);

      // 1. ZONAS FÍSICAS (Caixas)
      // Calçada / Entrada (Fila 1)
      ctx.fillStyle = 'rgba(220, 38, 38, 0.08)';
      ctx.strokeStyle = '#DC2626';
      ctx.lineWidth = 2;
      ctx.fillRect(620, 30, 180, 220);
      ctx.strokeRect(620, 30, 180, 220);
      ctx.fillStyle = '#F87171';
      ctx.font = 'bold 12px sans-serif';
      ctx.fillText('ZONA 1: CALÇADA / ENTRADA', 630, 50);

      // Catracas
      const wCat = 70;
      const hCat = 50;
      const yCat = 180;
      for (let c = 0; c < SimState.c1; c++) {{
        const xC = 520 - c * 25;
        const yC = yCat + c * 28;
        ctx.fillStyle = '#1E293B';
        ctx.strokeStyle = '#38BDF8';
        ctx.lineWidth = 2;
        ctx.fillRect(xC, yC, wCat, hCat);
        ctx.strokeRect(xC, yC, wCat, hCat);
        ctx.fillStyle = '#38BDF8';
        ctx.font = 'bold 10px sans-serif';
        ctx.fillText(`CATRACA ${{c+1}}`, xC + 6, yC + 20);
      }}

      // Corredor do Buffet (Fila 2)
      ctx.fillStyle = 'rgba(22, 163, 74, 0.08)';
      ctx.strokeStyle = '#16A34A';
      ctx.lineWidth = 2;
      ctx.fillRect(320, 160, 160, 260);
      ctx.strokeRect(320, 160, 160, 260);
      ctx.fillStyle = '#4ADE80';
      ctx.font = 'bold 12px sans-serif';
      ctx.fillText('ZONA 2: BUFFET / SERVIÇO', 330, 180);

      // Balcões térmicos
      for (let b = 0; b < SimState.c2; b++) {{
        const xB = 340 + b * 50;
        ctx.fillStyle = '#334155';
        ctx.strokeStyle = '#16A34A';
        ctx.fillRect(xB, 220, 38, 160);
        ctx.strokeRect(xB, 220, 38, 160);
        ctx.fillStyle = '#86EFAC';
        ctx.font = '9px sans-serif';
        ctx.fillText(`BUFFET ${{b+1}}`, xB + 2, 240);
      }}

      // Salão de Mesas (Zona 3)
      ctx.fillStyle = 'rgba(236, 72, 153, 0.08)';
      ctx.strokeStyle = '#EC4899';
      ctx.lineWidth = 2;
      ctx.fillRect(40, 40, 250, 440);
      ctx.strokeRect(40, 40, 250, 440);
      ctx.fillStyle = '#F472B6';
      ctx.font = 'bold 12px sans-serif';
      ctx.fillText(`SALÃO DE MESAS (K = ${{SimState.capacidadeMesas}})`, 50, 60);

      // Desenhar grade de 36 mesas (4 fileiras de 9 mesas)
      const mesasOcupadasCount = SimState.alunos.filter(al => al.tEntrouMesa <= t && al.tSaiuMesa > t).length;
      let mesasPreenchidas = 0;

      for (let fil = 0; fil < 4; fil++) {{
        for (let col = 0; col < 9; col++) {{
          const mx = 60 + fil * 56;
          const my = 85 + col * 42;
          const idxMesa = fil * 9 + col;
          const lugaresMesaOcupados = Math.max(0, Math.min(6, mesasOcupadasCount - idxMesa * 6));

          ctx.fillStyle = lugaresMesaOcupados > 0 ? 'rgba(236, 72, 153, 0.35)' : '#1E293B';
          ctx.strokeStyle = lugaresMesaOcupados === 6 ? '#EC4899' : '#475569';
          ctx.lineWidth = 1;
          ctx.fillRect(mx, my, 40, 24);
          ctx.strokeRect(mx, my, 40, 24);

          // Cadeirinhas
          ctx.fillStyle = lugaresMesaOcupados > 0 ? '#F472B6' : '#64748B';
          ctx.font = '8px sans-serif';
          ctx.fillText(`${{lugaresMesaOcupados}}/6`, mx + 12, my + 15);
        }}
      }}

      // Porta de Saída
      ctx.fillStyle = '#1E293B';
      ctx.strokeStyle = '#A855F7';
      ctx.lineWidth = 2;
      ctx.fillRect(50, 490, 80, 20);
      ctx.strokeRect(50, 490, 80, 20);
      ctx.fillStyle = '#C084FC';
      ctx.font = 'bold 10px sans-serif';
      ctx.fillText('SAÍDA RU ➔', 58, 504);

      // 2. RENDERIZAÇÃO DOS ESTUDANTES (BLOCO / CÍRCULOS DINÂMICOS)
      let f1Index = 0;
      let f2Index = 0;
      let blockIndex = 0;

      for (const al of SimState.alunos) {{
        if (al.tChegada <= t) {{
          // A. Fila 1 (Na calçada esperando catraca)
          if (al.tIniCatraca === null || al.tIniCatraca > t) {{
            const posX = 740 - (f1Index % 5) * 22;
            const posY = 70 + Math.floor(f1Index / 5) * 20;
            f1Index++;

            ctx.fillStyle = '#EF4444';
            ctx.beginPath();
            ctx.arc(posX, posY, 7, 0, Math.PI * 2);
            ctx.fill();
            ctx.strokeStyle = '#FFFFFF';
            ctx.lineWidth = 1;
            ctx.stroke();
          }}
          // B. Na Catraca sendo atendido
          else if (al.tFimCatraca > t) {{
            const frac = (t - al.tIniCatraca) / (al.tFimCatraca - al.tIniCatraca);
            const posX = 560 - frac * 30;
            const posY = 195;

            ctx.fillStyle = '#F59E0B'; // Amarelo (processando)
            ctx.beginPath();
            ctx.arc(posX, posY, 9, 0, Math.PI * 2);
            ctx.fill();
            ctx.strokeStyle = '#fff';
            ctx.stroke();
          }}
          // C. Fila 2 (No corredor do Buffet esperando prato)
          else if (al.tIniBuffet === null || al.tIniBuffet > t) {{
            const posX = 440 - (f2Index % 4) * 22;
            const posY = 200 + Math.floor(f2Index / 4) * 20;
            f2Index++;

            ctx.fillStyle = '#22C55E';
            ctx.beginPath();
            ctx.arc(posX, posY, 7, 0, Math.PI * 2);
            ctx.fill();
            ctx.strokeStyle = '#FFFFFF';
            ctx.lineWidth = 1;
            ctx.stroke();
          }}
          // D. No Buffet pegando comida
          else if (al.tFimBuffet > t) {{
            const frac = (t - al.tIniBuffet) / (al.tFimBuffet - al.tIniBuffet);
            const posX = 360;
            const posY = 230 + frac * 120;

            ctx.fillStyle = '#10B981';
            ctx.beginPath();
            ctx.arc(posX, posY, 9, 0, Math.PI * 2);
            ctx.fill();
            ctx.strokeStyle = '#fff';
            ctx.stroke();
          }}
          // E. Aluno bloqueado segurando bandeja (Service Blocking)
          else if (al.tEntrouMesa > t) {{
            const posX = 310 - (blockIndex % 2) * 18;
            const posY = 320 + Math.floor(blockIndex / 2) * 18;
            blockIndex++;

            ctx.fillStyle = '#EF4444';
            ctx.beginPath();
            ctx.arc(posX, posY, 8, 0, Math.PI * 2);
            ctx.fill();
            // Desenhar mini bandeja
            ctx.fillStyle = '#FCD34D';
            ctx.fillRect(posX - 5, posY + 4, 10, 3);
          }}
          // F. Nas Mesas comendo
          else if (al.tSaiuMesa > t) {{
            // Já desenhado nas mesinhas do salão!
          }}
          // G. Saindo do RU
          else if (t - al.tSaiuMesa <= 4) {{
            const frac = (t - al.tSaiuMesa) / 4;
            const posX = 90 - frac * 30;
            const posY = 500;

            ctx.fillStyle = '#A855F7';
            ctx.beginPath();
            ctx.arc(posX, posY, 6, 0, Math.PI * 2);
            ctx.fill();
          }}
        }}
      }}

      ctx.restore();
    }}

    // Iniciar na carga
    reconstruirEventosSimulacao();
    atualizarInterface();
    renderizarCanvas();
  </script>
</body>
</html>
"""

with open("/home/luizcaripuna/Documentos/AVALIAÇÃO DE DESEMPENHO/projeto-ru/divisao-trabalho/simulador_ru_interativo.html", "w", encoding="utf-8") as f:
    f.write(html_content)

# Copiar também para a pasta public do projeto
with open("/home/luizcaripuna/Documentos/AVALIAÇÃO DE DESEMPENHO/projeto-ru/fila-ru-contador/public/simulador_ru_interativo.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("Simulador gerado com sucesso em:")
print("1. divisao-trabalho/simulador_ru_interativo.html")
print("2. fila-ru-contador/public/simulador_ru_interativo.html")
