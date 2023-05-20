import itertools
import sys

import pygame

from minesweeper.core.world import CellStatus, CellType, World

pygame.init()

world = World.from_((20, 20, 20))
clicked = False

WINDOW_WIDTH = world.map_size[0] * 30
WINDOW_HEIGHT = world.map_size[1] * 30

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


def drawWorld(world: World, screen: pygame.Surface):
    screen.fill((255, 255, 255))

    for i, j in itertools.product(range(world.map_size[0]), range(world.map_size[1])):
        rect = pygame.Rect(i * 30, j * 30, 30, 30)
        match world.cells[i][j]:
            case (_, CellStatus.CLOSED, mines):
                pygame.draw.rect(screen, (128, 128, 128), rect)
                pygame.draw.rect(screen, (192, 192, 192), rect.inflate(-4, -4))
            case (CellType.EMPTY, CellStatus.OPENED, mines):
                neighbours = world.get_neighbour_cells(i, j)
                render_neighbours = (
                    any(map(lambda x: x[1] == CellStatus.OPENED, neighbours))
                    and mines > 0
                )
                if render_neighbours:
                    font = pygame.font.SysFont("arial", 30)
                    text = font.render(str(mines), True, (192, 192, 192))
                    screen.blit(text, rect)
                else:
                    pygame.draw.rect(screen, (192, 192, 192), rect)
            case (CellType.MINE, CellStatus.OPENED, _):
                pygame.draw.rect(screen, (255, 0, 0), rect)
            case (_, CellStatus.MARKED_MINE, _):
                font = pygame.font.SysFont("Segoe UI Emoji", 30)
                text = font.render("🚩", True, (192, 192, 192))
                screen.blit(text, rect)
            case (_, CellStatus.MARKED_UNKNOWN, _):
                font = pygame.font.SysFont("Segoe UI Emoji", 30)
                text = font.render("❓", True, (192, 192, 192))
                screen.blit(text, rect)
            case _:
                pass


def renderWin(screen: pygame.Surface):
    font = pygame.font.SysFont("arial", 30)
    text = font.render("You win!", True, (0, 255, 0))
    screen.blit(text, (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))


def renderOver(screen: pygame.Surface):
    font = pygame.font.SysFont("arial", 30)
    text = font.render("Game over!", True, (255, 0, 0))
    screen.blit(text, (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))


def handle_mouseup(event: pygame.event.Event):
    global clicked, world
    if event.type == pygame.MOUSEBUTTONUP:
        if event.button == 1:
            row = event.pos[0] // 30
            column = event.pos[1] // 30
            if not clicked:
                clicked = True
                while world.cells[row][column][0] == CellType.MINE:
                    world = World.from_((20, 20, 20))
            world.open(row, column)
        elif event.button == 2:
            world.mark_unknown(event.pos[0] // 30, event.pos[1] // 30)
        elif event.button == 3:
            world.mark_mine(event.pos[0] // 30, event.pos[1] // 30)


def checkExit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


while True:
    if not (world.win or world.game_over):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            handle_mouseup(event)
        drawWorld(world, screen)
    elif world.win:
        renderWin(screen)
        checkExit()
    else:
        renderOver(screen)
        checkExit()
    pygame.display.update()
