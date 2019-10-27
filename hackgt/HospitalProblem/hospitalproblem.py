file = open("test.txt",'r')
data = file.readlines()
file.close()

for line in data:
    line = line.rstrip('\n')

num_patients = int(data[0])
num_hospitals = int(data[1])
patient_distances_from_hospitals = dict()
patient_problems = dict()
hospitalSlots = dict()


for i in range(1, num_hospitals+1):
    hospitalSlots[i] = 10
    
for i in range(1, num_patients + 1):
    patient_problems[i] = data[2].split(",")[i-1]
    distances_from_hospital_j = []
    for j in range(1, num_hospitals + 1):
        dist =float(data[3+i].split(",")[j-1])
        hospital_distance_pair = (j, dist)
        distances_from_hospital_j.append(hospital_distance_pair)
    distances_from_hospital_j.sort(key=lambda tup: tup[1])
    patient_distances_from_hospitals[i] = distances_from_hospital_j
hospital_ranked_specialties = dict()
for i in range(1, num_hospitals + 1):
    speciality_list = data[3].split(",")[i-1].split()
    hospital_ranked_specialties[i] = speciality_list
patient_preferences = dict()
for i in range(1, num_patients + 1):
    hospitals = []
    for j in range(0, len(patient_distances_from_hospitals[i])):
        tup = patient_distances_from_hospitals[i][j]
        hospitals.append(tup[0])
    patient_preferences[i] = hospitals
hospital_preferences = dict()
for i in range(1,num_hospitals+1):
    hospital_preferences[i] = []
    for j in hospital_ranked_specialties[i]:
        for k in range(1, num_patients+1):
            if patient_problems[k] == j:
                hospital_preferences[i] += [k,]
import copy
from collections import defaultdict
patients = sorted(patient_preferences.keys())
hospitals = sorted(hospital_preferences.keys())
def matchmaker():
    patientsfree = patients[:]
    patientslost = []
    matched = {}
    for hospitalName in hospitals:
        if hospitalName not in matched:
             matched[hospitalName] = list()
    patientprefers2 = copy.deepcopy(patient_preferences)
    hospitalprefers2 = copy.deepcopy(hospital_preferences)
    while patientsfree:
        patient = patientsfree.pop(0)
        #print("%s is on the market" % (patient))
        patientslist = patientprefers2[patient]
        hospital = patientslist.pop(0)
        #print("  %s (hospital's #%s) is checking out %s (patient's #%s)" % (patient, (hospitalprefers[hospital].index(patient)+1), hospital, (patientprefers[patient].index(hospital)+1)) )
        tempmatch = matched.get(hospital)
        if len(tempmatch) < hospitalSlots.get(hospital):
            # hospital's free
            if patient not in matched[hospital]:
                matched[hospital].append(patient)
                #print("    There's a spot! Now matched: %s and %s" % (patient.upper(), hospital.upper()))
        else:
            # The patient proposes to an full hospital!
            hospitalslist = hospitalprefers2[hospital]
            for (i, matchedAlready) in enumerate(tempmatch):
                if hospitalslist.index(matchedAlready) > hospitalslist.index(patient):
                    # hospital prefers new patient
                    if patient not in matched[hospital]:
                        matched[hospital][i] = patient
                        #print("  %s dumped %s (hospital's #%s) for %s (hospital's #%s)" % (hospital.upper(), matchedAlready, (hospitalprefers[hospital].index(matchedAlready)+1), patient.upper(), (hospitalprefers[hospital].index(patient)+1)))
                        if patientprefers2[matchedAlready]:
                            # Ex has more hospitals to try
                            patientsfree.append(matchedAlready)
                        else:
                            patientslost.append(matchedAlready)
                else:
                    # hospital still prefers old match
                    #print("  %s would rather stay with %s (their #%s) over %s (their #%s)" % (hospital, matchedAlready, (hospitalprefers[hospital].index(matchedAlready)+1), patient, (hospitalprefers[hospital].index(patient)+1)))
                    if patientslist:
                        # Look again
                        patientsfree.append(patient)
                    else:
                        patientslost.append(patient)
    #print
    #for lostsoul in patientslost:
    #    print('%s did not match' % lostsoul)
    return (matched, patientslost)
def check(matched):
    inversematched = defaultdict(list)
    for hospitalName in matched.keys():
        for patientName in matched[hospitalName]:
            inversematched[hospitalName].append(patientName)
    for hospitalName in matched.keys():
        for patientName in matched[hospitalName]:
            hospitalNamelikes = hospital_preferences[hospitalName]
            try:
                hospitalNamelikesbetter = hospitalNamelikes[:hospitalNamelikes.index(patientName)]
            except:
                hospitalNamelikesbetter = hospitalNamelikes[:]
            helikes = patient_preferences[patientName]
            helikesbetter = helikes[:helikes.index(hospitalName)]
            for patient in hospitalNamelikesbetter:
                for p in inversematched.keys():
                    if patient in inversematched[p]:
                        patientshospital = p
                patientlikes = patient_preferences[patient]
                                ## Not sure if this is correct
                try:
                    patientlikes.index(patientshospital)
                except ValueError:
                    continue
                if patientlikes.index(patientshospital) > patientlikes.index(hospitalName):
                    #print("%s and %s like each other better than "
                    #      "their present match: %s and %s, respectively"
                    #      % (hospitalName, patient, patientName, patientshospital))
                    return False
                
            for hospital in helikesbetter:
                hospitalspatients = matched[hospital]
                hospitallikes = hospital_preferences[hospital]
                for hospitalspatient in hospitalspatients:
                    if hospitallikes.index(hospitalspatient) > hospitallikes.index(patientName):
                        #print("%s and %s like each other better than "
                        #      "their present match: %s and %s, respectively"
                        #      % (patientName, hospital, hospitalName, hospitalspatient))
                        return False
    return True
(matched, patientslost) = matchmaker()
print('\nCouples:')
print('  ' + ',\n  '.join('Hospital %s is matched to Patient Numbers: %s' % couple
                          for couple in sorted(matched.items())))
print
print('Match stability check PASSED'
      if check(matched) else 'Match stability check FAILED')