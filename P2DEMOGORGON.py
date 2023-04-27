import random
import sys

'''Crear un tablero de tamaño size con el símbolo symbol'''
def create_board(size, symbol):
    
    return [[symbol for _ in range(size)] for _ in range(size)]



'''Añadimos las el lugar donde estarán el Demogorgon, el Agujero y la Salida'''
def add_letters(board):
    letters = ["D", "A", "S"]
    # Inicialmente se añade la posición (0,0) para que no se eliga
    chosen_positions = [(0,0)] 
    for letter in letters:
        # Elegir una posición aleatoria
        row = random.randint(0, len(board)-1)
        col = random.randint(0, len(board[0])-1)
        pos = (row,col)
        # Comprobar si ya ha sido elegida anteriormente
        while pos in chosen_positions:
            row = random.randint(0, len(board)-1)
            col = random.randint(0, len(board[0])-1)
            pos = (row,col)
        
        board[row][col] = letter
        chosen_positions.append(pos)


'''Funcionalidad para moverse por el tablero'''
def move(board, current_pos):
    # Preguntar por pantalla la dirección del movimiento
    direction = input("Hacia que dirección deseas moverte? (izquierda, derecha, arriba, abajo): ")
    direction = direction.lower()

    # Comprobar que la dirección es válida
    if direction not in ["izquierda", "derecha", "arriba", "abajo"]:
        print("Dirección no válida")
        new_pos = move(board, current_pos)
    

    # Calcular la nueva posición
    if direction == "izquierda":
        new_pos = (current_pos[0], current_pos[1] - 1)
    elif direction == "derecha":
        new_pos = (current_pos[0], current_pos[1] + 1)
    elif direction == "arriba":
        new_pos = (current_pos[0] - 1, current_pos[1])
    elif direction == "abajo":
        new_pos = (current_pos[0] + 1, current_pos[1])

    # Comprobar que la nueva posición está dentro del tablero
    if (new_pos[0] < 0 or new_pos[0] >= len(board) or new_pos[1] < 0 or new_pos[1] >= len(board)):
        print("Movimiento fuera del tablero")
        new_pos = move(board, current_pos)

    else:

        #Comprobar que la nueva posición no es un obstáculo
        check_position(board, new_pos)
        #Añadir la nueva posición al camino
        add_camino(new_pos, camino)
    
        return new_pos

'''Función para ver si hemos caido en un peligro'''
def check_position(board, current_pos):
    row, col = current_pos

    if board[row][col] == "D":
        print("El Demogorgon te ha atrapado")
        for row in board:
            print(row)
        sys.exit()
    if board[row][col] == "A":
        print("Caes al vacío")
        for row in board:
            print(row)
        sys.exit()
    if board[row][col] == "S":
        print("Has salido de la cueva")
        for row in board:
            print(row)
        sys.exit()


'''Función para guardar el valor de las posiciones que hay alrededor de la posición actual'''
def check_adjacent_positions(board, current_pos):

    row, col = current_pos
    adjacent_positions = []
    # Comprobar posición arriba
    if row > 0:
        adjacent_positions.append(board[row-1][col])
    # Comprobar posición abajo
    if row < len(board) - 1:
        adjacent_positions.append(board[row+1][col])
    # Comprobar posición izquierda
    if col > 0:
        adjacent_positions.append(board[row][col-1])
    # Comprobar posición derecha
    if col < len(board[0]) - 1:
        adjacent_positions.append(board[row][col+1])

    return adjacent_positions


'''Creamos un diccionario con las posiciones adyacentes a cada posición del tablero'''
def create_adjacent_positions_dict(board):
    positions_dict = {}
    for row in range(len(board)):
        for col in range(len(board[0])):
            current_pos = (row, col)
            positions_dict[current_pos] = check_adjacent_positions(board, current_pos)
    return positions_dict


'''Creamos un diccionario donde a cada casilla se le asigna de 0.1 de que esté el Demogorgon, el Agujero o la Salida (no sirve
para nada aquí, sin embargo si realmente hay un peligro alrededor, pone que su probabilidad es de 0.8)'''
def create_positions_dict(board):
    positions_dict = {}
    for row in range(len(board)):
        for col in range(len(board[0])):
            current_pos = (row, col)
            positions_dict[current_pos] = [0.05,0.05,0.05]
            #comprobar las posiciones adyacentes
            adj_pos = check_adjacent_positions(board, current_pos)
            for pos in adj_pos:
                if pos == "D":
                    positions_dict[current_pos][0] = 0.8
                elif pos == "A":
                    positions_dict[current_pos][1] = 0.8
                elif pos == "S":
                    positions_dict[current_pos][2] = 0.8

    return positions_dict


'''Crearmos otro diccionario donde a cada casilla se le asigna la probabilidad de que esté el Demogorgon, el Agujero o la Salida inicialmente'''
def create_probabilities_dict(board, size):
    positions_dict = {}
    for row in range(len(board)):
        for col in range(len(board[0])):
            current_pos = (row, col)
            positions_dict[current_pos] = [1/(size**2 -1),1/(size**2 -1),1/(size**2 -1)]
    
    positions_dict[(0,0)] = [0,0,0]
    return positions_dict

'''Si estamos en una casilla de peligro, la probabilidad de que esté el peligro es 1
si no, la probabilidad de que esté el peligro es 0'''

def check_position2(board, current_pos, positions_dict):
    row, col = current_pos
    if board[row][col] == 'D':
        positions_dict[current_pos][0] = 1
        positions_dict[current_pos][1] = 0
        positions_dict[current_pos][2] = 0
    elif board[row][col] == 'A':
        positions_dict[current_pos][0] = 0
        positions_dict[current_pos][1] = 1
        positions_dict[current_pos][2] = 0
    elif board[row][col] == 'S':
        positions_dict[current_pos][0] = 0
        positions_dict[current_pos][1] = 0
        positions_dict[current_pos][2] = 1
    else:
        positions_dict[current_pos][0] = 0
        positions_dict[current_pos][1] = 0
        positions_dict[current_pos][2] = 0
    
    return positions_dict

'''Función para ir añadiendo las posiciones al camino'''
def add_camino(new_pos, camino):
    if new_pos not in camino:
        camino.append(new_pos)


'''Función para ver qué sentimos en la casilla actual'''
def sensations(positions_dict, current_pos):
    #Inicalmente no se siente nada
    feelings = [False, False, False]
    #Verdadero positivo
    f1  = random.randint(0, 100)
    f2  = random.randint(0, 100)
    f3  = random.randint(0, 100)


    #Demogorgon // Cosquilleo
    if f1 < positions_dict[current_pos][0]*100:
        feelings[0] = True
    
    #Agujero // Brisa
    if f2 < positions_dict[current_pos][1]*100:
        feelings[1] = True
    
    #Salida // Luz
    if f3 < positions_dict[current_pos][2]*100:
        feelings[2] = True
    


    if feelings[0] == True:
        print("Sientes un cosquilleo")
    if feelings[1] == True:
        print("Sientes una brisa")
    if feelings[2] == True:
        print("Ves una  pequeña luz")

    print("\n")
    return feelings


'''Función para guardar las posiciones adyacentes en coordenadas'''
def adjacent_positions(board, current_pos):
    row, col = current_pos
    adjacent_positions = []
    # Comprobar posición arriba
    if row > 0:
        adjacent_positions.append((row-1,col))
    # Comprobar posición abajo
    if row < len(board) - 1:
        adjacent_positions.append((row+1,col))
    # Comprobar posición izquierda
    if col > 0:
        adjacent_positions.append((row,col-1))
    # Comprobar posición derecha
    if col < len(board[0]) - 1:
        adjacent_positions.append((row,col+1))
    return adjacent_positions



'''Función para calcular las probabilidades de que esté el Demogorgon, el Agujero o la Salida en las casillas adyacentes'''
def feels2(current_pos, position_know, camino, positions_dict):

    feelings = sensations(positions_dict, current_pos)

    NOSENTIR = ((1-0.8)*(1/(size**2 - len(camino)))) / ((1-0.8)*(1/(size**2 - len(camino))) + (1-0.05)*(1 - (1/(size**2 - len(camino)))))

    adj_pos = adjacent_positions(board, current_pos)
    for pos in adj_pos:
        if pos not in camino:

            #Demogorgon // Cosquilleo
            if feelings[0] == False:
                position_know[pos][0] = NOSENTIR
            elif feelings[0] == True:
                position_know[pos][0] = 1 - NOSENTIR

            #Agujero // Brisa
            if feelings[1] == False:
                position_know[pos][1] = NOSENTIR
            elif feelings[1] == True:
                position_know[pos][1] = 1 - NOSENTIR
            
            #Salida // Luz
            if feelings[2] == False:
                position_know[pos][2] = NOSENTIR
            elif feelings[2] == True:
                position_know[pos][2] = 1 - NOSENTIR


    return position_know


'''Fn para normalizar las probabilidades'''
def normalize_probabilities(dictionary):
    total1 = sum(val[0] for val in dictionary.values())
    total2 = sum(val[1] for val in dictionary.values())
    total3 = sum(val[2] for val in dictionary.values())
    for key in dictionary:
        dictionary[key][0] = dictionary[key][0]/total1
        dictionary[key][1] = dictionary[key][1]/total2
        dictionary[key][2] = dictionary[key][2]/total3

    return dictionary


'''Función para disparar'''
def disparar(board, current_pos, known_positions):
    # Preguntar por pantalla la dirección del disparo
    direction = input('Quieres disparar? (si/no): ')
    direction = direction.lower()

    if direction == 'si':

        direction = input("Hacia que dirección deseas apuntar? (izquierda, derecha, arriba, abajo): ")

        # Comprobar que la dirección es válida
        if direction not in ["izquierda", "derecha", "arriba", "abajo"]:
            print("Dirección no válida")
            disparar(board, current_pos)

        # Calcular la posición del disparo
        
        if direction == "izquierda":
            new_pos = (current_pos[0], current_pos[1] - 1)
        elif direction == "derecha":
            new_pos = (current_pos[0], current_pos[1] + 1)
        elif direction == "arriba":
            new_pos = (current_pos[0] - 1, current_pos[1])
        elif direction == "abajo":
            new_pos = (current_pos[0] + 1, current_pos[1])

        # Comprobar que la posición del disparo está dentro del tablero
        if (new_pos[0] < 0 or new_pos[0] >= len(board) or
                new_pos[1] < 0 or new_pos[1] >= len(board[0])):
            print("Disparo fuera del tablero")
            disparar(board, current_pos)

        # Comprobar si en la posición del disparo hay una D
        if board[new_pos[0]][new_pos[1]] == 'D':
            d1 = 0.75
            p1 = random.randint(0,100)
            if p1 < d1*100:
                print("¡Disparo exitoso! Has dado a una D")
                for key in known_positions:
                    if key == new_pos:
                        known_positions[key][0] = 1
                        known_positions[key][1] = 0
                        known_positions[key][2] = 0
                    else:
                        known_positions[key][0] = 0
            else:

                print("¡Disparo fallido!")

            known_positions = normalize_probabilities(known_positions)
            

        else:
            print("Fallaste el disparo")

        
    return known_positions
    

'''Función mostrar el tablero de juego'''
def print_board(path, current_pos, size):
    
    board_play = create_board(size, 'X')

    for i in path:
        board_play[i[0]][i[1]] = '-'
    board_play[current_pos[0]][current_pos[1]] = '*'
    for row in board_play:
        print(row)

'''Función para imprimir el mapa lógico'''   
def imprimir_mapa_logico(knowledge_base):
    for key in knowledge_base:
        print(f'{key}:  D:{round(knowledge_base[key][0]*100, 5)}% A:{round(knowledge_base[key][1]*100, 5)}% S:{round(knowledge_base[key][2]*100, 5)}%')


        

if __name__ == '__main__':

    size = 5
    # Crear un tablero de tamaño 5x5
    board = create_board(size, '0')
    camino = []
    add_letters(board)

    # Posición inicial
    current_pos = (0, 0)
    
    positions_dict = create_adjacent_positions_dict(board)

    positions_dict = create_positions_dict(board)

    probablities_dict = create_probabilities_dict(board, size)

    camino.append((current_pos))

    print('\n')
    print_board(camino, current_pos, size)
    print('\n')

    position_know = check_position2(board, current_pos, probablities_dict)

    position_know = feels2(current_pos, position_know, camino, positions_dict)

    position_know = normalize_probabilities(position_know)
    imprimir_mapa_logico(position_know)
    print('\n')

    position_know = disparar(board, current_pos, position_know)
    print('\n')
    print('Dirígete a la casilla con la probabilidad más baja de peligro')


    for i in range(1000):
        current_pos = move(board, current_pos)
        print("La nueva posición es:", current_pos)
        print_board(camino, current_pos, size)  
        print('\n')


        position_know = check_position2(board, current_pos, probablities_dict)

        position_know = feels2(current_pos, position_know, camino, positions_dict)
        position_know = normalize_probabilities(position_know)
        imprimir_mapa_logico(position_know)
        print('\n')

        position_know = disparar(board, current_pos, position_know)

        print('\n')
        print('Dirígete a la casilla con la probabilidad más baja de peligro')


