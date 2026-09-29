# Planejamento de interfaces e zonas V32

[English](../INTERFACES_AND_ZONES_V32.md) · [Português (Brasil)](INTERFACES_AND_ZONES_V32.md)

Status: **PROVISIONAL — CNC BLOCKED — sessões físicas PAUSED**. Retomada em 28/09/2026 a partir de `0398d16857e66e415805b7154b0df7e37e7964a6`, após o blecaute. Este é o próximo pacote da [revisão Pinscape](PINSCAPE_ACCELERATION_REVIEW.md), baseado na [intenção de iluminação](LIGHTING_INTENT_V32.md), no [registro de peças](PART_CODES.md) e no [pacote V32](../../exports/generated/cabinet-v32/README.md). Não aprova geometria, compra, medição ou características elétricas.

Esclarecimento do proprietário em 2026-09-29: painéis Cleveland com controle Arnoz MX-DONNY. [Dimensões e projeto aberto](LIGHTING_INTENT_V32.md) substituem a hipótese de kit completo. Instalação definida pelo proprietário; esta etapa registra dimensões nominais e não exige projeto de instalação agora.

## Registro de interfaces

Os identificadores `IF-*` organizam requisitos, não são códigos permanentes de peças. Todas as interfaces continuam `BLOCKED_UNMEASURED`. Modelo CAD ou dimensão nominal não comprova encaixe da ferragem.

| ID / interface | Base registrada | Evidência faltante | Próxima entrega / aceitação |
|---|---|---|---|
| IF-01 Pernas e brackets | Pernas reais; gabinete de 600 mm | Brackets, parafusos, arruelas, furos, ferramentas e zonas de carga | Desenho medido; comparar SideL/SideR e sulcos propostos antes do cupom CNC original |
| IF-02 Plunger | Intenção Arnoz; interface final pendente | Revisão, curso, corpo/conectores e furação | Proposta de suporte substituível; verificar curso completo e acesso |
| IF-03 Vidro e lockdown | Lockdown personalizado permitido; madeira nominal de 18 mm | Vidro/bordas, canaletas, receptor, retenção e remoção | Seção com material/ferragens medidos; cupom antes dos cortes finais |
| IF-04 Fans e grades | Dois envelopes V32; referência nominal de moldura de 120 mm | Modelo, grade/filtro, recorte, furos, cabo e acesso | Desenho de interface e remoção; comprovação térmica separada |
| IF-05 Matriz | Seis painéis Cleveland, nominais 79.375 × 79.375 mm cada; controladora Donny | Dimensão montada final, espessura e folgas abertas | Somente referência dimensional; disposição e instalação decididas pelo proprietário |
| IF-06 LEDs de speakers/gabinete/gap | Dois anéis selecionados; fitas laterais do kit; iluminação sob gabinete e gap opcionais | Modelos, comprimentos/pixels, dimensões, características e conectores | Registros separados; LED do speaker acompanha sua remoção; preservar folga da tela |
| IF-07 Manutenção de backbox/playfield | BBBase e suportes de monitor; duas escoras cativas exigidas | Dobradiças/fixações/cabos; receptores, travas, recolhimento e retenção sob carga total | Estudo separado de movimento/acesso e plano de prova com uma escora; nenhum ensaio físico declarado |
| IF-08 Módulos de manutenção | S1/S2/S3, T1/T2/T3 e PCBase na V32 | Ferramentas/fixações, desconexão, retenção e trajetórias | Sequência de acesso e dependências; resolver primeiro divergência do PC abaixo |
| IF-09 Alimentação, rede e feedback | Um cabo aterrado; distribuição fechada; desabilitação independente do feedback | Dispositivos, invólucro, alívio de tração, acesso, proteção e cargas | Mapa funcional e revisão elétrica qualificada antes de fiação ou recortes |

### Divergência na arquitetura do PC

As instruções fornecidas nesta sessão exigem gaveta traseira de extensão total para o PC; o pacote V32 salvo registra PCBase baixo sem gaveta. Este documento não escolhe entre eles. A interface de manutenção do PC fica **BLOCKED_OWNER_DECISION** antes de projetar remoção ou alterar geometria. Os arquivos V32 permanecem como evidência; sua decisão sem gaveta não substitui silenciosamente a instrução recebida.

## Zonas de alimentação, dados e manutenção

O [registro estruturado](../../config/interface_zones_v32.json) mantém características desconhecidas como `null`, nunca zero. IDs de zona não são números de circuitos ou alocação confirmada de portas.

| Zona | Relação de alimentação/dados a resolver | Limite de manutenção |
|---|---|---|
| MATRIX | Alimentação dos painéis versus dados; ordem/orientação e revisão do controlador | Suporte removível; desconexão acessível e chaveada; movimento de playfield/backbox |
| SPEAKER_LED / CABINET_LED / GAP_LED | Mapas e brilho separados; gap opcional | Speaker / acabamento removível; preservar substituição da tela |
| UNDERCABINET_LED | Opção autorizada; produto, pixels, alimentação e portas indefinidos; fora do subtotal do kit | Iluminação removível sob gabinete; acesso e cabos pendentes |
| AUDIO | Música/Bluetooth, amplificadores e canais StarTech | Dispositivos substituíveis; registrar conectores |
| SSF | Quatro zonas espaciais; canal → amplificador → exciter pendente | Fixação local e terminais; evitar travamento amplo das paredes ativas |
| FEEDBACK | Dispositivo → driver → proteção → desabilitação independente; regimes pendentes | Fixação positiva e estado de manutenção independentemente desabilitado |
| PC / DISPLAYS | Características de entrada e conectores de dados | Decisão sobre PC; adaptadores e acesso aos conectores das telas |
| COOLING / CONTROL | Alimentação e dependências entre modos pendentes | Acesso a grades/filtros; configuração offline e acesso deliberado de serviço |

Objetivos funcionais, **não um esquema de ligação**:

- **OFF:** cargas desligadas. Documentar e verificar isolamento para manutenção; nome de modo não comprova isolamento seguro.
- **AUDIO ONLY/Bluetooth:** música disponível, PC/telas e feedback mecânico desligados. Receptor, amplificador, controle e refrigeração necessários ainda precisam ser definidos. Política de LEDs decorativos aberta.
- **FULL PINBALL:** sistemas de jogo disponíveis. Feedback mantém desabilitação independente; LEDs mantêm efeitos desligáveis e brilho por zona.

Terra de proteção, retornos DC e referências de sinal precisam de registros distintos no futuro projeto; esta folha não prescreve topologia de ligação. Rede elétrica permanece enclausurada e inacessível na manutenção normal. Nenhum fusível, condutor, fonte ou pinagem é selecionado.

## Registros para cálculo de cargas

Criar uma linha por modelo real e alimentação em cada zona. Registrar quantidade, fabricante/fonte/revisão, tensão, corrente máxima de entrada (ou potência de entrada documentada), partida, regime, capacidade dos conectores e evidência de medição. Capacidade de controle/dados é distinta da distribuição de potência.

Para uma linha DC com corrente documentada: `I_row = quantity × I_unit`; `P_row = voltage × I_row`. Somar correntes somente na mesma alimentação. Linha obrigatória desconhecida mantém o total **UNKNOWN**; não omitir cargas, partida ou regime. Não contar potência DC e entrada da fonte que a alimenta como cargas independentes do gabinete. Entrada AC, perdas e proteção exigem dados próprios e revisão.

A aritmética da matriz estabelece somente `6 × 16 × 16 = 1536` pixels. Disposição física e portas não foram selecionadas. O exemplo antigo de 60 mA/pixel da revisão Pinscape é cenário de sensibilidade, não característica para preencher o registro.

## Próxima entrada e evidência de conclusão

1. Preservar dimensões dos painéis Cleveland para comparação de tamanhos. Disposição e instalação ficam com o proprietário; esta etapa não solicita especificação de instalação.
2. Preencher IF-05 e zonas de iluminação com essa evidência; manter dúvidas abertas. Esclarecer requisito do PC antes do estudo de manutenção.
3. Adicionar dispositivos restantes e revisar dependências dos modos, mapeamento, totais, conectores e movimentos.
4. Propor geometria visível somente com dados suficientes. Sessões físicas seguem pausadas; encaixe, elétrica, temperatura, movimento e carga dependem de evidência futura.

Esta etapa entrega documentação e registro inicial. Geometria-fonte e dimensões principais permanecem iguais, dispensando regeneração CAD neste passo. Não substitui verificações de sólidos V32 nem encerra bloqueios de fabricação.

Material original: CERN-OHL-S-2.0. Preservar [LICENSE](../../LICENSE), [NOTICE.md](../../NOTICE.md) e Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet.
