#-*- coding: utf-8 -*-
import numpy as np

reset_value = 0
enc_pos_prev = 0
enc_pos_prev_kalman = 0
pos_N_1 = 0
N = 100
new_marker_index = -1
encoder_reset = 0

TASK_NUMBER = 4 # Update this value in the beginning of each task!


####################################################
# Task 1: Calculate velocity for different sensors #
####################################################
def calculate_velocity(position1, time1, position2, time2):
    """
    Calculate the velocity based on two positions and 
    the times at which these positions were measured.
    :param position1: A floating point number representing the position of the robot at time1
    :param time1: A floating point number representing the time at which position1 was measured
    :param position2: A floating point number representing the position of the robot at time2
    :param time2: A floating point number representing the time at which position2 was measured
    :return: The velocity calculated from the two positions
    """
    velocity = -(position2-position1)/(time2-time1)
    return velocity


#####################################
# Task 2: Live encoder adjustment   #
#####################################
def measure_with_encoders_enhanced(robot, current_marker_index):
    global encoder_reset
    global new_marker_index
    """
    Calculate the distance to the end of the track using encoders and when the 
    robot moves to the next marker remove any drift accumulated by the encoders.
    :param robot: The same gopigo robot object that you have used in previous labs
    :param current_marker_index: The index of the marker that the robot is currently 
                                 on, it is the same value as the one returned by 
                                 check_markers(marker_sensor_value, current_marker_index) 
                                 that you implemented in the previous lab
    :return: The distance from the end measured with the combination of encoders and markers
    """
    #get the marker distances 
    marker_distances = [1800, 1600, 1300, 900, 600, 400, 200]
    #calculate the value for encoder
    value_encoder = 1800-robot.read_encoders_average()*10
    #this condition is to check if we have gotten a new marker or not
    #if the condition is true, it means we have a new marker 
    if new_marker_index != current_marker_index:
        #reset encoder. marker_distances [current_marker_index] this because the
        #current marker index is incorporated in the marker distance. I then calculate
        #the difference, indicating error.
        encoder_reset =  marker_distances [current_marker_index]- value_encoder        
    new_marker_index = current_marker_index
    #it returns the error and encoder value
    return encoder_reset + value_encoder



############################################
# Task 3: Implement complementary filter   #
############################################
def complementary_filter(us_pos, enc_pos):
    global enc_pos_prev
    global pos_N_1
    """
    Implement the complementary filter.
    :param us_pos: The latest reading from the ultrasonic
    :param enc_pos: The latest reading from the encoders
    :return: The updated position estimate from the complementary filter
    """
    # Fill in the function.
    #function for complemntary value. Here I set the vale for alpa
    #to be very low bucause at higher value there was noise, the ultrasonic
    #spiked forward and the complementary couldnt correct it at that
    #highe alpha value. Also given that the addition of alpha beta should be equal to 1. 
    pos_N = 0.001*us_pos + 0.999*(pos_N_1 + (enc_pos-enc_pos_prev))
    #reset reading from emcoder
    enc_pos_prev = enc_pos
    #reset new postion estimate
    pos_N_1 = pos_N
    return pos_N
    

##############################################
#           Task 4: Kalman Filter            #
# The following code blocks should be edited #
#    while solving the Kalman filter task.   #
##############################################

# A class for performing operations with Gaussians
class Gaussian:
    def __init__(self, mu, sigma):
        # Initializes a Gaussian with given mu and sigma values
        self.mu = mu
        self.sigma = sigma

    def __repr__(self):
        # Allows the gaussian to be displayed as a string
        return f"Gaussian(mu={self.mu}, sigma={self.sigma})"
        
    #################################################
    # Task 4.2: Implement addition of two Gaussians #
    #################################################
    def __add__(self, other: 'Gaussian'):
        """
        Add two gaussians.
        :param self: The previous location estimate gaussian
        :param other: The gaussian to add
        :return: The sum of the two gaussians (which is also a gaussian)
        """
        add = self.mu + other.mu
        sigma = ((self.sigma)**2 + (other.sigma)**2)**0.5
        new_gaussian = Gaussian(add, sigma)
        return new_gaussian

    #######################################################
    # Task 4.3: Implement multiplication of two Gaussians #
    #######################################################
    def __mul__(self, other: 'Gaussian'):
        """
        Multiply two gaussians.
        :param self: The previous location estimate gaussian
        :param other: The gaussian to multiply
        :return: The product of the two gaussians (which is also a gaussian)
        """
        mul = ((self.mu*other.sigma**2) + (other.mu*self.sigma**2))/(self.sigma**2+other.sigma**2)
        inv_sigma = (1/((1/self.sigma**2)+(1/other.sigma**2)))**0.5
        new_mul_gaussian = Gaussian(mul, inv_sigma)
        return new_mul_gaussian


# A Kalman filter class
class Kalman:
    def __init__(self, initial_gaussian: Gaussian):
        # Initializes a Kalman filter with the initial state given as an input
        self.filtered_result = initial_gaussian

    def __repr__(self):
        # Allows the Kalman filter to be displayed as a string
        return f"Kalman({self.filtered_result})"
        
    ########################################
    # Task 4.2: Implement the predict step #
    ########################################
    def predict(self, measurement: Gaussian):
        """
        Kalman filter predict step.
        :param self: The kalman filter instance
        :param measurement: The measurement to predict upon
        :return: The new position estimate
        """
        # Fill in the function
        filtered_result_gausian = self.filtered_result + measurement
        self.filtered_result = filtered_result_gausian
        return filtered_result_gausian.mu

    #######################################
    # Task 4.3: Implement the update step #
    #######################################
    def update(self, measurement: Gaussian):
        """
        Kalman filter update step.
        :param self: The kalman filter instance
        :param measurement: The measurement to update upon
        :return: The new position estimate
        """
        # Fill in the function
        filtered_result_gausian = self.filtered_result * measurement
        self.filtered_result = filtered_result_gausian
        return filtered_result_gausian.mu

# Global variables for holding the encoder difference and camera Gaussians
# and the Kalman class object for use in other files
# DO NOT CHANGE THE NAMES OF THESE VARIABLES!
camera_gaussian = Gaussian(0, 80)
encoder_diff_gaussian = Gaussian(0, 10)
kalman_filter = Kalman(None)

def on_encoder_measurement(enc_pos):
    global enc_pos_prev_kalman
    """
    This function is called every time the robot's encoders 
    receive a new reading. Do Kalman prediction here.
    :param enc_pos: The latest reading from the encoders
    :return: The updated position estimate from the Kalman filter or None if the estimate should not change
    """
    delta_enc = enc_pos-enc_pos_prev_kalman
    encoder_diff_gaussian.mu = delta_enc
    enc_pos_prev_kalman = enc_pos
    if kalman_filter.filtered_result != None:
        #print(kalman_filter)
        return kalman_filter.predict(encoder_diff_gaussian)
        
    return

first_cam_pos = True
#value_cam_pos = []
def on_camera_measurement(cam_pos):
    global first_cam_pos
    """
    This function is called every time the robot calculates a new 
    distance estimate from the camera image. Do Kalman update here.
    :param cam_pos: The latest distance estimate based on the image from the camera
    :return: The updated position estimate from the Kalman filter or None if the estimate should not change
    """
#     if len(value_cam_pos) < N and cam_pos != None:
#         value_cam_pos.append(cam_pos)
#     else:   
#         np.std(value_cam_pos)
#     print ("SD: ", np.std(value_cam_pos))
    
    #this ensures that even if the programme doesnt get a value from the camera it will
    #not stop working and it will do its best to estimate the location and the uncertainty
    #this ensures that even if the programme doesnt get a value from the camera it will
    #not stop working and it will do its best to estimate the location and the uncertainty
    if cam_pos != None:
        camera_gaussian.mu = cam_pos
    #to take just the first meaurement and now take any after(only applicable to task4.3)
        if first_cam_pos == True:
            kalman_filter.filtered_result = camera_gaussian
            first_cam_pos = False
            
        else:
    #the code below is to make sure that when data is received from update() function
    #this should also happen in the on_camera_measurement()
            return kalman_filter.update(camera_gaussian)
   # return np.std(value_cam_pos)
    return None


