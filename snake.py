'''
    Snake Game built in python using Pygame
'''


#imports 
import random, sys
import pygame as pg

#CONSTANTS
TILE_SIZE = 25
DIRECTIONS = {
    'UP':(-1,0),
    'DOWN':(1,0),
    'RIGHT':(0,1),
    'LEFT':(0,-1)
}

#helper functions
def check_tiles_placment(tile_1,tile_2):
    if tile_1[0] - tile_2[0] <= 0 and tile_1[1] - tile_2[1] <= 0 :
        return True
    else:
        return False
        

class Snake():
    def __init__(self,grid_width,grid_height):
        self.grid_width = grid_width//TILE_SIZE
        self.grid_height = grid_height//TILE_SIZE
        self.grid_tiles = self.get_grid_tiles()
        self.food_available = False
        self.food_slot = []
        self.reset()
        self.snake_head = self.snake_tiles[0]
        self.snake_vel = [0,0]
        self.previous_direction = ""
        self.still_alive = False

    def reset(self):
        self.snake_length = 1
        self.snake_tiles = []
        self.alive = True
        self.snake_spawn = random.choice(self.grid_tiles)
        self.snake_tiles.append(self.snake_spawn)
        self.spawn_food()

    def __str__(self):
        '''
            String represetation of snake object printing it's tiles locations and length
        '''
        print("snake length: " + str(self.snake_length))

        return str(self.snake_tiles)

    def get_grid_width(self):
        '''
        returning grid width
        '''
        return self.grid_width

    def get_grid_height(self):
        '''
        returning grid height
        '''
        return self.grid_height    

    def get_empty_tiles(self):
        '''
            returning empty tiles on the grid that doens't contain snake tiles
        '''
        empty_tiles = list(self.grid_tiles)
        for tile in self.snake_tiles:
            if tile in empty_tiles:
                empty_tiles.remove(tile)
        
        return empty_tiles
        
    def get_grid_tiles(self):
        '''
        returning grid tiles based on width, height, TILE_SIZE
        '''
        grid_tiles = []
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                grid_tiles.append([row,col])

        return grid_tiles

    def spawn_food(self):
        if not self.food_available:
            self.food_slot = random.choice(self.get_empty_tiles())
            self.food_available = True

    def snake_movement(self):
        snake_head = list(self.snake_tiles[0])
        snake_head[0] += self.snake_vel[0]
        snake_head[1] += self.snake_vel[1]
        movement_allowed = True

        if self.check_death(snake_head):
            movement_allowed = False
            self.still_alive = False
        else:
            if movement_allowed:
                for idx in range(len(self.snake_tiles)-1,0,-1):
                    self.snake_tiles[idx][0] = self.snake_tiles[idx-1][0]
                    self.snake_tiles[idx][1] = self.snake_tiles[idx-1][1]
                self.snake_growth()

                if snake_head[0] < 0:
                    self.snake_tiles[0][0] = self.grid_height-1
                    self.snake_tiles[0][1] += self.snake_vel[1]
                elif snake_head[0] > self.grid_height-1:
                    self.snake_tiles[0][0] = 0
                    self.snake_tiles[0][1] += self.snake_vel[1]
                elif snake_head[1] < 0:
                    self.snake_tiles[0][0] += self.snake_vel[0]
                    self.snake_tiles[0][1] = self.grid_width-1
                elif snake_head[1] > self.grid_width-1:
                    self.snake_tiles[0][0] += self.snake_vel[0]
                    self.snake_tiles[0][1] = 0
                else:
                    self.snake_tiles[0][0] += self.snake_vel[0]
                    self.snake_tiles[0][1] += self.snake_vel[1]
            
                
                

        self.snake_head = list(self.snake_tiles[0])

    def snake_growth(self):
        if self.snake_head == self.food_slot:
            new_tile = list(self.snake_tiles[self.snake_length-1])
            self.snake_tiles.append(new_tile)
            self.snake_length += 1
            self.food_available = False
            self.spawn_food()

    def check_death(self, snake_head):
        for idx in range(2,len(self.snake_tiles)) :           
            if snake_head == self.snake_tiles[idx]:
                return True
    
    def set_snake_vel(self,direction):
        snake_head = list(self.snake_tiles[0])
        snake_head[0] += DIRECTIONS[direction][0]
        snake_head[1] += DIRECTIONS[direction][1]

        if self.snake_length > 1:
            if snake_head != self.snake_tiles[1]:
                self.snake_vel[0] = DIRECTIONS[direction][0]
                self.snake_vel[1] = DIRECTIONS[direction][1]
            else:
                self.snake_vel[0] = self.snake_vel[0] 
                self.snake_vel[1] = self.snake_vel[1]
        else:
            self.snake_vel[0] = DIRECTIONS[direction][0]
            self.snake_vel[1] = DIRECTIONS[direction][1]

           
        
class Game_GUI():
    def __init__(self,snake):
        pg.init()
        self._snake = snake
        self.grid_width = self._snake.get_grid_width()
        self.grid_height = self._snake.get_grid_height()
        self.frame_width = self.grid_width * TILE_SIZE
        self.frame_height = self.grid_height * TILE_SIZE
        self.screen = pg.display.set_mode((self.frame_width, self.frame_height))
        self.clock = pg.time.Clock()

    def play(self):
        '''
            Main loop to run frame and handling events
        '''
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    sys.exit()
                else:
                    if self._snake.still_alive:
                        self.movement_handler(event)
                    else:
                        self.mouse_handler(event)

            self.screen.fill((0,0,0))       
            if self._snake.still_alive:
                self.draw_grid()
                self._snake.snake_movement()
                self.draw_snake_and_food()
            else:
                self.draw_splash()
            pg.display.update()
            self.clock.tick(8)

    def draw_grid(self):
        '''
            drawing grid based on rect and snake tiles
        '''
        for col in range(self.grid_width):
            start_pos = ((TILE_SIZE + col*TILE_SIZE),0)
            end_pos = ((TILE_SIZE + col*TILE_SIZE),self.frame_height)
            pg.draw.line(self.screen,(255,255,255),start_pos,end_pos,1)

        for row in range(self.grid_height):
            start_pos = (0,(TILE_SIZE + row*TILE_SIZE))
            end_pos = (self.frame_width,(TILE_SIZE + row*TILE_SIZE))
            pg.draw.line(self.screen,(255,255,255),start_pos,end_pos,1)
     
    def draw_snake_and_food(self):
        '''
            drawing snake tiles & food based on rect
        '''
        food_slot = self._snake.food_slot
        food_x_pos = (food_slot[1]*TILE_SIZE)+TILE_SIZE//2 + 1
        food_y_pos = (food_slot[0]*TILE_SIZE)+TILE_SIZE//2 + 1
        food_circle = pg.draw.circle(self.screen,(30,144,255),(food_x_pos,food_y_pos),7)

        idx = 0
        for tile in self._snake.snake_tiles:
            rect = pg.Rect(tile[1]*(TILE_SIZE)+1,tile[0]*(TILE_SIZE)+1,TILE_SIZE-1,TILE_SIZE-1)
            if idx == 0:
                pg.draw.rect(self.screen,(128,0,0),rect)
            else:
                pg.draw.rect(self.screen,(255,0,0),rect) 
            idx += 1

    def movement_handler(self,event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                self._snake.set_snake_vel('UP')

            elif event.key == pg.K_DOWN:
                self._snake.set_snake_vel('DOWN')

            elif event.key == pg.K_RIGHT:
                self._snake.set_snake_vel('RIGHT')

            elif event.key == pg.K_LEFT:
                self._snake.set_snake_vel('LEFT')

        elif event.type == pg.KEYUP:
            pass

    def draw_splash(self):
        global start_game_button
        logo_font = pg.font.Font(None,100)
        logo_text_surface = logo_font.render("Snake Game",True,(200,200,200))
        logo_rect = [logo_text_surface.get_rect().width/2,logo_text_surface.get_rect().height/2]
        self.screen.blit(logo_text_surface,((self.frame_width/2)-logo_rect[0],(self.frame_height/4)-logo_rect[1]))

        start_game_button = pg.Rect((self.frame_width/2)-150,(self.frame_height/2)-37,300,75)
        pg.draw.rect(self.screen,(245,50,99),start_game_button)

        new_game_font = pg.font.Font(None,50)
        new_game_text_surface = new_game_font.render("Start New Game",True,(200,200,200))
        new_game_rect = [new_game_text_surface.get_rect().width/2,new_game_text_surface.get_rect().height/2]
        self.screen.blit(new_game_text_surface,(start_game_button.centerx-new_game_rect[0],start_game_button.centery-new_game_rect[1]))

    def mouse_handler(self,event):
        global start_game_button
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if start_game_button.collidepoint(event.pos):
                    self._snake.still_alive = True
                    self._snake.reset()


snake = Snake(500,500)
game = Game_GUI(snake)

game.play()
