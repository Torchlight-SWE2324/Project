import os

class VerificaFileCaricato:
    def verifica_formato(self, percorso_file:str) -> bool:
        if (percorso_file.endswith('.json')):
            return True
        return False

    def verifica_dimensione(self, percorso_file:str) -> bool:
        file_stats = os.stat('database/' + percorso_file)
        if (file_stats.st_size / (1024 * 1024) < 200):
            return True
        return False