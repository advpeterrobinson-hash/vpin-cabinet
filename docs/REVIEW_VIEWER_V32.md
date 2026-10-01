> CURRENT PLAYFIELD: [wooden lift-out pivot](WOOD_DOWEL_PIVOT_V32.md). Viewer states: PLAY, SERVICE, LIFT-OUT, EXPLODED. Previous prop-only states below are historical and superseded.

# Visualizador 3D de revisão V32

Abrir `exports/generated/viewer-v32/index.html` diretamente no Chrome, Edge ou
Firefox com WebGL. Arquivo único, offline, sem instalação, servidor ou conta.

Arrastar gira, botão direito desloca, roda aproxima. Em tela de toque, usar um
dedo para girar e dois para zoom/deslocamento. Selecionar uma peça pela geometria
ou pelo ID na lista; ocultar, isolar ou focar. As camadas permitem inspecionar
carcaça, prateleiras, playfield, PC, SSF, controles, traseira e ferragens.
O botão Interior oculta algumas peças para revelar o interior; não representa
uma posição mecânica de serviço. Restaurar recupera a apresentação inicial.
Transparência e corte são apenas ferramentas de inspeção. O corte não fecha
faces; a caixa de seleção não é recortada. Salvar imagem exporta a vista atual.

## Atualização

```sh
python3 tools/build_review_viewer.py
```

Reutiliza `exports/generated/consolidated-v32/mesh.json`. A geração completa
`bash tools/run_consolidated_v32.sh` agora também atualiza o visualizador após
atualizar o CAD e a malha. Não depende de npm, rede ou serviços externos.
Alternativas podem ser passadas com `--mesh caminho/mesh.json --output caminho/index.html`.
A malha precisa conter uma lista de peças com `name`, `vertices` e `faces`
triangulares. IDs são preservados; posições estão em X/Y/Z e milímetros do CAD.
Coordenadas são arredondadas a 0,001 mm exclusivamente na apresentação.
O visualizador registra o caminho e SHA-256 da malha de origem.

O HTML é um retrato do CAD exportado: editar um parâmetro sem regenerar o CAD
e a malha não muda o visualizador. Não altera documentos FreeCAD nem valida
interferências, resistência, fiação ou movimentos. A lista de 202 peças inclui
reservas e referências simplificadas; não é uma BOM. No conjunto atual faltam
backbox completo, pernas, lockdown final, escoras e cabeamento. Reservas de
amplificador/fonte/USB e outras instalações são uma camada desligada inicialmente.
Playfield e PC também são envelopes, identificados ao selecionar.

Escopo limitado: uma página de revisão, sem editor CAD, animação cinemática,
plataforma de hospedagem ou motor próprio. Madeira e metal usam cores de
identificação; não são materiais/acabamentos selecionados para fabricação.

Original CERN-OHL-S-2.0. Source Location:
https://github.com/advpeterrobinson-hash/vpin-cabinet
Three.js / OrbitControls: MIT, conforme `THIRD_PARTY_NOTICES.md`.
