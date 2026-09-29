# Painel frontal: controles e revisão para fechamento

[English](../FRONT_PANEL_REVIEW_V32.md) · [Português (Brasil)](FRONT_PANEL_REVIEW_V32.md)

**FRONT_LAYOUT_PROPOSAL — CNC não liberado.** Primeira etapa da sequência frente → laterais → traseira → piso. V32 original e proposta de iluminação no fórum permanecem intactas. [Imagem](../../exports/generated/front-panel-v32/01-front-review.png) · [CAD separado](../../exports/generated/front-panel-v32/front-layout-proposal.FCStd) · [Verificação](../../exports/generated/front-panel-v32/validation.json).

As fotos `414893.jpg` e `414888.jpg` mostram três controles iluminados à esquerda, porta central, plunger à direita e Launch Ball abaixo. São referências de disposição, não de medidas ou furação. Os textos dos três botões não são todos legíveis; Start / Extra Ball / Exit-Back são funções propostas. Não copiamos arte temática nem importamos as fotos para o pacote.

## Proposta

X cresce da esquerda para a direita olhando a frente; Z parte do fundo do gabinete; Y cresce para trás. Dimensões em mm. Mantidos corpo de 600, altura frontal 400.05 e painel existente de 564 × 400.05 × 18, X18..582. A proposta separada de encaixes capturados ainda não foi adotada.

| Função | X | Z |
|---|---:|---:|
| Start | 90 | 310 |
| Extra Ball / configurável | 90 | 260 |
| Exit / Back | 90 | 210 |
| Plunger | 520 | 280 |
| Launch Ball | 520 | 210 |

Passo esquerdo de 50; plunger/Launch de 70. Faces 35/50 e placa de plunger 60 × 60 são hipóteses visuais. Furos nominais de 25.4 são estudo, não especificação da ferragem selecionada. Plunger continua sem furação. Não adicionamos placa, janela adaptadora ou código definitivo para imitar a foto.

Em relação à V32, dois botões esquerdos Z280/230 passam a três em Z310/260/210; acrescenta-se Launch à direita. Reserva do plunger passa de Z250 para Z280. Rebaixos anteriores dos botões foram omitidos porque a montagem real não está definida. Abertura e quatro furos de referência da porta foram preservados.

Crédito pela porta, confirmando seus interruptores; power/reset, calibração, volume e desabilitação independente do feedback ficam no acesso interno. Funções/legendas podem mudar sem redesenhar madeira; manter Exit separado de Start e considerar comando prolongado no software. Não criar banco externo de manutenção.

## Dependências encontradas

- Porta: referência X144.425..455.575, Z92.840625..357.159375, abertura 311.15 × 264.31875. Modelo, flange, dobradiça, fechadura, fixações e profundidade não confirmados. O envelope menor da v27 não valida esta abertura.
- S1 começa em Y120; face interna frontal em Y18: **102 mm disponíveis até a prateleira**, antes de cabos e mãos. Um volume conservador de acesso com profundidade 140 e margem de flange 20 intercepta S1, display e StarTech. **Não prova colisão da porta real**: extrudar toda a flange pela profundidade superestima a ocupação. Obter desenho/medidas antes de decidir ajuste de S1/áudio removível ou interface da porta.
- Corpo provisório de plunger 40 × 202 × 40 em Z300 colidia com MonRailR. Z280 limpa os vizinhos testados. Curso, sensor, cabo, porca e mão ainda exigem geometria real.
- Reserva proposta do receptor do lockdown: Z380..400.05. Com flange ilustrativa de 20, sobra somente 2.84 mm até essa faixa. Isso não comprova espaço para o receptor ou ferramentas.
- Brackets das pernas, reforços, arruelas, parafusos e ferramentas não são definidos pelas chapas decorativas da foto. Continuam pendência compartilhada entre frente e laterais.

## Verificação

`freecadcmd tools/front_panel_v32_entry.py` salva/reabre um CAD separado. **20 verificações aprovadas:** 45 sólidos válidos, identidades originais, alteração apenas de Front/reserva do plunger, dimensões, abertura/fixações da porta, quatro furos e madeira ao redor, posição do plunger e ausência de seu recorte. Quatro controles negativos rejeitam Launch preenchido, Start alargado, S1 deslocada e reserva deslocada. Permanecem três sobreposições do volume conservador de acesso à porta. Proxies de botões e plunger rebaixado não interceptam os vizinhos testados.

Render: `uv run --with numpy --with matplotlib python tools/render_front_panel_v32.py`. Parâmetros: `config/front_panel_v32.json`. Não comprova resistência, movimento, ferramentas, elétrica ou fabricação; sessões físicas seguem pausadas.

## Evidência pendente

Considerados fonte dimensional V32, gates HF-019/020/022/030, envelopes v27, avaliação Pinscape e proveniência PinSim. PDFs antigos das ferragens não foram encontrados nos arquivos acessíveis; não declaramos revisão nova deles. Reanexar desenhos da porta, botões, plunger, lockdown/pernas ou indicar caminhos acessíveis.

Para fechar: confirmar funções visíveis; obter envelopes reais de montagem/manutenção; resolver porta/S1/display, cantos das pernas e receptor; validar uma furação paramétrica original com material/ferramenta/cupom medidos. Depois propagar interfaces para laterais. [Sequência de fechamento](PANEL_CLOSURE_V32.md).

Contexto externo: [Pinscape, reforços de canto](https://mjrnet.org/pinscape/BuildGuideV2/BuildGuide.php?sid=cornerBraceCutting) alerta para interferências de reforços altos com controles; sua receita de marcenaria não é adotada. [POTAR Arnoz](https://shop.arnoz.com/en/plunger/44-potar.html) descreve sensor, não o conjunto mecânico completo ou gabarito selecionado.

Material original: CERN-OHL-S-2.0. Preservar LICENSE e NOTICE.md. Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet.
