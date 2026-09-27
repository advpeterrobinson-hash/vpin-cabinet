# Sistema de códigos permanentes de peças / Permanent part-code system

## Objetivo

O projeto passa a usar uma identidade curta e estável por peça para reduzir ambiguidade entre CAD, renderizações, BOM, montagem e discussão.

Um código representa **a função daquela peça**, não apenas um nome temporário de arquivo.

### Regra principal

1. Enquanto uma peça/conceito ainda estiver em avaliação, o nome aparece em Markdown entre dois asteriscos, por exemplo: `**suporte provisório do fan**`.
2. Quando a proposta daquela peça for aceita como parte da arquitetura, ela recebe um código permanente.
3. O código **não é reutilizado** para outra função mesmo se a peça for retirada posteriormente.
4. Alterações de geometria que preservem a mesma função mantêm o código e avançam a revisão: `T1-R2`, `T1-R3`.
5. Uma mudança que crie outra função recebe novo código.
6. Códigos devem aparecer em CAD, BOM, desenhos, documentação e, quando legível, nas renderizações futuras.

## Convenção

A convenção favorece leitura humana, conforme direção do proprietário:

- `T#` — travessa estrutural / crossmember.
- `S#` — prateleira / shelf.
- `S#SupL`, `S#SupR` — suporte esquerdo/direito da prateleira.
- `T#GuideL`, `T#GuideR` — guia substituível esquerda/direita da travessa.
- `T#SupL`, `T#SupR` — apoio/cantoneira esquerda/direita da travessa.
- `MonRailL`, `MonRailR`, `MonBridge` — peças do suporte principal do monitor.
- `SideL`, `SideR`, `Front`, `Rear`, `Floor` — painéis principais do gabinete.
- `RearDoor` — porta traseira de serviço.
- `PCBase` — base inferior do PC.
- `BBBase` — base/apoio do backbox.

`L` e `R` são definidos olhando o gabinete pela frente, salvo documentação específica em contrário.

## Registro V32

| Código permanente | ID legado V32 | Função | Estado |
|---|---|---|---|
| SideL | SIDE_L | lateral esquerda | arquitetura aceita; detalhes de furação ainda bloqueados |
| SideR | SIDE_R | lateral direita | arquitetura aceita; detalhes de furação ainda bloqueados |
| Front | FRONT | painel frontal | arquitetura aceita; alguns recortes ainda pendentes |
| Rear | REAR | painel traseiro | arquitetura aceita; interfaces específicas pendentes |
| RearDoor | REAR_DOOR | porta traseira de serviço | arquitetura aceita; ferragens pendentes |
| Floor | FLOOR | piso | arquitetura aceita; recortes finais pendentes |
| S1 | SHELF_1 | prateleira transversal dianteira | aceita na arquitetura V32 |
| S1SupL | SHELF_SUPPORT_1L | apoio esquerdo de S1 | aceita na arquitetura V32; fixação pendente |
| S1SupR | SHELF_SUPPORT_1R | apoio direito de S1 | aceita na arquitetura V32; fixação pendente |
| S2 | SHELF_2 | prateleira transversal central | aceita na arquitetura V32 |
| S2SupL | SHELF_SUPPORT_2L | apoio esquerdo de S2 | aceita na arquitetura V32; fixação pendente |
| S2SupR | SHELF_SUPPORT_2R | apoio direito de S2 | aceita na arquitetura V32; fixação pendente |
| S3 | SHELF_3 | prateleira transversal traseira | aceita na arquitetura V32 |
| S3SupL | SHELF_SUPPORT_3L | apoio esquerdo de S3 | aceita na arquitetura V32; fixação pendente |
| S3SupR | SHELF_SUPPORT_3R | apoio direito de S3 | aceita na arquitetura V32; fixação pendente |
| T1 | CROSS_1 | travessa vertical dianteira | aceita na arquitetura V32 |
| T1GuideL | CROSS_GUIDE_1L | guia substituível esquerda de T1 | aceita como conceito; ferragens pendentes |
| T1GuideR | CROSS_GUIDE_1R | guia substituível direita de T1 | aceita como conceito; ferragens pendentes |
| T2 | CROSS_2 | travessa vertical central | aceita na arquitetura V32 |
| T2GuideL | CROSS_GUIDE_2L | guia substituível esquerda de T2 | aceita como conceito; ferragens pendentes |
| T2GuideR | CROSS_GUIDE_2R | guia substituível direita de T2 | aceita como conceito; ferragens pendentes |
| T3 | CROSS_3 | travessa vertical traseira | aceita na arquitetura V32 |
| T3GuideL | CROSS_GUIDE_3L | guia substituível esquerda de T3 | aceita como conceito; ferragens pendentes |
| T3GuideR | CROSS_GUIDE_3R | guia substituível direita de T3 | aceita como conceito; ferragens pendentes |
| MonRailL | MONITOR_RAIL_L | régua esquerda do monitor | arquitetura aceita; fixação final pendente |
| MonRailR | MONITOR_RAIL_R | régua direita do monitor | arquitetura aceita; fixação final pendente |
| MonBridge | MONITOR_BRIDGE | ponte/placa VESA substituível | função aceita; furos do display pendentes |
| PCBase | PC_BASE | base inferior do PC | arquitetura aceita |
| BBBase | BACKBOX_BASE | apoio/base do backbox | função aceita; ferragens Williams pendentes |

## Nomes ainda provisórios

Os itens abaixo permanecem sem código permanente deliberadamente:

- **cantoneira/apoio metálico ajustável de T1 esquerda/direita**
- **cantoneira/apoio metálico ajustável de T2 esquerda/direita**
- **cantoneira/apoio metálico ajustável de T3 esquerda/direita**
- **ventilador traseiro esquerdo**
- **ventilador traseiro direito**
- **suporte removível da StarTech ICUSBAUDIO7D**
- **plunger Arnoz e respectivo suporte**
- **entrada de rede/RJ45 definitiva**
- **entrada elétrica/master disconnect definitiva**
- **subwoofer definitivo**
- **grelhas dos ventiladores**
- **chicote removível da porta traseira**

Os IDs legados `CROSS_BRACKET_*`, `FAN_*` e envelopes reservados continuam existindo no V32 para rastreabilidade, mas não devem ser interpretados como código permanente.

## Migração CAD

O V32 publicado preserva IDs internos legados para não quebrar o arquivo FreeCAD/STEP já gerado. Na próxima regeneração do CAD:

- adicionar propriedade `PartCode` aos objetos;
- mostrar o código permanente no Label bilíngue;
- preservar o ID legado como `LegacyId`;
- não renomear silenciosamente um código já atribuído;
- gerar automaticamente esta relação no BOM/manifesto.

Isso permite migrar sem invalidar referências históricas.
