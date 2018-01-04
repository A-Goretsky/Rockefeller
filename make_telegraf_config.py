oid_s = open("liebert_oids.txt", "r")
names = open("oid_name.txt", "r")
result = open("final_test1.txt", "r+")

name_list = names.read().split('\n')
oid_list = oid_s.read().split('\n')

ctr = 0
for single_name in name_list:
    temp = ""
    temp = single_name
    temp2 = ""
    i = -1
    try:
        i = name_list.index(single_name, ctr + 1)
        temp2 = name_list[i]
        if single_name == temp2:
            temp += "_0"
            temp2 += "_1"
            name_list[ctr] = temp
            name_list[i] = temp2
    except:
        pass
    ctr += 1

for x in range(0, 273):
    name_str = ""
    name_split = name_list[x].lower().split(' ')
    for i in range(0, len(name_split)):
        #print name_split[i]
        if name_split[i] == '-':
            name_str += '-'
        else:
            name_str += name_split[i]
            if (i != len(name_split) - 1):
                if (name_split[i + 1] != '-'):
                    name_str += '_'
    correct = '[[inputs.snmp.field]]\nname = "' + name_str + '"\n' + 'oid = "' + oid_list[x] + '"\n\n'
    result.write(correct)

oid_s.close()
names.close()
result.close()
