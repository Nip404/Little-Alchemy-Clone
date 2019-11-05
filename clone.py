from Elements import Inventory, Merger
import pygame
import time
import sys

# window dimensions
s = [1000, 800]

# initialisations
pygame.init()
screen = pygame.display.set_mode(s, 0, 32)
pygame.display.set_caption("Alchemist v1.1.4 by NIP")

big = pygame.font.SysFont("Garamond MS", 50)
med = pygame.font.SysFont("Garamond MS", 14)
med2 = pygame.font.SysFont("Garamond MS", 22)

def main():
    startscreen()
    highscore = None

    while True:
        bag = Inventory(screen, med)
        merger = Merger(screen, med)
        t0 = time.time()

        while True:
            screen.fill((255, 255, 255))

            # event handler
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # checks if mouse overlaps with icon
                    merger.update(bag.select(pygame.mouse.get_pos(), merger))
                    bag = merger.interact(pygame.mouse.get_pos(), bag)

                elif event.type == pygame.KEYDOWN:
                    # keyboard shortcuts
                    if event.key == pygame.K_SPACE:
                        merger.inputs = []
                    elif event.key == pygame.K_RETURN:
                        merger.interact([i+5 for i in merger.boxes[-1]], bag)
                        
            bag.draw()
            merger.draw()

            # checks if all items are discovered
            if all([all([i[1] for i in bag.grid[j]]) for j in range(4)]):
                break
            
            pygame.display.flip()

        # updates highscore and does endscreen
        highscore = endscreen(int(time.time() - t0), highscore)

def startscreen():
    head = big.render("Alchemist", True, (0, 0, 0))
    foot = med2.render("Click to play", True, (0, 0, 0))
    
    while True:
        screen.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                return

        screen.blit(head, head.get_rect(center=(s[0]/2, s[1]/2 - 100)))
        screen.blit(foot, foot.get_rect(center=(s[0]/2, s[1]/2 + 50)))

        pygame.display.flip()

def endscreen(time, high):
    if high is None or time > high:
        high = time
        
    head = big.render("Congradulations!", True, (0, 0, 0))
    head2 = big.render(f"You completed the game in {time} seconds!", True, (0, 0, 0))
    head3 = big.render(f"Highscore: {high} seconds", True, (0, 0, 0))
    foot = med2.render("Click to play again", True, (0, 0, 0))

    while True:
        screen.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                return high

        screen.blit(head, head.get_rect(center=[s[0]/2, s[1]/3]))
        screen.blit(head2, head2.get_rect(center=[s[0]/2, s[1]/2 - 70]))
        screen.blit(head3, head3.get_rect(center=[s[0]/2, s[1]/2]))
        screen.blit(foot, foot.get_rect(center=[s[0]/2, s[1]/2 + 50]))

        pygame.display.flip()

if __name__ == "__main__":
    main()
