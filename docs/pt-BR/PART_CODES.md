# Sistema de códigos permanentes de peças

[English](../PART_CODES.md) · [Português (Brasil)](PART_CODES.md)

## Objetivo

O projeto usa uma identidade curta e estável para cada peça aceita, reduzindo ambiguidade entre CAD, renderizações, BOM, montagem e discussões de design.

Um código representa **a função da peça**, não apenas um nome temporário de arquivo.

## Regras principais

1. Enquanto uma peça ou conceito ainda estiver em avaliação, a documentação mostra o nome em negrito, por exemplo **suporte provisório do ventilador**.
2. Quando a proposta dessa peça for aceita na arquitetura, ela recebe um código permanente.
3. O código permanente **nunca é reutilizado** para outra função, mesmo se a peça original for posteriormente retirada.
4. Alterações de geometria que preservem a função mantêm o código e avançam a revisão, por exemplo `T1-R2`, `T1-R3`.
5. Uma função diferente recebe outro código.
6. Os códigos devem aparecer no CAD, BOM, desenhos, documentação e, quando legível, nas futuras renderizações.

## Convenção

- `T#` — travessa estrutural.
- `S#` — prateleira.
- `S#SupL`, `S#SupR` — suporte esquerdo/direito da prateleira.
- `T#GuideL`, `T#GuideR` — guia substituível esquerda/direita da travessa.
- `T#SupL`, `T#SupR` — apoio/cantoneira esquerda/direita da travessa quando finalizado.
- `MonRailL`, `MonRailR`, `MonBridge` — peças principais do suporte do monitor.
- `SideL`, `SideR`, `Front`, `Rear`, `Floor` — painéis principais do gabinete.
- `RearDoor` — porta traseira de serviço.
- `PCBase` — base inferior do PC.
- `BBBase` — base/apoio do backbox.

`L` e `R` são definidos olhando o gabinete pela frente, salvo indicação expressa em contrário.

## Registro V32

| Código permanente | ID legado V32 | Função | Estado |
|---|---|---|---|
| SideL | SIDE_L | lateral esquerda | arquitetura aceita; furação final ainda bloqueada |
| SideR | SIDE_R | lateral direita | arquitetura aceita; furação final ainda bloqueada |
| Front | FRONT | painel frontal | arquitetura aceita; alguns recortes ainda pendentes |
| Rear | REAR | painel traseiro | arquitetura aceita; interfaces de componentes pendentes |
| RearDoor | REAR_DOOR | porta traseira de serviço | arquitetura aceita; ferragens pendentes |
| Floor | FLOOR | piso | arquitetura aceita; recortes finais pendentes |
| S1 | SHELF_1 | prateleira transversal dianteira | aceita na arquitetura V32 |
| S1SupL | SHELF_SUPPORT_1L | apoio esquerdo de S1 | aceito; fixação pendente |
| S1SupR | SHELF_SUPPORT_1R | apoio direito de S1 | aceito; fixação pendente |
| S2 | SHELF_2 | prateleira transversal central | aceita na arquitetura V32 |
| S2SupL | SHELF_SUPPORT_2L | apoio esquerdo de S2 | aceito; fixação pendente |
| S2SupR | SHELF_SUPPORT_2R | apoio direito de S2 | aceito; fixação pendente |
| S3 | SHELF_3 | prateleira transversal traseira | aceita na arquitetura V32 |
| S3SupL | SHELF_SUPPORT_3L | apoio esquerdo de S3 | aceito; fixação pendente |
| S3SupR | SHELF_SUPPORT_3R | apoio direito de S3 | aceito; fixação pendente |
| T1 | CROSS_1 | travessa vertical dianteira | aceita na arquitetura V32 |
| T1GuideL | CROSS_GUIDE_1L | guia substituível esquerda de T1 | conceito aceito; ferragens pendentes |
| T1GuideR | CROSS_GUIDE_1R | guia substituível direita de T1 | conceito aceito; ferragens pendentes |
| T2 | CROSS_2 | travessa vertical central | aceita na arquitetura V32 |
| T2GuideL | CROSS_GUIDE_2L | guia substituível esquerda de T2 | conceito aceito; ferragens pendentes |
| T2GuideR | CROSS_GUIDE_2R | guia substituível direita de T2 | conceito aceito; ferragens pendentes |
| T3 | CROSS_3 | travessa vertical traseira | aceita na arquitetura V32 |
| T3GuideL | CROSS_GUIDE_3L | guia substituível esquerda de T3 | conceito aceito; ferragens pendentes |
| T3GuideR | CROSS_GUIDE_3R | guia substituível direita de T3 | conceito aceito; ferragens pendentes |
| MonRailL | MONITOR_RAIL_L | régua esquerda do monitor | arquitetura aceita; fixação final pendente |
| MonRailR | MONITOR_RAIL_R | régua direita do monitor | arquitetura aceita; fixação final pendente |
| MonBridge | MONITOR_BRIDGE | ponte VESA substituível | função aceita; furos do display pendentes |
| PCBase | PC_BASE | base inferior do PC | arquitetura aceita |
| BBBase | BACKBOX_BASE | base/apoio do backbox | função aceita; ferragens Williams pendentes |

## Nomes provisórios

Os itens abaixo permanecem deliberadamente sem código permanente:

- **apoio metálico ajustável esquerdo/direito de T1**
- **apoio metálico ajustável esquerdo/direito de T2**
- **apoio metálico ajustável esquerdo/direito de T3**
- **ventilador traseiro esquerdo**
- **ventilador traseiro direito**
- **suporte removível da StarTech ICUSBAUDIO7D**
- **plunger Arnoz e respectivo suporte**
- **interface definitiva de rede/RJ45**
- **interface definitiva de entrada elétrica/master disconnect**
- **subwoofer definitivo**
- **grelhas dos ventiladores**
- **chicote removível da porta traseira**

IDs legados como `CROSS_BRACKET_*`, `FAN_*` e envelopes reservados permanecem na V32 para rastreabilidade, mas não são códigos permanentes.

## Migração CAD

A V32 publicada preserva IDs internos legados para manter rastreabilidade dos arquivos FreeCAD/STEP existentes. O gerador agora carrega metadados de identidade permanente para a próxima regeneração:

- `PartCode` armazena o código permanente quando atribuído;
- `LegacyId` preserva o identificador interno anterior;
- `PartStatus` diferencia identidade permanente e provisória;
- futuras gerações de BOM/manifesto devem derivar a identidade do mesmo mapa-fonte.

Isso evita renomeação silenciosa e preserva referências históricas.
