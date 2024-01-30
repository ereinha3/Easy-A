from gradeData import courseDict

crns = []
for subject, course in courseDict.items():
    for instance in course:
        crns.append(instance["crn"])

print(len(crns))
print(len(set(crns)))
