# Avaliação de ferramenta CAD para agentes — text-to-cad

**Revisado em:** 2026-10-21  
**Fonte:** [earthtojake/text-to-cad](https://github.com/earthtojake/text-to-cad)  
**Tipo de revisão:** README e licença declarada; sem instalação, execução de código ou importação CAD.

## Avaliação

É um fluxo CAD para agentes de programação, não apenas uma coleção de prompts. O repositório oferece skills e um plugin que inicia o serviço local cadgen MCP. A pilha documentada inclui Python, build123d e Open CASCADE; gera STEP, GLB, STL e 3MF e anuncia verificações de desenho técnico e manufaturabilidade. O README lista Codex como compatível. O repositório declara licença MIT.

**Relevância para o VPin Cabinet: útil em um piloto independente e delimitado.** Pode ser avaliado em uma peça separada de baixo risco, em um cupom de teste dimensionado ou na inspeção de sólidos exportados. O modelo paramétrico FreeCAD, as configurações por revisão, os scripts de validação e a geometria aprovada do gabinete devem continuar como autoridade de engenharia.

## Compatibilidade e limites

- O fluxo documentado de build123d/Open CASCADE é diferente da fonte FreeCAD e do pipeline de geração/validação existente no projeto. A geometria gerada não deve substituir nem modificar silenciosamente o modelo canônico.
- Geometria produzida por agente é uma proposta. Ela não determina dimensões de ferragens comerciais ainda não medidas, segurança estrutural, encaixe do vidro, tolerâncias de fabricação ou validação física.
- O README informa que a telemetria vem ativada por padrão para estatísticas de uso e relatórios de falha, usando identificador aleatório; afirma que não inclui arquivos, caminhos ou prompts e documenta como desativá-la. O runtime é baixado localmente no primeiro uso e requer conexão de rede.
- As instruções de instalação podem instalar código, skills e um serviço local. Não são uma etapa inofensiva de consulta.

## Piloto recomendado

1. Usar uma área de trabalho descartável e com acesso limitado, especificando separadamente uma peça não estrutural de baixo risco ou um cupom de teste. Não conceder ao agente a árvore canônica de trabalho FreeCAD.
2. Fixar uma versão/commit revisado, inspecionar pacote e dependências e desativar a telemetria antes da execução.
3. Exportar STEP neutro. Comparar unidades, dimensões globais, posicionamento, validade dos sólidos e folgas do conjunto com valores explícitos controlados pelo projeto.
4. Registrar falhas e correções manuais. Manter a saída fora da liberação de fabricação até passar pelas verificações existentes do projeto e pela revisão humana.

**Decisão:** manter como candidata revisada para um piloto restrito. Não instalar no repositório VPin, não incorporar ao fluxo normal de build e não usar a saída para liberação CNC com base apenas nesta revisão.

## Evidências relacionadas

- [Relatório técnico V35.1](https://github.com/advpeterrobinson-hash/vpin-cabinet/blob/e6fe42152565a167e9d4e4d0ad4eb080f09c1c28/docs/STANDARD_WIDEBODY_V351.md)
- [Bloqueios externos V35.1](https://github.com/advpeterrobinson-hash/vpin-cabinet/blob/e6fe42152565a167e9d4e4d0ad4eb080f09c1c28/docs/V351_REMAINING_EXTERNAL_GATES.md)
- [Auditoria documental atual](PUBLIC_DOCUMENTATION_AUDIT.md)

Esta avaliação descreve o README e a licença declarada na data da revisão; não é auditoria de segurança nem garantia de que versões futuras mantenham o mesmo comportamento.
