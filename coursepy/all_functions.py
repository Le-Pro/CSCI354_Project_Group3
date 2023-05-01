# from collections import deque
import json
import time


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
        # print(self.indegree_dict)
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
        raise "Cycle in the Graph!"


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
        print("The format of those file must be (unless specified): \n{Course Number: [Department, Credits]}")
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
            "The format is:\n{Course Number: {Prereq1: Prereq1 credits, Prereq2: Prereq2 Credits}, "
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

        return self.g.doTopologicalSort()


if __name__ == "__main__":
    user = UserInteraction(4, "Computer Science", 120)
    user.give_info()
    time.sleep(5)
    user.ask_required_courses()
    user.ask_nontech_electives()
    user.ask_tech_electives()
    user.ask_already_taken_courses()
    user.ask_courses_want_to_take()
    user.ask_course_relationship()
    print(user.makeGraph())
    print(user.g.adjacency_dict)
