class Ship:
    def __init__(self, size, locations) -> None:
        self.size = size
        self.positions = locations

class Player:
    def __init__(self, name) -> None:
        self.name = name
        self.boats = []
        self.grid = [[0 for _ in range(5)] for _ in range(5)]

    def create_boat(self, size):
        # Check if the size fits within the grid dimensions
        if size > len(self.grid):
            print("* Error, the boat size doesn't fit in the grid *")
            return False
        
        print(f'You want to create a boat of size {size}')
        
        # Get the head coordinates
        x = int(input("Give me the X coordinate of the head of your boat: "))
        y = int(input("Give me the Y coordinate of the head of your boat: "))

        # Choose the orientation
        print("1. Up\n2. Down\n3. Right\n4. Left")
        orientation = input("What way do you want to orientate your boat? ")

        # Dictionary to define directional movements
        direction_map = {
            "1": (0, -1),  # Up
            "2": (0, 1),   # Down
            "3": (1, 0),   # Right
            "4": (-1, 0)   # Left
        }

        # Validate input and apply the directional movement
        if orientation not in direction_map:
            print("Invalid option")
            return False

        dx, dy = direction_map[orientation]
        locations = []

        # Generate boat locations and check if they fit within the grid
        for i in range(size):
            new_x = x + i * dx
            new_y = y + i * dy

            # Check if new coordinates are within the grid boundaries
            if not (0 <= new_x < len(self.grid) and 0 <= new_y < len(self.grid[0])):
                print("* Error, given boat doesn't fit in the grid *")
                return False

            locations.append((new_x, new_y))

        # If all coordinates are valid, create the boat
        self.boats.append(Ship(size, locations))
        print(f"Boat created with locations: {locations}")
        return True

    def choose_coordinates(self):
        while True:
            try:
                # Get and validate x coordinate
                x_coordinate = int(input("Give me the X coordinate where you want to shoot: "))
                if not (0 <= x_coordinate < len(self.grid)):
                    raise ValueError("That is not a valid X coordinate")
                
                # Get and validate y coordinate
                y_coordinate = int(input("Give me the Y coordinate where you want to shoot: "))
                if not (0 <= y_coordinate < len(self.grid[0])):
                    raise ValueError("That is not a valid Y coordinate")

                # If both are valid, return the coordinates
                return (x_coordinate, y_coordinate)
            
            except ValueError as e:
                print(e)


class Game:

    def __init__(self) -> None:
        self.players = []

    def setup(self):
        self.players = [Player('Player_1'), Player('Player_2')]
        boat_sizes = [4,3,2]
        for player in self.players:
            for boat_size in boat_sizes:
                # Repeat the create_boat method until it returns True
                while not player.create_boat(boat_size):
                    print(f"Failed to place a boat of size {boat_size}. Try again.")
                print(f"Boat of size {boat_size} successfully placed.")

    def attack(self, attacking_player, defending_player):
        # Attacker chooses coordinates
        coordinates = attacking_player.choose_coordinates()
        
        # Check if the defending player's boat is hit
        for boat in defending_player.boats:
            if coordinates in boat.positions:
                boat.positions.remove(coordinates)
                print(f"Hit! {defending_player.name} lost part of a boat!")
                
                # Check if the boat has been completely destroyed
                if len(boat.positions) == 0:
                    defending_player.boats.remove(boat)
                    print(f"{defending_player.name}'s boat of size {boat.size} has been sunk!")
                return  # Exit after a successful hit
                
        print("Miss!")  # If no boat is hit

    def check_winner(self, defending_player):
        # Check if the defending player has no boats left
        if len(defending_player.boats) == 0:
            return True
        return False

    def play(self):
        self.setup()
        turn = 0

        while True: 
            attacking_player = self.players[turn % 2]
            defending_player = self.players[(turn + 1) % 2]

            print(f"{attacking_player.name}'s turn to attack")
            self.attack(attacking_player, defending_player)

            # Check if there is a winner after the attack
            game_over, winner_name = self.check_winner(defending_player)
            if game_over:
                print(f"\n{attacking_player} has won the game!")
                break

            turn += 1

game = Game()
game.play()