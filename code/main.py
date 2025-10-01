from settings import *
from support import *
from timer import Timer
from monster import Monster, Opponent

class Game():
    def __init__(self):
        # Inicializacion de pygame y variables del juego
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)) # Hace el window surface
        pygame.display.set_icon(icon)
        pygame.display.set_caption('Vaqueromon')
        self.clock = pygame.time.Clock()
        self.running = True
        self.import_assets()

        # Grupos
        self.all_sprites = pygame.sprite.Group()    # Todos los sprites del juego estan en este grupo

        # Data
        player_monster_list = ['Sparchu', 'Cleaf', 'Jacana']
        self.player_monsters = [Monster(name, self.back_surfs[name]) for name in player_monster_list]
        self.monster = self.player_monsters[0]
        self.all_sprites.add(self.monster)
        opponent_name = 'Plumette'
        self.opponent = Opponent(opponent_name,self.front_surfs[opponent_name],self.all_sprites)

    def import_assets(self):
        self.back_surfs = folder_importer('images', 'back')
        self.front_surfs = folder_importer('images', 'front')
        self.bg_surfs = folder_importer('images', 'other')

    def draw_monster_floor(self):
        for sprite in self.all_sprites:
            floor_rect = self.bg_surfs['floor'].get_frect(center = sprite.rect.midbottom + pygame.Vector2(0, -10))
            self.display_surface.blit(self.bg_surfs['floor'], floor_rect)

    def run(self):
        while self.running:
            self.dt = self.clock.tick() / 1000      # Recoge el tiempo en milisegundos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # updates
            self.all_sprites.update(self.dt)               # Actualiza todos los sprites en cada frame      
        
            # draw
            self.display_surface.blit(self.bg_surfs['bg'],(0,0))
            self.draw_monster_floor()
            self.all_sprites.draw(self.display_surface)     # Dibuja los sprites en display surface cada segundo
            pygame.display.update()                         # Actualiza el display window

        pygame.quit()

if __name__ == '__main__':                          # Solo corre el programa si es llamado main.py
    game = Game()
    game.run()
        
    