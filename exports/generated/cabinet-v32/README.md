# V32 — Gabinete central / Main cabinet

**Revisão para discussão — não liberada para CNC. / Design review — not released for machining.**

Esta revisão consolida a direção do proprietário: gabinete convencional, três prateleiras transversais estreitas, PC baixo e peças substituíveis. Os nomes no FreeCAD, na lista de peças e nas imagens estão em português e inglês. Dimensões em milímetros.

This revision consolidates the owner's direction: a conventional cabinet, three narrow transverse shelves, a low PC base and replaceable parts. FreeCAD labels, the parts list and images use Portuguese and English. Dimensions are in millimetres.

## Galeria / Gallery

### 1. Interior / Interior
![Prateleiras e PC / Shelves and PC](01-interior.png)

### 2. Travessas verticais / Upright crossmembers
![Travessas, guias e suporte do monitor / Crossmembers, guides and monitor support](02-travessas.png)

### 3. Planta / Plan
![Prateleiras e espaços de acesso / Shelves and access gaps](03-planta.png)

### 4. Traseira / Rear
![Porta com duas ventoinhas / Door with two exhaust fans](04-traseira.png)

### 5. Guia substituível / Replaceable guide
![Detalhe do encaixe / Guide detail](05-encaixe.png)

### 6. Frente / Front
![Coin door, botões e reserva do plunger / Coin door, buttons and plunger reserve](06-frente.png)

## Incorporado / Incorporated

| Elemento / Element | Configuração / Configuration |
|---|---|
| Corpo / Body | 600 × 1308,1 mm; alturas / heights 400,05–596,9 mm; compensado / plywood 18 mm nominal |
| Prateleiras / Shelves | 3 × 560 × 150 × 12 mm; Y120, Y600, Y1080; alturas inferiores / underside heights Z160, Z180, Z240 |
| Acesso à fiação / Wiring access | 330 mm entre prateleiras / between shelves; acesso por ambos os lados / access from both edges |
| Travessas / Crossmembers | 3 peças verticais / upright pieces; 539,6 × 18 mm; altura central / centre height 80 mm; Y380, Y700, Y980 |
| Guias / Guides | 6 × 18 × 60 × 145 mm; ranhura / groove 18,4 mm wide × 6 mm deep; 12 mm de fundo / remaining guide backing |
| Cantoneiras / Support angles | 6 envelopes genéricos / generic envelopes, 40 × 40 × 50 × 3 mm; apoio sob a travessa / positive seat under beam |
| Áudio / Audio | StarTech ICUSBAUDIO7D selecionada / selected; corpo / body 100 × 60 × 25 mm, representado em P1 / shown on P1 |
| PC | Base / base 285 × 460 × 18 mm sobre o piso / on floor; envelope 265 × 440 × 128 mm; sem gaveta / no drawer |
| Ventilação / Ventilation | 2 × 120 mm na porta traseira / on rear access door; exaustão / exhaust; entrada inferior / bottom intake |
| Coin door | Abertura de referência / reference opening 311,15 × 264,32 mm |
| Fundo / Bottom | Subwoofer Ø139,7 provisório / provisional; ar / intake 100 × 160; 4 botões / buttons Ø28 nominal |

A travessa desliza para cima após remover o suporte do monitor e soltar sua retenção. O rasgo está na guia substituível, não na lateral estrutural. A face superior da travessa tem um chanfro que acompanha o plano do monitor; isso precisa constar da operação CNC. O comprimento reduzido acomoda o encaixe nas guias. As primeiras travessas horizontais da V29 foram substituídas, não duplicadas.

The crossmember lifts out after the monitor support and retention hardware are removed. Its slot is in the replaceable guide, not the structural cabinet wall. The beam's top bevel follows the monitor plane and must be included in the CNC operation. The shorter span accommodates the guides. These beams replace the V29 flat crossmembers rather than adding another set.

Os três níveis de furos das cantoneiras ilustram posições a cada 10 mm. Os parafusos, insertos/porcas, distâncias finais e retenção contra levantamento continuam provisórios. Alterar a altura de uma travessa também altera o apoio do monitor; não ajustar uma isoladamente mantendo as outras fixas sem verificar o plano. Os pontos de montagem CSD não foram inventados.

The angle-hole rows illustrate 10 mm height steps. Screws, inserts/nuts, final edge distances and anti-lift retention remain provisional. Moving a crossmember changes monitor support height; do not move one independently without checking the support plane. CSD mounting holes have not been invented.

## Interfaces e compras / Interfaces and purchases

- **1 StarTech ICUSBAUDIO7D:** seleção do proprietário, compra não confirmada / owner selected, purchase not confirmed. Corpo modelado; cabos, portas e suporte removível ainda exigem folga / body modelled; cables, ports and removable retention still require clearance.
- **2 fans de 120 mm / 120 mm fans:** modelo elétrico não selecionado / electrical model not selected. Quadro de 25 mm e passo 105 mm usados como referência / 25 mm frame and 105 mm hole pitch used as reference. Ø116 e Ø4,5 são decisões provisórias de recorte/furação / provisional cutout and screw-hole decisions.
- **Grelhas e chicote / Guards and harness:** proteção nas faces acessíveis e conector para retirar a porta / guards on accessible faces and a disconnectable door harness. Não modelados / not modelled.
- **6 cantoneiras / support angles:** quantidade de conceito / concept quantity. O envelope não é especificação de compra nem classificação de carga / envelope is not a purchasing specification or load rating.
- **Bornes com tampa / covered terminal blocks:** mantidos como preferência de distribuição; quantidades e correntes pendentes / retained distribution preference; quantities and ratings pending.
- **Williams:** pernas, chapas internas, dobradiças do backbox e suas fixações continuam previstas / legs, inner plates, backbox hinges and their fixings remain planned. A furação completa não está resolvida / full mounting pattern unresolved.

A P3 ampliada termina em Y1230; os fans começam em Y1265,1, deixando 35,1 mm brutos entre ambos. Fans começam em Z220; PC termina em Z182: 38 mm brutos. Grelhas e fios não estão incluídos nessas folgas. A entrada de ar tem 160 cm² brutos; as duas saídas circulares somam cerca de 211 cm². Não é uma validação de vazão ou temperatura.

The enlarged P3 ends at Y1230; fan bodies start at Y1265.1, leaving 35.1 mm gross clearance. Fans start at Z220; the PC ends at Z182, giving 38 mm gross clearance. Guards and wires are excluded. Intake gross area is 160 cm²; the two circular outlets total about 211 cm². This does not validate airflow or temperature.

## Validação e próximos detalhes / Validation and remaining details

**45 sólidos válidos; nenhuma interseção acima de 0,01 mm³. / 45 valid solids; no positive-volume intersection above 0.01 mm³.** Three shelves, three upright beams and two fans are checked by the build script. Names are bilingual. Images were reviewed for readability. The drawings show packaging, not tested load-bearing performance.

Ainda faltam / Still required:

1. Fixações completas das guias, travessas, cantoneiras, prateleiras e porta; acesso a porcas/insertos e retenção contra vibração / complete fixing, nut/insert access and vibration retention.
2. Ferragens, curso e sustentação do monitor aberto; estrutura com cargas reais / monitor service movement and support, actual load verification.
3. Furação das pernas Williams, dobradiças/base do backbox, passagem de cabos e giro / Williams leg pattern, backbox hinge/base fixings, cable passage and sweep.
4. Recortes definitivos do plunger Arnoz, entrada elétrica, RJ45, grelhas e subwoofer escolhido / final selected-component openings.
5. Dimensões das fontes e do conjunto CSD, cabos e zonas térmicas / PSU and CSD dimensions, cables and thermal clearances.
6. Encaixes, canais de vidro, lockdown bar, espessura real da madeira, fresa, raios, folgas e plano de chapas / joints, glass channels, lockdown bar, measured stock, cutter, radii, allowances and sheet layout.

A direção de arquitetura está definida pelo proprietário. A liberação de usinagem não está. Sessões físicas permanecem pausadas. / The owner has set the architecture direction. Machining is not released. Physical sessions remain paused.

## Arquivos / Files

- [FreeCAD](vpin-central-v32.FCStd) — nomes bilíngues / bilingual labels.
- [STEP](vpin-central-v32.step) — peças físicas e envelopes genéricos das ferragens / physical parts and generic hardware envelopes; display, PC body, audio body and reserved zones omitted.
- [Lista de peças / Parts list](PECAS-PARTS.md).
- [Fonte do CAD / CAD source](build_v32.py) — executar com FreeCAD / run with FreeCAD; writes outputs to its own directory.
- [Fonte das imagens / Image source](render_v32.py) — run after CAD generation using Python, NumPy and Matplotlib.
- [Verificação / Validation](validation.json).

A geometria intermediária `geometry.json` é regenerada pelo script CAD. As imagens 01/02 usam transparência de escopo (painéis ocultados), não representam ausência de paredes; os desenhos 03–06 são vistas de revisão dimensionadas. / Intermediate geometry.json is regenerated by the CAD script. Views 01/02 hide panels to expose internal parts; 03–06 are dimensioned review drawings.

## Referências / References

- [WPC dimensional reference](https://github.com/jonaskello/wpc-cabinet) — dimensional facts only; external CAD not copied.
- [StarTech datasheet](https://media.startech.com/cms/pdfs/icusbaudio7d_datasheet.pdf).
- [120 mm fan dimensional reference](https://www.noctua.at/en/products/nf-a12x25-pwm/specifications) — not a fan selection.
- [Cleveland solenoid](https://www.clevelandsoftwaredesign.com/pinball-parts/p/high-quality-solenoid) — mounting pattern still unconfirmed.

## Proveniência / Provenance

Revisão local V32, 26/09/2026, consolidando V29–V31. Publicação em branch de revisão separado, derivado do commit remoto 9ec47db. O commit local bae2ff2 e as alterações pessoais do master não são sobrescritos nem incorporados por esta publicação. A geometria ativa de fabricação permanece intacta. / Local V32 consolidates V29–V31 and is published on a separate review branch based on remote commit 9ec47db. Local commit bae2ff2 and personal master edits are not overwritten or included. Active manufacturing geometry remains untouched.

Copyright © 2026 Peter Jr. and contributors. CERN-OHL-S-2.0. See [LICENSE](LICENSE) and [NOTICE](NOTICE.md). Official source: https://github.com/advpeterrobinson-hash/vpin-cabinet . This modified review source is supplied alongside its images and CAD.
