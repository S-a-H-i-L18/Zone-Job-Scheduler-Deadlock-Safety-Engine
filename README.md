# Zone Job-Scheduler & Deadlock-Safety Engine

## Overview

This project implements operating-system concepts for a Zone Job-Scheduler & Deadlock-Safety Engine. The project includes:

* FCFS scheduling
* Non-preemptive SJF scheduling
* SRTF scheduling
* Round Robin scheduling with quantum values 3 and 6
* Priority scheduling with and without aging
* Race condition demonstration
* Peterson's Algorithm
* Banker's Algorithm
* Paging address translation
* Segmentation address translation

---

# Task 8: Production Scheduling Algorithm Recommendation

## Recommended Algorithm Family: SJF/SRTF Family

For production use, I recommend the **SJF/SRTF scheduling family**, specifically **Shortest Remaining Time First (SRTF)**.

The main reason for this choice is that SRTF produced the best overall scheduling performance among the implemented algorithms.

### Measured SRTF Results

* Average Waiting Time: **11.50**
* Average Turnaround Time: **17.00**

These are the lowest average waiting time and average turnaround time among the tested scheduling algorithms.

Non-preemptive SJF also performed well:

* Average Waiting Time: **13.00**
* Average Turnaround Time: **18.50**

Therefore, the SJF/SRTF family provides the best overall efficiency for the tested Zone Job-Scheduler workload. SRTF is the strongest choice because it can preempt a longer running job when a newly arrived job has a shorter remaining execution time.

---

## Why FCFS Is Less Suitable

FCFS is less suitable for this workload because it produced higher waiting and turnaround times.

### FCFS Results

* Average Waiting Time: **17.12**
* Average Turnaround Time: **22.62**

### Comparison with SRTF

* SRTF Average Waiting Time: **11.50**
* FCFS Average Waiting Time: **17.12**

FCFS therefore has an average waiting time that is **5.62 time units higher** than SRTF.

* SRTF Average Turnaround Time: **17.00**
* FCFS Average Turnaround Time: **22.62**

FCFS therefore has an average turnaround time that is **5.62 time units higher** than SRTF.

FCFS executes jobs strictly according to arrival order. As a result, a long job can cause shorter jobs arriving later to wait for a long time.

---

## Why Round Robin Is Less Suitable

Round Robin is less suitable for this workload because both tested quantum values produced higher average waiting and turnaround times than SRTF.

### Round Robin with Quantum = 3

* Average Waiting Time: **22.62**
* Average Turnaround Time: **28.12**
* Context Switches: **16**

Compared with SRTF:

* SRTF Average Waiting Time: **11.50**
* Round Robin Average Waiting Time: **22.62**

Round Robin with quantum 3 has an average waiting time that is **11.12 time units higher** than SRTF.

It also produced **16 context switches**, creating greater context-switch overhead.

### Round Robin with Quantum = 6

* Average Waiting Time: **20.38**
* Average Turnaround Time: **25.88**
* Context Switches: **10**

Although quantum 6 reduced the context-switch count from **16 to 10**, its waiting and turnaround times were still significantly higher than SRTF.

Therefore, for this workload, Round Robin provides fairness but does not provide the best overall efficiency.

---

## Why Priority Scheduling Is Less Suitable

Priority scheduling is less suitable because its best measured average waiting time was still higher than SRTF.

### Priority Scheduling Without Aging

* Average Waiting Time: **14.12**
* Average Turnaround Time: **19.62**

The average waiting time is **2.62 time units higher** than SRTF:

* SRTF: **11.50**
* Priority without aging: **14.12**

The longest waiting job was:

* **Z3-J02**
* Waiting Time: **33**

This shows that priority scheduling without aging can cause some lower-priority jobs to wait for a long time.

### Priority Scheduling With Aging

* Average Waiting Time: **17.12**
* Average Turnaround Time: **22.62**

The longest waiting job was:

* **Z2-J03**
* Waiting Time: **29**

Aging reduced the longest observed waiting time from **33 to 29**, which helps reduce starvation risk. However, the overall average waiting and turnaround times were still worse than SRTF.

---

## Final Conclusion

The **SJF/SRTF family, specifically SRTF**, is the recommended production scheduling choice for the tested workload.

SRTF produced:

* The lowest Average Waiting Time: **11.50**
* The lowest Average Turnaround Time: **17.00**

The other scheduling families were less suitable because:

1. **FCFS** produced higher waiting and turnaround times.
2. **Round Robin** produced substantially higher waiting and turnaround times and introduced context-switch overhead.
3. **Priority scheduling** produced higher average waiting times, and the no-aging version allowed one job to wait as long as **33 time units**.

Based on the measured results, SRTF provides the best overall efficiency for the Zone Job-Scheduler workload.
