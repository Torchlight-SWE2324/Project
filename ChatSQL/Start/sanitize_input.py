import re

class SanificaInputInserito:
    def sanitize_input(self, input:str) -> str:
        return re.sub(r"['']", " ", input)
