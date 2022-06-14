import pygame
from network import Network
import pickle

from pygame import mixer
pygame.mixer.init()
mixer.music.load('./music/background.wav')
mixer.music.play(-1)


pygame.font.init()

width = 1920
height = 1080
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")


class Button:
    def __init__(self, text, x, y):
        self.text = text
        self.x = x
        self.y = y
        self.width = 160
        self.height = 165


    def draw(self, win):
        font = pygame.font.Font("AznKnuckles.otf", 40)
        if self.text == "Rock":
            btn = pygame.image.load("./img/rock.png")
            win.blit(btn, (self.x + round(self.width/2) - round(btn.get_width()/2), self.y + round(self.height/2) - round(btn.get_height()/2)))
        elif self.text == "Scissors":
            btn = pygame.image.load("./img/scissors.png")
            win.blit(btn, (self.x + round(self.width/2) - round(btn.get_width()/2), self.y + round(self.height/2) - round(btn.get_height()/2)))
        elif self.text == "Paper":
            btn = pygame.image.load("./img/paper.png")
            win.blit(btn, (self.x + round(self.width/2) - round(btn.get_width()/2), self.y + round(self.height/2) - round(btn.get_height()/2)))
        text = font.render(self.text, 1, (0,0,0))
        win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) + round(btn.get_height()/2) + 20))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False


def redrawWindow(win, game, p):
    bg = pygame.image.load("./img/background.jpg")
    win.blit(bg, (0, 0))

    if not(game.connected()):
        font = pygame.font.Font("AznKnuckles.otf", 80)
        text = font.render("Waiting for Player...", 1, (70, 70, 70))
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
    else:
        font = pygame.font.Font("AznKnuckles.otf", 60)
        text = font.render("Your Move Opponents", 1, (0, 51,102))
        win.blit(text, (width/2 - text.get_width()/2, height/2 - 300))

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)
        if game.bothWent():
            text1 = font.render(move1, 1, (0,0,0))
            text2 = font.render(move2, 1, (0, 0, 0))
        else:
            if game.p1Went and p == 0:
                text1 = font.render(move1, 1, (0,0,0))
            elif game.p1Went:
                text1 = font.render("Locked In", 1, (0, 0, 0))
            else:
                text1 = font.render("Waiting...", 1, (0, 0, 0))

            if game.p2Went and p == 1:
                text2 = font.render(move2, 1, (0,0,0))
            elif game.p2Went:
                text2 = font.render("Locked In", 1, (0, 0, 0))
            else:
                text2 = font.render("Waiting...", 1, (0, 0, 0))

        if p == 1:
            win.blit(text2, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
            win.blit(text1, (width / 2 - text.get_width() / 2 + 400, height / 2 - text.get_height() / 2))
        else:
            win.blit(text2, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
            win.blit(text1, (width / 2 - text.get_width() / 2 + 400, height / 2 - text.get_height() / 2))

        for btn in btns:
            btn.draw(win)

    pygame.display.update()


btns = [Button("Rock", 680, 700), Button("Scissors", 880, 700), Button("Paper", 1080, 700)]
def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP())
    print("You are player", player)

    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run = False
            print("Couldn't get game")
            break

        if game.bothWent():
            redrawWindow(win, game, player)
            pygame.time.delay(500)
            try:
                game = n.send("reset")
            except:
                run = False
                print("Couldn't get game")
                break

            font = pygame.font.Font("AznKnuckles.otf", 90)
            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                text = font.render("You Won!", 1, (255,0,0))
            elif game.winner() == -1:
                text = font.render("Tie Game!", 1, (255,0,0))
            else:
                text = font.render("You Lost...", 1, (255,0,0))

            win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2 - 130))
            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos) and game.connected():
                        if player == 0:
                            if not game.p1Went:
                                n.send(btn.text)
                        else:
                            if not game.p2Went:
                                n.send(btn.text)

        redrawWindow(win, game, player)

def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        bg = pygame.image.load("./img/background.jpg")
        win.blit(bg, (0, 0))
        font = pygame.font.Font("AznKnuckles.otf", 150)
        text = font.render("Click to Play!", 1, (70,70,70))
        win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main()

while True:
    menu_screen()