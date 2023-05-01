from collections import deque
import json
import time

class Graph:

    def __init__(self):

        # {(AFRO-101, 3): {(AFRO 105, 2), (AFRO 102, 2)}}
        '''
            What this means is that the 3 credit course AFRO-101 is a prerequisite to AFRO 105
            and AFRO 102
        '''
        self.adjacency_dict = {}
    
    def add_vertex(self, course):
        if course not in self.adjacency_dict:
            self.adjacency_dict[course] = set()
    
    def add_edge(self, course1, course2):
        self.add_vertex(course1)
        if course2 not in self.adjacency_dict[course1]:
            self.adjacency_dict[course1].add(course2)
    
    def doTopologicalSort(self):
        self.indegree_dict = {}

        total_num_courses = len(self.adjacency_dict)
        for k, v in self.adjacency_dict.items():
            for course in v:
                if course in self.indegree_dict:
                    self.indegree_dict[course] += 1
                else:
                    self.indegree_dict[course] = 1
            if k not in self.indegree_dict:
                self.indegree_dict[k] = 0
        
        print(self.indegree_dict)
        sorted_courses = []
        temp_dict = self.indegree_dict.copy()
        while 0 in self.indegree_dict.values():
            for k, v in temp_dict.items():
                if v == 0:
                    sorted_courses.append(k)
                    prereq_for_courses = self.adjacency_dict[k]
                    for courses in prereq_for_courses:
                        self.indegree_dict[courses] -= 1
                    del self.indegree_dict[k]
            temp_dict = self.indegree_dict.copy()
        if len(sorted_courses) == total_num_courses:
            return sorted_courses
        raise("Cycle in the Graph!")
        

class UserInteraction:
    def __init__(self, sems_remaining, major, total_credits):
        self.sems_remaining = sems_remaining
        self.major = major
        self.credits = total_credits

    def give_info(self):
        print("We are thrilled to provide you any help with your course schedule. We may ask some JSON files from you.")
        print("The format of those file must be (unless specified): \n{Course Number: [Department, Credits]}")
        print("Let's proceed.")
        print()
    
    def json_read(self, path):
        with open(path) as f_in:
            return json.load(f_in)

    def ask_required_courses(self):
        print("So, we'd need to know what your degree requirements are in order to proceed.")
        print("Input the filepath to your course list (JSON File): ", end = "")
        path = input()
        self.course_reqs = self.json_read(path)
        print()
    
    def ask_tech_electives(self):
        print("If your degree requires any electives (technical), please provide them below.")
        print("Input the filepath to the Tech Elective Courses List (JSON File): ", end = "")
        path = input()
        self.tech_electives = self.json_read(path)
        print()
        
    def ask_nontech_electives(self):
        print("If your degree requires any electives (non-technical), please provide them below.")
        print("Input the filepath to the Non-tech Elective Courses List (JSON File): ", end = "")
        path = input()
        self.nontech_electives = self.json_read(path)
        print()
    
    def ask_already_taken_courses(self):
        print("Now please provide the list of your transferred courses and required courses you've taken already.")
        print("Input the filepath here (JSON File): ", end = "")
        path = input()
        self.already_taken = self.json_read(path)
        print()
        
    
    def ask_courses_want_to_take(self):
        print("Finally, if there are any non-mandatory courses that you'd like to take, please provide them below.")
        print("Input the filepath to the non-mandatory courses you want to take here (JSON File): ", end = "")
        path = input()
        self.courses_want_to_take = self.json_read(path)
        print()
    
    def course_relationship(self):
        print("Now, we finally need to know how courses are organized at your university.")
        print("Please provide us with the pre-requisites for all of the courses you're yet to take")

        print("The format is:\n{Course Number: {Prereq1: Prereq1 credits, Prereq2: Prereq2 Credits}, \nPrereq1: {Prereq for prereq1: Num of Credits} }")
        print("Input the filepath to the pre-requisites (JSON File): ", end = "")
        path = input()
        self.course_relationship = self.json_read(path)
        print()
    
    def makeGraph(self):
        self.g = Graph()
        for course, prereqs in self.course_relationship.items():
            course_credit = None
            if course in self.course_reqs:
                course_credit = self.course_reqs[course][1]
            elif course in self.tech_electives:
                course_credit = self.tech_electives[course][1]
            elif course in self.nontech_electives:
                course_credit = self.nontech_electives[course][1]
            elif course in self.courses_want_to_take:
                course_credit = self.courses_want_to_take[course][1]
            else:
                raise(f"Credit Information not provided for {course}")

            for prereq in prereqs:
                prereq_credit = None
                if prereq in self.course_reqs:
                    prereq_credit = self.course_reqs[prereq][1]
                elif prereq in self.tech_electives:
                    prereq_credit = self.tech_electives[prereq][1]
                elif prereq in self.nontech_electives:
                    prereq_credit = self.nontech_electives[prereq][1]
                elif prereq in self.courses_want_to_take:
                    prereq_credit = self.courses_want_to_take[prereq][1]
                else:
                    raise(f"Prerequisite Credit Error. No number of credits for {prereq} course provided")

                self.g.add_edge((prereq, prereq_credit), (course, course_credit))
        
        for k, v in self.course_reqs.items():
            self.g.add_vertex((k, v[1]))
        
        for k, v in self.tech_electives.items():
            self.g.add_vertex((k, v[1]))
        
        for k, v in self.nontech_electives.items():
            self.g.add_vertex((k, v[1]))
        
        for k, v in self.courses_want_to_take.items():
            self.g.add_vertex((k, v[1]))

if __name__ == "__main__":
    user = UserInteraction(4, "Computer Science", 120)
    user.give_info()
    time.sleep(5)
    user.ask_required_courses()
    user.ask_nontech_electives()
    user.ask_tech_electives()
    user.ask_already_taken_courses()
    user.ask_courses_want_to_take()
    user.course_relationship()
    user.makeGraph()
    print(user.g.adjacency_dict)
    print(user.g.doTopologicalSort())

