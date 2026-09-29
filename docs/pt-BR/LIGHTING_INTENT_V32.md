# Iluminação endereçável — kit selecionado

[English](../LIGHTING_INTENT_V32.md) · [Português (Brasil)](LIGHTING_INTENT_V32.md)

**OWNER_SELECTED 2026-09-29; integração PROVISIONAL; CNC BLOCKED.** O proprietário selecionou o [Addressable LED Plug and Play Kit da Cleveland Software Design](https://www.clevelandsoftwaredesign.com/pinball-parts/p/addressable-led-plug-and-play-kit). Mantida a intenção anterior de seis painéis. Em 2026-09-29 o proprietário confirmou dois anéis dos speakers e iluminação opcional sob o gabinete; o SKU final do pedido permanece sem registro. Não há declaração de compra ou recebimento.

A controladora incluída substitui a previsão de Arnoz MX-DONNY para este kit. Isso não altera outros dispositivos Arnoz. Notas anteriores de Pinscape/MX-DONNY permanecem como histórico, não como alocação atual de portas.

## Dados publicados e limites dimensionais

Fonte consultada em 2026-09-29. O fornecedor lista controladora Wemos S2 com 10 saídas, painéis, duas fitas laterais, cabos/extensões, espaçadores/parafusos, cabo USB e fonte de 5 V / 15 A. Seis painéis fornecem 1.536 pixels; as fitas somam 288. Anéis opcionais possuem 45 pixels cada, 5 V e dimensões anunciadas de 120/102/9 mm (confirmar o significado de cada dimensão).

Cada painel é anunciado com 3.125 polegadas de lado: 79.375 mm. O comprimento dos seis painéis é aproximado separadamente como 18.5 polegadas: 469.9 mm. Seis larguras nominais somam 476.25 mm, diferença de 6.35 mm. Nenhum valor define envelope de usinagem; espessura, furação, espaçamento e folga de conectores seguem desconhecidos.

A saída nominal da fonte corresponde aritmeticamente a 75 W, não ao consumo medido dos LEDs nem à comprovação de brilho irrestrito. Correntes permanecem desconhecidas até documentar limites de operação. Preservar a entrada externa única aterrada; o cabo fornecido não autoriza segunda entrada externa ou terminais de rede expostos.

## Configuração e decisões restantes

Usar o [gerador de arquivo do fabricante](https://pinball-docs.clevelandsoftwaredesign.com/docs/AddressableLED/cabinetGenerator/) para a configuração real e porta COM detectada. Os presets incluem fitas laterais. Salvar a configuração e verificar ordem dos pixels, orientação, brilho e zonas no comissionamento; não reutilizar o cálculo de três saídas da MX-DONNY. Nenhuma porta ou cabinet.xml está congelado agora.

Os seis painéis mantêm a intenção anterior de 16×16. Disposição física e posição exata acima do playfield seguem abertas. Fitas incluídas não comprovam cobertura sob o gabinete nem nas folgas opcionais da tela. Os dois anéis selecionados acrescentam 90 pixels, totalizando 1.914 com matriz e fitas laterais do kit. A iluminação opcional sob o gabinete constitui a zona separada UNDERCABINET_LED, com produto, comprimento, pixels, alimentação e portas ainda indefinidos; sua carga não está incluída nesse subtotal. LEDs opcionais nas folgas da tela também permanecem separados.

## Integração mecânica e elétrica a desenvolver

- **Suporte da matriz** e **acabamento da iluminação** permanecem nomes provisórios, sem códigos definitivos. Usar adaptadores removíveis com fixadores e conectores acessíveis; evitar móveis estruturais adicionais ou furos permanentes específicos de componentes.
- Verificar abertura de serviço do playfield, movimento do backbox, ângulo de visão, reflexos no vidro e acesso aos conectores antes de introduzir geometria CAD. A matriz não deve obstruir manutenção nem usar a TV como suporte.
- Manter a iluminação dos speakers removível com o conjunto; reservar iluminação do gabinete sem fixar posições ainda. LEDs opcionais nas folgas devem preservar substituição e ventilação do display.
- Selecionar painéis/fitas antes de calcular tensão, corrente máxima, capacidade da fonte, proteção de ramais, bitolas e pontos de injeção de alimentação. Capacidade de controle não equivale à capacidade da fonte. Preservar regras existentes de isolamento de rede e roteamento de áudio/dados.
- Prever brilho independente por zona e opção de desligar efeitos; aparência final exige revisão visual do proprietário.

Próximos dados: SKU de seis painéis/pedido, produto sob o gabinete caso adotado, medidas montadas, fixações/conectores, comprimentos das fitas e limites documentados de operação. Sessões físicas seguem pausadas; nenhuma geometria CAD foi alterada.
