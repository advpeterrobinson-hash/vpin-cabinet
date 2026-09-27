# Auditoria local de regeneração e limpeza V32

[English](../V32_LOCAL_AUDIT.md) · [Português (Brasil)](V32_LOCAL_AUDIT.md)

Remoto inicial: `08d4538b61b3f11b65b0a2bd19e0c5aa455a7ac8`, branch `feat/cabinet-review-v32`. O checkout original tinha um commit V28 local, master histórico modificado e backup histórico excluído. Foi preservado sem reset, stash ou troca de branch. O trabalho ocorreu em worktree V32 separado.

## Resultados

- Inventário inicial: **331 arquivos rastreados**, incluindo **118 Python em tools/**; nenhum cache Python versionado.
- `make doctor` **falha** no worktree novo porque o artefato ignorado `cad/active/vpin-active.FCStd` está ausente. Python, FreeCAD GUI, FreeCADCmd 1.1.3, Git e configs foram detectados.
- `make validate` chega a `validate-owner-execution` e **falha** na proteção binária PRE-V32 de `bom/README.md`. O baseline é `25bc483d7e5ae47dfe13cea3bfbdd64086074715`; mudanças documentais posteriores explicam a falha. O verificador não foi enfraquecido nem teve seu baseline alterado.
- `make review-v32` **passa**: geração, verificação do documento salvo e seis imagens em inglês. Três controles negativos rejeitam label incorreto, ausência de metadado em português e geometria alterada no baseline.
- FCStd salvo: **45 objetos válidos com um sólido cada**, três prateleiras, três travessas e dois fans; interseções ≤0,01 mm³ (`collisions=[]`). Todos têm `PartCode`, `LegacyId`, `PartStatus`, `NameEN`, `NamePTBR` e label canônico verificados.
- Diferença simétrica dos sólidos contra o FCStd original do commit: zero na tolerância de 0,00001 mm³ para os 45 objetos. Identidades, limites e volumes não mudaram.
- `geometry.json` é um intermediário ignorado, ausente no checkout limpo e regenerado pelo builder; a equivalência geométrica é comprovada contra o FCStd versionado, não contra esse JSON. O STEP mudou apenas o timestamp do cabeçalho. O binário FCStd foi regenerado sem mudança geométrica. Os seis PNGs aplicam o renderizador em inglês já versionado; prateleiras usam S1/S2/S3.
- `validation.json` agora deriva dos testes no CAD salvo, incluindo verificação de metadados e lista vazia de mudanças geométricas. `manufacturing_ready` permanece falso.

Os testes comprovam posicionamento e reprodução, não resistência, movimento, térmica, hardware ou fabricação. Sessões físicas seguem pausadas. A proposta de encaixes capturados **não** foi aplicada à geometria V32.

## Classificação reproduzível

Execute `python3 tools/audit_repository.py`. `.work/v32-audit/repository-inventory.json` registra classe, justificativa, referências e alcance do build para cada arquivo rastreado, incluindo os novos scripts antes do primeiro commit. Classes: CURRENT, HISTORY, GENERATED-REVIEW, REFERENCE e REMOVE.

O grafo pesquisa caminhos, basenames e módulos Python no texto rastreado, partindo de Make, CI, V32 e auditoria. CURRENT pode indicar dependência viva **PRE-V32**, não autoridade arquitetural. HISTORY fora desse grafo é candidato à revisão, não prova de código morto: referências dinâmicas e evidência de engenharia exigem análise. Nenhuma exclusão é automatizada.

Arquivos rastreados claramente removíveis: **nenhum comprovado nesta passagem**. Caches Python locais ignorados podem ser removidos. Backups FreeCAD continuam ignorados como evidência. As únicas duplicatas exatas são LICENSE e NOTICE.md da raiz/pacote; são avisos obrigatórios da distribuição e permanecem.

## Dependências preservadas

`build_active.py` ainda depende de `build_cabinet_structure_v20`, `build_structure_v14`, `build_playfield_mechanics_v18`, `build_playfield_fixed_anchors_v19`, `build_cabinet_service_v21`, `build_owner_services_v27`, `build_rear_utility_v26` e `build_cabinet_rear_cpu_shelf_v24`. Make usa validadores antigos e ferramentas de evidência física. Não há justificativa para excluir por versão.

Famílias de gavetas v22/v23, revisões v28 e antigos extratores/shells ficam fora do build principal, mas mantêm wrappers, documentação ou histórico de engenharia. Arquivar somente grupos completos após migrar referências e links. Wrappers explícitos FreeCAD também resolvem comportamento headless; semelhança visual não basta para consolidá-los.

## Primeiro lote seguro

Implementado: rota V32 explícita, verificação independente do CAD salvo e controles negativos, help/README corretamente separados do legado, documentação EN/PT-BR, artefatos atuais regenerados e auditoria reproduzível. Nenhum fonte ou histórico de engenharia foi excluído. Caches Python gerados foram removidos após testes.

Próximo lote: migrar um grupo documental histórico com todos os links e espelhos; preservar famílias de código até que a substituição cubra suas responsabilidades de engenharia. A proteção histórica PRE-V32 deve receber migração delimitada, não aceitação geral de novos baselines.

Esta passagem não exige decisão de projeto do proprietário. Mudanças futuras de forma, encaixe, hardware ou arquitetura exigem proposta explícita e comparação geométrica. CNC continua **BLOCKED**.

A inspeção visual também separou as legendas S1 e StarTech na planta; apenas a posição do texto mudou.
