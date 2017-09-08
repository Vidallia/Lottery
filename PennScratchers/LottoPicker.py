#                         LottoPicker 0.1.0
#                     created by V11 ("ConcernedCarry")
#         This code is filled with some useful functions/generators that helped me acheive my goal.
#         

from PennScratchers import PaLottery
PA = PaLottery()
# Required action similar to other modules init
PA.init()

def Gross_Prize():
    """Generator that yeilds the gross prize,
       for each game. Which can easily be correlated,
       with which game it belongs to via enumeration."""
    for value in PA.gStruct:
        yield sum(value['Prize'])


def Gross_Left():
    """Generator that yeilds the gross amount,
       of prizes left for each game. Typically,
       used as a helper function but, has other utilities."""
    for value in PA.gStruct:
        yield sum(value['Left'])


def Adjusted_Prize():
    """Generator that yeilds the Adujusted Gross Prize,
        which is defined as (GrossPrize // Cost)."""
    for i, value in enumerate(Gross_Prize()):
        yield value // PA.gStruct[i]['Cost']


def Highest_Adj_Prizes(n):
    """This function uses Adjusted_Prize() and pairs,
       the prize with its game. Then the function gets,
       the n most games with highest prizes."""
    Names_Prizes = list(zip(Adjusted_Prize(),PA.gNames))
    top_prizes = sorted(Names_Prizes,reverse=True)[:n]
    return top_prizes


def Highest_Left(n):
    """This function uses finds the games with the highest,
        total amount of prizes left, for use with Highest_Adj_Prizes,
        to then get the top games to play  """
    Names_Left = list(zip(Gross_Left(),PA.gNames))
    top_left = sorted(Names_Left,reverse=True)[:n]
    return dict(top_left)


def find_index(lst, key, value):
    """Gets the index of a list of dictionarys by its key,
       only the list of dicts,the expected key, and the value."""
    for i, dic in enumerate(lst):
        if dic[key] == value:
            return i
    return -1


def ParseProfitable(n):
    """ Takes n as the amount of Games you would to find in your most Profitable,
        list, games are represented in order the best chance of hitting it big,
        being the first in the list. A tupple pair of Adjusted_Prize/Games name is returned."""
    Profit = []
    for value in Highest_Left(n).items():
        DEX = find_index(PA.gStruct,'Game',value[1])
        # Gets the Adjusted Prize amount (Gross Prize//Cost of ticket)
        ADJPrice = sum(PA.gStruct[DEX]['Prize']) // PA.gStruct[DEX]['Cost']
        Profit.append((ADJPrice,value[1]))

    return sorted(Profit,reverse=True)[:n]

# Just an example of the code at work
print(ParseProfitable(5))
