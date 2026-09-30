# V32 — chapa inferior e manutenção dos filtros

Estudo separado que parte do gabinete com a traseira integrada. [Situação da traseira](REAR_CLOSURE_STATUS_V32.md). Preservados PC baixo, prateleiras, laterais e todos os objetos traseiros; somente piso e dois suportes de filtro mudam.

## Geometria e fixação

Piso564×1272,1×18, X18..582/Y18..1290,1/Z18..36. Duas entradas100×160 nos pontosX100/Y630 eX400/Y630 passam a ter **cantosR3**, hipótese de fresaØ6 não confirmada. Sem dogbones: nenhuma peça quadrada foi selecionada para ocupar os cantos. Um plugue quadrado de tamanho integral é rejeitado no controle negativo.

Cada suporte inferior passa a130×190×8, com borda15 em volta da janela e cantosR3. Envelope candidato de suporte, não especificação do material ou do filtro comprado. A borda mais larga acomoda quatro fixações sem colocá-las imediatamente junto ao recorte. Oito passagensØ4,5 atravessam piso e suportes:

| Suporte | CoordenadasX | CoordenadasY |
|---|---|---|
| Esquerdo |92,5 /207,5 |622,5 /797,5 |
| Direito |392,5 /507,5 |622,5 /797,5 |

Quatro combinaçõesX/Y por suporte. CandidatoM4×35 passante, cabeça por cima; hipótese arruela superior0,8, piso18, suporte8, arruela inferior0,8 e porca3,2. A ponta fica emZ1,8 e a porca emZ6..9,2. Rosca/arruelas/cabeça/travamento finais não escolhidos. O CAD salva os furos e suportes, não sólidos de cada parafuso.

Para limpar, soltar as quatro porcas inferiores e baixar o suporte; retirar o meio filtrante. Não foi projetado sistema rápido/cativo. O teste verifica80mm de retirada vertical e corredores de ferramenta no conjunto modelado; folga externa real ao chão depende das pernas. O material filtrante e sua retenção contra sucção ainda precisam ser especificados; não afirmar que o filtro está completo apenas com a moldura vazada. Montar inicialmente antes de povoar o gabinete e manter o acesso superior às cabeças.

Área geométrica bruta das duas entradas comR3:31984,55mm². Não representa área livre do filtro ou vazão medida. Não há afirmação de desempenho térmico ou resistência do piso.

## Aberturas e itens preservados

- Subwoofer: abertura de referênciaØ139,7 emX300/Y440. Faltam modelo real, flange, parafusos, cesta, proteção inferior, montagem/carga vibratória e acesso. Não inventar furação universal de alto-falante.
- Os quatro furos auxiliares sem função emY90 continuam eliminados.
- PCBase baixo mantido. Fixação do chassi e base requer definição própria; não adicionar furos aleatórios no piso.
- Sem rodas integradas. Iluminação inferior segue opcional, sem furação permanente ainda.
- União estrutural piso/laterais ainda é a arquitetura vigente; a proposta de caixa capturada não foi incorporada silenciosamente.

## Arquivos e validação

[CAD](../exports/generated/floor-detail-v32/floor-detail.FCStd) · [Relatório](../exports/generated/floor-detail-v32/validation.json) · [Parâmetros](../config/floor_detail_v32.json).

`bash tools/run_floor_detail_v32.sh`:48 verificações. Cortes, raios, oito pontos de fixação, envelopes candidatos de fixadores/ferramentas, retirada dos suportes, simetria, limites do piso, ausência de colisões modeladas, fonte preservada e arquivo salvo/reaberto.195 sólidos; somente três peças mudam. Não substitui ensaio de montagem/carga nem confirmação das peças.

Este estudo inicia o detalhamento do piso; não o declara concluído. Próximos itens são subwoofer, retenção do PC, distribuição protegida e fixações opcionais, além da qualificação estrutural/CAM do painel. CNC permanece sem liberação.

Original CERN-OHL-S-2.0. Preservar LICENSE e NOTICE.md. Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet
