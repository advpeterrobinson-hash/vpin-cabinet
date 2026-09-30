# V32 — ventoinhas fixas, energia, Ethernet e piso

**As duas ventoinhas cabem acima da porta.** O novo CAD as transfere para o painel fixo, com grades e parafusos. A porta passa a ser lisa, conservando chave, puxador e dobradiças. Não precisa mais carregar cabos das ventoinhas. PC baixo, laterais e prateleiras aprovadas permanecem inalterados.

![Traseira e piso](../exports/generated/fixed-rear-services-v32/01-fixed-rear-and-floor.png)

## Ventoinhas e acesso

CentrosX230/370, Z500; molduras de referência120 ×120 ×25 e grades de1,5 mm. RecortesØ116 e padrão105 mm com passagensØ4,5 mantêm as referências anteriores. Tudo depende da correspondência com o fan/grade realmente escolhido.

A base das molduras fica emZ440, **57 mm acima da porta fechada**. O topo emZ560 deixa **18,9 mm até a face inferior do apoio do backbox**. Os corpos ficam emY1265,1..1290,1, atrás do painel fixo. Subir os centros mais20 mm produz colisão com esse apoio; esse caso é controle negativo, não uma opção de montagem.

O painel fixo tem18 mm, contra12 da porta. Por isso o estudo troca os parafusos candidatos dos fans de M4 ×50 para **M4 ×55**, mantendo as arruelas, porcas e grades nos lados correspondentes. Comprimento/rosca real e travamento continuam sujeitos à ferragem selecionada. Os corredores candidatos de ferramenta, externos e internos, foram conferidos; o soquete interno tem alívio central para a ponta do parafuso.

A porta continua com abertura amostrada0..110°. A rota excepcional do PC passa a110°. **A90° ainda há interferência com o corpo/lingueta da fechadura**, embora o obstáculo dos fans tenha desaparecido. Não afirmar que a retirada completa do PC passa a90°. Limitadores seguem opcionais; feltro no contato real do miolo continua a solução do proprietário. Repouso livre além do ângulo testado não foi avaliado.

## Energia e Ethernet: recortes feitos na madeira do estudo

As aberturas ficam na parte fixa, separadas da porta. Dimensões em mm; X visto de frente do gabinete, Z acima da base externa. A imagem traseira é um esquema com esse mesmo datum, não um gabarito de usinagem invertido.

| Interface | Abertura na madeira, X / Z / largura / altura | Placa substituível, X / Z / largura / altura |
|---|---|---|
| Energia | 60 /405 /70 /50 | 45 /390 /100 /80 |
| Ethernet | 515 /415 /30 /30 | 500 /400 /60 /60 |

Cantos das aberturas de serviço com raio candidato3 mm. Placas candidatas2 mm, quatro passagensØ4,5 cada, também abertas no painel. Energia: X52,5/137,5 eZ397,5/462,5. Ethernet: X507,5/552,5 eZ407,5/452,5. Esses pontos são decisões de interface, não furação universal de IEC/RJ45. Retenção das placas e ferragens ainda precisam ser detalhadas.

**As placas estão em branco no CAD.** O recorte do inlet de energia e o encaixe do RJ45/keystone são feitos nas placas depois de confirmar os módulos. As aberturas na madeira e sua localização já entram no estudo; trocar um conector altera a placa pequena, não o painel inteiro. Não há banco permanente HDMI/USB.

Para energia há um invólucro mecânico candidato separado,100 ×100 ×100, emX45/Y1190,1/Z385, paredes2 mm e entrada alinhada à janela. Ele ocupa um espaço livre sem tocar fans, PC ou backbox. É uma reserva modelada de invólucro fechado, **não um equipamento elétrico certificado**. A fixação/lidagem de serviço, material, proteção, aterramento, alívio de tração, saídas isoladas, corrente/tensão e conexão à distribuição ainda exigem especificação adequada. Não foi desenhado ou liberado cabeamento de rede elétrica. Nenhum terminal deve ficar exposto à área de manutenção.

## Piso e entrada de ar

O novo piso mantém dimensões/posição, abertura de referência do subwooferØ139,7 emX300/Y440 e a entrada100 ×160 emX400/Y630. Acrescenta uma entrada simétrica100 ×160 emX100/Y630. Os quatro furos auxiliaresØ28 emY90 foram omitidos porque não têm função definida; não produzir aberturas sem finalidade.

Dois porta-filtros candidatos120 ×180 ×8 ficam por baixo das entradas, emZ10..18. São molduras removíveis; meios filtrantes, fixações e folga ao chão ainda não estão definidos. As janelas do piso são contornos nominais; raios finais da ferramenta e instruções de acabamento aguardam CAM. Não há rodas integradas.

Área bruta de entrada32000 mm²; isso não é área livre após filtros nem vazão. A combinação de filtros/grades, caminhos internos, calor e ruído precisa de avaliação térmica. O estudo não qualifica a rigidez do piso após os recortes nem substitui a prova de carga.

## Lockdown: direção definida, furação provisória acrescentada

A [interface registrada](LOCKDOWN_INTERFACE_V32.md) continua baseada em barra personalizada para corpo600 mm e receptor WPC compatível. Neste CAD foram abertos **os dois furos externos candidatosØ7,14375**, X68,225/477,8 eZ365,096875. O centroX300 existente é compartilhado com a porta de moedas; não foi duplicado.

Escolha explícita deste rascunho: usarØ9/32 da figura do Pinscape, igual ao furo central existente. O texto do guia usaØ5/16; essa alternativa continua registrada e a ferragem real governa a dimensão de fabricação. A mudança não prova o encaixe do corpo do receptor, alavanca, linguetas ou barra.

A definição para fornecer/cotar a barra está em [LOCKDOWN_BUILD_BRIEF_V32.txt](LOCKDOWN_BUILD_BRIEF_V32.txt). **Não há desenho de fabricação completo da barra metálica**: perfil, linguetas e receptor real ainda não têm cotas suficientes. Finalizar esses detalhes com dados do conjunto evita entregar um DXF inventado. O fechamento funcional não é liberação de corte.

## Evidência e pacote atual

[CAD fechado](../exports/generated/fixed-rear-services-v32/closed.FCStd) · [Porta90°](../exports/generated/fixed-rear-services-v32/open90.FCStd) · [Porta110°](../exports/generated/fixed-rear-services-v32/open110.FCStd) · [Relatório](../exports/generated/fixed-rear-services-v32/validation.json).

`bash tools/run_fixed_rear_services_v32.sh` exige `FIXED_REAR_SERVICES_PASS`: **27 verificações,197 sólidos por posição**, incluindo envelopes. Validade e identidade após reabrir; fans/piso simétricos; montagem e ferramentas; folgas do backbox e porta; abertura amostrada; rota do PC; retirada dos furos auxiliares; preservação de laterais/prateleiras/PC e dos arquivos de entrada. Casos rejeitados: fans20 mm mais altos e saída do PC a90° bloqueada pela fechadura.

Mudam neste estudo Rear, RearDoor, Floor, os dois furos externos de Front e a posição/fixações dos fans. Os arquivos anteriores permanecem intactos. Render: `uv run --with matplotlib python tools/render_fixed_rear_services_v32.py`.

O gabinete ainda não está integralmente finalizado para fabricar: receptor/barra reais, retenção das canaletas, dobradiça/escoras do playfield, fixações do PC/SSF/backbox, componentes elétricos, cargas e requisitos de CNC permanecem abertos. As medidas dependentes das peças importadas continuam podendo ser conferidas depois, como autorizado; não bloqueiam este avanço de disposição.

Original: CERN-OHL-S-2.0. Preservar LICENSE e NOTICE.md. Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet.
