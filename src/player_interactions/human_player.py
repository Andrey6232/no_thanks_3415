from src.player import Player
from src.player_interaction import PlayerInteraction


class Human(PlayerInteraction):
    @classmethod
    def choose_action(cls, player: Player):
        while True:
            print("Choose action: type 't' (take card) or 's' (spend chips)")
            action = input()
            if action == 't':
                return 'Take card'
            elif action == 's':
                if player.chips <= 0:
                    print("You don't have enough chips, choose another action")
                    continue
                return 'Spend'
            else:
                print('Incorrect input')