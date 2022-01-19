import tkinter as tk
from PIL import Image, ImageTk
from random import randint

MOVE_INC = 20
MOVES_PER_SEC = 10
GAME_SPEED = 1000 // MOVES_PER_SEC #floor division rounds down to nearest whole number

class Snake(tk.Canvas):
    def __init__(self):
        super().__init__(width=600, height=620, background="black", highlightthickness=0)

        self.score = 0
        self.direction = "Right"
        self.bind_all("<Key>", self.on_key_press)

        self.snake_positions = [(100,100), (80,100), (60,100)]
        self.food_position = self.set_new_food_position()

        self.load_assets()

        self.create_objects()

        self.after(GAME_SPEED, self.perform_actions)

    def load_assets(self):
        try:
            self.snake_body_image = Image.open('/Users/sailormetz/Python/Completed_Projects/Snake_Game/assets/snake.png')
            self.snake_body = ImageTk.PhotoImage(self.snake_body_image)

            self.food_image = Image.open('/Users/sailormetz/Python/Completed_Projects/Snake_Game/assets/food.png')
            self.food = ImageTk.PhotoImage(self.food_image)
        except IOError as error:
            print(error)
            root.destroy()

    def create_objects(self):
        """
        places all initial assets from load_assets(): the snake body parts, food, and the canvas rectangle that defines the game boundaries.
        """
        self.create_text(45, 12, text=f"Score: {self.score}", fill="#fff", tag="score", font=("TkDefaultFont", 14))

        for x_pos, y_pos in self.snake_positions:
            self.create_image(x_pos, y_pos, image=self.snake_body, tag="snake")

        self.create_image(*self.food_position, image=self.food, tag="food")
        self.create_rectangle(20, 40, 580, 600, outline="#525d69")

    def move_snake(self):
        head_x_pos, head_y_pos = self.snake_positions[0]

        if self.direction == "Left":
            new_head_pos = (head_x_pos - MOVE_INC, head_y_pos)

        elif self.direction == "Right":
            new_head_pos = (head_x_pos + MOVE_INC, head_y_pos)

        elif self.direction == "Down":
            new_head_pos = (head_x_pos, head_y_pos + MOVE_INC)

        elif self.direction == "Up":
            new_head_pos = (head_x_pos, head_y_pos - MOVE_INC)

        self.snake_positions = [new_head_pos] + self.snake_positions[:-1]

        for segment, position in zip(self.find_withtag("snake"), self.snake_positions):
            self.coords(segment, position)

    def perform_actions(self):
        if self.check_collisions():
            self.end_game()

        self.check_food_collision()

        self.move_snake()
        self.after(GAME_SPEED, self.perform_actions)

    def check_collisions(self):
        head_x_pos, head_y_pos = self.snake_positions[0]

        return (
            head_x_pos in (20, 580)
            or head_y_pos in (40, 600)
            or (head_x_pos, head_y_pos) in self.snake_positions[1:]
        )

    def on_key_press(self, e):
        new_direction = e.keysym
        all_directions = ("Up", "Down", "Left", "Right")
        opposites = ({"Up", "Down"}, {"Left", "Right"}) #using sets because they don't care about order just unique members.

        if (
            new_direction in all_directions
            and {new_direction, self.direction} not in opposites
            ):
            self.direction = new_direction

    def check_food_collision(self):
        if self.snake_positions[0] == self.food_position:
            self.score += 1
            #we duplicate the tail, so that when we cut it to move it stays the same length
            self.snake_positions.append(self.snake_positions[-1])

            self.create_image(*self.snake_positions[-1], image=self.snake_body, tag="snake")

            self.food_position = self.set_new_food_position()
            self.coords(self.find_withtag("food"), self.food_position)

            score = self.find_withtag("score")
            self.itemconfigure(score, text=f"Score: {self.score}", tag="score") #must update score with canvas.itemconfigure()

    def set_new_food_position(self):
        while True:
            x_pos = randint(2, 28) * MOVE_INC
            y_pos = randint(3, 29) * MOVE_INC

            food_position = (x_pos, y_pos)

            if food_position not in self.snake_positions:
                return food_position

    def end_game(self):
        self.delete(tk.ALL)
        self.create_text(
            self.winfo_width()/2,
            self.winfo_height()/2,
            text=f"Game over. Your score: {self.score}",
            fill="#fff",
            font=18
        )

root = tk.Tk()
root.title("Snake")
root.resizable(False, False)

board = Snake()

board.pack()

root.mainloop()
