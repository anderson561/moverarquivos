import os
import unittest
from unittest.mock import patch, MagicMock
import sys

# Adiciona o diretório src ao path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from organizer import FileOrganizer
from strategies import BaseStrategy

class DummyStrategy(BaseStrategy):
    def get_destination_subpath(self, file_path: str):
        if file_path.endswith('.txt'):
            return "TEXT_FILES"
        return None

class TestFileOrganizer(unittest.TestCase):

    @patch('os.path.exists')
    def test_organize_path_not_found(self, mock_exists):
        # Configura exists para retornar False
        mock_exists.return_value = False
        
        organizer = FileOrganizer(dry_run=True)
        # Limita os caminhos testados para simplificar
        organizer.paths_and_strategies = {"C:\\dummy_path": DummyStrategy()}
        
        with patch('organizer.logger') as mock_logger:
            organizer.organize()
            mock_logger.warning.assert_any_call("Caminho não encontrado: C:\\dummy_path")

    @patch('os.path.exists')
    @patch('os.listdir')
    @patch('os.path.isfile')
    def test_organize_dry_run(self, mock_isfile, mock_listdir, mock_exists):
        mock_exists.return_value = True
        mock_listdir.return_value = ["file1.txt", "file2.jpg"]
        
        # isfile retorna True para os caminhos construídos
        mock_isfile.side_effect = lambda path: True

        organizer = FileOrganizer(dry_run=True)
        organizer.paths_and_strategies = {"C:\\dummy_path": DummyStrategy()}

        with patch('organizer.logger') as mock_logger:
            organizer.organize()
            # Deve indicar dry run para o arquivo .txt
            mock_logger.info.assert_any_call("[DRY RUN] Moveria: C:\\dummy_path\\file1.txt -> C:\\dummy_path\\TEXT_FILES\\file1.txt")
            # file2.jpg não deve ser movido pois get_destination_subpath retorna None

    @patch('os.path.exists')
    @patch('os.listdir')
    @patch('os.path.isfile')
    @patch('os.makedirs')
    @patch('shutil.move')
    def test_organize_real_move(self, mock_move, mock_makedirs, mock_isfile, mock_listdir, mock_exists):
        # mock_exists retorna True para o diretório raiz, mas False para o destino do arquivo
        def exists_side_effect(path):
            if path == "C:\\dummy_path":
                return True
            return False
        
        def isfile_side_effect(path):
            if path == "C:\\dummy_path\\file1.txt":
                return True
            return False
        
        mock_exists.side_effect = exists_side_effect
        mock_listdir.return_value = ["file1.txt"]
        mock_isfile.side_effect = isfile_side_effect

        organizer = FileOrganizer(dry_run=False)
        organizer.paths_and_strategies = {"C:\\dummy_path": DummyStrategy()}

        organizer.organize()
        
        mock_makedirs.assert_called_once_with("C:\\dummy_path\\TEXT_FILES", exist_ok=True)
        mock_move.assert_called_once_with("C:\\dummy_path\\file1.txt", "C:\\dummy_path\\TEXT_FILES\\file1.txt")

    @patch('os.path.exists')
    @patch('os.listdir')
    @patch('os.path.isfile')
    @patch('os.makedirs')
    @patch('os.path.getmtime')
    @patch('shutil.move')
    def test_organize_real_move_with_duplicate(self, mock_move, mock_getmtime, mock_makedirs, mock_isfile, mock_listdir, mock_exists):
        # Ambos existem (raiz e arquivo de destino já existente)
        def exists_side_effect(path):
            if path in ("C:\\dummy_path", "C:\\dummy_path\\TEXT_FILES\\file1.txt"):
                return True
            return False
            
        def isfile_side_effect(path):
            if path in ("C:\\dummy_path\\file1.txt", "C:\\dummy_path\\TEXT_FILES\\file1.txt"):
                return True
            return False

        mock_exists.side_effect = exists_side_effect
        mock_listdir.return_value = ["file1.txt"]
        mock_isfile.side_effect = isfile_side_effect
        mock_getmtime.return_value = 123456789

        organizer = FileOrganizer(dry_run=False)
        organizer.paths_and_strategies = {"C:\\dummy_path": DummyStrategy()}

        organizer.organize()
        
        # Como o destino já existe, deve renomear usando o mtime
        expected_dest = "C:\\dummy_path\\TEXT_FILES\\file1_123456789.txt"
        mock_move.assert_called_once_with("C:\\dummy_path\\file1.txt", expected_dest)

    @patch('os.path.exists')
    @patch('os.listdir')
    @patch('os.path.isfile')
    @patch('os.makedirs')
    @patch('os.rename')
    @patch('shutil.move')
    def test_organize_conflict_resolution(self, mock_move, mock_rename, mock_makedirs, mock_isfile, mock_listdir, mock_exists):
        # Para simular o conflito de arquivo bloqueando pasta:
        # Quando verificar se o diretório acumulado existe e é arquivo, retornamos True para a pasta intermediária
        # C:\dummy_path\TEXT_FILES -> TEXT_FILES é a pasta a ser criada.
        # Se TEXT_FILES já existir como arquivo, os.path.exists("C:\dummy_path\TEXT_FILES") é True e os.path.isfile("C:\dummy_path\TEXT_FILES") é True.
        
        def exists_side_effect(path):
            if path == "C:\\dummy_path":
                return True
            if path == "C:\\dummy_path\\TEXT_FILES":
                return True # Diz que existe
            return False
            
        def isfile_side_effect(path):
            if path == "C:\\dummy_path\\file1.txt":
                return True
            if path == "C:\\dummy_path\\TEXT_FILES":
                return True # É um arquivo!
            return False

        mock_exists.side_effect = exists_side_effect
        mock_listdir.return_value = ["file1.txt"]
        mock_isfile.side_effect = isfile_side_effect

        organizer = FileOrganizer(dry_run=False)
        organizer.paths_and_strategies = {"C:\\dummy_path": DummyStrategy()}

        organizer.organize()

        # Deve ter renomeado a pasta/arquivo conflitante
        mock_rename.assert_called_once_with("C:\\dummy_path\\TEXT_FILES", "C:\\dummy_path\\TEXT_FILES_CONFLITO_F_P")
        # E depois prosseguido com a criação e movimentação
        mock_makedirs.assert_called_once_with("C:\\dummy_path\\TEXT_FILES", exist_ok=True)
        mock_move.assert_called_once_with("C:\\dummy_path\\file1.txt", "C:\\dummy_path\\TEXT_FILES\\file1.txt")

    def test_custom_base_path(self):
        custom_path = r"C:\custom_test_dir"
        organizer = FileOrganizer(base_path=custom_path, dry_run=True)
        self.assertEqual(organizer.base_path, os.path.abspath(custom_path))
        
        # Verify the key paths are built relative to custom_path
        expected_keys = {
            os.path.join(organizer.base_path, "Impostos"),
            os.path.join(organizer.base_path, "Notas"),
            organizer.base_path
        }
        self.assertEqual(set(organizer.paths_and_strategies.keys()), expected_keys)

if __name__ == '__main__':
    unittest.main()
