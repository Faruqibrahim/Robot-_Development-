from helper.FieldDisplay import *
from helper.Node import *

def getNeighbors(nodes, node):
    neighbors = []

    # <-- Add code to generate a list of neighbours for a node

    return neighbors

def AStar(field):
    # translate the field array into node representation. See file Node.py
    nodes, start, finish = createNodesFromField(field)
    open_list = []  # Empty list for opened nodes
    closed_list = []  # Empty list for closed nodes

    # Set up starting node
    start.gScore = 0
    start.fScore = start.dist(finish)
    open_list.append(start)

    # Find path using A* algorithm
    while len(open_list) > 0 and finish not in closed_list:
    # <-- Write you code here (before the following lines):

        # This structure is used as you only need to display nodes on the first task
        if __name__ == "__main__":
            display.draw_map(nodes)  # Draw the result of this step

    # Mark the path (go from finish to start using parents)
    currentNode = finish  # Start of the reverse path finding
    path = []
    while not currentNode == start:  # If start is reached the path is complete
        path.append(currentNode)
        if currentNode.type != 3:  # Mark all steps except the finish as a path
            currentNode.type = 4
        if __name__ == "__main__":
            display.draw_node(currentNode)  # Update the graphics now that we have marked the path
        currentNode = currentNode.parent  # Take the next point
    path = list(reversed(path))  # Reverse the path to make it go start to finish


    return path, finish.gScore

# This construction make the following code run only when this file is
# executed directly, and not when it is imported into other files
def main():
    global display
    # 0 - Wall
    # 1 - Passable
    # 2 - Start
    # 3 - End
    # 4 - Path
    field = [[1, 0, 1, 0, 1, 0, 3],
             [1, 0, 1, 0, 1, 0, 1],
             [1, 0, 1, 0, 1, 0, 1],
             [1, 0, 1, 0, 1, 0, 1],
             [1, 0, 1, 0, 1, 0, 1],
             [1, 0, 1, 0, 1, 0, 1],
             [2, 1, 1, 1, 1, 1, 1]]  # Field is a 2d array of numbers representing passable terrain and obstacles

    fieldX = len(field[0])
    fieldY = len(field)

    display = FieldDisplay(60 * fieldX, 60 * fieldY, fieldX, fieldY)  # initializing field display. See file FieldDisplay.py

    AStar(field)

    display.closeOnMouse()  # Makes the program close on mouse click when done

if __name__ == "__main__":
	main()