# Relatório de teste da skill

Esta versão da skill está em teste. Ao fim de **cada sessão**, escreva um relatório em `.agents/relatorios-skill/AAAA-MM-DD-sessao-N.md`. O usuário leva esse arquivo ao laboratório para corrigir a skill. Seja específico: cite o arquivo e a seção da skill quando apontar um problema.

## Modelo

```markdown
# Relatório de teste: sessão N (AAAA-MM-DD)

- **Versão da skill:** 0.3.0
- **Projeto:** <nome> (`<slug>`)
- **Modo:** projeto novo | projeto existente
- **Nível ao começar / ao terminar:** 1 / 1

## O que foi feito
Passos executados, na ordem, com o resultado de cada um.

## Onde a skill foi ambígua
Instruções que permitiram mais de uma interpretação. Para cada uma: arquivo e seção, o que estava escrito, como você interpretou e o que teria resolvido.

## O que faltou na skill
Situações que a skill não previu e que você teve de resolver por conta própria. O que você fez e o que a skill deveria dizer.

## O que estava errado
Regras, comandos, caminhos ou modelos que não funcionaram (por exemplo, build falhando por causa do modelo de `mkdocs.yml`). Inclua a mensagem de erro.

## Gerador de páginas
O que `gerar_paginas.py` gerou errado ou deixou de gerar (tabela, relacionamento, RLS, grupo de cálculo, medida), com o trecho do `.tmdl` que o causou. O que você teve de corrigir à mão nos blocos `gerado` (não deveria haver nada).

## Perguntas feitas ao usuário
Cada pergunta e a resposta. Marque as que a skill deveria ter respondido sozinha.

## O que foi ensinado ao usuário
Temas de `educacao-mantenedores.md` tratados nesta sessão, e o que gerou dúvida.

## Retrabalho
O que precisou ser refeito e por quê.

## Sugestões para a próxima versão
Mudanças concretas, em ordem de importância.
```
