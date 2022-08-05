"""
~~~~~~~~~~~~~~~~~~~~~
Optimal Matching!
C-Love!
Ben Gao
8/5/22
~~~~~~~~~~~~~~~~~~~~~
Given csv of format:
FirstName, LastName, O, O, C, C, E, E, A, A, N, N
where O,C,E,A,N are the scores for openness, neuroticism,
extraversion, agreeableness, and conscientiousness, main
outputs either the optimal (stable) matches or a list, 
in order of the most compatible matches for each figure. 
~~~~~~~~~~~~~~~~~~~~~
Example: 
First,Last,-2,-2,-1,0,0,1,1,1,1,-1
Firsts2,Lasst2,1,-1,-2,1,-1,2,1,-2,2,2
another,name,-1,-2,1,1,1,2,1,1,-1,0
another2,name5,-1,2,1,-1,1,2,1,2,-1,0
~~~~~~~~~~~~~~~~~~~~~
"""

import math
from matching.games import StableRoommates


class Resident:
    
    def __init__(self, firstName: str, lastName: str, O: int, C: int, E: int, A: int, N: int):
        self.firstName = firstName
        self.lastName = lastName
        self.name = self.firstName + self.lastName

        # OCEAN score
        self.openness = O
        self.neuroticism = N
        self.extraversion = E
        self.agreeableness = A
        self.conscientiousness = C

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name

    def getSimilarity(self, other):
        person1 = [self.openness, -self.neuroticism, self.extraversion, self.agreeableness, self.conscientiousness]
        person2 = [other.openness, other.neuroticism, other.extraversion, other.agreeableness, other.conscientiousness]
        return math.sqrt(sum(pow(x-y, 2) for x, y in zip(person1, person2)))


def getData(dataSheetName="newResInfoTest.csv"):
    residents = list()
    with open(dataSheetName, "r") as file:
        data = file.readlines()
        for line in data:
            parts = line.split(",")
            scores = [int(parts[idx]) + int(parts[idx + 1]) for idx in range(2, len(parts), 2)]
            resident = Resident(parts[0], parts[1], scores[0], scores[1], scores[2], scores[3], scores[4])
            residents.append(resident)
    return residents


def getPreferences(residents: list):
    preferences = dict()
    for resident in residents:
        otherResidents = [res for res in residents if res != resident]
        otherResidents.sort(key=resident.getSimilarity, reverse=True)
        preferences[resident.name] = [res.name for res in otherResidents]
    return preferences


def getStableMatches(preferences: dict):
    unmatched = StableRoommates.create_from_dictionary(preferences)
    solved = unmatched.solve()
    for resident in solved:
        print(f"The optimal match for {resident} is {solved[resident]}")


def getBestList(preferences: dict):
    for resident in preferences:
        print(f"In order, the most compatible residents for {resident} are: ")
        for index, res in enumerate(preferences[resident]):
            print(index + 1, f"{res}")


def main():
    if input("Space for Stable else Best: ") == "":
        getStableMatches(getPreferences(getData()))
    else:
        getBestList(getPreferences(getData()))


# https://www.typematchapp.com/who-should-you-date-based-on-your-big-5-personality-results/


if __name__ == "__main__":
    main()
