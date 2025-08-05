from gpiozero import LED
from time import sleep
import heapq

# Threshold for car count
CAR_THRESHOLD = 12

# Set duration (seconds)
DEFAULT_GREEN_DURATION = 10
EXTENDED_GREEN_DURATION = 20

# Define LED pins for each junction
junction_leds = {
    'J1': {'R': LED(2), 'Y': LED(3), 'G': LED(4)},
    'J2': {'R': LED(5), 'Y': LED(6), 'G': LED(7)},
    'J3': {'R': LED(8), 'Y': LED(9), 'G': LED(10)},
}

# Sample input: vehicle flow at each junction
incoming_traffic = [
    ('J1', 'Car'), ('J1', 'Car'), ('J1', 'Car'), ('J1', 'Car'),
    ('J1', 'Car'), ('J1', 'Car'), ('J1', 'Car'), ('J1', 'Car'),
    ('J1', 'Car'), ('J1', 'Car'), ('J1', 'Car'), ('J1', 'Car'),
    ('J1', 'Car'), ('J1', 'Car'), ('J1', 'Ambulance'),

    ('J2', 'Car'), ('J2', 'Car'), ('J2', 'Car'), ('J2', 'Car'),
    ('J2', 'Car'), ('J2', 'Car'), ('J2', 'Car'), ('J2', 'Ambulance'),
    ('J2', 'Car'), ('J2', 'Car'), ('J2', 'Car'), ('J2', 'Car'),

    ('J3', 'Car'), ('J3', 'Car'), ('J3', 'Car'), ('J3', 'Car'),
    ('J3', 'Car'), ('J3', 'Car'), ('J3', 'Car'), ('J3', 'Car'),
    ('J3', 'Car'), ('J3', 'Car'),
]

# Count vehicles per junction
vehicle_count = {
    'J1': {'Car': 0, 'Ambulance': 0},
    'J2': {'Car': 0, 'Ambulance': 0},
    'J3': {'Car': 0, 'Ambulance': 0}
}

for junction, vehicle in incoming_traffic:
    if vehicle in vehicle_count[junction]:
        vehicle_count[junction][vehicle] += 1

# Create priority queue: (-priority, junction)
# Higher ambulance count = higher priority
pq = []
for j in vehicle_count:
    amb = vehicle_count[j]['Ambulance']
    cars = vehicle_count[j]['Car']
    priority = (amb * 100) + cars  # Ambulance has stronger weight
    heapq.heappush(pq, (-priority, j))

# Process junctions in order of priority
while pq:
    _, j = heapq.heappop(pq)
    cars = vehicle_count[j]['Car']
    amb = vehicle_count[j]['Ambulance']

    print(f"\nJunction {j}:")
    print(f"  Cars: {cars}")
    print(f"  Ambulance: {amb}")

    # Red ON, Yellow OFF, Green OFF for all others
    for other in junction_leds:
        junction_leds[other]['R'].on()
        junction_leds[other]['Y'].off()
        junction_leds[other]['G'].off()

    if amb > 0:
        print("  🚨 Ambulance detected! Giving emergency green.")
        junction_leds[j]['R'].off()
        junction_leds[j]['G'].on()
        sleep(EXTENDED_GREEN_DURATION)
    elif cars > CAR_THRESHOLD:
        print(f"  🚗 High traffic! Extending green time.")
        junction_leds[j]['R'].off()
        junction_leds[j]['G'].on()
        sleep(EXTENDED_GREEN_DURATION)
    else:
        print("  Normal traffic. Standard green time.")
        junction_leds[j]['R'].off()
        junction_leds[j]['G'].on()
        sleep(DEFAULT_GREEN_DURATION)

    # Yellow blink before red
    junction_leds[j]['G'].off()
    junction_leds[j]['Y'].on()
    sleep(2)
    junction_leds[j]['Y'].off()
    junction_leds[j]['R'].on()

print("\n✅ Traffic cycle completed.\n")
