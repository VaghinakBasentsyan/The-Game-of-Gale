import pickle
import uuid


class Node(object):

    def __init__(self, id, pos_x, pos_y, color):
        self.id = id
        self.color = color
        self.pos_x = pos_x
        self.pos_y = pos_y

    def __str__(self):
        return "{}".format(self.id)


class Edge(object):

    def __init__(self, n1, n2):
        self.node1 = n1
        self.node2 = n2
        # self.weight = w

    def __str__(self):
        return "color : {} :: node_1: {} :: node_2: {}".format(self.node1.color, self.node1.id, self.node2.id)


class Graph(object):
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.which_next = 'blue'
        self.nodes = []
        self.edges = []

        self.error_msg = None
        id = 1
        for i in range(1, 11, 2):
            for j in range(0, 11, 2):
                self.add_node(id, i, j, 'blue')
                id += 1

        for i in range(0, 11, 2):
            for j in range(1, 11, 2):
                self.add_node(id, i, j, 'red')
                id += 1

    def add_egde(self, id1, id2):
        n1 = self.find_node(id1)
        n2 = self.find_node(id2)

        if n1 == None or n2 == None:
            return

        if not n1.color == self.which_next:
            return False

        if not self.has_edge(id1, id2) and n1.color == n2.color:
            if (n1.pos_x - n2.pos_x) == 0 or (n1.pos_y - n2.pos_y) == 0:
                if not self.is_intersect(n1, n2):
                    self.edges.append(Edge(n1, n2))
                    return True
            else:
                return False

    def add_edge_by_pos(self, pos_x, pos_y, neighbour_pos_x, neighbour_pos_y):
        n1 = self.find_node_by_pos(pos_x, pos_y)
        n2 = self.find_node_by_pos(neighbour_pos_x, neighbour_pos_y)
        return self.add_egde(n1.id, n2.id)

    def has_edge(self, id1, id2):
        for e in self.edges:
            if e.node1.id == id1 and e.node2.id == id2:
                return True
        return False

    def find_node(self, id):
        for n in self.nodes:
            if n.id == id:
                return n
        return None

    def find_node_by_pos(self, pos_x, pos_y):
        for node in self.nodes:
            if node.pos_x == pos_x and node.pos_y == pos_y:
                return node
        return None

    def add_node(self, id, pos_x, pos_y, color):
        if not self.has_node(id):
            self.nodes.append(Node(id, pos_x, pos_y, color))

    def has_node(self, id):
        for n in self.nodes:
            if n.id == id:
                return True
        return False

    def is_intersect(self, nd_1, nd_2):
        if not self.edges:
            return False
        for edge in self.edges:
            if edge.node1.color == nd_1.color:

                continue
            if (nd_1.pos_x > edge.node1.pos_x > nd_2.pos_x) or (nd_1.pos_x < edge.node1.pos_x < nd_2.pos_x ):
                if (edge.node1.pos_y < nd_1.pos_y < edge.node2.pos_y) or (edge.node1.pos_y > nd_1.pos_y > edge.node2.pos_y):
                    return True
            elif (nd_1.pos_y > edge.node1.pos_y > nd_2.pos_y) or (nd_1.pos_y < edge.node1.pos_y < nd_2.pos_y ):
                if (edge.node1.pos_x < nd_1.pos_x < edge.node2.pos_x) or (edge.node1.pos_x > nd_1.pos_x > edge.node2.pos_x):
                    return True
        return False

    def is_over(self):
        for edge in self.edges:
            if edge.node1.pos_y == 0:
                start_node = edge.node1
                end_node = self.get_end_node(start_node)
                if self.dif_by_color(start_node, end_node):
                    return True
            elif edge.node2.pos_y == 0:
                start_node = edge.node2
                end_node = self.get_end_node(start_node)
                if self.dif_by_color(start_node, end_node):
                    return True
            elif edge.node1.pos_x == 0:
                start_node = edge.node1
                end_node = self.get_end_node(start_node)
                if self.dif_by_color(start_node, end_node):
                    return True
            elif edge.node2.pos_x == 0:
                start_node = edge.node2
                end_node = self.get_end_node(start_node)
                if self.dif_by_color(start_node, end_node):
                    return True
        return False

    def dif_by_color(self, nd_start, nd_end):
        if nd_start.color == "blue" and nd_end.pos_y - nd_start.pos_y == 10:
            return True
        if nd_start.color == "red" and nd_end.pos_x - nd_start.pos_x == 10:
            return True
        return False

    def get_end_node(self, node, checked_ids=None):
        if not checked_ids:
            checked_ids = list()
        for edge in self.edges:
            if edge.node1.id == node.id and edge.node2.id not in checked_ids:
                checked_ids.append(node.id)
                node = edge.node2

                return self.get_end_node(node, checked_ids)
            elif edge.node2.id == node.id and edge.node1.id not in checked_ids:
                checked_ids.append(node.id)
                node = edge.node1
                return self.get_end_node(node, checked_ids)
            else:
                continue

        return node

    def save(self, fn):
        try:
            fh = open('games/{}'.format(fn), "wb")
            pickle.dump(self.id, fh)
            pickle.dump(self.which_next, fh)
            pickle.dump(self.nodes, fh)
            pickle.dump(self.edges, fh)
            pickle.dump(self.error_msg, fh)
            fh.close()
        except IOError:
            return

    def clear(self):
        self.nodes = []
        self.edges = []
        self.error_msg = None

    def load(self, fn):
        self.clear()
        try:
            fh = open('games/{}'.format(fn), "rb")
            self.id = pickle.load(fh)
            self.which_next = pickle.load(fh)
            self.nodes = pickle.load(fh)
            self.edges = pickle.load(fh)
            self.error_msg = pickle.load(fh)
            fh.close()
        except IOError:
            self.error_msg = "Cant load data"

    def move_validation(self, node):
        pass