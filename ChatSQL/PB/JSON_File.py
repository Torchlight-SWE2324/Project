import os
import FileService

class JSON_File(FileService):
    def verificaDimensioni(percorsoFile:str) -> bool:
        file_stats = os.stat(percorsoFile)
        if (file_stats.st_size / (1024 * 1024) < 200):
            return True
        return False

    def verificaFormato(percorsoFile:str) -> bool:
        if (percorsoFile.endswith('.json')):
            return True
        return False