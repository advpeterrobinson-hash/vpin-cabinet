# Renderizações / Renders

> **Página de acesso rápido às renderizações atuais do projeto.**  
> Current owner-facing design review: **V32** on `feat/cabinet-review-v32`.  
> **Não liberado para CNC / Not released for machining.**

Esta página existe para que o estado visual do projeto seja encontrado sem navegar pela árvore de arquivos. As imagens abaixo representam a revisão atual publicada; o pacote técnico completo permanece em [`exports/generated/cabinet-v32/`](../exports/generated/cabinet-v32/README.md).

## V32 — gabinete central / main cabinet

### R01 — Interior

[![Interior V32](../exports/generated/cabinet-v32/01-interior.png)](../exports/generated/cabinet-v32/01-interior.png)

Mostra as prateleiras transversais, PC baixo e estrutura interna. Algumas paredes são ocultadas apenas para leitura visual.

### R02 — Travessas / Crossmembers

[![Travessas V32](../exports/generated/cabinet-v32/02-travessas.png)](../exports/generated/cabinet-v32/02-travessas.png)

Mostra T1, T2 e T3, suas guias substituíveis e o sistema de apoio do monitor.

### R03 — Planta / Plan

[![Planta V32](../exports/generated/cabinet-v32/03-planta.png)](../exports/generated/cabinet-v32/03-planta.png)

Mostra S1, S2 e S3 e os corredores de acesso à fiação.

### R04 — Traseira / Rear

[![Traseira V32](../exports/generated/cabinet-v32/04-traseira.png)](../exports/generated/cabinet-v32/04-traseira.png)

Porta de serviço traseira e dois ventiladores de referência de 120 mm.

### R05 — Guia substituível / Replaceable guide

[![Guia V32](../exports/generated/cabinet-v32/05-encaixe.png)](../exports/generated/cabinet-v32/05-encaixe.png)

Detalhe do encaixe removível das travessas. A ranhura está na guia substituível, não na lateral estrutural.

### R06 — Frente / Front

[![Frente V32](../exports/generated/cabinet-v32/06-frente.png)](../exports/generated/cabinet-v32/06-frente.png)

Coin door, comandos frontais e reserva ainda provisória do plunger.

## Estado desta revisão

- V32 consolida V29–V31.
- 45 sólidos válidos no modelo.
- Nenhuma interseção de volume positivo acima de 0,01 mm³ na validação atual.
- Isso valida embalagem/interferência CAD, **não** resistência estrutural.
- Sessões físicas permanecem pausadas.
- CNC/manufatura permanecem bloqueados.

## Identificação das peças

Os códigos permanentes e nomes provisórios são controlados em [`docs/PART_CODES.md`](PART_CODES.md).

Regra visual:

- `T1`, `S2`, `S1SupR` = identidade permanente já atribuída.
- `**nome provisório**` = conceito ainda sem código permanente.
- Um código nunca é reutilizado para outra função.
- Mudanças posteriores preservam o código e acrescentam revisão quando necessário.

## Arquivos técnicos

- [Pacote V32](../exports/generated/cabinet-v32/README.md)
- [Lista de peças](../exports/generated/cabinet-v32/PECAS-PARTS.md)
- [FreeCAD](../exports/generated/cabinet-v32/vpin-central-v32.FCStd)
- [STEP](../exports/generated/cabinet-v32/vpin-central-v32.step)
- [Validação](../exports/generated/cabinet-v32/validation.json)

## Próxima atualização visual

A próxima revisão deve incorporar, quando aprovada, a proposta de encaixe capturado CNC do gabinete inferior documentada em [`docs/CABINET_JOINERY_PROPOSAL.md`](CABINET_JOINERY_PROPOSAL.md). Até lá, nenhuma renderização deve sugerir que esses rasgos já fazem parte da geometria liberada.
