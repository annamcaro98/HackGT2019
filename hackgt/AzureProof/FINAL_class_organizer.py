import copy
from collections import defaultdict
import pyodbc
server = 'rags.database.windows.net'
database = 'ClassMatch'
username = 'sam'
password = 'Typhoon123'
driver= '{ODBC Driver 17 for SQL Server}'
cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()
cursor.execute("SELECT * FROM values_file")
data = cursor.fetchone()

    
student_rank = dict()
class_size = dict()
class_rank = dict()
student_properties = dict()
course_id = dict()

while data:
    print(data)
    
    student_properties[data[0]]= [data[i] for i in range(1,5)]
    """
    0 ID
    1 ORDER
    2 Major *0.35
    3 Credit Hours *0.35
    4 GPA *0.3
    
    """
    student_rank[data[0]] = [data[i] for i in range(5, len(data))]
    data = cursor.fetchone()


cursor.execute("SELECT * FROM class_size")
data = cursor.fetchone()
while data:
    course_id[data[1]] = int(data[0])
    class_size[data[1]] = int(data[2])
    data = cursor.fetchone()


student_list = []
for student in student_properties:
     studentweight = (float(student_properties[student][2])/120)*0.35 + (float(student_properties[student][3])/4)*0.3
     student_list.append([student, studentweight])

for period in class_size:
    for student in student_list:
        if student_properties[student[0]][1] == period.split()[0]: student[1] += 0.35
    student_list.sort(key = lambda x: x[1], reverse = True )
    class_rank[period] = [i[0] for i in student_list]
    
studprefers = student_rank

clsrmprefers = class_rank

clsrmSlots = class_size


studs = sorted(studprefers.keys())
clsrms = sorted(clsrmprefers.keys())


def matchmaker():
    studsfree = studs[:]
    studslost = []
    matched = {}
    for clsrmName in clsrms:
        if clsrmName not in matched:
             matched[clsrmName] = list()
    studprefers2 = copy.deepcopy(studprefers)
    clsrmprefers2 = copy.deepcopy(clsrmprefers)
    while studsfree:
        stud = studsfree.pop(0)
        #print("%s is on the market" % (stud))
        studslist = studprefers2[stud]
        if studslist:
            clsrm = studslist.pop(0)
        #print("  %s (clsrm's #%s) is checking out %s (stud's #%s)" % (stud, (clsrmprefers[clsrm].index(stud)+1), clsrm, (studprefers[stud].index(clsrm)+1)) )
        tempmatch = matched.get(clsrm)
        if len(tempmatch) < clsrmSlots.get(clsrm):
            # clsrm's free
            if stud not in matched[clsrm]:
                matched[clsrm].append(stud)
                print("There's a spot! Now matched: %s and %s\n" % (stud.upper(), clsrm.upper()))
        else:
            # The stud proposes to an full clsrm!
            clsrmslist = clsrmprefers2[clsrm]
            for (i, matchedAlready) in enumerate(tempmatch):
                if clsrmslist.index(matchedAlready) > clsrmslist.index(stud):
                    # clsrm prefers new stud
                    if stud not in matched[clsrm]:
                        matched[clsrm][i] = stud
                        print("  %s dumped %s (class's #%s) for %s (class's #%s)\n" % (clsrm.upper(), matchedAlready, (clsrmprefers[clsrm].index(matchedAlready)+1), stud.upper(), (clsrmprefers[clsrm].index(stud)+1)))
                        if studprefers2[matchedAlready]:
                            # Ex has more clsrms to try
                            studsfree.append(matchedAlready)
                        else:
                            studslost.append(matchedAlready)
                else:
                    # clsrm still prefers old match
                    print("  %s would rather stay with %s (their #%s) over %s (their #%s)\n" % (clsrm, matchedAlready, (clsrmprefers[clsrm].index(matchedAlready)+1), stud, (clsrmprefers[clsrm].index(stud)+1)))
                    if studslist:
                        # Look again
                        studsfree.append(stud)
                    else:
                         studslost.append(stud)
            # clsrm's free

                #print("    There's a spot! Now matched: %s and %s" % (stud.upper(), clsrm.upper()))
    #print
    #for lostsoul in studslost:
    #    print('%s did not match' % lostsoul)
    return (matched, studslost)
def check(matched):
    inversematched = defaultdict(list)
    for clsrmName in matched.keys():
        for studName in matched[clsrmName]:
            inversematched[clsrmName].append(studName)
    for clsrmName in matched.keys():
        for studName in matched[clsrmName]:
            clsrmNamelikes = clsrmprefers[clsrmName]
            clsrmNamelikesbetter = clsrmNamelikes[:clsrmNamelikes.index(studName)]
            helikes = studprefers[studName]
            helikesbetter = helikes[:helikes.index(clsrmName)]
            for stud in clsrmNamelikesbetter:
                for p in inversematched.keys():
                    if stud in inversematched[p]:
                        studsclsrm = p
                studlikes = studprefers[stud]
                                ## Not sure if this is correct
                try:
                    studlikes.index(studsclsrm)
                except ValueError:
                    continue
                if studlikes.index(studsclsrm) > studlikes.index(clsrmName):
                    #print("%s and %s like each other better than "
                    #      "their present match: %s and %s, respectively"
                    #      % (clsrmName, stud, studName, studsclsrm))
                    return False
            for clsrm in helikesbetter:
                clsrmsstuds = matched[clsrm]
                clsrmlikes = clsrmprefers[clsrm]
                for clsrmsstud in clsrmsstuds:
                    if clsrmlikes.index(clsrmsstud) > clsrmlikes.index(studName):
                        #print("%s and %s like each other better than "
                        #      "their present match: %s and %s, respectively"
                        #      % (studName, clsrm, clsrmName, clsrmsstud))
                        return False
    return True

ultimate_match = {}
for i in range(4):
    print('\nPlay-by-play:')
    (matched, studslost) = matchmaker()
#    print('\nCouples:')
#    print('  ' + ',\n  '.join('%s is matched to %s' % couple
#                              for couple in sorted(matched.items())))
    print("\n Check Source folder for 'output.txt' containing full class listings!")
    for key,values in matched.items():
        if ultimate_match.get(key, False):
            ultimate_match[key] += values
        else:
            ultimate_match[key] = values
        clsrmSlots[key] -= len(values)
        for value in values:
            try:
                student_rank[value].remove(key)
            except:
                pass
try:
    sql_command = """DROP TABLE autoschedule;"""
    cursor.execute(sql_command)
except:
    pass
            
sql_command = """
CREATE TABLE autoschedule ( 
CourseID INTEGER PRIMARY KEY,
Course VARCHAR(255),
RegisteredStudents VARCHAR(8000));"""

cursor.execute(sql_command)


for key, value in ultimate_match.items():
    value = [int(i) for i in value]
    format_str = """INSERT INTO autoschedule (CourseID, Course, RegisteredStudents)
    VALUES ({a}, '{b}','{c}');"""
    
    sql_command = format_str.format(a = course_id[key], b = key, c = value)
    print(sql_command)
    cursor.execute(sql_command)
cnxn.commit()
cursor.close()
cnxn.close()
