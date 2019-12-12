from intcomputer import intcomputer 

class amplifier():
    def __init__(self, phase_setting, program):
        self.comp_input = [phase_setting]
        self.computer = intcomputer(program, self.comp_input)
    
    def run(self, comp_input):
        self.comp_input.append(comp_input)
        return self.computer.run()
