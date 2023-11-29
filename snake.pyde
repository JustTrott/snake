# snake game in Python 2.7.1 (not by choice, but by the virtue)
import os, random, sys

RESOLUTION = 600
COLS_COUNT = 20
ROWS_COUNT = 20
CELL_WIDTH = RESOLUTION / COLS_COUNT
CELL_HEIGHT = RESOLUTION / ROWS_COUNT
SNAKE_START_LENGTH = 2
FOOD_VALUE = 1

BACKGROUND_COLOR = color(205)
BLACK_BACKDROP = color(0, 128)
GAME_OVER_COLOR = color(255)
BLACK = color(0)

# a dictionary of directions used to determine numerical changes in columns (dcol, drow)
# i.e. (1, 0) means +1 to column and +0 to row, which is movement to the right
DIRECTIONS = {RIGHT: (1, 0), LEFT: (-1, 0), UP: (0, -1), DOWN: (0, 1)}

GAME_OVER_MSG = "Game Over"
WIN_MSG = "HAMILTON!"

# utility class containing common functions
class Utils:
    def getTopLeftCorner(self, col, row):
        return (CELL_WIDTH  * col, CELL_HEIGHT * row)
    
    def getCenter(self, col, row):
        x, y = self.getTopLeftCorner(col, row)
        return (x + CELL_WIDTH / 2, y + CELL_HEIGHT / 2)
    
    def getPath(self, location):
        if os is mac:
            /
        else:
            \\
        return os.getcwd() + "\\data\\" + location
    
    def resizeImagesToFitCells(self, *images):
        for img in images:
            img.resize(CELL_WIDTH, CELL_HEIGHT)
            

# class representing the main game logic
class Game:
    def __init__(self, foodImageLocations, foodColors, snakeHeadUpImageLocation, snakeHeadLeftImageLocation, snakeColor):
        self.foodImages = [loadImage(utils.getPath(location)) for location in foodImageLocations]
        # resize images to fit the cell size
        utils.resizeImagesToFitCells(*self.foodImages)
        self.foodColors = [color(*code) for code in foodColors]
        snakeHeadUpImage = loadImage(utils.getPath(snakeHeadUpImageLocation))
        snakeHeadLeftImage = loadImage(utils.getPath(snakeHeadLeftImageLocation))
        utils.resizeImagesToFitCells(snakeHeadUpImage, snakeHeadLeftImage)
        self.snake = Snake(COLS_COUNT // 2, ROWS_COUNT // 2, SNAKE_START_LENGTH, snakeHeadUpImage, snakeHeadLeftImage, color(*snakeColor))
        self.food = self.generateFood()
        self.isFinished = False
        self.score = 0
        
    def display(self):
        background(BACKGROUND_COLOR)
        self.snake.display()
        self.food.display()
        fill(BLACK)
        self.displayScore()
    
    def displayGameOver(self):
        fill(BLACK_BACKDROP)
        rect(0, 0, RESOLUTION, RESOLUTION)
        fill(GAME_OVER_COLOR)
        textSize(CELL_WIDTH * 2)
        x, y = utils.getTopLeftCorner(COLS_COUNT // 2, ROWS_COUNT // 2)
        text(GAME_OVER_MSG, x, y)
        self.displayScore()
    
    def displayScore(self):
        textAlign(CENTER)
        textSize(CELL_WIDTH / 1.5)
        x, y= utils.getTopLeftCorner(COLS_COUNT - 4, 1)
        text("Score: " + str(self.score), x, y)
        
    def restart(self):
        self.snake = Snake(COLS_COUNT // 2, ROWS_COUNT // 2, SNAKE_START_LENGTH, self.snake.head.upImage, self.snake.head.leftImage, self.snake[1].fillColor)
        self.food = self.generateFood()
        self.isFinished = False
        self.score = 0
        
    def update(self):
        if self.isFinished:
            return
        if self.snake.head.futureDirection is not None:
            self.snake.head.applyDirection()
            # display the head to correctly show the new direction even if the the game ends later
            self.snake.head.display() 
            
        lastTailPosition = self.snake.move()
        if not self.snake.isMovePossible():
            self.isFinished = True
            self.displayGameOver()
            return
        if self.snake.isItemColliding(self.food):
            self.handleFoodCollision(lastTailPosition)
            
    
    def handleFoodCollision(self, lastTailPosition):
        self.score += self.food.value
        self.snake.append(SnakeElement(lastTailPosition[0], lastTailPosition[1], self.food.growColor))
        if len(self.snake) >= COLS_COUNT * ROWS_COUNT:
            background(BACKGROUND_COLOR)
            self.snake.display()
            self.displayGameOver(WIN_MSG)
            self.isFinished = True
            return
        self.food = self.generateFood()
        
    def generateFood(self):
        foodType = random.randint(0, len(self.foodImages) - 1)
        img = self.foodImages[foodType]
        growColor = self.foodColors[foodType]
        
        newFood = Food(random.randint(0, COLS_COUNT - 1), random.randint(0, ROWS_COUNT - 1), growColor, img, FOOD_VALUE)
        # try to regenerate food so that it does not appear in the snake's body
        while self.snake.isItemColliding(newFood):
            newFood.setPosition(random.randint(0, COLS_COUNT - 1), random.randint(0, ROWS_COUNT - 1))
        
        return newFood

# define the snake class to inherit from list, to store it's elements
class Snake(list):
    def __init__(self, col, row, startLength, headUpImage, headLeftImage, snakeColor):
        # head is defined explicitly for simplicity of access 
        self.head = SnakeHead(col, row, headUpImage, headLeftImage, RIGHT)
        self.append(self.head)
        for i in range(startLength):
            # subtract i + 1 from col to add snake body elements to the left of the head
            self.append(SnakeElement(col - i - 1, row, snakeColor))
                        
    def display(self):
        for item in self:
            item.display()
         
    def isItemColliding(self, item):
        for snakeElement in self:
            if item == snakeElement:
                continue
            if item.getPosition() == snakeElement.getPosition():
                return True
        return False
       
    def isMovePossible(self):
        if self.head.col < 0 or self.head.col >= COLS_COUNT or self.head.row < 0 or self.head.row >= ROWS_COUNT:
            return False
        if self.isItemColliding(self.head):
            return False
        return True
    
    def move(self):
        lastTailPosition = self[-1].getPosition()
        for i in reverse(range(1, len(self))):
            self[i].row = self[i - 1].row
            self[i].col = self[i - 1].col
        direction = DIRECTIONS[self.head.direction]
        self.head.setPosition(self.head.col + direction[0], self.head.row + direction[1])
        return lastTailPosition


# inheritance from object is required in older versions of python for super() to work
# declare a super class representing all objects on the game field
class GameItem(object):
    def __init__(self, col, row):
        self.col = col
        self.row = row
        
    def getPosition(self):
        return (self.col, self.row)
    
    def setPosition(self, col, row):
        self.col, self.row = col, row
    
    # __str__ and __repr__ are defined for debugging purposes
    def __str__(self):
        return self.__class__.__name__ + " at " + str(self.col) + " " + str(self.row)
    
    def __repr__(self):
        return self.__str__()
    
    
class SnakeElement(GameItem):
    def __init__(self, col, row, fillColor):
        super(SnakeElement, self).__init__(col, row)
        self.fillColor = fillColor
        
    def display(self):
        noStroke()
        fill(self.fillColor)
        x, y = utils.getCenter(self.col, self.row)
        circle(x, y, CELL_WIDTH)


class SnakeHead(GameItem):
    def __init__(self, col, row, upImage, leftImage, direction):
        super(SnakeHead, self).__init__(col, row)
        self.direction = direction
        # define a variable to store the direction to be applied later
        # otherwise bugs arise when inputting directions too quickly
        self.futureDirection = None
        self.upImage = upImage
        self.leftImage = leftImage
        
    def setDirection(self, directionKey):
        # skip new direction if it is the same or opposite of the current one
        if self.direction in (LEFT, RIGHT) and directionKey in (LEFT, RIGHT):
            return
        if self.direction in (UP, DOWN) and directionKey in (UP, DOWN):
            return
        self.futureDirection = directionKey
    
    def applyDirection(self):
        if self.futureDirection is not None:
            self.direction = self.futureDirection
            self.futureDirection = None
    
    def display(self):
        x, y = utils.getTopLeftCorner(self.col, self.row)
        if self.direction == UP:
            image(self.upImage, x, y, CELL_WIDTH, CELL_HEIGHT, 0, 0, CELL_WIDTH, CELL_HEIGHT)
        elif self.direction == DOWN:
            image(self.upImage, x, y, CELL_WIDTH, CELL_HEIGHT, CELL_HEIGHT, CELL_WIDTH, 0, 0) # Displaying head looking up flipped vertically
        elif self.direction == RIGHT:
            image(self.leftImage, x, y, CELL_WIDTH, CELL_HEIGHT, CELL_WIDTH, 0, 0, CELL_HEIGHT)
        else:
            image(self.leftImage, x, y, CELL_WIDTH, CELL_HEIGHT, 0, 0, CELL_WIDTH, CELL_HEIGHT) # Displaying head looking left flipped horizontally
                
class Food(GameItem):
    def __init__(self, col, row, growColor, img, value):
        super(Food, self).__init__(col, row)
        self.growColor = growColor
        self.img = img
        self.value = value
    
    def display(self):
        x, y = utils.getTopLeftCorner(self.col, self.row)
        image(self.img, x, y, CELL_WIDTH, CELL_WIDTH)
                
# initialize game and utility objects
utils = Utils()
game = Game(["apple.png", "banana.png"], [(173, 48, 32), (251, 226, 76)], "head_up.png", "head_left.png", (80, 153, 32))

# setup and draw functions for processing
def setup():
    size(RESOLUTION, RESOLUTION)
    background(BACKGROUND_COLOR)
    frameRate(60)

def draw():
    if frameCount % 12 == 0:
        game.update()
        if not game.isFinished:
            game.display()

# mouse and key event handlers
def mouseClicked():
    # to prevent restarts during the game
    if game.isFinished:
        game.restart()

def keyPressed():
    if not game.isFinished:
        game.snake.head.setDirection(keyCode)
