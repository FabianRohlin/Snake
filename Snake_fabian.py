import pygame
import random
import pygame_menu
import csv

# Set up game variables
windowWidth = 520
windowHeight = 600
gridSize = 20
snakeSize = 20
snakeColor = (227, 28, 121)
foodColor = (255, 0, 0)
score = 0
header = 80

# Initialize pygame
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((windowWidth, windowHeight))

# Define classes
class Snake:
    # Generating snake spawn coordinates
    def __init__(self):
        self.x = windowWidth // 2
        self.y = (windowHeight + header) // 2
        self.dx = 0
        self.dy = 0
        self.body = [(self.x, self.y)]
    # Updating the snake
    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.body.insert(0, (self.x, self.y))
        self.body.pop()
    # Drawing the snake
    def draw(self):
        for x, y in self.body:
            pygame.draw.rect(screen, snakeColor, (x, y, snakeSize, snakeSize))

class Food:
    # Generating food spawn coordinates
    def __init__(self):
        self.x = random.randint(0, windowWidth // gridSize - 1) * gridSize
        self.y = random.randint(0 + header // gridSize, (windowHeight) // gridSize - 1) * gridSize
    # Drawing the food
    def draw(self):
        pygame.draw.rect(screen, foodColor, (self.x, self.y, gridSize, gridSize))

def background(cellSize):
    # Function to make a checkered background
    for i in range(round(windowWidth // cellSize // 2)):
        for j in range(round(windowWidth // cellSize)):
            pygame.draw.rect(screen, "green", ((j * cellSize) + cellSize * i * 2, j * cellSize + 80, cellSize, cellSize))
            pygame.draw.rect(screen, "green", ((j * cellSize) - cellSize * i * 2, j * cellSize + 80, cellSize, cellSize))

def sort(name, score):
    filename = 'scoreboard.csv'
    # Open the CSV file and read its contents
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        data = list(reader)
        data.append([name, score])

    # Convert the data into a list of tuples
    data = [(row[0], float(row[1])) for row in data]

    # Sort the data using insertion sort by the second column
    insertionSort(data)

    # Write the sorted data back to the CSV file
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        for row in data:
            writer.writerow(row)

# Sorting the scoreboard
def insertionSort(arr):
    for i in range(1, len(arr)):
        j = i - 1
        key = arr[i]
        while j >= 0 and arr[j][1] > key[1]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

# Displaying the scoreboard
def scoreboard():
    # Essential variables
    windowWidth = 520
    windowHeight = 600

    screen = pygame.display.set_mode((windowWidth, windowHeight))
    font = pygame.font.Font(None, 36)

    filename = 'scoreboard.csv'
    scoreboardRun = True
    while scoreboardRun:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                scoreboardRun = False
        screen.fill((28, 105, 10))
        # Reading the scoreboard and puts it in a list
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            data = list(reader)
            y = 50  # starting y-position for the scores
        # Drawing the scoreboard
        for i, (player, score) in enumerate(data[::-1]):
            text = font.render(f"{i + 1}. {player}: {score}", True, (0, 0, 0))
            text_rect = text.get_rect(center=(windowWidth // 2, y))
            screen.blit(text, text_rect)
            y += 50
            if y >= windowHeight:
                break

        pygame.display.flip()

def startTheGame():
    # Essential variables
    windowWidth = 520
    windowHeight = 600
    gridSize = 20
    score = 0
    name = name_1.get_value()
    font = pygame.font.Font('freesansbold.ttf', 32)
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((windowWidth, windowHeight))
    snake = Snake()
    food = Food()
    running = True
    while running:

        # Movement
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and (time.time()-delay)>0.1:
                if (event.key == pygame.K_UP or event.key == pygame.K_w) and snake.dy != gridSize:
                    snake.dx = 0
                    snake.dy = -gridSize
                    delay=time.time()
                elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and snake.dy != -gridSize:
                    snake.dx = 0
                    snake.dy = gridSize
                    delay=time.time()
                elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and snake.dx != gridSize:
                    snake.dx = -gridSize
                    snake.dy = 0
                    delay=time.time()
                elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and snake.dx != -gridSize:
                    snake.dx = gridSize
                    snake.dy = 0
                    delay=time.time()

        # Updating the snake object
        snake.update()

        # Check for collisions
        if snake.x < 0 or snake.x >= windowWidth or snake.y < header or snake.y >= windowHeight:
            sort(name, score)
            running = False
        for x, y in snake.body[1:]:
            if snake.x == x and snake.y == y:
                running = False
        if snake.x == food.x and snake.y == food.y:
            food = Food()
            snake.body.append(snake.body[-1])
            score += 1

        # Draw game objects
        screen.fill((28, 105, 10))
        background(gridSize)
        pygame.draw.rect(screen, 'blue', pygame.Rect(0, 0, 600, header))
        scoreText = font.render("Score: " + str(score), True, (255, 255, 255))
        screen.blit(scoreText, (10, 10))
        snake.draw()
        food.draw()
        pygame.display.flip()

        # Set game speed
        clock.tick(10)

# Menu
menu = pygame_menu.Menu('Welcome', windowWidth, windowHeight, theme=pygame_menu.themes.THEME_BLUE)

name_1 = menu.add.text_input('Name:', default='', maxchar=15)
menu.add.button('Play', startTheGame)
menu.add.button('Scoreboard', scoreboard)
menu.add.button('Quit', pygame_menu.events.EXIT)

# Game loop
menu.mainloop(screen)
