from random import random
from math import e, log
from copy import deepcopy

# Create a cube of voxels with random attenuation coefficients between 1 and 2
cube = []
for i in range(5):
    cube.append([])
    for j in range(5):
        cube[i].append([])
        for k in range(5):
            cube[i][j].append([])
            cube[i][j][k] = random() + 1

# Create 3 square projections of the cube where the initial intensity is 1 and is attenuated by the voxels of length 1
# This performs the integral
Pij = []
Pjk = []
Pik = []
for i in range(5):
    Pij.append([])
    Pik.append([])
    for j in range(5):
        Pij[i].append(1)
        if i == 0:
            Pjk.append([])
        for k in range(5):
            if j == 0:
                Pik[i].append(1)
            if i == 0:
                Pjk[j].append(1)
            Pij[i][j] *= e ** -cube[i][j][k]
            Pik[i][k] *= e ** -cube[i][j][k]
            Pjk[j][k] *= e ** -cube[i][j][k]

# define a way to round to a specified number of digits to prevent differences of a couple bytes from performing different operations
# on numbers that would turn out the same if not for precision errors
def roundDigits(num, digits):
    return round(num * 10 ** digits) / 10 ** digits

# Print the square projections and print a cube in layers, if it is a square, also adjust its values by taking the natural log and dividing by -5
# To get the average attenuation as described in the theory section
def printSquare(square, digits, truth):
    if truth:
        print('square')
    for i in range(len(square)):
        row = []
        for j in range(len(square[0])):
            if truth:
                square[i][j] = -log(square[i][j]) / 5
            row.append(square[i][j])
        print(*[roundDigits(i, digits) for i in row])
    print('')

# Prints the values of the randomly generated cube
def printCube(cube, digits, truth):
    print('cube')
    for i in range(len(cube)):
        print('i =', i)
        printSquare(cube[i], digits, truth)

printSquare(Pij, 3, True)
printSquare(Pik, 3, True)
printSquare(Pjk, 3, True)
printCube(cube, 3, False)

# Check each pixel of each projection to see if the average attenuation is calculated properly
for i in range(5):
    for j in range(5):
        print(roundDigits(Pij[i][j], 5) == roundDigits(sum(cube[i][j][:]) / 5, 5))
        print(roundDigits(Pik[i][j], 5) == roundDigits(sum([cube[i][k][j] for k in range(5)]) / 5, 5))
        print(roundDigits(Pjk[i][j], 5) == roundDigits(sum([cube[k][i][j] for k in range(5)]) / 5, 5))

# Make an initial guess at a solution for the cube
reconstructedCube = []
for i in range(5):
    reconstructedCube.append([])
    for j in range(5):
        reconstructedCube[i].append([])
        for k in range(5):
            reconstructedCube[i][j].append([])
            reconstructedCube[i][j][k] = Pij[i][j] / 3 + Pjk[j][k] / 3 + Pik[i][k] / 3

def divide(row, num):
    for i in range(len(row)):
        row[i] /= num
    return row

def distance(Pij, Pik, Pjk, cube):
    dist = 0
    for i in range(5):
        for j in range(5):
            dist += abs(Pij[i][j] - sum([cube[i][j][k] for k in range(5)]) / 5)
            dist += abs(Pik[i][j] - sum([cube[i][k][j] for k in range(5)]) / 5)
            dist += abs(Pjk[i][j] - sum([cube[k][i][j] for k in range(5)]) / 5)
    return dist

# attempt a reconstruction. It is late and I don't even understand what I wrote well enough to write a descriptive comment.
# it was supposed to be like a monte carlo sequence
previousCubes = []
iterations = 0
l = 0
while reconstructedCube != cube and iterations < 100000:
    if len(previousCubes) != l:
        iterations = 0
        l = len(previousCubes)
        print(l)
        print(distance(Pij, Pik, Pjk, previousCubes[-1]))
    if previousCubes != [] and distance(Pij, Pik, Pjk, reconstructedCube) < distance(Pij, Pik, Pjk, previousCubes[-1]):
        previousCubes.append(deepcopy(reconstructedCube))
    elif previousCubes != []:
        reconstructedCube = deepcopy(previousCubes[-1])
    else:
        previousCubes.append(deepcopy(reconstructedCube))
    for i in range(5):
        for j in range(5):
            if random() < 0.5:
                divisor = sum([reconstructedCube[i][j][k] for k in range(5)]) / 5 / Pij[i][j]
                for k in range(5):
                    reconstructedCube[i][j][k] /= divisor
    for i in range(5):
        for k in range(5):
            if random() < 0.5:
                divisor = sum([reconstructedCube[i][j][k] for j in range(5)]) / 5 / Pik[i][k]
                for j in range(5):
                    reconstructedCube[i][j][k] /= divisor
    for j in range(5):
        for k in range(5):
            if random() < 0.5:
                divisor = sum([reconstructedCube[i][j][k] for i in range(5)]) / 5 / Pik[j][k]
                for j in range(5):
                    reconstructedCube[i][j][k] /= divisor
    iterations += 1
print(iterations)

print(reconstructedCube == cube)
printCube(reconstructedCube, 3, False)
printCube(cube, 3, False)



