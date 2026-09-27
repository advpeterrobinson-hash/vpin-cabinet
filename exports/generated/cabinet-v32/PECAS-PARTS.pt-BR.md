# Peças

[English](PECAS-PARTS.md) · **Português (Brasil)**

A V32 distingue **código permanente** de **ID interno legado**.

- Código permanente: identidade curta e estável de uma peça aceita.
- ID legado: identificador técnico preservado para rastreabilidade no modelo V32 publicado.
- **nome provisório**: conceito que ainda não possui identidade permanente.
- Um código permanente nunca é reutilizado para outra função.
- Alterações de geometria que preservem a função mantêm o código e avançam a revisão, por exemplo `T1-R2`.

Registro mestre: [`docs/pt-BR/PART_CODES.md`](../../../docs/pt-BR/PART_CODES.md).

| Código | ID legado V32 | Nome em português | Grupo |
|---|---|---|---|
| SideL | SIDE_L | Lateral esquerda | shell |
| SideR | SIDE_R | Lateral direita | shell |
| Front | FRONT | Painel frontal | shell |
| Rear | REAR | Painel traseiro | shell |
| — | FAN_230 | **Ventilador traseiro esquerdo** | fan |
| — | FAN_370 | **Ventilador traseiro direito** | fan |
| RearDoor | REAR_DOOR | Porta traseira de serviço | door |
| Floor | FLOOR | Piso | floor |
| — | FLOOR_CLEAT_18 | **Apoio esquerdo do piso** | support |
| — | FLOOR_CLEAT_552 | **Apoio direito do piso** | support |
| S1 | SHELF_1 | Prateleira transversal 1 | shelf |
| S1SupL | SHELF_SUPPORT_1L | Apoio esquerdo de S1 | support |
| S1SupR | SHELF_SUPPORT_1R | Apoio direito de S1 | support |
| S2 | SHELF_2 | Prateleira transversal 2 | shelf |
| S2SupL | SHELF_SUPPORT_2L | Apoio esquerdo de S2 | support |
| S2SupR | SHELF_SUPPORT_2R | Apoio direito de S2 | support |
| S3 | SHELF_3 | Prateleira transversal 3 | shelf |
| S3SupL | SHELF_SUPPORT_3L | Apoio esquerdo de S3 | support |
| S3SupR | SHELF_SUPPORT_3R | Apoio direito de S3 | support |
| T1 | CROSS_1 | Travessa vertical 1 | brace |
| T1GuideL | CROSS_GUIDE_1L | Guia esquerda de T1 | guide |
| — | CROSS_BRACKET_1L | **Apoio metálico esquerdo de T1** | bracket |
| T1GuideR | CROSS_GUIDE_1R | Guia direita de T1 | guide |
| — | CROSS_BRACKET_1R | **Apoio metálico direito de T1** | bracket |
| T2 | CROSS_2 | Travessa vertical 2 | brace |
| T2GuideL | CROSS_GUIDE_2L | Guia esquerda de T2 | guide |
| — | CROSS_BRACKET_2L | **Apoio metálico esquerdo de T2** | bracket |
| T2GuideR | CROSS_GUIDE_2R | Guia direita de T2 | guide |
| — | CROSS_BRACKET_2R | **Apoio metálico direito de T2** | bracket |
| T3 | CROSS_3 | Travessa vertical 3 | brace |
| T3GuideL | CROSS_GUIDE_3L | Guia esquerda de T3 | guide |
| — | CROSS_BRACKET_3L | **Apoio metálico esquerdo de T3** | bracket |
| T3GuideR | CROSS_GUIDE_3R | Guia direita de T3 | guide |
| — | CROSS_BRACKET_3R | **Apoio metálico direito de T3** | bracket |
| MonRailL | MONITOR_RAIL_L | Régua esquerda do monitor | mount |
| MonRailR | MONITOR_RAIL_R | Régua direita do monitor | mount |
| MonBridge | MONITOR_BRIDGE | Ponte VESA | mount |
| — | PLAYFIELD_ENVELOPE | Envelope do display | envelope |
| — | AUDIO_STARTECH | StarTech ICUSBAUDIO7D selecionada | audio |
| PCBase | PC_BASE | Base do PC | pcbase |
| — | PC_ENVELOPE | Envelope do PC | pc |
| BBBase | BACKBOX_BASE | Base/apoio do backbox | shell |
| — | PLUNGER_RESERVED | **Reserva do plunger** | reserved |
| — | MAINS_RESERVED | **Reserva da entrada elétrica** | reserved |
| — | RJ45_RESERVED | **Reserva de rede** | reserved |

## Itens provisórios

Nomes provisórios em negrito não significam que o item seja descartável. Significam apenas que **a identidade final ainda não foi concedida**.

Os apoios atuais do piso permanecem provisórios porque a proposta de encaixe capturado CNC pode eliminá-los ou redefinir sua função. Veja [`docs/pt-BR/CABINET_JOINERY_PROPOSAL.md`](../../../docs/pt-BR/CABINET_JOINERY_PROPOSAL.md).
