class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def rate_lecturer(self, lecturer, course, grade):
        if int(grade) < 0 or int(grade) > 10:
            print("Оценка должна быть от 0 до 10")
        elif (isinstance(lecturer, Lecturer)
              and course in lecturer.courses_attached
              and course in self.courses_in_progress):
            if course in lecturer.course_rate:
                lecturer.course_rate[course] += [grade]
            else:
                lecturer.course_rate[course] = [grade]
        else:
            print("Вы не можете оценивать преподавателя, на лекции которого вы не закреплены!")

    def __str__(self):
        average_rate = get_average_rate(self.grades)
        return f'Имя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за домашние задания: {average_rate}\n'\
               f'Курсы в процессе изучения: {", ".join(self.courses_in_progress[::1])}\n'\
               f'Завершенные курсы: {", ".join(self.finished_courses[::1])}\n'

    def __gt__(self, other):
        average_rate_self = get_average_rate(self.grades)
        average_rate_other = get_average_rate(other.grades)

        return average_rate_self > average_rate_other

    def __lt__(self, other):
        average_rate_self = get_average_rate(self.grades)
        average_rate_other = get_average_rate(other.grades)

        return average_rate_self < average_rate_other


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):

    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.course_rate = {}

    def __str__(self):
        average_rate = get_average_rate(self.course_rate)

        return f'Имя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за лекции: {average_rate}\n'

    def __gt__(self, other):
        average_rate_self = get_average_rate(self.course_rate)
        average_rate_other = get_average_rate(other.course_rate)

        if average_rate_self > average_rate_other:
            answer = True
        else:
            answer = False

        return answer

    def __lt__(self, other):
        average_rate_self = get_average_rate(self.course_rate)
        average_rate_other = get_average_rate(other.course_rate)

        if average_rate_self < average_rate_other:
            answer = True
        else:
            answer = False

        return answer


class Reviewer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)

    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        return f'Имя: {self.name}\nФамилия: {self.surname}'


def get_average_rate(dict_for_rate):
    average_rate = 0
    count = 0

    for value in dict_for_rate.values():
        for mark in value:
            average_rate += mark
            count += 1

    average_rate = average_rate / count

    return average_rate


def average_students_rate_in_course(students_list, course_name):
    average_rate = get_average_rate_on_course(students_list, course_name)

    return average_rate


def average_lectures_rate_in_course(lectures_list, course_name):
    average_rate = get_average_rate_on_course(lectures_list, course_name)

    return average_rate


def get_average_rate_on_course(people_list, course_name):
    sum_rate = 0

    for human in people_list:
        if isinstance(human, Student):
            assessments = human.grades[course_name]
        else:
            assessments = human.course_rate[course_name]

        sum_rate += get_average_rate(dict.fromkeys([course_name], assessments))

    average_rate = sum_rate / len(people_list)

    return average_rate


best_student = Student('Ruoy', 'Eman', 'your_gender')
best_student.courses_in_progress += ['Python']
best_student.courses_in_progress += ['Java']
best_student.finished_courses += ['JavaScript']

best_student2 = Student('Ruoy2', 'Eman2', 'your_gender')
best_student2.courses_in_progress += ['Python']
best_student2.courses_in_progress += ['Java']
best_student2.finished_courses += ['Golang']

cool_reviewer = Reviewer('Some', 'Buddy')
cool_reviewer.courses_attached += ['Python']
cool_reviewer.courses_attached += ['Java']

cool_reviewer2 = Reviewer('Was', 'Told')
cool_reviewer2.courses_attached += ['Python']
cool_reviewer2.courses_attached += ['Java']

cool_lecturer = Lecturer('Guy', 'Ritchie')
cool_lecturer.courses_attached += ['Python']
cool_lecturer.courses_attached += ['Java']

cool_lecturer2 = Lecturer('Quentin', 'Tarantino')
cool_lecturer2.courses_attached += ['Python']
cool_lecturer2.courses_attached += ['Java']

best_student.rate_lecturer(cool_lecturer, best_student.courses_in_progress[0], 10)
best_student.rate_lecturer(cool_lecturer, best_student.courses_in_progress[1], 8)
best_student.rate_lecturer(cool_lecturer2, best_student.courses_in_progress[0], 7)
best_student.rate_lecturer(cool_lecturer2, best_student.courses_in_progress[1], 7)

best_student2.rate_lecturer(cool_lecturer, best_student.courses_in_progress[0], 9)
best_student2.rate_lecturer(cool_lecturer, best_student.courses_in_progress[1], 6)
best_student2.rate_lecturer(cool_lecturer2, best_student.courses_in_progress[0], 8)
best_student2.rate_lecturer(cool_lecturer2, best_student.courses_in_progress[1], 10)

cool_reviewer.rate_hw(best_student, 'Python', 7)
cool_reviewer.rate_hw(best_student, 'Java', 10)
cool_reviewer.rate_hw(best_student2, 'Python', 5)
cool_reviewer.rate_hw(best_student2, 'Java', 8)

cool_reviewer2.rate_hw(best_student, 'Python', 8)
cool_reviewer2.rate_hw(best_student, 'Java', 9)
cool_reviewer2.rate_hw(best_student2, 'Python', 10)
cool_reviewer2.rate_hw(best_student2, 'Java', 5)

print(best_student)
print(best_student2)
print(cool_lecturer)
print(cool_lecturer2)
print(cool_reviewer)
print(cool_reviewer2)
print(best_student > best_student2)
print(best_student < best_student2)
print(cool_lecturer2 > cool_lecturer)
print(cool_lecturer2 < cool_lecturer)
print(average_students_rate_in_course([best_student, best_student2], 'Python'))
print(average_lectures_rate_in_course([cool_lecturer, cool_lecturer2], 'Java'))
