from satsp.SAclass import SimulatedAnnealing

sa_obj = None

def Solve(city_list = None, dist_matrix = None, start_temp = None, \
          stop_temp = None, alpha = None, epochs = None, epoch_length = None, \
          epoch_length_factor = 1.00, stopping_count = 100, screen_output = True):
    
# Solve the TSP given an instance
# @param city_list a dataframe containing three columns on city information: id, x, y
# @param dist_matrix a dataframe containing the distances between the cities
# @param start_temp initial temperature for SA. Will be estimated if not given
# @param stop_temp stopping temperature for SA
# @param alpha cooling rate for SA
# @param epochs number of epochs for SA. If not given, the stopping condition
# will be set to non-improvement after stopping_count
# @param epoch_length initial epoch length for SA
# @param epoch_length_factor the rate at which epoch length increases at each epoch
# @param stopping_count the number of epochs after which the program will stop if no 
# improvement is made, if epochs is not given
# @param screen_output Parameters, progress of the algorithm and the results
# will be displayed if set to True
# @return the total distance of the best TSP tour found
    
    try:
        global sa_obj
        sa_obj = SimulatedAnnealing(city_list, dist_matrix, start_temp, \
                                    stop_temp, alpha, epochs, epoch_length, \
                                    epoch_length_factor, stopping_count, \
                                    screen_output)
    except Exception as e:
        print("Cannot initialize instance. " + str(e))
        sa_obj = None
        return
    
    if sa_obj.screen_output:
        sa_obj.PrintParam()
    
    try:
        sa_obj.Annealing()
    except KeyboardInterrupt:
        
        if sa_obj.screen_output:
            print("\nSimulated Annealing terminated after " + \
                  str(sa_obj.epoch_count) + " epochs.")
        return
    except Exception as e:
        print("Cannot process annealing. " + str(e))
        sa_obj = None
        return
        
    return

    
def GetBestDist():
    if sa_obj is None:
        print("Instance not solved correctly.")
        return
    return sa_obj.incumbent_dist

def GetBestTour():
    if sa_obj is None:
        print("Instance not solved correctly.")
        return
    return sa_obj.GetBestTour()

def PrintBestTour():
    if sa_obj is None:
        print("Instance not solved correctly.")
        return
    if sa_obj.city_list is None:
        print("Coordinates not provided.")
        return
    sa_obj.PrintBestTour()

def PrintConvergence():
    if sa_obj is None:
        print("Instance not solved correctly.")
        return
    sa_obj.PrintConvergence()
    
def PrintSolution():
    if sa_obj is None:
        print("Instance not solved correctly.")
        return
    print("Best TSP tour length: ", GetBestDist())
    sa_obj.PrintConvergence()
    
    print("Best TSP tour: ", GetBestTour())
    PrintBestTour()