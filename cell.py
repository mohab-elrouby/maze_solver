


class Cell:
    def __init__(self, position, connections = [], isVisited = False):
        self.position = position
        self.connections = connections
        self.isVisited = isVisited
    
    def set_new_connection(self, connectedCell):
        self.connections.append(connectedCell)

    def set_visited(self, flag):
        self.isVisited = flag

    def get_position(self):
        return self.position

    def get_connections(self):
        return self.connections


