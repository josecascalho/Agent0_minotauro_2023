import tkinter as tk
import game_object as go
import sys


# ------------------------------------------------------------
# CLASS GAMEBOARD:
# ------------------------------------------------------------
class GameBoard(tk.Frame):

    def __init__(self, parent, config, columns=16, rows=16, size=64):
        """size is the size of a square, in pixels"""

        self.rows = rows
        self.columns = columns
        self.size = size
        self.config = config
        self.bg_color = self.config["background_color"]
        self.view_color = self.config["view_color"]
        self.step_color = self.config["step_color"]
        self.object_matrix = [[[] for _ in range(self.rows)] for _ in range(self.columns)]
        # Test
        # print("Object_matrix:",self.object_matrix)
        self.parent = parent
        self.rectangles = [[0] * rows for _ in range(columns)]
        tk.Frame.__init__(self, parent, relief = tk.RAISED, borderwidth = 5)
        self.quitButton = tk.Button(self, text='Quit')
        self.quitButton.pack(side="bottom", fill="both", expand=False)
        self.startButton = tk.Button(self, text='Start')
        self.startButton.pack(side="top", fill="both", expand=False)
        canvas_width = columns * size
        canvas_height = rows * size
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0,
                                width=canvas_width, height=canvas_height, background="bisque")
        self.canvas.pack(side="top", fill="both", expand=True, padx=2, pady=2)

        # using bind to update the window
        # this binding will cause a refresh if the user interactively
        # changes the window size
        self.canvas.bind("<Configure>", self.refresh)
        self.startButton.bind("<Button-1>",self.handle_start)
        self.quitButton.bind("<Button-1>",self.handle_quit)

    def handle_start(self,event):
        print("Handling the start!!!")


    def handle_quit(self,event):
        print("Handling the quit!!!")

    def refresh(self, event):
        """Redraw the board, possibly in response to window being resized"""
        x_size = int((event.width - 1) / self.columns)
        y_size = int((event.height - 1) / self.rows)
        self.size = min(x_size, y_size)
        self.canvas.delete("square")
        for row in range(self.rows):
            for col in range(self.columns):
                x1 = (col * self.size)
                y1 = (row * self.size)
                x2 = x1 + self.size
                y2 = y1 + self.size
                previous_color = self.canvas.itemcget(self.rectangles[col][row], "fill")
                self.rectangles[col][row] = self.canvas.create_rectangle(x1,
                                                                         y1,
                                                                         x2,
                                                                         y2,
                                                                         outline="black" if self.bg_color!="black" else "#7b145c",
                                                                         fill= previous_color if previous_color != "" else self.bg_color,
                                                                         tags="square",
                                                                         width=1) # (1 if self.bg_color != "black" else 0))

        for column in self.object_matrix:
            for square in column:
                for game_object in square:
                    self.place(game_object, game_object.get_x(), game_object.get_y())
        self.canvas.tag_raise("piece")
        self.canvas.tag_lower("square")



    def quit(self):
        """ handle button click event and output text from entry area"""
        print('quitting!')  # do here whatever you want
        self.parent.destroy()
        sys.exit()

    def start(self):
        pass

    # ------------------------------------------------
    # GET_MAX_COORD
    # ------------------------------------------------

    def get_max_coord(self):
        """Get the maximum values of the  coordinates from the actual world"""
        # test
        # print("Coordinates:",(self.columns,self.rows))
        return self.columns, self.rows

    # ------------------------------------------------
    # PRINT_STEP:
    # ------------------------------------------------
    def print_step(self, game_object):
        """Set the step of the object, giving the color yellow to the patch"""
        self.canvas.itemconfig(self.rectangles[game_object.get_x()][game_object.get_y()],
                               fill=self.step_color)

    # ------------------------------------------------
    # SET_STEPS_VIEW:
    # ------------------------------------------------
    def set_steps_view(self, game_object):
        game_object.set_steps_view()
        return True

    def reset_steps_view(self, game_object):
        game_object.reset_steps_view()
        self.clean_board()
        return False

    # ------------------------------------------------
    # REMOVE_VIEWSCREEN
    # ------------------------------------------------
    def remove_viewscreen(self, game_object, x, y):
        """Remove the identification on screen (color) of the patches an object sees"""
        if game_object.get_view_type() == "front":
            if self.canvas.itemcget(self.rectangles[x][y], "fill") == self.view_color:
                self.canvas.itemconfig(self.rectangles[x][y], fill=self.bg_color)
        elif game_object.get_view_type() == "around":
            pass

    # ------------------------------------------------
    # SET_VIEWSCREEN:
    # ------------------------------------------------
    def set_viewscreen(self, game_object, x, y):
        """Set the identification on screen (color) of the patches an object sees"""
        if game_object.get_view_type() == "front":
            if self.canvas.itemcget(self.rectangles[x][y], "fill") == self.view_color:
                self.canvas.itemconfig(self.rectangles[x][y], fill=self.bg_color)
            else:
                self.canvas.itemconfig(self.rectangles[x][y], fill=self.view_color)
        elif game_object.get_view_type() == "around":
            pass

    # ------------------------------------------------
    # CLEAN_BOARD:
    # ------------------------------------------------
    def clean_board(self):
        """Clean the board, removing all the colour to the patches"""
        for x in range(self.rows):
            for y in range(self.columns):
                if self.canvas.itemcget(self.rectangles[x][y], "fill") == "yellow":
                    self.canvas.itemconfig(self.rectangles[x][y], fill=self.bg_color)
        return True

    # ------------------------------------------------
    # PLACE:
    # ------------------------------------------------
    def place(self, game_object, x, y):
        """Place object at x y"""

        # Clean before moving
        if game_object.is_eyes_open():
            self.remove_viewscreen(game_object, x, y)
        game_object.set_position(x, y)
        x0 = (x * self.size) + int(self.size / 2)
        y0 = (y * self.size) + int(self.size / 2)
        self.canvas.coords(game_object.get_name(), x0, y0)
        # Print object's view on screen after moving
        if game_object.is_eyes_open():
            new_x, new_y = self.get_place_ahead(game_object)
            self.set_viewscreen(game_object, new_x, new_y)

    # ------------------------------------------------
    # ADD
    # ------------------------------------------------

    def add(self, game_object, x=0, y=0):
        """Add object to the playing board"""
        #print("Adding object",game_object," with image ",game_object.get_image_file()," in position (x,y)= (", x,",", y,")")
        canvas_image = self.canvas.create_image(x, y, image=game_object.get_image(),
                                                tags=(game_object.get_name(), "piece"),
                                                anchor="c")
        game_object.set_canvas_image(canvas_image)
        self.place(game_object, x, y)
        # print(x, y)
        self.object_matrix[x][y].append(game_object)

    # ------------------------------------------------
    # REMOVE:
    # ------------------------------------------------

    def remove(self, game_object):
        self.canvas.delete(game_object.get_name())
        self.object_matrix[game_object.get_x()][game_object.get_y()].remove(game_object)
        del game_object
        # self.moving_refresh()

    # ------------------------------------------------
    # CHANGE POSITION:
    # ------------------------------------------------

    def change_x(self, x):
        if x >= self.columns:
            x = 0
        if x < 0:
            x = self.columns - 1
        return x

    def change_y(self, y):
        if y >= self.rows:
            y = 0
        if y < 0:
            y = self.rows - 1
        return y

    def change_position(self, game_object, x, y):
        if game_object.get_steps_view():
            # print("Player was at: ", game_object.get_x(), game_object.get_y())
            self.print_step(game_object)
        x = self.change_x(x)
        y = self.change_y(y)
        self.place(game_object, x, y)
        return x, y

    # ------------------------------------------------
    # TURN north, south, east, west (absolute turn)
    # ------------------------------------------------

    def turn_north(self, game_object):
        (nx, ny) = self.get_place_ahead(game_object)
        if game_object.is_eyes_open():
            self.remove_viewscreen(game_object, nx, ny)
        game_object.set_direction("north")
        self.canvas.itemconfig(game_object.get_canvas_image(), image=game_object.get_image())
        self.place(game_object, game_object.get_x(), game_object.get_y())
        return "north"

    def turn_south(self, game_object):
        (nx, ny) = self.get_place_ahead(game_object)
        if game_object.is_eyes_open():
            self.remove_viewscreen(game_object, nx, ny)
        game_object.set_direction("south")
        self.canvas.itemconfig(game_object.get_canvas_image(), image=game_object.get_image())
        self.place(game_object, game_object.get_x(), game_object.get_y())
        return "south"

    def turn_east(self, game_object):
        (nx, ny) = self.get_place_ahead(game_object)
        if game_object.is_eyes_open():
            self.remove_viewscreen(game_object, nx, ny)
        game_object.set_direction("east")
        self.canvas.itemconfig(game_object.get_canvas_image(), image=game_object.get_image())
        self.place(game_object, game_object.get_x(), game_object.get_y())
        return "east"

    def turn_west(self, game_object):
        (nx, ny) = self.get_place_ahead(game_object)
        if game_object.is_eyes_open():
            self.remove_viewscreen(game_object, nx, ny)
        game_object.set_direction("west")
        self.canvas.itemconfig(game_object.get_canvas_image(), image=game_object.get_image())
        self.place(game_object, game_object.get_x(), game_object.get_y())
        return "west"

    # ------------------------------------------------
    # TURN left, right (relative turn)
    # ------------------------------------------------

    def turn_left(self, game_object):
        (nx, ny) = self.get_place_ahead(game_object)
        if game_object.is_eyes_open():
            self.remove_viewscreen(game_object, nx, ny)
        if game_object.get_direction() == "north":
            res = self.turn_west(game_object)
        elif game_object.get_direction() == "south":
            res = self.turn_east(game_object)
        elif game_object.get_direction() == "west":
            res = self.turn_south(game_object)
        else:
            res = self.turn_north(game_object)
        return res

    def turn_right(self, game_object):
        (nx, ny) = self.get_place_ahead(game_object)
        if game_object.is_eyes_open():
            self.remove_viewscreen(game_object, nx, ny)
        if game_object.get_direction() == "north":
            res = self.turn_east(game_object)
        elif game_object.get_direction() == "south":
            res = self.turn_west(game_object)
        elif game_object.get_direction() == "west":
            res = self.turn_north(game_object)
        else:
            res = self.turn_south(game_object)
        return res

    # ------------------------------------------------
    # MOVE (forward and backward*)
    # * backward not yet implemented
    # Find the coordinates to move. The movement is done
    # after testing obstacles in the function which calls this one
    # ------------------------------------------------
    def move_north(self, game_object, movement):
        if movement == "forward":
            x = game_object.get_x()
            y = (game_object.get_y() - 1) % self.rows
        elif movement == "backward":
            x = game_object.get_x()
            y = (game_object.get_y() + 1) % self.rows
        #        self.change_position(object, x, y)
        else:
            return self.move_idle(game_object)
        return x, y

    def move_south(self, game_object, movement):
        if movement == "forward":
            x = game_object.get_x()
            y = (game_object.get_y() + 1) % self.rows
        elif movement == "backward":
            x = game_object.get_x()
            y = (game_object.get_y() - 1) % self.rows
        #       self.change_position(object, x, y)
        else:
            return self.move_idle(game_object)
        return x, y

    def move_east(self, game_object, movement):
        if movement == "forward":
            x = (game_object.get_x() + 1) % self.columns
            y = game_object.get_y()
        elif movement == "backward":
            x = (game_object.get_x() - 1) % self.columns
            y = game_object.get_y()
        #       self.change_position(object, x, y)
        else:
            return self.move_idle(game_object)
        return x, y

    def move_west(self, game_object, movement):
        if movement == "forward":
            x = (game_object.get_x() - 1) % self.columns
            y = game_object.get_y()
        elif movement == "backward":
            x = (game_object.get_x() + 1) % self.columns
            y = game_object.get_y()
        #        self.change_position(object, x, y)
        else:
            return self.move_idle(game_object)
        return x, y

    def move_idle(self, game_object):
        x = game_object.get_x()
        y = game_object.get_y()
        return x, y

    def is_target_obstacle(self, coordinates):
        """Test if in the coordinates there is an obstacle"""
        return any(isinstance(obj, go.Obstacle) for obj in self.object_matrix[coordinates[0]][coordinates[1]])

    def move(self, game_object, movement):
        """Moves to direction selected but only if there is no obstacle!"""
        if game_object.get_direction() == "north":
            res = self.move_north(game_object, movement)
            if not self.is_target_obstacle(res):
                self.change_position(game_object, res[0], res[1])

        elif game_object.get_direction() == "south":
            res = self.move_south(game_object, movement)
            if not self.is_target_obstacle(res):
                self.change_position(game_object, res[0], res[1])

        elif game_object.get_direction() == "east":
            res = self.move_east(game_object, movement)
            if not self.is_target_obstacle(res):
                self.change_position(game_object, res[0], res[1])

        elif game_object.get_direction() == "west":
            res = self.move_west(game_object, movement)
            if not self.is_target_obstacle(res):
                self.change_position(game_object, res[0], res[1])
        else:
            res = self.move_idle(game_object)
        return res

    # ------------------------------------------------
    # MOVE_HOME ()
    # ------------------------------------------------
    def move_home(self, game_object):
        home = game_object.get_home()
        self.place(game_object, home[0], home[1])

    # ------------------------------------------------
    # GET_PLACE_AHEAD (return coordinates of place ahead)
    # ------------------------------------------------
    def get_place_ahead(self, game_object):
        """Preview position ahead of the object"""
        if game_object.get_direction() == "north":
            return game_object.get_x(), self.change_y(game_object.get_y() - 1)

        elif game_object.get_direction() == "south":
            return game_object.get_x(), self.change_y(game_object.get_y() + 1)

        elif game_object.get_direction() == "east":
            return self.change_x(game_object.get_x() + 1), game_object.get_y()

        elif game_object.get_direction() == "west":
            return self.change_x(game_object.get_x() - 1), game_object.get_y()

        else:
            return game_object.get_x(), game_object.get_y()

    def get_place_direction(self, game_object, direction):
        """Preview position in direction"""
        if direction == "north":
            return game_object.get_x(), self.change_y(game_object.get_y() - 1)

        elif direction == "south":
            return game_object.get_x(), self.change_y(game_object.get_y() + 1)

        elif direction == "east":
            return self.change_x(game_object.get_x() + 1), game_object.get_y()

        elif direction == "west":
            return self.change_x(game_object.get_x() - 1), game_object.get_y()

        else:
            return game_object.get_x(), game_object.get_y()

    # ------------------------------------------------
    # GET_GOAL_POSITION (return the position of the goal)
    # ------------------------------------------------
    def get_goal_position(self):
        for column in self.object_matrix:
            for square in column:
                for game_object in square:
                    if isinstance(game_object, go.Goal):
                        return game_object.get_x(), game_object.get_y()
        return None

    # ------------------------------------------------
    # VIEW OBJECTS (return objects ahead)
    # ------------------------------------------------

    def view_object(self, x, y):
        """Return the type of object in the position given by 'coordinates'"""
        return [type(x).name for x in self.object_matrix[x][y]]

    def view_weights(self, game_object, view):
        if view == "front":
            x,y = self.get_place_ahead(game_object)
            return self.object_matrix[x][y][0].get_weight()
        else:
            return 0.0

    def view_global_weights(self):
        # Assuming the first element's type is always Patch...
        # return [[square[0].get_weight() for square in column] for column in self.object_matrix]
        weights =[]
        for c in range(self.columns):
            for r in range(self.rows):
                weights.append([(c,r),self.object_matrix[c][r][0].get_weight()])
        return weights

    def view_obstacles(self):
        obst =[]
        for column in self.object_matrix:
            for square in column:
                for obj in square:
                    if isinstance(obj,go.Obstacle) and obj.is_visible():
                        obst.append((obj.get_x(),obj.get_y()))
        return obst


#        return [[int(any(isinstance(obj, go.Obstacle) and obj.is_visible() for obj in square))
#                for square in column]
#                for column in self.object_matrix]


    # EXAMPLE_AGENT_SEARCH
    def mark(self, x, y, color):
        self.canvas.itemconfig(self.rectangles[x][y], fill=color)


    def unmark(self, x, y):
        self.canvas.itemconfig(self.rectangles[x][y], fill=self.bg_color)
