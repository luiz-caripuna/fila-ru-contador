import json
import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

# Diretório de saída
GRAFICOS_DIR = '/home/luizcaripuna/Documentos/AVALIAÇÃO DE DESEMPENHO/projeto-ru/divisao-trabalho/graficos'
os.makedirs(GRAFICOS_DIR, exist_ok=True)

# 1. Carregar dados reais da coleta
EVENTOS_PATH = '/home/luizcaripuna/Documentos/AVALIAÇÃO DE DESEMPENHO/projeto-ru/fila-ru-contador/dados/sessao_2026-11-04T20-25-18-492Z_azuq2/eventos.jsonl'
METADADOS_PATH = '/home/luizcaripuna/Documentos/AVALIAÇÃO DE DESEMPENHO/projeto-ru/fila-ru-contador/dados/sessao_2026-11-04T20-25-18-492Z_azuq2/metadados.json'

with open(EVENTOS_PATH, 'r', encoding='utf-8') as f:
    eventos = [json.loads(line) for line in f if line.strip()]

with open(METADADOS_PATH, 'r', encoding='utf-8') as f:
    meta = json.load(f)

t_inicio = meta['inicioMs']
t_fim = meta['fimMs']
dur_min = (t_fim - t_inicio) / 60000.0

# 2. Segmentação em blocos de 5 minutos
n_blocos = int(np.ceil(dur_min / 5.0))
rotulos_blocos = [f'{i*5}–{(i+1)*5}m' for i in range(n_blocos)]

chegadas_f1 = [0] * n_blocos
saidas_f1 = [0] * n_blocos
chegadas_f2 = [0] * n_blocos
saidas_f2 = [0] * n_blocos
chegadas_f3 = [0] * n_blocos
saidas_f3 = [0] * n_blocos

# Timeline de ocupação de mesas
mesas_timeline = [(0.0, 0)]
cur_mesas = 0

for ev in eventos:
    t_ev = ev.get('t', t_inicio)
    delta_s = max(0, int((t_ev - t_inicio) / 1000.0))
    b_idx = min(n_blocos - 1, int(delta_s / 300)) # 300s = 5min
    t_rel_min = (t_ev - t_inicio) / 60000.0
    
    tipo = ev.get('tipo')
    fila = ev.get('fila')
    
    if tipo == 'chegada' and fila == 1 and not ev.get('anulada'):
        chegadas_f1[b_idx] += 1
    elif tipo == 'atendimento' and fila == 1:
        saidas_f1[b_idx] += 1
    elif tipo == 'chegada' and fila == 2:
        chegadas_f2[b_idx] += 1
    elif tipo == 'atendimento' and fila == 2:
        saidas_f2[b_idx] += 1
        # Saiu do buffet -> sentou nas mesas
        cur_mesas += 1
        mesas_timeline.append((t_rel_min, cur_mesas))
    elif tipo == 'chegada' and fila == 3:
        chegadas_f3[b_idx] += 1
    elif tipo == 'atendimento' and fila == 3:
        saidas_f3[b_idx] += 1
        # Saiu das mesas e deixou o RU
        cur_mesas = max(0, cur_mesas - 1)
        mesas_timeline.append((t_rel_min, cur_mesas))

# Capacidades médias de atendimento (pessoas/min) observadas
mu1 = 3.316674 # Catraca
mu2 = 3.715669 # Buffet

# Taxas de chegada por minuto em cada bloco de 5 minutos
lambda1_blocos = [ch / 5.0 for ch in chegadas_f1]
lambda2_blocos = [ch / 5.0 for ch in chegadas_f2]

# Fator de utilização rho(t) por bloco
rho1_blocos = [lam / mu1 for lam in lambda1_blocos]
rho2_blocos = [lam / mu2 for lam in lambda2_blocos]

# Cores institucionais do projeto
COR_NAVY = '#16263A'
COR_BLUE = '#2663B4'
COR_RED = '#DC2626'
COR_GREEN = '#16A34A'
COR_PINK = '#EC4899'
COR_ORANGE = '#EA580C'

plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#CBD5E1'
plt.rcParams['axes.linewidth'] = 0.8


# ==============================================================================
# GRÁFICO 1: Utilização Global Comparativa das Filas (Médias e Picos)
# ==============================================================================
fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
filas = ['Fila 1\n(Entrada/Catraca)', 'Fila 2\n(Buffet/Serviço)', 'Salão de Mesas\n(216 Cadeiras)', 'Fila 3\n(Saída / Almoço)']
rho_medio = [0.8860 * 100, 0.7908 * 100, 24.6, 132.8] # Mesas média = 24.6%
rho_pico = [1.1450 * 100, 0.9800 * 100, 53.7, 132.8]  # Mesas pico = 116/216 = 53.7%

x = np.arange(len(filas))
width = 0.35

rects1 = ax.bar(x - width/2, rho_medio, width, label='Utilização Média Global', color=[COR_RED, COR_GREEN, COR_PINK, '#9333EA'], alpha=0.85)
rects2 = ax.bar(x + width/2, rho_pico, width, label='Utilização no Horário de Pico', color=[COR_RED, COR_GREEN, COR_PINK, '#9333EA'], alpha=0.45, hatch='//')

# Linha de saturação 100%
ax.axhline(100, color='#B91C1C', linestyle='--', linewidth=1.8, label='Limite Crítico de Saturação (ρ = 1,0 / 100%)')

ax.set_ylabel('Taxa de Utilização (%)', fontsize=12, fontweight='bold', color=COR_NAVY)
ax.set_title('Utilização do Sistema por Subsistema — Média vs. Pico (04/11/2026)', fontsize=14, fontweight='bold', color=COR_NAVY, pad=15)
ax.set_xticks(x)
ax.set_xticklabels(filas, fontsize=11, fontweight='bold', color=COR_NAVY)
ax.set_ylim(0, 155)
ax.legend(frameon=True, facecolor='white', framealpha=0.9, fontsize=10, loc='upper left')

for rect in rects1:
    h = rect.get_height()
    ax.annotate(f'{h:.1f}%', xy=(rect.get_x() + rect.get_width()/2, h), xytext=(0, 3),
                textcoords="offset points", ha='center', va='bottom', fontsize=9.5, fontweight='bold', color=COR_NAVY)

for rect in rects2:
    h = rect.get_height()
    ax.annotate(f'{h:.1f}%', xy=(rect.get_x() + rect.get_width()/2, h), xytext=(0, 3),
                textcoords="offset points", ha='center', va='bottom', fontsize=9.5, fontweight='bold', color=COR_NAVY)

plt.tight_layout()
p1 = os.path.join(GRAFICOS_DIR, 'grafico1_utilizacao_comparativa_filas.png')
plt.savefig(p1, dpi=300)
plt.close()
print(f'Salvo: {p1}')


# ==============================================================================
# GRÁFICO 2: Evolução Temporal da Utilização da Fila 1 (Blocos de 5 min)
# ==============================================================================
fig, ax = plt.subplots(figsize=(11, 5.5), dpi=300)
x_indices = np.arange(len(rotulos_blocos))
rho1_pct = [r * 100 for r in rho1_blocos]

ax.plot(x_indices, rho1_pct, marker='o', markersize=7, linewidth=2.4, color=COR_RED, label='Utilização Efetiva da Catraca (Fila 1)')
ax.fill_between(x_indices, 0, rho1_pct, color=COR_RED, alpha=0.15)

# Linha de 100%
ax.axhline(100, color='#B91C1C', linestyle='--', linewidth=1.8, label='Saturação (ρ = 1,0): Chegadas > Atendimento')

# Faixas de regime
ax.axvspan(0, 2, color='#3B82F6', alpha=0.10, label='Regime de Calma (ρ < 25%)')
ax.axvspan(6, 10, color='#EF4444', alpha=0.15, label='Regime de Pico (ρ > 100% — Fila física acumula)')
ax.axvspan(12, 13, color='#EF4444', alpha=0.10)

ax.set_title('Evolução da Taxa de Utilização na Fila 1 por Blocos de 5 Minutos', fontsize=14, fontweight='bold', color=COR_NAVY, pad=15)
ax.set_xlabel('Janela de Tempo (Blocos de 5 minutos)', fontsize=11, fontweight='bold', color=COR_NAVY)
ax.set_ylabel('Fator de Utilização ρ (%)', fontsize=11, fontweight='bold', color=COR_NAVY)
ax.set_xticks(x_indices)
ax.set_xticklabels(rotulos_blocos, rotation=35, ha='right', fontsize=9)
ax.set_ylim(0, 130)
ax.legend(frameon=True, facecolor='white', framealpha=0.9, fontsize=9.5, loc='upper left')

idx_max = np.argmax(rho1_pct)
ax.annotate(f'PICO CRÍTICO: {rho1_pct[idx_max]:.1f}%\n(19 chegadas em 5 min)',
            xy=(idx_max, rho1_pct[idx_max]), xytext=(idx_max - 2.8, rho1_pct[idx_max] + 8),
            arrowprops=dict(facecolor=COR_RED, shrink=0.08, width=1.5, headwidth=6),
            fontsize=9.5, fontweight='bold', color=COR_RED, bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=COR_RED, lw=1))

plt.tight_layout()
p2 = os.path.join(GRAFICOS_DIR, 'grafico2_evolucao_utilizacao_fila1_blocos.png')
plt.savefig(p2, dpi=300)
plt.close()
print(f'Salvo: {p2}')


# ==============================================================================
# GRÁFICO 3: Taxas Simultâneas: Chegadas (λ) vs. Capacidade (μ) nas Filas 1 e 2
# ==============================================================================
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 8), dpi=300, sharex=True)

# Subplot Fila 1
ax1.plot(x_indices, lambda1_blocos, marker='s', markersize=6, linewidth=2.0, color=COR_RED, label='Taxa de Chegadas λ_1(t) [p/min]')
ax1.axhline(mu1, color=COR_NAVY, linestyle='-', linewidth=2.0, label=f'Capacidade da Catraca μ_1 = {mu1:.2f} p/min')
ax1.fill_between(x_indices, mu1, lambda1_blocos, where=[l > mu1 for l in lambda1_blocos], color=COR_RED, alpha=0.35, interpolate=True, label='Sobrecarga Estocástica (λ > μ)')
ax1.set_title('Fila 1 (Entrada / Catraca): Taxa de Chegada λ vs. Capacidade μ', fontsize=12, fontweight='bold', color=COR_NAVY)
ax1.set_ylabel('Pessoas / minuto', fontsize=10, fontweight='bold', color=COR_NAVY)
ax1.set_ylim(0, 4.5)
ax1.legend(loc='upper left', fontsize=9, frameon=True, facecolor='white')

# Subplot Fila 2
ax2.plot(x_indices, lambda2_blocos, marker='^', markersize=6, linewidth=2.0, color=COR_GREEN, label='Taxa de Chegadas ao Buffet λ_2(t) [p/min]')
ax2.axhline(mu2, color=COR_NAVY, linestyle='-', linewidth=2.0, label=f'Capacidade do Buffet μ_2 = {mu2:.2f} p/min')
ax2.fill_between(x_indices, mu2, lambda2_blocos, where=[l > mu2 for l in lambda2_blocos], color=COR_GREEN, alpha=0.35, interpolate=True, label='Sobrecarga no Buffet (λ > μ)')
ax2.set_title('Fila 2 (Buffet / Atendimento): Taxa de Chegada λ_2 vs. Capacidade μ_2', fontsize=12, fontweight='bold', color=COR_NAVY)
ax2.set_xlabel('Janela de Tempo (Blocos de 5 minutos)', fontsize=11, fontweight='bold', color=COR_NAVY)
ax2.set_ylabel('Pessoas / minuto', fontsize=10, fontweight='bold', color=COR_NAVY)
ax2.set_xticks(x_indices)
ax2.set_xticklabels(rotulos_blocos, rotation=35, ha='right', fontsize=9)
ax2.set_ylim(0, 6.5)
ax2.legend(loc='upper left', fontsize=9, frameon=True, facecolor='white')

plt.tight_layout()
p3 = os.path.join(GRAFICOS_DIR, 'grafico3_taxas_chegada_vs_capacidade.png')
plt.savefig(p3, dpi=300)
plt.close()
print(f'Salvo: {p3}')


# ==============================================================================
# GRÁFICO 4: Ocupação do Salão de Mesas ao Longo do Tempo (vs. Limite 216 Cadeiras)
# ==============================================================================
fig, ax = plt.subplots(figsize=(11, 5.5), dpi=300)
t_mesas, n_mesas = zip(*mesas_timeline)

ax.plot(t_mesas, n_mesas, color=COR_PINK, linewidth=2.5, label='Alunos Sentados Almoçando (Ocupação Real)')
ax.fill_between(t_mesas, 0, n_mesas, color=COR_PINK, alpha=0.20)

# Limite físico
ax.axhline(216, color='#DC2626', linestyle='--', linewidth=2.0, label='Capacidade Máxima Físico-Arquitetural (K = 216 Cadeiras)')

# Faixas qualitativas de lotação
ax.axhspan(0, 108, color='#10B981', alpha=0.08, label='Faixa Tranquila (< 50% de ocupação)')
ax.axhspan(108, 162, color='#F59E0B', alpha=0.08, label='Faixa Moderada (50% a 74% de ocupação)')

pico_val = max(n_mesas)
idx_pico = n_mesas.index(pico_val)
t_pico = t_mesas[idx_pico]

ax.scatter([t_pico], [pico_val], color='#BE185D', s=80, zorder=5)
ax.annotate(f'PICO MÁXIMO:\n{pico_val} cadeiras ({pico_val/216*100:.1f}%)\nàs {t_pico:.1f} min',
            xy=(t_pico, pico_val), xytext=(t_pico - 14, pico_val + 22),
            arrowprops=dict(facecolor='#BE185D', shrink=0.08, width=1.5, headwidth=6),
            fontsize=9.5, fontweight='bold', color='#831843',
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec='#BE185D', lw=1))

ax.set_title('Ocupação Dinâmica do Salão de Mesas (Capacidade Nominal K = 216 Assentos)', fontsize=14, fontweight='bold', color=COR_NAVY, pad=15)
ax.set_xlabel('Tempo Decorrido da Coleta (minutos)', fontsize=11, fontweight='bold', color=COR_NAVY)
ax.set_ylabel('Cadeiras Ocupadas no Salão', fontsize=11, fontweight='bold', color=COR_NAVY)
ax.set_xlim(0, max(t_mesas) + 1)
ax.set_ylim(0, 240)
ax.legend(frameon=True, facecolor='white', framealpha=0.9, fontsize=9.5, loc='upper left')

plt.tight_layout()
p4 = os.path.join(GRAFICOS_DIR, 'grafico4_ocupacao_salao_mesas_limite.png')
plt.savefig(p4, dpi=300)
plt.close()
print(f'Salvo: {p4}')


# ==============================================================================
# GRÁFICO 5: PAINEL CONSOLIDADO 4 EM 1 (DASHBOARD COMPLETO DE UTILIZAÇÃO)
# ==============================================================================
fig, ((ax_a, ax_b), (ax_c, ax_d)) = plt.subplots(2, 2, figsize=(15, 10), dpi=300)

# (A) Barras de Utilização
bars = ax_a.bar(['F1 (Catraca)', 'F2 (Buffet)', 'Mesas (Pico)', 'F3 (Saída)'], 
                [88.6, 79.1, 53.7, 132.8], 
                color=[COR_RED, COR_GREEN, COR_PINK, '#9333EA'], width=0.55)
ax_a.axhline(100, color='#B91C1C', linestyle='--', linewidth=1.5, label='Limite ρ = 100%')
ax_a.set_ylabel('Utilização (%)', fontweight='bold', fontsize=10, color=COR_NAVY)
ax_a.set_title('(A) Fator de Utilização Comparativo por Subsistema', fontweight='bold', fontsize=11, color=COR_NAVY)
ax_a.set_ylim(0, 155)
for b in bars:
    h = b.get_height()
    ax_a.annotate(f'{h:.1f}%', xy=(b.get_x() + b.get_width()/2, h), xytext=(0, 3),
                  textcoords="offset points", ha='center', va='bottom', fontsize=9, fontweight='bold')
ax_a.legend(loc='upper right', fontsize=8.5)

# (B) Utilização F1 ao Longo do Tempo
ax_b.plot(x_indices, rho1_pct, marker='o', color=COR_RED, linewidth=2.0)
ax_b.fill_between(x_indices, 0, rho1_pct, color=COR_RED, alpha=0.15)
ax_b.axhline(100, color='#B91C1C', linestyle='--', linewidth=1.5, label='Saturação ρ = 100%')
ax_b.set_ylabel('ρ Fila 1 (%)', fontweight='bold', fontsize=10, color=COR_NAVY)
ax_b.set_title('(B) Utilização da Fila 1 (Entrada) por Blocos de 5 min', fontweight='bold', fontsize=11, color=COR_NAVY)
ax_b.set_xticks(x_indices[::2])
ax_b.set_xticklabels(rotulos_blocos[::2], rotation=30, ha='right', fontsize=8)
ax_b.set_ylim(0, 130)
ax_b.legend(loc='upper left', fontsize=8.5)

# (C) Taxa de Chegada vs Capacidade (F1)
ax_c.plot(x_indices, lambda1_blocos, marker='s', color=COR_RED, label='Chegadas λ_1(t) [p/min]')
ax_c.axhline(mu1, color=COR_NAVY, linestyle='-', linewidth=1.8, label=f'Capacidade μ_1 = {mu1:.2f} p/min')
ax_c.fill_between(x_indices, mu1, lambda1_blocos, where=[l > mu1 for l in lambda1_blocos], color=COR_RED, alpha=0.3)
ax_c.set_ylabel('Pessoas / min', fontweight='bold', fontsize=10, color=COR_NAVY)
ax_c.set_title('(C) Chegadas λ vs. Capacidade μ na Catraca (Fila 1)', fontweight='bold', fontsize=11, color=COR_NAVY)
ax_c.set_xticks(x_indices[::2])
ax_c.set_xticklabels(rotulos_blocos[::2], rotation=30, ha='right', fontsize=8)
ax_c.set_ylim(0, 4.5)
ax_c.legend(loc='upper left', fontsize=8.5)

# (D) Ocupação das Mesas
ax_d.plot(t_mesas, n_mesas, color=COR_PINK, linewidth=2.2, label='Ocupação Real')
ax_d.axhline(216, color='#DC2626', linestyle='--', linewidth=1.5, label='Capacidade (216 cadeiras)')
ax_d.fill_between(t_mesas, 0, n_mesas, color=COR_PINK, alpha=0.20)
ax_d.set_ylabel('Cadeiras Ocupadas', fontweight='bold', fontsize=10, color=COR_NAVY)
ax_d.set_title('(D) Ocupação do Salão de Mesas (0 a 65 min)', fontweight='bold', fontsize=11, color=COR_NAVY)
ax_d.set_xlabel('Minutos Decorridos', fontweight='bold', fontsize=10, color=COR_NAVY)
ax_d.set_xlim(0, max(t_mesas)+1)
ax_d.set_ylim(0, 240)
ax_d.legend(loc='upper left', fontsize=8.5)

plt.suptitle('PAINEL CONSOLIDADO DE UTILIZAÇÃO E OCUPAÇÃO DO RU (Sessão 04/11/2026)', fontsize=15, fontweight='bold', color=COR_NAVY, y=0.99)
plt.tight_layout()
p5 = os.path.join(GRAFICOS_DIR, 'painel_completo_utilizacao_todas_filas.png')
plt.savefig(p5, dpi=300)
plt.close()
print(f'Salvo: {p5}')
