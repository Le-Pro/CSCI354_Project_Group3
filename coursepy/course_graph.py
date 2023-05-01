import json


class CourseGraph:
    def __init__(self):
        self.nodes = []
        self.graph = {}

    def add_node(self, node):
        if node not in self.graph:
            self.graph[node] = {}
            self.nodes.append(node)

    def add_edge(self, src, dest, weight):
        self.graph[src][dest] = weight

    def get_nodes(self):
        """Returns the nodes of the graph."""
        return self.nodes

    def get_outgoing_edges(self, node):
        """Returns the neighbors of a node."""
        connections = []
        for out_node in self.nodes:
            if self.graph[node].get(out_node, False):
                connections.append(out_node)
        return connections

    def value(self, node1, node2):
        """Returns the value of an edge between two nodes."""
        return self.graph[node1][node2]


prereqs_dict = json.loads("".join(open("prereqs_file.json").readlines()))
req_course_dict = json.loads("".join(open("req_course_file.json").readlines()))
tech_elect_dict = json.loads("".join(open("tech_elect_file.json").readlines()))
nontech_elect_dict = json.loads("".join(open("nontech_elect_file.json").readlines()))
taken_course_list = json.loads("".join(open("taken_course_file.json").readlines()))
voluntary_course = json.loads("".join(open("voluntary_course_file.json").readlines()))

g = CourseGraph()

for course in req_course_dict.keys():
    g.add_node(course)

for course in tech_elect_dict.keys():
    g.add_node(course)

for course in nontech_elect_dict.keys():
    g.add_node(course)

for course in voluntary_course.keys():
    g.add_node(course)

for course in prereqs_dict.keys():
    for edge in prereqs_dict[course]:
        weight = None
        if edge in req_course_dict:
            weight = req_course_dict[edge][1]
        if edge in tech_elect_dict:
            weight = tech_elect_dict[edge][1]
        if edge in nontech_elect_dict:
            weight = nontech_elect_dict[edge][1]
        if edge in voluntary_course:
            weight = voluntary_course[edge][1]
        g.add_edge(edge, course, weight=weight)


print(g.graph)


