field = [
    [0,0,0,0,0,0,0],
    [0,1,0,0,0,0,0],
    [0,1,1,0,0,0,0],
    [0,0,0,0,0,1,0],
    [0,0,0,0,1,1,0],
]
def print_field():
    # this function will print the contents of the array
    for y in range(len(field)):
        for x in range(len(field[0])):
	        # value by column and row
            print(field[y][x], end=' ')
            if x == len(field[0])-1:
                # print a visited_val line at the end of each row
                print('\n')

def flood_fill(x ,y, empty_val, visited_val):
    # we need the x and y of the start position, the empty_val value,
    # and the visited_val value
    # the flood fill has 4 parts
    # firstly, make sure the x and y are inbounds
    if x < 0 or x >= len(field[0]) or y < 0 or y >= len(field):
        return
    # secondly, check if the current position equals the empty_val value
    if field[y][x] != empty_val:
        return

    # thirdly, set the current position to the visited_val value
    field[y][x] = visited_val
    # fourthly, attempt to fill the neighboring positions
    flood_fill(x+1, y, empty_val, visited_val)
    flood_fill(x-1, y, empty_val, visited_val)
    flood_fill(x, y+1, empty_val, visited_val)
    flood_fill(x, y-1, empty_val, visited_val)

if __name__ == "__main__":
    # print field before the flood fill
    print_field()
    flood_fill(2,1, 0, 3)
    print("Doing flood fill with '3'")

    # print the field after the flood fill
    print_field()