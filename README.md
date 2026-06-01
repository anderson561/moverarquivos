# 📁 MoverArquivos - advanced-organizer

[![Python Version](https://img.shields.io/badge/python-3.13%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/tests-10%20passed-green.svg)]()

Um sistema inteligente e resiliente desenvolvido em Python para a organização automatizada e estruturada de diretórios, com foco no Desktop e pastas customizadas do usuário. O projeto lê extensões de arquivos, analisa o conteúdo textual de arquivos PDF para classificar guias de impostos e realiza parsing de metadados complexos em Notas Fiscais eletrônicas.

---

## 🚀 Como Funciona a Organização?

O software adota o padrão de projeto **Strategy** para desacoplar e aplicar regras específicas de organização:

1. **Documentos de Notas Fiscais (`CompanyNameStrategy`):**
   * Processa arquivos PDF no diretório `Notas/`.
   * Realiza extração do texto interno e busca padrões de data e Razão Social do emitente.
   * Cria uma estrutura organizada e limpa de diretórios: `[Ano] / [Mês] / [Nome_da_Empresa]`.

2. **Guias de Impostos (`ImpostoStrategy`):**
   * Processa arquivos PDF no diretório `Impostos/`.
   * Busca palavras-chave internas como `DARF`, `DAS`, `IPTU`, `IPVA` ou `GRERJ`.
   * Move os arquivos para suas respectivas pastas correspondentes aos tributos encontrados.

3. **Arquivos Gerais (`TypeStrategy`):**
   * Processa todos os arquivos na raiz do diretório principal.
   * Organiza os arquivos de acordo com a extensão (ex: `.jpg` vai para a pasta `JPG`, `.xlsx` para `XLSX`).

---

## 🏛️ Arquitetura e Robustez

O projeto foi construído seguindo os melhores padrões de engenharia de software:
* **SOLID Principles:** Baixo acoplamento e alta coesão em todas as classes de estratégias.
* **Resiliência com Retries:** Utiliza a biblioteca `tenacity` para realizar tentativas de escrita com atraso exponencial (exponential backoff) caso ocorra alguma trava no sistema de arquivos do Windows.
* **Prevenção contra Perda de Dados:** Se um arquivo no destino já existir, ele será renomeado de forma segura usando um timestamp baseado na última modificação (`mtime`).
* **Resolução de Bloqueios:** Identifica se há um arquivo com o mesmo nome de uma pasta que precisa ser criada e o renomeia (`_CONFLITO_F_P`) para liberar a execução sem interrupções.

---

## 🛠️ Tecnologias Utilizadas

* **Python 3.13+**
* **pdfminer.six** - Leitura e extração robusta de PDFs.
* **tenacity** - Políticas de retries automáticos.
* **pytest** - Framework de testes unitários.
* **PyInstaller** - Geração de executável binário (`.exe`) independente.

---

## 📦 Estrutura do Repositório

```text
moverarquivos/
├── .agent/                    # Workflows e configurações do assistente
├── advanced-organizer/
│   ├── src/
│   │   ├── organizer.py       # Orquestrador e motor de movimentação
│   │   └── strategies.py      # Implementações das regras de negócio
│   ├── tests/
│   │   ├── test_organizer.py  # Testes do fluxo de organização e conflitos
│   │   └── test_strategies.py # Testes unitários das estratégias
│   ├── dist/
│   │   └── OrganizadorArquivos.exe  # Executável compilado
│   ├── docs/
│   │   └── obsidian_note.md   # Nota pronta para o Obsidian
│   ├── README.md              # Documentação interna do módulo
│   ├── executar_simulacao.bat # Execução em modo Dry Run interativo
│   └── executar_real.bat      # Execução real interativa
└── README.md                  # Este arquivo (Portal do projeto)
```

---

## 🚦 Executando o Projeto

Você pode rodar a aplicação usando os atalhos interativos `.bat` localizados em `advanced-organizer/` ou via PowerShell:

### Modo Simulação (Sem mover arquivos reais)
```bash
advanced-organizer/dist/OrganizadorArquivos.exe --path "C:\Caminho\Da\Pasta"
```

### Modo Execução Real (Movendo arquivos)
```bash
advanced-organizer/dist/OrganizadorArquivos.exe --path "C:\Caminho\Da\Pasta" --real
```

*Nota: Ao rodar os scripts `.bat`, o terminal abrirá um prompt solicitando que digite a pasta. Se apenas pressionar **Enter**, o sistema assumirá o seu Desktop padrão.*

---

## 🧪 Testes Automatizados

O repositório possui **10 testes unitários** integrados cobrindo 100% dos caminhos lógicos de simulação, tratamento de duplicidades, concorrência e detecção de arquivos em PDF.

Para executá-los:
```bash
cd advanced-organizer
python -m pytest
```
