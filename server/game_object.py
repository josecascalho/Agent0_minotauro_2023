from PIL import Image, ImageTk
# ------------------------------------------------------------
# CLASS OBJECT:
# ------------------------------------------------------------

class GameObject:
    """Every object in the world is an object.
    Different types of objects are special objects with specific attributes. This
    is the general object.
    """
    def __init__(self, name, image_file, config, x, y, direction, eyes_open=False, width=64, height=64):
        self.name = name
        self.x = x
        self.y = y
        self.home = (x, y)  # by default
        self.width = width
        self.height = height
        self.direction = direction
        self.graphics_mode = config["graphics_mode"]
        self.image_file = image_file
        self.image = None  # só para declarar em __init__
        self.canvas_image = None  # só para declarar em __init__
        self.image_dir = config["image_directory"]
        self.set_image()
        self.eyes_open = eyes_open
        self.view = {}
        self.view_type = ''
        self.weight = 0.0
        self.steps_view = False

    def get_weight(self):
        return self.weight

    def is_eyes_open(self):
        return self.eyes_open

    def open_eyes(self):
        self.eyes_open = True

    def close_eyes(self):
        self.eyes_open = False

    def set_image(self):
        if self.graphics_mode == 'bitmap':
            bitmap = tk.BitmapImage(file=self.image_dir + self.image_file + "_" + self.direction + ".xbm")
            self.image = bitmap
        else:
            im = Image.open(self.image_dir + self.image_file + "_" + self.direction + ".png")
            # print(self.image_dir + self.image_file + "_" + self.direction + ".png", self.width, self.height)
            im.thumbnail((self.width, self.height))
            photo = ImageTk.PhotoImage(im)
            self.image = photo

    def __del__(self):
        print('object {}" deleted'.format(self.name))

    def get_name(self):
        return self.name

    def set_home(self, home):
        self.home = home

    def get_home(self):
        return self.home

    def get_steps_view(self):
        return self.steps_view

    def set_steps_view(self):
        self.steps_view = True

    def reset_steps_view(self):
        self.steps_view = False

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def get_y(self):
        return self.y

    def get_x(self):
        return self.x

    def set_y(self, y):
        self.y = y

    def set_x(self, x):
        self.x = x

    def set_direction(self, direction):
        """direction can be north (up), south(down), east(right), west(left)"""
        self.direction = direction
        self.set_image()

    def get_direction(self):
        return self.direction

    def get_image(self):
        return self.image

    def get_image_file(self):
        return self.image_file

    def get_canvas_image(self):
        return self.canvas_image

    def set_canvas_image(self, canvas_image):
        self.canvas_image = canvas_image

    def get_worldview(self):
        return self.view

    def set_worldview(self, front='', north='', east='', south='', west=''):
        if self.view_type == "front":
            self.view = {"front": front}
        elif self.view == "around":
            self.view = {"north": north, east: "east", "south": south, "west": west}
        else:
            set.view = {}

    def get_view_type(self):
        return self.view_type


# ------------------------------------------------------------
# CLASS PLAYER:
# ------------------------------------------------------------
class Player(GameObject):
    name = "player"
    def __init__(self, name, x, y, direction, view_type, config, width=64, height=64):
        super().__init__(name, "agent1", config, x, y, direction, width=width, height=height)
        self.view_type = view_type


# ------------------------------------------------------------
# CLASS OBSTACLE:
# ------------------------------------------------------------
class Obstacle(GameObject):
    name = "obstacle"

    def __init__(self, name, x, y, config, visible):
        self.visible = visible
        super().__init__(name, "obstacle"+str(int(visible)), config, x, y, "south")

    def is_visible(self):
        return self.visible


# ------------------------------------------------------------
# CLASS Bomb:
# ------------------------------------------------------------
class Bomb(GameObject):
    name = "bomb"

    def __init__(self, name, x, y, config):
        super().__init__(name, "bomb1", config, x, y, "south")


# ------------------------------------------------------------
# CLASS BombSound:
# ------------------------------------------------------------
class BombSound(GameObject):
    name = "bomb_sound"

    def __init__(self, name, x, y, config):
        super().__init__(name, "bomb_sound1", config, x, y, "south")


# ------------------------------------------------------------
# CLASS PATCH:
# ------------------------------------------------------------
class Patch(GameObject):
    name = "unknown"

    def __init__(self, name, image_file, x, y, w, config):
        super().__init__(name, image_file, config, x, y, "south")
        self.weight = w

# ------------------------------------------------------------
# CLASS GOAL:
# ------------------------------------------------------------
class Goal(GameObject):
    name = "goal"

    def __init__(self, name, x, y, config):
        super().__init__(name, "goal", config, x, y, "south")

