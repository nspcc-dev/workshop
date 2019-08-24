"""
The Game
===================================

"""

from boa.interop.Neo.Runtime import Notify, GetTrigger, CheckWitness, Serialize, Deserialize
from boa.interop.Neo.TriggerType import Application, Verification
from boa.interop.Neo.Storage import GetContext, Get, Put, Delete
from boa.interop.System.ExecutionEngine import GetExecutingScriptHash 
from boa.interop.Neo.App import DynamicAppCall
from boa.interop.Neo.Blockchain import GetHeight, GetHeader
from boa.interop.Neo.Header import GetHash

from boa.builtins import range, concat, list, sha256, hash160
 

# -------------------------------------------
# CONTEXT
# -------------------------------------------
ctx = GetContext()

def Main(operation, args):
 
    # The trigger determines whether this smart contract is being
    # run in 'verification' mode or 'application'

    trigger = GetTrigger()
    ExecutingScriptHash = byte_swap(GetExecutingScriptHash())


    # 'Verification' mode is used when trying to spend assets ( eg NEO, Gas)
    if trigger == Verification():
        return False

    # 'Application' mode
    elif trigger == Application():

        """
        Users Operations:
        - OnBattle - return action for battle-round
        - OnWin - do somethig in case of victory
        - OnLose - do somthing in case of lose
        """
        if operation == 'Name':
            return "<set your name here>"

        if operation == 'OnBattle':

            # Input data
            battle_id = args[0]
            battle_round = args[1]
            players_data = Deserialize(args[2])

            print("ROUND:")
            print(battle_round)

            # Players Data:
            # { player_1: { 'hp': 10, 'repair_drone': 1, 'missile': 1 }, player_2: { 'hp': 10, 'repair_drone': 1, 'missile': 1 } }    
            # Battle Story:
            # [ {'battle_round': battle_round, player_1: action_player_1, player_2: action_player_2} ]
          
            # Actions types and targets for selection
            action_limit = 1
            action_types = ["attack", "defence", "repair", "missile"]
            target_types = ["head", "body", "hands", "legs"]

            """
            if (players_data[ExecutingScriptHash][''] > 0):
                action_types.append("repair")
                action_limit += 1

            if (players_data[ExecutingScriptHash]['missile'] > 0):
                action_types.append("missile")
                action_limit += 1
            """     
            #if (battle_round == 1):
            selected_action = "attack"
            target_list = ["body"]

            action_data = { 'action_type': selected_action, 'targets': target_list }

            serialized_action = Serialize(action_data)

            return serialized_action


        elif operation == 'OnWin':
            return True

        elif operation == 'OnLose':
            return True

        print("Unknown operation.")

    return False








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


def del_serialized(ctx, key, value):
    list_bytes = Get(ctx, key)
    new_list = []
    deleted = False
    if len(list_bytes) != 0:
        deserialized_list = Deserialize(list_bytes)

        for item in deserialized_list:
            if item == value:
                deleted = True
            else:
                new_list.append(item)

        if (deleted):
            if len(new_list) != 0:
                serialized_list = Serialize(new_list)
                Put(ctx, key, serialized_list)
            else:
                Delete(ctx, key)
            print("Target element has been removed.")
            return True

    print("Target element has not been removed.")

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