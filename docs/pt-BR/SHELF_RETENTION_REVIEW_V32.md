# V32: proposta de fixação removível das prateleiras

> Estudo histórico, substituído pela [fixação simples por cima](SIMPLE_SHELVES_V32.md). Não retomar esse mecanismo como direção atual.

[English / relatório técnico completo](../SHELF_RETENTION_REVIEW_V32.md)

**Proposta separada, com 106 verificações aprovadas. V32 original inalterado; CNC BLOQUEADO.**

![Fixação das prateleiras](../../exports/generated/side-panel-v32/05-shelf-retention.png)

Cada prateleira recebe quatro parafusos acessíveis por cima, com porcas quadradas capturadas nos apoios substituíveis. A proposta alarga esses apoios de 18 para **42 mm**, mantendo altura, comprimento e contato com a lateral. Isso afasta os furos das bordas sem criar outra travessa ligando as paredes. A fixação dos próprios apoios às laterais ainda precisa de detalhamento.

S1/S2/S3 mantêm dimensões e posição. Na proposta, recebem apenas quatro furos nominais Ø5,5 mm, com eixos X48/552 e deslocamentos Y25/100 a partir da borda dianteira de cada prateleira. Nenhum painel permanente é recortado. Os afastamentos mínimos da borda do furo são 22,25 mm na prateleira e 9,25 mm na lateral do apoio; não são valores de resistência certificados.

As porcas ficam em bolsões inferiores, fechados por seis tampas com identidade funcional S1NutCoverL/R a S3NutCoverL/R. Os bolsões impedem geometricamente a rotação de 45° da porca; as tampas interceptam sua queda depois de retirar o parafuso. A resistência e o comportamento sob vibração ainda precisam de comprovação.

O envelope de equipamentos de 60 mm passa a reservar quatro corredores verticais Ø20 mm por prateleira para ferramenta e parafusos. **Esses Ø20 não são furos na madeira:** são regiões que equipamentos e fios devem deixar livres.

A primeira disposição foi rejeitada porque o acesso traseiro da S1 encontrava o botão lateral e o da S2 encostava na guia T2. As posições corrigidas passaram nos dois lados:

- 12 acessos superiores para ferramenta candidata Ø16 ×100 mm;
- retirada vertical de 40 mm dos 12 parafusos e arruelas;
- três rotas das prateleiras preservadas após retirar as respectivas fixações;
- 24 acessos inferiores para ferramenta candidata Ø10 ×80 mm nas tampas das porcas.

Um parafuso deixado instalado bloqueia o deslocamento de 1 mm da prateleira no controle negativo. Isso verifica engate geométrico, não força ou segurança estrutural. Na retirada normal da prateleira, as tampas e porcas ficam nos apoios. Os parafusos pequenos das tampas ainda não estão modelados; só suas posições e o espaço axial para ferramenta foram estudados.

O conjunto candidato usa 12 parafusos com envelope de haste Ø5 ×35 mm e cabeça Ø9 ×4 mm, 12 arruelas Ø12 ×1 mm, 12 porcas quadradas 10 ×10 ×5 mm e seis tampas 42 ×150 ×3 mm. **São hipóteses de projeto, não lista de compra.** Roscas, encaixe da ferramenta, torque, material, resistência, retenção contra vibração, tolerâncias e alívio dos cantos dos bolsões dependem da ferragem e fabricação escolhidas.

[Abrir proposta FreeCAD](../../exports/generated/side-panel-v32/shelf-retention-proposal.FCStd) · [Relatório de validação](../../exports/generated/side-panel-v32/retention-validation.json)

O arquivo foi reaberto e conferido: 114 sólidos válidos, incluindo volumes candidatos que não são peças de fabricação. O modelo original permanece idêntico. Para reproduzir:

```sh
bash tools/run_side_review_v32.sh
uv run --with matplotlib python tools/render_shelf_retention_v32.py
```

O próximo detalhamento deve resolver a ancoragem dos apoios, retenção independente do monitor/travessas e escoras cativas. A proposta não fecha cargas, ferragens nem fabricação; sessões físicas permanecem pausadas.

Material original: CERN-OHL-S-2.0. Preservar LICENSE e NOTICE.md. Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet.

A direção funcional foi aprovada pelo proprietário em 2026-09-29 e registrada em [DEC-OWNER-V32-SHELVES](../DESIGN_DECISIONS.md#dec-owner-v32-shelves--removable-shelf-retention). Dimensões, ferragens e fabricação continuam provisórias.

O [estudo de ancoragem lateral](SHELF_ANCHORAGE_REVIEW_V32.md) acrescenta apoios removíveis com furos cegos candidatos, preservando os acessos às prateleiras. Essa nova usinagem lateral permanece sem aprovação.
