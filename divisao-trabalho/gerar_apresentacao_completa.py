import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.chart.data import ChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION

OUT = '/home/luizcaripuna/Documentos/AVALIAÇÃO DE DESEMPENHO/projeto-ru/divisao-trabalho/Afericao_Filas_RU_Seminario.pptx'

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# Paleta Institucional e do Projeto RU
NAVY = RGBColor(22, 38, 58)        # Fundo escuro / Títulos principais
BLUE = RGBColor(38, 99, 180)       # Azul destaque / Primário
LIGHT_BLUE = RGBColor(234, 242, 252) # Fundo cartões suaves
RED = RGBColor(220, 38, 38)        # Fila 1 - Entrada / Catraca (Vermelha)
GREEN = RGBColor(22, 163, 74)      # Fila 2 - Buffet / Atendimento (Verde)
PINK = RGBColor(236, 72, 153)      # Fila 3 / Mesas - Salão & Saída (Rosa)
ORANGE = RGBColor(234, 138, 34)    # Destaques secundários / Alertas
DARK = RGBColor(33, 41, 54)        # Texto escuro
GRAY = RGBColor(100, 116, 139)     # Texto secundário
LIGHT = RGBColor(248, 250, 252)    # Fundo de cartões neutros
BORDER = RGBColor(226, 232, 240)   # Bordas suaves
WHITE = RGBColor(255, 255, 255)

def rect(slide, x, y, w, h, color, radius=True):
    shp = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    shp.fill.solid()
    shp.fill.fore_color.rgb = color
    shp.line.fill.background()
    return shp

def card_box(slide, x, y, w, h, bg_color=LIGHT, border_color=None):
    shp = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    shp.fill.solid()
    shp.fill.fore_color.rgb = bg_color
    if border_color:
        shp.line.color.rgb = border_color
        shp.line.width = Pt(1.2)
    else:
        shp.line.fill.background()
    return shp

def textbox(slide, text, x, y, w, h, size=14, color=DARK, bold=False, align=PP_ALIGN.LEFT, font='Calibri'):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.clear()
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.alignment = align
    if len(p.runs) > 0:
        r = p.runs[0]
        r.font.name = font
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.color.rgb = color
    return box

def multi_text(slide, lines, x, y, w, h, align=PP_ALIGN.LEFT, font='Calibri'):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.clear()
    tf.word_wrap = True
    for i, (txt, sz, col, bld, sp_after) in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = txt
        p.alignment = align
        if sp_after > 0:
            p.space_after = Pt(sp_after)
        if len(p.runs) > 0:
            r = p.runs[0]
            r.font.name = font
            r.font.size = Pt(sz)
            r.font.color.rgb = col
            r.font.bold = bld
    return box

def title_header(slide, kicker, heading, subtitle=None):
    rect(slide, 0, 0, 13.333, 0.14, BLUE, False)
    textbox(slide, kicker.upper(), 0.75, 0.40, 11.5, 0.35, size=11, color=BLUE, bold=True)
    textbox(slide, heading, 0.75, 0.78, 11.8, 0.65, size=24, color=NAVY, bold=True)
    if subtitle:
        textbox(slide, subtitle, 0.75, 1.45, 11.8, 0.40, size=13, color=GRAY)

def footer(slide, n, presenter=None):
    footer_text = 'Aferição, Modelagem e Simulação das Filas do RU • Coleta em 04/11/2026'
    if presenter:
        footer_text += f' • Apresentador(a): {presenter}'
    textbox(slide, footer_text, 0.75, 7.10, 10.0, 0.25, size=9, color=GRAY)
    textbox(slide, f'{n} / 17', 12.0, 7.10, 0.6, 0.25, size=9, color=GRAY, bold=True, align=PP_ALIGN.RIGHT)

def add_table(slide, x, y, cx, cy, headers, rows, col_widths=None):
    t_shape = slide.shapes.add_table(len(rows) + 1, len(headers), Inches(x), Inches(y), Inches(cx), Inches(cy))
    table = t_shape.table
    if col_widths:
        for idx, w in enumerate(col_widths):
            table.columns[idx].width = Inches(w)
    
    # Headers
    for c_idx, h in enumerate(headers):
        cell = table.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY
        cell.text_frame.clear()
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.alignment = PP_ALIGN.CENTER
        r = p.runs[0]
        r.font.size = Pt(11)
        r.font.bold = True
        r.font.color.rgb = WHITE
        r.font.name = 'Calibri'
    
    # Data rows
    for r_idx, row in enumerate(rows):
        bg = LIGHT if r_idx % 2 == 0 else WHITE
        for c_idx, val in enumerate(row):
            cell = table.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg
            cell.text_frame.clear()
            p = cell.text_frame.paragraphs[0]
            p.text = str(val)
            p.alignment = PP_ALIGN.CENTER if c_idx > 0 else PP_ALIGN.LEFT
            r = p.runs[0]
            r.font.size = Pt(11)
            r.font.color.rgb = DARK
            r.font.name = 'Calibri'
            if c_idx == 0 or c_idx == len(row) - 1:
                r.font.bold = True
    return t_shape


# ==============================================================================
# SLIDE 1: CAPA
# ==============================================================================
s1 = prs.slides.add_slide(prs.slide_layouts[6])
rect(s1, 0, 0, 13.333, 7.5, NAVY, False)
rect(s1, 0.75, 0.85, 0.14, 5.8, BLUE, False)

multi_text(s1, [
    ('AVALIAÇÃO DE DESEMPENHO DE SISTEMAS', 14, RGBColor(176, 202, 240), True, 12),
    ('Aferição, Modelagem e Simulação\ndas Filas do Restaurante Universitário', 34, WHITE, True, 16),
    ('Estudo Experimental de Engenharia com Abordagem M/M/c e Simulação Discreta (DES)', 18, RGBColor(210, 226, 245), False, 42),
    ('Equipe do Projeto:', 13, RGBColor(176, 202, 240), True, 4),
    ('Adriana  •  Jaiane  •  Lucas  •  Otávio  •  Vanessa', 16, WHITE, True, 20),
    ('Data da Coleta: 04 de Novembro de 2026  •  Duração: 65,34 minutos  •  RU Central', 12, RGBColor(176, 202, 240), False, 0)
], 1.1, 1.15, 11.2, 5.2)


# ==============================================================================
# SLIDE 2: ESTRUTURA DA APRESENTAÇÃO / AGENDA
# ==============================================================================
s2 = prs.slides.add_slide(prs.slide_layouts[6])
title_header(s2, 'Visão Geral do Seminário', 'Estrutura da Apresentação e Divisão da Equipe', 'Alinhamento metodológico do campo à simulação computacional.')

agenda_items = [
    ('01', 'Introdução & Contexto', 'Adriana', 'Desafio do RU, as 3 filas e organização da equipe em campo.'),
    ('02', 'Aferição: Método', 'Lucas', 'Aplicação web offline-first, rede local e método de cronometragem.'),
    ('03', 'Aferição: Resultados', 'Jaiane', 'Dados das filas, separação calma vs. pico e métricas empíricas.'),
    ('04', 'Modelagem Teórica', 'Otávio', 'Espaço de estados, cadeia de Markov, matriz P e Lei de Little.'),
    ('05', 'Simulação & Conclusão', 'Vanessa / Adriana', 'Trace-driven DES, cenários what-if e diagnóstico final (quando/quanto/por quê).')
]

for i, (num, titulo, resp, desc) in enumerate(agenda_items):
    x = 0.75 + i * 2.40
    card_box(s2, x, 2.15, 2.25, 4.5, LIGHT, BORDER)
    rect(s2, x, 2.15, 2.25, 0.12, BLUE, False)
    multi_text(s2, [
        (num, 24, BLUE, True, 4),
        (titulo, 15, NAVY, True, 6),
        (f'Responsável: {resp}', 11, ORANGE, True, 12),
        (desc, 12, GRAY, False, 0)
    ], x + 0.18, 2.45, 1.89, 4.0)

footer(s2, 2)


# ==============================================================================
# SLIDE 3: ADRIANA - CONTEXTO E O SISTEMA DO RU
# ==============================================================================
s3 = prs.slides.add_slide(prs.slide_layouts[6])
title_header(s3, 'Introdução e Contexto Operacional', 'O Desafio do Restaurante Universitário e as Três Filas em Série', 'Compreendendo o fluxo contínuo dos estudantes desde a calçada até a saída final.')

filas_boxes = [
    ('FILA 1 (VERMELHA)', 'Entrada → Catraca', '192 Chegadas Efetivas', 'Espera externa na calçada até a validação do cartão/identificação.', RED),
    ('FILA 2 (VERDE)', 'Catraca → Atendimento', '192 Passagens Registradas', 'Fila interna para pegar bandeja, talheres e servir os alimentos.', GREEN),
    ('SALÃO & FILA 3 (ROSA)', 'Mesas → Saída', '216 Cadeiras (36 Mesas)', 'Consumo da refeição nas mesas e efluxo contínuo até a porta de saída.', PINK)
]

for i, (f_nome, f_etapa, f_vol, f_desc, cor) in enumerate(filas_boxes):
    x = 0.75 + i * 4.0
    card_box(s3, x, 2.15, 3.8, 3.2, WHITE, cor)
    rect(s3, x, 2.15, 3.8, 0.14, cor, False)
    multi_text(s3, [
        (f_nome, 12, cor, True, 4),
        (f_etapa, 18, NAVY, True, 8),
        (f_vol, 14, cor, True, 10),
        (f_desc, 12, DARK, False, 0)
    ], x + 0.25, 2.45, 3.3, 2.6)

card_box(s3, 0.75, 5.65, 11.8, 1.2, LIGHT_BLUE, BLUE)
multi_text(s3, [
    ('OBJETIVO CENTRAL DA AVALIAÇÃO DE DESEMPENHO', 12, BLUE, True, 2),
    ('Avaliar quantitativamente as filas do RU por meio de medição em campo, confrontar com as fórmulas clássicas de Teoria das Filas (M/M/c e Lei de Little) e construir um simulador para testar intervenções operacionais (segunda catraca e segundo buffet), identificando o gargalo definitivo.', 12, NAVY, False, 0)
], 0.95, 5.75, 11.4, 1.0)

footer(s3, 3, 'Adriana')


# ==============================================================================
# SLIDE 4: ADRIANA - RELATO DE CAMPO E ORGANIZAÇÃO DA EQUIPE
# ==============================================================================
s4 = prs.slides.add_slide(prs.slide_layouts[6])
title_header(s4, 'Organização de Campo', 'Relato da Coleta: Do Replanejamento à Execução em 04/11/2026', 'Como a equipe superou imprevistos para realizar a medição de 1 hora exigida pelo professor.')

card_box(s4, 0.75, 2.15, 5.7, 4.6, LIGHT, BORDER)
multi_text(s4, [
    ('DIÁRIO DE BORDO E APRENDIZADOS', 13, BLUE, True, 8),
    ('• Primeira tentativa (21/10/2026):', 13, NAVY, True, 2),
    ('  A equipe compareceu ao RU, porém um grande evento acadêmico na universidade descaracterizou o fluxo normal e dificultou a medição padrão.', 12, GRAY, False, 8),
    ('• Replanejamento & Melhorias:', 13, NAVY, True, 2),
    ('  Decidimos aprimorar o sistema de coleta web (botões maiores, melhor tolerância a toques acidentais) e agendar nova ida estratégica.', 12, GRAY, False, 8),
    ('• Coleta Definitiva (04/11/2026):', 13, NAVY, True, 2),
    ('  Chegamos com antecedência para posicionar os operadores. Coleta rigorosa de 65,34 minutos (1 hora solicitada), capturando 1.074 eventos puros.', 12, GRAY, False, 0)
], 0.95, 2.35, 5.3, 4.2)

card_box(s4, 6.75, 2.15, 5.8, 4.6, WHITE, BORDER)
rect(s4, 6.75, 2.15, 5.8, 0.12, NAVY, False)
multi_text(s4, [
    ('DISTRIBUIÇÃO DOS 4 OPERADORES EM CAMPO', 13, NAVY, True, 10),
    ('1. Fila 1 - Entrada / Calçada (Operador 1):', 13, RED, True, 2),
    ('   Responsável por marcar cada novo estudante que entrava no final da fila externa.', 12, DARK, False, 8),
    ('2. Fila 1 - Catraca / Validação (Operador 2):', 13, RED, True, 2),
    ('   Cronometrava o instante de passagem na catraca (acionando entrada na F2).', 12, DARK, False, 8),
    ('3. Fila 2 - Buffet / Alimento (Operador 3):', 13, GREEN, True, 2),
    ('   Registrava a saída da linha de servir ao receber o prato e avançar para as mesas.', 12, DARK, False, 8),
    ('4. Fila 3 - Saída do Restaurante (Operador 4):', 13, PINK, True, 2),
    ('   Marcava o momento em que os alunos entregavam a bandeja e deixavam o RU.', 12, DARK, False, 0)
], 6.95, 2.35, 5.4, 4.2)

footer(s4, 4, 'Adriana')


# ==============================================================================
# SLIDE 5: LUCAS - MÉTODO & ARQUITETURA DE SOFTWARE
# ==============================================================================
s5 = prs.slides.add_slide(prs.slide_layouts[6])
title_header(s5, 'Aferição — Método & Engenharia', 'Arquitetura do Sistema Fila RU: Solução Web Autônoma e Offline-First', 'Tecnologia desenvolvida em JavaScript nativo para garantir 100% de confiabilidade em campo.')

cards_eng = [
    ('ZERO DEPENDÊNCIA DE INTERNET', 'Hotspot Wi-Fi Local', 'O notebook do coordenador emitiu sua própria rede Wi-Fi local (192.168.137.1). Os celulares dos operadores conectaram diretamente via navegador, sem precisar de internet ou gastar dados 4G/5G.', BLUE),
    ('EVENT SOURCING APPEND-ONLY', 'Imutabilidade dos Dados', 'Cada toque do operador gerou um evento imutável com timestamp em milissegundos gravado em `eventos.jsonl`. O estado do sistema é derivado por função pura, permitindo replay e auditoria temporal.', NAVY),
    ('RESILIÊNCIA & FILA OFFLINE', 'Tolerância a Quedas', 'Caso o operador se afastasse e perdesse sinal Wi-Fi, os toques eram armazenados no localStorage do celular. Ao reconectar, a sincronização ocorria mantendo a cronologia original (flag tardio: true).', GREEN),
    ('CONCORRÊNCIA E SEGURANÇA', 'PIN & Validação Atômica', 'Sessão protegida por PIN aleatório de 4 dígitos. Bloqueio automático de comandos conflitantes (ex: se dois operadores tentassem atender a mesma pessoa, o segundo era rejeitado com JA_ATENDIDO).', ORANGE)
]

for i, (kicker, tit, desc, c) in enumerate(cards_eng):
    col = i % 2
    row = i // 2
    x = 0.75 + col * 6.0
    y = 2.15 + row * 2.35
    card_box(s5, x, y, 5.8, 2.15, WHITE, BORDER)
    rect(s5, x, y, 0.12, 2.15, c, False)
    multi_text(s5, [
        (kicker.upper(), 10, c, True, 2),
        (tit, 16, NAVY, True, 6),
        (desc, 12, DARK, False, 0)
    ], x + 0.28, y + 0.20, 5.3, 1.75)

footer(s5, 5, 'Lucas')


# ==============================================================================
# SLIDE 6: LUCAS - OPERAÇÃO DE CAMPO & COLETA CRONOMETRADA
# ==============================================================================
s6 = prs.slides.add_slide(prs.slide_layouts[6])
title_header(s6, 'Aferição — Método & Coleta', 'Interfaces Móveis Ergonomicamente Adaptadas e Encadeamento Atômico', 'Controle tátil em tempo real e preservação contínua da identidade de cada usuário.')

card_box(s6, 0.75, 2.15, 5.7, 4.6, LIGHT, BORDER)
multi_text(s6, [
    ('ERGONOMIA DOS COLETORES MÓVEIS (CELULAR.HTML)', 12, BLUE, True, 8),
    ('• Botões Táteis Gigantes:', 13, NAVY, True, 2),
    ('  Projetados para operação ágil com apenas uma das mãos, sem que o operador precisasse desviar o olhar do fluxo da fila física.', 12, GRAY, False, 8),
    ('• Perfis Específicos por Posto:', 13, NAVY, True, 2),
    ('  Quem ficou na entrada só via botão "CHEGADA". Quem operava a catraca via botão "PASSOU NA CATRACA" com o número da próxima pessoa.', 12, GRAY, False, 8),
    ('• Tolerância a Erros Humanos:', 13, NAVY, True, 2),
    ('  Botão "Reverter Último" para desatendimento acidental e botão "×" para anular desistências reais sem comprometer o fluxo de dados.', 12, GRAY, False, 0)
], 0.95, 2.35, 5.3, 4.2)

card_box(s6, 6.75, 2.15, 5.8, 4.6, WHITE, BORDER)
rect(s6, 6.75, 2.15, 5.8, 0.12, BLUE, False)
multi_text(s6, [
    ('ENCADEAMENTO ATÔMICO ENTRE FILAS', 12, NAVY, True, 8),
    ('• Rastreamento Unificado do Aluno:', 13, BLUE, True, 4),
    ('  Quando o operador da catraca registrava a saída da Fila 1, o sistema disparava atomicamente o evento de entrada na Fila 2 com o mesmo número de identificador e timestamp.', 12, DARK, False, 10),
    ('• Transição para as Mesas:', 13, GREEN, True, 4),
    ('  A saída do buffet (Fila 2) ocupava automaticamente uma cadeira no módulo de monitoramento do salão de mesas (216 lugares).', 12, DARK, False, 10),
    ('• Medição Exata dos Tempos:', 13, PINK, True, 4),
    ('  Permitiu calcular com precisão de milissegundos o tempo de trânsito até as mesas (F1+F2) e o tempo total de permanência no RU.', 12, DARK, False, 0)
], 6.95, 2.35, 5.4, 4.2)

footer(s6, 6, 'Lucas')


# ==============================================================================
# SLIDE 7: JAIANE - RESULTADOS GLOBAIS DAS TRÊS FILAS
# ==============================================================================
s7 = prs.slides.add_slide(prs.slide_layouts[6])
title_header(s7, 'Aferição — Resultados Empíricos', 'Síntese Numérica das Três Filas Coletadas em 04/11/2026', '65,34 minutos de observação contínua e 1.074 eventos analisados estatisticamente.')

headers = ['Etapa / Fila', 'Entradas', 'Saídas', 'λ (p/min)', 'μ (p/min)', 'Utilização (ρ)', 'Espera Média (Wq)']
rows = [
    ['Fila 1 — Entrada → Catraca', '192', '192', '2,94', '3,32', '0,886 (88,6%)', '131,5 s (2m 11s)'],
    ['Fila 2 — Buffet / Alimentos', '192', '185', '2,94', '3,72', '0,791 (79,1%)', '142,1 s (2m 22s)'],
    ['Fila 3 — Mesas → Saída', '185', '95', '2,83', '2,13', '1,328 (132,8%)', '1.391,9 s (23m 12s)']
]
col_w = [2.9, 1.2, 1.2, 1.5, 1.5, 1.8, 1.7]
add_table(s7, 0.75, 2.15, 11.8, 2.3, headers, rows, col_w)

res_cards = [
    ('FILA 1 (ENTRADA)', 'ρ = 0,886', 'Operou perto do limite de 1 servidor (88,6%). Pico de 51 pessoas na fila física externa.', RED),
    ('FILA 2 (BUFFET)', 'ρ = 0,791', 'Capacidade técnica do buffet foi ligeiramente superior à da catraca (3,72 vs 3,32 p/min).', GREEN),
    ('SALÃO & SAÍDA', 'ρ = 1,328', 'Taxa ρ > 1 na saída reflete a permanência de 23 min nas mesas: alunos acumularam no salão.', PINK)
]

for i, (tit, val, desc, c) in enumerate(res_cards):
    x = 0.75 + i * 4.0
    card_box(s7, x, 4.75, 3.8, 2.0, LIGHT, BORDER)
    rect(s7, x, 4.75, 3.8, 0.10, c, False)
    multi_text(s7, [
        (tit, 11, c, True, 2),
        (val, 20, NAVY, True, 4),
        (desc, 11, DARK, False, 0)
    ], x + 0.20, 4.95, 3.4, 1.7)

footer(s7, 7, 'Jaiane')


# ==============================================================================
# SLIDE 8: JAIANE - SEPARAÇÃO CALMA VS. PICO PELAS CHEGADAS
# ==============================================================================
s8 = prs.slides.add_slide(prs.slide_layouts[6])
title_header(s8, 'Aferição — Resultados Empíricos', 'Separação Rigorosa: Regime de Calma vs. Regime de Pico', 'Exigência da disciplina: a distinção deve ser feita pelas chegadas por minuto, e não pelas ondas da fila.')

card_box(s8, 0.75, 2.15, 5.7, 4.6, LIGHT, BORDER)
rect(s8, 0.75, 2.15, 5.7, 0.12, BLUE, False)
multi_text(s8, [
    ('REGIME DE CALMA (MINUTOS 0 A 10)', 13, BLUE, True, 8),
    ('• Taxa Média de Chegadas (λ):', 13, NAVY, True, 2),
    ('  Apenas 6 alunos chegaram nos primeiros 10 minutos (λ = 0,60 pessoas/min).', 12, DARK, False, 8),
    ('• Capacidade da Catraca (μ):', 13, NAVY, True, 2),
    ('  Com μ = 3,32 pessoas/min, o fator de utilização foi de apenas ρ = 0,18.', 12, DARK, False, 8),
    ('• Comportamento Operacional:', 13, NAVY, True, 2),
    ('  Atendimento instantâneo, sem formação de fila externa sustentada.', 12, GRAY, False, 0)
], 0.95, 2.35, 5.3, 4.2)

card_box(s8, 6.75, 2.15, 5.8, 4.6, WHITE, RED)
rect(s8, 6.75, 2.15, 5.8, 0.12, RED, False)
multi_text(s8, [
    ('REGIME DE PICO (MINUTOS 30 A 50 E 55 A 65)', 13, RED, True, 8),
    ('• Taxa Média de Chegadas no Pico (λ_pico):', 13, NAVY, True, 2),
    ('  Chegaram 74 alunos em 20 minutos (λ_pico = 3,70 a 3,80 pessoas/min).', 12, DARK, False, 8),
    ('• Inversão Crítica (λ > μ):', 13, RED, True, 2),
    ('  A taxa de chegada superou a capacidade máxima de serviço (3,70 > 3,32), elevando a utilização para ρ = 1,12 a 1,15 (> 1,0).', 12, DARK, False, 8),
    ('• Consequência Direta:', 13, NAVY, True, 2),
    ('  A fila acumulou bruscamente, atingindo pico físico de 51 pessoas.', 12, GRAY, False, 0)
], 6.95, 2.35, 5.4, 4.2)

footer(s8, 8, 'Jaiane')


# ==============================================================================
# SLIDE 9: JAIANE - TEMPOS DE ESPERA Wq E DISPERSÃO ESTATÍSTICA
# ==============================================================================
s9 = prs.slides.add_slide(prs.slide_layouts[6])
title_header(s9, 'Aferição — Resultados Empíricos', 'Distribuição dos Tempos de Espera (Wq) e Dispersão Amostral', 'Análise estatística completa com médias, medianas, percentis P90/P95 e tempos extremos.')

headers_disp = ['Métrica de Espera', 'Fila 1 (Entrada)', 'Fila 2 (Buffet)', 'Trânsito Mesas (F1+F2)', 'Permanência Mesas']
rows_disp = [
    ['Média Aritmética (Wq)', '131,5 s (2m 11s)', '142,1 s (2m 22s)', '299,7 s (~5m 00s)', '1.391,9 s (~23m 12s)'],
    ['Mediana (50% da amostra)', '27,4 s (0m 27s)', '132,9 s (2m 13s)', '167,1 s (2m 47s)', '1.421,9 s (~23m 42s)'],
    ['Desvio Padrão Amostral', '225,3 s (3m 45s)', '74,3 s (1m 14s)', '278,9 s (4m 39s)', '352,5 s (5m 52s)'],
    ['Percentil 90 (P90)', '542,0 s (9m 02s)', '236,4 s (3m 56s)', '811,4 s (13m 31s)', '1.802,0 s (~30m 02s)'],
    ['Percentil 95 (P95)', '664,4 s (11m 04s)', '260,1 s (4m 20s)', '895,0 s (14m 55s)', '1.920,0 s (~32m 00s)'],
    ['Pior Tempo Registrado (Máx)', '978,0 s (16m 18s)', '421,4 s (7m 01s)', '1.205,0 s (20m 05s)', '2.215,0 s (~36m 55s)']
]
col_w_disp = [2.8, 2.2, 2.2, 2.4, 2.2]
add_table(s9, 0.75, 2.15, 11.8, 3.4, headers_disp, rows_disp, col_w_disp)

card_box(s9, 0.75, 5.80, 11.8, 1.05, LIGHT_BLUE, BLUE)
multi_text(s9, [
    ('INSIGHT ANALÍTICO SOBRE A DISPERSÃO', 11, BLUE, True, 2),
    ('Na Fila 1, a grande diferença entre a mediana (27 s) e o P90 (9 min) evidencia a disparidade da experiência dos alunos: quem chegou na calma passou quase direto, enquanto quem chegou no pico enfrentou mais de 10 minutos de retenção externa.', 12, DARK, False, 0)
], 0.95, 5.90, 11.4, 0.9)

footer(s9, 9, 'Jaiane')


# ==============================================================================
# SLIDE 10: OTÁVIO - MODELAGEM: ESPAÇO DE ESTADOS & PROCESSO
# ==============================================================================
s10 = prs.slides.add_slide(prs.slide_layouts[6])
title_header(s10, 'Modelagem Teórica', 'Fundamentação Estocástica: Espaço de Estados e Parâmetros', 'Modelando as filas do RU como um processo estocástico de nascimento e morte.')

model_cards = [
    ('DEFINIÇÃO DO ESTADO', 'N(t) = Número na Fila', 'O estado do sistema em qualquer instante t é o número inteiro N(t) de pessoas presentes (em espera ou em atendimento). Varia por transições pontuais discretas (+1 chegada, -1 saída).', BLUE),
    ('PASSO TEMPORAL', 'Δt e Janelas de Análise', 'Modelagem em tempo contínuo com taxas constantes médias (Poisson/Exponencial) e discretização por blocos analíticos de Δt = 5 minutos para confrontação de séries históricas.', NAVY),
    ('PROBABILIDADES', 'Distribuição P_n', 'P_n representa a probabilidade estacionária de encontrar exatamente n pessoas no sistema. Permite calcular a probabilidade de fila vazia (P_0) e probabilidade de espera.', GREEN),
    ('CAPACIDADE FÍSICA', 'K = 216 Cadeiras', 'Enquanto as Filas 1 e 2 possuem capacidade infinita de espera na calçada/corredor, o Salão possui limite rígido K = 216 assentos (4 fileiras de 9 mesas de 6 lugares).', ORANGE)
]

for i, (kicker, tit, desc, c) in enumerate(model_cards):
    x = 0.75 + i * 3.02
    card_box(s10, x, 2.15, 2.82, 4.5, WHITE, BORDER)
    rect(s10, x, 2.15, 2.82, 0.12, c, False)
    multi_text(s10, [
        (kicker.upper(), 10, c, True, 4),
        (tit, 15, NAVY, True, 10),
        (desc, 12, DARK, False, 0)
    ], x + 0.20, 2.45, 2.42, 4.0)

footer(s10, 10, 'Otávio')


# ==============================================================================
# SLIDE 11: OTÁVIO - MATRIZ DE TRANSIÇÃO P & EQUILÍBRIO
# ==============================================================================
s11 = prs.slides.add_slide(prs.slide_layouts[6])
title_header(s11, 'Modelagem Teórica', 'Matriz de Transição P e Equações de Equilíbrio Global', 'Estrutura matemática das taxas de nascimento e morte para filas M/M/1 e M/M/c.')

card_box(s11, 0.75, 2.15, 5.7, 4.6, LIGHT, BORDER)
multi_text(s11, [
    ('MATRIZ DE PROBABILIDADES DE TRANSIÇÃO (P)', 12, BLUE, True, 6),
    ('Para um intervalo infinitesimal Δt, a matriz estocástica P é tridiagonal:', 11, GRAY, False, 8),
    ('P = [ 1-λΔt    λΔt       0        0     ... ]\n    [  μΔt   1-(λ+μ)Δt   λΔt       0     ... ]\n    [   0      μΔt    1-(λ+μ)Δt   λΔt    ... ]\n    [   0       0       μΔt    1-(λ+μ)Δt ... ]', 12, NAVY, True, 12),
    ('• Equação de Equilíbrio (Corte n):', 12, NAVY, True, 2),
    ('  λ · P_n = μ · P_(n+1)', 13, BLUE, True, 6),
    ('• Solução Geral:', 12, NAVY, True, 2),
    ('  P_n = (1 - ρ) · ρ^n   (onde ρ = λ / μ)', 13, BLUE, True, 0)
], 0.95, 2.35, 5.3, 4.2)

card_box(s11, 6.75, 2.15, 5.8, 4.6, WHITE, BORDER)
rect(s11, 6.75, 2.15, 5.8, 0.12, BLUE, False)
multi_text(s11, [
    ('FÓRMULAS ANALÍTICAS DO MODELO M/M/1', 12, NAVY, True, 8),
    ('1. Fator de Utilização:', 12, NAVY, True, 2),
    ('   ρ = λ / μ   (condição de estabilidade: ρ < 1)', 12, DARK, False, 8),
    ('2. Probabilidade de Fila Vazia (Sistema Ocioso):', 12, NAVY, True, 2),
    ('   P_0 = 1 - ρ', 12, DARK, False, 8),
    ('3. Número Médio de Pessoas na Fila (Lq):', 12, NAVY, True, 2),
    ('   Lq = ρ² / (1 - ρ) = λ² / [μ(μ - λ)]', 12, BLUE, True, 8),
    ('4. Tempo Médio de Espera na Fila (Wq):', 12, NAVY, True, 2),
    ('   Wq = Lq / λ = ρ / (μ - λ)', 12, BLUE, True, 8),
    ('5. Tempo Total no Sistema (W):', 12, NAVY, True, 2),
    ('   W = Wq + (1 / μ) = 1 / (μ - λ)', 12, DARK, False, 0)
], 6.95, 2.35, 5.4, 4.2)

footer(s11, 11, 'Otávio')


# ==============================================================================
# SLIDE 12: OTÁVIO - VERIFICAÇÃO PELA LEI DE LITTLE
# ==============================================================================
s12 = prs.slides.add_slide(prs.slide_layouts[6])
title_header(s12, 'Modelagem Teórica', 'Verificação Experimental da Lei de Little: L = λ · W', 'Confronto entre a média ponderada no tempo (Lq) e o produto da taxa empírica pela espera (λ·Wq).')

headers_little = ['Etapa / Fila', 'Lq Observado (Ponderado)', 'λ (p/min)', 'Wq Médio (min)', 'λ · Wq Calculado', 'Divergência (Δ%)', 'Diagnóstico']
rows_little = [
    ['Fila 2 — Buffet / Alimentos', '6,72 alunos', '2,94', '2,37 min', '6,96 alunos', '3,48%', 'Altamente Consistente'],
    ['Fila 1 — Entrada / Catraca', '12,65 alunos', '2,94', '2,19 min', '6,44 alunos', '49,08%', 'Efeito Transitório Inicial']
]
col_w_lit = [2.5, 2.0, 1.2, 1.6, 1.8, 1.3, 1.4]
add_table(s12, 0.75, 2.15, 11.8, 2.2, headers_little, rows_little, col_w_lit)

card_box(s12, 0.75, 4.65, 5.7, 2.2, LIGHT_BLUE, BLUE)
multi_text(s12, [
    ('SUCESSO NA FILA 2 (BUFFET): Δ = 3,48%', 12, BLUE, True, 4),
    ('A Fila 2 operou em regime estacionário livre de represamentos externos:', 11, NAVY, False, 6),
    ('• Lq observado = 6,72 pessoas\n• λ · Wq = 2,938 × 2,369 = 6,96 pessoas\n• Desvio mínimo de 3,48% confirma com rigor experimental a consistência matemática da Teoria das Filas no RU.', 12, DARK, False, 0)
], 0.95, 4.80, 5.3, 1.9)

card_box(s12, 6.75, 4.65, 5.8, 2.2, WHITE, BORDER)
multi_text(s12, [
    ('JUSTIFICATIVA DO TRANSITÓRIO NA FILA 1', 12, ORANGE, True, 4),
    ('Por que a Fila 1 divergiu da média global da Lei de Little?', 11, NAVY, False, 6),
    ('• Aferição registrou 27 pessoas já acumuladas na calçada antes da catraca começar a liberar os alunos (regime transiente inicial).\n• A Lei de Little pressupõe regime permanente estável; ao isolar os blocos pós-abertura, o erro residual cai abaixo de 10%.', 12, GRAY, False, 0)
], 6.95, 4.80, 5.4, 1.9)

footer(s12, 12, 'Otávio')


# ==============================================================================
# SLIDE 13: VANESSA - SIMULAÇÃO: MOTOR DE EVENTOS DISCRETOS
# ==============================================================================
s13 = prs.slides.add_slide(prs.slide_layouts[6])
title_header(s13, 'Simulação Computacional', 'Motor de Simulação por Eventos Discretos Guiado por Traço', 'Diferente de geradores aleatórios abstratos, o simulador preserva o traço empírico real de chegadas.')

des_pillars = [
    ('TRAÇO EMPÍRICO REAL', 'Preservação das Chegadas', 'O horário exato de chegada de cada um dos alunos observados em campo é mantido 100% idêntico, respeitando os picos e pausas naturais da comunidade universitária.', BLUE),
    ('DESACOPLAMENTO DE SERVIÇO', 'Tempo Puro de Atendimento', 'O simulador deduz o tempo que a catraca e o buffet levaram exclusivamente para atender cada indivíduo (descontando o tempo de espera na fila), evitando duplicidades.', NAVY),
    ('FILA ÚNICA COMPARTILHADA', 'Modelagem M/G/c', 'Havendo 2 ou mais servidores (catracas ou linhas de buffet), os estudantes aguardam em fila única e avançam para o primeiro posto desocupado, minimizando tempos ociosos.', GREEN),
    ('SERVICE BLOCKING REAL', 'Restrição das Mesas', 'Se as 216 mesas lotarem, o aluno com a bandeja retém o buffet até vagar cadeira, reproduzindo com fidelidade a física e o bloqueio operacional do restaurante.', RED)
]

for i, (kicker, tit, desc, c) in enumerate(des_pillars):
    x = 0.75 + i * 3.02
    card_box(s13, x, 2.15, 2.82, 4.5, WHITE, BORDER)
    rect(s13, x, 2.15, 2.82, 0.12, c, False)
    multi_text(s13, [
        (kicker.upper(), 10, c, True, 4),
        (tit, 15, NAVY, True, 10),
        (desc, 12, DARK, False, 0)
    ], x + 0.20, 2.45, 2.42, 4.0)

footer(s13, 13, 'Vanessa')


# ==============================================================================
# SLIDE 14: VANESSA - VERIFICAÇÃO E VALIDAÇÃO DO SIMULADOR
# ==============================================================================
s14 = prs.slides.add_slide(prs.slide_layouts[6])
title_header(s14, 'Simulação Computacional', 'Verificação e Validação do Simulador: Aderência de 0,27%', 'Comprovação da fidelidade computacional através da reprodução do cenário de referência (baseline).')

card_box(s14, 0.75, 2.15, 5.7, 4.6, LIGHT, BORDER)
multi_text(s14, [
    ('CALIBRAÇÃO DO BASELINE REAL VS. SIMULADO', 12, BLUE, True, 8),
    ('• Espera Média na Fila 1 (Real):', 13, NAVY, True, 2),
    ('  Wq1_real = 131,52 segundos (2 min 11 s)', 14, DARK, False, 8),
    ('• Espera Média na Fila 1 (Simulado Baseline):', 13, NAVY, True, 2),
    ('  Wq1_sim = 131,88 segundos (2 min 12 s)', 14, BLUE, True, 8),
    ('• Erro Relativo de Calibração:', 13, NAVY, True, 2),
    ('  Δ_calibração = 0,27%  (Altamente Aderente, critério < 5%)', 16, GREEN, True, 12),
    ('• Validação de Conservação de Fluxo:', 13, NAVY, True, 2),
    ('  192 chegadas = 192 atendimentos processados sem perdas na simulação.', 12, GRAY, False, 0)
], 0.95, 2.35, 5.3, 4.2)

card_box(s14, 6.75, 2.15, 5.8, 4.6, WHITE, BORDER)
rect(s14, 6.75, 2.15, 5.8, 0.12, GREEN, False)
multi_text(s14, [
    ('CRITÉRIOS DE QUALIDADE ATENDIDOS', 12, GREEN, True, 8),
    ('1. Verificação contra Fórmulas:', 13, NAVY, True, 2),
    ('   O simulador respeita as propriedades assintóticas de Erlang C e da Lei de Little quando submetido a distribuições teóricas puras.', 12, DARK, False, 8),
    ('2. Validação contra o Traço Anotado:', 13, NAVY, True, 2),
    ('   A curva de pessoas na fila minuto a minuto no simulador coincide com o perfil histórico da coleta real.', 12, DARK, False, 8),
    ('3. Regra de Ouro da Avaliação de Desempenho:', 13, NAVY, True, 2),
    ('   Para testar melhorias com rigor científico, varia-se exatamente uma dimensão operacional por vez.', 12, DARK, False, 0)
], 6.95, 2.35, 5.4, 4.2)

footer(s14, 14, 'Vanessa')


# ==============================================================================
# SLIDE 15: VANESSA - COMPARAÇÃO DE CENÁRIOS WHAT-IF
# ==============================================================================
s15 = prs.slides.add_slide(prs.slide_layouts[6])
title_header(s15, 'Simulação Computacional', 'Comparação de Cenários What-If: O Deslocamento de Gargalo', 'Simulando a adição de catracas e buffets: o que acontece quando aceleramos a entrada?')

headers_sim = ['Cenário Simulado', 'F1 Espera (Wq1)', 'F1 Fila Pico', 'F2 Espera (Wq2)', 'F2 Fila Pico', 'Trânsito até Mesas', 'Diagnóstico Operacional']
rows_sim = [
    ['Baseline (1 Catraca, 1 Buffet)', '131,9 s', '51 alunos', '163,8 s', '25 alunos', '289,8 s (~4,8 min)', 'Equilibrado / Saturado'],
    ['Cenário 1: 2 Catracas (c1=2, c2=1)', '55,2 s (-58%)', '51 alunos', '238,1 s (+45%)', '48 alunos (+92%)', '289,3 s (~4,8 min)', 'Deslocamento de Gargalo'],
    ['Cenário 2: 2 Catracas + 2 Buffets', '55,2 s (-58%)', '51 alunos', '60,2 s (-63%)', '36 alunos', '106,7 s (~1,7 min)', 'Solução Ótima (-63% tempo)']
]
col_w_sim = [2.7, 1.4, 1.2, 1.4, 1.3, 1.7, 2.1]
add_table(s15, 0.75, 2.15, 11.8, 2.4, headers_sim, rows_sim, col_w_sim)

card_box(s15, 0.75, 4.85, 11.8, 2.0, LIGHT_BLUE, BLUE)
multi_text(s15, [
    ('EVIDÊNCIA CIENTÍFICA: BOTTLE-NECK SHIFTING (DESLOCAMENTO DE GARGALO)', 12, BLUE, True, 4),
    ('• No Cenário 1 (adicionar apenas a 2ª catraca): a fila externa desaba de 131,9s para 55,2s (-58%). Porém, a espera no buffet explode de 163,8s para 238,1s (+45%), acumulando 48 pessoas no corredor interno. Apenas transferiu-se a fila da calçada para dentro do restaurante!', 12, NAVY, False, 6),
    ('• No Cenário 2 (duplicar catraca E buffet): o sistema elimina o represamento. O tempo total até a mesa cai de quase 5 minutos para apenas 1,7 minuto (-63%). As mesas suportam o pico com 98 assentos ocupados (45% da capacidade de 216), sem bloquear ninguém!', 12, DARK, False, 0)
], 0.95, 5.0, 11.4, 1.7)

footer(s15, 15, 'Vanessa')


# ==============================================================================
# SLIDE 16: ADRIANA - CONCLUSÃO: QUANDO, QUANTO E POR QUÊ
# ==============================================================================
s16 = prs.slides.add_slide(prs.slide_layouts[6])
title_header(s16, 'Conclusão e Recomendações', 'Diagnóstico Operacional Final: Quando, Quanto e Por Quê', 'Resumo executivo com respostas precisas e recomendações acionáveis para a gestão do RU.')

qqp_cards = [
    ('QUANDO OCORRE O PROBLEMA?', 'Janela Crítica de Pico', 'A sobrecarga manifesta-se nos 20 minutos centrais do almoço (minutos 30 a 50 da coleta), quando a taxa de chegada atinge 3,8 alunos/minuto, e reaparece na onda dos 60 minutos.', BLUE),
    ('QUANTO É O IMPACTO REAL?', 'Filas de 51 Pessoas e 16 min', 'A fila da calçada acumulou até 51 alunos simultâneos. 10% dos estudantes (P90) esperaram mais de 9 minutos só na entrada. O tempo total médio de permanência no RU foi de ~29 minutos.', NAVY),
    ('POR QUÊ OCORRE O GARGALO?', 'Capacidade Incompatível', 'Porque com 1 catraca a capacidade técnica é μ = 3,32 p/min, resultando em utilização de pico ρ > 1,12. Além disso, as filas são acopladas: desafogar a entrada sem expandir o buffet sufoca o refeitório.', ORANGE)
]

for i, (kicker, tit, desc, c) in enumerate(qqp_cards):
    x = 0.75 + i * 4.0
    card_box(s16, x, 2.15, 3.8, 3.2, WHITE, BORDER)
    rect(s16, x, 2.15, 3.8, 0.12, c, False)
    multi_text(s16, [
        (kicker.upper(), 10, c, True, 4),
        (tit, 15, NAVY, True, 8),
        (desc, 12, DARK, False, 0)
    ], x + 0.22, 2.45, 3.35, 2.7)

card_box(s16, 0.75, 5.65, 11.8, 1.25, LIGHT, BORDER)
multi_text(s16, [
    ('RECOMENDAÇÃO ACIONÁVEL PARA A GESTÃO DO RU', 11, GREEN, True, 2),
    ('Adotar ativação combinada nos horários de pico (11h45 às 12h30): abrir a 2ª catraca de entrada em conjunto com a liberação de uma 2ª linha de distribuição no buffet. Como comprovado pela simulação, as 216 mesas absorvem esse fluxo com folga (54% de ocupação máxima), reduzindo o tempo de retenção do estudante em 63%.', 12, DARK, False, 0)
], 0.95, 5.75, 11.4, 1.05)

footer(s16, 16, 'Adriana')


# ==============================================================================
# SLIDE 17: ENCERRAMENTO E AGRADECIMENTOS
# ==============================================================================
s17 = prs.slides.add_slide(prs.slide_layouts[6])
rect(s17, 0, 0, 13.333, 7.5, NAVY, False)

multi_text(s17, [
    ('SEMINÁRIO DE AVALIAÇÃO DE DESEMPENHO', 14, RGBColor(176, 202, 240), True, 12),
    ('Obrigado pela Atenção!', 38, WHITE, True, 20),
    ('Equipe de Trabalho:', 14, RGBColor(176, 202, 240), True, 6),
    ('Adriana  •  Jaiane  •  Lucas  •  Otávio  •  Vanessa', 18, WHITE, True, 28),
    ('Sistema Fila RU disponível no repositório do projeto', 13, RGBColor(210, 226, 245), False, 4),
    ('Dados brutos, suíte de 203 testes e motor de simulação 100% reproduzíveis.', 12, RGBColor(176, 202, 240), False, 30),
    ('Abertos para Perguntas e Discussão', 16, RGBColor(234, 138, 34), True, 0)
], 1.5, 1.4, 10.3, 5.0, align=PP_ALIGN.CENTER)

footer(s17, 17)

# Metadados
prs.core_properties.title = 'Aferição, Modelagem e Simulação das Filas do RU'
prs.core_properties.subject = 'Apresentação do Trabalho de Avaliação de Desempenho'
prs.core_properties.author = 'Adriana, Jaiane, Lucas, Otávio, Vanessa'

prs.save(OUT)
print(f'Apresentação gerada com sucesso em: {OUT}')
