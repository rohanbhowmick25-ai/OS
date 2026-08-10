from collections import deque

# -----------------------------
# Process Class
# -----------------------------
class Process:
    def __init__(self, pid, arrival, burst):
        self.pid = pid
        self.arrival = arrival
        self.burst = burst
        self.remaining = burst
        self.completion = 0
        self.waiting = 0
        self.turnaround = 0
        self.response = -1


# -----------------------------
# FCFS Scheduling
# -----------------------------
def fcfs(processes):
    time = 0
    context_switches = 0
    gantt = []

    for p in processes:
        if time < p.arrival:
            time = p.arrival

        if gantt:
            context_switches += 1

        p.response = time - p.arrival
        gantt.append((p.pid, time, time + p.burst))

        time += p.burst
        p.completion = time
        p.turnaround = p.completion - p.arrival
        p.waiting = p.turnaround - p.burst

    return context_switches, gantt


# -----------------------------
# Round Robin Scheduling
# -----------------------------
def round_robin(processes, quantum):
    queue = deque()
    time = 0
    completed = 0
    n = len(processes)

    context_switches = 0
    gantt = []

    processes.sort(key=lambda x: x.arrival)

    index = 0

    while completed < n:

        while index < n and processes[index].arrival <= time:
            queue.append(processes[index])
            index += 1

        if not queue:
            time += 1
            continue

        current = queue.popleft()

        if current.response == -1:
            current.response = time - current.arrival

        execution = min(quantum, current.remaining)

        gantt.append((current.pid, time, time + execution))

        time += execution
        current.remaining -= execution

        while index < n and processes[index].arrival <= time:
            queue.append(processes[index])
            index += 1

        if current.remaining > 0:
            queue.append(current)
        else:
            completed += 1
            current.completion = time
            current.turnaround = current.completion - current.arrival
            current.waiting = current.turnaround - current.burst

        if queue:
            context_switches += 1

    return context_switches, gantt


# -----------------------------
# Display Results
# -----------------------------
def display(processes, title):
    print("\n", "=" * 60)
    print(title)
    print("=" * 60)
    print("PID\tAT\tBT\tCT\tTAT\tWT\tRT")

    total_wt = 0
    total_tat = 0
    total_rt = 0

    for p in processes:
        print(f"{p.pid}\t{p.arrival}\t{p.burst}\t{p.completion}\t"
              f"{p.turnaround}\t{p.waiting}\t{p.response}")

        total_wt += p.waiting
        total_tat += p.turnaround
        total_rt += p.response

    n = len(processes)

    print("\nAverage Waiting Time     :", round(total_wt / n, 2))
    print("Average Turnaround Time :", round(total_tat / n, 2))
    print("Average Response Time   :", round(total_rt / n, 2))


# -----------------------------
# Gantt Chart
# -----------------------------
def gantt_chart(gantt):
    print("\nGantt Chart:")
    for g in gantt:
        print(f"| {g[0]} ", end="")
    print("|")

    print(gantt[0][1], end="")
    for g in gantt:
        print(f" ---- {g[2]}", end="")
    print()


# -----------------------------
# Main Program
# -----------------------------
n = int(input("Enter number of processes: "))

original = []

for i in range(n):
    at = int(input(f"Arrival Time of P{i+1}: "))
    bt = int(input(f"Burst Time of P{i+1}: "))
    original.append((f"P{i+1}", at, bt))

quantum = int(input("\nEnter Time Quantum: "))

# FCFS Copy
fcfs_processes = [Process(pid, at, bt) for pid, at, bt in original]

# RR Copy
rr_processes = [Process(pid, at, bt) for pid, at, bt in original]

# Sort FCFS by arrival
fcfs_processes.sort(key=lambda x: x.arrival)

# Execute FCFS
fcfs_cs, fcfs_gantt = fcfs(fcfs_processes)

# Execute RR
rr_cs, rr_gantt = round_robin(rr_processes, quantum)

# Results
display(fcfs_processes, "FCFS Scheduling")
gantt_chart(fcfs_gantt)
print("Context Switches:", fcfs_cs)

display(rr_processes, "Round Robin Scheduling")
gantt_chart(rr_gantt)
print("Context Switches:", rr_cs)

# -----------------------------
# Comparison
# -----------------------------
print("\n" + "=" * 60)
print("Comparison: FCFS vs Round Robin")
print("=" * 60)

print("""
1. Fairness
   FCFS:
      • Runs processes in arrival order.
      • Long processes can delay short ones.

   Round Robin:
      • Every process gets equal CPU time.
      • More fair for all processes.

2. Turnaround Time
   FCFS:
      • Lower when burst times are similar.
      • Can become large if long jobs arrive first.

   Round Robin:
      • Usually higher because processes are interrupted.

3. Response Time
   FCFS:
      • New processes may wait a long time.

   Round Robin:
      • Better response time since each process gets CPU quickly.

4. Context Switches
   FCFS:
      • Very few context switches.

   Round Robin:
      • More context switches due to time quantum.

5. Queue Management
   • Ready Queue implemented using collections.deque().
   • Processes whose quantum expires are placed at the end.
   • Newly arrived processes are inserted immediately.
""")
