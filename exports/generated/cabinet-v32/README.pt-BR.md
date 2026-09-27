# V32 — Gabinete central

[English](README.md) · **Português (Brasil)**

> **Revisão de design — não liberada para CNC ou fabricação.**

A V32 consolida a direção atual do proprietário: gabinete convencional de 600 mm, três prateleiras transversais estreitas, PC open-case baixo e interfaces substituíveis. Dimensões em milímetros.

**Acesso rápido:** [galeria dedicada](../../../docs/pt-BR/RENDERS.md) · [códigos permanentes](../../../docs/pt-BR/PART_CODES.md) · [proposta atual de encaixe CNC](../../../docs/pt-BR/CABINET_JOINERY_PROPOSAL.md).

## Identidade das peças

A V32 usa códigos humanos permanentes para peças aceitas, incluindo `T1`, `T2`, `T3`, `S1`, `S2`, `S3`, `S1SupL` e `S1SupR`.

Conceitos ainda não finalizados permanecem **provisórios** e não recebem código permanente antes de sua aceitação. O registro mestre está em [PART_CODES.md](../../../docs/pt-BR/PART_CODES.md).

Os arquivos FreeCAD/STEP V32 publicados ainda preservam IDs internos legados para rastreabilidade. O gerador-fonte agora contém metadados para código permanente, ID legado, estado e nome PT-BR separado.

## Galeria

### 1. Interior
![Prateleiras e PC](01-interior.png)

### 2. Travessas verticais
![Travessas, guias e suporte do monitor](02-travessas.png)

### 3. Planta de serviço
![Prateleiras e espaços de acesso](03-planta.png)

### 4. Traseira
![Porta com dois ventiladores](04-traseira.png)

### 5. Guia substituível
![Detalhe da guia](05-encaixe.png)

### 6. Frente
![Coin door, comandos e reserva do plunger](06-frente.png)

Para navegação mais fácil, use a [página dedicada de renderizações](../../../docs/pt-BR/RENDERS.md).

## Incorporado na V32

| Elemento | Configuração |
|---|---|
| Corpo | 600 × 1308,1 mm; alturas dianteira/traseira 400,05–596,9 mm; compensado nominal de 18 mm |
| Prateleiras | S1/S2/S3: 3 × 560 × 150 × 12 mm; Y120, Y600, Y1080; alturas inferiores Z160, Z180, Z240 |
| Acesso à fiação | 330 mm entre prateleiras; acesso por ambas as bordas |
| Travessas | T1/T2/T3: 3 peças verticais; 539,6 × 18 mm; altura central 80 mm; Y380, Y700, Y980 |
| Guias | 6 guias substituíveis; 18 × 60 × 145 mm; ranhura 18,4 mm × 6 mm; 12 mm de material mantido |
| **Apoios metálicos das travessas** | 6 envelopes genéricos provisórios, 40 × 40 × 50 × 3 mm; apoio positivo sob a travessa |
| Áudio | StarTech ICUSBAUDIO7D selecionada; corpo 100 × 60 × 25 mm mostrado próximo de S1 |
| PC | PCBase 285 × 460 × 18 mm sobre o piso; envelope do PC 265 × 440 × 128 mm; sem gaveta |
| Ventilação | 2 ventiladores traseiros provisórios de 120 mm; entrada inferior |
| Coin door | abertura de referência 311,15 × 264,32 mm |
| Piso | abertura provisória Ø139,7 para subwoofer; entrada de ar 100 × 160; quatro furos auxiliares Ø28 nominais |

T1/T2/T3 saem para cima após remover o suporte do monitor e liberar sua retenção. A ranhura fica na guia substituível, não na lateral estrutural. O chanfro superior da travessa acompanha o plano do monitor e deverá constar dos dados finais de usinagem.

Os três níveis ilustrados de apoio têm incrementos de 10 mm. Parafusos, inserts/porcas, distâncias finais de borda e retenção contra levantamento continuam provisórios. Alterar a altura de uma travessa também altera o plano de apoio do monitor.

## Interfaces e compras

- **StarTech ICUSBAUDIO7D:** selecionada pelo proprietário; compra não confirmada.
- **Dois ventiladores de 120 mm:** modelo elétrico final ainda não selecionado; geometria atual é apenas referência.
- **Grelhas e chicote da porta traseira:** necessários, ainda não modelados.
- **Seis apoios das travessas:** quantidade conceitual; envelope genérico não é especificação de compra nem classificação de carga.
- **Bornes com tampa:** preferência mantida; quantidades/correntes pendentes.
- **Ferragens Williams:** pernas, chapas internas, dobradiças do backbox e fixações continuam previstas; padrões completos ainda não resolvidos.

S3 termina em Y1230; os ventiladores começam em Y1265,1, deixando 35,1 mm brutos. Os ventiladores começam em Z220; o envelope do PC termina em Z182, deixando 38 mm brutos. Grelhas e fios não estão incluídos.

A entrada inferior tem 160 cm² de área bruta; as duas saídas circulares somam cerca de 211 cm². Isso **não** constitui validação térmica ou de fluxo.

## Validação e trabalho restante

**45 sólidos válidos; nenhuma interseção de volume positivo acima de 0,01 mm³.**

Isso valida empacotamento/interferência CAD, não resistência estrutural testada.

Ainda faltam:

1. fixações completas de guias, travessas, apoios, prateleiras e porta;
2. ferragens de serviço/sustentação do monitor e validação com cargas reais;
3. padrões Williams das pernas e dobradiças/base do backbox, passagem de cabos e sweep;
4. recortes finais dos componentes selecionados;
5. dimensões PSU/CSD, roteamento de cabos e zonas térmicas;
6. encaixes, canais do vidro, lockdown bar, espessura real da madeira, fresa, raios, folgas e plano de chapas.

A direção de arquitetura está definida para a revisão atual. A usinagem não está liberada. Sessões físicas permanecem pausadas.

A proposta de encaixe CNC autoindexado do gabinete inferior está documentada separadamente e **ainda não faz parte da geometria V32**: [CABINET_JOINERY_PROPOSAL.md](../../../docs/pt-BR/CABINET_JOINERY_PROPOSAL.md).

## Arquivos

- [FreeCAD](vpin-central-v32.FCStd) — arquivo de revisão publicado; o binário salvo tem códigos de peças, labels em inglês e metadados NameEN/NamePTBR verificados.
- [STEP](vpin-central-v32.step).
- [Lista de peças](PECAS-PARTS.pt-BR.md).
- [Fonte do CAD](build_v32.py).
- [Fonte das renderizações](render_v32.py).
- [Validação](validation.json).

## Proveniência

A V32 consolida V29–V31 e foi publicada em branch de revisão separado derivado do commit remoto `9ec47db`. O master local preexistente e alterações do proprietário não foram sobrescritos ou incorporados nessa publicação.

Copyright © 2026 Peter Jr. e colaboradores. CERN-OHL-S-2.0. Veja [LICENSE](LICENSE) e [NOTICE](NOTICE.md). Fonte oficial: https://github.com/advpeterrobinson-hash/vpin-cabinet .
