# Peças / Parts

A V32 passa a distinguir **código permanente** de **ID legado**.

- Código permanente: identidade curta e estável da peça já aceita na arquitetura.
- ID legado: identificador técnico preservado no arquivo V32 existente para rastreabilidade.
- `**nome provisório**`: peça/conceito ainda sem identidade permanente.
- Um código nunca é reutilizado para outra função.
- Alterações futuras que preservem a função mantêm o código e avançam a revisão, por exemplo `T1-R2`.

Registro completo: [`docs/PART_CODES.md`](../../../docs/PART_CODES.md).

| Código / Code | ID legado V32 | Português / English | Grupo / Group |
|---|---|---|---|
| SideL | SIDE_L | Lateral esquerda / Left side | shell |
| SideR | SIDE_R | Lateral direita / Right side | shell |
| Front | FRONT | Painel frontal / Front panel | shell |
| Rear | REAR | Painel traseiro / Rear panel | shell |
| — | FAN_230 | **Ventilador traseiro esquerdo / Left rear fan** | fan |
| — | FAN_370 | **Ventilador traseiro direito / Right rear fan** | fan |
| RearDoor | REAR_DOOR | Porta de acesso / Access door | door |
| Floor | FLOOR | Piso / Bottom panel | floor |
| — | FLOOR_CLEAT_18 | **Apoio esquerdo do piso / Left floor support** | support |
| — | FLOOR_CLEAT_552 | **Apoio direito do piso / Right floor support** | support |
| S1 | SHELF_1 | Prateleira transversal 1 / Transverse shelf 1 | shelf |
| S1SupL | SHELF_SUPPORT_1L | Apoio esquerdo de S1 / S1 left support | support |
| S1SupR | SHELF_SUPPORT_1R | Apoio direito de S1 / S1 right support | support |
| S2 | SHELF_2 | Prateleira transversal 2 / Transverse shelf 2 | shelf |
| S2SupL | SHELF_SUPPORT_2L | Apoio esquerdo de S2 / S2 left support | support |
| S2SupR | SHELF_SUPPORT_2R | Apoio direito de S2 / S2 right support | support |
| S3 | SHELF_3 | Prateleira transversal 3 / Transverse shelf 3 | shelf |
| S3SupL | SHELF_SUPPORT_3L | Apoio esquerdo de S3 / S3 left support | support |
| S3SupR | SHELF_SUPPORT_3R | Apoio direito de S3 / S3 right support | support |
| T1 | CROSS_1 | Travessa vertical 1 / Upright crossmember 1 | brace |
| T1GuideL | CROSS_GUIDE_1L | Guia esquerda de T1 / T1 left guide | guide |
| — | CROSS_BRACKET_1L | **Apoio metálico esquerdo de T1 / T1 left metal support** | bracket |
| T1GuideR | CROSS_GUIDE_1R | Guia direita de T1 / T1 right guide | guide |
| — | CROSS_BRACKET_1R | **Apoio metálico direito de T1 / T1 right metal support** | bracket |
| T2 | CROSS_2 | Travessa vertical 2 / Upright crossmember 2 | brace |
| T2GuideL | CROSS_GUIDE_2L | Guia esquerda de T2 / T2 left guide | guide |
| — | CROSS_BRACKET_2L | **Apoio metálico esquerdo de T2 / T2 left metal support** | bracket |
| T2GuideR | CROSS_GUIDE_2R | Guia direita de T2 / T2 right guide | guide |
| — | CROSS_BRACKET_2R | **Apoio metálico direito de T2 / T2 right metal support** | bracket |
| T3 | CROSS_3 | Travessa vertical 3 / Upright crossmember 3 | brace |
| T3GuideL | CROSS_GUIDE_3L | Guia esquerda de T3 / T3 left guide | guide |
| — | CROSS_BRACKET_3L | **Apoio metálico esquerdo de T3 / T3 left metal support** | bracket |
| T3GuideR | CROSS_GUIDE_3R | Guia direita de T3 / T3 right guide | guide |
| — | CROSS_BRACKET_3R | **Apoio metálico direito de T3 / T3 right metal support** | bracket |
| MonRailL | MONITOR_RAIL_L | Régua esquerda do monitor / Left monitor rail | mount |
| MonRailR | MONITOR_RAIL_R | Régua direita do monitor / Right monitor rail | mount |
| MonBridge | MONITOR_BRIDGE | Ponte VESA / VESA bridge | mount |
| — | PLAYFIELD_ENVELOPE | Espaço do monitor / Display envelope | envelope |
| — | AUDIO_STARTECH | StarTech ICUSBAUDIO7D selecionada / selected device | audio |
| PCBase | PC_BASE | Base do PC / PC base | pcbase |
| — | PC_ENVELOPE | Espaço do PC / PC envelope | pc |
| BBBase | BACKBOX_BASE | Base do backbox / Backbox support | shell |
| — | PLUNGER_RESERVED | **Reserva do plunger / Plunger reserve** | reserved |
| — | MAINS_RESERVED | **Reserva da entrada elétrica / Mains inlet reserve** | reserved |
| — | RJ45_RESERVED | **Reserva de rede / Network reserve** | reserved |

## Observação sobre peças provisórias

A marcação em negrito não significa que o item é descartável. Significa apenas que **a identidade final ainda não foi concedida**. Quando a proposta for aceita, o item recebe um código permanente e esse código passa a ser a referência para CAD, BOM, renderizações, montagem e futuras revisões.

Os suportes atuais do piso permanecem provisórios porque a proposta de encaixe capturado CNC pode eliminá-los ou alterar sua função. Veja [`docs/CABINET_JOINERY_PROPOSAL.md`](../../../docs/CABINET_JOINERY_PROPOSAL.md).
