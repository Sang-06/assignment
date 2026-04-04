def students(student_list):
    result = {} #dictionary to store final output

    for student in student_list:
        name = student['name']
        score = student['score']

        #determine grade using if-elif-else
        if score >= 90:
            grade = 'A'
        elif score >= 75:
            grade = 'B'
        elif score >= 60:
            grade = 'C'
        else:
            grade = 'F'
        
        result[name] = grade # add to dictionary

    return result

students_list = [
          {'name': 'Alice', 'score': 92},
          {'name': 'Bob', 'score': 74},
          {'name': 'Carol', 'score': 61},
          {'name': 'Dave', 'score': 45}
  ] 

print(students(students_list))