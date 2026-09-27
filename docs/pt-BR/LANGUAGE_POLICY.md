# Política de idiomas da documentação

[English](../LANGUAGE_POLICY.md) · [Português (Brasil)](LANGUAGE_POLICY.md)

## Idioma canônico

**O inglês é o idioma canônico da documentação do projeto.**

O objetivo é tornar o repositório imediatamente acessível a construtores, operadores CNC, engenheiros, desenvolvedores e revisores internacionais.

Português (Brasil) é uma tradução de primeira classe para uso do proprietário e colaboradores brasileiros, mas não deve se tornar uma fonte de engenharia separada.

## Estrutura do repositório

- `README.md` — página inicial canônica em inglês.
- `README.pt-BR.md` — página inicial em português.
- `docs/*.md` — documentação canônica em inglês.
- `docs/pt-BR/*.md` — traduções em português de documentos atuais selecionados.
- códigos estáveis como `T1`, `S1`, `S1SupL`, `SideL` são neutros em relação ao idioma e nunca devem ser traduzidos.

## O que deve ser bilíngue

Devem ter prioridade de tradução os documentos necessários para um novo colaborador decidir se participa:

1. página inicial do repositório;
2. índice da documentação;
3. galeria de renderizações/estado visual atual;
4. sistema de códigos de peças;
5. propostas atuais em revisão;
6. fluxo de contribuição e bloqueios de segurança/fabricação.

Documentos históricos e engenharia superada não precisam de tradução imediata. Devem ser traduzidos apenas quando voltarem a ser referência ativa ou quando um colaborador precisar deles.

## Regra de fonte da verdade

Se inglês e português divergirem em uma afirmação técnica, o **documento canônico em inglês prevalece até a correção da divergência**.

Traduções devem preservar exatamente:

- códigos e IDs de peças;
- medidas e unidades;
- caminhos de arquivos;
- comandos e código;
- estados como `BLOCKED`, `PROVISIONAL`, `MEASURE_BEFORE_CNC`;
- URLs e identificadores de licença;
- fórmulas e limites de teste.

Uma tradução nunca pode alterar silenciosamente geometria, medida, bloqueio de fabricação ou condição de segurança.

## Regra para contribuições

Colaboradores podem enviar alterações de documentação apenas em inglês. A ausência de tradução em português não deve bloquear uma contribuição técnica útil.

Quando possível, mantenedores ou automação de tradução atualizam o espelho em português após a aceitação da alteração canônica.

Identificadores de código, comentários-fonte destinados a colaboradores, mensagens de commit e campos-fonte de engenharia devem usar inglês.

## Meta de automação

O fluxo futuro pretendido é:

`editar inglês canônico -> validar tokens técnicos protegidos -> atualizar espelho PT-BR -> checar links -> relatório de estado da documentação`

A geração da tradução pode usar IA local ou hospedada, mas a validação para merge deve ser determinística e não depender de serviço de IA.

O manifesto/glossário de tradução deve ser criado após a fase de limpeza reduzir o conjunto de documentos ativos, evitando automatizar tradução de arquivos obsoletos.
