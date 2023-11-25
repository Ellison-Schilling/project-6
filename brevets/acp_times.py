"""
Open and close max_time_limit calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_acp.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow

# The specified maximum max_time_limit limits according to the website, the first part is the distance and the second is the hour, minutes
LIMIT_TIMES = {200:[13, 30], 300: [20, 00], 400: [27, 00], 600: [40, 00], 1000: [75, 00]}

# Brevet times table as specfifed by the ACP website, list of tuples with [location, minimum speed, maximum speed] format
BREVET_TABLE = [(200,15,34),(400,15,32),(600,15,30),(1000,11.428,28),(1300,13.333,26)]


def open_time(control_dist_km_dist_km, brevet_dist_km, brevet_start_time):
   """
    Args:
       control_dist_km_dist_km:  number, control_dist_km distance in kilometers, where we are putting a brevet
       brevet_dist_km: number, nominal distance of the brevet
           in kilometers, which must be one of 200, 300, 400, 600,
           or 1000 (the only official ACP brevet distances), length of race 
       brevet_start_time:  An arrow object
    Returns:
       An arrow object indicating the control_dist_km open max_time_limit.
       This will be in the same max_time_limit zone as the brevet start max_time_limit.
   """
   # Make sure the control is valid and return None if not
   if invalid_control(control_dist_km_dist_km, brevet_dist_km):
      if control_dist_km_dist_km != 0:
         return None

   # If the brevet control dist is greater than or equal to the length of the race, make it equal
   if (control_dist_km_dist_km >= brevet_dist_km):
      control_dist_km_dist_km = brevet_dist_km
   
   # Set the minimum brevet time shift 
   min_time_limit = update_time(control_dist_km_dist_km, 2)

   # Split up the minimum brevet time for race into hours and minutes (make sure your minutes are whole)
   mins = min_time_limit % 1    
   hr = min_time_limit - mins  
   mins = round(mins * 60) 

   # Updates the current brevet parameter to reflect time shift
   updated_brevet = update_brevet(brevet_start_time, hr, mins)
   return updated_brevet.isoformat()


def close_time(control_dist_km_dist_km, brevet_dist_km, brevet_start_time):
   """
   Args:
      control_dist_km_dist_km:  number, control_dist_km distance in kilometers
      brevet_dist_km: number, nominal distance of the brevet
      in kilometers, which must be one of 200, 300, 400, 600, or 1000
      (the only official ACP brevet distances)
      brevet_start_time:  An arrow object
   Returns:
      An arrow object indicating the control_dist_km close max_time_limit.
      This will be in the same max_time_limit zone as the brevet start max_time_limit.
   """
   # Brevet control_dist_km canot be more than 120% of brevet itseflf
   if invalid_control(control_dist_km_dist_km, brevet_dist_km):
      if control_dist_km_dist_km == 0:
         return brevet_start_time.shift(hours =+ 1)
      else:
         return None

   # Make sure that if control_dist_km is greater than brevet distance then the control_dist_km distance 
   # times for closing times are all the same 
   if (control_dist_km_dist_km >= brevet_dist_km):
	   mins = LIMIT_TIMES[brevet_dist_km][1]
	   hr = LIMIT_TIMES[brevet_dist_km][0]
	   return update_brevet(brevet_start_time, hr, mins)

   # Set the maximum brevet time for race
   max_time_limit = update_time(control_dist_km_dist_km, 1)

   # Split up the maximum brevet time for race into hours and minutes (make sure your minutes are whole)
   mins = max_time_limit % 1
   hr = max_time_limit - mins
   mins = round(mins * 60)

   updated_brevet = update_brevet(brevet_start_time, hr, mins)
   return updated_brevet.isoformat()


""" 
Helper Functions
"""

def invalid_control(control, brevet_time):
   '''
   Description:
      Shifts the brevet hours and minutes to alighn with hours and minutes. 
   Args:
      control: --> control_dist_km_dist_km:  number, control_dist_km distance in kilometers
      brevet_time: The starting time of the brevet
   Returns:
      bt: The properly shifted brevet_time
   '''
   # Control cannot be greater than the 1.2x the brevet distance and cannot be negative
   if ((control > (brevet_time * 1.2)) or (control <= 0)):
      return True
   else:
      return False

def update_brevet(brevet_time, hr, mins):
   '''
   Description:
      Shifts the brevet hours and minutes to alighn with hours and minutes. 
   Args:
      brevet_time: The starting time of the brevet
      hr: How many hours the brevet is being shifted by
      mins: How many minutes the brevet is being shifted by
   Returns:
      bt: The properly shifted brevet_time
   '''
   bt = arrow.get(brevet_time)
   bt = bt.shift(hours=hr)
   bt = bt.shift(minutes=mins)
   return bt


def update_time(control, limit_type_number): # Limit type can either be a one or a two indicating
   '''
   Description: 
      Finds the correct section working in and adds times of previous sections to total 
      time counter as progression happens.
   Args: 
      control: --> control_dist_km_dist_km:  number, control_dist_km distance in kilometers
      limit_type_number: 
         1: references close times  (slowest you could go)
         2: references open times   (fastest you could go)
   Returns:
      time: the time shift total that will be parsed and added to the brevet start time
   '''
   complete = False
   traveled = 0
   section = 0
   time = 0
   prev = 0

   while(not complete): # (for example 400 and 406 )
   # Determine if this is the correct section we will do final calculations with
      if (traveled + control) <= BREVET_TABLE[section][0]:
         time += control / BREVET_TABLE[section][limit_type_number] # The final time calculation
         complete = True

      # Update time to include current section
      else:
         prev = BREVET_TABLE[section][0] - traveled # Takes this section of the races distance usually 200 minus the time spent in the other sections
         time += prev/BREVET_TABLE[section][limit_type_number] # Adds the time it would take to complete said section under constraints
         section += 1   # Move up a section
         control -= prev   # Take away the distance from the control
         traveled += prev  # Add distance to traveled
   return time