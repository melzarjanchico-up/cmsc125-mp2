"""
    FILE:       cmsc125_mp2_chico.py
    ABOUT:      Implement the FCFS, SJF, SRPT, Priority and Round-robin scheduling.
    
    NAME:       Melzar Jan E. Chico
    COURSE:     CMSC125 B
    DATE:       2022 April 10

    TASK:       Machine Problem 2
    NOTES:      Process inputs are supplied via the given sample text files.
    CREDITS:    geeksforgeeks.org for the Round Robin and SRPT step-by-step algorithms
"""

class Process:
    def __init__(self, index:int, arrival:int, burst:int, priority:int) -> None:
        self.__index = index
        self.__arrival = arrival
        self.__burst = burst
        self.__priority = priority

    def at(self) -> int:
        return self.__arrival

    def bt(self) -> int:
        return self.__burst

    def pt(self) -> int:
        return self.__priority

    def __str__(self) -> str:
        return f'Process {str(self.__index).zfill(2)}'

    def __repr__(self) -> str: # for debug purposes
        processName = f'Process {str(self.__index).zfill(2)}'
        processDetails = f't={self.__burst}, d={self.__arrival}, p={self.__priority}'
        return f'<{processName}: {processDetails}>'

##### Scheduling Algorithms #####

###! first-come first-serve
def fcfs(processList:'list[Process]'):
    table_str = ''
    curr_wt = 0
    curr_tt = 0
    avg_wt = 0
    avg_tt = 0

    # iterate through the processes in order of position
    for process in processList:
        curr_tt += process.bt()
        avg_tt += curr_tt
        table_str += f'\t{process}\t{curr_wt}\t{curr_tt}\n'
        avg_wt += curr_wt
        curr_wt += process.bt()
    
    return {'str': table_str, 'avg_wt': avg_wt/len(processList), 'avg_tt': avg_tt/len(processList)}

###! shortest job first
def sjf(processList:'list[Process]'):
    table_str = ''
    curr_wt = 0
    curr_tt = 0
    avg_wt = 0
    avg_tt = 0

    # iterate through the processes in order of shortest burst time
    for process in sorted(processList, key = lambda process:process.bt()):
        curr_tt += process.bt()
        avg_tt += curr_tt
        table_str += f'\t{process}\t{curr_wt}\t{curr_tt}\n'
        avg_wt += curr_wt
        curr_wt += process.bt()
        
    return {'str': table_str, 'avg_wt': avg_wt/len(processList), 'avg_tt': avg_tt/len(processList)}

###! priority
def priority(processList:'list[Process]'):
    table_str = ''
    curr_wt = 0
    curr_tt = 0
    avg_wt = 0
    avg_tt = 0

    # iterate through the proceses in order of highest priority (lower value = higher priority)
    for process in sorted(processList, key = lambda process:process.pt()):
        curr_tt += process.bt()
        avg_tt += curr_tt
        table_str += f'\t{process}\t{curr_wt}\t{curr_tt}\n'
        avg_wt += curr_wt
        curr_wt += process.bt()
        
    return {'str': table_str, 'avg_wt': avg_wt/len(processList), 'avg_tt': avg_tt/len(processList)}

###! shortest remaining processing time
def srpt(processList:'list[Process]'):
    srpt_plist = [{'p': process, 'rb': process.bt(), 'wt': 0, 'tt': 0} for process in processList]
    done_processes = 0          # counts done processes in srpt_plist
    c_time = 0                  # holds current time
    min = 99999                 # holds the latest minimum burst time
    sp = None                   # holds current shortest process in srpt_plist
    sp_check = False            # checks if sp is not the same as last time

    while done_processes != len(srpt_plist):

        # find lowest burst time
        for process in srpt_plist:
            if ((process['p'].at() <= c_time) and (process['rb'] < min) and (process['rb'] > 0)):
                min = process['rb']
                sp = process
                sp_check = True
        
        # if shortest process still the same, just increment the time and continue
        if (not sp_check):
            c_time += 1
            continue
        
        # reduce remaining burst time of shortest process by one
        sp['rb'] -= 1

        # update min
        min = sp['rb']
        if (min == 0):
            min = 99999

        # if shortest process reaches zero (completely executed)
        if (sp['rb'] == 0):
            done_processes += 1
            sp_check = False

            # since this process is considered done when it reaches here
            # we can set final wt and tt values here
            fint = c_time + 1
            sp['wt'] = (fint - sp['p'].bt() - sp['p'].at())
            sp['tt'] = sp['p'].bt() + sp['wt']

            if (sp['wt'] < 0):
                sp['wt'] = 0
        
        c_time += 1

    table_str = ''
    avg_wt = 0
    avg_tt = 0

    for process in srpt_plist:
        avg_wt += process['wt']
        avg_tt += process['tt']
        table_str += f"\t{process['p']}\t{process['wt']}\t{process['tt']}\n"

    return {'str': table_str, 'avg_wt': avg_wt/len(processList), 'avg_tt': avg_tt/len(processList)}

##! round-robin
def roundrobin(processList:'list[Process]', quantum = 4):
    # 'p' = process, 'wt' = waiting time, 'tt' = turnaround time, 'rb' = remaining burst time
    rr_processList = [{'p': process, 'wt': 0, 'tt': 0, 'rb': process.bt()} for process in processList]
    c_time = 0

    while True:
        pending_check = True

        for process in rr_processList:

            # check if a process has remaining burst
            # if returns true, it means there are pending tasks
            if process['rb'] > 0:
                pending_check = False

                # check if remaining burst is lesser than quantum/timeslice
                if process['rb'] > quantum:
                    c_time += quantum
                    process['rb'] -= quantum
                else:
                    c_time = c_time + process['rb']
                    process['rb'] = 0
                    # since this process is considered done when it reaches here
                    # we can set final wt and tt values here
                    process['wt'] = c_time - process['p'].bt()
                    process['tt'] = process['p'].bt() + process['wt']
        
        if pending_check:
            break

    table_str = ''
    avg_wt = 0
    avg_tt = 0

    for process in rr_processList:
        avg_wt += process['wt']
        avg_tt += process['tt']
        table_str += f"\t{process['p']}\t{process['wt']}\t{process['tt']}\n"

    return {'str': table_str, 'avg_wt': avg_wt/len(processList), 'avg_tt': avg_tt/len(processList)}


##### Main Functions #####
def print_results(details):
    print(f'\t===== [{details[0]}] =====')
    print('\tPROCESSES\tWT(ms)\tTT(ms)\n')
    print(details[1]["str"])
    print(f'\tAverage WT: {"%.2f" % details[1]["avg_wt"]} ms')
    print(f'\tAverage TT: {"%.2f" % details[1]["avg_tt"]} ms')
    print()

def main():
    processList = []

    with open('./sample data/process1.txt') as f:
        # read the header line first
        f.readline()
        # read each line
        for line in f.readlines():
            row = line.split()
            processList.append(Process(int(row[0]), int(row[1]), int(row[2]), int(row[3])))

    fcfs_deets = ('FCFS SCHEDULING', fcfs(processList))
    sjf_deets = ('SJF SCHEDULING', sjf(processList))
    srpt_deets = ('SRPT SCHEDULING', srpt(processList))
    priority_deets = ('PRIORITY SCHEDULING', priority(processList))
    roundrobin_deets = ('ROUND ROBIN SCHEDULING', roundrobin(processList))

    # printing
    print('\n\t<<< LEGEND >>>')
    print('\tWT = waiting time (in milleseconds)')
    print('\tTT = turnaround time (in milleseconds)\n')

    print_results(fcfs_deets)
    print_results(sjf_deets)
    print_results(srpt_deets)
    print_results(priority_deets)
    print_results(roundrobin_deets)

    # algo evaluation
    algos = [fcfs_deets, sjf_deets, srpt_deets, priority_deets, roundrobin_deets]

    print('\t<<< EVALUATION >>>\n')

    curr_rank = 0
    print("\tLowest to Highest algorithm average waiting time:")
    for algo in sorted(algos, key = lambda algo: algo[1]["avg_wt"]):
        print(f'\t\t[{curr_rank+1}] {algo[0]} ({"%.2f" % algo[1]["avg_wt"]} ms)')
        curr_rank += 1
    print()

    curr_rank = 0
    print("\tLowest to Highest algorithm average turnaround time:")
    for algo in sorted(algos, key = lambda algo: algo[1]["avg_tt"]):
        print(f'\t\t[{curr_rank+1}] {algo[0]} ({"%.2f" % algo[1]["avg_tt"]} ms)')
        curr_rank += 1
    print()

main()