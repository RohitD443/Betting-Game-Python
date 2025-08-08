# Betting-Game-Python
import random

# Player class to handle each player's account and actions
class Player:
    def __init__(self, username, balance=50):
        self.username = username      # Store player's username
        self.balance = balance        # Initialize player's balance (default is $50)

    # Deposit amount into player's balance
    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"${amount} deposited successfully.")
        else:
            print("Deposit amount must be positive.")

    # Withdraw amount from player's balance
    def withdraw(self, amount):
        if amount <= 0:
            print("Withdraw amount must be positive.")
        elif amount > self.balance:
            print("Insufficient funds.")
        else:
            self.balance -= amount
            print(f"${amount} withdrawn successfully.")

    # Return player's current balance
    def get_balance(self):
        return self.balance

    # Play the number guessing game at the selected table
    def play_game(self, table_config, bet_amount):
        numbers = table_config["range"]
        win_rate = table_config["win_rate"]

        try:
            # Ask user to choose a number within the allowed range
            chosen_number = int(input(f"Enter a number between {numbers.start} and {numbers.stop - 1}: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            return

        if chosen_number not in numbers:
            print("Number not in range.")
            return

        # Randomly pick a winning number from the range
        winning_number = random.choice(list(numbers))
        print(f"The winning number is: {winning_number}")

        # Check if user wins
        if chosen_number == winning_number:
            win_amount = int(bet_amount * win_rate)
            self.deposit(win_amount)
            print(f"🎉 You won ${win_amount}!")
        else:
            self.withdraw(bet_amount)
            print("❌ You lost the bet.")


# Game class to handle the entire game system and menu
class Game:
    def __init__(self):
        self.credentials = {}    # Dictionary to store username-password pairs
        self.players = {}        # Dictionary to store username-Player object pairs
        self.tables = {          # Table configurations: number range and win rate
            1: {"range": range(1, 6), "win_rate": 0.25},
            2: {"range": range(1, 11), "win_rate": 0.50},
            3: {"range": range(1, 16), "win_rate": 0.75}
        }

    # Register a new user
    def register(self):
        username = input("Choose a username: ")
        if username in self.credentials:
            print("Username already exists. Try logging in.")
            return None

        password = input("Choose a password: ")
        self.credentials[username] = password                  # Save credentials
        self.players[username] = Player(username)              # Create a new Player object
        print("✅ Registration successful.")

    # Login existing user
    def login(self):
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        # Validate credentials
        if username in self.credentials and self.credentials[username] == password:
            print("✅ Login successful.")
            return self.players[username]
        else:
            print("❌ Incorrect username or password.")
            return None

    # Display the main in-game menu
    def display_menu(self):
        print("\n--- Game Menu ---")
        print("1. Check Balance")
        print("2. Deposit Amount")
        print("3. Play Game")
        print("4. Withdraw Amount")
        print("5. Logout")

    # Handle all in-game operations after login
    def play_session(self, player):
        while True:  # Keep running until user logs out
            self.display_menu()
            try:
                choice = int(input("Enter your choice: "))
            except ValueError:
                print("Invalid input.")
                continue

            if choice == 1:
                print(f"Your balance is: ${player.get_balance()}")
            elif choice == 2:
                try:
                    amount = int(input("Enter deposit amount: "))
                    player.deposit(amount)
                except ValueError:
                    print("Invalid amount.")
            elif choice == 3:
                print("\nChoose a table:")
                for num, table in self.tables.items():
                    r = table['range']
                    print(f"{num}. Numbers {r.start}-{r.stop - 1}, Win rate: {int(table['win_rate']*100)}%")

                try:
                    table_choice = int(input("Enter table number: "))
                    if table_choice not in self.tables:
                        print("Invalid table.")
                        continue
                    bet_amount = int(input("Enter bet amount: "))
                    if bet_amount <= 0 or bet_amount > player.get_balance():
                        print("Invalid or insufficient balance.")
                        continue
                    player.play_game(self.tables[table_choice], bet_amount)
                except ValueError:
                    print("Invalid input.")
            elif choice == 4:
                try:
                    amount = int(input("Enter withdrawal amount: "))
                    player.withdraw(amount)
                except ValueError:
                    print("Invalid input.")
            elif choice == 5:
                print("🔒 Logged out.")
                break
            else:
                print("Invalid choice.")

    # Run the game system
    def run(self):
        while True:
            print("\n--- Welcome to the Betting Game ---")
            print("1. Register")
            print("2. Login")
            print("3. Exit")

            try:
                choice = int(input("Enter your choice: "))
            except ValueError:
                print("Invalid input.")
                continue

            if choice == 1:
                self.register()
            elif choice == 2:
                player = self.login()
                if player:
                    self.play_session(player)  # Start game session after login
            elif choice == 3:
                print("👋 Exiting the game. Goodbye!")
                break
            else:
                print("Please choose a valid option (1-3).")


# Entry point: Start the game
game = Game()
game.run()
