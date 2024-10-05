import pandas as pd
import shlex

list_cols = ["last_name", "first_name", "grade", "classroom", "bus", "gpa"]
teacher_cols = ["teacher_last", "teacher_first", "classroom"]

filepath = "list.txt"
filepath2 = "teachers.txt"

try:
    df_students = pd.read_csv(filepath, names=list_cols, header=None)
    df_teachers = pd.read_csv(filepath2, names=teacher_cols, header=None)

    for index, row in df_teachers.iterrows():
        teacher_first = row["teacher_first"]
        teacher_last = row["teacher_last"]
        classroom = row["classroom"]

        df_students.loc[df_students['classroom'] == classroom, 'teacher_last'] = teacher_last
        df_students.loc[df_students['classroom'] == classroom, 'teacher_first'] = teacher_first

    try:
        df_students["grade"] = df_students["grade"].astype(int)
        df_students["classroom"] = df_students["classroom"].astype(int)
        df_students["bus"] = df_students["bus"].astype(int)
        df_students["gpa"] = df_students["gpa"].astype(float)
    except ValueError:
        print("Error converting some columns to the appropriate data types. Check your data.")

    def callSchoolSearch():
        while True:
            command = input("Please input your command:\n")
            if command.lower() == "q":
                break
            schoolSearch(command)

    def schoolSearch(command):
        inputArr = shlex.split(command)

        if inputArr[0] in ["S:", "Student:"]:
            search_student(inputArr)
        elif inputArr[0] in ["T:", "Teacher:"]:
            search_teacher(inputArr)
        elif inputArr[0] in ["G:", "Grade:"]:
            if len(inputArr) > 2 and inputArr[2] == "H":  # Handle 'high GPA' in grade
                search_grade_high_gpa(inputArr)
            elif len(inputArr) > 2 and inputArr[2] == "L":  # Handle 'low GPA' in grade
                search_grade_low_gpa(inputArr) 
            elif len(inputArr) > 2 and inputArr[2] == "T":  # Handle 'teachers teaching grade'
                search_grade_teachers(inputArr)
            else:
                search_grade(inputArr)
        elif inputArr[0] in ["B:", "Bus:"]:
            search_bus(inputArr)
        elif inputArr[0] in ["C:", "Classroom:"]:
            search_classroom_students(inputArr)
        elif inputArr[0] == "FindTeacher:":
            search_classroom_teachers(inputArr)
        elif inputArr[0] == "GradeTeachers:":
            search_grade_teachers(inputArr)
        elif inputArr[0] in ["E", "Enrollments"]:
            report_enrollments()
        elif inputArr[0] in ["Average:", "Avg:"]:
            search_average(inputArr)
        elif inputArr[0] in ["A:", "Analytics:"]:
            run_analytics(inputArr)
        elif inputArr[0] in ["I", "Info"]:
            displayInfo()
        elif inputArr[0].lower() in ["q", "Q"]:
            print("Exiting program.")
            exit()
        else:
            print("Invalid command, please try again.")

    def search_student(inputArr):
        printBusRoute = len(inputArr) == 3 and (inputArr[2] in ["Bus", "B"])
        last_name = inputArr[1]
        students = df_students[df_students['last_name'] == last_name]

        for i, student in students.iterrows():
            if printBusRoute:
                print(f"{student['last_name']}, {student['first_name']}, Bus: {student['bus']}")
            else:
                print(f"{student['last_name']}, {student['first_name']}, Grade: {student['grade']}, "
                      f"Classroom: {student['classroom']}, Teacher: {student['teacher_last']}, {student['teacher_first']}")

    def search_teacher(inputArr):
        teacher_last = inputArr[1]
        classrooms = df_teachers[df_teachers['teacher_last'] == teacher_last]['classroom']
        for classroom in classrooms:
            students = df_students[df_students['classroom'] == classroom]
            for i, student in students.iterrows():
                print(f"{student['last_name']}, {student['first_name']}")

    def search_grade(inputArr):
        grade = int(inputArr[1])
        students = df_students[df_students['grade'] == grade]
        for i, student in students.iterrows():
            print(f"{student['last_name']}, {student['first_name']}")

    def search_bus(inputArr):
        if len(inputArr) < 2:
            print("Error: Please provide a bus number.")
            return
        try:
            bus = int(inputArr[1])
        except ValueError:
            print("Error: Bus number should be a valid number.")
            return
        students = df_students[df_students['bus'] == bus]
        if students.empty:
            print(f"No students found for bus route '{bus}'.")
            return
        for i, student in students.iterrows():
            print(f"{student['last_name']}, {student['first_name']}, Grade: {student['grade']}, Classroom: {student['classroom']}")

    def search_classroom_students(inputArr):
        if len(inputArr) < 2:
            print("Error: Please provide a classroom number.")
            return
        classroom = inputArr[1].strip()
        try:
            classroom_int = int(classroom)
        except ValueError:
            print("Error: Classroom number should be a valid number.")
            return
        students = df_students[df_students['classroom'] == classroom_int] 
        if students.empty:
            print(f"No students found for classroom '{classroom_int}'.")
            return
        for i, student in students.iterrows():
            print(f"{student['last_name']}, {student['first_name']}")

    def search_classroom_teachers(inputArr):
        if len(inputArr) < 2:
            print("Error: Please provide a classroom number.")
            return
        classroom = inputArr[1].strip()
        try:
            classroom_int = int(classroom) 
        except ValueError:
            print("Error: Classroom number should be a valid number.")
            return
        teachers = df_teachers[df_teachers['classroom'] == classroom_int]
        if not teachers.empty:
            for i, teacher in teachers.iterrows():
                print(f"Teacher: {teacher['teacher_last']}, {teacher['teacher_first']}")
        else:
            print(f"No teachers found for classroom {classroom_int}")

    def search_grade_teachers(inputArr):
        grade = int(inputArr[1])
        classrooms = df_students[df_students['grade'] == grade]['classroom'].unique()
        teachers = df_teachers[df_teachers['classroom'].isin(classrooms)]
        for i, teacher in teachers.iterrows():
            print(f"Teacher: {teacher['teacher_last']}, {teacher['teacher_first']}")

    def report_enrollments():
        enrollments = df_students.groupby('classroom').size().reset_index(name='enrollment')
        enrollments = enrollments.sort_values(by='classroom')
        for i, row in enrollments.iterrows():
            print(f"Classroom: {row['classroom']}, Students: {row['enrollment']}")

    def run_analytics(inputArr):
        if inputArr[1] == "GradeGPA":
            report_gpa_by_grade()
        elif inputArr[1] == "TeacherGPA":
            report_gpa_by_teacher()
        elif inputArr[1] == "BusGPA":
            report_gpa_by_bus()

    def report_gpa_by_grade():
        gpa_by_grade = df_students.groupby('grade')['gpa'].mean().reset_index()
        for i, row in gpa_by_grade.iterrows():
            print(f"Grade: {row['grade']}, Average GPA: {round(row['gpa'], 2)}")

    def report_gpa_by_teacher():
        df_students['classroom'] = df_students['classroom'].astype(str).str.strip()
        df_teachers['classroom'] = df_teachers['classroom'].astype(str).str.strip()
        merged_df = pd.merge(df_students, df_teachers, on='classroom', how='left')
        merged_df.rename(columns={'teacher_last_y': 'teacher_last', 'teacher_first_y': 'teacher_first'}, inplace=True)
        gpa_by_teacher = merged_df.groupby(['teacher_last', 'teacher_first'])['gpa'].mean().reset_index()
        if gpa_by_teacher.empty:
            print("No data available for GPA by teacher.")
        else:
            for i, row in gpa_by_teacher.iterrows():
                print(f"Teacher: {row['teacher_last']} {row['teacher_first']}, Average GPA: {round(row['gpa'], 2)}")

    def report_gpa_by_bus():
        gpa_by_bus = df_students.groupby('bus')['gpa'].mean().reset_index()
        for i, row in gpa_by_bus.iterrows():
            print(f"Bus: {row['bus']}, Average GPA: {round(row['gpa'], 2)}")

    def search_grade_high_gpa(inputArr):
        grade = int(inputArr[1])
        students = df_students[df_students['grade'] == grade]
        if not students.empty:
            highest_gpa_student = students.loc[students['gpa'].idxmax()]
            print(f"{highest_gpa_student['last_name']}, {highest_gpa_student['first_name']}, "
                  f"{round(highest_gpa_student['gpa'], 2)}, {highest_gpa_student['teacher_last']}, {highest_gpa_student['classroom']}")
        else:
            print(f"No students found for grade {grade}.")

    def search_grade_low_gpa(inputArr):
        grade = int(inputArr[1])
        students = df_students[df_students['grade'] == grade]
        if not students.empty:
            lowest_gpa_student = students.loc[students['gpa'].idxmin()]
            print(f"{lowest_gpa_student['last_name']}, {lowest_gpa_student['first_name']}, "
                  f"{round(lowest_gpa_student['gpa'], 2)}, {lowest_gpa_student['teacher_last']}, {lowest_gpa_student['classroom']}")
        else:
            print(f"No students found for grade {grade}.")

    def search_average(inputArr):
        grade = int(inputArr[1])
        avg_gpa = df_students[df_students['grade'] == grade]['gpa'].mean()
        print(f"Grade: {grade}, Average GPA: {round(avg_gpa, 2)}")

    def displayInfo():
        for grade in range(0, 7):
            print(str(grade) + ": " + str((df_students['grade'] == grade).sum()))

    callSchoolSearch()

except FileNotFoundError:
    print("Invalid file, check your filepath.")
except pd.errors.ParserError:
    print("Bad CSV formatting")