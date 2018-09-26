# Travelling Salesman Problem Using Simulated Annealing

This package solves the Travelling Salesman Problem (TSP) using Simulated Annealing (SA). 


## Required Libraries
- Numpy
- Pandas
- Matplotlib
- Math

## Installation
The *satsp*  package can be installed using *pip*:
```
pip install satsp
```

## Usage
Basic usage:
```
from satsp import solver

cities = [[1, 6.0, 7.0],
          [2, 4.0, 9.0],
	  [3, 7.0, 1.0]]

solver.Solve(cities)
solver.PrintSolution()
```

The three columns in cities represent id, x coordinate and y coordinate.

Advanced Usage:
```
<<<<<<< HEAD
solver.Solve(city_list = None, dist_matrix = None, start_temp = None, \
          stop_temp = None, alpha = None, epochs = None, epoch_length = None, \
          epoch_length_factor = 1.00, stopping_count = 100, screen_output = True)
=======
solver.Solve(city_list = None, dist_matrix = None, start_temp = None, 
          stop_temp = None, alpha = None, epochs = None, epoch_length = None, 
          epoch_length_factor = 1.00, stopping_count = 100, screen_output = True):
>>>>>>> 72d2547a53f52e0452304c1e66e1970875cd7d85
```
Arguments of ```solver.Solve()``` function:

*city_list*: a N*3 matrix containing three columns representing id, x coordinate and y coordinate of the N cities. Can be ```None```.

*dist_matrix*: a N*N matrix containing the distances between the N cities. If ```None``` is passed and a ```None``` *city_list* is passed, the program will calculate the Eclidean distances between the cities. If both *city_list* and *dist_matrix* are ```None```, a test instance with 48 cities will be solved.

*start_temp*: initial temperature for SA. If None is passed, the program will estimate the initial temperature using a small sample from the data.

*stop_temp*: stopping temperature for SA. Can be ```None```.

*alpha*: cooling rate for SA. If ```None``` is passed, the program will calculate alpha if *stop_temp* and *epochs* are given. Otherwise *alpha* is set at 0.99.

*epochs*: number of epochs for SA. A decisive factor for the running time of the algorithm. The program will terminate after this number of epochs. If ```None``` is passed, and *stop_temp* and *alpha* are given, the program will calculate number of epochs. Otherwise, the stopping condition will be switched to no improvement after a certain number of epochs, where the number is decided by *stopping_count*.

*epoch_length*: number of iterations in each epoch. The default is min(100, N*(N-1) / 2).

*epoch_length_factor*: the rate at which epoch length increases at each epoch. Should be greater than or equal to 1. Default is 1.00. A small value is recommended for large instances.

*stopping_count*: the number of epochs after which the program will stop if no improvement is made. This stopping condition is only activated if the number of total epochs is neither specified by the user nor can be calculated by the program. Default is 100.
*screen_output*: Parameters of SA, progress of the algorithm and the results will be displayed if set to ```True```. Default is ```True```.

###
Other functions provided by ```solver```:
```solver.GetBestDist()```: return the total distance of the best TSP tour
```solver.GetBestTour()```: return a list of cities of the best TSP tour
```solver.PrintBestTour()```: Output a picture drawing the best TSP tour
```solver.PrintConvergence()```: Plot the convergence of the distances at the end of each epoch


## Algorithm
This package implements the simulated annealing (SA) metaheuristic to solve TSP. A sketch of the algorithm is as follows:
1. Generate a random initial tour, and set an initial temperature.
2. Set a number for the iterations to be performed, determined by epoch length.
3. Randomly pick two cities in the tour and perform a "2-opt" operation, i.e., reverse the tour between the two cities.
4. If a tour with shorter distance is obtained, accept the new tour. Otherwise, accept the new tour with a certain probability determined by the difference between old and new distances and the current temperature.
5. Repeat 3-4 for the number of iterations determined in 2.
6. If a stopping condition is met, terminate. Otherwise go to 7.
7. Decrease the temperature and repeat 2-5.


## References
Kirkpatrick, Scott, C. Daniel Gelatt, and Mario P. Vecchi. "Optimization by simulated annealing." Science 220.4598 (1983): 671-680.

Park, Moon-Won, and Yeong-Dae Kim. "A systematic procedure for setting parameters in simulated annealing algorithms." Computers & Operations Research 25.3 (1998): 207-217.
