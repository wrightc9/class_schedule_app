#  Title:		Visualize graph implementation
#  Purpose:     Creates a visual of the course schedule that is generated in graph.py. 
#                   It adapts for the starting quarter and credit limit, and shows all the courses, along with
#                   their pre-reqs in a quarter separated fashion.
# 
#  TC:          O(n^3)

import matplotlib.pyplot as plt
from reader import Reader

class GraphUI:
    def __init__(self, course_data, file_reader) -> None:
        self.courses_dict = course_data
        self.read_major = file_reader
    
    def create_graph(self):
        # define courses and quarters
        courses = self.read_major.courseDict.keys()
        quarters = {}
        prerequisite_edges = []
        pos = {}
        qtr_count = 0
        first_class_done = False
        prev_classes = set()
        total_quarters = []
        
        # n, 3, n, n
        for y in self.courses_dict:
            for q in self.courses_dict[y]:
                # Generates labels for plot
                qtr_count += 1
                qtr = 'Q' + str(qtr_count)
                total_quarters.append(qtr)
                # Define quarters, and put courses from that quarter in it
                quarters[qtr] = self.courses_dict[y][q]
                y_pos_count = 1
                
                # Checks for and adds lines between courses and their pre-reqs
                for c in self.courses_dict[y][q]:
                    if first_class_done:
                        for class_potential_req in prev_classes:
                            if class_potential_req in self.read_major.courseDict[c][2]:
                                prerequisite_edges.append((class_potential_req, c))
                        
                    # Define positions on graph
                    pos[c] = (qtr_count * 2.25, y_pos_count * 3)
                    y_pos_count += 1
                
                prev_classes.update(self.courses_dict[y][q])
                
            # Used to check and create pre-req edges
            first_class_done = True

        # Ensures proper list sizes as required to adjust x-ticks   
        if len(total_quarters) < ((len(prev_classes) // 2) - 1):
            while (len(total_quarters) < ((len(prev_classes) // 2) - 1)):
                total_quarters.append('')
        else:
            prev_classes = list(prev_classes)
            while (len(total_quarters) != ((len(prev_classes) // 2) - 1)):
                prev_classes.append('')

        # creates figure    
        fig, ax = plt.subplots(figsize=(10, 8))
        # adjust the size of the plot
        fig.subplots_adjust(left=.1, bottom=.1, right=.9, top=.9)


        # draw nodes, and put the names of the nodes on top of them
        for course in courses:
            quarter = None
            for q, c_list in quarters.items():
                if course in c_list:
                    quarter = q
                    break
            if quarter is not None:
                ax.add_patch(plt.Circle(pos[course], radius=.7, facecolor='grey', edgecolor='black'))
                ax.text(pos[course][0], pos[course][1], course, ha='center', va='center', size=10, color='black')

        # draw edges between the different nodes
        for edge in prerequisite_edges:
            x = [pos[edge[0]][0], pos[edge[1]][0]]
            y = [pos[edge[0]][1], pos[edge[1]][1]]
            ax.plot(x, y, color='gray', linestyle='solid', alpha=0.2)

        # Creates the size of the x and y axis
        ax.set_xlim(0, len(prev_classes) * 1.1)
        ax.set_ylim(0, 16)
        ax.set_aspect('equal')
        total_quarters.insert(0, '')

        # Adjusts the spacing between the ticks on the x-axis
        plt.xticks([i * 2.25 for i in range(len(prev_classes) // 2)], total_quarters)
        # Sets y-axis as not visible
        plt.gca().get_yaxis().set_visible(False)
        # Makes the graph fullscreen by default
        fig.canvas.manager.full_screen_toggle()
        ax.axis('scaled')
        # Shows the graph
        plt.show()
