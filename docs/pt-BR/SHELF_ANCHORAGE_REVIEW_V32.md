# V32: ancoragem substituível dos apoios das prateleiras

> Estudo histórico, substituído pela [fixação simples por cima](SIMPLE_SHELVES_V32.md). Não retomar esse mecanismo como direção atual.

[English / relatório técnico completo](../SHELF_ANCHORAGE_REVIEW_V32.md)

**Proposta separada; 138 verificações aprovadas; CNC BLOQUEADO.** A aprovação da fixação removível das prateleiras foi registrada em DEC-OWNER-V32-SHELVES. Este estudo avança na ancoragem dos apoios; não transforma a aprovação anterior em autorização para usinar as laterais.

![Ancoragem dos apoios](../../exports/generated/side-panel-v32/06-shelf-anchorage.png)

Cada apoio recebe dois parafusos acessíveis pelo interior, com insertos em furos cegos na lateral. Assim, o apoio pode ser substituído sem acesso pela face externa. Os apoios continuam locais a cada parede, sem uma nova ligação rígida atravessando o gabinete.

Os eixos ficam no meio da altura dos apoios: Z151/171/231 para S1/S2/S3. Os deslocamentos Y são 55/125 mm a partir da frente do apoio. São 12 conjuntos candidatos de parafuso, arruela e inserto.

O estudo usa haste Ø5 ×50 mm, cabeça Ø9 ×4 mm, arruela Ø12 ×1 mm e inserto Ø8 ×10 mm. O furo cego candidato Ø8,5 ×10,5 deixa **7,5 mm de madeira até a face externa**, considerando chapa nominal de 18 mm. A sobreposição axial haste/inserto é de 7 mm. **Essas medidas não são uma especificação de compra, recomendação de furação de fabricante ou comprovação da rosca e resistência.** A ferragem real pode exigir revisão.

Foram verificados os 12 acessos internos com ferramenta candidata Ø16 ×100 mm, a retirada de 55 mm dos parafusos/arruelas e seis rotas para trocar os apoios. Primeiro, a prateleira deve estar descarregada e removida, assim como os pré-requisitos de desmontagem do monitor e travessas usados no estudo anterior. O apoio sai 70 mm para dentro, desloca-se ao vão de manutenção correspondente e sobe, levando sua tampa e duas porcas capturadas. O apoio oposto permanece no modelo. Os insertos ficam na lateral.

Após retirar o apoio, há espaço axial candidato para alcançar cada inserto. Isso ainda não comprova encaixe da ferramenta real de instalação/extração nem reparo da madeira. Na retirada normal da prateleira, esses parafusos laterais ficam instalados.

As novas ferragens preservam os acessos superiores das prateleiras, os acessos inferiores às tampas e as três rotas de retirada com envelopes de equipamentos. Um controle com parafuso/arruela ainda instalado bloqueia 1 mm de movimento do apoio. Outro controle detecta uma furação indevidamente passante.

[Abrir proposta FreeCAD](../../exports/generated/side-panel-v32/shelf-anchorage-proposal.FCStd) · [Relatório de validação](../../exports/generated/side-panel-v32/anchorage-validation.json)

O arquivo separado foi reaberto e conferido: 150 sólidos válidos, incluindo volumes candidatos. As únicas peças anteriores que mudam são os seis apoios e as duas laterais **da proposta**. O V32 original permanece idêntico. As tampas aprovadas receberam identidades permanentes S1NutCoverL/R a S3NutCoverL/R, com medidas e fixações ainda provisórias.

A execução integrada passou em **418 verificações**:

```sh
bash tools/run_side_review_v32.sh
uv run --with matplotlib python tools/render_shelf_anchorage_v32.py
```

Próximos requisitos: ferragens reais, espessura medida, prova de ancoragem no compensado, retenção contra vibração e cargas; depois, liberação independente das travessas/monitor e escoras cativas. Não há aprovação estrutural nem liberação de fabricação. Sessões físicas continuam pausadas e a decisão sobre a arquitetura do PC permanece aberta.

Material original: CERN-OHL-S-2.0. Preservar LICENSE e NOTICE.md. Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet.
