from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.chart.data import ChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION

OUT='/home/luizcaripuna/Documentos/AVALIAÇÃO DE DESEMPENHO/projeto-ru/divisao-trabalho/Afericao_Filas_RU_Seminario.pptx'
prs=Presentation(); prs.slide_width=Inches(13.333); prs.slide_height=Inches(7.5)

NAVY=RGBColor(22,38,58); BLUE=RGBColor(38,99,180); RED=RGBColor(204,63,63)
GREEN=RGBColor(38,143,94); PINK=RGBColor(203,98,132); WHITE=RGBColor(255,255,255)
LIGHT=RGBColor(242,246,250); DARK=RGBColor(43,51,62); ORANGE=RGBColor(232,145,54)
GRAY=RGBColor(105,115,125)


def rect(slide,x,y,w,h,color, radius=True):
    shp=slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE,Inches(x),Inches(y),Inches(w),Inches(h))
    shp.fill.solid(); shp.fill.fore_color.rgb=color
    shp.line.fill.background()
    return shp

def textbox(slide,text,x,y,w,h,size=20,color=DARK,bold=False,align=PP_ALIGN.LEFT,font='Aptos'):
    box=slide.shapes.add_textbox(Inches(x),Inches(y),Inches(w),Inches(h))
    tf=box.text_frame; tf.clear(); tf.word_wrap=True
    p=tf.paragraphs[0]; p.text=text; p.alignment=align
    r=p.runs[0]; r.font.name=font; r.font.size=Pt(size); r.font.bold=bold; r.font.color.rgb=color
    return box

def title(slide,kicker,heading,sub=None):
    textbox(slide,kicker.upper(),0.65,0.35,12,0.35,10,BLUE,bold=True)
    textbox(slide,heading,0.65,0.75,12.05,0.75,28,NAVY,bold=True)
    if sub: textbox(slide,sub,0.68,1.43,11.8,0.42,12,GRAY)

def base(kicker,heading,sub=None):
    slide=prs.slides.add_slide(prs.slide_layouts[6]); rect(slide,0,0,13.333,0.12,BLUE,False)
    title(slide,kicker,heading,sub)
    return slide

def footer(slide,n):
    textbox(slide,'Aferição das filas do RU • 04/11/2026',0.68,7.08,8,0.22,9,GRAY)
    textbox(slide,str(n),12.05,7.03,0.55,0.28,9,GRAY,bold=True,align=PP_ALIGN.RIGHT)

# 1 capa
slide=prs.slides.add_slide(prs.slide_layouts[6]); rect(slide,0,0,13.333,7.5,NAVY,False)
rect(slide,0.7,0.75,0.12,5.9,BLUE,False)
textbox(slide,'AVALIAÇÃO DE DESEMPENHO',0.95,1.05,8.8,0.45,15,RGBColor(176,202,240),bold=True)
textbox(slide,'Aferição das filas\ndo Restaurante Universitário',0.95,1.65,10.9,1.75,34,WHITE,bold=True)
textbox(slide,'Medição, modelagem M/M/c e simulação',0.95,3.55,9.8,0.55,20,RGBColor(210,220,232))
textbox(slide,'Equipe: Adriana • Jaiane • Lucas • Otávio • Vanessa',0.95,5.45,11,0.45,16,WHITE)
textbox(slide,'Coleta realizada em 04/11/2026 • 1 hora',0.95,6.05,9,0.35,12,RGBColor(176,202,240))

# 2 agenda
s=base('Visão geral','Objetivo e percurso da apresentação','Como transformamos observação de campo em evidência quantitativa.')
items=[('01','Contexto','Por que medir as filas do RU?'),('02','Aferição','O que medimos e como coletamos'),('03','Resultados','Chegadas, atendimentos e gargalo'),('04','Modelagem','Estado, capacidade e métricas'),('05','Simulação','Verificação, validação e cenários')]
for i,(n,h,b) in enumerate(items):
    x=0.7+i*2.48
    rect(s,x,2.15,2.15,3.25, LIGHT)
    textbox(s,n,x+0.18,2.38,1.7,0.45,17,BLUE,bold=True)
    textbox(s,h,x+0.18,3.05,1.75,0.55,16,NAVY,bold=True)
    textbox(s,b,x+0.18,3.85,1.75,1.15,12,GRAY)
footer(s,2)

# 3 contexto
s=base('Contexto','Três filas sequenciais no RU','A coleta seguiu o fluxo real da entrada até a saída.')
stages=[('FILA 1','Entrada → Catraca',RED,'202 chegadas'),('FILA 2','Catraca → Mesas',GREEN,'194 chegadas'),('FILA 3','Mesas → Saída',PINK,'185 chegadas')]
for i,(lab,sub,c,val) in enumerate(stages):
    x=0.75+i*4.15
    rect(s,x,2.1,3.65,2.8,c)
    textbox(s,lab,x+0.25,2.38,3.1,0.38,12,WHITE,bold=True)
    textbox(s,sub,x+0.25,3.02,3.1,0.55,18,WHITE,bold=True)
    textbox(s,val,x+0.25,4.05,3.1,0.35,13,WHITE)
textbox(s,'Pergunta central',0.75,5.35,2.1,0.35,12,BLUE,bold=True)
textbox(s,'Onde ocorre o gargalo e quanto a capacidade reduz a espera?',2.55,5.28,9.6,0.55,20,NAVY,bold=True)
footer(s,3)

# 4 method
s=base('Aferição','Método de coleta em campo','Aplicação web, celulares distribuídos e registro sincronizado.')
steps=[('1','Preparação','Rede local, PIN e celulares atribuídos às zonas'),('2','Coleta','Chegadas por minuto e passagens cronometradas'),('3','Registro','Evento, horário, fila, pessoa e dispositivo'),('4','Encerramento','Sessão de 65,34 min e exportação dos dados')]
for i,(n,h,b) in enumerate(steps):
    y=2.05+i*1.05
    rect(s,0.75,y,11.8,0.82,LIGHT)
    rect(s,0.95,y+0.13,0.55,0.55,BLUE)
    textbox(s,n,0.95,y+0.18,0.55,0.35,14,WHITE,bold=True,align=PP_ALIGN.CENTER)
    textbox(s,h,1.72,y+0.15,2.2,0.35,14,NAVY,bold=True)
    textbox(s,b,3.95,y+0.15,8.1,0.35,13,GRAY)
textbox(s,'Divisão prática',0.75,6.55,2.0,0.3,11,BLUE,bold=True)
textbox(s,'2 pessoas na entrada • 1 no atendimento • 1 na saída',2.55,6.48,8.8,0.35,15,DARK,bold=True)
footer(s,4)

# 5 team
s=base('Equipe','Divisão de trabalho','Responsabilidades alinhadas à estrutura do seminário.')
team=[('Adriana','Introdução e conclusão','Coordenação'),('Lucas','Aferição — método','Dados e demonstração'),('Jaiane','Aferição — resultados','Cálculo de λ e μ'),('Otávio','Modelagem','Estado, K, matriz P e fórmulas'),('Vanessa','Simulação','Verificação, validação e cenários')]
for i,(name,role,task) in enumerate(team):
    x=0.7+i*2.48
    rect(s,x,2.05,2.18,3.85,LIGHT)
    rect(s,x,2.05,2.18,0.12,[BLUE,RED,GREEN,ORANGE,PINK][i],False)
    textbox(s,name,x+0.18,2.42,1.82,0.45,17,NAVY,bold=True)
    textbox(s,role,x+0.18,3.12,1.82,0.85,13,DARK,bold=True)
    textbox(s,task,x+0.18,4.45,1.82,0.85,11,GRAY)
footer(s,5)

# 6 results overview
s=base('Resultados','Resumo da sessão observada','Uma hora de coleta revelou capacidade próxima ou abaixo da demanda em todas as filas.')
metrics=[('202','chegadas','Fila 1',RED),('194','chegadas','Fila 2',GREEN),('185','chegadas','Fila 3',PINK),('65,34','minutos','duração',BLUE)]
for i,(v,lab,sub,c) in enumerate(metrics):
    x=0.75+i*3.03
    rect(s,x,2.15,2.72,2.05,c)
    textbox(s,v,x+0.18,2.55,2.35,0.65,29,WHITE,bold=True,align=PP_ALIGN.CENTER)
    textbox(s,lab,x+0.18,3.25,2.35,0.38,12,WHITE,align=PP_ALIGN.CENTER)
    textbox(s,sub,x+0.18,3.72,2.35,0.28,10,WHITE,align=PP_ALIGN.CENTER)
textbox(s,'Indicador crítico',0.75,4.75,2.1,0.35,11,RED,bold=True)
textbox(s,'F1: ρ = 1,041  •  F2: ρ = 1,049  •  F3: ρ = 1,947',2.55,4.68,9.7,0.55,22,NAVY,bold=True)
textbox(s,'ρ > 1 indica que a chegada supera a capacidade média observada.',2.55,5.35,9.4,0.45,14,GRAY)
footer(s,6)

# 7 table by fila
s=base('Aferição','Chegadas, atendimentos e taxas por fila','Taxas calculadas sobre a duração efetiva da sessão.')
# header
cols=[0.75,3.05,5.25,7.45,9.65,11.55]; widths=[2.3,2.2,2.2,2.2,1.9]
headers=['Fila','Chegadas','Atendimentos','λ (p/min)','μ (p/min)','ρ']
for i,h in enumerate(headers):
    x=[0.75,3.15,5.25,7.35,9.45,11.55][i]
    rect(s,x,2.05,1.95 if i else 2.25,0.58,NAVY,False)
    textbox(s,h,x+0.08,2.20,1.8 if i else 2.1,0.25,11,WHITE,bold=True,align=PP_ALIGN.CENTER)
rows=[('F1 — Entrada',202,194,'3,092','2,969','1,041',RED),('F2 — Atendimento',194,185,'2,969','2,831','1,049',GREEN),('F3 — Saída',185,95,'2,831','1,454','1,947',PINK)]
for r,(fila,ch,att,lam,mu,rho,c) in enumerate(rows):
    y=2.75+r*0.95
    vals=[fila,str(ch),str(att),lam,mu,rho]
    for i,v in enumerate(vals):
        x=[0.75,3.15,5.25,7.35,9.45,11.55][i]
        rect(s,x,y,1.95 if i else 2.25,0.70,WHITE,False)
        textbox(s,v,x+0.08,y+0.18,1.8 if i else 2.1,0.28,14,c if i==5 else NAVY,bold=(i in [0,5]),align=PP_ALIGN.CENTER)
textbox(s,'Leitura',0.75,5.85,1.25,0.35,11,BLUE,bold=True)
textbox(s,'A Fila 3 apresenta a maior pressão relativa: 185 entradas, mas apenas 95 passagens registradas.',2.05,5.78,10.25,0.55,17,NAVY,bold=True)
footer(s,7)

# 8 5min chart
s=base('Aferição','Comportamento por blocos de cinco minutos','Chegadas observadas em cada período da sessão.')
labels=['0–5','5–10','10–15','15–20','20–25','25–30','30–35','35–40','40–45','45–50','50–55','55–60','60–65']
f1=[39,2,12,8,9,11,17,19,19,19,11,15,19] # corrected as recorded block metrics aggregate; indices 0 only block 39 and 19 in 60-65
# replace based on actual blocks output: 39,2,12,8,9,11,17,19,19,19,11,15,2
f1=[39,2,12,8,9,11,17,19,19,19,11,15,2]
f2=[0,0,12,28,29,6,20,18,19,18,13,14,15]
f3=[0,0,1,19,23,18,22,21,20,18,18,14,11]
cd=ChartData(); cd.categories=labels
cd.add_series('Fila 1',f1); cd.add_series('Fila 2',f2); cd.add_series('Fila 3',f3)
chart=s.shapes.add_chart(XL_CHART_TYPE.LINE,Inches(0.75),Inches(2.05),Inches(11.85),Inches(4.45),cd).chart
chart.has_legend=True; chart.legend.position=XL_LEGEND_POSITION.BOTTOM; chart.legend.include_in_layout=False
chart.value_axis.minimum_scale=0; chart.value_axis.maximum_scale=45; chart.value_axis.has_major_gridlines=True
chart.category_axis.has_title=False
series=chart.series
series[0].format.line.color.rgb=RED; series[1].format.line.color.rgb=GREEN; series[2].format.line.color.rgb=PINK
for ser in series: ser.format.line.width=Pt(2.25)
footer(s,8)

# 9 model
s=base('Modelagem','Modelo M/M/c aplicado às três filas','O estado observado é representado por chegadas, atendimento e capacidade finita.')
# formulas cards
cards=[('Estado','N(t) = número de pessoas na fila','Passagem entre estados a cada evento'),('Passo','Δt = 5 minutos','Agregação por blocos'),('Capacidade','K = 216 lugares no salão','Limite físico da ocupação'),('Métricas','ρ = λ/(cμ); L = λW','Wq = Lq/λ')]
for i,(h,a,b) in enumerate(cards):
    x=0.75+i*3.03
    rect(s,x,2.1,2.72,2.15,LIGHT)
    textbox(s,h,x+0.18,2.38,2.35,0.35,14,BLUE,bold=True)
    textbox(s,a,x+0.18,3.05,2.35,0.42,16,NAVY,bold=True)
    textbox(s,b,x+0.18,3.67,2.35,0.4,11,GRAY)
textbox(s,'Uso na prática',0.75,4.75,1.8,0.35,11,BLUE,bold=True)
textbox(s,'A matriz de probabilidades e o estado devem reproduzir',2.45,4.68,9.7,0.35,16,DARK)
textbox(s,'chegadas • filas • atendimentos • saída',2.45,5.15,9.7,0.45,22,NAVY,bold=True)
textbox(s,'Quando a simulação mantém o padrão observado, ela passa de descrição para previsão.',2.45,5.78,9.7,0.48,14,GRAY)
footer(s,9)

# 10 simulation
s=base('Simulação','Cenários e teste de capacidade','Mudança controlada: variar uma coisa por vez.')
# baseline and scenario
rect(s,0.75,2.05,3.7,3.95,LIGHT); textbox(s,'CENÁRIO BASE',1.05,2.35,3.1,0.35,13,BLUE,bold=True)
textbox(s,'1 servidor por fila',1.05,3.05,3.1,0.45,24,NAVY,bold=True)
textbox(s,'Fila 1: ρ = 1,041\nFila 2: ρ = 1,049\nFila 3: ρ = 1,947',1.05,3.75,3.1,1.55,16,DARK)
rect(s,4.75,2.05,3.7,3.95,RGBColor(236,244,255)); textbox(s,'CENÁRIO DE TESTE',5.05,2.35,3.1,0.35,13,BLUE,bold=True)
textbox(s,'2 servidores na Fila 1',5.05,3.05,3.1,0.45,24,NAVY,bold=True)
textbox(s,'Objetivo: reduzir a pressão\nde entrada e liberar a Fila 2',5.05,3.85,3.1,1.45,16,DARK)
textbox(s,'Próximo teste',8.85,2.05,3.1,0.35,13,BLUE,bold=True)
rect(s,8.75,2.55,3.55,3.45,WHITE)
textbox(s,'2 servidores na Fila 2',9.05,3.05,2.95,0.45,20,NAVY,bold=True)
textbox(s,'Mudança isolada\npara identificar o\ngargalo real',9.05,3.75,2.95,1.35,16,GRAY)
footer(s,10)

# 11 validation
s=base('Simulação','Verificação e validação','A qualidade da simulação depende de comparar o modelo com a fila anotada.')
checks=[('Verificação','O resultado da simulação respeita as fórmulas do modelo?'),('Validação','A curva simulada acompanha chegadas e filas observadas?'),('Comparação','Mudou o cenário sem alterar outros parâmetros?')]
for i,(h,b) in enumerate(checks):
    y=2.05+i*1.25
    rect(s,0.75,y,11.85,1.05,LIGHT)
    textbox(s,h,1.02,y+0.25,2.05,0.38,16,BLUE,bold=True)
    textbox(s,b,3.15,y+0.22,8.95,0.48,16,NAVY,bold=True)
textbox(s,'Critério esperado',0.75,6.25,2.0,0.28,11,BLUE,bold=True)
textbox(s,'Mesmo λ observado • mesma distribuição de serviço • menor fila após aumentar capacidade',2.55,6.18,10,0.38,14,DARK,bold=True)
footer(s,11)

# 12 conclusion
s=base('Conclusão','O que, quando, quanto e por quê','Síntese pronta para a apresentação final.')
rect(s,0.75,2.05,11.85,3.95,NAVY)
textbox(s,'QUANDO',1.05,2.48,2.0,0.35,12,RGBColor(176,202,240),bold=True)
textbox(s,'04/11/2026 • período aferido de 65,34 min',3.05,2.40,8.85,0.48,18,WHITE,bold=True)
textbox(s,'QUANTO',1.05,3.38,2.0,0.35,12,RGBColor(176,202,240),bold=True)
textbox(s,'202 chegadas na F1 • 194 passagens na F2 • 95 passagens na F3',3.05,3.30,8.85,0.48,18,WHITE,bold=True)
textbox(s,'POR QUÊ',1.05,4.28,2.0,0.35,12,RGBColor(176,202,240),bold=True)
textbox(s,'A capacidade observada ficou abaixo da demanda: ρ indica sobrecarga, especialmente na saída.',3.05,4.18,8.85,0.72,18,WHITE,bold=True)
textbox(s,'Gargalo provável: Fila 3 / saída — confirmar no painel detalhado e no cenário com maior capacidade.',1.05,5.42,11.0,0.42,14,RGBColor(210,220,232),bold=True)
footer(s,12)

# 13 thanks
s=prs.slides.add_slide(prs.slide_layouts[6]); rect(s,0,0,13.333,7.5,NAVY,False)
textbox(s,'PERGUNTAS',0.95,1.25,11.5,0.55,16,RGBColor(176,202,240),bold=True,align=PP_ALIGN.CENTER)
textbox(s,'Obrigado!',0.95,2.15,11.5,0.9,42,WHITE,bold=True,align=PP_ALIGN.CENTER)
textbox(s,'Adriana • Jaiane • Lucas • Otávio • Vanessa',0.95,4.05,11.5,0.45,16,WHITE,align=PP_ALIGN.CENTER)
textbox(s,'Aferição das filas do RU',0.95,5.05,11.5,0.35,13,RGBColor(176,202,240),align=PP_ALIGN.CENTER)

# Document properties
prs.core_properties.title='Aferição das filas do RU'
prs.core_properties.subject='Apresentação do seminário'
prs.core_properties.author='Equipe: Adriana, Jaiane, Lucas, Otávio e Vanessa'
prs.save(OUT)
print(OUT)
