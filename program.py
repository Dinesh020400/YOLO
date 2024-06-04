# Read vehicle counts from out.txt
with open("out.txt", "r") as file:
    no_of_vehicles = []
    for line in file:
        line = line.strip()
        if line:  # Check if the line is not empty
            no_of_vehicles.append(int(line))

# Calculate baseTimer and timeLimits here if needed
baseTimer = 120  # You can calculate this dynamically if needed
timeLimits = [5, 30]  # You can calculate this dynamically if needed

print("Input no of vehicles:", *no_of_vehicles)

# Calculate timings
t = [(i / sum(no_of_vehicles)) * baseTimer if timeLimits[0] < (i / sum(no_of_vehicles)) * baseTimer < timeLimits[1] 
     else min(timeLimits, key=lambda x: abs(x - (i / sum(no_of_vehicles)) * baseTimer)) for i in no_of_vehicles]

# Round timings to 2 decimal places
t_rounded = [round(time, 2) for time in t]

print(t_rounded, round(sum(t_rounded), 2))

# Write the timing to timing.txt
with open('timing.txt', 'w') as file:
    file.write(f"{t_rounded} {round(sum(t_rounded), 2)}")
