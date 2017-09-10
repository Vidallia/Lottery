# PennScratchers 0.1.1

try:
    import requests
    from bs4 import BeautifulSoup
    # map()
except ImportError as e:
    print(f"{e}\nTry using pip to install the package...")

class PaLottery:
    def __init__(self):
        """
         Names = The Scratch-Offs name
         Cost = The Cost of each game
         Prize = The games prizes
         Left = The amount of prizes left
         Struct contains the information for each game as a list of Dictionaries.
        """
        self.Names  = []
        self.Costs   = []
        self.Prizes  = []
        self.Left   = []
        self.Struct = []

        # Scrape/Extract all of the data and fill up all list attributes.
        self.init()

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
            self.Names.append(game)
            for z in tr.find_all('div', attrs={'class':'remaining-detail'}):
                if (str(z.text)[0] == "$" or
                    str(z.text)[0].isalpha() == True):
                    # Checks for prizes like cars, all returns True/False
                    if bool(z.text) == all(c.isalpha() for c in z.text):
                        Cars = z.text.replace(z.text[:],'30000')
                        self.Prizes.append(int(cars))
                    # Checks for prizes like 100k for life or something
                    elif bool(z.text) == any(c.isalpha() for c in z.text):
                        LifePrize = z.text.replace(z.text[:],'400000')
                        self.Prizes.append(int(LifePrize))
                    # if neither car nor prize continues as usual
                    else:
                        p = z.text.replace('$','').replace(',','').replace('.00','')
                        self.Prizes.append(int(p))
                else:
                    l = z.text.replace(',','').replace('.00','')
                    self.Left.append(int(l))
        # Grabing the cost for each game.
        for td in table.tbody.find_all('td'):
            cost = str(td.text)
            if cost[0] == '$':
                cost = cost.strip('$')
                self.Costs.append(int(cost))
        # Small test to make sure there is a equal amount of names and cost
        assert len(self.Names) == len(self.Costs)

    def _FormStructure(self):
        """ This method forms the main Data Structure to make use of. """
        start = -6
        for i,x in enumerate(self.Names):
            start += 6
            # Creates a new dict to hold the Game data,
            # PA website only yeilds 6 prizes/left for each game.
            self.Struct.append({})
            self.Struct[i]['Game'] = x
            self.Struct[i]['Cost'] = self.Costs[i]
            self.Struct[i]['Prize'] = self.Prizes[start:start+6]
            self.Struct[i]['Left'] = self.Left[start:start+6]

    def init(self):
        """
        Ran at the creation of each object. This will fill up list attributes.
        """
        self._ExtractData()
        self._FormStructure()
