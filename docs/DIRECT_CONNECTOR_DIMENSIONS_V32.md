# V32 — cotas dos conectores recebidas em 2026-09-30

Montagem direta na madeira, sem placa intermediária, conforme escolha do proprietário. Imagens originais preservadas em `library/references/local/` e identificadas por hash no inventário; direitos de terceiros não transferidos ao projeto.

## RJ45: furação provisória incorporada ao CAD

Imagem416185 do anúncio indicado: chamadaØ23,6; dois furosØ3,1; diferença horizontal19 e vertical24 entre seus centros. A vista lateral também indica30,7,27,8 e21,7. Essas últimas medidas não bastam para deduzir espessura da flange, profundidade útil atrás do painel ou acesso à trava do patch cord.

Escolhas explícitas do rascunho: abertura circularØ24 (0,4 acima da chamada23,6), duas passagens na madeiraØ3,2 para fixação candidataM3. O desenho comercial não identificaØ23,6 como tolerância de recorte; confirmar corpo passante e cobertura da flange antes de usinar. O furoØ3,1 indicado pertence à peça;Ø3,2 é a escolha de folga na madeira, não uma nova especificação do fabricante.

Centro globalX530/Z430. Furos globalX539,5/Z442 eX520,5/Z418. A foto mostra a face externa do conector; na traseira, esquerda visual corresponde aX maior. Por isso o par diagonal é invertido emX ao passar da foto ao CAD. Mantém-se a orientação da tomada mostrada na foto. O esquema geral usa coordenadas globais, não é um gabarito da vista externa.

Os três cortes atravessam os18 mm nominais da madeira. A menor ponte entre o recorte e cada furo fica aproximadamente1,705 mm: valor geométrico, **não comprovação de resistência da fixação**. Conferir apoio da flange, arruelas, aperto, comprimento dos parafusos, acesso às porcas e às travas dos cabos. Não há parafusos/porcas ou conectores modelados em escala; o estudo valida os cortes, não a montagem completa.

Nenhuma placa extra ou rebaixo foi acrescentado. Se o encaixe do cabo interno exigir alívio local, ele será definido com o componente; não presumir compatibilidade de toda tomada de painel com madeira18 mm.

## Energia: nova foto não define o recorte

Imagem416183 apresenta um módulo retangular sem as duas orelhas de parafuso visíveis na imagem416182 anterior. O formato sugere retenção por encaixe, mas a foto não prova o mecanismo. As chamadas50,30 e24 não incluem um desenho de recorte, tolerâncias, passo de parafusos ou espessura de painel permitida. Não se deve interpretar50×30 como janela de corte nem24 como profundidade útil.

A posição de planejamentoX95/Z430 permanece. A madeira fica intacta ali; `footprint:null` continua deliberado. Para cumprir a preferência por dois parafusos, o modelo com orelhas anterior ainda é uma alternativa, mas não foi selecionado silenciosamente no lugar do novo anúncio. É necessário desenho da traseira/recorte ou identificação exata da peça para fechar essa interface. O invólucro interno protetor permanece independente da forma de fixação do inlet.

Link curto recebido: https://meli.la/13BjJHD. Acesso web falhou; HTTP403 sem destino resolvido e navegador indisponível. Não afirmar ter revisado o anúncio ou homologação elétrica. A leitura aqui se baseia nas imagens fornecidas.

## Verificação

`bash tools/run_fixed_rear_services_v32.sh`:33 verificações;195 sólidos por posição. Novas verificações conferem três furos passantes, par diagonal19×24 e conversão de vista, ponte positiva e volume removido somente pelos três cortes. Mantidos fans fixos, abertura amostrada da porta, rota excepcional do PC e prateleiras aprovadas. CNC continua pendente de ferragens, stock/ferramenta/tolerâncias e demais requisitos do projeto.

Original CERN-OHL-S-2.0. Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet
