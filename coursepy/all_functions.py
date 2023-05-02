# from collections import deque
import json
from pulp import *
import sys, os




class Graph:

    def __init__(self):
        """
        A directed graph class made with an adjacency dictionary where the key-value pairs uses the following format 
        # {(AFRO-101, 3): {(AFRO 105, 2), (AFRO 102, 2)}}
            What this means is that the 3 credit course AFRO-101 is a prerequisite to AFRO 105
            and AFRO 102
        """
        self.indegree_dict = {}
        self.adjacency_dict = {}
    
    def add_vertex(self, course):
        if course not in self.adjacency_dict:
            self.adjacency_dict[course] = set()

    def add_edge(self, course1, course2):
        self.add_vertex(course1)
        self.add_vertex(course2)
        if course2 not in self.adjacency_dict[course1]:
            self.adjacency_dict[course1].add(course2)

    def doTopologicalSort(self):
        total_num_courses = len(self.adjacency_dict)
        for k, v in self.adjacency_dict.items():
            for course in v:
                if course in self.indegree_dict:
                    self.indegree_dict[course] += 1
                else:
                    self.indegree_dict[course] = 1
            if k not in self.indegree_dict:
                self.indegree_dict[k] = 0
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
            self.sorted_courses = sorted_courses
            return sorted_courses
        raise("Cycle in the Graph!")
        

class UserInteraction:
    def __init__(self, sems_remaining, major, total_credits):
        """
        This is the start of our program where the user is asked important information

        :param sems_remaining: Number of semesters left
        :param major: User's current major
        :param total_credits: Minimum credits user needs in order to graduate

        """
        self.sems_remaining = sems_remaining
        self.major = major
        self.credits = total_credits
        self.g = None
        self.course_reqs = None
        self.tech_electives = None
        self.nontech_electives = None
        self.already_taken = None
        self.courses_want_to_take = None
        self.course_relationship = None

    @staticmethod
    def give_info():
        print("We are thrilled to provide you any help with your course schedule. We may ask some JSON files from you.")
        print("The format of those file must be (unless specified): \n{Course Number(ASFT-101): [Department, Credits]}")
        print("Let's proceed.")
        print()

    @staticmethod
    def json_read(path):
        with open(path) as f_in:
            return json.load(f_in)

    def ask_required_courses(self):
        """
        Get required courses
        :return: None
        """
        print("So, we'd need to know what your degree requirements are in order to proceed.")
        print("Input the filepath to your course list (JSON File): ", end="")
        path = input()
        print(path)
        self.course_reqs = self.json_read(path)
        print()

    def ask_tech_electives(self):
        """
        Get technical electives
        :return: None
        """
        print("If your degree requires any electives (technical), please provide them below.")
        print("Input the filepath to the Tech Elective Courses List (JSON File): ", end="")
        path = input()
        self.tech_electives = self.json_read(path)
        print()

    def ask_nontech_electives(self):
        """
        Get non-technical electives
        :return: None
        """
        print("If your degree requires any electives (non-technical), please provide them below.")
        print("Input the filepath to the Non-tech Elective Courses List (JSON File): ", end="")
        path = input()
        self.nontech_electives = self.json_read(path)
        print()

    def ask_already_taken_courses(self):
        """
        Get list of courses already taken
        :return: None
        """
        print("Now please provide the list of your transferred courses and required courses you've taken already.")
        print("Please note that the format should be \n{ Course Number(ASFT-101): 0  }\n")
        print("Input the filepath here (JSON File): ", end="")
        path = input()
        self.already_taken = self.json_read(path)
        print()

    def ask_courses_want_to_take(self):
        """
        Get courses that are not mandatory
        :return: None
        """
        print("Finally, if there are any non-mandatory courses that you'd like to take, please provide them below.")
        print("Input the filepath to the non-mandatory courses you want to take here (JSON File): ", end="")
        path = input()
        self.courses_want_to_take = self.json_read(path)
        print()

    def ask_course_relationship(self):
        """
        To find out the pre-requisite of each course
        :return: None
        """
        print("Now, we finally need to know how courses are organized at your university.")
        print("Please provide us with the pre-requisites for all of the courses you're yet to take")
        print(
            "The format is:\n{Course Number: [Prereq1 Course Number, Prereq2 Course Number, ...], "
            "\nPrereq1: {Prereq for prereq1: Num of Credits} }")
        print("Input the filepath to the pre-requisites (JSON File): ", end="")
        path = input()
        self.course_relationship = self.json_read(path)
        print()

    def makeGraph(self):
        """
        Creates the graph for processing
        :return: An orderly list of courses based on how quickly they can be taken
        """
        self.g = Graph()
        for course, prereqs in self.course_relationship.items():
            if course in self.course_reqs:
                course_credit = self.course_reqs[course][1]
            elif course in self.tech_electives:
                course_credit = self.tech_electives[course][1]
            elif course in self.nontech_electives:
                course_credit = self.nontech_electives[course][1]
            elif course in self.courses_want_to_take:
                course_credit = self.courses_want_to_take[course][1]
            else:
                raise f"Credit Information not provided for {course}"

            for prereq in prereqs:
                if prereq in self.course_reqs:
                    prereq_credit = self.course_reqs[prereq][1]
                elif prereq in self.tech_electives:
                    prereq_credit = self.tech_electives[prereq][1]
                elif prereq in self.nontech_electives:
                    prereq_credit = self.nontech_electives[prereq][1]
                elif prereq in self.courses_want_to_take:
                    prereq_credit = self.courses_want_to_take[prereq][1]
                else:
                    raise f"Prerequisite Credit Error. No number of credits for {prereq} course provided"
                self.g.add_edge((prereq, prereq_credit), (course, course_credit))

        for k, v in self.course_reqs.items():
            self.g.add_vertex((k, v[1]))

        for k, v in self.tech_electives.items():
            self.g.add_vertex((k, v[1]))

        for k, v in self.nontech_electives.items():
            self.g.add_vertex((k, v[1]))

        for k, v in self.courses_want_to_take.items():
            self.g.add_vertex((k, v[1]))
    
    def ask_cost_per_credit(self):
        print("We are almost done. What is the per credit cost at your school? ")
        self.cost_per_credit = float(input())
        return self.cost_per_credit
    
    def recommend_courses(self):
        all_sems = []
        current_semester = []
        current_credits = 0

        already_taken = set(list(self.already_taken))

        for course, credit in self.g.sorted_courses:
            if course in already_taken:
                continue
                
            if current_credits + credit > 21:
                all_sems.append(current_semester)
                current_semester = [(course, credit)]
                current_credits = credit
                already_taken.add(course)
            else:
                current_semester.append((course, credit))
                current_credits += credit


        all_sems.append(current_semester)
        return all_sems


    def print_schedule(self):
        all_sems = self.recommend_courses()
        for i in range(1, len(all_sems) + 1):
            print(f'Semester {i}: ')
            print("Course \t       Credit")
            for course, credit in all_sems[i-1]:
                print(course, '\t', credit)
            print()
            print()
        if len(all_sems) > self.sems_remaining:
            print(f"We're sorry but you can't finish all the remaining courses in {self.sems_remaining} semesters. The fastest you could do is {len(all_sems)}.")


    def cost_analysis(self):
        schedule = self.recommend_courses()
        print("The cost v/s credit analysis for your schedule is as follows: ")  
        for count, sch in enumerate(schedule):
            total_credit = 0
            for course, credit in sch:
                total_credit += credit  
            print(f"Semester {count + 1}: ${self.cost_per_credit * total_credit}")


sems_remaining, major, total_credits, user = None, None, None, None
def main():
    global sems_remaining, major, total_credits, user
    print("How many semesters do you plan to be in school for? ")
    sems_remaining = int(input())
    print("What's your major? ")
    major = input()
    print("What's the total number of credits required for you to graduate? ")
    total_credits = int(input())
    user = UserInteraction(sems_remaining, major , total_credits)
    user.give_info()
    user.ask_required_courses()
    user.ask_nontech_electives()
    user.ask_tech_electives()
    user.ask_already_taken_courses()
    user.ask_courses_want_to_take()
    user.ask_course_relationship()
    user.ask_cost_per_credit()
    user.makeGraph()
    user.g.doTopologicalSort()


def speed_schedule():
    global sems_remaining, major, total_credits, user

    if not sems_remaining or not major or not total_credits:
        main()
    
    user.print_schedule()
    
def cost_v_credit():
    global sems_remaining, major, total_credits, user
    if not sems_remaining or not major or not total_credits:
        main()
    user.cost_analysis()

if __name__ == "__main__":
    cost_v_credit()
    speed_schedule()
    


