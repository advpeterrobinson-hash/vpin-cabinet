# Virtual Pinball Cabinet

## [ABRIR A GALERIA ATUAL →](https://github.com/advpeterrobinson-hash/vpin-cabinet/blob/feat/cabinet-review-v32/docs/pt-BR/RENDERS.md)

[English](README.md) · [Galeria em inglês](https://github.com/advpeterrobinson-hash/vpin-cabinet/blob/feat/cabinet-review-v32/docs/RENDERS.md)

Acompanhe o projeto diretamente pela galeria. **V32 é a revisão visual/arquitetural atual; CNC/fabricação continua BLOCKED e as sessões físicas estão pausadas.**

[![Interior V32: S1/S2/S3 e PCBase baixo](https://raw.githubusercontent.com/advpeterrobinson-hash/vpin-cabinet/refs/heads/feat/cabinet-review-v32/exports/generated/cabinet-v32/01-interior.png)](https://github.com/advpeterrobinson-hash/vpin-cabinet/blob/feat/cabinet-review-v32/docs/pt-BR/RENDERS.md)

[Interior](https://github.com/advpeterrobinson-hash/vpin-cabinet/blob/feat/cabinet-review-v32/exports/generated/cabinet-v32/01-interior.png) · [Travessas](https://github.com/advpeterrobinson-hash/vpin-cabinet/blob/feat/cabinet-review-v32/exports/generated/cabinet-v32/02-travessas.png) · [Planta](https://github.com/advpeterrobinson-hash/vpin-cabinet/blob/feat/cabinet-review-v32/exports/generated/cabinet-v32/03-planta.png) · [Traseira](https://github.com/advpeterrobinson-hash/vpin-cabinet/blob/feat/cabinet-review-v32/exports/generated/cabinet-v32/04-traseira.png) · [Guia](https://github.com/advpeterrobinson-hash/vpin-cabinet/blob/feat/cabinet-review-v32/exports/generated/cabinet-v32/05-encaixe.png) · [Frente](https://github.com/advpeterrobinson-hash/vpin-cabinet/blob/feat/cabinet-review-v32/exports/generated/cabinet-v32/06-frente.png)

Gabinete paramétrico inspirado nas proporções Williams WPC, destinado a um produto CNC flat-pack reproduzível com eletrônica substituível.

## Arquitetura atual

O trabalho atual está no branch [`feat/cabinet-review-v32`](https://github.com/advpeterrobinson-hash/vpin-cabinet/blob/feat/cabinet-review-v32/README.pt-BR.md). O [pacote técnico V32](https://github.com/advpeterrobinson-hash/vpin-cabinet/blob/feat/cabinet-review-v32/exports/generated/cabinet-v32/README.pt-BR.md) reúne CAD, STEP, dimensões e bloqueios. O material antigo deste branch é histórico e não substitui V32.

- Gabinete de 600 mm, interior nominal de 564 mm e compensado nominal de 18 mm; fabricação depende da espessura medida.
- Playfield independente de modelo: envelope de 560 × 970 × 55 mm e até 12 kg.
- Prateleiras removíveis S1/S2/S3, travessas T1/T2/T3 e guias substituíveis.
- PC aberto baixo sobre PCBase, sem gaveta.
- Dois fans traseiros de referência de 120 mm.
- Pernas clássicas e mobilidade por dispositivos externos removíveis tipo PinSkates; sem rodas integradas.
- **Playfield levantado manualmente, com duas escoras cativas e pinos/travas positivos; sem amortecedores a gás.** Ambas devem ficar engatadas durante manutenção; cada uma deve passar individualmente pela prova de retenção da carga completa. Geometria final de pivô/escoras e movimentos de serviço ainda precisam ser definidos e validados para V32.
- DOF/SSF e iluminação modulares; entrada única aterrada, com distribuição de rede em invólucro protegido contra toque.

A madeira e a estrutura devem sobreviver a gerações de eletrônica. O backbox tem alvo de 780 mm e envelope substituível de display de 740 × 450 × 100 mm; carriers e adaptadores evitam amarrar a estrutura permanente a um componente específico.

## Revisão e validação

V32 tem 45 sólidos válidos e nenhuma interseção detectada acima de 0,01 mm³. Isso comprova posicionamento, **não** resistência, movimento, encaixe de hardware ou fabricação.

Scripts e parâmetros documentados são a fonte de verdade. No branch V32, `make review-v32` regenera CAD e galeria, verifica sólidos salvos/metadados bilíngues e rejeita alterações geométricas inesperadas contra a evidência versionada. O pipeline v25–v27 permanece **PRE-V32**, preservado por suas dependências vivas. Veja a [auditoria local](https://github.com/advpeterrobinson-hash/vpin-cabinet/blob/feat/cabinet-review-v32/docs/pt-BR/V32_LOCAL_AUDIT.md).

## Licença e participação

Material original sob **CERN-OHL-S-2.0**, com uso comercial permitido e obrigações recíprocas de disponibilização do fonte aplicável conforme [LICENSE](LICENSE). Preserve [NOTICE.md](NOTICE.md) e o Source Location oficial: https://github.com/advpeterrobinson-hash/vpin-cabinet.

Consulte [CONTRIBUTING.md](CONTRIBUTING.md), [GOVERNANCE.md](GOVERNANCE.md), [SUPPORT.md](SUPPORT.md), [SECURITY.md](SECURITY.md) e [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md). O [FAQ de licenciamento](docs/LICENSING_FAQ.md) e a [política open-source](docs/OPEN_SOURCE_POLICY.md) detalham as regras; em caso de divergência documental, o inglês é canônico.

Nenhum arquivo CNC está aprovado: hardware medido, estoque, ferramenta, coupon físico, provas e aprovação de fabricação continuam pendentes.
