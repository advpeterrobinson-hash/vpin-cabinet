# Iluminação endereçável — intenção do proprietário

[English](../LIGHTING_INTENT_V32.md) · [Português (Brasil)](LIGHTING_INTENT_V32.md)

Estado: **planejamento PROVISIONAL; geometria V32 sem alterações; CNC BLOCKED**.

O proprietário pretende instalar uma matriz de LEDs acima do playfield usando Arnoz MX-DONNY, provisoriamente com seis painéis de 16×16 LEDs (1.536 pixels). Também pretende iluminação nos speakers e no gabinete. LEDs na folga restante ao redor do display do playfield são opcionais, dependendo do espaço real e da revisão visual.

“16×16” é resolução em pixels, não milímetros. Seis painéis podem formar 96×16 pixels em uma fileira ou 48×32 em um arranjo de três por dois; nenhum arranjo ou envelope físico está selecionado. A posição exata pretendida por “acima do playfield”, dimensões dos painéis, passo dos pixels, espaço para conectores e orientação permanecem abertos. Não alterar o gabinete nem reduzir o envelope de troca do display para acomodar uma dimensão presumida.

## Referência da controladora e limites de planejamento

A [página oficial da MX-DONNY](https://shop.arnoz.com/en/dude-s-cab/151-mx-donny.html) descreve uma expansão usada com Dude's Cab, com oito saídas e até 4.096 LEDs endereçáveis. O [manual da Dude's Cab](https://dude.arnoz.com/dude_Cab_English_guide.pdf) informa 512 LEDs por saída para animações fluidas. Fontes consultadas em 2026-09-27; somente links e um resumo factual foram registrados, sem importar arquivos do fabricante.

Apenas cálculo preliminar: dois painéis de 256 pixels equivalem a 512 pixels; seis painéis poderiam usar três saídas de dados se chipset, encadeamento e mapeamento da matriz escolhidos permitirem esse arranjo. Restariam cinco saídas para outras zonas, conforme suas quantidades de pixels. Isso não confirma distribuição de cabos, orçamento elétrico ou compra. Confirmar a revisão da controladora/placa principal e a compatibilidade dos LEDs antes de congelar a configuração.

## Integração mecânica e elétrica a desenvolver

- **Suporte da matriz** e **acabamento da iluminação** permanecem nomes provisórios, sem códigos definitivos. Usar adaptadores removíveis com fixadores e conectores acessíveis; evitar móveis estruturais adicionais ou furos permanentes específicos de componentes.
- Verificar abertura de serviço do playfield, movimento do backbox, ângulo de visão, reflexos no vidro e acesso aos conectores antes de introduzir geometria CAD. A matriz não deve obstruir manutenção nem usar a TV como suporte.
- Manter a iluminação dos speakers removível com o conjunto; reservar iluminação do gabinete sem fixar posições ainda. LEDs opcionais nas folgas devem preservar substituição e ventilação do display.
- Selecionar painéis/fitas antes de calcular tensão, corrente máxima, capacidade da fonte, proteção de ramais, bitolas e pontos de injeção de alimentação. Capacidade de controle não equivale à capacidade da fonte. Preservar regras existentes de isolamento de rede e roteamento de áudio/dados.
- Prever brilho independente por zona e opção de desligar efeitos; aparência final exige revisão visual do proprietário.

Próximos dados de engenharia: modelo e dimensões dos painéis/fitas, chipset/tensão/corrente, arranjo físico pretendido, dimensões da iluminação dos speakers e comprimentos das fitas do gabinete. Sessões físicas continuam pausadas; este registro não pressupõe medições ou aprovações.
