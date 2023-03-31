#  Title:		Graph and schedule implementation
#  Purpose:     This class creates a graph from the processed csv input. It is then sorted using a topological sort,
#                   eventually being used to create the class schedule.
# 
#  TC:          O(n^3)
import networkx as nx
import matplotlib.pyplot as plt
import re

class Graph:
    def __init__(self) -> None:
        # The graph created from processed input
        self.course_graph = None
        # The topological sorting of course_graph
        self.top_graph = None

    # Adds each course from the csv to the graph, along with all the pre-reqs. Pre-reqs
    # that have alternatives options are also accounted for here.
    def create_graph(self, course_input):
        graph = nx.DiGraph()
        for n in course_input:
            graph.add_node(n)
            
            # Adding edges for pre-reqs
            for c in course_input[n][2]:
                # Checks to ensure we don't get an empty node added
                if len(c) == 0:
                    continue
                else:
                    optionals = c.split(' | ')
                    # Need special case for the classes that have alternatives as a pre-req
                    if len(optionals) != 0:
                        for i in optionals:
                            graph.add_edge(i, n)
                    # Adding all the regular classes that are required
                    else:
                        graph.add_edge(c, n)

        # Adding the course data to the nodes of the graph
        nodes = graph.nodes
        for course in nodes:
            nodes[course]["data"] = course_input.get(course)

        self.course_graph = graph

    # Creates a topological sorting of the original graph
    def create_top_sort(self):
        # creates a topological ordering of the previous graph
        sorted = list(nx.topological_sort(self.course_graph))
        new_graph = nx.DiGraph()
        new_graph.add_nodes_from(sorted)
        new_graph.add_edges_from(self.course_graph.edges())

        # Adding the course data to the nodes of the graph
        nodes = new_graph.nodes
        nodes_old = self.course_graph.nodes
        for course in nodes:
            nodes[course]["data"] = nodes_old[course]["data"]

        self.top_graph = new_graph

    # Creates a rudimentary graph showing the courses and their relations
    def draw_graph(self):
        pos = nx.spring_layout(self.top_graph, k=5)
        nx.draw(self.top_graph, pos=pos, with_labels=True, arrows=True)
        plt.show()

    # Creates and returns a schedule that is formed for the desired number of credits, and starting quarter
    def create_schedule(self, desired_credits, start_quarter):
        # Initialize the schedule
        schedule = {}
        # Create a year layout
        year = {"Quarter 1": [], "Quarter 2": [], "Quarter 3": []}
        # Initialize list of credits per quarter
        creds_per_q = [0, 0, 0]
        # year counter
        curr_year = 1
        # Iterator for the list of courses
        i = 0

        # Input validation for desired credits per quarter
        if desired_credits == '' or int(desired_credits) not in range(12, 19):
            desired_credits = '18'
        
        # Input validation for desired starting quarter
        if start_quarter == '' or int(start_quarter) not in range(1, 4):
            start_quarter = '1'
        
        # Get nodes from graph and store them in an iterable list
        nodes = self.top_graph.nodes()
        list_nodes = list(nodes)
        
        # loop until there are no more classes to take
        while len(list_nodes) != 0:

            # Save current course in list to course
            course = list_nodes[i]

            # Retrieve data from course
            course_number = course
            course_name, credits, prerequisites, quarters_offered = nodes[course]['data']

            credits = int(credits)
            desired_credits = int(desired_credits)

            # Get the first number of course number and subtract 1.
            # EX. CSC 3450 -> 3 - 1 -> 2
            course_year = re.sub('\D', '', course_number)
            course_year = int(course_year[0]) - 1

            # Checks if class meets prereq requirements
            goodToGo = True
            for prerequisite in prerequisites:
                optionals = prerequisite.split(' | ')
                if len(optionals) > 1:
                    for option in optionals:
                        if option in list_nodes:
                            goodToGo = False
                        else:
                            goodToGo = True
                            break
                else:
                    if prerequisite in list_nodes:
                        goodToGo = False


            # If it does not meet prereq requirements, iterates to the next course
            # Also validates that course will only be taken after first number of 
            # course number - 1. 
            if (not goodToGo) and prerequisites[0] != '' or curr_year < course_year:
                i += 1
            else:
                # Loops through the quarters in the current year
                for quarter in year:
                    # Gets the current quarer we are on.
                    curr_quarter = int(quarter[-1])

                    # Validates desired start_quarter
                    if curr_year == 1 and curr_quarter < int(start_quarter):
                        continue

                    # Skips the quarter if the class isn't offered in the current quarter
                    if str(curr_quarter) not in quarters_offered:
                        continue
                    
                    # Skips quarter if the class will put the quarter over max credits
                    if (creds_per_q[curr_quarter - 1] + credits > desired_credits):
                        continue
                    
                    # If it passes all tests, adds the course to current quarter and adds credits to
                    # the current quarter and removes course from list
                    year[quarter].append(course)
                    creds_per_q[curr_quarter - 1] += credits
                    list_nodes.pop(i)
                    break
                # iterates to next course if it doesn't fit
                else:
                    i += 1

            # if the year is full it creates a new year, iterates current year, and resets credits in the year
            if i >= len(list_nodes) or sum(creds_per_q) ==  desired_credits * 3:
                i=0
                schedule["Year " + str(curr_year)] = year
                curr_year += 1
                creds_per_q = [0, 0, 0]
                year = {"Quarter 1": [], "Quarter 2": [], "Quarter 3": []}
            


        return schedule