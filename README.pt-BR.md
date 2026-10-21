# Virtual Pinball Cabinet

## [ABRIR A GALERIA ATUAL →](docs/pt-BR/RENDERS.md)

[English](README.md) · [Galeria em inglês](docs/RENDERS.md)

**V35.1 é a revisão corrente de engenharia e arquitetura. CNC e fabricação permanecem BLOQUEADOS.** V32 é histórico. Verificações CAD não certificam resistência, ferragens reais ou fabricação.

## Arquitetura corrente — V35.1

O desenvolvimento está em `feat/v351-cncaudit-qn90f`. Consulte o [relatório V35.1 em inglês](https://github.com/advpeterrobinson-hash/vpin-cabinet/blob/e6fe42152565a167e9d4e4d0ad4eb080f09c1c28/docs/STANDARD_WIDEBODY_V351.md) e o [pacote técnico](https://github.com/advpeterrobinson-hash/vpin-cabinet/blob/e6fe42152565a167e9d4e4d0ad4eb080f09c1c28/exports/generated/widebody-v351/README.md). Os links fixam a evidência revisada; não incorporam o CAD à `main`.

- Standard widebody: gabinete externo **628,65 mm**, interior nominal **592,65 mm**, comprimento **1308,10 mm** e backbox de **780 mm**.
- **66 componentes de madeira: 60 peças CNC em compensado e seis blocos sólidos; 45 famílias.** Compensado nominal de **18 / 12 mm**, sujeito à medição do lote.
- Prateleiras removíveis S1/S2/S3 sem manípulos, travessas T1/T2/T3 e guias substituíveis; PCBase baixo fixo, **sem gaveta de PC**.
- Cartucho removível para a matriz de LEDs; kit de seis painéis da Cleveland Software Design selecionado como alvo, com medidas físicas dos painéis e espaçamento óptico ainda pendentes.
- Arquitetura de playfield com pino de madeira e apoios abertos preservada; **apoio primário de manutenção com playfield elevado ainda pendente / HOLD**.
- Interfaces comerciais de lockdown/receiver; siderails opcionais. Estratégia/encaixe do receiver ainda pendentes quando controlam usinagem permanente.
- Vidro temperado local de **5 mm**, corte final após montagem de prova do gabinete/canais; perfil real dos canais laterais e cupom do rasgo ainda necessários.
- Pernas clássicas, mobilidade externa removível e sem rodas integradas; eletrônica modular e distribuição aterrada protegida contra toque.

## Televisão escolhida e registro atual

**Samsung QN43QN90FAGXZD (QN90F de 43 polegadas)** é o alvo escolhido. A configuração mais recente registra o chassi dentro do envelope genérico e informa aprovação dos testes modelados de rotação 0–50° e retirada de 0–48 mm. Isso cobre somente o envelope modelado do chassi nu; conectores, curvatura de cabos, encaixe físico e qualificação térmica continuam pendentes.

A configuração registra **folga nominal de 10 mm entre o vidro e o playfield**, conforme a decisão mais recente do proprietário. O relatório e o pacote gerado da V35.1 ainda contêm texto antigo de validação pendente e uma folga de **7,5 mm**. A divergência está registrada na [auditoria documental](docs/PUBLIC_DOCUMENTATION_AUDIT.md); não trate o pacote antigo como prova de que a atualização para 10 mm está presente.

O relatório registra 32 vistas CAD e verificações aprovadas do estado de referência modelado. A configuração mais recente da QN90F registra aprovação do envelope do chassi nu e do movimento de serviço modelado. Isso não certifica encaixe de conectores/cabos, montagem física, comportamento térmico, ferragens reais, resistência ou segurança física. O nesting preliminar é estudo, não CAM de produção.

**Nenhum arquivo CNC está aprovado. A liberação de chapas completas permanece BLOQUEADA.** Faltam estratégia/encaixe do receiver quando dependente de usinagem; medição dos canais e cupom do rasgo; lote de compensado e cupom de tolerância; parâmetros do fornecedor/ferramenta e regeneração dos encaixes; interfaces permanentes de ferragens/comandos e métodos de fixação; reconciliação das evidências da QN90F e da folga de 10 mm entre relatório e pacote; apoio primário do playfield elevado; qualificação física de carga, nudge, borda do vidro e térmica.

Furos da lockdown e do canal traseiro são interfaces ajustadas com as peças reais após CNC, com envelopes protegidos; não são, por si, bloqueios de chapas completas. O reforço F06 segue obrigatório e é qualificado após montagem de prova da caixa. Consulte o relatório para os limites exatos dos bloqueios.

## Histórico e documentação

- [Avaliação da ferramenta CAD para agentes](docs/CAD_AGENT_TOOLING_REVIEW.pt-BR.md): análise delimitada do text-to-cad para um piloto separado; não instalado nem adotado no pipeline.

[Índice](docs/README.md) · [Auditoria de contradições](docs/PUBLIC_DOCUMENTATION_AUDIT.md) · [Galeria histórica V32](https://github.com/advpeterrobinson-hash/vpin-cabinet/blob/feat/cabinet-review-v32/docs/pt-BR/RENDERS.md) · [Pacote V32](https://github.com/advpeterrobinson-hash/vpin-cabinet/blob/feat/cabinet-review-v32/exports/generated/cabinet-v32/README.pt-BR.md).

V32 preserva a arquitetura de 600 mm como histórico. Estudos antigos de largura, amortecedores, escoras e gaveta de PC não são requisitos correntes de V35.1. Scripts/parâmetros de cada revisão continuam sendo autoridade técnica; comandos antigos da `main` não certificam V35.1.

## Licença e participação

Material original sob **CERN-OHL-S-2.0**, com uso comercial permitido e obrigações recíprocas conforme [LICENSE](LICENSE). Preserve [NOTICE.md](NOTICE.md) e o Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet.

Consulte [CONTRIBUTING.md](CONTRIBUTING.md), [GOVERNANCE.md](GOVERNANCE.md), [SUPPORT.md](SUPPORT.md), [SECURITY.md](SECURITY.md), [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md), [FAQ de licenciamento](docs/LICENSING_FAQ.md) e [política open-source](docs/OPEN_SOURCE_POLICY.md). Inglês é canônico em caso de divergência documental.
