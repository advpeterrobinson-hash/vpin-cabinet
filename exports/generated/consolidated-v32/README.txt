V32 — DESENHO CONSOLIDADO PARA REVISÃO / NÃO LIBERADO PARA CNC

Comece por output/pdf/v32-desenho-consolidado.pdf (8 pranchas A3).
CAD, STEP, DXF nominal do piso e evidência: exports/generated/consolidated-v32/.
Limitações detalhadas: docs/CONSOLIDATED_DRAWING_V32.md e prancha 8.
39 verificações; 202 sólidos incluindo reservas simplificadas de componentes.
O DXF não contém nesting, compensação de ferramenta ou CAM.

Reprodução desta consolidação a partir do CAD de entrada incluído:
  bash tools/run_consolidated_v32.sh
Requer FreeCADCmd com Part, rg, uv, numpy/matplotlib/reportlab e fontes DejaVu.
O script usa o nome freecadcmd. Execute a partir da raiz extraída do ZIP.
  python3 tools/package_consolidated_v32.py
O manifest.json contém SHA256 dos arquivos individuais. Não inclui a si mesmo.

A genealogia paramétrica completa das etapas anteriores está no repositório:
https://github.com/advpeterrobinson-hash/vpin-cabinet/tree/feat/cabinet-review-v32
Referências externas são URLs em library/references/links.txt. Não há desenhos
proprietários ou backups de CAD neste pacote. PDFs Dayton não foram baixados:
os servidores recusaram download; cotas vieram do conteúdo técnico indexado.

Original: CERN-OHL-S-2.0. Preserve LICENSE e NOTICE.md.
Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet
