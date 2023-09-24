import client
import ast
import random

#FSM STATES
INICIO = 0
PESQUISA  = 1
VIRA_ESQ = 2
VIRA_DIR = 3
PARA = 4
VAI_FRENTE = 5

class FiniteState_Agent:
    def __init__(self,address,port):
        self.state = INICIO
        self.c = client.Client(address, port)
        self.c.connect()
        random.seed()  # To become true random, a different seed is used! (clock time)
        self.position = None
        self.goal = None
        self.direction = None
        self.objects = []
        self.end = False

    def inicio_exe(self):
        print("INÍCIO INÍCIO INÍCIO")
        msg = self.c.execute("info", "goal")
        self.goal = ast.literal_eval(msg)

    def inicio_exit(self):
        self.state = PESQUISA

    def pesquisa_exe(self):
        print("PESQUISA PESQUISA PESQUISA")
        msg = self.c.execute("info", "position")
        self.position = ast.literal_eval(msg)
        self.direction = self.c.execute("info", "direction")


    def pesquisa_exit(self):
        dx, dy = self.goal[0] - self.position[0], self.goal[1] - self.position[1]
        # Test
        print(dx,dy,self.direction)

        if dx>0 and dy>0:
            if self.direction == "south" or self.direction == "east":
                    self.state = VAI_FRENTE
            else:
                self.state = VIRA_DIR if self.direction == "north" else VIRA_ESQ

        elif dx<0 and dy>0:
            if self.direction == "south" or self.direction == "west":
                    self.state = VAI_FRENTE
            else:
                self.state = VIRA_DIR if self.direction == "east" else VIRA_ESQ

        elif dx<0 and dy<0:
            if self.direction == "north" or self.direction == "east":
                    self.state = VAI_FRENTE
            else:
                self.state = VIRA_DIR if self.direction == "west" else VIRA_ESQ

        elif dx>0 and dy<0:
            if self.direction == "north" or self.direction == "west":
                    self.state = VAI_FRENTE
            else:
                self.state = VIRA_DIR if self.direction == "south" else VIRA_ESQ

        elif dx == 0:
            if dy < 0:
                if self.direction == "north":
                    self.state = VAI_FRENTE
                else:
                    self.state = VIRA_DIR
            else:
                if self.direction == "south":
                    self.state = VAI_FRENTE
                else:
                    self.state = VIRA_ESQ

        elif dy == 0:
            if dx < 0:
                if self.direction == "west":
                    self.state = VAI_FRENTE
                else:
                    self.state = VIRA_DIR
            else:
                if self.direction == "east":
                    self.state = VAI_FRENTE
                else:
                    self.state = VIRA_ESQ

        else:
            self.state = VIRA_DIR

    def virar_esq_exe(self):
        print("VIRA_ESQ VIRA_ESQ VIRA_ESQ")
        self.c.execute("command","left")

    def virar_esq_exit(self):
        msg = self.c.execute("info", "view")
        print(msg)
        self.objects = ast.literal_eval(msg)
        if 'obstacle' not in self.objects and 'bomb' not in self.objects:
            self.state = PESQUISA
        else:
            self.state = VIRA_ESQ

    def virar_dir_exe(self):
        print("VIRA_DIR VIRA_DIR VIRA_DIR")
        self.c.execute("command" , "right")


    def virar_dir_exit(self):
        msg = self.c.execute("info", "view")
        self.objects = ast.literal_eval(msg)
        if 'obstacle' not in self.objects and 'bomb' not in self.objects:
            self.state = PESQUISA
        else:
            self.state = VIRA_ESQ


    def para_exe(self):
        print("Atingi o objetivo!")


    def para_exit(self):
        self.end = True

    def vai_frente_exit(self):
        msg = self.c.execute("info", "position")
        self.position = ast.literal_eval(msg)
        if "obstacle" in self.objects:
            self.state = VIRA_DIR
        elif self.position == self.goal:
            self.state = PARA
        else:
            self.state = PESQUISA

    def vai_frente_exe(self):

        self.c.execute("command", "forward")


    def run(self):
        while self.end == False:
            # Get information from world
            msg = self.c.execute("info","view")
            self.objects = ast.literal_eval(msg)
            if self.state == INICIO:
                self.inicio_exe()
                self.inicio_exit()
            if self.state == PESQUISA:
                self.pesquisa_exe()
                self.pesquisa_exit()
            elif self.state == VIRA_ESQ:
                self.virar_esq_exe()
                self.virar_esq_exit()

            elif self.state == VIRA_DIR:
                self.virar_dir_exe()
                self.virar_dir_exit()

            elif self.state == PARA:
                self.para_exe()
                self.para_exit()

            elif self.state == VAI_FRENTE:
                self.vai_frente_exe()
                self.vai_frente_exit()

def main():
    fsm_agent = FiniteState_Agent('127.0.0.1', 50000)
    fsm_agent.run()


main()
