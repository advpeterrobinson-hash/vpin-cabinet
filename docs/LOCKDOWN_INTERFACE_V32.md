# V32 — interface da lockdown com a frente

**Atualização:** [fans fixos acima da porta, energia/Ethernet, piso e furação candidata da lockdown](FIXED_REAR_SERVICES_V32.md). Fans não acompanham mais a porta nesta proposta.

Continuação após aprovação da porta traseira. Mantida a direção: barra personalizada para corpo600 mm com receptor WPC compatível, vidro removido pela frente e liberação da barra pela porta de moedas. Este avanço registra os eixos de fixação; não acrescenta um receptor genérico sem dimensões nem faz novos cortes.

## Referência recuperada

O MHT do Pinscape enviado contém o texto da seção2.19.6 e links para figuras externas. Duas figuras foram baixadas e inspecionadas, arquivadas somente em `library/references/local/`, com URL/hash no inventário. A figura de montagem confirma que o parafuso superior central da porta de moedas é compartilhado com o receptor.

A [figura cotada](https://head.pinscape-build-guide.pages.dev/images/front-panel-lockbar-and-door-bolts.png) mostra a face **interna** do painel frontal. Portanto, seu sentido horizontal precisa ser invertido para o X do projeto, visto de frente. Não tornar o padrão simétrico: as distâncias indicadas são7 e9⅛ polegadas do centro.

| Eixo | X do projeto, mm | Z candidato, mm | Tratamento |
|---|---:|---:|---|
| Externo esquerdo, visto pelo jogador | 68,225 | 365,096875 | Planejar; não perfurado |
| Central compartilhado | 300 | 365,096875 | Preservar furo superior existente da porta de moedas |
| Externo direito, visto pelo jogador | 477,8 | 365,096875 | Planejar; não perfurado |

A figura coloca a linha1⅜ polegada abaixo da borda superior interna: para400,05 nominal, resultaZ365,125. A diferença0,028125 mm em relação ao furo existente foi registrada; o planejamento mantém o datum existente para não duplicar o furo central. O ajuste final da montagem depende de barra, siderails e vidro assentados.

Há uma discrepância de diâmetro: figuraØ9/32 polegada (7,14375 mm), texto do guiaØ5/16 (7,9375 mm), com parafusos nominais¼-20. Nenhum dos diâmetros foi adotado nesta etapa. O comprimento de parafuso citado no guia também não libera o nosso conjunto de18 mm sem conferir as peças e o engajamento.

A [listagem de fornecedor](https://www.marcospecialties.com/pinball-parts/A-16773-1) identifica o receptor WPC/WPC95 com mola como **A-16773-1**. O texto enviado do Pinscape registra A-16673-1 / A-9174-4. Preservamos essa discrepância no arquivo de parâmetros; não presumimos intercambialidade nem usamos a transcrição antiga como SKU de compra confirmado. O resultado de busca da página foi consultado; a abertura direta posterior falhou. Não há desenho dimensional completo do receptor nessa evidência.

## Acesso e ordem de montagem

Conferir primeiro o conjunto de vidro/canaletas/siderails e barra assentada; alinhar o receptor com o eixo compartilhado; liberar lingueta/alavanca e acesso às porcas; somente então qualificar os dois furos externos e o diâmetro da passagem. A CNC deverá entregar os furos prontos quando a interface estiver confirmada, sem depender de marcação precisa pelo montador.

O teste de ferramenta usa um cilindro candidatoØ20 ×100, começando emY26 em cada eixo. Com o display fechado, encontra o envelope do playfield. Com o display na pose assumida100° e vidro removido, os três corredores ficam livres da cena modelada. Isso não é um ensaio de montagem do receptor: corpo, linguetas, porcas, mão e chegada da ferramenta através da porta ainda não estão representados.

A reserva anterior Z380..400,05 é insuficiente para descrever a fixação do receptor, cuja linha de parafusos está emZ365,096875. Não interpretar aquela faixa como envelope completo. Esta constatação altera a documentação da interface, não desloca S1, o display ou a porta frontal.

## Evidência

[Parâmetros](../config/lockdown_interface_v32.json) · [Relatório](../exports/generated/lockdown-interface-v32/validation.json).

Executar `freecadcmd tools/lockdown_interface_v32_entry.py` e exigir `LOCKDOWN_INTERFACE_PASS`: **7 verificações**. Eixo central existente, material nos eixos externos, diferença dos datums, discrepância de diâmetro explicitamente mantida, corredores com display elevado, controle negativo com display fechado e arquivos de entrada intactos. Não salva nem altera CAD.

A geometria do receptor, sua compatibilidade com a barra personalizada e as fixações definitivas continuam pendentes das ferragens. A conferência pode ser feita quando as peças chegarem, conforme autorizado; as demais interfaces continuam avançando. Fabricação não liberada.

Original: CERN-OHL-S-2.0. Preservar LICENSE e NOTICE.md. Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet.
