#                      PennScratchers v0.1.0
#                  created by V11 ("ConcernedCarry")
#     When creating an instance of PennScratchers dong forget to run the .init() method to fill up your DataStructures!
#
try:
    import requests
    from bs4 import BeautifulSoup
   
except ImportError as e:
    print(f"{e}\nTry using pip to install the package...")

class PaLottery:
    def __init__(self):
        """
         gNames = The Scratch-Offs name
         gCost = The Cost of each game
         gPrize = The games prizes
         gLeft = The amount of prizes left
         gStruct contains the information for each game as a list of Dictionaries.
        """
        self.gNames  = []
        self.gCost   = []
        self.gPrize  = []
        self.gLeft   = []
        self.gStruct = []

    def _ExtractData(self):
        """
        Extracts the game data from the PA Lottery's Website,
        then appends it to gNames, gPrize, and gLeft.
        """
        url = r'https://www.palottery.state.pa.us/Scratch-Offs/Scratch-Offs-Tabs.aspx?g=ag#remaining-prizes'
        soup = soup = BeautifulSoup(requests.get(url).text, 'lxml')
        table = soup.find('table', attrs = {'title': 'Remaining Games'})

        for tr in table.tbody.find_all('tr'):
            game = tr.find('a').string
            self.gNames.append(game)
            
            for z in tr.find_all('div', attrs={'class':'remaining-detail'}):
                if (str(z.text)[0] == "$" or
                    str(z.text)[0].isalpha() == True):
                    # Checks for prizes like cars, all returns True/False
                    if bool(z.text) == all(c.isalpha() for c in z.text):
                        Cars = z.text.replace(z.text[:],'30000')
                        self.gPrize.append(int(cars))
                        
                    # Checks for prizes like 100k for life or something
                    elif bool(z.text) == any(c.isalpha() for c in z.text):
                        LifePrize = z.text.replace(z.text[:],'400000')
                        self.gPrize.append(int(LifePrize))
                        
                    # if neither car nor prize continues as usual
                    else:
                        p = z.text.replace('$','').replace(',','').replace('.00','')
                        self.gPrize.append(int(p))
                else:
                    l = z.text.replace(',','').replace('.00','')
                    self.gLeft.append(int(l))
                    
        # Grabing the cost for each game.
        for td in table.tbody.find_all('td'):
            cost = str(td.text)
            if cost[0] == '$':
                cost = cost.strip('$')
                self.gCost.append(int(cost))
                
        # Small test to make sure there is a equal amount of names and cost
        assert len(self.gNames) == len(self.gCost)

    def _FormStructure(self):
        """ This method forms the main Data Structure to make use of. """
        start = -6
        for i,name in enumerate(self.gNames):
            start += 6
            # Creates a new dict to hold the Game data,
            # PA website only yeilds 6 prizes/left for each game.
            self.gStruct.append({})
            self.gStruct[i]['Game'] = name
            self.gStruct[i]['Cost'] = self.gCost[i]
            self.gStruct[i]['Prize'] = self.gPrize[start:start+6]
            self.gStruct[i]['Left'] = self.gLeft[start:start+6]

    def init(self):
        """
        MUST run this init with every new object of the class to get the right,
        information for gStruct. Otherwise, it'll  be empty.
        """
        self._ExtractData()
        self._FormStructure()
