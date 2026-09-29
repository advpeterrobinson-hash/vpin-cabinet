# V32 — quatro parafusos por cima

[English / evidência técnica](../SIMPLE_SHELVES_V32.md)

**Esta é a direção atual solicitada pelo proprietário. Substitui a complexidade das tampas de porcas e dos apoios removíveis.**

![Fixação simples](../../exports/generated/side-panel-v32/07-simple-shelves.png)

O uso pretendido é: abrir e apoiar positivamente o playfield, desconectar o chicote da prateleira, soltar **dois parafusos de cada lado, todos por cima**, deslizar a prateleira até o vão de saída e levantar o conjunto com os equipamentos presos nela. Os apoios ficam no gabinete. As roscas ficam presas nos apoios, sem porcas soltas para segurar por baixo.

O novo modelo separado elimina as tampas inferiores e o mecanismo de remoção dos apoios. As três travessas permanecem instaladas nos testes. Os equipamentos precisam deixar livre o espaço de acesso aos quatro parafusos.

A S3 passa a começar em **Y820**, avançando 180 mm em relação à proposta anterior e 260 mm em relação ao V32 original. Seus parafusos ficam em Y845/920. S1 e S2 permanecem na mesma posição; tamanhos, alturas e travessas são preservados. A S3 desliza 60 mm para a frente antes de subir; S1 e S2 mantêm suas rotas anteriores.

As **90 verificações da estrutura fixa passaram**. O novo estudo inclui o conjunto do display levantado em um eixo proposto: a 100° de abertura em relação à posição fechada, próximo da vertical, os 12 acessos superiores e as três rotas carregadas passam. As 51 posições de abertura amostradas a cada 2° não colidem com a cena modelada. Acessos ainda ficam obstruídos entre 60° e 90°; não basta dizer apenas “playfield aberto”.

![Acesso com display levantado](../../exports/generated/side-panel-v32/08-shelf-raised-display.png)

**O eixo é uma hipótese geométrica, não uma dobradiça selecionada.** Escoras, ferragens, cabos, backbox superior e manuseio ainda não foram integrados. Não há prova contínua entre amostras nem aprovação de resistência. O V32 original permanece intacto.

A [tabela de 12 furos](../../exports/generated/side-panel-v32/shelf-hole-schedule-review.csv) registra posições e envelopes atuais. Os centros ficam a 28 mm das bordas laterais de cada prateleira. As medidas dos alojamentos de insertos ainda dependem da ferragem: a tabela é para revisão, não para mandar cortar. A furação de fixação dos apoios à parede permanece pendente.

[Proposta FreeCAD](../../exports/generated/side-panel-v32/simple-shelves-proposal.FCStd) · [Relatório](../../exports/generated/side-panel-v32/simple-shelves-validation.json)

Reproduzir com `bash tools/run_simple_shelves_v32.sh` e `bash tools/run_shelf_service_pose_v32.sh`. Os estudos mais complexos permanecem como histórico; não são a solução atual. As identidades das antigas tampas ficam aposentadas, sem reutilização.

CNC bloqueado. Material original: CERN-OHL-S-2.0. Preservar LICENSE e NOTICE.md. Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet.
