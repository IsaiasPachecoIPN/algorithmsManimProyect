from manim import *
from utils import *

#Default values
DEFAULT_BUFF = 0.25
Y_DEFAULT_COORD = DEFAULT_BUFF * 3
DEFAULT_BOX_HEIGHT = 1
DEFAULT_BOX_WIDTH = 3

DEFAULT_ELEM_COLOR = "#00AAFF"
DEFAULT_ELEM_LIST_COLOR = "#F6CECE"
DEFAULT_SELECTED_COLOR = "#878787"
DEFAULT_ENGAGED_COLOR = "#00FF04"

DEFAULT_FRAME_WIDTH = 30


#Gale Shapley init values
dics = [{},{}]
galeShapleyGroupOne = dics[0]
galeShapleyGroupTwo = dics[1]

def readInitData( file ):
    """
    Function to read the initial data from a file
    (param) file: File
    """
    with open(file, "r") as f:
        data = f.readlines()
        counter = 0
        for line in data:
            line = line.strip()
            if (line == "*"):
                counter += 1
            elif ("#" in line):
                continue
            else:
                element, preferences = line.split(";") 
                preferences = list(preferences.strip().split(","))
                dics[counter][element] = preferences


def isWomanSingle( w, arr_solteras):
    """
    Function to return if a woman is in the single array
    w - woman
    arr_solteras - single array
    """
    return True if w in arr_solteras else False

def assignMandWToBeEngaged(m,w, lista_asignaciones):
    """
    Function to assign w and m to be engaged
    m - man
    w - woman
    lista_asignaciones - list of engaged
    """
    lista_asignaciones.append([m, w])

def isSomeManSingle( arr_solteros ):
    """
    Function to return if man is single
    arr_solteros - single array
    """
    return True if len(arr_solteros) > 0 else False

def addSingleManToArr( man, arr_solteros ):
    """
    Function to add a man to the single array
    man - man
    arr_solteros - single array
    """
    arr_solteros.append(man)

def getPreferenceOfElements(group_id, elem_1, elem_2):
    """
    Function to return the preference of elem_1 over elem_2
    """
    #print("group_id: ", group_id)
    #print("elem_1: ", elem_1)
    #print("elem_2: ", elem_2)
    #Retorna si el elemento 1 esta antes que el elemento 2 en la lista de preferencias del galeShapleyGroupTwo
    return galeShapleyGroupTwo[group_id].index(elem_1) < galeShapleyGroupTwo[group_id].index(elem_2)

def getFianceOfElement(elem_val, lista_asignaciones):
    """
    Function to return the fiance of an element
    """
    for elem in lista_asignaciones:
        if elem[1] == elem_val:
            return elem[0]
    return None

def removeElemFromList(elem, lista):
    """
    Function to remove an element from a list
    """
    return [x for x in lista if x != elem]

def galeShapleyAlgorithm(scene,groupOne, groupTwo):

    """
    Function that executes the Gale Shapley Algorithm over the two groups
    """

    lista_asignaciones = []
    solteras = [key for key in galeShapleyGroupTwo.keys()]
    solteros = [key for key in galeShapleyGroupOne.keys()]

    #print("solteras: ", solteras)
    #print("solteros: ", solteros)

    #Se inicia recorrer la lista de preferencias de cada elemento del grupo 1
    while isSomeManSingle(solteros):
        for m, m_preference_list in galeShapleyGroupOne.items():
            if not isSomeManSingle(solteros):
                break
            #print("m: ", m)
            for w in m_preference_list:
                #print("val: ", val)
                addGSEvalueationPairsAnimation(scene, m, m+w)
                #If w is single, then m and w become engaged
                if isWomanSingle(w, solteras):
                    assignMandWToBeEngaged(m, w, lista_asignaciones)
                    solteras = removeElemFromList(w, solteras)
                    solteros = removeElemFromList(m, solteros)
                    #if m and w are engaged, w is removed from m's preference list
                    galeShapleyGroupOne[m] = removeElemFromList(w, galeShapleyGroupOne[m])
                    addWomanTextAnimation(scene, "Estoy soltera, Ok", w+m)
                    addTextToScene( scene, str(lista_asignaciones))
                    addEngagedAnimation(scene, w, w+m)
                    break
                # If w is not single, then w chooses between m and her fiance
                elif (getPreferenceOfElements(w, m, getFianceOfElement(w, lista_asignaciones))):
                    old_fiance = getFianceOfElement(w, lista_asignaciones)
                    lista_asignaciones.remove([old_fiance, w])
                    assignMandWToBeEngaged(m, w, lista_asignaciones)
                    galeShapleyGroupOne[m] = removeElemFromList(w, galeShapleyGroupOne[m])
                    addWomanTextAnimation(scene, "No eres tu, soy yo", w+old_fiance)
                    addEngagedAnimation(scene, w, w+m, w+old_fiance)
                    solteros = removeElemFromList(m, solteros)
                    addSingleManToArr(old_fiance, solteros)
                    break
                else:
                    #w rejects m
                    addWomanTextAnimation(scene, "Lo siento, ya tengo pareja", w+m)
                    None                

            print("lista_asignaciones: ", lista_asignaciones)
    
def getNextListStartPoint(scence):

    """
        Function to get the next coord point to add the next
        first group list of preferences in the scene
    """

    #Return fistElement x and LastElement y
    firstElement = scence.mobjects[0]
    lastElement = scence.mobjects[-1]
    y_coord =  lastElement.get_y() - ( 1 + firstElement.get_height() - Y_DEFAULT_COORD) 
    #print("y_coord: ", y_coord)
    return [firstElement.get_center()[0], y_coord, 0]

def addGSEvalueationPairsAnimation(scene, elemA, elemB ):

    """
    Function to add the animation over the evaluation of the pairs
    """

    elem_a = getElemByID(elemA, scene)
    elem_b = getElemByID(elemB, scene)

    scene.play(elem_a.animate.set_fill(DEFAULT_SELECTED_COLOR))
    scene.play(elem_b.animate.set_fill(DEFAULT_SELECTED_COLOR))

    scene.play(elem_a.animate(rate_func=there_and_back).rotate(PI/4))    
    scene.play(elem_b.animate(rate_func=there_and_back).rotate(PI/4))

def addElementToScene(scene, elem, nextTo = None, position = DOWN, coords = None):
    
    """
    Function to add an element to the scene
    (param) scene: Scene
    (param) elem: Element
    (param) nextTo: Element
    (param) position: Position
    """

    if nextTo == None:
        scene.play(GrowFromCenter(elem.getElemento().getFigure()))
    elif coords != None:
        scene.play(GrowFromCenter(elem.getElemento().getFigure().move_to(coords)))
    else:
        scene.play(GrowFromCenter(elem.getElemento().getFigure().next_to(nextTo, position)))

    first_elem = elem.lista_preferencias[0].getFigure()   
    scence_lenght = len(scene.mobjects)
    last_mobject = scene.mobjects[scence_lenght-1]

    scene.play(GrowFromCenter(first_elem.next_to(last_mobject, RIGHT)))

    #mostrar coordenadas de firs_elem
    for i in range(1,len(elem.lista_preferencias)):
        scence_lenght = len(scene.mobjects)
        #scene.wait(1)
        new_mobject = elem.lista_preferencias[i].getFigure()
        last_mobject = scene.mobjects[scence_lenght-1]
        scene.play(GrowFromCenter(new_mobject.next_to(last_mobject.get_center(), DOWN, buff = Y_DEFAULT_COORD)))
        #Print y coord of new_mobject
        #print("new_mobject: ", new_mobject.get_y())


def showAllMobjectIDs(scene):
    for elem in scene.mobjects:
        #Si el elemento es de tipo VGroup se obtiene el elemnto [1]
        if( type (elem) == VGroup):
            print("elem: ", elem.name)


def getElemByID(id, scene):
    """
    Function to get an element by id from the scene mobjects
    """
    for elem in scene.mobjects:
        if elem.name == id:
            return elem
    return None

def addTextToScene(scene, text):
    text_container = getElemByID("txtEngaged", scene)
    #Se reemplaza el texto del text_container
    text_container[0] = Text("Asignaciones: "+text).next_to( getElemByID("amyzeus", scene), UP)
    scene.play(Write(text_container[0]))
    #scene.play(text_container.animate.write(text)
    #mover el contenedor 
    #scene.play(text_container.animate.move_to(getElemByID("amyyancey", scene).get_center()))

def addWomanTextAnimation(scene, text, nextToId):
    text_container = VGroup()
    text = Text(text)
    text_container.add(text)
    scene.add(text_container.next_to( getElemByID(nextToId, scene), RIGHT))
    #Remover el texto animado despues de 2 segundos
    scene.play(Write(text_container[0]))
    scene.play(FadeOut(text_container, run_time=2))

def addEngagedAnimation(scene, elemA, elemB, oldElem = None):

    elem_a = getElemByID(elemA, scene)
    elem_b = getElemByID(elemB, scene)
    if oldElem != None:
        elem_c = getElemByID(oldElem, scene)

    if oldElem != None:
        scene.play(elem_c.animate.set_fill(DEFAULT_ELEM_LIST_COLOR))

    scene.play(elem_a.animate.set_fill(DEFAULT_ENGAGED_COLOR))
    scene.play(elem_b.animate.set_fill(DEFAULT_ENGAGED_COLOR))
    
    scene.play(elem_a.animate(rate_func=there_and_back).shift(RIGHT))    
    scene.play(elem_b.animate(rate_func=there_and_back).shift(RIGHT))


def createScence(scene, galeShapleyGroupOne, galeShapleyGroupTwo):

    galeShapleyGroupOneKeys = [key for key in galeShapleyGroupOne.keys()]

    for idx, m in enumerate(galeShapleyGroupOne.keys()):
        if idx == 0:
            elem = construirListaPreferencias(m, galeShapleyGroupOne[m])
        else:
            elem = construirListaPreferencias(m, galeShapleyGroupOne[m], DEFAULT_ELEM_LIST_COLOR)

        if idx == 0:
            addElementToScene(scene, elem)
        else:
            addElementToScene(scene, elem, scene.mobjects[idx-1], coords=getNextListStartPoint(scene))

    for idx, m in enumerate(galeShapleyGroupTwo.keys()):
        if idx == 0:
            elem = construirListaPreferencias(m, galeShapleyGroupTwo[m], DEFAULT_ELEM_LIST_COLOR)
        else:
            elem = construirListaPreferencias(m, galeShapleyGroupTwo[m], DEFAULT_ELEM_LIST_COLOR)

        #print("ElemCoords: ", getElemByID(galeShapleyGroupOneKeys[idx]+m, scene))
        go_key = galeShapleyGroupOneKeys[idx]
        addElementToScene(scene, elem, getElemByID(go_key+galeShapleyGroupOne[go_key][0], scene), position=RIGHT)

    #Se agrega el texto para representar las asignaciones
    text_container = VGroup()
    text_container.name = "txtEngaged"
    text = Text("Asignaciones: ")
    text_container.add(text)
    scene.add(text_container.next_to( getElemByID("xavieramy", scene), UP))

class CreateScene(MovingCameraScene):
    def construct(self):

        try:
            readInitData("inputdata")
            self.camera.frame.set(width = DEFAULT_FRAME_WIDTH)
            self.camera.frame.shift(RIGHT * (DEFAULT_FRAME_WIDTH/2) - (DEFAULT_BOX_WIDTH))
            self.camera.frame.shift(DOWN* (self.camera.frame.get_height()/4) + DEFAULT_BOX_HEIGHT) 
            #numberplane = NumberPlane()
            #self.add(numberplane)
            createScence(self, galeShapleyGroupOne, galeShapleyGroupTwo)
            galeShapleyAlgorithm(self, galeShapleyGroupOne, galeShapleyGroupTwo)
        except:
            print("Error al leer el archivo")
            