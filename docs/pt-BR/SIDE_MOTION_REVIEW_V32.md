# V32: retirada das travessas e prateleiras

[English / relatório técnico completo](../SIDE_MOTION_REVIEW_V32.md)

**Dez rotas candidatas livres; seis comparações de subida direta obstruídas. Nenhum painel alterado. CNC BLOQUEADO.**

![Rotas de manutenção das prateleiras](../../exports/generated/side-panel-v32/04-shelf-service-routes.png)

As três travessas podem subir pelas guias existentes após a retirada do conjunto do monitor. Cada uma foi verificada com as outras duas presentes. Com o monitor instalado, as três rotas encontram interferências.

As prateleiras precisam primeiro deslizar para um vão livre e só depois subir. A análise mantém as guias, apoios, outras prateleiras, ferragens candidatas da porta e a geometria atual do PC baixo.

| Prateleira | Obstáculo à subida direta | Deslocamento horizontal candidato | Subida testada |
|---|---|---|---|
| S1 | Áudio estacionário, botões laterais candidatos em Y255 e reserva atual do plunger | 310 mm para trás: Y120 → Y430 | 446,9 mm |
| S2 | Guias e cantoneiras da T2 | 170 mm para a frente: Y600 → Y430 | 426,9 mm |
| S3 | BBBase | 320 mm para a frente: Y1080 → Y760 | 366,9 mm |

Y é a borda dianteira da prateleira. S1 e S2 usam o mesmo vão em operações separadas. Antes dessas rotas, o conjunto do monitor e T1/T2/T3 estão removidos; as demais prateleiras ficam instaladas. A altura final foi escolhida para sair 10 mm acima de todos os sólidos retidos, sem representar uma instrução de levantamento manual.

Também passaram as três rotas com um envelope candidato de equipamentos de **560 × 150 × 60 mm acima de cada placa de 12 mm**. Os envelopes das outras prateleiras permanecem presentes. A placa StarTech acompanha S1 e cabe em seu envelope. Esses 60 mm incluem equipamentos, suportes e fios contidos; não representam capacidade de carga. Cabos externos precisam ser desconectados e equipamentos devem estar presos antes da movimentação.

A verificação cobre todo o deslocamento retilíneo pela extrusão das faces dos sólidos, em vez de conferir somente posições espaçadas. Um controle com obstáculo entre duas posições finais livres confirma a detecção no meio do percurso. Não é uma simulação de giro, dobradiça, esforço ou segurança de levantamento.

As posições intermediárias estão em arquivos separados, reabertos e verificados:

- [S1 deslocada para manutenção](../../exports/generated/side-panel-v32/service-stage-SHELF_1.FCStd)
- [S2 deslocada para manutenção](../../exports/generated/side-panel-v32/service-stage-SHELF_2.FCStd)
- [S3 deslocada para manutenção](../../exports/generated/side-panel-v32/service-stage-SHELF_3.FCStd)

Cada arquivo tem 65 sólidos, incluindo volumes candidatos que não são peças de fabricação. O FCStd original permanece idêntico.

O detalhamento das fixações deve permitir liberar o monitor sem depender dos parafusos das guias que ele bloqueia; liberar a retenção das travessas antes de extraí-las; e soltar as prateleiras antes de deslizá-las. Ferragens ou cabos novos não podem ocupar essas trajetórias sem nova análise. As prateleiras atuais não precisam ser encurtadas para as rotas testadas.

A retirada vertical do conjunto do monitor é apenas um estudo de desmontagem maior. **Não substitui o uso normal com duas escoras cativas**, a prova de cada escora isolada ou o projeto das dobradiças. Vidro, lockdown, iluminação, cabos, fixações reais e cargas não estão certificados. A decisão sobre a gaveta do PC permanece aberta; uma mudança de arquitetura exige refazer as verificações.

Reproduzir a partir do worktree V32:

```sh
bash tools/run_side_review_v32.sh
uv run --with matplotlib python tools/render_side_motion_v32.py
```

Resultado: 46 verificações das laterais, 29 de acesso às guias e 99 de movimento/arquivos salvos. São 16 rotas, das quais seis devem continuar sendo detectadas como obstruídas. O comando exige marcadores explícitos de sucesso, pois FreeCADCmd pode retornar zero após uma exceção.

Sessões físicas continuam pausadas. Fixações, ferramentas reais, cargas, tolerâncias, cupom físico e liberação para fabricação permanecem pendentes.

Material original: CERN-OHL-S-2.0. Preservar LICENSE e NOTICE.md. Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet.

A [proposta de fixação das prateleiras](SHELF_RETENTION_REVIEW_V32.md) acrescenta parafusos acessíveis por cima, porcas capturadas e apoios substituíveis mais largos. As rotas continuam livres, mas os equipamentos precisam respeitar os corredores de ferramenta. O comando único também executa as 105 verificações adicionais.
