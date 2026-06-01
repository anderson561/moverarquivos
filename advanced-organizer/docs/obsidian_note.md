# MoverArquivos - Advanced Organizer

#projeto #python #automação #organizador-arquivos

## Visão Geral
Este é um sistema desenvolvido em Python estruturado com princípios **SOLID** e utilizando o padrão de projeto **Strategy** para organizar automaticamente arquivos localizados em qualquer pasta de origem fornecida pelo usuário (tendo por padrão o Desktop).

## Estratégias de Organização
O sistema distribui e organiza os arquivos sob três estratégias bem delineadas:
1. **TypeStrategy**: Classifica arquivos com base em suas extensões de arquivos em maiúsculo (ex: `.xlsx` vai para a subpasta `XLSX`).
2. **ImpostoStrategy**: Identifica e separa guias de tributos (como `DARF`, `DAS`, `IPTU`, `IPVA` e `GRERJ`) lendo o texto do PDF por meio de processamento interno.
3. **CompanyNameStrategy**: Extrai metadados estruturados de Notas Fiscais eletrônicas em PDF, determinando o `Ano / Mês / Razão Social` da empresa para estruturar a árvore de diretórios.

## Resolução de Conflitos
* **Duplicados:** Arquivos com o mesmo nome recebem um sufixo numérico correspondente à data de modificação (`mtime`).
* **Conflito de Tipo:** Se existir um arquivo físico com o mesmo nome da pasta que o organizador precisa criar, o sistema detecta e renomeia o arquivo conflitante com a marcação `_CONFLITO_F_P` antes de prosseguir.

## Setup e Execução
* O projeto possui uma suíte com **10 testes automatizados** rodando sob o `pytest`.
* Pode ser empacotado em executável `.exe` único usando o `PyInstaller`.
* Possui scripts em lote (`.bat`) amigáveis para simulação e movimentação real.

---
**Notas Relacionadas:**
* [[Python Automation Pro]]
* [[Software Craftsmanship & Architecture]]
