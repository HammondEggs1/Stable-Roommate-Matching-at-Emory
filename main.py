import student
import re
from api_connector import getStudentData
from model import solve_SRI, OptimalityCriteria
from feasibility_checker import check_feasibility



# takes an array of all students and generates a two dimensional nxn array of preferences.
# First, every student is compared to every other student using compareStudents(), then
# the scores are pairwise sorted to produce an nxn array where [i][j] represents student
# i's jth choice to be their match
def calculatePreferences(students):
    preferences = [[0 for x in range(len(students)-1)] for y in (range(len(students)))] 

    for i, student in enumerate(students):
        for j in range(len(students)):
            if(i > j):
                preferences[i][j] = student.compareStudents(students[j])
            elif (i < j):
                preferences[i][j-1] = student.compareStudents(students[j])
    prefIndeces = [[0 for x in range(len(students)-1)] for y in range(len(students))] 

    print(preferences)

    for i, preference in enumerate(preferences):
        for j in range(len(preferences)):
            if(i > j):
                prefIndeces[i][j] = j
            elif (i < j):
                prefIndeces[i][j-1] = j

        pairwiseQuickSort(preference, prefIndeces[i], 0, len(preference)-1)

    print(prefIndeces)

    return prefIndeces


def pairwisePartition(array, indices, low, high):
 
    # choose the rightmost element as pivot
    pivot = array[high]
 
    # pointer for greater element
    i = low - 1
 
    # traverse through all elements
    # compare each element with pivot
    for j in range(low, high):
        if array[j] <= pivot:
 
            # If element smaller than pivot is found
            # swap it with the greater element pointed by i
            i = i + 1
 
            # Swapping element at i with element at j
            (array[i], array[j]) = (array[j], array[i])
            (indices[i], indices[j]) = (indices[j], indices[i])
 
    # Swap the pivot element with the greater element specified by i
    (array[i + 1], array[high]) = (array[high], array[i + 1])
    (indices[i + 1], indices[high]) = (indices[high], indices[i + 1])
 
    # Return the position from where partition is done
    return i + 1
 
# function to perform quicksort
 
 # Pairwise Quicksort adapted from Geeks for Geeks Quicksort code
def pairwiseQuickSort(array, indices, low, high):
    if low < high:
 
        # Find pivot element such that
        # element smaller than pivot are on the left
        # element greater than pivot are on the right
        pi = pairwisePartition(array, indices, low, high)
 
        # Recursive call on the left of pivot
        pairwiseQuickSort(array, indices, low, pi - 1)
 
        # Recursive call on the right of pivot
        pairwiseQuickSort(array, indices, pi + 1, high)


students = getStudentData()

prefArray = calculatePreferences(students)
matches = str(solve_SRI(prefArray, optimisation = OptimalityCriteria.EGALITARIAN)).splitlines()[-1:]
matches = [int(s) for s in re.findall(r'\b\d+\b', matches[0])]
print(matches)
for i in range(int(len(matches)/2)):
    student1 = students[int(matches[i*2])-1].name
    student2 = students[int(matches[i*2+1]-1)].name
    print("Match "+str(i+1)+": "+student1+" and "+student2)