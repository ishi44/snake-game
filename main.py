
from tkinter import *
import random


GAME_WIDTH = 700                    #dimensions of grid
GAME_HEIGHT = 700                  #dimensions of grid
SPEED = 100                        #speed of snake
SPACE_SIZE = 50                    #size of each grid block
BODY_PARTS = 3                   #initial size of snake
SNAKE_COLOR = 'green'
FOOD_COLOR = 'red'
BACKGROUND_COLOR = "black"


# defining class for snake object
class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = [ ]
        self.squares = [ ]

        # asessing coordinates for body parts of snake
        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x,y, x+SPACE_SIZE, y+SPACE_SIZE,fill =SNAKE_COLOR,tag = 'snake')
            self.squares.append(square)


# defining class for food object
class Food:

   def __init__(self):
       # generating random coordinates within valid range
      a = random.randint(0, (GAME_WIDTH/SPACE_SIZE)-1) * SPACE_SIZE
      b = random.randint(0, (GAME_HEIGHT/SPACE_SIZE)-1)* SPACE_SIZE

      self.coordinates = [a, b]

      #creating food object
      canvas.create_oval(a, b, a + SPACE_SIZE, b + SPACE_SIZE, fill=FOOD_COLOR,tag = "food")



# defining movement of snake's head in response to the direction
def next_turn(snake, food):

        # coordinates of snake head
        x, y = snake.coordinates[0]

        if direction == 'up':
            y -= SPACE_SIZE

        elif direction == 'down':
            y += SPACE_SIZE

        elif direction == 'left':
            x -= SPACE_SIZE

        elif direction == 'right':
            x += SPACE_SIZE

       # updating the snake's head position in the list to its new location
        snake.coordinates.insert(0, (x, y))

        # creating head of snake
        square = canvas.create_rectangle(x, y, x+SPACE_SIZE, y+SPACE_SIZE,fill=SNAKE_COLOR)

        #updating the head of track
        snake.squares.insert(0, square)

#overlapping of snake head and food
        if x == food.coordinates[0] and y == food.coordinates[1]:
            global score
            score += 1

            #changing score label
            label.config(text="Score: {}".format(score))

            #deleting food object by using tag
            canvas.delete('food')

            food = Food()

# deleting last part of snake if didnt eat food object
        else:

            del snake.coordinates[-1]
            canvas.delete(snake.squares[-1])
            del snake.squares[-1]


        if check_collisions(snake):
            game_over()
        else:
            window.after(SPEED, next_turn, snake, food)



# create a restart function:
def restart_game():
    global snake, food, score, direction

    # Reset game variables to initial values;game reset logic
    canvas.delete(ALL)
    snake = Snake()
    food = Food()
    score = 0
    direction = 'down'
    label.config(text="Score:{}".format(score))
    next_turn(snake, food)



# responsible for changing the direction of the snake when a key is pressed.
def change_direction(new_direction):

    '''
enable the player to control the snake's movement
in a way that ensures it doesn't immediately reverse and
collide with itself
    '''

    global direction
    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction

    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction

    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction

    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction



#defining function check collisions

def check_collisions(snake):
#unpack head of snake
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True

    elif y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        #if snake collides with itself
        if x == body_part[0] and y == body_part[1] :
            print('GAME OVER')
            return True

    return False


#defining function game over

def game_over():
    canvas.delete(ALL)
    canvas.create_text(350,350, text = 'GAME OVER',fill='red',font=('Roboto',50),tags='gameover')
    canvas.update()



#creating main application window
window = Tk()

#creating title for application window
window.title("Snake Game")

#creating non-resizable window
window.resizable(False, False)

score = 0
direction = 'down'

#creating a score label
label = Label(window, text='Score: {}'.format(score), font=('Verdana', 30))
label.pack()

#creating a canvas
canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH  )

canvas.pack()

# add a restart button to the window:
restart_button = Button(window, text="Restart", command= restart_game, font=('consolas', 20), fg='blue', bg='lightgray')
restart_button.place(x=0, y=0)


#setting window in the center of the screen
window.update()
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width//2)-(window_width//2))
y = int((screen_height-window_height)//2)

#setting the tkinter main window size and position using string formatting
window.geometry('%dx%d+%d+%d' % (window_width, window_height, x, y))


#game controls
window.bind('<Left>',lambda event: change_direction('left'))
window.bind('<Right>',lambda event: change_direction('right'))
window.bind('<Up>',lambda event: change_direction('up'))
window.bind('<Down>',lambda event: change_direction('down'))

#access the event object to print information about the keypress event
# Function to handle key presses

def print_key_event(event):
    key_pressed = event.keysym
    print(f"Key Pressed: {key_pressed}")
    TEXT = canvas.create_text(350, 30, text="Key Pressed: " + key_pressed, font=('Arial', 10), fill='white', tags='keys')
    canvas.update()
    canvas.after(500, canvas.delete, TEXT)

# Bind the key press event
window.bind('<KeyPress>', print_key_event)

# Focus the window to capture key events
window.focus_set()


#creating snake object , calling snake function
snake = Snake()

#creating food object , calling food function
food = Food()

#calling next_turn function
next_turn(snake, food)

window.update()

#start the main event loop
window.mainloop()
