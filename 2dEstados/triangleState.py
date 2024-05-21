import sys
import math
from enum import Enum
from OpenGL.GL import *
from OpenGL.GLU import *
from state import State
from geometries import Object

# controle de estados dentro do estado de triângulo
class States(Enum):
    INIT_DRAW = 1
    FINISH_DRAW = 2

# estado inicial de desenho
currentState = States.INIT_DRAW

currentPoints = []

# ========================================================
# TriangleState - ESTADO DE DESENHAR TRIÂNGULO
# ========================================================
# possibilita desenhar um triângulo e ver o desenho em tempo real
# no fim, o triângulo é adicionado à lista de objetos do programa

class TriangleState(State):
    def __init__(self, manageStates):
        super().__init__(manageStates)
        # triângulo temporário para ver o que está sendo desenhado em tempo real
        self.tempTriangle = Object("triangle", self.manageStates.color, self.manageStates.style, self.manageStates.lineWidth)


    # ========================================================
    # CALLBACKS - MOUSE
    # ========================================================

    # click do mouse quando pressiona e quando solta
    def MouseClick(self, event, x, y):
        global currentState, currentPoints
        triangulo = Object("triangle", self.manageStates.color, self.manageStates.style, self.manageStates.lineWidth)

        if event.LeftDown():
            print("TriangleState - Click Esquerdo") 

        elif event.LeftUp():
            print("TriangleState - Soltou Click Esquerdo") 

            # verifica qual é o estado atual do estado de triângulo
            if currentState == States.INIT_DRAW:
                # primeiro ponto
                currentPoints.append((x, y))

                # troca o estado dentro do estado de triângulo, para fazer as ações de finalização do desenho
                currentState = States.FINISH_DRAW

            elif currentState == States.FINISH_DRAW:
                # segundo ponto
                currentPoints.append((x, y))

                # terceiro ponto
                dist = currentPoints[1][0] - currentPoints[0][0]
                currentPoints.append((currentPoints[0][0] - dist, currentPoints[1][1]))

                # todos os pontos
                triangulo.points = currentPoints
                triangulo.selected = True
                self.manageStates.objects.append(triangulo)
                self.tempTriangle.points = []

                currentPoints = []
                
                # se o estado geral do progama continuasse no de triângulo, 
                # o estado dentro do estado de triângulo deveria voltar ao inicial,
                # para que mais triângulos pudessem ser desenhados
                #currentState = States.INIT_DRAW

                # troca o estado geral do programa para o estado de "espera"
                self.manageStates.setState(self.manageStates.getIdleState())

    # mouse em movimento pressionado
    def MouseMotion(self, x, y):
        print("TriangleState - MouseMotion") 
        pass

    # mouse em movimento solto
    def MousePassiveMotion(self, x, y):
        print("TriangleState - MousePassiveMotion") 

        global currentState, currentPoints

        if currentState == States.FINISH_DRAW:
            # copia a lista de pontos atual para evitar modificação direta
            tempPoints = currentPoints.copy()
            # adiciona o ponto atual do mouse à lista temporária
            tempPoints.append((x, y))

            dist = tempPoints[1][0] - tempPoints[0][0]

            tempPoints.append((tempPoints[0][0] - dist, tempPoints[1][1]))

            # atualiza os pontos do triângulo temporário
            self.tempTriangle.points = tempPoints
    
    # roda do mouse
    def onMouseWheel(self, event):
        print("TriangleState - onMouseWheel")
        if self.ctrl_pressed:
            rotation = event.GetWheelRotation()
            self.manageStates.zoom -= rotation / event.GetWheelDelta() * 0.1

    # ========================================================
    # DRAW - desenhos
    # ========================================================

    def draw(self):
        print("TriangleState - Draw") 
        super().draw()
        self.tempTriangle.draw()

