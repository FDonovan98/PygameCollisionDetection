import pygame
import sys
import math

background_colour = (0, 0, 0)
(width, height) = (800, 600)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Project')
screen.fill(background_colour)

pygame.display.flip()

lineColor = (255, 255, 255)
vertices = []
triangles = []
allowInput = True

def GetEvents():
    global vertices
    global triangles
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
                triangles = []
                allowInput = True
            if event.key == pygame.K_c and len(vertices) > 2:
                allowInput = False

def CalculateTriAreas(vertices):
    area = vertices[0][0] * (vertices[2][1] - vertices[1][1])
    area += vertices[1][0] * (vertices[0][1] - vertices[2][1])
    area += vertices[2][0] * (vertices[1][1] - vertices[0][1])

    return abs(area)

class Triangle:
    area = 0
    distToTargetVert = [0] * 2
    targetVert = [0] * 2
    def __init__(self, rootVert):
        self.rootVert = rootVert

    def CalculateArea(self):
        self.area = CalculateTriAreas((self.rootVert, self.targetVert[0], self.targetVert[1]))

def CalculateTris():
    global triangles

    i = 0
    for rootVertex in vertices:
        triangles.append(Triangle(rootVertex))

        for targetVertex in vertices:
            if rootVertex != targetVertex:
                dist = math.sqrt((rootVertex[0] - targetVertex[0]) ** 2 + (rootVertex[1] - targetVertex[1]) ** 2)
                if dist > triangles[-1].distToTargetVert[0]:
                    triangles[-1].targetVert[0] = targetVertex
                    triangles[-1].distToTargetVert[0] = dist
                elif dist > triangles[-1].distToTargetVert[1]:
                    triangles[-1].targetVert[1] = targetVertex
                    triangles[-1].distToTargetVert[1] = dist

        triangles[-1].CalculateArea()
            
        i += 1

def DrawShape():
    global vertices
    global allowInput

    i = 0
    for element in vertices:
        if i > 0:
            pygame.draw.line(screen, lineColor, vertices[i-1], vertices[i])
        
        i = i + 1

    for element in triangles:
        pygame.draw.polygon(screen, (0, 0, 255), (element.rootVert, element.targetVert[0], element.targetVert[1]))

    if not allowInput:
        pygame.draw.line(screen, lineColor, vertices[0], vertices[-1])
        CalculateTris()
        
def CalculateIfMouseIsInTri():
    global vertices

    mousePos = pygame.mouse.get_pos()

    i = 0
    for element in triangles:
        mouseArea = CalculateTriAreas((mousePos, element.rootVert, element.targetVert[0]))
        mouseArea += CalculateTriAreas((mousePos, element.rootVert, element.targetVert[1]))
        mouseArea += CalculateTriAreas((mousePos, element.targetVert[0], element.targetVert[1]))

        if element.area == mouseArea:
            return True

        i = i + 1

    return False

def DoMouseCollision():
    global vertices
    global allowInput

    if CalculateIfMouseIsInTri():
        pygame.draw.circle(screen, (255, 0, 0), pygame.mouse.get_pos(), 5)
    else:
        pygame.draw.circle(screen, (0, 255, 0), pygame.mouse.get_pos(), 5)

running = True
while running:
    screen.fill(background_colour)

    GetEvents()
    DrawShape()
    if not allowInput:
        DoMouseCollision()

    pygame.display.update()

pygame.quit()
sys.exit()