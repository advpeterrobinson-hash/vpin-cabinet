# Virtual Pinball Cabinet

[Novo desenvolvimento: alturas congeladas, furação dos apoios e reforços das pernas](docs/SUPPORT_LEG_CNC_V32.md). O gabarito STL foi arquivado com atribuição; seu entre-eixos medido de57 mm difere do segundo modelo de58 mm. Ferragens e liberação CNC continuam pendentes.

## Por onde começar a revisão atual

Use a branch `feat/cabinet-review-v32`. O layout aprovado das prateleiras está congelado em Y120/565/865, com vãos295/150 mm e quatro parafusos por cima em cada prateleira. Comece pela [comparação em planta](exports/generated/side-panel-v32/09-shelf-spacing.png), pela [explicação atual](docs/pt-BR/SIMPLE_SHELVES_V32.md) e pelo [CAD atual das prateleiras](exports/generated/side-panel-v32/simple-shelves-proposal.FCStd). As vistas antigas do gabinete abaixo representam a base preservada, não a nova posição das prateleiras.

O [registro de congelamento](config/shelf_layout_freeze_v32.json), as [93 verificações](exports/generated/side-panel-v32/simple-shelves-validation.json) e o [estudo de abertura em eixo proposto](exports/generated/side-panel-v32/shelf-service-pose-screen.json) estão disponíveis. Pontos úteis para análise: ancoragem dos apoios, dobradiças/escoras/cabos reais, cargas/vibração e tolerâncias de fabricação. A arquitetura de serviço do PC continua pendente na [sequência de fechamento](docs/PANEL_CLOSURE_V32.md). Os testes geométricos não liberam fabricação.

O [índice de links em texto simples](library/references/links.txt) explica as referências externas. Originais de terceiros, backups/caches e o CAD de trabalho antigo protegido ficam fora desta revisão publicada. Os JSON de entrada dos renderizadores do gabinete-base e da proposta separada de encaixes também estão incluídos; a proposta de encaixes ainda não foi adotada.

**[ABRIR A GALERIA ATUAL →](docs/pt-BR/RENDERS.md)** · [English gallery](docs/RENDERS.md)

[English](README.md) · **Português (Brasil)**

> **Revisão atual: V32 — sessões físicas PAUSADAS e CNC/fabricação NÃO liberados.**

Gabinete paramétrico para virtual pinball, preparado para evolução até fabricação CNC, inspirado nas proporções Williams WPC e pensado para eletrônica substituível.

## Comece aqui

Se esta é sua primeira visita:

1. **[Veja as renderizações](docs/pt-BR/RENDERS.md)** — forma mais rápida de entender o design atual.
2. **[Leia o índice da documentação](docs/pt-BR/README.md)**.
3. **[Veja os códigos permanentes de peças](docs/pt-BR/PART_CODES.md)**.
4. **[Leia a proposta atual de encaixe CNC](docs/pt-BR/CABINET_JOINERY_PROPOSAL.md)**.
5. Para contribuir, consulte [CONTRIBUTING.md](CONTRIBUTING.md). O inglês é o idioma canônico das contribuições e da documentação técnica.

Você também pode apenas acompanhar o desenvolvimento. Não é necessário contribuir para usar as renderizações e o histórico como referência.

## Estado V32

A revisão atual está no branch `feat/cabinet-review-v32`.

- gabinete principal de 600 mm;
- três prateleiras transversais S1/S2/S3;
- três travessas removíveis T1/T2/T3;
- guias substituíveis;
- base baixa para PC open-case;
- dois ventiladores traseiros de referência de 120 mm;
- 45 sólidos válidos;
- nenhuma interseção de volume positivo acima de 0,01 mm³ na validação atual.

Esses resultados validam empacotamento/interferência CAD, **não** resistência estrutural nem liberação para fabricação.

## Onde uma contribuição é útil agora

É possível ajudar sem assumir o projeto inteiro:

- **CNC / encaixes:** revisar os encaixes capturados propostos, raios de fresa, coupons de tolerância e sequência de montagem.
- **Projeto mecânico:** fixação/retenção das guias e apoios T1–T3, prateleiras, porta traseira, suporte/serviço do monitor e interfaces Williams.
- **Medições / prototipagem:** padrões reais de ferragens, espessura da chapa, coupons, montagem a seco e observações de rigidez/carga.
- **Térmica / empacotamento:** PC, grelhas, fios, envelopes PSU/CSD e análise de fluxo/folgas.
- **FreeCAD / Python:** integrar V32/V33 em um pipeline limpo e validado que substitua o pipeline pré-V32 mantido em transição.
- **Documentação:** revisão técnica em inglês, espelhos PT-BR, diagramas, montagem e verificação de links/consistência.

Se nenhuma área combinar com seu tempo ou experiência, acompanhar a [página de renderizações](docs/pt-BR/RENDERS.md) já permite observar o andamento.


## Imagens

| Interior | Travessas | Planta |
|---|---|---|
| [![Interior](exports/generated/cabinet-v32/01-interior.png)](exports/generated/cabinet-v32/01-interior.png) | [![Travessas](exports/generated/cabinet-v32/02-travessas.png)](exports/generated/cabinet-v32/02-travessas.png) | [![Planta](exports/generated/cabinet-v32/03-planta.png)](exports/generated/cabinet-v32/03-planta.png) |

| Traseira | Guia | Frente |
|---|---|---|
| [![Traseira](exports/generated/cabinet-v32/04-traseira.png)](exports/generated/cabinet-v32/04-traseira.png) | [![Guia](exports/generated/cabinet-v32/05-encaixe.png)](exports/generated/cabinet-v32/05-encaixe.png) | [![Frente](exports/generated/cabinet-v32/06-frente.png)](exports/generated/cabinet-v32/06-frente.png) |

## Idiomas

O inglês é a fonte canônica da documentação. O português é mantido como espelho para documentos atuais prioritários.

Veja [docs/pt-BR/LANGUAGE_POLICY.md](docs/pt-BR/LANGUAGE_POLICY.md).

## Licença

Projeto open hardware sob **CERN-OHL-S-2.0**. O texto da licença e os avisos oficiais permanecem canônicos no repositório.

## Revisão local atual

Execute `make review-v32` para regenerar V32, verificar os 45 sólidos salvos e metadados bilíngues, comparar a geometria com o commit e gerar seis imagens em inglês. Uma mudança geométrica inesperada interrompe a rota para revisão. Consulte a [auditoria local](docs/pt-BR/V32_LOCAL_AUDIT.md).

`make doctor`, `make validate`, `make build-current` e `make open-master` continuam sendo ferramentas **PRE-V32**. Suas falhas conhecidas estão documentadas; não comprovam validação de V32.
