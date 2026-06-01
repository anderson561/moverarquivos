import os
import shutil
import logging
from typing import Dict
from tenacity import retry, stop_after_attempt, wait_exponential
from strategies import BaseStrategy, TypeStrategy, ImpostoStrategy, CompanyNameStrategy

# Configuração de Logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FileOrganizer:
    def __init__(self, base_path: str = r"C:\Users\ANDERSON\Desktop", dry_run: bool = True):
        self.dry_run = dry_run
        self.base_path = os.path.abspath(base_path)
        self.paths_and_strategies: Dict[str, BaseStrategy] = {
            os.path.join(self.base_path, "Impostos"): ImpostoStrategy(),
            os.path.join(self.base_path, "Notas"): CompanyNameStrategy(),
            self.base_path: TypeStrategy(),
        }

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def _move_file(self, source: str, destination: str):
        # Garantir caminhos absolutos e lidar com caminhos longos no Windows (prefixo \\?\)
        abs_source = os.path.abspath(source)
        abs_dest = os.path.abspath(destination)
        
        if self.dry_run:
            logger.info(f"[DRY RUN] Moveria: {abs_source} -> {abs_dest}")
            return

        dest_dir = os.path.dirname(abs_dest)
        
        # Validação de conflitos (Arquivo bloqueando pasta)
        path_acc = ""
        # Divide o caminho para verificar cada componente
        # No Windows, removemos o drive para iterar nas pastas
        drive, path_parts = os.path.splitdrive(dest_dir)
        path_acc = drive + os.sep
        for part in path_parts.strip(os.sep).split(os.sep):
            path_acc = os.path.join(path_acc, part)
            if os.path.exists(path_acc) and os.path.isfile(path_acc):
                # Conflito fatal: Existe um arquivo onde deveria ser uma pasta
                new_path_acc = path_acc + "_CONFLITO_F_P"
                logger.warning(f"CONFLITO DETECTADO: O arquivo '{path_acc}' impede a criacao da pasta. Renomeando arquivo para prosseguir.")
                os.rename(path_acc, new_path_acc)

        try:
            os.makedirs(dest_dir, exist_ok=True)
            
            # Evita sobrescrever se o arquivo já existir no destino
            if os.path.exists(abs_dest):
                base, ext = os.path.splitext(abs_dest)
                abs_dest = f"{base}_{int(os.path.getmtime(abs_source))}{ext}"

            shutil.move(abs_source, abs_dest)
            logger.info(f"MOVIDO: {os.path.basename(abs_source)} -> {abs_dest}")
        except Exception as e:
            logger.error(f"FALHA AO MOVER '{os.path.basename(abs_source)}': {str(e)}")
            raise # Relança para o retry se necessário

    def organize(self):
        logger.info(f"Iniciando organização no diretório: {self.base_path} (Modo Simulação: {self.dry_run})")
        
        for root_path, strategy in self.paths_and_strategies.items():
            if not os.path.exists(root_path):
                logger.warning(f"Caminho não encontrado: {root_path}")
                continue

            logger.info(f"Processando diretório: {root_path}")
            
            # Lista apenas os arquivos no diretório atual (não recursivo para o Desktop geral)
            for item in os.listdir(root_path):
                source_path = os.path.join(root_path, item)
                
                if os.path.isfile(source_path):
                    sub_path = strategy.get_destination_subpath(source_path)
                    
                    if sub_path:
                        dest_path = os.path.join(root_path, sub_path, item)
                        
                        # Evita mover para dentro de si mesmo se já estiver na pasta certa
                        if os.path.abspath(source_path) == os.path.abspath(dest_path):
                            continue
                            
                        try:
                            self._move_file(source_path, dest_path)
                        except Exception as e:
                            logger.error(f"Erro ao mover {item}: {e}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Organizador Avançado de Arquivos")
    parser.add_argument("--path", type=str, default=r"C:\Users\ANDERSON\Desktop", help="Caminho da pasta a ser organizada")
    parser.add_argument("--real", action="store_true", help="Executa a movimentação real dos arquivos (caso contrário, apenas simula)")
    args = parser.parse_args()
    
    organizer = FileOrganizer(base_path=args.path, dry_run=not args.real)
    organizer.organize()
