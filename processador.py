class Processador:
    def __init__(self):
        # Registradores de uso geral
        regs = {}
        for x in range(32):
            regs.append(f'r{x}')
        self.registradores = regs

        # Registradores de estado/uso específico
        self.pc = 0
        self.rsp = 0
        self.ra = 0
        self.of = 0
    
    def __str__(self):
        valor_reg = ''.join([f'{nome}: {valor}' for nome, valor in self.registradores.items()])
        return (f'PC: {self.pc}\n'
                f'RSP: {self.rsp}\n'
                f'RA: {self.ra}\n'
                f'OF: {self.of}\n'
                f'Registers: {valor_reg}')

    def definir_valor_reg(self, nome_reg, valor_reg):
        if nome_reg in self.registradores:
            self.registradores[nome_reg] = valor_reg
        else:
            raise ValueError(f"O registrador '{nome_reg}' não existe.")
    
    def acessar_reg(self, nome_reg):
        if nome_reg in self.registradores:
            return self.registradores[nome_reg]
        else:
            raise ValueError(f"O registrador '{nome_reg}' não existe.")