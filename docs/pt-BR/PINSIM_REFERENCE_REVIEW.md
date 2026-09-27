# Avaliação da referência PinSim

[English](../PINSIM_REFERENCE_REVIEW.md) · [Português (Brasil)](PINSIM_REFERENCE_REVIEW.md)

Avaliado em 2026-09-27. **Referência útil; não é gabarito CNC nem qualificação estrutural.** A geometria V32 não mudou e a fabricação continua BLOCKED.

## Duas fontes, escopos diferentes

[Jerware/PinSim](https://github.com/Jerware/PinSim) é um controlador XInput baseado em Teensy LC. Commit avaliado: `d0f35c2ff881b99ffcf9fc341bdacf742de84128` (2023-02-05). Firmware e README descrevem botões, acelerômetro ADXL345 e entrada/calibração analógica do plunger. Serve para pesquisa de controles, mas não é um projeto CNC de gabinete completo nem comprova compatibilidade com nossas escolhas Arnoz. Não propomos substituir o controlador. Licença do firmware: GPL-3.0.

O ZIP identifica outra fonte: **PinSim Cabinet por twistedream13**, [Thingiverse 5903318](https://www.thingiverse.com/thing:5903318). Seu README descreve gabinete impresso em 3D de grande formato, peças para teste de encaixe, dobradiças impressas montadas e montagem principalmente com M4. Relata encaixes de dedos folgados e alterações de furos ainda não testadas. Isso não estabelece tolerâncias CNC validadas para nosso compensado.

## Inspeção real das malhas

O ZIP passou na verificação CRC. Os seis STLs binários têm contagem de triângulos consistente e malhas fechadas; a conversão no FreeCAD resultou em sete sólidos válidos e fechados. `Hinge_Test.stl` contém duas peças. Isso comprova integridade geométrica, não resistência. O F3D e sete imagens foram inventariados; o histórico paramétrico do F3D não foi validado.

| Arquivo | Dimensões da caixa envolvente, unidades do STL | Sólidos | Uso recomendado |
|---|---|---:|---|
| Leg_Bracket_Test.stl | 73,308 × 139,700 × 18,397 | 1 | Estudar cupom local de encaixe do bracket |
| Plunger_test.stl | 58,738 × 1,588 × 62,706 | 1 | Estudar cupom da abertura do plunger |
| Arcade_Button_Test.stl | 33,792 × 33,172 × 9,737 | 1 | Referência de botão; peça inclinada nas coordenadas originais |
| Paddle_Button_Test.stl | 1,588 × 44,440 × 44,445 | 1 | Referência de botão |
| StartButtonTest.stl | 31,743 × 1,588 × 31,746 | 1 | Referência de botão |
| Hinge_Test.stl | 76,200 × 12,697 × 38,100 | 2 | Experimento de dobradiça impressa; não é a dobradiça do nosso backbox |

STL não declara unidades. Milímetros parecem plausíveis, mas **não estão confirmados**. As dimensões seguem os eixos da montagem original e não constituem desenhos de fabricação. O [manifesto](../../reference/pinsim/manifest.json) registra limites exatos, triângulos, hashes, fechamento das malhas e validade dos sólidos.

## Bracket da perna: viável como estudo de interface

A inspeção visual mostra um cupom raso com formato de canal/canto e duas aberturas. Ajuda a planejar um teste de encaixe do bracket comprado contra a interface local do gabinete. Não demonstra que uma peça impressa sustente um gabinete de aproximadamente 150 kg sob nudges, nem que os furos correspondam à ferragem real.

Preservar o caminho de carga em aço. Medir ângulo do bracket, centros e diâmetros dos furos, espessura da chapa, área de apoio, engajamento dos parafusos e acesso da chave antes de criar uma interface CNC paramétrica original. Validar primeiro em cupom e depois executar a prova de carga exigida. Não importar esse STL como bracket permanente nem copiar seus furos para V32.

## Plunger: viável como estudo da abertura

A inspeção mostra uma placa fina com abertura triangular arredondada, não um conjunto completo de plunger ou suporte de sensor. A espessura de aproximadamente 1,588 unidade não valida montagem em compensado de 18 mm.

Aplicar o método de cupom ao plunger físico selecionado: medir flange/abertura, fixações, comprimento roscado e porcas, espessura admissível do painel, curso da haste, envelope de mola/arruelas e acesso traseiro ao sensor/cabo. Determinar o sensor compatível independentemente do firmware PinSim. Gerar geometria CNC original a partir dessas medidas e manter o suporte do sensor substituível quando possível. Esta avaliação não congela furação nem código de ferragem.

## Preservação e publicação

A licença do ZIP declara “Creative Commons - Attribution - Non-Commercial - Share Alike”, sem versão ou URL do texto legal. Não conseguimos confirmar a versão na página original durante esta avaliação. O AGENTS.md proíbe importar CAD com licença ambígua. Por isso, **STLs, F3D, imagens e ZIP não foram publicados em nosso GitHub**. A restrição não comercial também precisa ser considerada antes de incluir material em um produto reutilizável comercialmente; nossa licença CERN e a GPL do firmware não a substituem.

O ZIP integral foi preservado localmente, com hashes e links centralizados no [registro de referência](../../reference/pinsim/README.md). Isso preserva os arquivos neste computador, mas não cria backup remoto dos modelos. Confirmar a licença exata e obter autorização do autor quando necessária continuam pendentes antes de redistribuir/adaptar. Não contatamos o autor em nome do proprietário.

## Próximo uso na engenharia

1. Manter PinSim como referência de controles e pequenos cupons de encaixe.
2. Quando as sessões físicas forem retomadas, medir bracket e plunger reais e criar interfaces e cupons independentes, dimensionados.
3. Esclarecer a licença antes de publicar modelos recebidos. Nem a licença nem a validade da malha liberam a fabricação.
