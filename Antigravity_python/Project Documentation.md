# 📚 Documentação do Projeto XML Fixer – SaaS

## Visão Geral

Este projeto fornece uma aplicação web **SaaS** para edição cirúrgica de arquivos XML. O usuário pode fazer upload de arquivos XML individuais ou em lote, visualizar as primeiras 200 linhas, e aplicar transformações específicas em campos como **CFOP** e **UF**.

### Principais Funcionalidades
- **Upload de arquivos** (único ou lote) com interface drag‑and‑drop.
- **Pré‑visualização** das primeiras linhas do XML antes da modificação.
- **Busca e substituição de CFOP**:
  - Busca valores que começam com `5***` e altera para `6***`.
  - Exceção: o valor `6405` é convertido para `5404`.
- **Busca e substituição de UF** (estado) com auto‑correção.
- **Botões de ação** com rótulos claros (`Buscar valor campo CFOP`, `Modificar valores tags CFOPs`).
- **Download do XML modificado**.

## Stack Tecnológica
- **Frontend**: HTML5, CSS (vanilla), JavaScript (ES6) – arquivos em `public/`.
- **Backend**: Node.js + Express (`server.js`).
- **Processamento de XML**: Python script `xml_fixer.py` (executado via child process).
- **Gerenciamento de arquivos**: Multer (upload), Archiver (zip de múltiplos arquivos).
- **Desenvolvimento**: Nodemon para hot‑reload (`npm run dev`).

## Estrutura de Pastas
```
editorxml/
├─ .antigravity/            # Metadados do agente
├─ .gitignore               # Ignora node_modules, .antigravity, etc.
├─ node_modules/            # Dependências npm
├─ package.json / package-lock.json
├─ public/                  # Assets estáticos
│   ├─ index.html           # Página principal
│   ├─ css/style.css        # Estilos (glassy, dark mode, tipografia Inter)
│   └─ js/app.js            # Lógica da UI
├─ server.js                # API Express e rotas de upload
├─ xml_fixer.py             # Script Python que corrige CFOP/UF
├─ test.js                  # Testes unitários (Jest) – ainda a ser expandido
└─ requirements.txt         # Dependências Python
```

## Instalação
```bash
# Clone o repositório
git clone https://github.com/anderson561/editorxml.git
cd editorxml

# Instale dependências Node
npm install

# Instale dependências Python (virtual env recomendado)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Executando a aplicação
```bash
# Inicie o servidor Node (modo desenvolvimento)
npm run dev
# Abra http://localhost:3000 no navegador
```

## Como funciona a modificação de CFOP
1. O frontend envia o XML ao backend (`/upload`).
2. `server.js` chama `xml_fixer.py` com o argumento `--cfop-fix`.
3. O script Python procura por tags `<CFOP>` usando a expressão regular:
   ```python
   pattern = r"(<CFOP\\b[^>]*>)(.*?)(</CFOP>)"
   ```
4. Para cada ocorrência:
   - Se o conteúdo for `6405`, substitui por `5404`.
   - Se iniciar com `5` (ex.: `5405`), troca o primeiro dígito por `6` (ex.: `5405` → `6405`).
5. O XML corrigido é devolvido ao cliente para download.

## Como funciona a modificação de UF
- Similar ao CFOP, mas busca a tag `<UF>` e substitui o valor encontrado pelo novo valor informado.

## Testes
- O repositório contém um diretório `testsprite_tests/` (ainda não utilizado).
- Testes unitários podem ser executados via:
```bash
npm test
```
- Futuras implementações incluirão testes de integração para o fluxo completo de upload → correção → download.

## Contribuição
1. Fork o projeto.
2. Crie uma branch (`git checkout -b feature/xyz`).
3. Commit suas mudanças (`git commit -m "Add xyz"`).
4. Abra um Pull Request.

## Licença
Este projeto está licenciado sob a **MIT License**.
