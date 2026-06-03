# MoverArquivos Verification Report

Generated on 2026-06-03T14:12:56.959971

## Test Execution (pytest)

```
============================= test session starts =============================
platform win32 -- Python 3.13.13, pytest-9.0.2, pluggy-1.6.0
rootdir: C:\python\moverarquivos\advanced-organizer\tests
plugins: anyio-3.7.1
collected 10 items

test_organizer.py ......                                                 [ 60%]
test_strategies.py ....                                                  [100%]

============================= 10 passed in 0.45s ==============================


```

## Coverage Report

```
No data to report.


```

## Ruff Linting

```
F401 [*] `typing.Dict` imported but unused
 --> advanced-organizer\src\strategies.py:5:30
  |
3 | from abc import ABC, abstractmethod
4 | from datetime import datetime
5 | from typing import Optional, Dict
  |                              ^^^^
6 | from pdfminer.high_level import extract_text
  |
help: Remove unused import: `typing.Dict`

E741 Ambiguous variable name: `l`
  --> advanced-organizer\src\strategies.py:79:36
   |
77 |             # LÃ³gica para RazÃ£o Social
78 |             company = "Desconhecido"
79 |             lines = [l.strip() for l in text.split('\n') if l.strip()]
   |                                    ^
80 |             for i, line in enumerate(lines):
81 |                 upper_line = line.upper()
   |

Found 2 errors.
[*] 1 fixable with the `--fix` option.


```

## Executable (real mode)

```

2026-06-03 14:13:01,820 - INFO - Iniciando organização no diretório: C:\python\moverarquivos\test_dummy (Modo Simulação: False)
2026-06-03 14:13:01,820 - WARNING - Caminho não encontrado: C:\python\moverarquivos\test_dummy\Impostos
2026-06-03 14:13:01,820 - WARNING - Caminho não encontrado: C:\python\moverarquivos\test_dummy\Notas
2026-06-03 14:13:01,820 - INFO - Processando diretório: C:\python\moverarquivos\test_dummy

```

