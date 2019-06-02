class Crime:
    def __init__(self, dateTime, address, district, beat, grid, crimeDesc, UCR_NCIC, latitude, longitude):
        self.dateTime = dateTime
        self.address = address
        self.district = district
        self.beat = beat
        self.grid = grid
        self.crimeDesc = crimeDesc
        self.UCR_NCIC = UCR_NCIC
        self.latitude = latitude
        self.longitude = longitude

    def printCrime(self):
        return self.dateTime+" "+self.address