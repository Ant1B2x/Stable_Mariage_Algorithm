class Students:
    def __init__(self, name: str):
        self.__name : str = name
        self.__schools_rank : list = []

    def get_name(self):
        return self.__name

    def get_schools_rank(self):
        return self.__schools_rank

    def get_first_school_name(self):
        return self.__schools_rank[1].get_name()

    def set_schools_rank(self, schools_rank : list):
        self.__schools_rank = schools_rank

    def serenade_school(self):
        self.__schools_rank[1].rank_student(self)

    def school_refused(self):
        self.__schools_rank.pop(1)

class Schools:
    def __init__(self, name: str, nmax_students : int):
        self.__name : str = name
        self.__nmax_students = nmax_students
        self.__students_rank : list = []
        self.__serenading_students : list = []
        self.__nb_serenades : int = 0

    def get_name(self):
        return self.__name

    def get_nmax_students(self):
        return self.__nmax_students

    def get_nb_serenades(self):
        return self.__nb_serenades

    def set_students_rank(self, students_rank : list):
        self.__students_rank = students_rank
        self.__serenading_students = [False] * len(self.__students_rank)

    def get_student_rank(self, student : Students):
        i = 0
        while i < len(self.__students_rank) and self.__students_rank[i] != student:
            i += 1
        return i

    def rank_student (self, student : Students):
        self.__serenading_students[self.get_student_rank(student) - 1] = True
        self.__nb_serenades += 1

    def reply_to_students(self):
        accepted_students : int = 0
        for i in range(len(self.__serenading_students)):
            if accepted_students < self.__nmax_students and self.__serenading_students[i]:
                accepted_students += 1
            elif self.__serenading_students[i]:
                self.__students_rank[i].school_refused()

    def reset_serenades(self):
        self.__nb_serenades = 0
        self.__serenading_students = [False] * len(self.__students_rank)

    def get_serenading_students(self):
        serenading_students = []
        for i in range(len(self.__serenading_students)):
            if self.__serenading_students[i]:
                serenading_students.append(self.__students_rank[i])
        return serenading_students

student1 = Students("Esteban")
student2 = Students("Antoine")
student3 = Students("Yvan")

school1 = Schools("N7", 1)
school2 = Schools("X", 1)
school3 = Schools("A7", 1)

student1.set_schools_rank([school2, school1, school3])
student2.set_schools_rank([school1, school2, school3])
student3.set_schools_rank([school1, school2, school3])

school1.set_students_rank([student1, student3, student2])
school2.set_students_rank([student2, student1, student3])
school3.set_students_rank([student3, student1, student2])

serenade_end = False
while not serenade_end:
    serenade_end = True
    for student in [student1, student2, student3]:
        student.serenade_school()
    for school in [school1, school2, school3]:
        school.reply_to_students()
    for school in [school1, school2, school3]:
        if school.get_nmax_students() > school.get_nb_serenades():
            serenade_end = False
        school.reset_serenades()

for student in [student1, student2, student3]:
    print(f"{student.get_name()} : {student.get_first_school_name()}")