import pygame
import solve
from pygame.locals import *
from sys import exit

colors = [
    (0xff, 0x00, 0xff), (0x80, 0x00, 0x80),
    (0x00, 0x00, 0xff), (0x00, 0x00, 0x80),
    (0x00, 0xff, 0xff), (0x00, 0x80, 0x80),
    (0x00, 0xff, 0x00), (0x00, 0x80, 0x00),
    (0xff, 0xff, 0x00), (0x80, 0x80, 0x00),
    (0xff, 0x00, 0x00), (0x80, 0x00, 0x00),
    (0xc0, 0xc0, 0xc0), (0xff, 0xff, 0xff),
    (0x80, 0x80, 0x80),
]

BLACK_COLOR = (0, 0, 0)

SENS_DIS = 10
R_RADIUS = 5
l_count = 0


class Menu:
    def __init__(self, scn):
        self.screen = scn
        self.update = pygame.image.load("update.png").convert_alpha()
        self.update_rect = pygame.Rect(5, 100, 90, 30)

    def draw(self):
        self.screen.blit(self.update, self.update_rect.topleft)

    def click_button(self, pos):
        if self.update_rect.collidepoint(pos):
            global l_count
            l_count = solve.solve2(solve.loop_ceiling)
            return True
        return False


def draw_routers(routers, scn):
    # print("draw routers")
    for r in routers:
        pygame.draw.circle(scn, colors[r.curr], r.get_location(), int(solve.interfere_ranges[r.curr]))
    scn.set_alpha(5)
    for r in routers:
        pygame.draw.circle(scn, BLACK_COLOR, r.get_location(), R_RADIUS)


def get_catch_index(routers, pos, dist):
    (x2, y2) = pos
    for i, r in enumerate(routers):
        (x1, y1) = r.get_location()
        print((x1, y1), (x2, y2))
        if (x1 - x2) ** 2 + (y1 - y2) ** 2 < dist ** 2:
            return i
    return -1


if __name__ == '__main__':

    pygame.init()
    screen = pygame.display.set_mode((800, 600), 0, 32)
    screen.fill((255, 255, 255))
    clock = pygame.time.Clock()
    solve.load()
    # print(len(solve.variables))
    l_count = solve.solve2(solve.loop_ceiling)
    # print("solving end")
    # for v in variables:
    #     print(v)

    # print("solving end")
    drag_index = -1
    pygame.display.set_caption('Router Demo')

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                exit()
            if event.type == KEYDOWN and event.key == K_RETURN:
                print("enter")
                l_count = solve.solve2(solve.loop_ceiling)
                screen.fill((255, 255, 255))
                draw_routers(solve.variables, screen)
                pygame.display.update()
            if event.type == MOUSEBUTTONUP:
                drag_index = -1
            if event.type == MOUSEBUTTONDOWN:
                print("mouse button down")
                pressed_mouse = pygame.mouse.get_pressed()
                if pressed_mouse[0]:
                    print("left button")
                    drag_index = get_catch_index(solve.variables, pygame.mouse.get_pos(), SENS_DIS)
                    print(drag_index)
                    if drag_index != (len(solve.variables)-1):
                        variable = solve.variables[drag_index]
                        solve.variables.pop(drag_index)
                        solve.variables.append(variable)
                        drag_index = len(solve.variables) - 1
                    # screen.fill((255, 255, 255))

                elif pressed_mouse[1]:
                    print("middle button")
                    pos = pygame.mouse.get_pos()
                    solve.append_variables(pos)
                    draw_routers(solve.variables, screen)
                    pygame.display.update()
                elif pressed_mouse[2]:
                    print("right button")
                    drag_index = get_catch_index(solve.variables, pygame.mouse.get_pos(), SENS_DIS)
                    if drag_index != -1:
                        solve.variables.pop(drag_index)
                    # l_count = solve.solve2(solve.loop_ceiling)
                        screen.fill((255, 255, 255))
                        draw_routers(solve.variables, screen)
                        pygame.display.update()
                        drag_index = -1
            if event.type == MOUSEMOTION and drag_index >= 0:
                solve.variables[drag_index].set_location(pygame.mouse.get_pos())
                screen.fill((255, 255, 255))
                draw_routers(solve.variables, screen)
                pygame.display.update()


        screen.fill((255, 255, 255))
        draw_routers(solve.variables, screen)
        clock.tick(30)
        pygame.display.update()
