import matplotlib.pyplot as plt
import numpy as np
import math
import os

script_dir = os.path.dirname(__file__)
outputs_dir = os.path.join(script_dir, 'outputs/')
if not os.path.isdir(outputs_dir):
    os.makedirs(outputs_dir)
	
file_names = ['i170b1h0_t0', 'i170b2h0_t0', 'i170b3h0_t0', 'i170b4h0_t0']
txt = ""
size = 500
min_scale = 0 
max_scale = 255 
min_value = 0
max_value = 0
totalNumberofValues = size * size
#This function is needed to save the images
def saveimage(data, title, file_name, type):
    plt.clf()
    txt = "Maria Carmela Dipinto"
    plt.subplots_adjust(bottom=0.2, left=0.2)
    plt.figtext(0.99, 0.01, txt, wrap=True,
                ha="right", va="bottom", fontsize=8)
    plt.title(title)
    if type == 'im':     #im is the black and white image 
        plt.imshow(data, 'gray')
    if type == 'imc':    #imc is the colored image 
        plt.imshow(data)
    if type == 'imb':       #imb is the image with colorbar
        plt.imshow(data)        
        plt.colorbar()
        plt.clim(0, 255);
    x = [10, 150, 290, 430]
    y = [90, 130, 210, 330, 450]
    plt.gca()
    plt.ylabel("Dec")
    plt.xlabel("RA")    

    xlabels = ['5h45m', '5h30m', '5h15m', '5h00m']
    ylabels = ['-6:00','5h45m','-9:00','-12:00','-15:00']
    plt.xticks(x, xlabels)
    plt.yticks(y, ylabels)
    plt.savefig(outputs_dir +file_name + ".png", dpi=300)

#This function is needed to save the histogram
def savehist(data, title, file_name):
    plt.clf()
    txt = "Maria Carmela Dipinto"
    plt.subplots_adjust(bottom=0.2, left=0.2)
    plt.figtext(0.99, 0.01, txt, wrap=True,
                ha="right", va="bottom", fontsize=8)
    plt.title(title)
    plt.xlabel('Values')
    plt.ylabel('Occurrences')        

    plt.xscale('log') #the x axis is a logaritmic scale

    plt.plot(np.log(list(data.keys())), list(data.values()))    
    plt.savefig(outputs_dir + file_name + ".png", dpi=300)
    
def saveplot(data, title, file_name):
    plt.clf()
    txt = "Maria Carmela Dipinto"
    plt.xlabel("pixels on x-axis")
    plt.ylabel("values")       
    plt.yscale('log') #the y axis is a logaritmic scale
    
    plt.subplots_adjust(bottom=0.2, left=0.2)
    plt.figtext(0.99, 0.01, txt, wrap=True,
                ha="right", va="bottom", fontsize=8)
    plt.title(title)
    plt.plot(data)
    plt.savefig(outputs_dir + file_name + ".png", dpi=300)

def nonlinear(value, min_value, max_value):
    log_min = math.log(min_value) if min_value > 0 else 0
    log_max = math.log(max_value) if max_value > 0 else 0
    if value > 0:
        log = math.log(value)
        if log > 0:
            return (log - log_min) / (log_max - log_min) * max_scale
    return 0

def calculateVariance(mean, arr):
    sd = 0
    for row in arr:
        for col in row:
            sd += (col - mean)**2
    variance = sd/totalNumberofValues
    return variance 
    
def read_file(file):
    totalvalue = 0
    histogram = {}
    with open(file) as fp:    
       line = fp.readline()
       pixels = np.zeros((size, size))
       x = size-1
       while line:
           ListSplit = line.split(",")
           i=0
           for y in range(0, size):
               pixels[x, y] = float(ListSplit[i].replace('"', ''))
               totalvalue += pixels[x, y]
               if pixels[x, y] in histogram:
                  histogram[pixels[x, y]] += 1
               else:
                  histogram[pixels[x, y]] = 1              
               i +=1
           x -=1
           line = fp.readline()
    mean = totalvalue/ totalNumberofValues
    return mean, pixels, histogram

# This function creates the equalized histogram
def cdf255(data, file_name):
        
    r, indices,counts  = np.unique(data, return_inverse=True, return_counts=True)
    pr = np.zeros(len(r))
    cdf = np.zeros(len(r))
    cdf255 = np.zeros(len(r))

    sum_pr = 0
    minHist = min(counts)
    for i, v in enumerate(counts):
        if counts[i] > 0:
            pr[i] = v/(size*size)
        else:
            pr[i] = 0

        sum_pr += pr[i]
        cdf[i] = sum_pr
        cdf255[i] = cdf[i] *  max_scale
    
    cdf255_all = cdf255[indices]
    cdf255_matrix = np.ndarray.reshape(cdf255_all, (size, size))
    saveimage(cdf255_matrix, "Histogram Equalization: " + file_name, file_name + "-he", "im")


    return cdf255_matrix
                
def getMinMax( M ):
    maxVal = 0
    rowmaxVal = []
    for row in M:
        if max(row) > maxVal: 
           maxVal = max(row)
           rowmaxVal = row
    minVal = maxVal
    for row in M:
        if min(row) < minVal: minVal = min(row)

    return ( minVal,  maxVal,rowmaxVal  )

def main() :
    cdf255_data = {}
    for file_name in file_names:
        file_path = "./orion/" + file_name + ".txt"
        mean, readdata, histdata = read_file(file_path)
        if (file_name == "i170b2h0_t0"):
##################################################################
# a. save in a text file min, max, mean variance of data set b2
###############################################################
           variance = calculateVariance(mean, readdata)
           min_value, max_value, row_max = getMinMax( readdata )   # function return min, max and row containing max value
           text = ""
           text += "file: " + file_name + "\n"
           text += "min: " + str(min_value) + "\n"
           text += "max: " + str(max_value) + "\n"
           text += "mean: " + str(mean) + "\n"
           text += "variance: " + str(variance) + "\n"
           
           with open(outputs_dir + file_name + ".txt", "w+") as out:
             out.write(text)
#################################################
# b. draw profile line of row containing max value 
#################################################

           saveplot(np.log(row_max), "Profile Line of row with max value (y-value log-scaled): " + file_name, file_name + "-pline")

#####################################
# c. display histogram of data set b2
######################################

           data = {}                          #store sorted dict data for histogram  
           for key in sorted(histdata.keys()) :
              data[key] = histdata[key]
           savehist(data, "Histogram  (x-value log-scaled): " + file_name, file_name + "-hist")

######################################################
# d. rescale values of data set b2 in range 0-255
#######################################################

          # nonlinear transformation
           nonlinear_data = np.zeros((size, size))
           
           for i in range(size):
               for j in range(size):
                  nonlinear_data[i][j] = nonlinear(readdata[i][j], min_value, max_value)

           saveimage(nonlinear_data, "Non Linear Transformation in range 0-255 : " + file_name, file_name + "-rescale", "imb")
        
#######################################################################################################
# e. Save Histogram equalization  of all data sets. The cdf255_data function has been created before. 
###################################################################################################àà

        cdf255_data[file_name] = cdf255(readdata, file_name)   
        
        
############################################
# f. combine  bands 4,3, 1 in RGB color  
############################################
    
    combine_data = np.zeros((size, size, 3), dtype=np.uint8)
    for x in range(size):
        for y in range(size):
            r = int(round(cdf255_data['i170b4h0_t0'][x][y]))
            g = int(round(cdf255_data['i170b3h0_t0'][x][y]))
            b = int(round(cdf255_data['i170b1h0_t0'][x][y]))
            color = [r, g, b]
            combine_data[x][y] = color

    saveimage(combine_data, "Histogram Equalization: Combine bands in RGB" , "combine-RGB", "imc")

if __name__ == "__main__":
    main()
