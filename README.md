# Traffic-control-with-Raspberry-pi-5
## INTELLIGENCE USED:

## 1. Directional Priority Sum Intelligence
The controller calculates a weighted sum of vehicle priorities at each junction:
Assign higher weights to emergency vehicles (Ambulance, Police) than regular traffic.
The direction with the highest sum gets green first.
This ensures lanes with more total urgency get cleared fastest.


## 2. Congestion Aging Adjustment
If a junction hasn’t received green for a long time, incrementally boost its priority score over time.
Prevents starvation for less busy lanes.


Helps ensure fairness during extended peak hours.
