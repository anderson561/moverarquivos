import os
import unittest
from unittest.mock import patch
import sys

# Adiciona o diretório src ao path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from strategies import sanitize_path_component, TypeStrategy, ImpostoStrategy, CompanyNameStrategy

class TestStrategies(unittest.TestCase):

    def test_sanitize_path_component(self):
        self.assertEqual(sanitize_path_component("Pasta: Teste/123?"), "Pasta Teste123")
        self.assertEqual(sanitize_path_component("Nome\nCom\nQuebra"), "Nome Com Quebra")
        self.assertEqual(sanitize_path_component("a" * 100), "a" * 60)

    def test_type_strategy(self):
        strategy = TypeStrategy()
        self.assertEqual(strategy.get_destination_subpath("document.pdf"), "PDF")
        self.assertEqual(strategy.get_destination_subpath("IMAGE.PNG"), "PNG")
        self.assertEqual(strategy.get_destination_subpath(".gitignore"), "Outros")
        self.assertEqual(strategy.get_destination_subpath("no_extension"), "Outros")

    @patch('strategies.extract_text')
    def test_imposto_strategy(self, mock_extract):
        strategy = ImpostoStrategy()
        
        # Test non-PDF fallback
        self.assertEqual(strategy.get_destination_subpath("receipt.txt"), "TXT")

        # Test DARF
        mock_extract.return_value = "Este é um documento DARF de exemplo"
        self.assertEqual(strategy.get_destination_subpath("imposto.pdf"), "DARF")

        # Test DAS
        mock_extract.return_value = "Guia do DAS do Simples Nacional"
        self.assertEqual(strategy.get_destination_subpath("imposto.pdf"), "DAS - Simples Nacional")

        # Test IPTU
        mock_extract.return_value = "Carnê de IPTU 2026"
        self.assertEqual(strategy.get_destination_subpath("imposto.pdf"), "IPTU")

        # Test General Taxes
        mock_extract.return_value = "Outro tipo de taxa qualquer"
        self.assertEqual(strategy.get_destination_subpath("imposto.pdf"), "Impostos Gerais")

        # Test Exception handling
        mock_extract.side_effect = Exception("Erro ao ler PDF")
        self.assertEqual(strategy.get_destination_subpath("imposto.pdf"), "Impostos - Erro na Leitura")

    @patch('strategies.extract_text')
    def test_company_name_strategy(self, mock_extract):
        strategy = CompanyNameStrategy()

        # Test non-PDF fallback
        self.assertEqual(strategy.get_destination_subpath("nota.xml"), "XML")

        # Test PDF with date and Razão Social on same line
        mock_extract.return_value = "Emissão: 15/04/2026\nRazão Social: Empresa Teste LTDA\nValor: R$ 100,00"
        subpath = strategy.get_destination_subpath("nota.pdf")
        self.assertEqual(subpath, os.path.join("2026", "04 - Abril", "Empresa Teste LTDA"))

        # Test PDF with Emitente on next line
        mock_extract.return_value = "Data: 20/12/2025\nEmitente\nMinha Empresa S/A\nCNPJ: 00.000.000/0001-00"
        subpath = strategy.get_destination_subpath("nota.pdf")
        self.assertEqual(subpath, os.path.join("2025", "12 - Dezembro", "Minha Empresa SA"))

        # Test PDF without date (defaults to current year/month)
        mock_extract.return_value = "Nome/Razão Social: Outra Empresa\nOutras informações"
        subpath = strategy.get_destination_subpath("nota.pdf")
        from datetime import datetime
        current_year = str(datetime.now().year)
        current_month_str = CompanyNameStrategy.MONTHS[datetime.now().month]
        self.assertEqual(subpath, os.path.join(current_year, current_month_str, "Outra Empresa"))

        # Test PDF with no recognizable company (falls back to first line)
        mock_extract.return_value = "Primeira Linha da Nota\nOutra linha\nMais dados"
        subpath = strategy.get_destination_subpath("nota.pdf")
        self.assertEqual(subpath, os.path.join(current_year, current_month_str, "Primeira Linha da Nota"))

        # Test Exception handling
        mock_extract.side_effect = Exception("Erro ao ler PDF")
        self.assertEqual(strategy.get_destination_subpath("nota.pdf"), "Notas - Erro na Leitura")

if __name__ == '__main__':
    unittest.main()
