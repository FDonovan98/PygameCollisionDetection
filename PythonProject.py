import pygame
import sys

background_colour = (0, 0, 0)
(width, height) = (800, 600)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Project')
screen.fill(background_colour)

pygame.display.flip()

lineColor = (255, 255, 255)
vertices = []
triAreas = []
allowInput = True

def GetEvents():
    global vertices
    global triAreas
    global allowInput

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            global running
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and allowInput:
            vertices.append(pygame.mouse.get_pos())
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                vertices = []
                triAreas = []
                allowInput = True
            if event.key == pygame.K_c and len(vertices) > 2:
                allowInput = False

def DrawShape():
    global vertices
    global allowInput

    i = 0
    for element in vertices:
        if i > 0:
            pygame.draw.line(screen, lineColor, vertices[i-1], vertices[i])
        
        i = i + 1

    if not allowInput:
        pygame.draw.line(screen, lineColor, vertices[0], vertices[-1])

def CalculateTriAreas(vertices):
    area = vertices[0][0] * (vertices[2][1] - vertices[1][1])
    area += vertices[1][0] * (vertices[0][1] - vertices[2][1])
    area += vertices[2][0] * (vertices[1][1] - vertices[0][1])

    return abs(area)

def CalculateIfMouseIsInTri():
    global triAreas
    global vertices

    mousePos = pygame.mouse.get_pos()

    i = 0
    for element in triAreas:
        mouseArea = CalculateTriAreas((mousePos, vertices[i * 3], vertices[i * 3 + 1]))
        mouseArea += CalculateTriAreas((mousePos, vertices[i * 3], vertices[i * 3 + 2]))
        mouseArea += CalculateTriAreas((mousePos, vertices[i * 3 + 1], vertices[i * 3 + 2]))

        if element == mouseArea:
            return True

        i = i + 1

    return False

def DoMouseCollision():
    global vertices
    global triAreas
    global allowInput

    if not allowInput:
        if len(triAreas) == 0:
            i = 0
            while i < int(round(len(vertices) / 3)):
                triAreas.append(CalculateTriAreas((vertices[i * 3], vertices[i * 3 + 1], vertices[i * 3 + 2])))
                i += 1

        if CalculateIfMouseIsInTri():
            pygame.draw.circle(screen, (255, 0, 0), pygame.mouse.get_pos(), 5)
        else:
            pygame.draw.circle(screen, (0, 255, 0), pygame.mouse.get_pos(), 5)

running = True
while running:
    screen.fill(background_colour)

    GetEvents()
    DrawShape()
    DoMouseCollision()

    pygame.display.update()

pygame.quit()
sys.exit()