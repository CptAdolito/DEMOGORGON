import random
import sys
import os


'''Función encargada de crear un tablero cuadrado de tamaño size
    y rellenarlo con el valor value'''

def create_board(size, value):

    board = []

    for i in range(size):
        row = []

        for j in range(size):
            row.append(value)

        board.append(row)

    return board



'''Función encargada de imprimir el tablero'''

def print_board(board):

    for row in board:

        print('|', ' | '.join(map(str, row)), '|')



'''Función encargada de asignar la posición del agujero
    de forma aleatoria'''

def assign_ones(board):

    row = random.randint(0, size-1)
    col = random.randint(0, size-1)

    if board[row][col] != 'A':
        board[row][col] = 'A'

    else:
        assign_ones(board)



'''Función encargada de asignar la posición del demogorgon
    de forma aleatoria'''

def assign_demogorgon(board):

    row = random.randint(0, size-1)
    col = random.randint(0, size-1)

    if board[row][col] != 'A' and board[row][col] != 'D':

        board[row][col] = 'D'

    else:
        assign_demogorgon(board)



'''Función encargada de asignar la posición de la salida
    de forma aleatoria'''

def assign_exit(board):

    row = random.randint(0, size-1)
    col = random.randint(0, size-1)

    if board[row][col] != 'A' and board[row][col] != 'D' and board[row][col] != 'S':

        board[row][col] = 'S'

    else:
        assign_exit(board)



'''Función que no permite que haya un agujero, demogorgon o salida en una esquina
    lo hago para evitar que se quede la casilla atrapada'''

def quitar_esquinas(board):

    if board[size-1][0] == 'A' or board[size-1][size-1] == 'S' or board[size-1][0] == 'D':
        return True

    if board[0][size-1] == 'A' or board[0][size-1] == 'S' or board[0][size-1] == 'D':
        return True

    if board[size-1][size-1] == 'A' or board[size-1][size-1] == 'S' or board[size-1][size-1] == 'D':
        return True

    return False
        


'''Función para disparar'''

def disparar(posicion, shots):

    entrada = input('¿Quieres disparar? (si/no) ')
    entrada = entrada.upper()

    if entrada == 'SI':
        if shots < 1:
            
            shots += 1
            entrada = input('¿A dónde quieres disparar? (arriba/abajo/derecha/izquierda) ')
            entrada = entrada.upper()

            if entrada == 'ARRIBA' and board[posicion[0]-1][posicion[1]] == 'D':
                print('Has matado al demogorgon')
                return False, shots
            
            elif entrada == 'ABAJO' and board[posicion[0]+1][posicion[1]] == 'D':
                print('Has matado al demogorgon')
                return False, shots
            
            elif entrada == 'DERECHA' and board[posicion[0]][posicion[1]+1] == 'D':
                print('Has matado al demogorgon')
                return False, shots
            
            elif entrada == 'IZQUIERDA' and board[posicion[0]][posicion[1]-1] == 'D':
                print('Has matado al demogorgon')
                return False, shots

            else:
                print('Has fallado')
                return True, shots
        else:
            print('No tienes más balas')
            return True, shots
    else:
        return True, shots



'''Función para que el jugador se mueva'''

def movement(posicion):

    correcto = False

    #Mientras no se introduzca una dirección correcta, se seguirá pidiendo
    while correcto == False:

        entrada = input('Indica la dirección a la que quieres moverte (salir): ')
        entrada = entrada.upper()

        if entrada == 'IZQUIERDA':

            if posicion[1] == 0:
                print('No puedes salirte del tablero')
                print('\n')
            else:
                posicion[1] -= 1
                correcto = True
                return posicion

        elif entrada == 'DERECHA':

            if posicion[1] == size-1:
                print('No puedes salirte del tablero')
                print('\n')
            else:
                posicion[1] += 1
                correcto = True
                return posicion

        elif entrada == 'ARRIBA':

            if posicion[0] == 0:
                print('No puedes salirte del tablero')
                print('\n')
            else:
                posicion[0] -= 1
                correcto = True
                return posicion

        elif entrada == 'ABAJO':

            if posicion[0] == size-1:
                print('No puedes salirte del tablero')
                print('\n')
            else:
                posicion[0] += 1
                correcto = True
                return posicion

        elif entrada == 'SALIR':
            sys.exit()

        else:
            print('No has introducido una dirección válida')
            print('\n')
 


'''Función que mira si el jugador ha caido en la casilla un agujero, en el demogorgon o en la salida'''

def mirar(board_play, pos):

    posX = pos[0]
    posY = pos[1]

    if 'A' in board_play[posX][posY]:
        print('Has caido en un agujero')
        sys.exit()
        
    elif 'D' in board_play[posX][posY]:
        print('Has caido en el demogorgon')
        sys.exit()

    elif 'S' in board_play[posX][posY]:
        print('Has llegado a la salida')
        sys.exit()

    else:
        return board_play



'''Función que mira alrededor de la casilla en la que se encuentra el jugador
    y si hay un agujero, demogorgon o salida, se añade a la casilla en la que se encuentra
    el jugador un B (brisa), C (cosquilleo) o L (luz) respectivamente'''

def mirar_alrededor(board_play, pos, board):

    try:
        if board[pos[0]-1][pos[1]] == 'A' and pos[0]-1 >= 0 and pos[1] >= 0:
            board_play[pos[0]][pos[1]].add('B')

        elif board[pos[0]-1][pos[1]] == 'D' and pos[0]-1 >= 0 and pos[1] >= 0:
            board_play[pos[0]][pos[1]].add('C')

        elif board[pos[0]-1][pos[1]] == 'S' and pos[0]-1 >= 0 and pos[1] >= 0:
            board_play[pos[0]][pos[1]].add('L')

    except:
        pass

    try:
        if board[pos[0]+1][pos[1]] == 'A' and pos[0]+1 >= 0 and pos[1] >= 0:
            board_play[pos[0]][pos[1]].add('B')

        elif board[pos[0]+1][pos[1]] == 'D' and pos[0]+1 >= 0 and pos[1] >= 0:
            board_play[pos[0]][pos[1]].add('C')

        elif board[pos[0]+1][pos[1]] == 'S' and pos[0]+1 >= 0 and pos[1] >= 0:
            board_play[pos[0]][pos[1]].add('L')

    except:
        pass

    try:
        if board[pos[0]][pos[1]-1] == 'A' and pos[0] >= 0 and pos[1]-1 >= 0:
            board_play[pos[0]][pos[1]].add('B')

        elif board[pos[0]][pos[1]-1] == 'D' and pos[0] >= 0 and pos[1]-1 >= 0:
            board_play[pos[0]][pos[1]].add('C')

        elif board[pos[0]][pos[1]-1] == 'S' and pos[0] >= 0 and pos[1]-1 >= 0:
            board_play[pos[0]][pos[1]].add('L')

    except:
        pass

    try:
        if board[pos[0]][pos[1]+1] == 'A' and pos[0] >= 0 and pos[1]+1 >= 0:
            board_play[pos[0]][pos[1]].add('B')

        elif board[pos[0]][pos[1]+1] == 'D' and pos[0] >= 0 and pos[1]+1 >= 0:
            board_play[pos[0]][pos[1]].add('C')

        elif board[pos[0]][pos[1]+1] == 'S' and pos[0] >= 0 and pos[1]+1 >= 0:
            board_play[pos[0]][pos[1]].add('L')

    except:
        pass

    return board_play



'''Función que asigna a cada casilla un número dependiendo de lo que sienta el jugador'''

def check_board(board, pos):
    
    #Sientes cosquillas, luz y brisa
    if 'C' in board[pos[0]][pos[1]] and 'L' in board[pos[0]][pos[1]] and 'B' in board[pos[0]][pos[1]]:
        board[pos[0]][pos[1]] = '1'
    
    #Sientes cosquillas y luz
    elif 'C' in board[pos[0]][pos[1]] and 'L' in board[pos[0]][pos[1]]:
        board[pos[0]][pos[1]] = '2'
    
    #Sientes cosquillas y brisa
    elif 'C' in board[pos[0]][pos[1]] and 'B' in board[pos[0]][pos[1]]:
        board[pos[0]][pos[1]] = '3'

    #Sientes luz y brisa  
    elif 'L' in board[pos[0]][pos[1]] and 'B' in board[pos[0]][pos[1]]:
        board[pos[0]][pos[1]] = '4'
    
    #Sientes cosquillas
    elif 'C' in board[pos[0]][pos[1]]:
        board[pos[0]][pos[1]] = '5'
    
    #Sientes luz
    elif 'L' in board[pos[0]][pos[1]]:
        board[pos[0]][pos[1]] = '6'
    
    #Sientes brisa
    elif 'B' in board[pos[0]][pos[1]]:
        board[pos[0]][pos[1]] = '7'
    
    #No sientes nada
    else:
        board[pos[0]][pos[1]] = '0'
    

    return board



'''Función que dada una posición, nos devolverá una lista con las posiciones de las
    casillas alrededor que aún no hemos pisado de la posición dada'''

def posiciones_alrededor(pos):

    pos_alrededor = []

    try:
        if pos[0]-1 >= 0 and pos[1] >= 0 and board_play[pos[0]-1][pos[1]] == 'X':
            pos_alrededor.append((pos[0]-1, pos[1]))

    except:
        pass

    try:
        if pos[0]+1 >= 0 and pos[1] >= 0 and board_play[pos[0]+1][pos[1]] == 'X':
            pos_alrededor.append((pos[0]+1, pos[1]))

    except:
        pass

    try:
        if pos[0] >= 0 and pos[1]-1 >= 0 and board_play[pos[0]][pos[1]-1] == 'X':
            pos_alrededor.append((pos[0], pos[1]-1))

    except:
        pass

    try:
        if pos[0] >= 0 and pos[1]+1 >= 0 and board_play[pos[0]][pos[1]+1] == 'X':
            pos_alrededor.append((pos[0], pos[1]+1))

    except:
        pass

    return pos_alrededor


'''Función que dada una posición, nos devolverá una lista con las posiciones de las
    casillas alrededor de la posición dada'''

def posiciones_alrededor_2(pos):

    pos_alrededor = []

    try:
        if pos[0]-1 >= 0 and pos[1] >= 0:
            pos_alrededor.append((pos[0]-1, pos[1]))

    except:
        pass

    try:
        if pos[0]+1 >= 0 and pos[1] >= 0:
            pos_alrededor.append((pos[0]+1, pos[1]))

    except:
        pass

    try:
        if pos[0] >= 0 and pos[1]-1 >= 0:
            pos_alrededor.append((pos[0], pos[1]-1))

    except:
        pass

    try:
        if pos[0] >= 0 and pos[1]+1 >= 0:
            pos_alrededor.append((pos[0], pos[1]+1))

    except:
        pass

    return pos_alrededor

'''Función que añade a la base de conocimiento la información que se obtiene de la posición
    en la que se encuentra el jugador'''

def knowledge(KB, board_play, pos):
    
    pos_alrededor = posiciones_alrededor(pos)

            
    if board_play[pos[0]][pos[1]] == '0':
        KB['ND'].append(pos_alrededor)
        KB['NS'].append(pos_alrededor)
        KB['NA'].append(pos_alrededor)
        
    elif board_play[pos[0]][pos[1]] == '1':
        if KB['A'] == []:
            pass
        else:
            try:
                KB['A'].append(pos_alrededor)
            except:
                pass

        if KB['S'] == []:
            pass
        else:
            try:
                KB['S'].append(pos_alrededor)
            except:
                pass

        if KB['D'] == []:
            pass
        else:
            try:
                KB['D'].append(pos_alrededor)
            except:
                pass

    elif board_play[pos[0]][pos[1]] == '2':
        if KB['D'] == []:
            pass
        else:
            try:
                KB['D'].append(pos_alrededor)
            except:
                pass
        if KB['S'] == []:
            pass
        else:
            try:
                KB['S'].append(pos_alrededor)
            except:
                pass

        KB['NA'].append(pos_alrededor)

    elif board_play[pos[0]][pos[1]] == '3':
        if KB['D'] == []:
            pass
        else:
            try:
                KB['D'].append(pos_alrededor)
            except:
                pass
        KB['NS'].append(pos_alrededor)
        if KB['A'] == []:
            pass
        else:
            try:
                KB['A'].append(pos_alrededor)
            except:
                pass

    elif board_play[pos[0]][pos[1]] == '4':
        KB['ND'].append(pos_alrededor)
        if KB['S'] == []:
            pass
        else:
            try:
                KB['S'].append(pos_alrededor)
            except:
                pass
        if KB['A'] == []:
            pass
        else:
            try:
                KB['A'].append(pos_alrededor)
            except:
                pass

    elif board_play[pos[0]][pos[1]] == '5':
        if KB['D'] == []:
            pass
        else:
            try:
                KB['D'].append(pos_alrededor)
            except:
                pass
        KB['NS'].append(pos_alrededor)
        KB['NA'].append(pos_alrededor)

    elif board_play[pos[0]][pos[1]] == '6':
        KB['ND'].append(pos_alrededor)
        if KB['S'] == []:
            pass
        else:
            try:
                KB['S'].append(pos_alrededor)
            except:
                pass
        KB['NA'].append(pos_alrededor)

    elif board_play[pos[0]][pos[1]] == '7':
        KB['ND'].append(pos_alrededor)
        KB['NS'].append(pos_alrededor)
        if KB['A'] == []:
            pass
        else:
            try:
                KB['A'].append(pos_alrededor)
            except:
                pass

    return KB



'''Función que junta las posiciones de la base de conocimiento 
    y que elimina las posiciones repetidas de la base de conocimiento.

    Además, si hay una posición que se repite en las posibles posiciones de 
    agujero, salida y demogorgon; podemos confirmar que en esa posición
    está el agujero, la salida o el demogorgon'''

def eliminar_repetidos(KB):

    t = 0

    for i in KB:

        #Unión de las nuevas posiciónes
        try:
            KB[i] = [KB[i][0] + KB[i][1]]

        except:
            pass
        
        #Lógica de repetición
        try:
            for j in range(0, len(KB[i][0])):
                
                if t < 3:
                    if KB[i][0].count(KB[i][0][j]) > 1:
                        KB[i][0] = [KB[i][0][j]]
                     
        except:
            pass  

        t += 1

        #Eliminación de repetidos
        try:
            KB[i] = [list(set(KB[i][0]))]
        except:
            pass

    return KB



'''Si hay una posición en la que podría estar el agujero, la salida o el demogorgon
    y en la que no puede estar, podemos confirmar que en esa posición no está el agujero,
    la salida o el demogorgon'''

def eliminar_dobles(KB):

    try: 
        for i in KB['A'][0]:

            if i in KB['NA'][0]:

                try:
                    KB['A'][0].remove(i)

                except:
                    pass

    except:
        pass
   
    try:
        for i in KB['D'][0]:

            if i in KB['ND'][0]:
                try:
                    KB['D'][0].remove(i)
                except:
                    pass
    except:
        pass

    try:
        for i in KB['S'][0]:
            if i in KB['NS'][0]:
                try:
                    KB['S'][0].remove(i)
                except:
                    pass

    except:
        pass

    return KB



'''Función que comprueba que como estamos en una casilla segura, no puede haber
    un agujero, una salida o un demogorgon y elimina las posiciones si estaban en la 
    base de conocimiento como posibles casillas de agujero, salida o demogorgon y
    añade las posiciones en la base de conocimiento como sitios donde seguro que no
    hay ningún peligro'''

def check_pos(KB, board_play, pos):

    if board_play[pos[0]][pos[1]] in ['0', '1', '2', '3', '4', '5', '6', '7']:
        try:
            KB['D'][0].remove(tuple(pos))
        except:
            pass

        try:
            KB['S'][0].remove(tuple(pos))
        except:
            pass

        try:
            KB['A'][0].remove(tuple(pos))
        except:
            pass

        try:
            KB['ND'].append([tuple(pos)])
        except:
            pass

        try:
            KB['NS'].append([tuple(pos)])
        except:
            pass

        try:
            KB['NA'].append([tuple(pos)])
        except:
            pass

        try:
            KB = eliminar_repetidos(KB)
        except:
            pass

    return KB



'''Función que comprueba si en la base de conocimientos de posibles agujeros,
    salidas y demogorgones hay solo una posición, entonces podemos confirmar que
    está ahí'''

def SDA(KB, board_play):

    try:    
        if len(KB['D'][0]) == 1:
            x = KB['D'][0][0][0]
            y = KB['D'][0][0][1]
            board_play[x][y] = 'D'
            KB['D'] = (x,y)
            
            try:
                if (x,y) in KB['A'][0]:
                    KB['A'][0].remove((x,y))
                if (x,y) in KB['S'][0]:
                    KB['S'][0].remove((x,y))

            except:
                pass

    except:
        pass
    
    try:
        if len(KB['S'][0]) == 1:
            x = KB['S'][0][0][0]
            y = KB['S'][0][0][1]
            board_play[x][y] = 'S'
            KB['S'] = (x,y)

            try:
                if (x,y) in KB['A'][0]:
                    KB['A'][0].remove((x,y))
                if (x,y) in KB['D'][0]:
                    KB['D'][0].remove((x,y))

            except:
                pass
            
    except:
        pass

    try:
        if len(KB['A'][0]) == 1:
            x = KB['A'][0][0][0]
            y = KB['A'][0][0][1]
            board_play[x][y] = 'A'
            KB['A'] = (x,y)

            try:
                if (x,y) in KB['S'][0]:
                    KB['S'][0].remove((x,y))
                if (x,y) in KB['D'][0]:
                    KB['D'][0].remove((x,y))

            except:
                pass
        
    except:
        pass
    
    x = [KB, board_play]

    return x



'''Función que comprueba si en la base de conocimientos e
    informa de lo que se sabe y de las posibles posiciones
    de agujero, salida y demogorgon
    
    Informa también de la sensación en la casilla actual'''

def info(KB, pos):

    if KB['D'] != []:

        try:
            if len(KB['D'][0]) > 0:
                print('El demogorgon puede estar en: ', KB['D'][0])

        except:
            pass

        try:
            if len(KB['ND'][0]) > 0:
                print('El demogorgon NO puede estar en:', KB['ND'][0])

        except:
            pass

    if KB['S'] != []:

        try:
            if len(KB['S'][0]) > 0:
                print('La salida puede estar en: ', KB['S'][0])
        except:
            pass

        try:
            if len(KB['NS'][0]) > 0:
                print('La salida NO puede estar en: ', KB['NS'][0])
        except:
            pass

    if KB['A'] != []:

        try:
            if len(KB['A'][0]) > 0:
                print('El agujero puede estar en: ', KB['A'][0])
        except:
            pass

        try:
            if len(KB['NA'][0]) > 0:
                print('El agujero NO puede estar en: ', KB['NA'][0])
        except:
            pass


    print('\n')

    if board_play[pos[0]][pos[1]] == '0':
        print('No sientes nada')

    elif board_play[pos[0]][pos[1]] == '1':
        print('Sientes una ligera brisa, cosquilleo y ves algo de luz')

    elif board_play[pos[0]][pos[1]] == '2':
        print('Sientes cosquilleo y ves algo de luz')

    elif board_play[pos[0]][pos[1]] == '3':
        print('Sientes una ligera brisa y cosquilleo')

    elif board_play[pos[0]][pos[1]] == '4':
        print('Sientes una ligera brisa y ves algo de luz')

    elif board_play[pos[0]][pos[1]] == '5':
        print('Sientes un cosquilleo')

    elif board_play[pos[0]][pos[1]] == '6':
        print('Ves algo de luz')

    elif board_play[pos[0]][pos[1]] == '7':
        print('Sientes una ligera brisa')



'''Función que pide al usuario el tamaño del tablero y lo devuelve
    como entero y mayor a 2'''

def tamaño():

    while True:

        try:
            size = int(input('Ingrese el tamaño del tablero: '))

            if size > 2:
                break

            else:
                print('El tamaño del tablero debe ser mayor a 2')

        except:
            print('Ingrese un número entero')

    return size



'''Si se inicia en la terminal. Se va limpiando la pantalla
    es meramente estético'''

def clear_terminal():

    os.system('cls' if os.name == 'nt' else 'clear')



'''MAIN'''

if __name__ == '__main__':


    print('Bienvenido al juego de la demogorgon')
    size = tamaño()

    '''Base de conocimientos D = demogorgon, S = salida, A = agujero
        ND = no demogorgon, NS = no salida, NA = no agujero'''
    KB = {'D':[[]], 'S':[[]], 'A':[[]], 'ND':[[]], 'NS':[[]], 'NA':[[]]}


    '''Creación del tablero de forma correcta'''
    while True:
        board = create_board(size, (0))
        assign_ones(board)
        assign_demogorgon(board)
        assign_exit(board)
        esquinas = quitar_esquinas(board)
        if board[0][0] == 0 and esquinas == False:
            break


    #Disparo
    shots = 0

    #Demogorgon vivo o muerto
    ESTADO = True

    #Camino recorrido
    CAMINO = []


    '''Inicio de la partida'''

    #Casilla que ve el jugador
    board_play = create_board(size, 'X')

    #Posición inicial del jugador
    pos = [0, 0]

    #La metemos en el camino recorrido
    y = pos.copy()
    CAMINO.append(y)


    '''Comprobación del tablero'''
    board_play[pos[0]][pos[1]] = {board[pos[0]][pos[1]]}
    board_play = mirar(board_play, pos)
    print('\n')
    board_play = mirar_alrededor(board_play, pos, board)
    board_play = check_board(board_play, pos)

    '''Funciones lógicas'''
    KB = knowledge(KB, board_play, pos)
    KB = eliminar_repetidos(KB)
    KB = check_pos(KB, board_play, pos)
    KB = eliminar_dobles(KB)

    #Limpia la terminal
    clear_terminal()

    print('\n')

    '''Información del tablero'''
    info(KB, pos)
    
    print('\n')

    '''Imprime el tablero que ve el jugador'''
    z = board_play[pos[0]][pos[1]]
    if z not in ['1','2','3','4','5','6','7','!']:
        board_play[pos[0]][pos[1]] = '*'

    else:
        board_play[pos[0]][pos[1]] = '!'
        
    print_board(board_play)
    print('\n')
    print('Estás en la posición: ', pos)
    print('\n')

    if board_play[pos[0]][pos[1]] == '*':
            print('No hay peligro en ninguna dirección desconocida')

    if board_play[pos[0]][pos[1]] == '!':

            print('¡Cuidado! Hay peligro')
            print('Ve por una camino que conozcas')

            alrededor = posiciones_alrededor_2(pos)

            peligro = []
            for i in alrededor:

                try:
                    if i in KB['A'][0]:
                        peligro.append(i)

                    if i in KB['D'][0]:
                        peligro.append(i)

                    if i in KB['S'][0]:
                        peligro.append(i)

                except:
                    pass

            if len(peligro) > 0:
                print('NO puedes ir a:', peligro)

            else:
                print('Los peligros han sido revelados puedes ir por una ruta desconocida')

            print('Si no hay otra opción arriésgate')

    if z not in ['1','2','3','4','5','6','7','!']:
        board_play[pos[0]][pos[1]] = '0'


    print('\n')

    ESTADO, shots = disparar(pos,shots)
    if ESTADO == False:
        print('El demogorgon está muerto')
        
    else:
        print('El demogorgon sigue vivo')
    
    if shots > 0:
        print('Has gastado tu único disparo')

    print('\n')




    '''Bucle de juego'''

    for i in range(1, 4*(size**2)):

        print('\n')

        '''Movimiento del jugador'''
        pos = movement(pos)

        #Limpiamos la terminal
        clear_terminal()


        '''Si hemos vuelto a una casilla anterior
            no nos va a proporcionas información'''
        añadir = True
        try:
            if pos in CAMINO:
                añadir = False
            else:  
                y = pos.copy()
                CAMINO.append(y)
        except:
            pass
        

        if añadir == True:
            
            '''Comprobación del tablero'''
            board_play[pos[0]][pos[1]] = {board[pos[0]][pos[1]]}
            board_play = mirar(board_play, pos)
            board_play = mirar_alrededor(board_play, pos, board)
            board_play = check_board(board_play, pos)

            '''Funciones lógicas'''
            KB = knowledge(KB, board_play, pos)
            KB = eliminar_repetidos(KB)
            KB = check_pos(KB, board_play, pos)
            KB = eliminar_dobles(KB)
            x = SDA(KB, board_play)
            KB = x[0]
            board_play = x[1]
 
            print('\n')

        '''Información del tablero'''
        info(KB, pos)
        
        print('\n')

        '''Imprime el tablero que ve el jugador'''
        z = board_play[pos[0]][pos[1]]
        if z not in ['1','2','3','4','5','6','7','!']:
            board_play[pos[0]][pos[1]] = '*'

        else:
            board_play[pos[0]][pos[1]] = '!'

        print_board(board_play)
        print('\n')
        print('Estás en la posición: ', pos)
        print('\n')

        if board_play[pos[0]][pos[1]] == '*':
            print('No hay peligro en ninguna dirección desconocida')

        if board_play[pos[0]][pos[1]] == '!':

            print('¡Cuidado! Hay peligro')
            print('Ve por una camino que conozcas')
            
            alrededor = posiciones_alrededor_2(pos)

            peligro = []
            for i in alrededor:

                try:
                    if i in KB['A'][0]:
                        peligro.append(i)
                except:
                    pass

                try:
                    if i in KB['D'][0]:
                        peligro.append(i)
                except:
                    pass

                try:
                    if i in KB['S'][0]:
                        peligro.append(i)
                except:
                    pass

            if len(peligro) > 0:
                print('NO puedes ir a:', list(set(peligro)))

            else:
                print('Los peligros han sido revelados puedes ir por una ruta desconocida')

            print('Si no hay otra opción arriésgate')
        
        if z not in ['1','2','3','4','5','6','7','!']:
            board_play[pos[0]][pos[1]] = '0'

        print('\n')

        if shots == 0:
            ESTADO, shots = disparar(pos, shots)

        if ESTADO == False:
            print('El demogorgon está muerto')
            
        else:
            print('El demogorgon sigue vivo')
        
        if shots > 0:
            print('Has gastado tu único disparo')
        print('\n')
