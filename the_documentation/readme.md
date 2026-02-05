## Visão Geral

O projeto consiste na implementação completa de um **compilador** dividido em duas grandes partes:

* **Parte 1**: Análise (léxica, sintática e semântica) + **geração de código objeto** para uma linguagem de máquina hipotética, salvando o resultado em arquivo.

* **Parte 2**: **Leitura e execução** do código objeto gerado, simulando a máquina hipotética conforme visto em aula.

---

## Fluxo Geral do Projeto

### 1. Arquivo de Código-Fonte (Entrada)

* Arquivo de texto contendo o programa escrito na linguagem definida pela gramática do trabalho.
* Exemplo: `programa.py`
* Este será recebido na Main mesmo

---

### 2. Analisador Léxico (Lexer / Scanner)

**Responsabilidades:**

* Ler o código-fonte caractere por caractere
* Agrupar caracteres em **tokens**
* Identificar lexemas inválidos

**Entradas:**

* Código-fonte em texto

**Saídas:**

* Sequência de tokens (tipo, lexema, linha, coluna)

**Exemplos de tokens:**

* Identificadores
* Palavras-chave
* Operadores
* Literais
* Delimitadores

---

### 3. Analisador Sintático (Parser)

**Responsabilidades:**

* Verificar se a sequência de tokens obedece à gramática
* Construir a estrutura sintática do programa

**Tipo:**

* Descendente (LL, recursivo) **ou**
* Ascendente (LR, conforme RGA)

**Entradas:**

* Tokens gerados pelo analisador léxico

**Saídas:**

* Árvore sintática (explícita ou implícita)
* Erros sintáticos, se existirem

---

### 4. Analisador Semântico

**Responsabilidades:**

* Verificar regras semânticas da linguagem

**Exemplos:**

* Variáveis declaradas antes do uso
* Tipos compatíveis em expressões
* Escopo de variáveis

**Estruturas comuns:**

* Tabela de símbolos
* Pilha de escopos

**Entradas:**

* Estrutura sintática validada

**Saídas:**

* Programa semanticamente válido
* Erros semânticos, se existirem

---

### 5. Tradutor / Gerador de Código Objeto (Parte 1)

**Responsabilidades:**

* Converter o programa validado em **código de máquina hipotética**
* Traduzir comandos de alto nível para instruções simples

**Entradas:**

* Resultado da análise semântica

**Saídas:**

* Arquivo de texto contendo o código objeto

**Exemplo:**

```txt
LOAD A
ADD B
STORE C
HALT
```

---

### 6. Arquivo de Código Objeto

* Arquivo intermediário gerado pelo compilador
* Será a entrada da Parte 2 do projeto

Exemplo:

* `programa.obj`

---

### 7. Leitor do Código Objeto (Parte 2)

**Responsabilidades:**

* Ler o arquivo de código objeto linha por linha
* Interpretar cada instrução da máquina hipotética

**Entradas:**

* Arquivo de código objeto

**Saídas:**

* Estrutura interna de instruções

---

### 8. Executor / Máquina Virtual

**Responsabilidades:**

* Simular a execução da máquina hipotética
* Executar instruções conforme definido em aula (slides e vídeo)

**Componentes típicos:**

* Registradores
* Memória
* Contador de instruções

**Resultado:**

* Execução correta do programa
* Exibição de resultados (prints, valores finais, etc.)

---

## Resumo do Pipeline

```
Código-Fonte (.py)
      ↓
Analisador Léxico
      ↓
Analisador Sintático
      ↓
Analisador Semântico
      ↓
Gerador de Código Objeto
      ↓
Arquivo (.obj)
      ↓
Leitor de Código Objeto
      ↓
Executor / Máquina Hipotética
```

---

## Observações Importantes

* Erros devem ser tratados e reportados com linha e coluna
* A separação entre **compilação** e **execução** é obrigatória
* Código objeto deve ser salvo em arquivo de texto

