import pygame
import pygame_gui
from pygame.locals import *
from pygame_gui.elements import UIButton, UIPanel, UILabel, UIWindow


pygame.init()
clock = pygame.time.Clock()
clock.tick(60)


class Button():

	def __init__(self, image, pos, text_input, font, base_color, hovering_color) -> None:
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))


	def update(self, screen) -> None:
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)


	def checkForInput(self, position) -> bool:
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False


	def changeColor(self, position) -> None:
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)


class Grid:
    def __init__(self, filename, cell_size) -> None:
        self.cell_size = cell_size
        self.grid = self.load_level(filename)
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])

    def load_level(self, filename) -> list[list[str]]:
        with open(filename, 'r') as file:
            level_data = [line.strip().split() for line in file.readlines()]
        return level_data

    def draw(self, screen) -> None:
        for row in range(self.rows):
            for col in range(self.cols):
                x = col * self.cell_size
                y = row * self.cell_size
                cell_value = self.grid[row][col]
                
                if cell_value == '0':
                    color = (255, 255, 255) 
                elif cell_value == '1':
                    color = (0, 0, 0)
                elif cell_value == '2':
                    color = (0, 255, 0)
                elif cell_value == '#':
                    color = (255, 0, 0)
                elif cell_value == '$':
                    color = (0, 0, 255)
                
                rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, (200, 200, 200), rect, 1)


class Chat:
    def __init__(self, pos, width, font, line_height, max_commands) -> None:
        self.line_height = line_height
        self.max_commands = max_commands
        self.pos = pos
        self.width = width
        self.height = line_height * max_commands
        self.font = font
        self.messages = []
        

    def add_message(self, message) -> None:
        self.messages.append(message)

    def render(self, screen) -> None:
        pygame.draw.rect(screen, (255, 255, 255), (self.pos[0], self.pos[1], self.width, self.height), 2)
        
        for i in range(1, self.height // self.line_height):
            y = self.pos[1] + i * self.line_height
            pygame.draw.line(screen, (255, 255, 255), (self.pos[0], y), (self.pos[0] + self.width, y))

        current_y = self.pos[1] + 5
        for message in self.messages:
            text_surface = self.font.render(message, True, (255, 255, 255))
            screen.blit(text_surface, (self.pos[0] + 5, current_y))
            current_y += self.line_height


class Robot:

    def __init__(self, grid : Grid) -> None:
        self.grid = grid
        self.direction = 'UP'
        self.x, self.y = self.find_start_position()
        self.image = pygame.image.load("assets/robot.png")
        self.image = pygame.transform.scale(self.image, (self.grid.cell_size, self.grid.cell_size))
        self.rotated_image = self.image


    def find_start_position(self) -> None:
        for row in range(self.grid.rows):
            for col in range(self.grid.cols):
                if self.grid.grid[row][col] == '$':
                    return row, col


    def move_forward(self) -> None:
        new_x, new_y = self.x, self.y
        if self.direction == 'UP':
            new_y -= 1
        elif self.direction == 'DOWN':
            new_y += 1
        elif self.direction == 'LEFT':
            new_x -= 1
        elif self.direction == 'RIGHT':
            new_x += 1

        if 0 <= new_x < self.grid.cols and 0 <= new_y < self.grid.rows:
            cell_value = self.grid.grid[new_y][new_x]
            if cell_value != '1':
                self.x, self.y = new_x, new_y


    def turn_left(self) -> None:
        directions = ['UP', 'LEFT', 'DOWN', 'RIGHT']
        self.direction = directions[(directions.index(self.direction) + 1) % 4]
        self.rotate_image()


    def turn_right(self) -> None:
        directions = ['UP', 'RIGHT', 'DOWN', 'LEFT']
        self.direction = directions[(directions.index(self.direction) + 1) % 4]
        self.rotate_image()


    def rotate_image(self) -> None:
        angle = {'UP': 0, 'RIGHT': -90, 'DOWN': 180, 'LEFT': 90}[self.direction]
        self.rotated_image = pygame.transform.rotate(self.image, angle)


    def draw(self, screen) -> None:
        robot_rect = self.rotated_image.get_rect(center=(self.x * self.grid.cell_size + self.grid.cell_size // 2, 
                                                         self.y * self.grid.cell_size + self.grid.cell_size // 2))
        screen.blit(self.rotated_image, robot_rect.topleft)


class Robot_game:

    def __init__(self) -> None:
        self.screen_size = (1280, 720)
        self.screen = pygame.display.set_mode(self.screen_size)
        self.running = True


    @staticmethod
    def get_font(size: int) -> object:
        return pygame.font.Font("assets/font.ttf", size)


    def initialize_sucess_gui(self, score, max_commands) -> None:
        while self.running:
            MOUSE_POS = pygame.mouse.get_pos()

            OVER_BG = pygame.image.load("assets/background.png")
            OVER_BG = pygame.transform.scale(OVER_BG, self.screen_size)

            self.screen.blit(OVER_BG, (0, 0))

            VICTORY_TEXT = self.get_font(45).render(f"You WIN! With {max_commands - score} XP got", True, "White")
            VICTORY_RECT = VICTORY_TEXT.get_rect(center=(640, 20))
            self.screen.blit(VICTORY_TEXT, VICTORY_RECT)

            RETRY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 350), 
                                    text_input="PLAY", font=self.get_font(75), base_color="#ffffff", hovering_color="White")
            QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 500), 
                                    text_input="QUIT", font=self.get_font(75), base_color="#ffffff", hovering_color="White")

            RETRY_BUTTON.changeColor(MOUSE_POS)
            RETRY_BUTTON.update(self.screen)
            QUIT_BUTTON.changeColor(MOUSE_POS)
            QUIT_BUTTON.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if RETRY_BUTTON.checkForInput(MOUSE_POS):
                        self.init_level()
                    if QUIT_BUTTON.checkForInput(MOUSE_POS):
                        self.play()
            
            pygame.display.update()


    def initialize_failure_giu(self) -> None:
        while self.running:
            self.screen.fill("Black")

            MOUSE_POS = pygame.mouse.get_pos()

            OVER_BG = pygame.image.load("assets/background.png")
            OVER_BG = pygame.transform.scale(OVER_BG, self.screen_size)

            self.screen.blit(OVER_BG, (0, 0))

            FAILURE_TEXT = self.get_font(45).render("You LOSE!", True, "White")
            FAILURE_RECT = FAILURE_TEXT.get_rect(center=(640, 20))
            self.screen.blit(FAILURE_TEXT, FAILURE_RECT)

            RETRY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 350), 
                                    text_input="RETRY", font=self.get_font(75), base_color="#ffffff", hovering_color="White")
            QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 500), 
                                    text_input="QUIT", font=self.get_font(75), base_color="#ffffff", hovering_color="White")

            RETRY_BUTTON.changeColor(MOUSE_POS)
            RETRY_BUTTON.update(self.screen)
            QUIT_BUTTON.changeColor(MOUSE_POS)
            QUIT_BUTTON.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if RETRY_BUTTON.checkForInput(MOUSE_POS):
                        self.init_level()
                    if QUIT_BUTTON.checkForInput(MOUSE_POS):
                        self.play()
            
            pygame.display.update()


    def init_level(self) -> None:
        MAX_COMMANDS = 20
        grid = Grid("assets/level.txt", 50)
        robot = Robot(grid)
        
        chat = Chat(pos=(850, 0), width=400, font=self.get_font(20), line_height=30, max_commands=MAX_COMMANDS)
        BUTTONS = [
            Button(None, (100, 650), "Turn Left", self.get_font(25), "White", "Green"),
            Button(None, (300, 650), "Turn Right", self.get_font(25), "White", "Green"),
            Button(None, (500, 650), "Move Forward", self.get_font(25), "White", "Green")
        ]

        while self.running:
            self.screen.fill("#151d26")
            grid.draw(self.screen)
            robot.draw(self.screen)

            MOUSE_POS = pygame.mouse.get_pos()
            for button in BUTTONS:
                button.changeColor(MOUSE_POS)
                button.update(self.screen)

            START_BUTTON = Button(image=None, pos=(1050, 650), text_input="Start", font=self.get_font(30), base_color="White", hovering_color="Green")
            START_BUTTON.changeColor(MOUSE_POS)
            START_BUTTON.update(self.screen)
            
            chat.render(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in BUTTONS:
                        if button.checkForInput(MOUSE_POS):
                            chat.add_message(button.text_input)
                    
                    if START_BUTTON.checkForInput(MOUSE_POS):
                        if len(chat.messages) > chat.max_commands:
                            self.initialize_failure_giu()
                        for command in chat.messages:
                            if command == "Turn Left":
                                robot.turn_left()
                            elif command == "Turn Right":
                                robot.turn_right()
                            elif command == "Move Forward":
                                robot.move_forward()
                                if grid.grid[robot.y][robot.x] == '2':
                                    self.initialize_failure_giu()

                            pygame.time.delay(600)
                            grid.draw(self.screen)
                            robot.draw(self.screen)
                            
                            pygame.display.update()

                        pygame.time.delay(600)
                        if grid.grid[robot.y][robot.x] == '#':
                            self.initialize_sucess_gui(len(chat.messages), MAX_COMMANDS)
                        else:
                            self.initialize_failure_giu()
                            

            pygame.display.update()


    def play(self) -> None:
        while self.running:
            MOUSE_POS = pygame.mouse.get_pos()

            self.screen.fill("#151d26")

            PLAY_TEXT = self.get_font(45).render("This is the PLAY screen.", True, "White")
            PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 20))
            self.screen.blit(PLAY_TEXT, PLAY_RECT)

            BACK_BUTTON = Button(image=None, pos=(20, 10), 
                                text_input="BACK", font=self.get_font(25), base_color="White", hovering_color="Green")
            
            BACK_BUTTON.changeColor(MOUSE_POS)
            BACK_BUTTON.update(self.screen)

            LEVEL_BUTTON = Button(image=None, pos=(640, 320), 
                                text_input="LEVEL 1", font=self.get_font(25), base_color="White", hovering_color="Green")

            LEVEL_BUTTON.changeColor(MOUSE_POS)
            LEVEL_BUTTON.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if BACK_BUTTON.checkForInput(MOUSE_POS):
                        self.init_game()
                    if LEVEL_BUTTON.checkForInput(MOUSE_POS):
                        self.init_level()
            
            pygame.display.update()


    def init_game(self) -> None:
        while self.running:

            MAIN_BG = pygame.image.load("assets/background.png")
            MAIN_BG = pygame.transform.scale(MAIN_BG, self.screen_size)

            self.screen.blit(MAIN_BG, (0, 0))
            MOUSE_POS = pygame.mouse.get_pos()

            MENU_TEXT = self.get_font(100).render("MAIN MENU", True, "#ffffff")
            MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

            PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 350), 
                                text_input="PLAY", font=self.get_font(75), base_color="#ffffff", hovering_color="White")
            QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 500), 
                                text_input="QUIT", font=self.get_font(75), base_color="#ffffff", hovering_color="White")

            self.screen.blit(MENU_TEXT, MENU_RECT)
            
            for button in [PLAY_BUTTON, QUIT_BUTTON]:
                button.changeColor(MOUSE_POS)
                button.update(self.screen)

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                    pygame.quit()
				
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if QUIT_BUTTON.checkForInput(MOUSE_POS):
                        pygame.quit()
                    if PLAY_BUTTON.checkForInput(MOUSE_POS):
                          self.play()

            pygame.display.update()

game = Robot_game()
game.init_game()