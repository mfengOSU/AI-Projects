import pygame
import sys
import time

from nim import train

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (70, 102, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Create game
pygame.init()
size = width, height = 600, 400
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Play Nim")

# Fonts
largeFont = pygame.font.SysFont(name='copperplatettc, sans-serif', size=80)
mediumFont = pygame.font.SysFont(name='copperplatettc, sans-serif', size=30)
smallFont = pygame.font.SysFont(name='copperplatettc, sans-serif', size=22)

play = False
instructions = False
one_player = False
two_player = False

ai = train(10000)
circles 
while True:
    # Check for quit game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    
    screen.fill(BLACK)

    if not play:
        # Title
        title = largeFont.render('NIM', True, BLUE)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 50)
        screen.blit(title, titleRect)
        # Play Button   
        buttonRect = pygame.draw.polygon(screen, GREEN, [((width / 2) - (75 / 2)+10, (3 / 5) * height + 10),
                                                        ((width / 2) - (75 / 2)+10, (3 / 5) * height + 65),
                                                        ((width / 2) - (75 / 2)+65, (3 / 5) * height + (75 / 2))])
        # Check if play button pressed
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if buttonRect.collidepoint(mouse):
                play = True
                instructions = True
                time.sleep(0.3)
        pygame.display.flip()
        continue

    if instructions:
        rules = ["Nim is a 2-player game",
                "Each player takes turns removing 1 or more items",
                "     from a single row",
                "The last person to remove the last item loses"
                ]
        for i, rule in enumerate(rules):
            text = smallFont.render(rule, True, BLUE)
            textRect = text.get_rect()
            textRect.topleft = ((width / 22), 50 + 30 * i)
            screen.blit(text, textRect)

        computerRect = pygame.Rect((width / 22), (height - 150), width / 4, 50)
        computerText = smallFont.render("One player", True, WHITE)
        computerTextRect = computerText.get_rect()
        computerTextRect.center = computerRect.center
        pygame.draw.rect(screen, GREEN, computerRect)
        screen.blit(computerText, computerTextRect)

        humanRect = pygame.Rect((width - (width / 22) - (width / 4), (height - 150), width / 4, 50))
        humanText = smallFont.render("Two players", True, WHITE)
        humanTextRect = humanText.get_rect()
        humanTextRect.center = humanRect.center
        pygame.draw.rect(screen, GREEN, humanRect)
        screen.blit(humanText, humanTextRect)

        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if computerRect.collidepoint(mouse):
                instructions = False
                one_player = True
                time.sleep(0.3)
            elif humanRect.collidepoint(mouse):
                instructions = False
                two_player = True
                time.sleep(0.3)
        
        pygame.display.flip()
        continue
    
    if one_player:
        

    pygame.display.flip()

#ai = train(10000)
#play(ai)

