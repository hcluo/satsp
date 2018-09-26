from satsp import utilities as hp
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt

class SimulatedAnnealing:
	
    def __init__(self, city_list, dist_matrix, start_temp, stop_temp, alpha, \
                 epochs, epoch_length, epoch_length_factor, stopping_count, \
                 screen_output):
        self.city_list = city_list
        self.dist_matrix = dist_matrix
        self.start_temp = start_temp
        self.stop_temp = stop_temp
        self.alpha = alpha
        self.epochs = epochs
        self.epoch_length = epoch_length
        self.epoch_length_factor = epoch_length_factor
        self.stopping_count = stopping_count
        self.screen_output = screen_output
        self.temperature = []
        self.convergence = []
		
        # Load test instance if none is given
        if self.city_list is None and self.dist_matrix is None:
            self.city_list = hp.LoadDefault()
		
		  # Calculate distance matrix
        if self.city_list is not None:
            self.city_list = pd.DataFrame(self.city_list)
        if self.dist_matrix is None:
            self.dist_matrix = hp.CalDist(self.city_list)
        else:
            self.dist_matrix = pd.DataFrame(self.dist_matrix)
        if self.city_list is None:
            self.num_cities = len(self.dist_matrix)
        else:
            self.num_cities = len(self.city_list)
    
        # Set initial solution
        self.tour = [i for i in range(self.num_cities)] 
        self.tour_distance = []
        for i in range(self.num_cities-1):
            self.tour_distance.append( \
                self.dist_matrix.iloc[self.tour[i], self.tour[i+1]])
        self.tour_distance.append( \
            self.dist_matrix.iloc[self.tour[self.num_cities-1],self.tour[0]])
        self.current_dist = sum(self.tour_distance)
        self.best_so_far = self.incumbent_dist = self.current_dist
        self.incumbent_tour = self.tour
    
        # Set parameters
        if self.start_temp is None:
            self.SetStartTemp()
        self.current_temp = self.start_temp
    
        if self.stop_temp is not None and self.epochs is not None \
                and self.alpha is None:
            self.alpha = (self.stop_temp / self.start_temp)**(1/(self.epochs-1))
    
        if self.stop_temp is not None and self.alpha is not None \
                and self.epochs is None:
            self.epochs = int(math.log(self.stop_temp / self.start_temp, \
                    self.alpha))
        
        if self.epoch_length is None:
            self.epoch_length = min(100, \
                    int(self.num_cities * (self.num_cities - 1) / 2))
    
        if self.alpha is None:
            self.alpha = 0.99
    
        # Stopping condition can be either number of epochs or the 
        # non-imporvement of the best solution;
        # In case that number of epochs is not given, the stopping condition 
        # is set to be no improvement of the best solution after 100 epochs
        self.stopping_cond = False
        if self.epochs is None:
            self.epochs = int(1e10)
            self.stopping_cond = True
            self.reset_counter = 0
        self.epoch_count = 0
    
    def SetStartTemp(self):
        # Set the initial temperature for SA
        # Use a sample of 50 cities for estimation
        
        city_indices = [i for i in range(self.num_cities)]
        if(self.num_cities > 50):
            sample_indices = np.random.choice(city_indices, 50, False)
        else:
            sample_indices = city_indices
        sample_size = len(sample_indices)
    
        tour = [sample_indices[i] for i in range(sample_size)]
        tour_distance = []
        for i in range(sample_size - 1):
            tour_distance.append(self.dist_matrix.iloc[tour[i],tour[i+1]])
        tour_distance.append(self.dist_matrix.iloc[tour[sample_size - 1],tour[0]])

        count = 0
        sumdist = 0
        for i in range(min(100, int(sample_size * (sample_size-1) / 2))):
            ind_to_swap_1 = np.random.randint(1,sample_size)
            ind_to_swap_2 = np.random.randint(1,sample_size)
            while ind_to_swap_1 == ind_to_swap_2:
                ind_to_swap_2 = np.random.randint(1,sample_size)
        
            if ind_to_swap_1  > ind_to_swap_2:
                temp = ind_to_swap_1
                ind_to_swap_1 = ind_to_swap_2
                ind_to_swap_2 = temp
        
            city_to_swap_1 = tour[ind_to_swap_1]
            city_to_swap_2 = tour[ind_to_swap_2]
        
            dist_before_swap = tour_distance[ind_to_swap_1-1] + \
                    tour_distance[ind_to_swap_2]
            dist_after_swap = self.dist_matrix.iloc[tour[ind_to_swap_1 - 1], \
                    city_to_swap_2] + self.dist_matrix.iloc[city_to_swap_1, \
                    tour[(ind_to_swap_2 + 1) % sample_size]]
            dist = dist_before_swap - dist_after_swap
            if dist < 0:
                count += 1
                sumdist += dist
        if count == 0:
            self.start_temp = 10000
        else:
            self.start_temp = (sumdist / count) / np.log(0.9)

    def PrintParam(self):
        if self.screen_output:
            print("Simulated Annealing starts with parameters:")
            print("Initial Temperature: ", self.start_temp)
            print("Cooling Rate: ", self.alpha)
            print("Initial Epoch Length: ", self.epoch_length)
            if self.stopping_cond:
                print("Stopping Criterion: No Improvement for " + \
                        str(self.stopping_count) + " epochs\n")
            else:
                print("Stopping Criterion: After " + str(self.epochs) + " epochs\n")
    
    def TwoOpt(self, ind_to_swap_1, ind_to_swap_2):
        # Given the indices of two cities, swap the orders of the cities along the path
        # between the cities
        i, j = ind_to_swap_1, ind_to_swap_2
        while i < j:
            temp = self.tour[i]
            self.tour[i] = self.tour[j]
            self.tour[j] = temp
            i += 1
            j -= 1
        for i in range(len(self.tour_distance)):
            self.tour_distance[i] = self.dist_matrix.iloc[self.tour[i], \
                    self.tour[(i+1) % len(self.tour_distance)]]
    
    
    def Annealing(self):
        for i in range(self.epochs):
            for j in range(self.epoch_length):
                # Randomly pick two cities for 2-opt
                ind_to_swap_1 = np.random.randint(1,self.num_cities)
                ind_to_swap_2 = np.random.randint(1,self.num_cities)
                while ind_to_swap_1 == ind_to_swap_2:
                    ind_to_swap_2 = np.random.randint(1,self.num_cities)
            
                if ind_to_swap_1  > ind_to_swap_2:
                    temp = ind_to_swap_1
                    ind_to_swap_1 = ind_to_swap_2
                    ind_to_swap_2 = temp
            
                city_to_swap_1 = self.tour[ind_to_swap_1]
                city_to_swap_2 = self.tour[ind_to_swap_2]
            
                dist_before_swap = self.tour_distance[ind_to_swap_1-1] + \
                        self.tour_distance[ind_to_swap_2]
                dist_after_swap = self.dist_matrix.iloc[self.tour[ind_to_swap_1 - 1], \
                        city_to_swap_2] + self.dist_matrix.iloc[city_to_swap_1, \
                        self.tour[(ind_to_swap_2 + 1) % self.num_cities]]
            
                # If swapping yield a better objective, then perform 2-opt
                if dist_before_swap > dist_after_swap:
                    self.TwoOpt(ind_to_swap_1, ind_to_swap_2)
                    self.current_dist -= (dist_before_swap - dist_after_swap)
                    if self.incumbent_dist > self.current_dist:
                        self.incumbent_dist = self.current_dist
                        self.incumbent_tour = self.tour
                    continue
            
                # Otherwise, calculate a threshold for accepting uphill move
                if ((dist_after_swap - dist_before_swap)/self.current_temp) > 709:
                                                    # python limit for exponential
                    continue
                rand_num = np.random.rand()
                threshold = 1/(np.exp((dist_after_swap - dist_before_swap)/ \
                        self.current_temp))
			
                # If a random number is less than the threshold, then accept the 
                # uphill move
                if rand_num <= threshold:
                    self.TwoOpt(ind_to_swap_1, ind_to_swap_2)
                    self.current_dist -= (dist_before_swap - dist_after_swap)
        
		
            self.temperature = np.append(self.temperature, self.current_temp)
            self.convergence.append(self.current_dist)
            if self.screen_output:
                print("Epoch ", i + 1)
                print("Temperature: ", self.current_temp)
                print("Epoch Length: ", self.epoch_length)
                print("Current Dist: ", self.current_dist)
                print("Best Dist: ", self.incumbent_dist)
            
            # Decrease the temperature
            self.current_temp = self.alpha * self.current_temp
            # Increase the epoch length
            self.epoch_length = min(int(self.epoch_length_factor * \
                    self.epoch_length), int(self.num_cities * (self.num_cities-1) / 2))
            self.epoch_count += 1
            # Break the loop if number of epochs without improvement has met 
            # the stopping criterion value
            if self.stopping_cond:
                if self.best_so_far > self.incumbent_dist:
                    self.best_so_far = self.incumbent_dist
                    self.reset_counter = 0
                else:
                    self.reset_counter += 1
                if self.reset_counter == self.stopping_count:
                    break
                
        print("\nSimulated Annealing terminated after " + str(self.epoch_count) + \
                " epochs.")

    def GetBestTour(self):
        if self.city_list is None:
            incumbent_tour_cities = [i + 1 for i in self.incumbent_tour]
        else:
            incumbent_tour_cities = [self.city_list.iloc[i,0] for i in self.incumbent_tour]
        return incumbent_tour_cities
        
		
    def PrintBestTour(self):
        # Print the best TSP tour
        if self.city_list is not None:
            x = []
            y = []
            for i in self.incumbent_tour:
                x.append(self.city_list.iloc[i,1])
                y.append(self.city_list.iloc[i,2])
            plt.plot(x, y, 'co', color = 'black')
            for i in range(0,len(x)-1):
                plt.arrow(x[i], y[i], (x[i+1] - x[i]), (y[i+1] - y[i]), \
                          color = 'black', length_includes_head = True)
            plt.arrow(x[-1], y[-1], (x[0] - x[-1]), (y[0] - y[-1]), \
                      color ='black', length_includes_head=True)
		
            plt.axis('off')
            plt.show()
    
    def PrintConvergence(self):
        # Plot the convergence of SA
        plt.plot(self.temperature,self.convergence)
        plt.title("Distance vs. Temperature",fontsize=18)
        plt.xlabel("Temperature",fontsize=18)
        plt.ylabel("Distance",fontsize=18)
        plt.xlim(self.start_temp, self.current_temp)
		
        plt.show()
    