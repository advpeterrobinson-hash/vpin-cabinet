# Como contribuir com o Virtual Pinball Cabinet

[English](CONTRIBUTING.md) · **Português (Brasil)**

Obrigado por ajudar a melhorar o projeto. Contribuições são bem-vindas de construtores, projetistas mecânicos, operadores CNC, eletricistas, desenvolvedores, testadores e colaboradores de documentação.

> O inglês é o idioma canônico do projeto. Uma contribuição técnica útil pode ser enviada apenas em inglês; a tradução PT-BR não é requisito para aceitação.

## Antes de começar

Passe alguns minutos pelo caminho atual do projeto antes de abrir arquivos de revisões antigas:

1. [renderizações atuais](docs/pt-BR/RENDERS.md);
2. [índice da documentação](docs/pt-BR/README.md);
3. [pacote de revisão V32](exports/generated/cabinet-v32/README.md);
4. [registro de códigos permanentes](docs/pt-BR/PART_CODES.md).

Para alterações mecânicas ou arquitetônicas substanciais, abra primeiro uma issue de **Design proposal**. Correções pequenas, documentação, testes e bugs claramente isolados podem ir diretamente para pull request.

Comece pelo branch de engenharia/revisão atual indicado no README. Não presuma que branches históricos ou grupos antigos do FreeCAD sejam autoridade de design atual.

## Princípios de engenharia

Contribuições devem preservar os objetivos centrais:

- geometria estrutural pré-localizada por CNC em vez de marcação manual;
- montagem flat-pack amigável a apartamento/oficina pequena;
- medição de ferragens antes de congelar furos críticos de CNC;
- adaptadores substituíveis para eletrônica de ciclo de vida curto;
- caminhos de carga simples e inspecionáveis;
- nenhum terminal de rede elétrica exposto em áreas de serviço;
- segurança mecânica positiva para o playfield levantado;
- CAD reproduzível a partir de fontes, em vez de edição manual de um master binário.

Não invente padrões de furação de ferragens a partir de desenhos de catálogo quando o projeto marcar o item como **MEASURE_BEFORE_CNC**.

## Idioma da documentação

Inglês é canônico para documentação voltada a colaboradores, identificadores de fonte e campos de engenharia que funcionam como fonte da verdade.

Códigos estáveis como `T1`, `S1`, `S1SupL` e `SideL` são neutros em relação ao idioma e não devem ser traduzidos nem reutilizados.

Veja a [política de idiomas](docs/pt-BR/LANGUAGE_POLICY.md).

## Material atual e histórico

Documentos, configurações e ferramentas versionadas v04–v28 permanecem para preservar decisões e evidências. Isso não significa que sejam autoridade atual.

Se uma contribuição depender de arquivo antigo, explique por que ele continua relevante. O repositório está entrando em uma fase de limpeza controlada; veja o [plano de limpeza](docs/REPOSITORY_CLEANUP.md) em inglês.

## Fluxo de pull request

1. Faça fork ou crie um feature branch.
2. Mantenha a alteração focada e explique a razão de engenharia.
3. Atualize configs/fontes da verdade antes dos artefatos gerados.
4. Adicione ou atualize validação quando geometria ou regras mudarem.
5. Rode os checks locais relevantes.
6. Inclua screenshots ou views geradas para mudanças visuais.
7. Liste medições, hipóteses e gates de fabricação ainda não resolvidos.

Checks típicos:

```bash
make doctor
make validate
make build-current
git diff --check
```

## Licença

O projeto usa **CERN-OHL-S-2.0**. Ao enviar contribuição, você declara ter direito de fazê-lo e concorda em fornecê-la sob os mesmos termos.

Não adicione CAD, desenhos, imagens, manuais, código ou dados de terceiros sem direitos claros de redistribuição e documentação da fonte/licença.

## Arquivos gerados

Não faça commit de binários ou grandes arquivos gerados, salvo quando forem intencionalmente parte de um pacote de revisão/release ou forem solicitados especificamente.

## Expectativas de revisão

Um mantenedor pode solicitar:

- raciocínio mais claro do caminho de carga;
- medições físicas;
- construção mais simples;
- testes negativos adicionais;
- alteração menor/modular;
- remoção de geometria especulativa específica de hardware;
- prova de que a solução pode ser fabricada e montada com o conjunto de ferramentas pretendido.

Testes passando são necessários, mas não tornam automaticamente um design pronto para fabricação.
