"""Original engineering review sheets; reportlab PDF + actual CAD mesh view. CERN-OHL-S-2.0."""
from pathlib import Path
import json,hashlib,math,re
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgb
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A3,landscape
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor,Color
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph,Table,TableStyle
from reportlab.lib.styles import ParagraphStyle
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/consolidated-v32';P=R/'output/pdf';P.mkdir(parents=True,exist_ok=True)
r=json.loads((O/'validation.json').read_text());assert all(v['pass'] for v in r['checks']);c=r['config'];mesh=json.loads((O/'mesh.json').read_text())
for p,h in r['source_hashes'].items():assert hashlib.sha256((R/p).read_bytes()).hexdigest()==h
# Draw directly from saved mesh; hide front/left/glass/display to expose inside.
fig=plt.figure(figsize=(14,8),facecolor='#f3f5f7');ax=fig.add_subplot(111,projection='3d');ax.set_facecolor('#f3f5f7')
hidden={'SIDE_L','FRONT','PLAYFIELD_ENVELOPE','CandidateGlass','SHELF_1_CandidatePayload','SHELF_1','SHELF_2','SHELF_3'}
all_faces=[];all_colors=[]
for item in mesh:
 n=item['name']
 if n in hidden or n.startswith('CoinStudy_') or n.startswith('CandidateFrontButton') or n=='PLUNGER_RESERVED':continue
 vs=np.array(item['vertices']);faces=vs[np.array(item['faces'])]
 col='#cbb48e'
 if n.startswith('SSF_'):col='#d37d43' if 'Exciter' in n or 'BST' in n else '#326d92'
 elif n.startswith('PC_'):col='#5b8670'
 elif 'Fan' in n or n.startswith('FAN_'):col='#597184'
 elif 'GlassChannel' in n or 'MONITOR' in n:col='#75818d'
 elif 'Bolt' in n or 'Screw' in n or 'Hinge' in n or 'Lock' in n or 'Washer' in n:col='#71808b'
 elif n.startswith('SHELF_'):col='#d8bc8b'
 elif 'Enclosure' in n:col='#d6dce0'
 normals=np.cross(faces[:,1]-faces[:,0],faces[:,2]-faces[:,0]);normalizer=np.maximum(np.linalg.norm(normals,axis=1),1e-10);normals/=normalizer[:,None];light=.58+.42*np.abs(normals@np.array([.4,-.4,.824]));colors=np.clip(np.array(to_rgb(col))[None,:]*light[:,None],0,1)
 all_faces.extend(faces);all_colors.extend(colors)
ax.add_collection3d(Poly3DCollection(all_faces,facecolors=all_colors,edgecolors='none',linewidths=0,zsort='average'))
ax.set(xlim=(-30,630),ylim=(-30,1350),zlim=(0,650));ax.set_box_aspect((660,1380,650));ax.view_init(elev=35,azim=-135);ax.set_axis_off();fig.subplots_adjust(0,0,1,1);fig.savefig(O/'01-consolidated-interior.png',dpi=160,bbox_inches='tight',facecolor=fig.get_facecolor());plt.close(fig)
# PDF drawing primitives in page millimetres, all model dimensions in mm.
pdfmetrics.registerFont(TTFont('Body','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'));pdfmetrics.registerFont(TTFont('Bold','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
C=canvas.Canvas(str(P/'v32-desenho-consolidado.pdf'),pagesize=landscape(A3));C.setTitle('V32 - Desenho consolidado do gabinete e SSF Cleveland4.1');C.setAuthor('vpin-cabinet / CERN-OHL-S-2.0')
ink='#233b4a';muted='#536877';wood='#eadbc0';blue='#467b98';orange='#d1874a';green='#6d9278';page=0
style=ParagraphStyle('body',fontName='Body',fontSize=10,leading=15,textColor=HexColor(ink));smallstyle=ParagraphStyle('small',fontName='Body',fontSize=8.5,leading=12,textColor=HexColor(ink))
def readable(t):
 t=re.sub(r'(?<=[a-zà-ÿ])(?=[0-9A-ZØ])',' ',str(t));return re.sub(r'(?<=[0-9])(?=[a-zà-ÿ])',' ',t)
def text(x,y,t,size=10,bold=False,color=ink):
 t=readable(t)
 C.setFont('Bold' if bold else 'Body',size);C.setFillColor(HexColor(color));C.drawString(x*mm,y*mm,t)
def para(x,top,w,t,small=False):
 obj=Paragraph(readable(t),smallstyle if small else style);ww,hh=obj.wrap(w*mm,230*mm);obj.drawOn(C,x*mm,top*mm-hh);return top-hh/mm

def rect(x,y,w,h,fill=None,stroke=ink,dash=False):
 C.setStrokeColor(HexColor(stroke));C.setLineWidth(.25*mm);C.setDash(2*mm,1*mm) if dash else C.setDash()
 if fill:C.setFillColor(HexColor(fill))
 C.rect(x*mm,y*mm,w*mm,h*mm,stroke=1,fill=int(fill is not None));C.setDash()
def line(x1,y1,x2,y2,col=ink,width=.25):
 C.setStrokeColor(HexColor(col));C.setLineWidth(width*mm);C.line(x1*mm,y1*mm,x2*mm,y2*mm)
def circle(x,y,rad,fill=None,stroke=ink):
 C.setStrokeColor(HexColor(stroke));C.setLineWidth(.2*mm)
 if fill:C.setFillColor(HexColor(fill))
 C.circle(x*mm,y*mm,rad*mm,stroke=1,fill=int(fill is not None))
def table(x,top,width,rows,colwidths=None):
 data=[[Paragraph(readable(v),smallstyle) for v in row] for row in rows];t=Table(data,colWidths=[v*mm for v in colwidths] if colwidths else [width*mm/len(rows[0])]*len(rows[0]));t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),HexColor('#e3ebef')),('GRID',(0,0),(-1,-1),.3,HexColor('#b8c6cf')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]));w,h=t.wrap(width*mm,250*mm);t.drawOn(C,x*mm,top*mm-h);return top-h/mm

def start(title,sub):
 global page
 if page:C.showPage()
 page+=1;C.setFillColor(HexColor('#fafbfc'));C.rect(0,0,420*mm,297*mm,fill=1,stroke=0)
 text(15,282,'VPIN / V32',11,True,blue);text(15,267,title,21,True);text(15,257,sub,9,color=muted)
 rect(312,279,93,9,fill='#f4e2ce',stroke='#f4e2ce');text(317,282,'REVISÃO CONSOLIDADA • CNC PENDENTE',8,True,'#87542b')
 line(15,249,405,249,'#bdccd5');line(15,18,405,18,'#bdccd5');text(15,11,'CERN-OHL-S-2.0 | github.com/advpeterrobinson-hash/vpin-cabinet | 30/09/2026',7,color=muted);text(360,11,f'V32-CSD / {page:02d}',8,True)

def dimh(x1,x2,y,label):
 line(x1,y,x2,y);line(x1,y-2,x1,y+2);line(x2,y-2,x2,y+2);text((x1+x2)/2-12,y+2,label,8)
def dimv(x,y1,y2,label):
 line(x,y1,x,y2);line(x-2,y1,x+2,y1);line(x-2,y2,x+2,y2);C.saveState();C.translate((x-2)*mm,((y1+y2)/2)*mm);C.rotate(90);C.setFont('Body',8);C.drawCentredString(0,0,label);C.restoreState()
#1
start('Gabinete consolidado + SSF Cleveland 4.1','Desenho de referência de montagem do corpo principal. Reservas de componentes identificadas; sem liberação de corte.')
C.drawImage(str(O/'01-consolidated-interior.png'),13*mm,57*mm,width=275*mm,height=181*mm,preserveAspectRatio=True,anchor='c')
text(287,236,'DECISÕES PRESERVADAS',12,True)
y=para(287,226,116,'Corpo de <b>600 mm</b>; PC baixo; três prateleiras com quatro parafusos acessíveis por cima; porta traseira com chave e abertura para baixo. Fans e conectores fixos.')
y=para(287,y-8,116,'<b>Áudio de referência:</b> quatro EX32EP2-4 nas laterais, um BST-1 e subwoofer DCS165-4 separado. Amplificador na S2 e fonte na S3. Suporte local do shaker desacoplado das prateleiras estruturalmente.')
y=para(287,y-8,116,'A vista usa o CAD salvo. Frente, lateral esquerda, prateleiras, vidro e envelope do display foram ocultados apenas nesta vista para mostrar os componentes abaixo deles.',True)
text(22,46,'Madeira',9,True);rect(15,45,4,4,wood);text(76,46,'SSF / shaker',9,True);rect(69,45,4,4,orange);text(143,46,'Áudio / subwoofer',9,True);rect(136,45,4,4,blue);text(225,46,'PC baixo',9,True);rect(218,45,4,4,green)
para(15,34,390,'<b>Escopo:</b> consolidação do corpo, piso e reservas SSF. Ferragens reais, receptor/barra metálica, escoras e dobradiça do playfield, cargas, montagem elétrica e CAM ainda exigem fechamento. Este PDF não certifica o gabinete para fabricar.',True)
#2 floor
start('Piso: ventilação, subwoofer e shaker','Vista superior. X = esquerda-direita vista de frente; Y = frente-traseira. Dimensões em mm; geometria nominal.')
ox,oy,sc=27,38,.15
Pxy=lambda x,y:(ox+x*sc,oy+y*sc)
rect(*Pxy(18,18),564*sc,1272.1*sc,wood)
for x,y,w,h in [[100,630,100,160],[400,630,100,160]]:
 X,Y=Pxy(x,y);C.setFillColor(HexColor('#d6e5ec'));C.setStrokeColor(HexColor(blue));C.roundRect(X*mm,Y*mm,w*sc*mm,h*sc*mm,3*sc*mm,stroke=1,fill=1)
 rect(*Pxy(x-15,y-15),130*sc,190*sc,None,blue,True)
circle(*Pxy(300,440),143.5/2*sc,'#ffffff');circle(*Pxy(300,440),83.5*sc,None,blue)
rect(*Pxy(210,170),180*sc,180*sc,'#f4d8bb',orange);circle(*Pxy(300,260),80.5*sc,None,orange)
rect(*Pxy(157.5,830),285*sc,460*sc,'#d8e4da',green)
for op in r['floor_operations']:
 if op['operation']!='through_cut':circle(*Pxy(*op['center_xy_mm']),op['diameter_mm']/2*sc,ink)
fc=json.loads((R/'config/floor_detail_v32.json').read_text())
for x,y in fc['filter_fixing_centers_xy_mm']:circle(*Pxy(x,y),2.25*sc,ink)
text(51,61,'BST-1',8,True);text(40,109,'DCS165-4',8,True);text(52,197,'PCBase',8,True)
text(43,29,'FRENTE / Y0',8,True);text(39,238,'TRASEIRA',8,True)
dimh(*[Pxy(18,0)[0],Pxy(582,0)[0]],35,'564');dimv(20,Pxy(0,18)[1],Pxy(0,1290.1)[1],'1272,1')
y=table(139,239,263,[['Item','Posição / dimensão','Montagem'],['Subwoofer','Centro X300/Y440; corte Ø143,5; PCD Ø158, 8 furosØ5,5','DCS165-4 como referência. Flange sobre face interna do piso; emissão para baixo.'],['BST-1','Centro X300/Y260; placa180×180×12','Quatro âncorasM5 candidatas. Furação da peça na placa local ainda depende da revisão física.'],['Filtros','Duas janelas100×160R3; molduras130×190×8','Quatro pontos por filtro; retirada por baixo. Meio filtrante a selecionar.'],['PCBase','285×460×18; X157,5/Y830; baseZ36','Quatro passagensØ5,5 e escareadoØ10,5×2,5 na base. Chassi sai antes do acesso superior.']],colwidths=[35,110,118])
para(139,y-8,263,'O corte do subwoofer passa de139,7 para143,5 mm:143 é a referência do desenho e0,5 é folga proposta. Furos do driver e das âncoras são nominais; o encaixe e a resistência precisam de conferência. Não há quatro furos auxiliares sem função no piso.',True)
para(139,y-31,263,'<b>Alturas:</b> pisoZ18..36; suporte do shakerZ36..48; BST-1 reservado atéZ113; subwoofer atéZ146 com folga de serviço. Corpo acústico do gabinete não foi calculado como caixa selada/sintonizada.',True)
#3 rear
start('Traseira: acesso e conexões fixas','Vista externa correta: o X global cresce para a esquerda nesta prancha. Porta não transporta fans ou cabos.')
ox,oy,sc=28,40,.31
Rz=lambda x,z:(ox+(600-x)*sc,oy+z*sc)
rect(ox,oy,600*sc,596.9*sc,wood)
rect(*Rz(498,54),396*sc,329*sc,'#f3e4ca')
for x in (230,370):
 rect(*Rz(x+60,440),120*sc,120*sc,'#dce7ed',blue);circle(*Rz(x,500),58*sc,None,blue)
 for dx in (-52.5,52.5):
  for dz in (-52.5,52.5):circle(*Rz(x+dx,500+dz),2.25*sc,ink)
X,Y=Rz(109,406);C.setFillColor(HexColor('#ffffff'));C.roundRect(X*mm,Y*mm,28*sc*mm,48*sc*mm,3*sc*mm,stroke=1,fill=1)
for x in (75,115):circle(*Rz(x,430),2.25*sc,ink)
circle(*Rz(530,430),12*sc,'#ffffff')
for x,z in [(539.5,442),(520.5,418)]:circle(*Rz(x,z),1.6*sc,ink)
circle(*Rz(450,350),11.5*sc,'#d0ad5c');rect(*Rz(338,184),76*sc,12*sc,'#697e88')
for x in (180,372):rect(*Rz(x+48,24),48*sc,60*sc,'#91a2aa')
dimh(ox,ox+600*sc,34,'600');dimv(22,oy,oy+596.9*sc,'596,9')
y=table(236,239,166,[['Interface','Cota / condição'],['Porta','396×329×12; abertura340×293. A110° a rota excepcional do PC passa; a90° a fechadura obstrui.'],['Fans','2×120; centros X230/370,Z500. CorteØ116; furosØ4,5 no passo105 mm; 57 mm acima da porta.'],['Energia','X95/Z430;28×48R3; doisØ4,5 a40.'],['Ethernet','X530/Z430;Ø24 candidato; doisØ3,2 a19×24.'],['Fechadura','X450/Z350; recorteØ19 limitado a17 entre faces, candidato.'],['Dobradiças','EixoY1324,1/Z54. Duas peças; pilotos na madeira e ferragens finais ainda pendentes.']],colwidths=[35,131])
para(236,y-7,166,'Limitadores opcionais. Feltro no contato real protege a pintura. Não tratar a porta aberta como bancada. Proteção interna da energia deve permitir acesso às porcas.',True)
#4 side
start('Laterais: SSF e alturas preservadas','Projeção lateral transparente das reservas. Não é gabarito de furação do suporte IMS nem seção única do gabinete.')
ox,oy,sc=25,79,.27
Lz=lambda y,z:(ox+y*sc,oy+z*sc)
pts=[Lz(0,0),Lz(1308.1,0),Lz(1308.1,596.9),Lz(1127.125,596.9),Lz(0,400.05)]
pth=C.beginPath();pth.moveTo(pts[0][0]*mm,pts[0][1]*mm)
for x,y in pts[1:]:pth.lineTo(x*mm,y*mm)
pth.close();C.setFillColor(HexColor(wood));C.setStrokeColor(HexColor(ink));C.drawPath(pth,stroke=1,fill=1)
for i,(y,z) in enumerate([(120,160),(565,180),(865,240)],1):rect(*Lz(y,z),150*sc,12*sc,'#c4a66e');text(*Lz(y,z+30),f'S{i} / topo{z+12}',8,True)
for y,z in c['exciters']['positions_yz_mm']:
 circle(*Lz(y,z),40*sc,'#f4d8bb',orange);text(*Lz(y-45,z+55),f'SSF Y{y}/Z{z}',8,True)
for y in (255,310):circle(*Lz(y,270),7.9375*sc,None,ink)
rect(*Lz(830,36),460*sc,18*sc,'#93b2a0');rect(*Lz(840,54),440*sc,128*sc,'#d2e1d6',green)
rect(*Lz(170,36),180*sc,12*sc,'#ddb087');rect(*Lz(179.5,48),161*sc,62*sc,'#f4d8bb',orange)
rect(*Lz(356.5,36),167*sc,90*sc,'#bad2df',blue)
for y,z in [(380,283.691),(700,339.579),(980,388.480)]:rect(*Lz(y-30,z-45),60*sc,145*sc,None,'#71808b',True)
dimh(ox,ox+1308.1*sc,72,'1308,1');dimv(18,oy,oy+400.05*sc,'400,05')
para(25,59,175,'Quatro exciters: dois por lateral, simétricos. Reserva de serviçoØ80×45 para dentro; acoplamento direto pelo IMS. Sem travessa nova unindo paredes. PilotosIMS aguardam peça real.',True)
para(220,59,175,'Prateleiras mantidas: Y120/565/865, altura inferior160/180/240. Guias: R3 ensaiado em estudo separado; dogbones não necessários nos fins25mm abaixo das travessas atuais.',True)
#5 audio
start('Áudio: referência Cleveland 4.1 + subwoofer','Organização funcional de baixa tensão. Não é diagrama de rede elétrica ou instrução de ligação de terminais.')
rect(20,184,72,37,'#d8e4da',green);text(29,204,'PC / USB7.1',12,True);para(27,196,60,'Conferir mapeamento real da placa de som.',True)
rect(124,164,100,76,'#dce7ed',blue);text(136,222,'Amplificador SSF',12,True);para(132,214,85,'Reserva na S2:<br/>240×120×60<br/>X180/Y580/Z202<br/><br/>Acesso frontal aos controles; conectores para retirada da prateleira.',True)
line(92,203,124,203,blue,.6)
for y,label,col in [(222,'4 exciters nas laterais',orange),(191,'1 BST-1 no piso',orange),(160,'Subwoofer + áudio do backbox',blue)]:
 line(224,203,249,203,blue,.5);line(249,203,249,y,blue,.5);line(249,y,273,y,blue,.5);rect(273,y-11,126,23,'#edf2f5',col);text(280,y-2,label,11,True,col)
rect(20,112,72,43,'#edf2f5');para(26,146,61,'<b>Fonte protegida na S3</b><br/>Reserva220×110×50<br/>X190/Y885/Z262',True)
rect(124,111,100,35,'#edf2f5');para(131,139,84,'<b>InterfaceUSB na S2</b><br/>Reserva80×60×25<br/>X80/Y600/Z202',True)
y=para(20,91,188,'<b>Kit4.1 não significa quatro exciters mais subwoofer acústico.</b> A Cleveland lista quatro exciters e um bass shaker; o DCS165-4 é adicional. São seis transdutores no corpo, além dos alto-falantes do backbox.')
para(228,109,170,'<b>Rotas propostas:</b> cabos SSF nas laterais abaixo das prateleiras, fixos e afastados de partes móveis; desconexão na prateleira antes de removê-la. Cabos de potência protegidos e separados dos sinais conforme a instalação elétrica final.<br/><br/>Amp/fonte são envelopes de projeto, não dimensões verificadas do kit. O PDF não presume suporte Bluetooth nem fornece pinagem elétrica.',True)
text(20,33,'Fontes: Cleveland High Power SSF Kit e guia oficial de instalação. Links completos na biblioteca do projeto.',8,color=muted)
#6 holecoords
start('Furação do piso: mapa de referência','Coordenadas globais X/Y em mm. Não substituir espessura medida, cupom e conferência da revisão das peças.')
subrows=[['Subwoofer / Ø5,5','X','Y']]
for i,op in enumerate([x for x in r['floor_operations'] if x['status']=='candidate_M5_on_reference_PCD'],1):subrows.append([str(i),f'{op["center_xy_mm"][0]:.3f}',f'{op["center_xy_mm"][1]:.3f}'])
y=table(20,239,117,subrows,[57,30,30]);para(20,y-8,117,'PCDØ158; fase22,5° adotada para distribuição simétrica. Ajustar a orientação do driver à furação depois da conferência da peça.',True)
rows=[['SuporteBST / Ø5,5','X','Y']]+[[str(i),str(x),str(y)] for i,(x,y) in enumerate(c['bass_shaker']['floor_anchor_holes_xy_mm'],1)]
y=table(151,239,117,rows,[57,30,30]);rows=[['BasePC / Ø5,5','X','Y']]+[[str(i),str(x),str(y)] for i,(x,y) in enumerate(c['pc_base']['anchor_holes_xy_mm'],1)];y=table(151,y-9,117,rows,[57,30,30]);para(151,y-7,117,'EscareadoØ10,5×2,5 somente na face superior da PCBase. Piso recebe apenas a passagem. Não escarear o piso por esta prancha.',True)
rows=[['Filtros / Ø4,5','X','Y']]+[[str(i),str(x),str(y)] for i,(x,y) in enumerate(fc['filter_fixing_centers_xy_mm'],1)];y=table(282,239,117,rows,[57,30,30]);para(282,y-8,117,'Molduras inferiores130×190×8. Diâmetros candidatosM4; meio filtrante e ferragens precisam corresponder ao conjunto real.',True)
para(20,57,379,'<b>DXF incluído:</b> floor-draft-mm.dxf, gerado das arestas da face plana do piso no CAD. CamadasFLOOR_THROUGH eDRILL_THROUGH; unidade mm, sem compensação. Não contém pilotos laterais/faceados, aninhamento de chapas, estratégia de corte ou aprovação de fabricação.',True)
#7 assembly
start('Montagem e manutenção','Sequência de referência para montar com ferramentas comuns e preservar a desmontagem dos componentes.')
rows=[['Etapa','Ação','Condição de acesso'],['1','Conferir estoque e cupom; instalar suportes estruturais e ferragens de canto.','União capturada da caixa e ferragens de pernas continuam em qualificação; não colar fechamentos sobre pontos de serviço.'],['2','Instalar subwoofer e placa localBST no piso; depois o shaker.','Subwoofer por dentro, emissão para baixo. Shaker usa placa rígida local; furos do próprioBST ficam nela.'],['3','Montar filtro por baixo e base baixa do PC.','Acesso aos quatro pontos por filtro; proteção inferior do cone/grille a confirmar. Cabeças daPCBase ficam rasantes.'],['4','Montar prateleiras; amp eUSB naS2, fonte naS3.','Preservar os quatro parafusos superiores de cada prateleira e os corredores de retirada já estudados.'],['5','Fixar quatro exciters pelas montagensIMS e organizar cabos.','Conferir face de contato, rotação para remoção e fios; não instalar espuma desacopladora sob o mount sem especificação.'],['6','Concluir proteção elétrica, fixações do chassi, vidro e playfield.','O conjunto de escoras e pivô do playfield precisa de retenção positiva e prova de carga antes de serviço com tela elevada.']],
y=table(20,239,379,rows[0],[17,167,195])
para(20,y-10,180,'<b>Serviço do BST-1:</b> removerS1 e desconectar fios antes de levantar o conjunto local. O teste rejeita retirada vertical comS1 instalada. Subwoofer tem corredor vertical de150mm verificado contra os sólidos modelados.',True)
para(217,y-10,182,'<b>Serviço do PC:</b> não há gaveta. Para acessar as cabeças daPCBase, retirar o chassi primeiro. Preservar a rota traseira existente com porta a110°; não presumir retirada do conjunto com todas as novas âncoras presas.',True)
#8 limits & source
start('Estado da entrega e rastreabilidade','O desenho está consolidado para revisão. A fabricação continua condicionada às confirmações abaixo.')
rows=[['Fechado nesta entrega','Confirmação necessária antes da fabricação'],['Layout do corpo600mm; prateleiras; PC baixo; traseira funcional.','Ferragens reais de dobradiças, fechadura/batente, pernas e fixadores.'],['Piso comR3, filtros, suporteBST e interfaceDCS165-4.','Espessura/fresa/folgas, resistência do piso, cupom, revisão do driver e retenção de filtros.'],['Quatro reservas de exciters e amp/fonte/USB.','MountsIMS, furos doBST na placa local, dimensões reais do amp/fonte, rotação/cabos e resultado acústico.'],['Barra customizada600 e eixos candidatos do receptor documentados.','Perfil metálico, linguetas e receptor reais: não háDXF de fabricação completo da lockdown.'],['Playfield e vidro mantidos nas posições aprovadas.','Cradle, pivô, duas escoras cativas e prova de carga individual; não há liberação estrutural.'],['Passagens de energia/RJ45 diretamente na madeira.','Isolação, proteção/aterramento, acesso interno, dimensionamento elétrico e testes.']]
y=table(20,239,379,rows,[180,199])
y=para(20,y-8,379,f'<b>Validação desta consolidação:</b> {len(r["checks"])} verificações e{r["solids"]} sólidos salvos/reabertos. Conferidos novos volumes, serviço de áudio, preservação de traseira/prateleiras/laterais, âncoras e exportação plana. Os testes não equivalem a certificação estrutural, elétrica ou acústica.',True)
para(20,y-8,379,'<b>Referências consultadas:</b> Cleveland High Power SSF Kit; guia oficialSSF; DaytonDCS165-4, BST-1 eEX32EP2-4. Cotas recuperadas do conteúdo técnico indexado; downloads diretos de PDFs foram bloqueados. Nenhum desenho de terceiro foi redistribuído neste PDF. PDFs indisponíveis e divergências de cotas estão registrados na biblioteca.',True)
C.linkURL('https://www.clevelandsoftwaredesign.com/pinball-parts/p/high-power-ssf-kit',(20*mm,25*mm,199*mm,35*mm),relative=0);text(20,29,'Referência Cleveland: High Power SSF Kit',9,True,blue)
C.linkURL('https://github.com/advpeterrobinson-hash/vpin-cabinet/tree/feat/cabinet-review-v32',(219*mm,25*mm,400*mm,35*mm),relative=0);text(219,29,'Fonte do projeto, CAD, parâmetros e evidência',9,True,blue)
C.save();print('CONSOLIDATED_PDF_PASS',page,'pages')
