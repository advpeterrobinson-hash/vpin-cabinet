# Proposta de encaixe CNC do gabinete inferior / Lower-cabinet CNC joinery proposal

**STATUS: PROPOSTA — NÃO INCORPORADA À GEOMETRIA V32 — NÃO LIBERADA PARA CNC.**

## Intenção

Transformar o gabinete inferior em um conjunto autoalinhável durante a montagem: as peças devem localizar umas às outras mecanicamente antes da cola e dos parafusos, reduzindo erro de esquadro e dependência de marcação manual.

A ideia descrita como “pequeno chanfro” é tratada tecnicamente aqui como **rasgo/dado/rebaixo CNC raso de captura**. Não é um chanfro ornamental de borda.

## Por que faz sentido

O próprio histórico do projeto já previa, em `config/cabinet_structure_v20.json`, encaixe capturado com:

- compensado nominal: 18 mm;
- profundidade nominal do rasgo: 6 mm;
- material nominal remanescente: 12 mm;
- folga nominal inicial: 0,2 mm;
- ajuste final condicionado à espessura real do compensado e ao coupon da CNC.

Essa proporção é um bom ponto de partida de engenharia, mas **não é automaticamente aprovada para V32**.

## Conceito proposto

### 1. Floor ↔ SideL / SideR

Criar em cada lateral um rasgo longitudinal raso que receba a borda do `Floor`.

Objetivo:

- localizar Z e manter o piso paralelo;
- impedir escorregamento durante a colagem;
- aumentar superfície de cola;
- permitir montagem a seco antes dos parafusos.

Ponto de partida para protótipo:

- profundidade: **6 mm nominal**;
- largura do rasgo: espessura **real** do painel + folga definida pelo coupon;
- fundo do rasgo sem atravessar a lateral;
- nenhum rasgo dentro de zonas críticas de parafusos das pernas ou ferragens.

### 2. Front / Rear ↔ SideL / SideR

Usar rebaixo/encaixe capturado nas extremidades para que frente e traseira encontrem posição sem medição manual.

O detalhe final pode ser:

- dado + lingueta;
- rebaixo/rabbet capturado;
- ombro CNC equivalente compatível com a fresa.

A escolha deve priorizar resistência, área de cola, acesso de montagem e usinagem simples.

### 3. S1 / S2 / S3

As prateleiras **não devem automaticamente receber rasgos profundos nas laterais estruturais**. Antes disso, comparar:

A. manter `S#SupL/R` como peças de apoio substituíveis;  
B. rasgo raso direto na lateral;  
C. encaixe híbrido em apoio substituível, preservando a parede lateral.

Preferência inicial: **preservar a lateral** e usar os suportes codificados `S1SupL/R`, `S2SupL/R`, `S3SupL/R` como interface de montagem, porque isso mantém reparabilidade e evita multiplicar cortes em uma peça estrutural grande.

### 4. T1 / T2 / T3

Manter o princípio V32:

- nenhuma ranhura profunda diretamente na lateral;
- `T1GuideL/R`, `T2GuideL/R`, `T3GuideL/R` recebem o desgaste e a geometria de ajuste;
- as guias permanecem substituíveis.

## Sequência pretendida de montagem

1. posicionar `SideL` sobre referência plana;
2. encaixar `Floor` no rasgo de captura sem cola;
3. encaixar `Front` e `Rear`;
4. posicionar `SideR`, fechando o conjunto;
5. instalar temporariamente peças internas que funcionem como referências de largura;
6. verificar assentamento completo dos ombros;
7. medir diagonais e largura externa;
8. desmontar se necessário;
9. aplicar cola nas juntas estruturais aprovadas;
10. remontar pelo mesmo caminho autoindexado;
11. clamp/prensagem;
12. verificar esquadro novamente;
13. somente então instalar os parafusos estruturais definidos.

Os parafusos não devem ser usados para “puxar” uma junta mal usinada até o lugar.

## Critérios para não perder estrutura

Nenhum rasgo é liberado apenas por parecer conveniente no CAD. Antes da adoção:

- verificar espessura real do compensado;
- executar coupon de tolerância com a mesma fresa/material;
- manter seção residual suficiente atrás do rasgo;
- manter distância adequada de bordas, furos e inserts;
- excluir zonas de carga das pernas e dobradiças;
- evitar concentração de rasgos próximos;
- preservar fibras/camadas externas sempre que possível;
- testar montagem seca sem martelamento pesado;
- fazer prova física de rigidez e falha antes da liberação de produção.

### Regra inicial de profundidade

`6 mm em 18 mm nominal` é mantido apenas como **baseline de teste**, porque deixa aproximadamente 12 mm atrás do rasgo. A profundidade final será derivada do material real e dos ensaios; não deve ser aumentada só para obter encaixe mais “firme”.

## Ajuste CNC

A largura não deve ser fixada em “18,0 mm” por conveniência. Compensado nominal varia.

Fluxo obrigatório:

`medir chapa -> usinar coupon -> testar encaixe manual -> registrar offset -> gerar toolpath`

A junta deve entrar com pressão manual previsível e espaço para cola. Interferência excessiva pode delaminar o compensado ou impedir o assentamento completo.

## Dogbones e raio da ferramenta

Cantos internos devem respeitar o raio real da fresa. Dogbones são usados apenas onde uma lingueta quadrada realmente precisa alcançar o canto interno; não devem aparecer em bordas visíveis por padrão.

## Decisão de engenharia proposta

Para a próxima iteração CAD:

- recuperar o conceito de **captured flat-pack joinery** já existente no v20;
- aplicar primeiro a `Floor ↔ SideL/SideR` e aos encontros `Front/Rear ↔ SideL/SideR`;
- manter prateleiras e travessas em interfaces substituíveis até avaliação estrutural;
- renderizar uma vista explodida mostrando a sequência de encaixe;
- produzir coupon físico antes de qualquer CNC do gabinete completo;
- comparar a geometria com V32 em validação de colisão e seção residual.

Até esses itens passarem, esta página é uma proposta e a V32 publicada continua sendo a referência visual atual.
