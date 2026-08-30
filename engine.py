"""
Zone Job-Scheduler & Deadlock-Safety Engine

This file implements the Part 1 operating-system concepts:
- FCFS scheduling
- Non-preemptive SJF scheduling
- SRTF scheduling
- Round Robin scheduling
- Priority scheduling with and without aging
- Race condition demonstration and Peterson's Algorithm
- Banker's Algorithm
- Paging and segmentation address translation
"""

from jobs import JOBS
import threading
import time
import random

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def print_schedule_results(algorithm_name, results):
    """Print per-job scheduling results and averages."""

    print("\n" + "=" * 70)
    print(algorithm_name)
    print("=" * 70)

    print(
        f"{'Job ID':<10}"
        f"{'Zone':<10}"
        f"{'Arrival':<10}"
        f"{'Burst':<10}"
        f"{'Waiting':<10}"
        f"{'Turnaround':<12}"
    )

    print("-" * 70)

    total_waiting = 0
    total_turnaround = 0

    for job in results:
        print(
            f"{job['job_id']:<10}"
            f"{job['zone']:<10}"
            f"{job['arrival_time']:<10}"
            f"{job['burst_time']:<10}"
            f"{job['waiting_time']:<10}"
            f"{job['turnaround_time']:<12}"
        )

        total_waiting += job["waiting_time"]
        total_turnaround += job["turnaround_time"]

    average_waiting = total_waiting / len(results)
    average_turnaround = total_turnaround / len(results)

    print("-" * 70)
    print(f"Average Waiting Time: {average_waiting:.2f}")
    print(f"Average Turnaround Time: {average_turnaround:.2f}")


# ============================================================
# TASK 2: FCFS
# ============================================================

def fcfs(jobs):
    """
    First-Come, First-Served scheduling.

    Tie-breaking rule:
    1. Earlier arrival_time
    2. Lower job_id
    """

    sorted_jobs = sorted(
        jobs,
        key=lambda job: (job["arrival_time"], job["job_id"])
    )

    current_time = 0
    results = []

    for job in sorted_jobs:

        # CPU remains idle until the job arrives, if necessary.
        if current_time < job["arrival_time"]:
            current_time = job["arrival_time"]

        start_time = current_time

        waiting_time = start_time - job["arrival_time"]

        current_time += job["burst_time"]

        completion_time = current_time

        turnaround_time = completion_time - job["arrival_time"]

        results.append({
            "job_id": job["job_id"],
            "zone": job["zone"],
            "arrival_time": job["arrival_time"],
            "burst_time": job["burst_time"],
            "waiting_time": waiting_time,
            "turnaround_time": turnaround_time,
        })

    return results


# ============================================================
# TASK 2: NON-PREEMPTIVE SJF
# ============================================================

def sjf_non_preemptive(jobs):
    """
    Non-preemptive Shortest Job First scheduling.

    Tie-breaking rule:
    1. Shorter burst_time
    2. Earlier arrival_time
    3. Lower job_id
    """

    remaining_jobs = [job.copy() for job in jobs]

    current_time = 0
    results = []

    while remaining_jobs:

        ready_jobs = [
            job for job in remaining_jobs
            if job["arrival_time"] <= current_time
        ]

        # If no job has arrived yet, jump to the next arrival.
        if not ready_jobs:
            current_time = min(
                job["arrival_time"]
                for job in remaining_jobs
            )
            continue

        selected_job = min(
            ready_jobs,
            key=lambda job: (
                job["burst_time"],
                job["arrival_time"],
                job["job_id"]
            )
        )

        start_time = current_time

        waiting_time = start_time - selected_job["arrival_time"]

        current_time += selected_job["burst_time"]

        completion_time = current_time

        turnaround_time = (
            completion_time
            - selected_job["arrival_time"]
        )

        results.append({
            "job_id": selected_job["job_id"],
            "zone": selected_job["zone"],
            "arrival_time": selected_job["arrival_time"],
            "burst_time": selected_job["burst_time"],
            "waiting_time": waiting_time,
            "turnaround_time": turnaround_time,
        })

        remaining_jobs.remove(selected_job)

    return results


# ============================================================
# TASK 2: SRTF
# ============================================================

def srtf(jobs):
    """
    Shortest Remaining Time First scheduling.

    Tie-breaking rule:
    1. Shorter remaining time
    2. Earlier arrival_time
    3. Lower job_id

    SRTF is the preemptive version of SJF.
    """

    job_data = []

    for job in jobs:
        copied_job = job.copy()
        copied_job["remaining_time"] = job["burst_time"]
        copied_job["completion_time"] = None
        job_data.append(copied_job)

    current_time = 0
    completed = 0
    total_jobs = len(job_data)

    while completed < total_jobs:

        ready_jobs = [
            job for job in job_data
            if job["arrival_time"] <= current_time
            and job["remaining_time"] > 0
        ]

        if not ready_jobs:
            current_time += 1
            continue

        selected_job = min(
            ready_jobs,
            key=lambda job: (
                job["remaining_time"],
                job["arrival_time"],
                job["job_id"]
            )
        )

        # Run for one time unit.
        selected_job["remaining_time"] -= 1
        current_time += 1

        # If the job is finished, record completion time.
        if selected_job["remaining_time"] == 0:
            selected_job["completion_time"] = current_time
            completed += 1

    results = []

    for job in job_data:

        turnaround_time = (
            job["completion_time"]
            - job["arrival_time"]
        )

        waiting_time = (
            turnaround_time
            - job["burst_time"]
        )

        results.append({
            "job_id": job["job_id"],
            "zone": job["zone"],
            "arrival_time": job["arrival_time"],
            "burst_time": job["burst_time"],
            "waiting_time": waiting_time,
            "turnaround_time": turnaround_time,
        })

    return results


# ============================================================
# TASK 3: ROUND ROBIN
# ============================================================

def round_robin(jobs, quantum):
    """
    Round Robin scheduling.

    Context-switch time is assumed to be zero.

    Boundary rule:
    If a job's quantum expires at exactly the same time that
    new jobs arrive, the newly arrived jobs are added to the
    ready queue before the expired job is re-added.
    """

    job_data = []

    for job in jobs:
        copied_job = job.copy()
        copied_job["remaining_time"] = job["burst_time"]
        copied_job["completion_time"] = None
        job_data.append(copied_job)

    # Sort by arrival time, then job_id for deterministic order.
    future_jobs = sorted(
        job_data,
        key=lambda job: (
            job["arrival_time"],
            job["job_id"]
        )
    )

    ready_queue = []
    current_time = 0
    completed = 0
    dispatch_count = 0
    context_switches = 0
    previous_job_id = None

    # Add jobs arriving at time 0.
    while (
        future_jobs
        and future_jobs[0]["arrival_time"] <= current_time
    ):
        ready_queue.append(future_jobs.pop(0))

    while completed < len(job_data):

        # If CPU is idle, jump to the next arrival time.
        if not ready_queue:

            current_time = future_jobs[0]["arrival_time"]

            while (
                future_jobs
                and future_jobs[0]["arrival_time"] <= current_time
            ):
                ready_queue.append(future_jobs.pop(0))

        # Select the next job from the front of the queue.
        current_job = ready_queue.pop(0)

        dispatch_count += 1

        # Record context switch when a different job starts.
        if (
            previous_job_id is not None
            and previous_job_id != current_job["job_id"]
        ):
            context_switches += 1

        previous_job_id = current_job["job_id"]

        # Run for either the quantum or the remaining burst time.
        run_time = min(
            quantum,
            current_job["remaining_time"]
        )

        current_time += run_time
        current_job["remaining_time"] -= run_time

        # ----------------------------------------------------
        # IMPORTANT BOUNDARY RULE
        # Add all jobs that arrived during or exactly at the
        # end of the time slice BEFORE re-adding an expired job.
        # ----------------------------------------------------

        while (
            future_jobs
            and future_jobs[0]["arrival_time"] <= current_time
        ):
            ready_queue.append(future_jobs.pop(0))

        # If the job is not finished, put it at the back.
        if current_job["remaining_time"] > 0:

            ready_queue.append(current_job)

        else:

            current_job["completion_time"] = current_time
            completed += 1

    # Calculate waiting and turnaround times.
    results = []

    for job in job_data:

        turnaround_time = (
            job["completion_time"]
            - job["arrival_time"]
        )

        waiting_time = (
            turnaround_time
            - job["burst_time"]
        )

        results.append({
            "job_id": job["job_id"],
            "zone": job["zone"],
            "arrival_time": job["arrival_time"],
            "burst_time": job["burst_time"],
            "waiting_time": waiting_time,
            "turnaround_time": turnaround_time,
        })

    return results, dispatch_count, context_switches

# ============================================================
# TASK 4: PRIORITY SCHEDULING WITH AND WITHOUT AGING
# ============================================================
def priority_scheduling(jobs, aging=False):
    """
    Non-preemptive Priority Scheduling.

    Lower priority number means higher priority.

    Tie-breaking rule:
    1. Lower effective priority
    2. Earlier arrival_time
    3. Lower job_id

    Aging formula:
    max(1, priority - (ticks waited since becoming ready) // 3)
    """

    remaining_jobs = [job.copy() for job in jobs]

    current_time = 0
    results = []

    while remaining_jobs:

        ready_jobs = [
            job for job in remaining_jobs
            if job["arrival_time"] <= current_time
        ]

        # If no job is ready, jump to the next arrival time.
        if not ready_jobs:
            current_time = min(
                job["arrival_time"]
                for job in remaining_jobs
            )
            continue

        # Calculate effective priority at this dispatch decision.
        for job in ready_jobs:

            if aging:

                ticks_waited = (
                    current_time
                    - job["arrival_time"]
                )

                job["effective_priority"] = max(
                    1,
                    job["priority"]
                    - ticks_waited // 3
                )

            else:

                job["effective_priority"] = (
                    job["priority"]
                )

        # Select the job with the highest effective priority.
        # Lower number = higher priority.
        selected_job = min(
            ready_jobs,
            key=lambda job: (
                job["effective_priority"],
                job["arrival_time"],
                job["job_id"]
            )
        )

        start_time = current_time

        waiting_time = (
            start_time
            - selected_job["arrival_time"]
        )

        current_time += selected_job["burst_time"]

        completion_time = current_time

        turnaround_time = (
            completion_time
            - selected_job["arrival_time"]
        )

        results.append({
            "job_id": selected_job["job_id"],
            "zone": selected_job["zone"],
            "arrival_time": selected_job["arrival_time"],
            "burst_time": selected_job["burst_time"],
            "waiting_time": waiting_time,
            "turnaround_time": turnaround_time,
            "effective_priority": selected_job[
                "effective_priority"
            ],
        })

        remaining_jobs.remove(selected_job)

    return results
def find_longest_waiting_job(results):
    """
    Return the single job with the longest waiting time.
    """

    return max(
        results,
        key=lambda job: job["waiting_time"]
    )

# ============================================================
# TASK 5: RACE CONDITION AND PETERSON'S ALGORITHM
# ============================================================
def run_unsynchronized_demo():
    """
    Demonstrates a race condition on the shared Zone-B
    compute-credit counter.
    """

    counter = [100]

    def subtract_credits():
        value = counter[0]
        time.sleep(random.uniform(0.001,0.02))
        counter[0] = value - 40

    def add_reimbursement():
        value = counter[0]
        time.sleep(random.uniform(0.001,0.02))
        counter[0] = value + 25

    thread1 = threading.Thread(
        target=subtract_credits
    )

    thread2 = threading.Thread(
        target=add_reimbursement
    )

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    return counter[0]
def run_peterson_demo():
    """
    Uses Peterson's Algorithm to protect the critical section.
    """

    counter = [100]

    flag = [False, False]
    turn = [0]

    def process(process_id):

        other = 1 - process_id

        # Peterson's entry section.
        flag[process_id] = True
        turn[0] = other

        while flag[other] and turn[0] == other:
            pass

        # Critical section.
        value = counter[0]

        time.sleep(0.01)

        if process_id == 0:
            counter[0] = value - 40
        else:
            counter[0] = value + 25

        # Exit section.
        flag[process_id] = False

    thread1 = threading.Thread(
        target=process,
        args=(0,)
    )

    thread2 = threading.Thread(
        target=process,
        args=(1,)
    )

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    return counter[0]

# ============================================================
# TASK 6: BANKER'S ALGORITHM
# ============================================================

AVAILABLE = [3, 3, 2]

MAX_NEED = {
    "P0": [7, 5, 3],
    "P1": [3, 2, 2],
    "P2": [9, 0, 2],
    "P3": [2, 2, 2],
}

ALLOCATION = {
    "P0": [0, 1, 0],
    "P1": [2, 0, 0],
    "P2": [3, 0, 2],
    "P3": [2, 1, 1],
}
def calculate_need(max_need, allocation):
    """
    Calculate:
    Need = Max Need - Allocation
    """

    need = {}

    for process in max_need:

        need[process] = [
            max_need[process][i]
            - allocation[process][i]
            for i in range(len(max_need[process]))
        ]

    return need
def is_safe_state(available, allocation, need):
    """
    Banker's Algorithm safety check.

    Returns:
    - True and a safe sequence if the state is safe
    - False and an empty sequence if unsafe
    """

    work = available.copy()

    finish = {
        process: False
        for process in allocation
    }

    safe_sequence = []

    while len(safe_sequence) < len(allocation):

        found_process = False

        for process in allocation:

            if not finish[process]:

                # Check whether Need <= Work
                can_finish = all(
                    need[process][i] <= work[i]
                    for i in range(len(work))
                )

                if can_finish:

                    # Process can finish and release its allocation.
                    for i in range(len(work)):
                        work[i] += allocation[process][i]

                    finish[process] = True
                    safe_sequence.append(process)
                    found_process = True

        # No unfinished process could proceed.
        if not found_process:
            return False, []

    return True, safe_sequence
def check_resource_request(
    process,
    request,
    available,
    max_need,
    allocation
):
    """
    Evaluate a resource request independently.

    The function checks:
    1. Request <= Need
    2. Request <= Available
    3. Hypothetical allocation leaves the system safe
    """

    need = calculate_need(
        max_need,
        allocation
    )

    # Check Request <= Need.
    if any(
        request[i] > need[process][i]
        for i in range(len(request))
    ):
        return False, (
            "Request exceeds the process's remaining Need."
        )

    # Check Request <= Available.
    if any(
        request[i] > available[i]
        for i in range(len(request))
    ):
        return False, (
            "Request exceeds Available resources."
        )

    # Make independent copies.
    temp_available = available.copy()

    temp_allocation = {
        p: allocation[p].copy()
        for p in allocation
    }

    temp_need = {
        p: need[p].copy()
        for p in need
    }

    # Pretend to grant the request.
    for i in range(len(request)):

        temp_available[i] -= request[i]

        temp_allocation[process][i] += request[i]

        temp_need[process][i] -= request[i]

    # Check safety of the hypothetical state.
    safe, sequence = is_safe_state(
        temp_available,
        temp_allocation,
        temp_need
    )

    if safe:

        return True, (
            "Request can be granted. "
            f"Resulting state is safe. "
            f"Safe sequence: {sequence}"
        )

    return False, (
        "Request is within Available and Need, but granting it "
        "would leave the system in an unsafe state."
    )

# ============================================================
# TASK 7: PAGING AND SEGMENTATION ADDRESS TRANSLATION
# ============================================================

PAGE_SIZE = 1024

PAGE_TABLE = {
    0: 5,
    1: 2,
    2: 9,
    3: 1,
}

SEGMENT_TABLE = {
    0: (1000, 400),
    1: (2200, 300),
    2: (500, 150),
}
def translate_paged_address(logical_address):
    """
    Translate a logical address using paging.

    page_number = logical_address // PAGE_SIZE
    offset = logical_address % PAGE_SIZE
    """

    page_number = logical_address // PAGE_SIZE
    offset = logical_address % PAGE_SIZE

    if page_number not in PAGE_TABLE:
        return None

    frame_number = PAGE_TABLE[page_number]

    physical_address = (
        frame_number * PAGE_SIZE
        + offset
    )

    return physical_address
def translate_segmented_address(segment, offset):
    """
    Translate a logical address using segmentation.

    Physical address = base + offset

    The offset must be smaller than the segment limit.
    """

    if segment not in SEGMENT_TABLE:
        return None

    base, limit = SEGMENT_TABLE[segment]

    if offset >= limit:
        return None

    physical_address = base + offset

    return physical_address

# ============================================================
# MAIN PROGRAM
# ============================================================

def main():

    # ============================================================
    # Task 2: Compare scheduling algorithms.
    # ============================================================

    fcfs_results = fcfs(JOBS)
    print_schedule_results(
        "FCFS SCHEDULING",
        fcfs_results
    )

    sjf_results = sjf_non_preemptive(JOBS)
    print_schedule_results(
        "NON-PREEMPTIVE SJF SCHEDULING",
        sjf_results
    )

    srtf_results = srtf(JOBS)
    print_schedule_results(
        "SRTF SCHEDULING",
        srtf_results
    )

    # ========================================================
    # TASK 3: ROUND ROBIN
    # ========================================================

    rr3_results, rr3_dispatches, rr3_switches = round_robin(
        JOBS,
        quantum=3
    )

    print_schedule_results(
        "ROUND ROBIN SCHEDULING (QUANTUM = 3)",
        rr3_results
    )

    print(f"Dispatch Slices: {rr3_dispatches}")
    print(f"Context Switches: {rr3_switches}")

    rr6_results, rr6_dispatches, rr6_switches = round_robin(
        JOBS,
        quantum=6
    )

    print_schedule_results(
        "ROUND ROBIN SCHEDULING (QUANTUM = 6)",
        rr6_results
    )

    print(f"Dispatch Slices: {rr6_dispatches}")
    print(f"Context Switches: {rr6_switches}")

    print("\nRound Robin Overhead Conclusion:")
    print(
        "Quantum 3 would cause more context-switch overhead "
        "in a real OS because it produced "
        f"{rr3_switches} context switches, compared with "
        f"{rr6_switches} context switches for quantum 6."
    )
    # ========================================================
    # TASK 4: PRIORITY SCHEDULING
    # ========================================================

    priority_no_aging_results = priority_scheduling(
        JOBS,
        aging=False
    )

    print_schedule_results(
        "PRIORITY SCHEDULING WITHOUT AGING",
        priority_no_aging_results
    )

    longest_no_aging = find_longest_waiting_job(
        priority_no_aging_results
    )

    print(
        "Longest Waiting Job Without Aging: "
        f"{longest_no_aging['job_id']} "
        f"(Waiting Time: {longest_no_aging['waiting_time']})"
    )


    priority_aging_results = priority_scheduling(
        JOBS,
        aging=True
    )

    print_schedule_results(
        "PRIORITY SCHEDULING WITH AGING",
        priority_aging_results
    )

    longest_aging = find_longest_waiting_job(
        priority_aging_results
    )

    print(
        "Longest Waiting Job With Aging: "
        f"{longest_aging['job_id']} "
        f"(Waiting Time: {longest_aging['waiting_time']})"
    )

    # ========================================================
    # TASK 5: RACE CONDITION AND PETERSON'S ALGORITHM
    # ========================================================

    print("\n" + "=" * 70)
    print("TASK 5: UNSYNCHRONIZED RACE CONDITION")
    print("=" * 70)

    for run in range(1, 6):

        final_value = run_unsynchronized_demo()

        print(
            f"Run {run}: Final counter value = "
            f"{final_value}"
        )


    print("\n" + "=" * 70)
    print("TASK 5: PETERSON'S ALGORITHM")
    print("=" * 70)

    for run in range(1, 6):

        final_value = run_peterson_demo()

        print(
            f"Run {run}: Final counter value = "
            f"{final_value}"
        )
  
    # ========================================================
    # TASK 6: BANKER'S ALGORITHM
    # ========================================================

    print("\n" + "=" * 70)
    print("TASK 6: BANKER'S ALGORITHM")
    print("=" * 70)

    # Calculate and print Need matrix.
    need = calculate_need(
        MAX_NEED,
        ALLOCATION
    )

    print("\nNeed Matrix:")
    print("Process   R0   R1   R2")
    print("-" * 25)

    for process in need:
        print(
            f"{process:<9} "
            f"{need[process][0]:<4} "
            f"{need[process][1]:<4} "
            f"{need[process][2]:<4}"
        )

    # Check initial state.
    safe, sequence = is_safe_state(
        AVAILABLE,
        ALLOCATION,
        need
    )

    print("\nInitial State Safe:", safe)

    if safe:
        print(
            "One Valid Safe Sequence:",
            " -> ".join(sequence)
        )

    # --------------------------------------------------------
    # Request 1: P1 requests [1, 0, 2]
    # --------------------------------------------------------

    print("\nRequest Check 1:")
    print("P1 requests [1, 0, 2]")

    granted, message = check_resource_request(
        "P1",
        [1, 0, 2],
        AVAILABLE,
        MAX_NEED,
        ALLOCATION
    )

    if granted:
        print("Result: GRANTED")
    else:
        print("Result: DENIED")

    print(message)

    # --------------------------------------------------------
    # Request 2: P0 requests [2, 0, 2]
    # --------------------------------------------------------

    print("\nRequest Check 2:")
    print("P0 requests [2, 0, 2]")

    granted, message = check_resource_request(
        "P0",
        [2, 0, 2],
        AVAILABLE,
        MAX_NEED,
        ALLOCATION
    )

    if granted:
        print("Result: GRANTED")
    else:
        print("Result: DENIED")

    print(message)
    # ========================================================
    # TASK 7: PAGING AND SEGMENTATION ADDRESS TRANSLATION
    # ========================================================

    print("\n" + "=" * 70)
    print("TASK 7: PAGING ADDRESS TRANSLATION")
    print("=" * 70)

    paged_addresses = [
        260,
        1500,
        3000,
        5000,
    ]

    for address in paged_addresses:

        result = translate_paged_address(
            address
        )

        if result is None:
            print(
                f"Logical Address {address}: "
                f"Page Fault"
            )
        else:
            print(
                f"Logical Address {address}: "
                f"Physical Address = {result}"
            )


    print("\n" + "=" * 70)
    print("TASK 7: SEGMENTATION ADDRESS TRANSLATION")
    print("=" * 70)

    segmented_addresses = [
        (0, 150),
        (1, 350),
        (2, 100),
    ]

    for segment, offset in segmented_addresses:

        result = translate_segmented_address(
            segment,
            offset
        )

        if result is None:
            print(
                f"Logical Address ({segment}, {offset}): "
                f"Segmentation Fault"
            )
        else:
            print(
                f"Logical Address ({segment}, {offset}): "
                f"Physical Address = {result}"
            )
if __name__ == "__main__":
    main()
