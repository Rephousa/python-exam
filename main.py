from crime import Crime
import csv
import math
import json
import os

FILE_NAME = "SacramentocrimeJanuary2006.csv"
crimes = []
crimesResult = []


def main():
    loadCSV()

    while(True):
        print("\n What do you want to?:")
        print("1 - Search in the dataset") #done
        print("2 - Get all crimes in 5 km distance of given point") #done - needs exporting search result
        print("3 - Add a new record")
        print("4 - Export whole dataset to JSON") #done
        print("5 - Export whole dataset to HTML") #done
        print("6 - Exit program") #done

        choice = 0
        try:
            choice = int(input("Choice (Enter the number): "))

            if(choice < 1 or choice > 6):
                print("\nWARNING: Only the listed options are available, please try again.")
        except TypeError:
            print("\nWARNING: You must enter a valid number.")
        except ValueError:
            print("\nWARNING: You must enter a valid number.")

        if(choice == 1):
            clearResults()
            counter = 0
            searchString = input("Enter the string you want to search for: ").upper()

            for crime in crimes:
                if(
                    crime.dateTime.find(searchString) != -1 or
                    crime.address.find(searchString) != -1 or
                    crime.district.find(searchString) != -1 or
                    crime.beat.find(searchString) != -1 or
                    crime.grid.find(searchString) != -1 or
                    crime.crimeDesc.find(searchString) != -1 or
                    crime.UCR_NCIC.find(searchString) != -1 or
                    crime.latitude.find(searchString) != -1 or
                    crime.longitude.find(searchString) != -1
                ):
                    crimesResult.append(crime)
                    print(crime.printCrime())
                    counter += 1

            print("Found "+str(counter)+" entries.")
            wantToExport()
                

        if(choice == 2):
            clearResults()
            latitude = 0
            longitude = 0

            while(True):
                try:
                    latitude = float(input("Latitude (between -90 to 90): "))
                    longitude = float(input("Longitude (between -180 to 180): "))

                    if(latitude < -90 or latitude > 90 or longitude < -180 or longitude > 180):
                        print("\nWARNING: Only the listed options are available, please try again.")
                    else:
                        break
                except ValueError:
                    print("\nWARNING: There was an error reading the values, try again.")

            for crime in crimes:
                if(calculateDistance(latitude, longitude, crime.latitude, crime.longitude) <= 5):
                    crimesResult.append(crime)
                    print(crime.printCrime())
                
            wantToExport()

        if(choice == 3):
            addNewRecord()

        if(choice == 4):
            exportToFile("JSON", crimes)

        if(choice == 5):
            exportToFile("HTML", crimes)

        if(choice == 6):
            break

def exportToFile(type, datas):
    if(type == "HTML"):
        exportString = """
            <html>
                <head>
                </head>
                <body>
                    <table>
                        <tr>
                            <th>Datetime:</th>
                            <th>Address:</th>
                            <th>District:</th>
                            <th>Beat:</th>
                            <th>Grid:</th>
                            <th>Crime Description:</th>
                            <th>UCR_NCIC:</th>
                            <th>Latitude:</th>
                            <th>Longitude:</th>
                        </tr>
        """

        for data in datas:
            exportString += """
            <tr>
                <td>"""+data.dateTime+"""</td>
                <td>"""+data.address+"""</td>
                <td>"""+data.district+"""</td>
                <td>"""+data.beat+"""</td>
                <td>"""+data.grid+"""</td>
                <td>"""+data.crimeDesc+"""</td>
                <td>"""+data.UCR_NCIC+""":</td>
                <td>"""+data.latitude+"""</td>
                <td>"""+data.longitude+"""</td>
            </tr>
        """

        exportString += """
            </table></body></html>
        """

        file = open("export.html", "w")
        file.write(exportString)
        file.close()

    elif(type == "JSON"):
        jsonArray = []

        file = open("export.json", "w")

        for data in datas:
            jsonArray.append(data.__dict__)
        
        file.write(json.dumps(jsonArray, indent=4))
        file.close()

        

def calculateDistance(latitudeA, longitudeA, latitudeB, longitudeB):
    #Code found stackoverflow to calculate distances
    earthRadius = 6371

    dLat = math.radians(float(latitudeB) - latitudeA)
    dLon = math.radians(float(longitudeB) - longitudeA)

    latA = math.radians(latitudeA)
    latB = math.radians(float(latitudeB))

    a = math.sin(dLat / 2) * math.sin(dLat / 2) + math.sin(dLon / 2) * math.sin(dLon / 2) * math.cos(latA) * math.cos(latB)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return earthRadius * c * 1000 #Returned in km
            
def loadCSV():
    global crimes
    
    print("Loading csv file, please wait!")

    with open(FILE_NAME) as csv_file:
        reader = csv.reader(csv_file, delimiter=",")
        count = 0
        firstLine = True

        for row in reader:
            if(firstLine != True):
                crimes.append(Crime(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8]))
                count += 1
            else:
                firstLine = False
            
    print("Loaded " + str(count) + " lines.")

def clearResults():
    global crimesResult
    crimesResult = []

def wantToExport():
    wantToExport = input("Do you want to export the search result? (y/n): ")

    if(wantToExport == "Y" or wantToExport == "y"):
        while(True):
            try:
                exportType = input("What type of export? (html/json): ")

                if(exportType == "html"):
                    exportToFile("HTML", crimesResult)
                    break
                elif(exportType == "JSON"):
                    exportToFile("JSON", crimesResult)
                    break
                else:
                    print("Input er ikke gyldt, indtast html eller json.")
            except TypeError:
                print("Ugyldigt input! Prøv igen.")

def addNewRecord():
    while(True):
        print("Enter the data in the following order, each field should be seperated by a comma \",\", if you need to make a comma in the sentence, make a punctation instead")
        print("Datetime, Address, District, Beat, Grid, Crime Description, UCR_NCIC, Latitude, Longitude:")

        try:
            addInput = input("Record: ")

            addInputArray = addInput.split(",")

            if(len(addInputArray) == 9):
                crimes.append(Crime(addInputArray[0],addInputArray[1],addInputArray[2],addInputArray[3],addInputArray[4],addInputArray[5],addInputArray[6],addInputArray[7],addInputArray[8]))

                f = open(FILE_NAME, "a+")
                f.write("\n"+addInput)
                f.close()
                print("Record was added.")
                break
            else:
                print("Input was incorrect, needs 9 parameteres, try again.")
        except TypeError:
            print("Try again")


if __name__ == "__main__":
    main()