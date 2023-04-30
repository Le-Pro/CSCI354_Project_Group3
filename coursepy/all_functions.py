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
    
    def ask_required_courses(self):
        print("So, we'd need to know what your degree requirements are in order to proceed.")
        print("Input the filepath to your course list (JSON File): ", end = "")
        path = input()
        # self.course_reqs = dict(open(path, "r"))
        print()
    
    def ask_tech_electives(self):
        print("If your degree requires any electives (technical), please provide them below.")
        print("Input the filepath to the Tech Elective Courses List (JSON File): ", end = "")
        path = input()
        # self.tech_electives = dict(open(path, "r"))
        print()
        
    def ask_nontech_electives(self):
        print("If your degree requires any electives (non-technical), please provide them below.")
        print("Input the filepath to the Non-tech Elective Courses List (JSON File): ", end = "")
        path = input()
        # self.nontech_electives = dict(open(path, "r"))
        print()
    
    
    def ask_already_taken_courses(self):
        print("Now please provide the list of your transferred courses and required courses you've taken already.")
        print("Input the filepath here (JSON File): ", end = "")
        path = input()
        # self.already_taken = dict(open(path, "r"))
        # self.remaining_credits = self.credits
        # for k, v in self.already_taken:
        #     if k in self.tech_electives or k in self.course_reqs or k in self.nontech_electives:
        #         self.remaining_credits -= v[1]
        print()
        
    
    def ask_courses_want_to_take(self):
        print("Finally, if there are any non-mandatory courses that you'd like to take, please provide them below.")
        print("Input the filepath to the non-mandatory courses you want to take here (JSON File): ", end = "")
        path = input()
        # self.courses_want_to_take = open(path, "r")
        print()
    
    def course_relationship(self):
        print("Now, we finally need to know how courses are organized at your university.")
        print("Please provide us with the pre-requisites for all of the courses you're yet to take")

        print("The format is:\n{Course Number: {Prereq1: Prereq1 credits, Prereq2: Prereq2 Credits}, \nPrereq1: {Prereq for prereq1: Num of Credits} }")
        print("Input the filepath to the pre-requisites (JSON File): ", end = "")
        path = input()
        # self.course_relationship = open(path, "r")
        print()

if __name__ == "__main__":
    user = UserInteraction(4, "Computer Science", 120)
    user.give_info()
    user.ask_required_courses()
    user.ask_already_taken_courses()
    user.ask_courses_want_to_take()
    user.ask_nontech_electives()
    user.ask_tech_electives()
    user.course_relationship()