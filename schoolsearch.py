import pandas as pd

cols = ["last_name", "first_name", "grade", "classroom", "bus", "gpa", "teacher_last", "teacher_first"]

filepath = "students.txt"
df = pd.read_csv(filepath, names=cols, header=None)

df["grade"] = df["grade"].astype(int)
df["classroom"] = df["classroom"].astype(int)
df["bus"] = df["bus"].astype(int)
df["gpa"] = df["gpa"].astype(float)

def callSchoolSearch():
    schoolSearch(input("Please input your command:\n"))

def schoolSearch(input):
    firstLetter = input[0]
    inputArr = input.split()
    printBusRoute = False

    if (firstLetter == "S" or inputArr[0] == "Student:"):
        # error checks to ensure wrong num of args not passed?
        if (len(inputArr) == 3):
            # Re initiates call
            if (inputArr[2][0] != "B" and inputArr[2] != "Bus"):
                callSchoolSearch()
            printBusRoute = True

        for index in df.index:
            lastName = df.loc[index, "last_name"]
            if (lastName == inputArr[1]):
                if (printBusRoute == False):
                    print(df.loc[index, "last_name"] + ", " + df.loc[index, "first_name"] + ", " + str(df.loc[index, "grade"]) + ", " + str(df.loc[index, "classroom"]) + ", " + df.loc[index, "teacher_last"] + ", " + df.loc[index, "teacher_first"])
                else:
                    print(df.loc[index, "last_name"] + ", " + df.loc[index, "first_name"] + ", " + str(df.loc[index, "bus"]))
            
    if (firstLetter == "T" or inputArr[0] == "Teacher:"):
        for index in df.index:
            teacherLast = df.loc[index, "teacher_last"]
            if (teacherLast == inputArr[1]):
                print(df.loc[index, "last_name"] + ", " + df.loc[index, "first_name"])
    
    if (firstLetter == "G" or inputArr[0] == "Grade:"):
        if (len(inputArr) == 2):
            for index in df.index:
                grade = df.loc[index, "grade"]
                if (grade.astype(str) == inputArr[1]):
                    print(df.loc[index, "last_name"] + ", " + df.loc[index, "first_name"])
        elif (len(inputArr) == 3):
            searchHighest = True

            if (inputArr[2][0] == "L" or inputArr[2] == "Low"):
                searchHighest = False
            
            grade = int(inputArr[1])
            extremeGpa = 0

            if (searchHighest):
                extremeGpa = df[df['grade'] == grade]['gpa'].max()
            else:
                extremeGpa = df[df['grade'] == grade]['gpa'].min()

            for index in df.index:
                grd = df.loc[index, "grade"]
                gpa = df.loc[index, "gpa"]
                if (searchHighest):
                    if (grd == grade and gpa >= extremeGpa):
                        print(df.loc[index, "last_name"] + ", " + df.loc[index, "first_name"] + ", " + str(df.loc[index, "gpa"]) + ", " + df.loc[index, "teacher_last"] + ", " + df.loc[index, "teacher_first"] + ", " + str(df.loc[index, "classroom"]))
                else:
                    if (grd == grade and gpa <= extremeGpa):
                        print(df.loc[index, "last_name"] + ", " + df.loc[index, "first_name"] + ", " + str(df.loc[index, "gpa"]) + ", " + df.loc[index, "teacher_last"] + ", " + df.loc[index, "teacher_first"] + ", " + str(df.loc[index, "classroom"]))

    if (firstLetter == "B" or inputArr[0] == "Bus:"):
        for index in df.index:
            bus = df.loc[index, "bus"]
            if (bus.astype(str) == inputArr[1]):
                print(df.loc[index, "last_name"] + ", " + df.loc[index, "first_name"] + ", " + str(df.loc[index, "grade"]) + ", " + str(df.loc[index, "classroom"]))
    
    if (firstLetter == "A" or inputArr[0] == "Average:"):
        grade = int(inputArr[1])
        averageGpa = round(df[df['grade'] == grade]['gpa'].mean(), 2)
        print(str(grade) + ", " + str(averageGpa))

    if (firstLetter == "I"):
        for grade in range(0, 7):
            print(str(grade) + ": " + str((df['grade'] == grade).sum()))
                                                             
    if (firstLetter == "Q"):
        return
    
    callSchoolSearch()

callSchoolSearch()
