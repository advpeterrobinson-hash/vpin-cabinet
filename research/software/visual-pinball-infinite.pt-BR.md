# Visual Pinball Infinite — referência externa de software

- **Adicionado em:** 29/10/2026
- **Categoria:** Virtual pinball / motor compatível com VPX e gerenciador de biblioteca
- **Status neste repositório:** PESQUISA / AVALIAR; **não instalado, testado ou adotado**
- **Site:** https://visualpinballinfinite.org/
- **Código-fonte upstream:** https://github.com/VPinInfinite/VisualPinballInfinite
- **Versões:** https://github.com/VPinInfinite/VisualPinballInfinite/releases
- **Licença upstream:** GPL-3.0-or-later (conforme declarada pelo upstream); conferir avisos de terceiros antes de reutilizar código

## Por que catalogar?

O projeto independente Visual Pinball Infinite apresenta um motor em Rust reimplementando partes de física e renderização do Visual Pinball X e uma interface integrada para execução de mesas VPX, organização de biblioteca, identificação de arquivos, gerenciamento de ROMs/PinMAME, configuração de múltiplas telas, produção de mídia, consulta ao Virtual Pinball Spreadsheet e integração com front-ends. Afirma preservar os arquivos `.vpx` originais.

**Não é** o repositório oficial do Visual Pinball X (https://github.com/vpinball/vpinball) nem o Visual Pinball Engine para Unity. São iniciativas distintas.

## Compatibilidade / avaliação futura

- Requisitos divulgados pelo upstream: **Windows 10/11 (64 bits) e GPU DirectX 12**. **Suporte Linux nativo não anunciado**; compatibilidade com Wine/Proton ainda não verificada.
- Verificar uso com mesas e ROMs existentes, PinMAME, backglass/PinUP, DOF/SSF, botões e nudging, 1–4 telas, mídia e front-end.
- Validar de maneira independente as alegações de física, latência e fidelidade visual: são **declarações do upstream**, não resultados do nosso projeto.
- Testar de forma isolada, com backup e sem movimentar ou regravar automaticamente a biblioteca original.
- Não alterar decisões estruturais, liberação CNC nem requisitos de segurança do gabinete com base nesta referência.

## Origem e limites

Projeto externo catalogado apenas para futura avaliação. Nenhum código, ROM, arte ou licença de terceiros foi incorporado ao repositório. A licença do hardware vpin-cabinet não substitui a licença deste software.

[English](visual-pinball-infinite.md)
