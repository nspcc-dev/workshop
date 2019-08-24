"""
Game Master contract
===================================

"""

from boa.interop.Neo.Runtime import Notify, GetTrigger, Serialize, Deserialize
from boa.interop.Neo.Action import RegisterAction
from boa.interop.Neo.TriggerType import Application, Verification
from boa.interop.Neo.Storage import GetContext, Get, Put, Delete
from boa.interop.Neo.App import DynamicAppCall
from boa.interop.Neo.Blockchain import GetHeight, GetHeader
from boa.interop.Neo.Header import GetHash
from boa.builtins import range, concat, list, sha256, hash160
 

# -------------------------------------------
# CONTEXT
# -------------------------------------------
ctx = GetContext()

# -------------------------------------------
# SETTINGS
# -------------------------------------------
  
OWNER = b'#\xba\'\x03\xc52c\xe8\xd6\xe5"\xdc2 39\xdc\xd8\xee\xe9'
MAX_HP = 10


OnBattleRound = RegisterAction('battle_step','battle_id', 'battle_round', 'player1_addr', 'player2_addr', 'player1_action', 'player2_action', 'player1_hp', 'player2_hp')
OnBattleResult = RegisterAction('battle_result','battle_id', 'winner', 'competition', 'competition_step')
OnBattlePlayers = RegisterAction('battle_players','player1', 'player2')

def Main(operation, args):
 
    # The trigger determines whether this smart contract is being
    # run in 'verification' mode or 'application'

    trigger = GetTrigger()

    if trigger == Verification():
        return False

    # 'Application' mode
    elif trigger == Application():

        """
        TODO: Description & HOWTO

        Example:
        sc build_run cc-workshop-game/master.py True True True 0710 05 Register [b'cf4741b5ef169d7170bfe725c5d36e7e177185e3']
        sc build_run cc-workshop-game/master.py True True True 0710 05 Player [b'cf4741b5ef169d7170bfe725c5d36e7e177185e3']
        sc build_run cc-workshop-game/master.py True True True 0710 05 Battle [b'cf4741b5ef169d7170bfe725c5d36e7e177185e3', b'7311e3cd33bbbec5b8fc6a146580c9121e849cf8']
        
        """
        if operation == 'CleanUp':
            # Input data - contract hash
            Delete(ctx, "Players")
            return True

        elif operation == 'Register':
            # Input data - contract hash without leading "0x"
            put_serialized(ctx, 'Players', args[0])
            return True

        elif operation == 'Battle':
            player_1 = args[0]
            player_2 = args[1]
            
            competition = args[2]
            competition_step = args[3]

            players_list = get_serialized(ctx, "Players")

            
            
            if player_1 == player_2:
                print("Error: Suiside is not accepted.")
                return False
            
            
            if not is_in_list(players_list, player_1):
                print("Error: Player 1 is not registred.")
                return False

            if not is_in_list(players_list, player_2):
                print("Error: Player 2 is not registred.")
                return False

            
            

            # Start Battle
            players = concat(player_1, player_2)
            battle_data = concat(get_height_hash(),players)
            battle_id = hash160(battle_data)


            # Set Users data
            started_data_p1 = { 'hp': 10, 'repair_drone': 1, 'missile': 1 }
            started_data_p2 = { 'hp': 10, 'repair_drone': 1, 'missile': 1 }
            
            players_data = { player_1: started_data_p1, player_2: started_data_p2 }
            
            battle_round = 1
           
             
            # Start BATTLE (15 rounds)
            params = []
            name_player_1 = DynamicAppCall(byte_swap(player_1), 'Name', params)
            name_player_2 = DynamicAppCall(byte_swap(player_2), 'Name', params)

            player1_name_struct = {'hash': player_1, 'name': name_player_1}
            player2_name_struct = {'hash': player_2, 'name': name_player_2}

            OnBattlePlayers(player1_name_struct, player2_name_struct)

            while ( players_data[player_1]['hp'] > 0 and players_data[player_2]['hp'] > 0 and battle_round < 16 ):
                 
                serialized_players_data = Serialize(players_data)

                params = [ battle_id, battle_round, serialized_players_data ]

                battle_round += 1

                serialized_action_player_1 = DynamicAppCall(byte_swap(player_1), 'OnBattle', params)
                serialized_action_player_2 = DynamicAppCall(byte_swap(player_2), 'OnBattle', params)

                action_player_1 = Deserialize(serialized_action_player_1)
                action_player_2 = Deserialize(serialized_action_player_2)


                # PLAYER 1    
                players_data = battle_round_actions(players_data, action_player_1, action_player_2, player_1, player_2)
                
                # PLAYER 2 
                players_data = battle_round_actions(players_data, action_player_2, action_player_1, player_2, player_1)

                round_story = { 'battle_round': battle_round, player_1: action_player_1, player_2: action_player_2 }
                OnBattleRound(battle_id, battle_round, player_1, player_2, action_player_1, action_player_2, players_data[player_1]['hp'], players_data[player_2]['hp'] )

            if players_data[player_1]['hp'] > players_data[player_2]['hp']:
                winner = player_1
                loser = player_2    
            else:
                winner = player_2
                loser = player_1
            
            params_result = []
            onWin = DynamicAppCall(byte_swap(winner), 'OnWin', params_result)
            onLose = DynamicAppCall(byte_swap(loser), 'OnLose', params_result)

            OnBattleResult(battle_id, winner, competition, competition_step)

            return True

        elif operation == 'Report':
            return True

        elif operation == 'Player':
            params = [ ]
            players_list = get_serialized(ctx, "Players")
           
            if is_in_list(players_list, args[0]):
                params = [ ]
                name = DynamicAppCall(byte_swap(args[0]), 'Name', params)
                print("Player name:") 
                print(name)
                return name
            else:
                print("Error: Need to register")
                return False
            

    return False



def battle_round_actions(players_data, action_player_1, action_player_2, player_1, player_2):
    if action_player_1['action_type'] == 'attack':
        if ( (action_player_2['action_type'] != 'defence') or ( (action_player_2['action_type'] == 'defence') and ( action_player_1['targets'][0] != action_player_2['targets'][0] and action_player_1['targets'][0] != action_player_2['targets'][1] ) ) ):
            players_data[player_2]['hp'] = players_data[player_2]['hp'] - 1

    elif action_player_1['action_type'] == 'missile':
        if players_data[player_1]['missile'] > 0 :
            players_data[player_2]['hp'] = players_data[player_2]['hp'] - 2
            players_data[player_1]['missile'] = players_data[player_1]['missile'] - 1
        else:
            print("Not enought missiles.")


    elif action_player_1['action_type'] == 'repair':
                    
        if players_data[player_1]['repair_drone'] > 0 :
            if players_data[player_1]['hp'] < MAX_HP:
                players_data[player_1]['hp'] = players_data[player_1]['hp'] + 3
                if players_data[player_1]['hp'] > MAX_HP:
                    players_data[player_1]['hp'] = MAX_HP
            players_data[player_1]['repair_drone'] = players_data[player_1]['repair_drone'] - 1

    return players_data


# -------------------------------------------
# UTILS
# -------------------------------------------

def get_height_hash():
    currentHeight = GetHeight()
    currentHeader = GetHeader(currentHeight)
    currentHash = GetHash(currentHeader)

    return currentHash
     
def is_in_list(input_list, key):
    if len(input_list) != 0:
        for item in input_list:
            if item == key:
                return True
    return False


def get_serialized(ctx, key):
    list_bytes = Get(ctx, key)
    # returns False or list
    if len(list_bytes) != 0:
        return Deserialize(list_bytes)
    return False


def put_serialized(ctx, key, value):
    list_bytes = Get(ctx, key)
    if len(list_bytes) != 0:
        lst = Deserialize(list_bytes)
        lst.append(value)
    else:
        lst = [value]
    list_bytes = Serialize(lst)
    Put(ctx, key, list_bytes)
    return True


def byte_swap(input):
    # do first element outside of while loop because `concat` to None adds a leading \x00
    counter = len(input)
    out = input[counter - 1:counter]
    counter = counter - 1

    while counter > 0:
        ctr_minus_one = counter - 1
        byte = input[ctr_minus_one:counter]
        out = concat(out, byte)
        counter = counter - 1

    return out