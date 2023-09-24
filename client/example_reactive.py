import client
import ast
import random

# ---------------------------------------------------------------------
def move_to(dir, new_dir):
    """Converts the movement to north, east, south and west to
    movements forward, left and right. It is useful when implementing
    the search algorithms"""
    if dir == "north":
        dir_nb = 0;
    elif dir == "east":
        dir_nb = 1;
    elif dir == "south":
        dir_nb = 2;
    else:
        dir_nb = 3;

    if new_dir == "north":
        n_dir_nb = 0;
    elif new_dir == "east":
        n_dir_nb = 1;
    elif new_dir == "south":
        n_dir_nb = 2;
    else:
        n_dir_nb = 3;
    calc = dir_nb - n_dir_nb
    if ( calc == 0):
        return [["command","forward"]]
    if (calc == 1):
        return [["command", "left"],["command", "forward"]]
    if (calc == 2):
        return [["command","left"],["command","left"],["command","forward"]]
    if (calc == 3):
        return [["command","right"],["command","forward"]]
    if (calc == -1):
        return [["command","right"],["command","forward"]]
    if (calc == -2):
        return [["command","right"],["command","right"],["command","forward"]]
    if (calc == -3):
        return [["command","left"],["command","forward"]]

def example_move_to(agent):
    dir = agent.execute("info","direction")
    commands = move_to(dir,"north")
    for c in commands:
        agent.execute(c[0],c[1])
    input("Press key")
    dir = agent.execute("info","direction")
    commands = move_to(dir,"west")
    for c in commands:
        agent.execute(c[0],c[1])
    input("Press key")
    dir = agent.execute("info","direction")
    commands = move_to(dir,"west")
    for c in commands:
        agent.execute(c[0],c[1])
    input("Press key")
    dir = agent.execute("info","direction")
    commands = move_to(dir,"east")
    for c in commands:
        agent.execute(c[0],c[1])
    input("Press key")
    dir = agent.execute("info","direction")
    commands = move_to(dir,"south")
    for c in commands:
        agent.execute(c[0],c[1])
    input("Press key")
# ---------------------------------------------------------------------



def reactive_example_1(agent):
    end = False
    while end == False:
        msg = agent.execute("info", "view")
        objects = ast.literal_eval(msg)
        if objects[0] == 'goal':
            agent.execute("command","north")
            end = True
            print("Found Goal!")
        elif objects[0] == 'obstacle':
            res = random.randint(0,4)
            if res <= 2:
                agent.execute("command", "east")
            else:
                agent.execute("command","west")
        else:
            agent.execute("command","north")
    input("Press key to exit!")

def reactive_example_2(agent):
    end = False
    msg = agent.execute("command", "set_steps")
    while end == False:
        msg = agent.execute("info","view")
        print("Message:",msg)
        objects = ast.literal_eval(msg)
        if 'obstacle' in objects or 'bomb' in objects:
            agent.execute("command","left")
        else:
            if 'goal' in objects:
                end = True
                print("Found Goal!\n")
            else:
              res = random.randint(0,4)
              if res <= 3:
                  agent.execute("command", "forward")
              else:
                  agent.execute("command","right")
        input("Press key to exit!")

def main():
    agent = client.Client('127.0.0.1', 50000)
    agent.connect()
    random.seed()  # To become true random, a different seed is used! (clock time)

    #reactive_example_1(agent)
    #reactive_example_2(agent)
    #example_move_to(agent)

main()
