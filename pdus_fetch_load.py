# 03032022 Julius Kaplan 755675@gmail.com
# Getting information about the load connected to the PDUs
# Model: AP8953
# Model: Eaton EPDU MA 0U (309 32A 3P)18XC13:6XC19
# Model: Enlogic EN2810


import csv
import datetime

now = datetime.datetime.now()
print("Current date and time : ")
print(now.strftime("%Y-%m-%d %H:%M:%S"))

# Open the file with eaton pdu list
eaton_list = open("eaton_pdu_list.txt", "r").read().splitlines()
eaton_list = list(eaton_list)
print("=======================:: EATON :: ===============================")
print(eaton_list)


apc_list = open("apc_pdu_list.txt", "r").read().splitlines()
apc_list = list(apc_list)
print("======================:: APC ::===================================")
print(apc_list)



enlogic_list = open("enlogic_pdu_list.txt", "r").read().splitlines()
enlogic_list = list(enlogic_list)
print("====================:: ENLOGIC ::=================================")
print(enlogic_list)
print("==================================================================")


SNMP_PORT = '161'
SNMP_COMMUNITY = 'public'


def snmpget(oid, *more_oids):
    from pysnmp.entity.rfc3413.oneliner import cmdgen

    global SNMP_PORT
    global SNMP_COMMUNITY

    cmdGen = cmdgen.CommandGenerator()

    errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
        cmdgen.CommunityData(SNMP_COMMUNITY, mpModel=0),
        cmdgen.UdpTransportTarget((SNMP_HOST, SNMP_PORT)),
        oid,
        *more_oids
    )

    # Predefine our results list
    results = []

    # Check for errors and print out results
    if errorIndication:
        print(errorIndication)
    else:
        if errorStatus:
            print('%s at %s' % (
                errorStatus.prettyPrint(),
                errorIndex and varBinds[int(errorIndex) - 1] or '?'
            )
                  )
        else:
            for name, val in varBinds:
                results.append(val)

        if len(results) == 1:
            return results[0]
        else:
            return results


for line in eaton_list:
    print(line)
    SNMP_HOST = line
    print("=========================================================")
    HOSTNAME = snmpget('.1.3.6.1.4.1.534.6.6.7.1.2.1.6.0')
    print("Hostname:", HOSTNAME)
    MODEL = snmpget('.1.3.6.1.4.1.534.6.6.7.1.2.1.2.0')
    print("Model:", MODEL)
    SERIAL = snmpget('.1.3.6.1.4.1.534.6.6.7.1.2.1.4.0')
    print("Serial:", SERIAL)
    LOAD = snmpget('.1.3.6.1.4.1.534.6.6.7.3.5.1.4.0.1')
    print("Total Power load (W):", LOAD)
    print("=========================================================")
    csvRow = [(now.strftime("%Y-%m-%d")), HOSTNAME, MODEL, SERIAL, LOAD]
    csvfile = "pdu_output_2.csv"
    with open(csvfile, "a") as fp:
        wr = csv.writer(fp, dialect='excel')
        wr.writerow(csvRow)

for line in apc_list:
    print(line)
    print("=========================================================")
    SNMP_HOST = line
    HOSTNAME = snmpget('.1.3.6.1.4.1.318.1.1.26.4.4.1.3.1')
    print("Hostname:", HOSTNAME)
    MODEL = snmpget('.1.3.6.1.4.1.318.1.1.26.2.1.8.1')
    print("Model:", MODEL)
    SERIAL = snmpget('.1.3.6.1.4.1.318.1.1.26.2.1.9.1')
    print("Serial:", SERIAL)
    LOAD = snmpget('.1.3.6.1.4.1.318.1.1.26.11.2.0')
    print("Total Power load (W):", LOAD)
    print("=========================================================")
    csvRow = [(now.strftime("%Y-%m-%d")), HOSTNAME, MODEL, SERIAL, LOAD]
    csvfile = "pdu_output_2.csv"
    with open(csvfile, "a") as fp:
        wr = csv.writer(fp, dialect='excel')
        wr.writerow(csvRow)

for line in enlogic_list:
    print(line)
    SNMP_HOST = line
    print("=========================================================")
    HOSTNAME = snmpget('1.3.6.1.4.1.38446.1.2.3.1.2.1')
    print("Hostname:", HOSTNAME)
    MODEL    = snmpget('1.3.6.1.4.1.38446.1.1.2.1.11.1')
    print("Model:", MODEL)
    SERIAL   = snmpget('1.3.6.1.4.1.38446.1.1.2.1.12.1')
    print("Serial:", SERIAL)
    LOAD =     snmpget('1.3.6.1.4.1.38446.1.2.4.1.4.1')
    print("Total Power load (W):", LOAD)
    print("=========================================================")
    csvRow = [(now.strftime("%Y-%m-%d")), HOSTNAME, MODEL, SERIAL, LOAD]
    csvfile = "pdu_output_2.csv"
    with open(csvfile, "a") as fp:
        wr = csv.writer(fp, dialect='excel')
        wr.writerow(csvRow)