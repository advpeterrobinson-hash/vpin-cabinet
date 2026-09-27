# Estudo de encaixes da caixa inferior — comparação com V32

[English](../JOINERY_STUDY_V32.md) · [Português (Brasil)](JOINERY_STUDY_V32.md)

**PROPOSAL_NOT_ADOPTED — V32 publicada sem alterações — CNC BLOCKED.**

Este é o primeiro experimento virtual da [proposta de encaixes](CABINET_JOINERY_PROPOSAL.md), não uma nova arquitetura aprovada ou revisão de fabricação. Ele avalia o posicionamento mútuo dos cinco painéis da caixa, preservando o exterior e os componentes internos atuais.

## Imagens para revisão

![Cortes dos encaixes extraídos do CAD](../../exports/generated/joinery-study-v32/01-joint-sections.png)

![Caixa proposta em vista explodida](../../exports/generated/joinery-study-v32/02-exploded-shell.png)

![Diferenças geométricas medidas](../../exports/generated/joinery-study-v32/03-change-summary.png)

A vista explodida separa as peças para identificação; não comprova todo o movimento de montagem nem acesso para ferramentas/mãos. Os 40 objetos preservados estão ocultos somente nessa vista, não removidos do FCStd do estudo.

## Mudanças geométricas explícitas

| Peça | V32 | Candidato do estudo |
|---|---|---|
| SideL / SideR | Caixa com juntas de topo | Rasgo interno de 6 mm para Floor e rebaixos abertos nas extremidades; 12 mm nominais de parede externa preservados |
| Floor | Largura 564 mm, X18..582 | Largura 576 mm, X12..588; entrada de 6 mm por lado |
| Front | Largura 564 mm, X18..582 | Largura 576 mm, X12..588; aberturas de coin door/controles preservadas |
| Rear | Largura 564 mm, X18..582 | Largura 576 mm, X12..588; abertura de serviço preservada |
| Outros 40 objetos | V32 existente | Geometria dos sólidos salvos preservada integralmente |

Largura externa continua 600 mm e comprimento das laterais 1308,1 mm. Alturas externas dianteira/traseira, prateleiras, PCBase, fans, travessas, guias, envelope do display e apoios do monitor permanecem iguais. Os apoios do piso continuam presentes; este experimento não elimina um caminho de carga apenas porque existe um rasgo.

O rasgo do piso percorre Y18..1290.1 e Z17.9..36.1: largura experimental de 18,2 mm ao redor de um painel de 18 mm. Os rebaixos dos painéis de extremidade têm 0,1 mm de folga para dentro em Y. São abertos nas extremidades/perfil superior; o dianteiro evita deixar uma pequena aba acima de Front. São cortes CAD ideais com cantos vivos. O alívio para raio de fresa nas interseções **ainda não foi definido**: estes arquivos não são percursos de usinagem.

As cinco identidades existentes permanecem. `ProposedRevision=R2-PROPOSAL` distingue o experimento; não significa R2 aceita e não cria códigos definitivos. O material nominal está deliberadamente fixado ao baseline V32 de 18 mm; outra espessura exige regeneração paramétrica completa, não apenas editar esse campo do estudo.

## Verificação

`make review-joinery` lê o FCStd V32 do commit, cria um documento separado e reabre os sólidos reais para verificação. Não edita V32 nem o master histórico do proprietário.

- **45 objetos válidos com um sólido cada**, mesmas identidades e nomes bilíngues.
- Exatamente cinco interfaces alteradas e **40 objetos geometricamente idênticos**.
- Nenhuma interseção volumétrica entre pares acima de 0,01 mm³.
- Vazios dos encaixes, entrada das bordas, parede externa e aberturas originais verificados geometricamente.
- **28 verificações passam**, além de quatro controles negativos: parede fina, prateleira alterada, recorte da coin door fechado e rasgo ausente.
- O [relatório](../../exports/generated/joinery-study-v32/validation.json) informa volumes removidos/adicionados e limites antes/depois para cada peça alterada.

Esses testes não comprovam resistência. Os 12 mm residuais são a seção nominal proposta, não capacidade demonstrada. Furos de referência existentes são preservados; isso não comprova afastamento de chapas de pernas, arruelas, parafusos ou regiões de carga das dobradiças reais.

## Bloqueios e sequência seguinte

1. Revisar visualmente a direção dos encaixes; não incorporá-los silenciosamente à V32.
2. Obter os envelopes medidos de pernas/suportes e fixação/cargas do backbox antes de decidir se os rasgos podem ser contínuos. O afastamento está **BLOCKED_UNMEASURED**; nenhum envelope histórico é usado como comprovação.
3. Definir raio da fresa e alívios locais com material e coupon reais. Não aprofundar rasgos para forçar um encaixe ruim.
4. Detalhar fixação pré-localizada por CNC e montagem a seco; depois verificar resistência/retenção. Sessões físicas continuam pausadas; nenhum ensaio é presumido concluído.
5. Somente após aceitação e validação, migrar a geometria para a próxima arquitetura aprovada e aposentar interfaces anteriores deliberadamente.

A matriz de LEDs continua como [intenção separada](LIGHTING_INTENT_V32.md): painéis, arranjo, alimentação e folgas de serviço estão indefinidos. Não foram adicionados envelope de LED presumido nem amortecedores a gás.

## Reproduzir / baixar

- `make review-joinery` — geração, sólidos salvos, controles negativos e três imagens em inglês.
- [FCStd do estudo](../../exports/generated/joinery-study-v32/captured-shell-proposal.FCStd).
- [Parâmetros](../../config/joinery_study_v32.json).
- [Fonte](../../tools/joinery_study.py).

Pacote de evidência de engenharia, não liberação CNC. Material original: CERN-OHL-S-2.0. Preserve [LICENSE](../../LICENSE), [NOTICE.md](../../NOTICE.md) e o Source Location oficial: https://github.com/advpeterrobinson-hash/vpin-cabinet.
