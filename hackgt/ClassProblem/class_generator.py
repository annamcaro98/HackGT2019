from random import *
def random_values():
    ECE_classes = ['ECE 2036','MATH 2551','PHYS 2212','MATH 1552','ECE 2035','ECE 2026', 'CHEM 1310', 'ECE 3072', 'ECE 2040', 'ECE 3040', 'ECE 3077', 'ECE 4320', 'ENG 1102', 'APPH 1050']
    CS_classes = ['CS 2340','CS 2119','CS 4641','CS 1332','CS 1331','PSYC 1101','CS 3240','CS 4476','CS 2050','CS 4649','PSYC 3040','CHEM 1310', 'ENG 1102', 'APPH 1050', 'MATH 1552']
    MSE_classes = ['ENG 1102', 'APPH 1050', 'MATH 1552', 'MATH 2551', 'PHYS 2112', 'MSE 2001', 'MSE 2021', 'MSE 3001', 'MSE 3025', 'MSE 3210', 'MSE 4002', 'MSE 3005', 'MSE 4775', 'MSE 3225']
    ME_classes = ['ME 1770', 'ME 2110', 'ME 3340', 'ME 3322', 'ME 3057', 'ME 4056', 'ME 3210', 'ME 3180', 'ME 4315', 'ME 3017', 'ME 3345', 'ME 2202', 'MATH 1552', 'MATH 2552', 'ENGL 1102']
    CHBE_classes = ['CHBE 2100', 'CHBE 2120', 'CHBE 2130', 'CHBE 3130', 'CHBE 3200', 'CHBE 3210', 'CHBE 3225', 'CHBE 4300', 'CHBE 4510', 'CHBE 4515', 'CHBE 4520', 'CHEM 2312', 'CS 1371', 'MATH 2552', 'CHEM 2311']
    Master_List = [{'ECE_class_list': ECE_classes}, {'CS_class_list' : CS_classes}, {'MSE_class_list': MSE_classes}, {'ME_class_list': ME_classes}, {'CHBE_class_list': CHBE_classes}]
    List_all = ['ECE 2036','MATH 2551','PHYS 2212','ECE 2035','ECE 2026', 'CHEM 1310', 'ECE 3072', 'ECE 2040', 'ECE 3040', 'ECE 3077', 'ECE 4320', 'ENG 1102', 'APPH 1050', 'CS 2340','CS 2119','CS 4641','CS 1332','CS 1331','PSYC 1101','CS 3240','CS 4476','CS 2050','CS 4649','PSYC 3040', 'MATH 1552', 'PHYS 2112', 'MSE 2001', 'MSE 2021', 'MSE 3001', 'MSE 3025', 'MSE 3210', 'MSE 4002', 'MSE 3005', 'MSE 4775', 'MSE 3225', 'ME 1770', 'ME 2110', 'ME 3340', 'ME 3322', 'ME 3057', 'ME 4056', 'ME 3210', 'ME 3180', 'ME 4315', 'ME 3017', 'ME 3345', 'ME 2202', 'MATH 2552', 'ENGL 1102', 'CHBE 2100', 'CHBE 2120', 'CHBE 2130', 'CHBE 3130', 'CHBE 3200', 'CHBE 3210', 'CHBE 3225', 'CHBE 4300', 'CHBE 4510', 'CHBE 4515', 'CHBE 4520', 'CHEM 2312', 'CS 1371', 'CHEM 2311']
    majorlist = ['ECE', 'CS', 'MSE', 'ME', 'CHBE']
    id = 111111110
    order = 0
    n = 0
    count = 0
    with open('values_file.csv', "w") as csvFile:
        while n <= 1000:
            sevenclasses = []
            id += 1
            order += 1
            major = choice(majorlist)
            credhrs = randrange(15, 86)
            gpa = round(uniform(1.0, 4.01), 2)
            for MCL in Master_List:
                for key, values in MCL.items():
                    if major in key:
                         sevenclasses += sample(values, 7)
            csvFile.write("{},{},{},{},{},".format(id,order,major,credhrs,gpa))
            for i in range(len(sevenclasses)-1):
                csvFile.write("{},".format(sevenclasses[i]))
            csvFile.write("{}\n".format(sevenclasses[-1]))
            n += 1
    csvFile.close()
    with open('class_size.csv', "w") as myFile:
        for c in List_all:
            count +=1
            class_size = randrange(20,101)
            x = c
            myFile.write("{},{},{}\n".format(count, x, class_size))
    myFile.close()
random_values()