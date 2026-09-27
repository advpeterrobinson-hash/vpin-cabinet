# Proposta de encaixe CNC do gabinete inferior

[English](../CABINET_JOINERY_PROPOSAL.md) · [Português (Brasil)](CABINET_JOINERY_PROPOSAL.md)

**STATUS: PROPOSTA — NÃO INCORPORADA À GEOMETRIA V32 — NÃO LIBERADA PARA CNC.**

## Intenção

Transformar o gabinete inferior em um conjunto autoindexado durante a montagem: as peças principais devem localizar umas às outras mecanicamente antes da cola e dos parafusos estruturais, reduzindo erro de esquadro e dependência de marcação manual.

A ideia inicialmente descrita como “pequeno chanfro” é tratada aqui como **rasgo/dado/rebaixo CNC raso de captura**. Não é um chanfro ornamental de borda.

## Precedente de engenharia já existente

O projeto já previa encaixe capturado em `config/cabinet_structure_v20.json`:

- compensado nominal: 18 mm;
- profundidade nominal do rasgo: 6 mm;
- material nominal remanescente atrás do rasgo: 12 mm;
- folga nominal inicial: 0,2 mm;
- ajuste final condicionado à espessura real do compensado e a um coupon de tolerância CNC.

Essa geometria é um bom ponto de partida de engenharia, mas **não está automaticamente aprovada para V32**.

## Conceito proposto

### 1. Floor ↔ SideL / SideR

Usinar em cada lateral um rasgo longitudinal raso que receba a borda de `Floor`.

Objetivos:

- localizar Z e manter o piso paralelo;
- impedir escorregamento durante a colagem;
- aumentar a área de cola;
- permitir montagem completa a seco antes dos parafusos estruturais.

Ponto de partida para protótipo:

- profundidade: **6 mm nominal**;
- largura do rasgo: **espessura real medida do painel** + folga definida pelo coupon;
- o rasgo não pode atravessar a lateral;
- nenhum rasgo pode entrar em zonas críticas de parafusos das pernas, inserts ou ferragens.

### 2. Front / Rear ↔ SideL / SideR

Usar rebaixos/dados capturados nos encontros das extremidades para que `Front` e `Rear` encontrem posição sem medição manual.

O detalhe final pode usar:

- dado + lingueta;
- rebaixo/rabbet capturado;
- outro ombro de localização compatível com a fresa.

A escolha deve priorizar seção estrutural, área de cola, montagem simples e usinagem simples.

### 3. S1 / S2 / S3

As prateleiras **não devem automaticamente receber rasgos profundos nas laterais estruturais principais**. Primeiro comparar:

A. manter `S#SupL/R` como peças de apoio substituíveis;  
B. usar rasgo raso diretamente na lateral;  
C. usar interface híbrida capturada no apoio substituível, preservando a lateral.

Preferência inicial: **preservar a lateral principal** e usar `S1SupL/R`, `S2SupL/R` e `S3SupL/R` como interface das prateleiras. Isso mantém reparabilidade e evita multiplicar cortes em uma peça estrutural grande.

### 4. T1 / T2 / T3

Manter o princípio V32:

- nenhuma ranhura profunda da travessa diretamente na lateral estrutural;
- `T1GuideL/R`, `T2GuideL/R` e `T3GuideL/R` recebem desgaste e geometria de ajuste;
- as guias permanecem substituíveis.

## Sequência pretendida de montagem

1. posicionar `SideL` sobre referência plana;
2. encaixar `Floor` a seco no rasgo de captura;
3. instalar `Front` e `Rear`;
4. instalar `SideR` e fechar a caixa;
5. instalar temporariamente peças internas que definam a largura;
6. verificar assentamento completo de todos os ombros de localização;
7. medir diagonais e largura externa;
8. desmontar se necessário;
9. aplicar cola somente nas juntas estruturais aprovadas;
10. remontar pelo mesmo caminho autoindexado;
11. prensar;
12. verificar o esquadro novamente;
13. somente então instalar os parafusos/fixadores estruturais definidos.

Os parafusos estruturais não devem ser usados para puxar uma junta mal usinada até a posição correta.

## Proteções estruturais

Nenhum rasgo é liberado apenas por ser conveniente no CAD. Antes da adoção:

- medir a espessura real do compensado;
- usinar coupon de tolerância usando o mesmo tipo de chapa e a mesma fresa;
- manter seção residual adequada atrás de cada rasgo;
- manter distância adequada de bordas, furos, inserts e fixadores;
- excluir zonas de carga das pernas e dobradiças;
- evitar concentração de rasgos próximos;
- preservar as lâminas externas do compensado quando possível;
- exigir montagem a seco por pressão manual, sem martelamento pesado;
- testar fisicamente rigidez e comportamento de falha antes da liberação para fabricação.

### Regra inicial de profundidade

`6 mm em compensado nominal de 18 mm` permanece apenas como **baseline de teste**, deixando aproximadamente 12 mm atrás do rasgo. A profundidade final deve seguir medição do material e ensaios; não deve ser aumentada apenas para produzir um encaixe mais apertado.

## Controle do encaixe CNC

A largura do rasgo não deve ser fixada em “18,0 mm” por conveniência. Compensado nominal varia.

Fluxo obrigatório:

`medir chapa -> usinar coupon -> testar encaixe manual -> registrar offset -> gerar toolpath`

A junta deve assentar com pressão manual previsível e espaço suficiente para cola. Interferência excessiva pode impedir o assentamento completo ou danificar as lâminas do compensado.

## Raio da fresa e dogbones

Cantos internos devem respeitar o raio real da fresa. Dogbones só devem aparecer onde uma lingueta quadrada realmente precise alcançar um canto interno; não devem ser adicionados a bordas visíveis por padrão.

## Próxima etapa proposta

Na próxima iteração CAD:

- recuperar o princípio de **captured flat-pack joinery** já presente no v20;
- aplicar primeiro em `Floor ↔ SideL/SideR` e `Front/Rear ↔ SideL/SideR`;
- manter prateleiras e travessas em interfaces substituíveis até concluir a comparação estrutural;
- gerar vista explodida mostrando a sequência de encaixe;
- fabricar coupon físico de tolerância antes de qualquer CNC do gabinete completo;
- comparar a geometria proposta contra a V32 quanto a colisões, seção residual e zonas de ferragens.

Até esses itens passarem, este documento permanece uma proposta e a V32 publicada continua sendo a referência visual atual.

Um [experimento CAD separado com sólidos salvos](JOINERY_STUDY_V32.md) agora ilustra esta proposta. Ele não incorpora os encaixes à V32.
