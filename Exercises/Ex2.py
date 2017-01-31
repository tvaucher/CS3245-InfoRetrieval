from random import randint

LIST_ACTION = ["p", "s", "t"]
WINS_OVER = {"p": "t", "s": "p", "t": "s"}
NAME_ACTION = {"p": "Paper", "s": "Scissors", "t": "Stone"}

def get_user_action():
    user_select = "invalid"
    while len(user_select) > 1 or user_select not in "pst":
        user_select = input("Choose (p)aper, (s)cissors, or s(t)one?")
    return user_select

def get_computer_action():
    return(LIST_ACTION[randint(0, 2)])

def judge(user_action, computer_action):
    print_action(user_action, computer_action)
    if user_action == computer_action:
        print("Nobody wins in this round!")
        return 0, 0
    elif WINS_OVER[user_action] == computer_action:
        print("User wins in this round!")
        return 1, 0
    else:
        print("Computer wins in this round!")
        return 0, 1

def print_action(user_action, computer_action):
    print(f"User's Choice is: {NAME_ACTION[user_action]},",
          f"Computer's choice is {NAME_ACTION[computer_action]}")

def update_score(score, res):
    for (k, point) in zip(score.keys(), res):
        score[k] += point
        print(f"{k} point is {score[k]}")

def print_winner(score):
    print(f"Game ends! Winner is {max(score, key=lambda x: score[x])}")

def main():
    print("Welcome to Paper, Scissors, Stone!")
    point_to_win = int(input("How many points are required for a win? "))
    score = {"User": 0, "Computer": 0}
    while score["User"] < point_to_win and score["Computer"] < point_to_win:
        update_score(score, judge(get_user_action(), get_computer_action()))
    print_winner(score)

if __name__ == '__main__':
    main()
