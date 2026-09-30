# V32 — dogbones, cantos de fresa e encaixes

**Dogbones estão considerados como requisito, mas não estão resolvidos em todo o gabinete.** Os arquivos anteriores contêm cantos internos ideais em várias operações. O desenho exportar corretamente não prova que a fresa consegue produzir esses cantos.

A regra é acrescentar alívio somente quando a peça de canto reto precisa ocupar o canto interno. Furos circulares não precisam de dogbone. Recortes com raio especificado pelo componente devem preservar esse raio. Encaixes abertos ou com espaço livre no fim podem dispensar alívio. A fresa real ainda não foi confirmada;6 mm é hipótese de ensaio, não escolha final para a oficina.

## Ensaio das seis guias de travessas

[CAD separado](../exports/generated/corner-relief-v32/natural-guide-corners.FCStd) · [Validação](../exports/generated/corner-relief-v32/validation.json) · [Inventário de decisões](../config/corner_relief_v32.json).

As guias substituíveis T1/T2/T3 têm canal nominal18,4 mm, profundidade6 mm, aberto no topo. O fim inferior do canal está25 mm abaixo da travessa instalada. Com uma fresa hipotéticaØ6, os cantos inferiores deixam material arredondadoR3, mas ainda restam22 mm até a travessa. **Não é necessário dogbone nesses cantos para a posição atual.**

O estudo acrescenta ao CAD os dois resíduos de canto por guia que a geometria ideal anterior omitia. Preserva os limites externos e não aprofunda o canal nem corta a lateral estrutural. Não migra automaticamente essa proposta para o arquivo integrado aprovado; a ferramenta e as demais operações da guia ainda precisam ser confirmadas.

Verificação negativa: deslocar a travessa até o fundo do canal faz seu canto reto colidir com o materialR3. Isso demonstra que a dispensa de dogbone depende da posição atual, não de uma regra geral. Se houver mudança de apoio/altura ou encaixe até o fundo, reavaliar o alívio.

## Situação por interface

| Interface | Tratamento atual | Pendência |
|---|---|---|
| Seis guias das travessas | R3 ensaiado, sem dogbone necessário na posição atual | Fresa real e confirmação da operação |
| Rasgos de piso e rebaixos da caixa capturada | Ainda cantos ideais na proposta separada | Aceitação da união; fresa, interseções, alívio e sequência de corte |
| Energia | Recorte28×48R3 do desenho enviado | Confirmar encaixe; não substituirR3 por dogbones |
| RJ45, fans e furos circulares | Sem canto interno reto | Diâmetros e processos de furação/CAM |
| Entradas de ar e molduras de filtros | Preferir raio natural se nenhuma peça quadrada ocupar o canto | Raios ainda não aplicados; filtro real e cobertura |
| Porta de moedas e acesso traseiro | Ainda verificar cantos contra corpo da ferragem e passagem de serviço | Não aplicar alívio visível indiscriminadamente |
| Demais bolsões/rasgos | Revisão por operação e peça encaixada | Inventário final de CAM ainda incompleto |

Não cortar dogbones nas faces cosméticas por padrão. Quando necessários, o raio/posição do alívio deve ser dirigido pela fresa e conferido contra pele remanescente, furos, fixadores e caminho de carga. Um alívio adicional não deve invadir essas regiões só para resolver o encaixe.

## Evidência e próximos passos

`bash tools/run_corner_relief_v32.sh`:42 verificações, incluindo seis controles negativos. Seis guias válidas, limites externos preservados, material de canto calculado, travessas livres, ausência de novas colisões no conjunto, simetria, somente seis peças alteradas, reabertura do arquivo e fontes intactas. O CAD salvo contém195 sólidos como o estudo de origem; não é prova de carga nem arquivo CAM.

Antes da fabricação, completar o inventário de operações, confirmar ferramenta/espessura/folgas, gerar os alívios que efetivamente faltarem e ensaiar as uniões em cupom. O cupom de conectores anterior testa esses conectores, **não substitui um cupom de encaixe/dogbone da caixa**. CNC permanece sem liberação.

Original CERN-OHL-S-2.0. Preservar LICENSE e NOTICE.md. Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet
