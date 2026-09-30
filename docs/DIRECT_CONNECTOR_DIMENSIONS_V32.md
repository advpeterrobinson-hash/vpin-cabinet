# V32 — cotas dos conectores recebidas em 2026-09-30

Montagem direta na madeira, sem placa intermediária, conforme escolha do proprietário. Imagens originais preservadas em `library/references/local/` e identificadas por hash no inventário; direitos de terceiros não transferidos ao projeto.

## RJ45: furação provisória incorporada ao CAD

Imagem416185 do anúncio indicado: chamadaØ23,6; dois furosØ3,1; diferença horizontal19 e vertical24 entre seus centros. A vista lateral também indica30,7,27,8 e21,7. Essas últimas medidas não bastam para deduzir espessura da flange, profundidade útil atrás do painel ou acesso à trava do patch cord.

Escolhas explícitas do rascunho: abertura circularØ24 (0,4 acima da chamada23,6), duas passagens na madeiraØ3,2 para fixação candidataM3. O desenho comercial não identificaØ23,6 como tolerância de recorte; confirmar corpo passante e cobertura da flange antes de usinar. O furoØ3,1 indicado pertence à peça;Ø3,2 é a escolha de folga na madeira, não uma nova especificação do fabricante.

Centro globalX530/Z430. Furos globalX539,5/Z442 eX520,5/Z418. A foto mostra a face externa do conector; na traseira, esquerda visual corresponde aX maior. Por isso o par diagonal é invertido emX ao passar da foto ao CAD. Mantém-se a orientação da tomada mostrada na foto. O esquema geral usa coordenadas globais, não é um gabarito da vista externa.

Os três cortes atravessam os18 mm nominais da madeira. A menor ponte entre o recorte e cada furo fica aproximadamente1,705 mm: valor geométrico, **não comprovação de resistência da fixação**. Conferir apoio da flange, arruelas, aperto, comprimento dos parafusos, acesso às porcas e às travas dos cabos. Não há parafusos/porcas ou conectores modelados em escala; o estudo valida os cortes, não a montagem completa.

Nenhuma placa extra ou rebaixo foi acrescentado. Se o encaixe do cabo interno exigir alívio local, ele será definido com o componente; não presumir compatibilidade de toda tomada de painel com madeira18 mm.

## Energia: desenho416187 incorporado

A nova referência enviada com o link ArcadeXpress resolve o recorte: **28×48 mm, cantosR3 e dois furosØ4,5 com40 mm entre centros**. Essas medidas vêm do quadro explícito PANEL CUT-OUT, não de estimativa sobre a foto. Montagem vertical, tomada acima e interruptor abaixo, diretamente na madeira. O modelo retangular sem orelhas416183 deixa de ser a base desta interface.

CentroX95/Z430. Recorte deX81 a109 eZ406 a454; parafusosX75/115, ambosZ430. Cortes atravessam os18 mm nominais do painel. Ponte lateral mínima entre recorte e furos:3,75 mm, sem atribuição de capacidade estrutural. PassagensØ4,5 preveem fixação candidataM4 passante; comprimento, arruelas/porcas e aperto dependem da flange real. Não foram modelados fixadores ou corpo do inlet como ferragens qualificadas.

O desenho mostra20,3 mm na vista lateral até o corpo, excluindo as pontas dos terminais. Isso não informa sozinho quanto sobra atrás da madeira, pois faltam espessura da flange e posição útil de cada terminal. A chamada frontal28,2 difere dos28 do corpo/recorte em outras vistas: mantido o recorte explicitamente indicado, com conferência física e cupom antes do corte final. Não foi adicionado rebaixo nem ampliada a janela sem evidência.

Foi verificada uma **reserva de projeto** para conexões isoladas de40×50×48 mm, X75/Y1240,1/Z406, inteiramente para dentro da face interna do painel. Ela não colide com os sólidos modelados e passa pela abertura do invólucro interno. Essa reserva não representa terminais, botas isolantes ou curvatura real dos fios; falta conferir o conjunto real, acesso a porcas, invólucro e especificação elétrica. Não há liberação de cabeamento ou terminais expostos.

https://www.arcadexpress.com/en/electronics-power-supplies/455-iec320-switch-power-socket-on-off.html
Página indisponível na ferramenta web; evidência dimensional é a imagem416187 fornecida, arquivada localmente com hash. Não foi presumida homologação elétrica ou compatibilidade universal com estoque18 mm.

## Verificação

`bash tools/run_fixed_rear_services_v32.sh`:37 verificações;195 sólidos por posição. Verificações conferem cortes passantes dos dois conectores, par diagonal19×24 e conversão de vista do RJ45, recorte28×48R3 e passo40 da energia, área removida, cantos preservados e reserva interna de conexões. Mantidos fans fixos, abertura amostrada da porta, rota excepcional do PC e prateleiras aprovadas. CNC continua pendente de ferragens, stock/ferramenta/tolerâncias e demais requisitos do projeto.

Original CERN-OHL-S-2.0. Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet

Continuação: [fixação, acesso e cupom físico dos conectores](CONNECTOR_FIT_V32.md).
