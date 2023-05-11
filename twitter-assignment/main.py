from building import Building

option = int(input("for rect click 1 for triangular click 2 for Exit click 3 "))
while option != 3:
    if option == 1:
        width = int(input("Choose a width "))
        height = int(input("Choose a height "))
        building = Building(width, 'R', height)
        building.information()
    else:
        width = int(input("Choose a width "))
        height = int(input("Choose a height "))
        building = Building(width, 'T', height)
        building.information()
    option = int(input("for rect click 1 for triangular click 2 for Exit click 3 "))
