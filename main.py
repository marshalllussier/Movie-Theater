import sys
import os

from Seat import Seat

rows = 10
columns = 20
theater = [[0 for i in range(columns)] for j in range(rows)]
reservations = {}
seating_info = {}


def get_group_from_id(groups, res_id):                  # Helper function to locate a group in a collection from its reservation ID
	for group in groups:
		if group == res_id:
			return group


def print_seats():
	print("                [[     SCREEN     ]]    ")
	print("                --------------------")
	for row in theater:
		print(row[0].alphabetic_row(), end="       ")
		for seat in row:
			print(seat, end=" ")
		print()
	print(f"\n        1               . . .                {columns}")


def assign_seats():
	total_seats_needed = list(reservations.values())                                    # Assign a variable to the total seats needed (all seats by all groups)
	while len(total_seats_needed) > 0:                                                  # While that list is not empty
		current_group = list(reservations.keys())[0]                                    # Get the current group of this iteration
		group_seats = int(total_seats_needed[0])                                        # Also get the number of seats requested
		for row in theater:                                                             # For each row in the theater
			for seat in row:                                                            # For each seat in that row
				if (columns - seat.column) < group_seats - 1:                           # If a group is not going to fit on this row
					continue                                                            # Go to the next row before trying to place them
				if not seat.is_sold and not seat.is_barrier and group_seats > 0:        # If the seat hasn't been sold, and the seat is not a 'social distancing' seat, and the current group still has members without a seat
					seat.set_sold()                                                     # Mark the current seat as sold
					group_seats -= 1                                                    # Remove one from the current groups seating requirements
					# print(f"{current_group} has been assigned seat {seat.position}")
					seating_info[seat.position] = current_group                         # In the new dictionary of seating information, mark the current seat as belonging to the current groups ID
					if group_seats == 0:                                                # If all the members of this group now have a seat
						next_three = row[seat.column:(seat.column + 3)]                 # Get a list of the next three seats
						for seat in next_three:                                         # For every seat in the list of three seats
							# print(f"{seat.position} has been made a barrier")
							seat.set_barrier()                                          # Mark that seat as a 'social distancing' seat
		total_seats_needed.pop(0)                                                       # Remove the first index of total_seats_needed, saying you no longer need those seats
		reservations.pop(current_group)                                                 # Remove the current group from the reservations to pass the iterater on to the remaining groups


def output_seating_info():
	flipped = {}                                                        # Create a new dictionary to flip the seating info into the file-output format
	for key in seating_info:                                            # For each key (Seat) in the seating info dictionary
		flipped.setdefault(seating_info[key], []).append(key)           # If the value (Reservation ID) does not exist in the flipped dictionary, create it and set the default to an empty list. Then, append each key to the list.
	with open("output.txt", "w+") as f:
		for key in flipped.keys():                                      # For each key (Reservation ID) in the flipped dictionary
			seats = ",".join(s for s in flipped[key])                   # Join each value for that key with a comma and set it to a new string
			f.write(f"{key} {seats}\n")                                 # Write the new line in the output file format of ResID X1,X2,X3
	print("Ticket information can be found at", os.path.abspath("output.txt"))      # Print the absolute path of the new file


if __name__ == '__main__':
	args = sys.argv
	input = open(args[1], "r").read()                   # Read the system 2nd system arg
	for value in input.split("\n"):                     # Split the file at each new line (different reservation)
		id, num = value.split(" ")                      # Unpack the reservation into its identifier and its seats requested
		if int(num) > columns:                          # Quick check to check the possibility of a group staying seated together
			print(f"Group {id} cannot fit in a single group due to theatre size, aborting . . .")
			sys.exit(1)                                 # If not possible, exit program
		reservations[id] = num                          # Add the current reservation to a dictionary with the ID as a key and the seats requested as value
	for row in range(rows):                             # For every row in the theater
		for col in range(columns):                      # For each seat in that row
			seat = Seat(row + 1, col + 1)               # Create a new Seat object and add 1 to both the row and column to get a "theater friendly" index
			theater[row][col] = seat                    # Add that seat into our 2d array of seats

	# print("Original theater:")                                    # Uncomment me for formatted printing
	# print_seats()                                                 # Uncomment me for formatted printing
	# print("\n" * 4)                                               # Uncomment me for formatted printing
	assign_seats()
	# print("New theater:")                                         # Uncomment me for formatted printing
	# print_seats()                                                 # Uncomment me for formatted printing
	# print("\n" * 4)                                               # Uncomment me for formatted printing
	output_seating_info()