import turtle
import winsound
from tkinter import *
import tkinter.font as tkFont
import random

# Main Menu class, contains the selections of gamemode and quitting the application
class Menu:
    def __init__(self):
        # The choice by the user of what game-mode to play
        self.choice = 0
        # Plays background music on start-up
        winsound.PlaySound("bg.wav", winsound.SND_ASYNC | winsound.SND_LOOP)
    
    def draw(self):
        # Creates a tKinter window
        self.root = Tk()
        self.root.title("Pong Menu")
        self.root.geometry("800x600")

        # Create interactables for user
        title_label = Label(self.root, text="PONG", font=("Comic Sans", 48))
        button_start = Button(self.root, text="Normal Game", padx="75", font=("Comic Sans", 24) , command=self.choice1)
        button_start2 = Button(self.root, text="Hardcore", padx="75", font=("Comic Sans", 24) , command=self.choice2)
        button_start3 = Button(self.root, text="Crazy", padx="75", font=("Comic Sans", 24) , command=self.choice3)
        button_exit = Button(self.root, text="Quit Game", padx="75", font=("Comic Sans", 24), command=exit)

        # Add the interactables to window
        title_label.pack()
        button_start.pack()
        button_start2.pack()
        button_start3.pack()
        button_exit.pack()

        # loop the window so it doesn't close
        self.root.mainloop()

    # Choice for normal gamemode. then close window
    def choice1(self):
        self.choice = 1
        winsound.PlaySound(None, winsound.SND_ASYNC)
        self.root.destroy()

    # Choice for hard gamemode. then close window
    def choice2(self):
        self.choice = 2
        winsound.PlaySound(None, winsound.SND_ASYNC)
        self.root.destroy()
    
    # Choice for crazy gamemode. then close window
    def choice3(self):
        self.choice = 3
        winsound.PlaySound(None, winsound.SND_ASYNC)
        self.root.destroy()

    # Returns the choice made by the user
    def getChoice(self):
        return self.choice

# Holds information about the game logic as well as the window, game objects and sound
class Pong:

    # Initializes window settings
    def __init__(self, window, choice):
        self.choice = choice # Choice made by the user
        self.window = window # Creates a new window
        # Sets window dimensions
        self.wWidth = 800
        self.wHeight = 600
        self.window.title("Pong") # Window title
        if(choice == 3): # If user chose crazy mode, change to specific title
            self.window.title("EXTREME PONG")
            self.wWidth = 1600
            self.wHeight = 1200
        self.window.bgcolor("black") # Set window background color
        if(choice == 3):
            self.window.bgcolor("#B0E0E6")
        self.window.setup(width=self.wWidth, height=self.wHeight) 
        self.window.tracer(0)
        
    # Starts the game by intialzing values and creating game objects
    def runGame(self):
        # Create game objects
        white = "white"
        if(self.choice == 1):
            ballspeed = .2
            ballmulti = 0.05
        if(self.choice == 2):
            ballspeed = .3
            ballmulti = 0.1
        if(self.choice == 3):
            ballspeed = .4
            ballmulti = 0.3
            white = "#ADD8E6"

        # Create game objects
        paddle_left = Paddle("Left Paddle", "square", white, -(self.wWidth / 2 - 50), 0)
        paddle_right = Paddle("Right Paddle", "square", white, self.wWidth / 2 - 50, 0)
        ball = Ball("Ball", "square", "white", 0, 0, ballspeed, ballmulti)
        scoreboard = Scoreboard("white", "Courier", 0, 260)

        # Update the content ofthe scoreboard
        scoreboard.update()

        # Keyboard binding
        self.window.listen() # Sets the window to be "listening" to keyboard inputs

        self.window.onkeypress(paddle_left.move_up, "w") # Calls the left_up function when the window hears "w" key
        self.window.onkeyrelease(paddle_left.stop, "w")
        self.window.onkeypress(paddle_left.move_down, "s") # Calls the left_down function when the window hears "s" key
        self.window.onkeyrelease(paddle_left.stop, "s")

        self.window.onkeypress(paddle_right.move_up, "Up") # Calls the left_up function when the window hears "w" key
        self.window.onkeyrelease(paddle_right.stop, "Up")
        self.window.onkeypress(paddle_right.move_down, "Down") # Calls the left_down function when the window hears "s" key
        self.window.onkeyrelease(paddle_right.stop, "Down")

        # Main Game Logic loop
        while True:
            self.window.update() # Constantly updates the locations of objects on the window
            
            # If the game is not over, then let the game objects move
            if(not scoreboard.isGameover()):
                
                # Ball movement
                ball.travel()

                # Paddle movement
                paddle_left.travel()
                paddle_right.travel()

            # Ball - Border Collision
            if ball.getY() > self.wHeight / 2 - 10: # If ball reaches top of window
                ball.sety(self.wHeight / 2 - 10)
                ball.bounceY(-1) # reflects the ball
                
                winsound.PlaySound("bounce.wav", winsound.SND_ASYNC) # ASYNC lets the sound play in the background

            if ball.getY() < -(self.wHeight / 2 - 10): # If ball reaches bottom of window
                ball.sety(-(self.wHeight / 2 - 10))
                ball.bounceY(-1)  # reflects the ball
                
                winsound.PlaySound("bounce.wav", winsound.SND_ASYNC) # ASYNC lets the sound play in the background

            if ball.getX() > self.wWidth / 2 - 10: # If ball reaches right of window
                ball.reset() # Reset the ball to the center

                scoreboard.score_left() # increase the score
                winsound.PlaySound("score.wav", winsound.SND_ASYNC)              
                
            if ball.getX() < -(self.wWidth / 2 - 10): # If ball reaches left of window
                ball.reset() # Reset the ball to the center

                scoreboard.score_right() # increase the score
                winsound.PlaySound("score.wav", winsound.SND_ASYNC)
            
            # Ball - Paddle Collisions

            # Right paddle
            if (ball.getX() > (self.wWidth / 2 - 60) and ball.getX() < (self.wWidth / 2 - 50)) and (ball.getY() < paddle_right.getY() + 40 and ball.getY() > paddle_right.getY() - 40):
                ball.setx((self.wWidth / 2 - 60))
                ball.accelerate() # Increase the speed of the ball
                ball.bounceX(-1)
                
                winsound.PlaySound("bounce.wav", winsound.SND_ASYNC) # ASYNC lets the sound play in the background


            # Left paddle
            if (ball.getX() < -(self.wWidth / 2 - 60) and ball.getX() > -(self.wWidth / 2 - 50)) and (ball.getY() < paddle_left.getY() + 40 and ball.getY() > paddle_left.getY() - 40):
                ball.setx(-(self.wWidth / 2 - 60))
                ball.bounceX(-1)
                ball.accelerate() # Increase the speed of the ball

                winsound.PlaySound("bounce.wav", winsound.SND_ASYNC) # ASYNC lets the sound play in the background

            # Paddle - Border Collisions
            if(paddle_left.getY() + 50 > self.wHeight / 2):
                paddle_left.sety(self.wHeight / 2 - 50)
                paddle_left.stop()
            
            if(paddle_left.getY() - 50 < -(self.wHeight / 2)):
                paddle_left.sety(-(self.wHeight / 2 - 50))
                paddle_left.stop()
            
            if(paddle_right.getY() + 50 > self.wHeight / 2):
                paddle_right.sety(self.wHeight / 2 - 50)
                paddle_right.stop()
            
            if(paddle_right.getY() - 50 < -(self.wHeight / 2)):
                paddle_right.sety(-(self.wHeight / 2 - 50))
                paddle_right.stop()

            # If the game is over, give user new key commands
            if(scoreboard.isGameover()):
                self.window.onkeypress(scoreboard.restart, "space") # Restarts the game
                self.window.onkeypress(self.window.bye, "t") # Closes the game

class Paddle:

    # Creats a paddle object, with a name, shape, color and starting position
    def __init__(self, name, shape, color, x, y): # Does nothing
        self.name = name
        self.turtle = turtle.Turtle()
        self.turtle.speed(0) # Animtation speed
        self.turtle.shape(shape) # Shape of the paddle
        self.turtle.color(color) # Color of the paddle
        self.turtle.shapesize(stretch_wid=5, stretch_len=1) # width is 5x bigger (100px), length is still 20px
        self.turtle.penup() # Prevents the drawing of a "line"
        self.turtle.goto(x, y)
        self.speed = 0 # starting speed of paddle

    # Moves the paddle automatically
    def travel(self):
        self.turtle.sety(self.turtle.ycor() + self.speed)

    # Gives paddle up velocity
    def move_up(self): # Moves the left paddle up
        self.speed = .75
    
    # Gives paddle down velocity
    def move_down(self): # Moves the left paddle up
        self.speed = -.75

    # Stops the paddle
    def stop(self):
        self.speed = 0

    def getY(self):
        return self.turtle.ycor()

    def getX(self):
        return self.turtle.xcor()

    def setx(self, x):
        self.turtle.setx(x)

    def sety(self, y):
        self.turtle.sety(y)

class Ball:
    # Creates a ball object with name, shape, color, start position, start speed, and speed incremenet mulitplier
    def __init__(self, name, shape, color, x, y, basespeed, multiplier):
        self.name = name
        self.multiplier = multiplier # the value at which the speed increases at each paddle bounce
        self.basespeed = basespeed # start speed of ball
        self.turtle = turtle.Turtle()
        self.turtle.speed(0) # Animtation speed
        self.turtle.shape(shape) # Shape of the paddle
        self.turtle.color(color) # Color of the paddle
        self.turtle.penup() # Prevents the drawing of a "line"
        self.turtle.goto(x, y)
        self.dx = random.choice([-basespeed, basespeed]) # Gives ball a random start direction
        self.dy = random.choice([-basespeed, basespeed])

    # Function for moving the ball
    def travel(self):
        self.turtle.setx(self.turtle.xcor() + self.dx) # Position of the ball changes by curr pos + dx
        self.turtle.sety(self.turtle.ycor() + self.dy) # Position of the ball changes by curr pos + dy

    def setx(self, x):
        self.turtle.setx(x)

    def sety(self, y):
        self.turtle.sety(y)
    
    def relocate(self, x, y):
        self.turtle.setx(x)
        self.turtle.sety(y)

    def getX(self):
        return self.turtle.xcor()
    
    def getY(self):
        return self.turtle.ycor()
    
    def setSpeed(self, value):
        self.dx = value
        self.dy = value
    
    # Increase the speed of the ball by its own mulitplier
    def accelerate(self):
        self.dx += self.multiplier
        self.dy += self.multiplier
    
    def bounceX(self, value):
        self.dx *= value

    def bounceY(self, value):
        self.dy *= value
    
    # Resets the position, and speed of the ball
    def reset(self):
        self.turtle.setx(0)
        self.turtle.sety(0)
        self.dx = random.choice([-self.basespeed, self.basespeed])
        self.dy = random.choice([-self.basespeed, self.basespeed])


# Keeps track of the players' scores and other instructions
class Scoreboard:

    def __init__(self, color, font, x, y):
        self.x = x
        self.y = y
        self.turtle = turtle.Turtle()
        self.turtle.speed(0) # Animation speed
        self.turtle.color(color) # Text color
        self.turtle.penup() # Removes trail
        self.turtle.hideturtle() # Won't see on screen
        self.turtle.goto(x, y) # 0, 260
        self.font = font

        # Score counter
        self.left_score = 0
        self.right_score = 0

        # Keeps track if game is over (IE player has won)
        self.gameover = False

    # Increase the score of left player then update scoreboard
    def score_left(self):
        self.left_score += 1
        self.update()

    # Increase the score of right player then update scoreboard
    def score_right(self):
        self.right_score += 1
        self.update()

    # Return if game is over
    def isGameover(self):
        return self.gameover

    # Update the values of the scoreboard or display new information depending on gamestate
    def update(self):
        self.turtle.clear() # Clears the scoreboard
        # Write score information
        self.turtle.write("Player A: {} Player B: {}".format(self.left_score, self.right_score), align="center", font=(self.font, 24, "normal"))
        # font holds a tuple object

        if(self.right_score >= 5):
            # Right player wins
            
            self.turtle.goto(0, 100)
            self.turtle.write("Player B wins!", align="center", font=(self.font, 24, "normal"))
            self.turtle.goto(0, -100)
            self.turtle.write("Press Space to Restart", align="center", font=(self.font, 24, "normal"))
            self.turtle.goto(0, -150)
            self.turtle.write("Press T to Quit", align="center", font=(self.font, 24, "normal"))
            winsound.PlaySound("win.wav", winsound.SND_ASYNC) # play win sound

            self.turtle.goto(self.x, self.y)
            self.gameover = True

        if(self.left_score >= 5):
            # Left player wins
            winsound.PlaySound("win.wav", winsound.SND_ASYNC)
            self.turtle.goto(0, 100)
            self.turtle.write("Player A wins!", align="center", font=(self.font, 24, "normal"))
            self.turtle.goto(0, -100)
            self.turtle.write("Press Space to Restart", align="center", font=(self.font, 24, "normal"))
            self.turtle.goto(0, -150)
            self.turtle.write("Press T to Quit", align="center", font=(self.font, 24, "normal"))
            winsound.PlaySound("win.wav", winsound.SND_ASYNC)  # play win sound

            self.turtle.goto(self.x, self.y)
            self.gameover = True # Sets the game to 'gameover'

    # Restarts the scoreboard
    def restart(self):
        self.right_score = 0
        self.left_score = 0
        self.update()

        self.gameover = False

# GAME STARTS HERE!

# Create an empty game menu
menu = Menu()
# Draw the values in the menu 
menu.draw()
# When menu is either closed or application is ended

# If menu is closed, then start a version of pong game
window = turtle.Screen() # Create empty screen
pong = Pong(window, menu.getChoice()) # Fill screen with game details, based on menu choice
pong.runGame() # Start the pong game