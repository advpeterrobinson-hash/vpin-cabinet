# Guia Pinscape: aplicações à V32

[English](../PINSCAPE_ACCELERATION_REVIEW.md) · [Português (Brasil)](PINSCAPE_ACCELERATION_REVIEW.md)

**Resultado:** aproveitar o guia para acelerar o planejamento de interfaces, os testes em bancada e a documentação de manutenção. Não adotar dimensões de gabinete, receitas de controladores antigos ou operações de marcenaria como requisitos da V32. Nenhuma geometria ou seleção de hardware foi alterada.

## Fonte e escopo

Michael J. Roberts, *The New Pinscape Build Guide*, versão 2.1.0, 31/10/2023. Avaliação em 27/09/2026. O MHTML recebido parece conter o livro completo, não apenas a página do gabinete indicada no fragmento da URL. Inspecionamos índice, licença e capítulos selecionados abaixo; não verificamos todos os circuitos ou capítulos. [Edição online](https://head.pinscape-build-guide.pages.dev/) · [Identificação do arquivo](../../reference/pinscape/source.json).

O livro declara CC BY-SA 4.0; software do controlador e projetos das placas possuem licenças próprias. Adicionamos somente nossa avaliação e metadados, sem copiar livro ou ilustrações. Compatibilidade atual depende da documentação atual dos fabricantes. Nosso leitor web não conseguiu recuperar a edição online nesta avaliação; as conclusões sobre capítulos vêm do arquivo recebido.

## Matriz de aplicação por prioridade

As ações e critérios abaixo são propostas da nossa engenharia, não afirmações de que o livro valida a V32.

| Prioridade / capítulo | Aprendizado útil | Entrega concreta para V32 | Evidência para concluir |
|---|---|---|---|
| P0 — 2.2 Manutenção | Planejar acesso e módulos removíveis antes de ocupar o interior | Sequência de acesso a PCBase, S1/S2/S3, T1/T2/T3, telas e fans traseiros; envelopes de conectores e ferramentas | Trajetórias de remoção e acesso a fixações no CAD; evitar desmontar outro módulo sem necessidade |
| P0 — 2.19 Ferragens / 2.33 Plunger | Resolver pernas, canaletas de vidro e plunger antes dos cortes finais | Registro de interface medida para bracket, plunger, canaleta e lockdown | Medidas das ferragens reais, cupom paramétrico original e teste de encaixe; não copiar furação do STL |
| P0 — 3.22 LEDs endereçáveis | Dados, disposição física e alimentação são problemas distintos | Registro de zonas: pixels, dimensões, tensão, corrente, mapeamento, conectores e porta do controlador | Dados do painel selecionado; orçamento elétrico; teste da ordem dos pixels; depois suporte removível e folgas de movimento |
| P0 — 2.7 Alimentação / 2.21 Aterramento / 3.4 Fiação / 4.19 Fusíveis | Alimentação e proteção são infraestrutura | Diagrama funcional OFF / AUDIO ONLY / FULL PINBALL; distinguir PE, retornos DC e referências de sinal; circuitos protegidos | Documentação dos dispositivos e verificação elétrica qualificada; preservar invólucro de rede sem terminais expostos |
| P1 — 2.37 Áudio | Música e sons mecânicos espaciais precisam de roteamento próprio | Mapa canal → amplificador → exciter da interface StarTech selecionada; quatro zonas SSF | Testar canais individualmente antes de montar; reservar acesso a terminais e suportes substituíveis |
| P1 — 3.10 Diodos / 3.11 Temporização | Transientes indutivos e bobina travada ligada exigem tratamentos distintos | Registro de driver, proteção e ciclo de trabalho por dispositivo; desabilitação independente do feedback | Proteção compatível com fabricante e teste de falhas; temporização somente por software não comprova proteção |
| P1 — 2.24 Ventilação | O ar precisa atravessar o gabinete ocupado | Vista do fluxo incluindo PC, prateleiras, fontes dos LEDs, filtro de entrada e grades | Teste térmico instrumentado sob carga e portas fechadas; quantidade de fans ou área de abertura não basta |
| P1 — 2.1 Roteiro / 3.3 DOF | Integrar e testar por etapas | Checklist reproduzível e backup das configurações | Um subsistema por vez, depois integração; versões explícitas e exportação das configurações de controlador/DOF |

## Achado imediato: os seis painéis LED

Seis painéis de 16×16 contêm **1.536 pixels**. O exemplo antigo do guia para WS2812 usa 60 mA por pixel a 5 V. Aplicado apenas como cenário de sensibilidade, resulta em **92,16 A / 460,8 W** somente na matriz; um painel de 256 pixels seria 15,36 A / 76,8 W. **Não são consumo medido, recomendação de fonte ou orçamento final do projeto.** Modelo, tensão, limitação de corrente e brilho de operação aprovado podem mudar bastante o resultado. LEDs de speakers, gabinete e eventual gap são cargas adicionais.

O próximo passo útil é registrar especificações e mapeamento dos painéis antes de reservar espaço para fontes ou desenhar o suporte. A [página atual da MX-DONNY](https://shop.arnoz.com/en/dude-s-cab/151-mx-donny.html), consultada em 27/09/2026, descreve expansão da Dude's Cab com oito saídas e até 4.096 LEDs endereçáveis. Isso é capacidade de controle, não potência disponível. Preservar a [intenção de iluminação](LIGHTING_INTENT_V32.md); não adicionar a receita Teensy/OctoWS2811 do livro nem presumir sua pinagem para Arnoz.

O espaçamento de injeção de alimentação do livro se refere ao exemplo de fita utilizado. Não aplicar uma quantidade fixa de LEDs entre pontos de alimentação a painéis 16×16 ainda não selecionados. Dimensionar conectores, condutores, proteção de circuitos e queda de tensão com os dados reais. Brilho é parâmetro de configuração, não substituto da proteção dimensionada.

## O que não copiar automaticamente

- Cortes WPC em polegadas, larguras históricas, encaixes feitos com tupia manual e montagem de oficina. Permanecem o gabinete de 600 mm, compensado medido, encaixes/cupons CNC e guias substituíveis.
- Geometria específica de TV que reduza o envelope futuro, suportes que impeçam remoção, retorno de molas a gás ou da antiga gaveta de PC. V32 mantém PCBase baixo sem gaveta; escoras positivas cativas continuam exigidas, com movimento e carga ainda pendentes de verificação detalhada.
- Recomendações antigas de sistema operacional, disponibilidade, versões e compras. O livro é referência datada, não catálogo atual.
- Aterramento por simples prensagem de malha sob uma fonte removível ou leitura informal de continuidade como qualificação do produto. O projeto de proteção deve sobreviver à substituição normal de módulos e usar terminações e verificação especificadas. Esta análise não aprova uma receita de montagem da rede elétrica.
- Dimensionamento universal de supressão ou avaliação do regime de bobina pelo toque. Usar documentação do driver/carga, proteção dimensionada e testes medidos. Não adicionar diodo genérico indiscriminadamente a drivers eletrônicos de motores ou cargas AC.
- “Fan de 120 mm” como diâmetro do recorte. É tamanho nominal da moldura; abertura, furação, grade e cabos dependem do desenho/ferragem selecionados.

## Próximos três pacotes de engenharia

1. **Registro de interfaces:** bracket, plunger, vidro/lockdown, fans e painel LED; separar dimensões conhecidas das medidas faltantes. Definir cupons originais quando houver dados. Não presumir medições enquanto as sessões físicas estão pausadas.
2. **Mapa elétrico e lógico:** associar LEDs, SSF, feedback, PC e telas a alimentação, dados, manutenção e modos de operação. Criar orçamento calculável sem inventar características dos dispositivos.
3. **Revisão de manutenção e testes:** representar envelopes de acesso/remoção em estudo separado e preparar verificações reproduzíveis de bancada/configuração e aceitação integrada. Introduzir geometria apenas como proposta visível para aprovação.

O guia fornece uma boa lista de problemas e métodos; não encerra as pendências de carga, movimento, temperatura, medição de ferragens ou liberação CNC da V32.
