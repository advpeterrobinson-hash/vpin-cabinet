# Documentation language policy

[English](LANGUAGE_POLICY.md) · [Português (Brasil)](pt-BR/LANGUAGE_POLICY.md)

## Canonical language

**English is the canonical documentation language for the project.**

The purpose is to make the repository immediately accessible to international builders, CNC operators, engineers, developers and reviewers.

Portuguese (Brazil) is a first-class companion translation for owner use and Brazilian contributors, but it must not become a separate source of engineering truth.

## Repository layout

- `README.md` — canonical English landing page.
- `README.pt-BR.md` — Portuguese landing page.
- `docs/*.md` — canonical English documentation.
- `docs/pt-BR/*.md` — Portuguese translations of selected current documents.
- stable part codes such as `T1`, `S1`, `S1SupL`, `SideL` are language-neutral and must never be translated.

## What must be bilingual

Priority mirrors are required for documents that a new contributor needs before deciding whether to participate:

1. repository landing page;
2. documentation index;
3. render gallery/current visual state;
4. part-code system;
5. current design proposals that are actively under review;
6. contribution workflow and safety/manufacturing gates.

Historical evidence and superseded engineering documents do not need immediate translation. Translate them only when they become active references again or when a contributor needs them.

## Source-of-truth rule

If English and Portuguese differ on a technical statement, the **canonical English document controls until the discrepancy is corrected**.

Translations must preserve exactly:

- part codes and IDs;
- measurements and units;
- file paths;
- commands and code;
- status tokens such as `BLOCKED`, `PROVISIONAL`, `MEASURE_BEFORE_CNC`;
- URLs and license identifiers;
- formulas and test thresholds.

A translation must never silently change geometry, a measurement, a manufacturing gate or a safety condition.

## Contribution rule

Contributors may submit documentation changes in English only. A missing Portuguese mirror must not block a useful engineering contribution.

When practical, maintainers or translation automation update the Portuguese mirror after the canonical English change is accepted.

Code identifiers, source comments intended for contributors, commit messages and engineering source-of-truth fields should be English.

## Automation target

The intended future workflow is:

`edit canonical English -> validate protected technical tokens -> update PT-BR mirror -> link check -> documentation status report`

Translation generation may use local or hosted AI, but merge validation must remain deterministic and must not require an AI service.

The cleanup phase should establish a translation manifest/glossary only after the active vs historical document set is reduced, so the project does not automate translation of obsolete files.
