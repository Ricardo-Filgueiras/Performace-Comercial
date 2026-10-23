<!-- Parte do padrão. Índice em padrao.md. -->
# 2. Princípios de escrita

1. **Cada página tem propósito único.** Se duas páginas parecem repetir a mesma coisa, uma delas está fora do lugar. Escreva uma vez e aponte com link nos outros lugares.
2. **Dois públicos.** O menu de cada projeto tem três blocos: *Para quem usa* (área de negócio), *Para quem mantém* (time de BI) e *Arquivo* (guias ocultas, rascunhos, medidas de teste e sem uso). *Por quê:* comprador e desenvolvedor procuram coisas diferentes; misturados, os dois se perdem.
3. **Nomenclatura: página × guia.** "Página" é uma página desta documentação; "guia" é uma aba do relatório no Power BI.
4. **Nome de arquivo estável.** O nome do arquivo segue o assunto, não o nome atual da guia ou da pasta de exibição. Renomear uma guia não pode quebrar a URL.
5. **Quebrar uma página só quando ela ficar grande demais para ler de relance**, usando uma organização que já existe (pastas de exibição, guias do relatório). Exceção: as guias do relatório já nascem uma por página.
6. **Não inventar; marcar o que falta.** O que não está nos arquivos vira um aviso de pendência:

    ```markdown
    !!! pendente "A confirmar"
        Qual é o objetivo da guia *Home* e quem a usa?
    ```

    Toda pendência também entra em `pendencias.md`. *Por quê:* uma afirmação errada escrita com confiança é pior que uma pergunta aberta.
7. **A documentação se adapta ao modelo, nunca o contrário.** A primeira rodada só lê o `.SemanticModel` e o `.Report`. Medidas sem pasta de exibição vão para uma página própria. Problemas viram pendência, não correção.
8. **Escrita com agente de IA, revisão humana.** O agente escreve as páginas; o autor revisa linha a linha contra o projeto. O agente confere contagens e dependências com o script de levantamento em vez de contar à mão.
9. **Dupla validação.** A data de uma página mostra quando ela mudou, não se está correta.
    - **Validação técnica:** pull request revisado por outra pessoa do time de BI.
    - **Validação de negócio:** a área responsável confirma a **regra** e um **resultado de exemplo** que ela conhece. O negócio nunca valida o DAX; a tradução para DAX é responsabilidade do BI.
10. **Fronteira de escopo.** A linhagem documentada começa no fluxo de dados (ou na fonte que o modelo lê). O que acontece antes é de outro projeto. A fronteira fica registrada em `fontes-de-dados.md`: equipe responsável, link da documentação do pipeline, horário de atualização e colunas que o painel usa.
11. **Nenhuma medida sem pasta de exibição ao final de uma tarefa no modelo.** É uma regra para quem altera o modelo, registrada no guia do desenvolvedor. A documentação não corrige isso: só registra.
12. **Docstring em duas camadas no modelo.** `///` antes de `measure 'Nome' =` vira a descrição exibida no Power BI; `/* */` na primeira linha da expressão aparece na barra de fórmulas. Adicioná-las é uma etapa posterior, em commits próprios, fora da documentação inicial.
