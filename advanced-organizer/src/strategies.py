import os
import re
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, Dict
from pdfminer.high_level import extract_text

def sanitize_path_component(name: str) -> str:
    """Remove caracteres inválidos para nomes de pastas no Windows."""
    # Remove: \ / : * ? " < > |
    sanitized = re.sub(r'[\\/:*?"<>|]', '', name)
    # Remove espaços extras e quebras de linha
    sanitized = sanitized.replace('\n', ' ').strip()
    # Limita o tamanho para evitar caminhos muito longos
    return sanitized[:60]

class BaseStrategy(ABC):
    @abstractmethod
    def get_destination_subpath(self, file_path: str) -> Optional[str]:
        pass

class TypeStrategy(BaseStrategy):
    """Organiza puramente por extensão de arquivo."""
    def get_destination_subpath(self, file_path: str) -> Optional[str]:
        ext = os.path.splitext(file_path)[1].lower().strip('.')
        if not ext:
            return "Outros"
        return sanitize_path_component(ext.upper())

class ImpostoStrategy(BaseStrategy):
    """Organiza Impostos lendo o conteúdo do PDF."""
    KEYWORDS = {
        "DARF": "DARF",
        "DAS": "DAS - Simples Nacional",
        "IPTU": "IPTU",
        "IPVA": "IPVA",
        "GRERJ": "GRERJ",
    }

    def get_destination_subpath(self, file_path: str) -> Optional[str]:
        if not file_path.lower().endswith('.pdf'):
            return TypeStrategy().get_destination_subpath(file_path)
        
        try:
            text = extract_text(file_path).upper()
            for key, folder in self.KEYWORDS.items():
                if key in text:
                    return folder
            return "Impostos Gerais"
        except Exception:
            return "Impostos - Erro na Leitura"

class CompanyNameStrategy(BaseStrategy):
    """Extrai Ano / Mês / Empresa de Notas Fiscais."""
    
    MONTHS = {
        1: "01 - Janeiro", 2: "02 - Fevereiro", 3: "03 - Março", 
        4: "04 - Abril", 5: "05 - Maio", 6: "06 - Junho",
        7: "07 - Julho", 8: "08 - Agosto", 9: "09 - Setembro", 
        10: "10 - Outubro", 11: "11 - Novembro", 12: "12 - Dezembro"
    }

    def get_destination_subpath(self, file_path: str) -> Optional[str]:
        if not file_path.lower().endswith('.pdf'):
            return TypeStrategy().get_destination_subpath(file_path)

        try:
            text = extract_text(file_path)
            
            # Tenta encontrar data (ex: 11/03/2026)
            date_match = re.search(r'(\d{2})/(\d{2})/(\d{4})', text)
            if date_match:
                day, month, year = map(int, date_match.groups())
            else:
                year, month = datetime.now().year, datetime.now().month

            # Lógica para Razão Social
            company = "Desconhecido"
            lines = [l.strip() for l in text.split('\n') if l.strip()]
            for i, line in enumerate(lines):
                upper_line = line.upper()
                if "RAZÃO SOCIAL" in upper_line or "EMITENTE" in upper_line or "NOME/RAZÃO SOCIAL" in upper_line:
                    # Tenta pegar após o sinal de dois pontos na mesma linha
                    if ":" in line:
                        potential = line.split(':')[-1].strip()
                        if len(potential) > 3:
                            company = potential
                            break
                    # Se não achou na linha, tenta a próxima
                    if i + 1 < len(lines):
                        company = lines[i+1].strip()
                        break
            
            if company == "Desconhecido" and len(lines) > 0:
                company = lines[0].strip()

            month_str = self.MONTHS.get(month, f"{month:02d}")
            
            # Sanitiza cada componente do caminho
            safe_year = sanitize_path_component(str(year))
            safe_month = sanitize_path_component(month_str)
            safe_company = sanitize_path_component(company)
            
            return os.path.join(safe_year, safe_month, safe_company)
            
        except Exception:
            return "Notas - Erro na Leitura"
