from cs50 import get_float


while True:
    # Ask the user how much change is owed
    change_owned = get_float("Change owed: ")
    if change_owned > 0:
        # Spits out the minimum number of coins
        # Convert the user's input to cents
        change_owned *= 100
        # Round it to avoid mistakes
        change_owned = round(change_owned)
        # How many dollars ?
        coins_used = change_owned // 100
        change_owned = change_owned % 100
        # How many quarters ?
        coins_used += change_owned // 25
        change_owned = change_owned % 25
        # How many dimes ?
        coins_used += change_owned // 10
        change_owned = change_owned % 10
        # How many nickels ?
        coins_used += change_owned // 5
        change_owned = change_owned % 5
        # How many cents ?
        coins_used += change_owned // 1
        change_owned = change_owned % 1
        print(coins_used)
        break