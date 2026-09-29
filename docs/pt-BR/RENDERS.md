# Renderizações

[English](../RENDERS.md) · [Português (Brasil)](RENDERS.md)

> **Página de acesso rápido ao estado visual atual do projeto.**  
> Revisão atual para avaliação do proprietário: **V32** no branch `feat/cabinet-review-v32`.  
> **Não liberado para CNC ou fabricação.**

Esta página permite que um novo colaborador entenda rapidamente a direção atual do gabinete sem primeiro navegar por toda a árvore do repositório. O pacote técnico completo permanece em [`exports/generated/cabinet-v32/`](../../exports/generated/cabinet-v32/README.md).

## Último desenvolvimento — porta de moedas abrindo para fora

Porta iluminada básica, mecanismos funcionais opcionais e bandeja compacta removível. São configurações candidatas separadas; V32 original inalterada. Encaixe das ferragens reais permanece **UNVERIFIED**.

[![Configurações da porta](../../exports/generated/front-panel-v32/02-coin-door-configurations.png)](FRONT_PANEL_REVIEW_V32.md)

[Abrir revisão frontal e verificações de movimento](FRONT_PANEL_REVIEW_V32.md).

## Proposta separada de encaixes

Três novas vistas mostram cortes dos encaixes, caixa explodida e alterações exatas. **É uma proposta separada; as vistas V32 aceitas abaixo permanecem iguais.**

**[Abrir estudo com três vistas](JOINERY_STUDY_V32.md)**

[![Proposta separada: caixa explodida](../../exports/generated/joinery-study-v32/02-exploded-shell.png)](JOINERY_STUDY_V32.md)

## V32 — gabinete central

### R01 — Interior

[![Interior V32](../../exports/generated/cabinet-v32/01-interior.png)](../../exports/generated/cabinet-v32/01-interior.png)

Mostra as prateleiras transversais, o PC baixo e a estrutura interna. Alguns painéis são ocultados apenas para melhorar a leitura visual.

### R02 — Travessas

[![Travessas V32](../../exports/generated/cabinet-v32/02-travessas.png)](../../exports/generated/cabinet-v32/02-travessas.png)

Mostra T1, T2 e T3, suas guias substituíveis e o sistema de apoio do monitor.

### R03 — Planta

[![Planta V32](../../exports/generated/cabinet-v32/03-planta.png)](../../exports/generated/cabinet-v32/03-planta.png)

Mostra S1, S2 e S3 e os corredores de acesso à fiação.

### R04 — Traseira

[![Traseira V32](../../exports/generated/cabinet-v32/04-traseira.png)](../../exports/generated/cabinet-v32/04-traseira.png)

Porta traseira de serviço e dois ventiladores de referência de 120 mm.

### R05 — Guia substituível

[![Guia V32](../../exports/generated/cabinet-v32/05-encaixe.png)](../../exports/generated/cabinet-v32/05-encaixe.png)

Detalhe da interface removível das travessas. A ranhura fica na guia substituível, não na lateral estrutural.

### R06 — Frente

[![Frente V32](../../exports/generated/cabinet-v32/06-frente.png)](../../exports/generated/cabinet-v32/06-frente.png)

Referência da coin door, comandos frontais e reserva ainda provisória do plunger.

## Estado atual

- V32 consolida V29–V31.
- 45 sólidos válidos no modelo atual.
- Nenhuma interseção de volume positivo acima de 0,01 mm³ na validação atual.
- Isso valida empacotamento/interferência CAD, **não** resistência estrutural.
- Sessões físicas permanecem pausadas.
- Liberação para CNC/fabricação permanece bloqueada.

## Identidade das peças

Os códigos permanentes e nomes provisórios são controlados em [`PART_CODES.md`](PART_CODES.md).

Regra visual:

- `T1`, `S2`, `S1SupR` = identidade permanente já atribuída.
- `**nome provisório**` = conceito ainda sem código permanente.
- Um código permanente nunca é reutilizado para outra função.
- Alterações futuras preservam o código e acrescentam revisão quando necessário.

## Arquivos técnicos

- [Pacote técnico V32](../../exports/generated/cabinet-v32/README.md)
- [Lista de peças](../../exports/generated/cabinet-v32/PECAS-PARTS.md)
- [FreeCAD](../../exports/generated/cabinet-v32/vpin-central-v32.FCStd)
- [STEP](../../exports/generated/cabinet-v32/vpin-central-v32.step)
- [Validação](../../exports/generated/cabinet-v32/validation.json)

## Próxima atualização visual

A próxima iteração poderá incorporar a proposta de encaixe capturado CNC documentada em [`CABINET_JOINERY_PROPOSAL.md`](CABINET_JOINERY_PROPOSAL.md). Até que ela seja aceita e validada, nenhuma renderização deve sugerir que esses rasgos fazem parte da geometria V32 liberada.

## Reproduzir a revisão atual

Execute `make review-v32`. A geometria é comparada com a evidência V32 do commit antes de aceitar os renders. Consulte a [validação local](V32_LOCAL_AUDIT.md). Fabricação continua bloqueada.
