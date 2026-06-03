# MoverArquivos – Documentação Completa

---

## 📖 Visão Geral

`MoverArquivos` é um utilitário de linha‑comando escrito em Python que organiza automaticamente arquivos em pastas com base em estratégias de classificação (tipo de arquivo, impostos, notas fiscais, etc.).

- **Modo Simulação** (padrão) – apenas relata o que seria movido.
- **Modo Real** – executa a movimentação de fato.
- **Interface Gráfica Opcional** – ao omitir `--path`, o programa abre um seletor de pasta (Tkinter).

O projeto está estruturado como um **pacote Python** (`advanced‑organizer`) contendo a lógica de organização e um *executable* (`OrganizadorArquivos.exe`) gerado via PyInstaller.

---

## 🛠️ Instalação

1. **Pré‑requisitos**
   - Python 3.10 ou superior
   - `pip` (gerenciador de pacotes)
   - Windows 10/11 (o executável foi empacotado para Windows)

2. **Instalar dependências**
   ```bash
   cd C:/python/moverarquivos/advanced-organizer
   python -m venv .venv
   .venv\Scripts\activate   # PowerShell: .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

3. **Compilar o executável (opcional)**
   ```bash
   pip install pyinstaller
   pyinstaller --onefile --name OrganizadorArquivos src/organizer.py
   ```
   O binário será colocado em `dist/OrganizadorArquivos.exe`.

---

## ▶️ Uso

### Executável
```bat
rem Simulação (padrão)
dist\OrganizadorArquivos.exe

rem Execução real
dist\OrganizadorArquivos.exe --real

rem Seleção de pasta via UI (sem fornecer --path)
dist\OrganizadorArquivos.exe --real
```

### Módulo Python
```python
from advanced_organizer.src.organizer import FileOrganizer

organizer = FileOrganizer(base_path="C:/Users/ANDERSON/Desktop", dry_run=False)
organizer.organize()
```

### Argumentos de linha de comando
| Argumento | Descrição | Valor padrão |
|-----------|-----------|--------------|
| `--path`  | Caminho da pasta a ser organizada. Se omitido, abre o seletor de pasta. | `None` |
| `--real`  | Executa a movimentação real (caso contrário, só simulação). | `False` |

---

## 🏗️ Arquitetura

```
advanced-organizer/
│
├─ src/
│   ├─ organizer.py      # Core da aplicação (classe FileOrganizer)
│   └─ strategies.py    # Estratégias de classificação (Imposto, Empresa, Tipo)
│
├─ tests/                # Testes unitários (pytest)
├─ docs/                 # Esta documentação
└─ build/                # Scripts de construção (build.bat)
```

- **`FileOrganizer`**: gerencia caminhos‑e‑estratégias, itera sobre diretórios e delega a movimentação.
- **`BaseStrategy`** e subclasses (`ImpostoStrategy`, `CompanyNameStrategy`, `TypeStrategy`) determinam a sub‑pasta de destino para cada arquivo.
- **`_move_file`**: encapsula a lógica de criação de diretórios, resolução de conflitos e retry com *tenacity*.
- **Logging**: configurado para `INFO` e inclui timestamps no formato ISO‑8601.

---

## 📚 API (Python)

### `FileOrganizer`
```python
class FileOrganizer:
    def __init__(self, base_path: str = r"C:\Users\ANDERSON\Desktop", dry_run: bool = True)
    def organize(self) -> None
```
- **`base_path`** – diretório raiz a ser organizado.
- **`dry_run`** – se `True`, apenas registra as ações.

### Estratégias (`strategies.py`)
```python
class BaseStrategy:
    def get_destination_subpath(self, source_path: str) -> Optional[str]
```
- **`ImpostoStrategy`** – move arquivos relacionados a impostos para `Impostos/`.
- **`CompanyNameStrategy`** – move documentos empresariais para `Notas/`.
- **`TypeStrategy`** – classifica por extensão (PDF, IMG, DOC, etc.) em sub‑pastas apropriadas.

---

## 🤝 Contribuindo

1. Fork o repositório.
2. Crie um branch para sua feature (`git checkout -b minha-feature`).
3. Instale as dependências de desenvolvimento:
   ```bash
   pip install -r dev-requirements.txt  # inclui pytest, flake8, ruff
   ```
4. Escreva testes e garanta que `pytest` passe.
5. Submeta um Pull Request com descrição clara e changelog.

---

## 📄 Changelog

| Versão | Data | Alterações |
|--------|------|------------|
| 1.0.0  | 2026‑06‑01 | Lançamento inicial – organização por tipo, UI de seleção de pasta, modo simulação/real. |
| 1.1.0  | 2026‑06‑03 | Integração de `ruff` como linter, relatório de cobertura, script de verificação automatizado. |

---

## 📞 Contato

- **Autor**: Anderson 561 (GitHub: `anderson561`)
- **E‑mail**: anderson@example.com
- **Issues**: abra tickets em <https://github.com/anderson561/moverarquivos/issues>

---

*Documentação gerada automaticamente em 2026‑06‑03.*
