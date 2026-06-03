# Layout NFS-e Salvador / BA

Nota sobre a implementação e suporte do layout de Nota Fiscal de Serviços Eletrônica (NFS-e) de Salvador / BA.

## Detalhes do Layout
- **Identificação**: Detectado via `PREFEITURA.*SALVADOR` no cabeçalho.
- **Número da NFS-e**: Rotulado como `Número NFS-e: <número>` ou em bloco de tabela após o label `Número NFS-e`.
- **Competência**: Pode aparecer no formato `Competência: DD/MM/YYYY` (por exemplo, `Competência: 01/02/2026`), necessitando de tratamento para extrair apenas o mês/ano como competência da nota fiscal.
- **Endereço (Município e UF)**: Tratado para evitar que o ruído `UF: BA` seja incorporado ao nome do município (ex: limpando `SALVADOR UF: BA` para `SALVADOR`).

## Alterações Realizadas
1. **Competência específica para Salvador**: Atualizada a expressão regular para capturar `COMPETÊNCIA: DD/MM/YYYY` e normalizar para o primeiro dia do respectivo mês.
2. **Extração de Número**: Adicionado o padrão de rótulo `Número NFS-e` para que o extrator de proximidade localize e extraia corretamente o número da nota.
3. **Limpeza do Município**: Adicionado tratamento no extrator de entidades para limpar tags de UF incorporadas no município (ex: `UF: BA`), salvando o município limpo e definindo o campo `uf` correspondente.
4. **Testes Unitários**: Criado teste `test_salvador_municipio_uf_new_layout` cobrindo o comportamento de detecção de layout, extração de número, competência e entidades de Prestador/Tomador.
