from settings import *

class Game():
    def __init__(self):
        # Inicializacion de pygame y variables del juego
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)) # Hace el window surface
        pygame.display.set_icon(icon)
        pygame.display.set_caption('Vaqueromon')    # Nombra al window
        self.clock = pygame.time.Clock()
        self.running = True

        # Grupos
        self.all_sprites = pygame.sprite.Group()    # Todos los sprites del juego estan en este grupo

    def run(self):
        while self.running:
            self.dt = self.clock.tick() / 1000      # Recoge el tiempo en milisegundos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # updates
            self.all_sprites.update()               # Actualiza todos los sprites en cada frame      
        
            # draw
            self.all_sprites.draw(self.display_surface)     # Dibuja los sprites en display surface cada segundo
            pygame.display.update                           # Actualiza el display window

        pygame.quit()

if __name__ == '__main__':                          # Solo corre el programa si es llamado main.py
    game = Game()
    game.run()
        
    