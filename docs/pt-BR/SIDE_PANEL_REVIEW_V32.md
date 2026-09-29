# V32: revisão das interfaces laterais

[English](../SIDE_PANEL_REVIEW_V32.md)

Auditoria somente de leitura dos sólidos salvos. **Compatibilidade com ferragens NÃO VERIFICADA; CNC BLOQUEADO.** Nenhum painel foi recortado.

As laterais são simétricas em X300, com espessura nominal de 18 mm e comprimento de 1308,1 mm. Os dois botões de cada lado ficam em Y255/310 e Z270, separados por 55 mm. Os furos passantes existentes têm Ø15,875 mm; não devem ser confundidos com os furos frontais nominais de Ø25,4 mm.

Os rebaixos de Ø28,575 mm têm profundidades externa/interna de 7,9375/4,7625 mm. Restam **5,3 mm no anel de fixação**, ainda sem comprovação de resistência ou compatibilidade com rosca, porca e arruela. Não se trata do bolsão de OLED.

Volumes provisórios de raio 18 mm e profundidade interna de 80 mm (60 de corpo +20 para cabo) não colidem com os sólidos vizinhos modelados. Ferragens ausentes não estão cobertas por esse resultado. O pivô de referência Ø12,7 em Y1270/Z508 deixa 31,75 mm até a borda traseira e 82,55 mm até o topo; fixação e reforço reais permanecem pendentes.

A auditoria passou em 46 verificações, incluindo um controle negativo com deslocamento lateral de 1 mm. O FCStd original permaneceu idêntico. Próximos passos: interfaces das pernas e lockdown, montagem SSF, cargas e movimento dos apoios cativos/playfield, canal do vidro e juntas aceitas. Depois, traseira e fundo. Consulte o [relatório completo e comando de execução](../SIDE_PANEL_REVIEW_V32.md).

O [plano de interfaces laterais](../SIDE_INTERFACE_PLAN_V32.md) registra os referenciais compartilhados, as regiões ocupadas por sete pares de apoios, alternativas de rebaixo dos botões e os caminhos propostos de carga e manutenção. A extensão da auditoria verifica a simetria dos sete pares e os 14 contatos com o plano interno nominal; não comprova acesso às ferragens nem resistência.

## Acesso às fixações das guias

O [estudo de acesso](../SIDE_SERVICE_REVIEW_V32.md) testou 24 posições com dois volumes provisórios de ferramenta. Com tudo montado, as réguas do monitor bloqueiam seis posições para o volume compacto (Ø16 × 100 mm). Removido o conjunto do monitor, esse volume fica livre nas 24 posições. O volume maior (Ø30 × 150 mm) exige também a remoção das três travessas. A sequência real de desmontagem ainda precisa ser comprovada, sem depender dos próprios parafusos bloqueados. Foram 144 combinações e 29 verificações da auditoria; isso não significa 144 acessos livres. Nenhuma furação foi alterada.

O [estudo de movimento contínuo](SIDE_MOTION_REVIEW_V32.md) agora verifica a extração das travessas e a retirada das três prateleiras por deslocamento horizontal seguido de subida, inclusive com envelopes de equipamentos de 60 mm. Há posições intermediárias salvas em FreeCAD e um comando único para as três auditorias.
