# Iluminação endereçável — dimensões da matriz e orientação do proprietário

[English](../LIGHTING_INTENT_V32.md) · [Português (Brasil)](LIGHTING_INTENT_V32.md)

**Esclarecimento do proprietário, 2026-09-29:** usar os painéis de matriz da Cleveland Software Design com a placa Arnoz MX-DONNY (Donny). A página da Cleveland é referência dos painéis/dimensões; controladora, fonte e configuração incluídas no kit não são selecionadas por esta decisão. Isso corrige a interpretação anterior de adoção do sistema completo plug-and-play.

O projeto permanece aberto. Instalação, fiação, fonte, configuração da controladora e disposição final serão decididas pelo proprietário. A tarefa atual de engenharia é preservar a referência dimensional da matriz sem congelar suporte, furos permanentes ou posição na V32.

## Dimensões da matriz

Fonte: [anúncio da matriz/kit Cleveland](https://www.clevelandsoftwaredesign.com/pinball-parts/p/addressable-led-plug-and-play-kit), consultado em 2026-09-29. São dimensões nominais publicadas, não medidas das peças reais.

| Item | Dimensão / quantidade | Significado |
|---|---|---|
| Um painel | 3.125 × 3.125 polegadas = 79.375 × 79.375 mm | Dimensão quadrada publicada; espessura não especificada |
| Seis painéis | 6 × 16 × 16 = 1.536 pixels | Quantidade anterior de planejamento mantida |
| Seis painéis em uma fileira | 476.25 × 79.375 mm | Cálculo pelas larguras individuais, sem espaçamento ou folga de conectores; não é disposição selecionada |
| Comprimento aproximado de seis painéis anunciado | 18.5 polegadas = 469.9 mm | Difere da soma das larguras em 6.35 mm; não usar como dimensão final de corte |

Usar o tamanho nominal individual para comparações preliminares. Dimensão montada final, espessura e folgas de instalação permanecem abertas. Este registro não altera envelope de montagem ou geometria do gabinete.

## Demais escolhas de iluminação mantidas

- Dois anéis LED dos alto-falantes incluídos na intenção do proprietário.
- Iluminação sob o gabinete opcional, separada das fitas laterais e dos LEDs opcionais nas folgas da tela.
- As duas fitas laterais do kit permanecem referência da discussão anterior; instalação e alocação não ficam congeladas pela escolha dos painéis.

Não se adota mapa de portas da controladora CSD, configuração de COM, preset cabinet.xml ou fonte incluída no kit. Compatibilidade e instalação cabem à implementação posterior do proprietário; este registro não declara compatibilidade testada. Sessões físicas seguem pausadas e liberação CNC bloqueada.
