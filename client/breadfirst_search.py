import client
import random
import nodes
import stack
import ast

class Agent:
    def __init__(self):
        self.c = client.Client('127.0.0.1', 50000)
        self.res = self.c.connect()
        random.seed()  # To become true random, a different seed is used! (clock time)
        self.visited_nodes = []
        self.frontier_nodes = stack.Stack()
        self.weight_map =[]
        self.weight_dict = {}
        self.goal_pos =(0,0)
        self.state = (0,0)
        self.max_coord = (0,0)
        self.obstacles = []

    def get_goal_position(self):
        """
        Get the goal position
        """
        msg = self.c.execute("info", "goal")
        goal = ast.literal_eval(msg)
        # test
        # print('Goal is located at:', goal)
        return goal

    def get_self_position(self):
        """
        Get the agent position
        """
        msg = self.c.execute("info", "position")
        pos = ast.literal_eval(msg)
        # Test
        print('Received agent\'s position:', pos)
        return pos

    def get_weight_dict(self):
        """Get weights and add them to a dictionary"""
        msg = self.c.execute("info", "map")
        w_map = ast.literal_eval(msg)
        w_dict = {}
        for elem in w_map:
            w_dict[elem[0]]=elem[1]
        # Test
        #print(w_dict)
        return w_dict

    def get_max_coord(self):
        """
        Get max coordinates
        """
        msg = self.c.execute("info","maxcoord")
        max_coord =ast.literal_eval(msg)
        # Test
        #print('Received maxcoord', max_coord)
        return max_coord

    def get_obstacles(self):
        """
        Return the obstacles
        """
        msg = self.c.execute("info","obstacles")
        obst =ast.literal_eval(msg)
        # Test
        #print('Received map of obstacles:', obst)
        return obst

    def step(self,pos,action):
        """
        Add new position after an action, using north, east, west or south.
        Test the frontiers in the world and adjust the values to zero or max_coord
        """
        if action == "east":
            if pos[0] + 1 < self.max_coord[0]:
                new_pos = (pos[0] + 1, pos[1])
            else:
                new_pos =(0,pos[1])

        if action == "west":
            if pos[0] - 1 >= 0:
                new_pos = (pos[0] - 1, pos[1])
            else:
                new_pos = (self.max_coord[0] - 1, pos[1])

        if action == "south":
            if pos[1] + 1 < self.max_coord[1]:
                new_pos = (pos[0], pos[1] + 1 )
            else:
                new_pos = (pos[0], 0)

        if action == "north":
            if pos[1] - 1 >= 0:
                new_pos = (pos[0], pos[1] - 1)
            else:
                new_pos = (pos[0], self.max_coord[1] - 1 )

        return new_pos

    def mark(self, pos:tuple, colour:str):
        """
        Paint the board with colour
        """
        mark_ground = str(pos[0])+","+str(pos[1])+"_"+colour
        msg = self.c.execute("mark",mark_ground)
        obst =ast.literal_eval(msg)

    def unmark(self,pos:tuple):
        """
        Unmark (remove painting in pos)
        """
        unmark_ground = str(pos[0])+","+str(pos[1])
        msg = self.c.execute("unmark",unmark_ground)
        obst =ast.literal_eval(msg)


    def create_node(self,parent_node,action):
        """
        Create a new node based on the action and on the parent_node
        """
        state = self.step(parent_node.get_state(),action)
        return nodes.Node(state, parent_node, action, self.weight_dict[state])

    def print_nodes(self,description,nds: list):
        print(description)
        print("Name(Parent):Total cost")
        for nd in nds:
            if nd.get_parent() != None:
                print(nd.get_state(),"(",nd.get_parent().get_state(),"):",nd.get_total_cost())
            else:
                print(nd.get_state(),"(---):",nd.get_total_cost())
        print("---------------------------")

    def in_visited_nodes(self, nd:nodes.Node):
        visited = False
        for vn in self.visited_nodes:
            if vn.get_state() == nd.get_state():
                visited = True
                break
        # Test
        #print("Node ",nd.get_state()," is in a visited state? ", visited)
        return visited

    def state_has_obstacle(self, nd:nodes.Node):
        obstacle = False
        for obst in self.obstacles:
            if nd.get_state() == obst:
                obstacle = True
                break
        # Test
        #print("Node ",nd.get_state()," is in an obstacle? ", obstacle)

        return obstacle
    def print_path(self, final_node):
        input("The path (to implement)")
    def run(self):
        # Goal's position...
        self.goal_pos = self.get_goal_position()
        # Test
        print("Goal node:",self.goal_pos)
        # Get weights for each step in the world ...
        self.weight_dict = self.get_weight_dict()
        # Test
        print("weights dict:",self.weight_dict)
        # Get obstacles' positions
        self.obstacles = self.get_obstacles()
        # Test
        print("obstacles:", self.obstacles)
        # Get maximum value for coordinates
        self.max_coord = self.get_max_coord()
        # Get the initial position of the agent
        self.state = self.get_self_position()
        # Start thinking
        end = False
        found = None
        # Add first node (root)
        root = nodes.Node(self.state,None,"",0)
        self.frontier_nodes.push(root)

        nd = self.frontier_nodes.pop()
        self.visited_nodes.append(nd)
        # Get the first four nodes.
        for action in ["east","south","west","north"]:
            nd = self.create_node(root,action)
            if not self.in_visited_nodes(nd) and not self.state_has_obstacle(nd):
                self.frontier_nodes.push(nd)
                self.mark(nd.get_state(),"red")
        self.frontier_nodes.print_stack("After first possible actions")


        input()
        # Cycle expanding nodes following the sequence in frontier nodes.
        while end == False:
            # Expanding strategy
            node_to_expand = self.frontier_nodes.pop()
            self.unmark(node_to_expand.get_state())
            self.state = node_to_expand.get_state()
            # Test
            print("Expanding node position:", self.state)
            self.visited_nodes.append(node_to_expand)
            self.mark(node_to_expand.get_state(),"blue")
            for act in ["east","west","south","north"]:
                nd = self.create_node(node_to_expand,act)
                if not self.in_visited_nodes(nd) and not self.state_has_obstacle(nd):
                    self.frontier_nodes.push(nd)
                    self.mark(nd.get_state(),"red")
            # test
            self.print_nodes("Frontier", self.frontier_nodes.get_list())
            self.print_nodes("Visitied", self.visited_nodes)
            for node in self.visited_nodes:
                if node.get_state() == self.goal_pos:
                    print("Node state:",node.get_state())
                    print("GoalNodePos",self.goal_pos)
                    found = node
                    self.print_path(found)
                    end = True
                    break
            input()
        input("Waiting for return!")


# Starting the program...
def main():
    agent = Agent()
    agent.run()

main()

