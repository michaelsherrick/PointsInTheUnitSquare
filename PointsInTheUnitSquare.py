#!/usr/bin/env python
# coding: utf-8

# In[2]:


import numpy as np
import matplotlib.pyplot as plt


# In[3]:


get_ipython().run_line_magic('matplotlib', 'qt')


# In[4]:


MAX_ATTEMPTS = 500


# In[9]:


def get_circ_rad(square_size, point_count, acc):
    # Generate numpy array of random coordinate pairs with a range of 0 -> square_size
    random_points = np.random.rand(point_count, 2) * square_size
    center = square_size / 2       # Center coordinate is half of square size (x and y are equal)
    circ_rad = square_size / 4     # Circle radius begins at 1 quarter of the square size
    
    # High limit for radius begins at half square size, bottom begins at 0
    top_rad, bot_rad = square_size / 2, 0
    
    # Begin at 0 attempts and not done
    attempt, done = 0, False
    
    # Loop until done or we've reached max attempts
    while(not done and attempt < MAX_ATTEMPTS):
        # Lists of inside distances to center and outside distances to square
        inside_dist, inside = [], []
        outside_dist, outside = [], []
        # Loop through all generated random points
        for point in random_points:
            
            # Calculate the distance to the center to check if point is in circle
            to_center = ((point[0] - center)**2 + (point[1] - center)**2)**0.5
            if(to_center < circ_rad):
                # In circle, save distance to center
                inside.append([point[0], point[1]])
                inside_dist.append(to_center)
            else:
                # Not in circle, save distance to square edge
                outside.append([point[0], point[1]])
                outside_dist.append(min(square_size - point[0], point[0], square_size - point[1], point[1]))
        
        # Calculate averages
        avg_in = np.average(inside_dist)
        avg_out = np.average(outside_dist)
        
        # Stop if difference between averages is less than accuracy threshold
        # or if difference between top and bottom limits is less than half accuracy threshold
        if(abs(avg_in - avg_out) < acc or abs(top_rad - bot_rad) < acc / 2):
            done = True
        elif(avg_in > avg_out):
            # Too big, set top limit and move radius halfway toward bottom limit
            top_rad = circ_rad
            circ_rad -= abs(circ_rad - bot_rad) / 2
        else:
            # Too small, set bottom limit and move radius halfway toward top limit
            bot_rad = circ_rad
            circ_rad += abs(top_rad - circ_rad) / 2
        attempt += 1    # Increment number of attempts
        print("\rAttempt: {} | Radius: {:2.8f} | Difference: {:2.8f} | Top: {:2.8f} | Bottom: {:2.8f}"
              .format(attempt, circ_rad, abs(avg_in - avg_out), top_rad, bot_rad), end='', flush=True)
    
    plt.figure(figsize=(6, 6))
    inside, outside = np.array(inside), np.array(outside)
    plt.scatter(inside[:, 0], inside[:, 1], s=1, color='blue')
    plt.scatter(outside[:, 0], outside[:, 1], s=1, color='orange')
    ax = plt.gca()
    ax.add_artist(plt.Circle((center, center), circ_rad, fill=False))
    plt.xlim([0, square_size])
    plt.ylim([0, square_size])
    
    return circ_rad


# In[12]:


get_circ_rad(1, 10000, 0.001)


# In[ ]:




