"""
Fixed sensor-processing job list for the Zone Job-Scheduler & Deadlock-Safety Engine.

PCB fields:
- job_id maps to the Process ID field in a Process Control Block (PCB).
- priority maps to the scheduling information field in a PCB.

Simulation-only metadata:
- arrival_time, burst_time, and zone are used only by the scheduling simulation
  and are not PCB fields in this project.
"""

JOBS = [
    {"job_id": "Z1-J01", "zone": "Zone-A", "arrival_time": 0, "burst_time": 8, "priority": 3},
    {"job_id": "Z1-J02", "zone": "Zone-A", "arrival_time": 1, "burst_time": 4, "priority": 1},
    {"job_id": "Z2-J01", "zone": "Zone-B", "arrival_time": 2, "burst_time": 9, "priority": 4},
    {"job_id": "Z2-J02", "zone": "Zone-B", "arrival_time": 3, "burst_time": 5, "priority": 2},
    {"job_id": "Z3-J01", "zone": "Zone-C", "arrival_time": 4, "burst_time": 2, "priority": 1},
    {"job_id": "Z3-J02", "zone": "Zone-C", "arrival_time": 5, "burst_time": 6, "priority": 5},
    {"job_id": "Z1-J03", "zone": "Zone-A", "arrival_time": 6, "burst_time": 3, "priority": 2},
    {"job_id": "Z2-J03", "zone": "Zone-B", "arrival_time": 8, "burst_time": 7, "priority": 3},
]
