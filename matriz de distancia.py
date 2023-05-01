import numpy as np
from scipy.spatial import Delaunay
import matplotlib.pyplot as plt


#we read the txt file containing the original array
with open('datos.txt', 'r') as file:
    matriz = file.read()

#we replace the blank spaces with comas
c_matrix = matriz.replace('  ' , ', ')

#for each line break, the matrix is divided
lines = c_matrix.split('\n')
#print(lines)

'''we split everything by lines'''
matrix_values = [linea.split(',') for linea in lines]
#print(matrix_values)

'''the process we did before is a way to make 
the input of the txt file readable to the np.array
function'''
distance_matix = np.array(matrix_values, dtype=float)
#print(distance_matix)


#here we will obtain the amount of nodes on the matrix
node_amnt = distance_matix.shape[1]

#here we will generate randomly every node's coordinate
coord = np.random.rand(node_amnt, 2)

'''we create an instance for Delaunay, where we triangulate the nodes
thus creating an optimal space in which no node interferes with one another'''
triangulation = Delaunay(coord)

#we graph the nodes
plt.triplot(coord[:, 0], coord[:, 1], triangulation.simplices)
plt.plot(coord[:, 0], coord[:, 1], 'o')

#tagging the nodes with an index, so every node can have a number
for i, (x, y) in enumerate(coord):
    plt.text(x, y, str(i), color='black')


for i in range(node_amnt):
    '''get the indexes from neighbors of the current node, which is 'i'
     in the dealunay triangulation to be able to access the neighbors and 
     carry out future operations on them'''
    neighbors = triangulation.vertex_neighbor_vertices[1][
        triangulation.vertex_neighbor_vertices[0][i]: triangulation.vertex_neighbor_vertices[0][i + 1]
    ]
    for j in neighbors:
        #we obtain the distance between one node and it's neighbor
        distance = distance_matix[i, j]
        '''the coordinates of the current(i) and neighbor(j) nodes are obtained
         respectively, from coord that contains the coordinates
         of all nodes'''
        x = [coord[i, 0], coord[j, 0]]
        y = [coord[i, 1], coord[j, 1]]
        '''we draw a black line between the current node and it's 
        neighbor'''
        plt.plot(x, y, 'k-')
        '''a text is placed at the midpoint between the nodes and we 
        display the distance between them with a blue-colored text'''
        plt.text(np.mean(x), np.mean(y), str(distance), color='blue')




# generating a random path that returns to the start
'''we take a random node as the starting node'''
start = np.random.randint(node_amnt)
'''we store the starting node in the route'''
route = [start]
'''we initialize the path cost at 0'''
total_cost = 0
'''we initialize the current node as the start node'''
current = start
while len(route) < node_amnt:
    neighbors = triangulation.vertex_neighbor_vertices[1][
        triangulation.vertex_neighbor_vertices[0][current]: triangulation.vertex_neighbor_vertices[0][current + 1]
    ]
    '''se verifica que no se visiten nodos visitados anteriormente'''
    neighbors = [v for v in neighbors if v not in route]
    '''se verifica si hay neighbors disponibles en los nodos, si no, se
    rompe el ciclo completo con el break'''
    if len(neighbors) == 0:
        break
    '''selecciona un vecino al azar'''
    next = np.random.choice(neighbors)
    '''se agrega ese vecino elegido a la route'''
    route.append(next)
    '''se busca el costo de route, la de el nodo actual al vecino y se 
    le suma al costo total'''
    total_cost += distance_matix[current, next]
    '''el nodo actual sera igual al nodo que esta en la variable next'''
    current = next

''''se regresa al start, especificamente, se agrega el nodo inicial
al final de la lista al agregar al final de la lista el nodo inicial'''
route.append(start)
'''se suma el costo de haber ido de vuelta al nodo inicial desde el ultimo nodo
visitado, para asi obtener el costo total de la route final'''
total_cost += distance_matix[current, start]

# Mostrar la route y el costo total
'''se obtienen las coordenadas de cada nodo en la route'''
route_coords = coord[route]
'''traza la route en el grafico utilizando coordenadas de los nodos en la variable
route_coords, y extrae las coordenadas X y Y respectivamente de la matriz
route_coords'''
plt.plot(route_coords[:, 0], route_coords[:, 1], '-o')
'''se le da un titulo al grafico'''
plt.title("random route")

'''se muestra el grafico'''
print("route:", route)
print("Total cost:", total_cost)
print("starting node: ", start)

plt.show()

