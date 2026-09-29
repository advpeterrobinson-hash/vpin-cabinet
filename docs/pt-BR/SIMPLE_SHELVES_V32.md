# V32 — quatro parafusos por cima

[English / evidência técnica](../SIMPLE_SHELVES_V32.md)

**Esta é a direção atual solicitada pelo proprietário. Substitui a complexidade das tampas de porcas e dos apoios removíveis.**

![Fixação simples](../../exports/generated/side-panel-v32/07-simple-shelves.png)

O uso pretendido é: abrir e apoiar positivamente o playfield, desconectar o chicote da prateleira, soltar **dois parafusos de cada lado, todos por cima**, deslizar a prateleira até o vão de saída e levantar o conjunto com os equipamentos presos nela. Os apoios ficam no gabinete. As roscas ficam presas nos apoios, sem porcas soltas para segurar por baixo.

O novo modelo separado elimina as tampas inferiores e o mecanismo de remoção dos apoios. As três travessas permanecem instaladas nos testes. Os equipamentos precisam deixar livre o espaço de acesso aos quatro parafusos.

Para que o caminho da ferramenta realmente venha de cima, corrigi a posição do parafuso traseiro da S2 e avancei a S3 em **80 mm**. Antes, havia interferências com T2 e com a base do backbox. S1 e S2 mantêm suas posições; tamanhos e alturas das três prateleiras permanecem iguais. A retirada exige deslizar até um vão livre antes de levantar; não exige retirar travessas no cenário fixo testado.

Foram aprovadas **90 verificações**, incluindo o corredor completo da ferramenta até acima do gabinete, retirada dos parafusos e três trajetórias com envelopes de equipamentos de 60 mm. O arquivo FreeCAD foi reaberto e conferido. O V32 original permanece intacto.

**Ainda falta integrar o playfield realmente levantado, as escoras e os cabos.** Neste teste, seu conjunto foi excluído explicitamente para verificar os obstáculos fixos. Isso não comprova a abertura real nem a segurança do sistema de elevação. Ferragens, ancoragem dos apoios, cargas e fabricação também continuam pendentes.

[Proposta FreeCAD](../../exports/generated/side-panel-v32/simple-shelves-proposal.FCStd) · [Relatório](../../exports/generated/side-panel-v32/simple-shelves-validation.json)

Reproduzir com `bash tools/run_simple_shelves_v32.sh`. Os estudos mais complexos permanecem como histórico; não são a solução atual. As identidades das antigas tampas ficam aposentadas, sem reutilização.

CNC bloqueado. Material original: CERN-OHL-S-2.0. Preservar LICENSE e NOTICE.md. Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet.
