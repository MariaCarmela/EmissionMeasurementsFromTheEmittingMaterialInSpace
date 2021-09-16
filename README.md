# Emission measurements from the emitting material in space
2D Spatial Data, Histogram Equalization, Color Transformation for emission measurements from the emitting material in space.

# Dataset
In the zip folder orion.zip you can find the description of the data(DataCharacterstics.txt,AllBands.png) and the dataset itself. The dataset is made of 4 .txt file:

• i170b1h0_t0.txt  for band 1
• i170b2h0_t0.txt for band 2
• i170b3h0_t0.txt for band 3
• i170b4h0_t0.txt fo band 4

# Installation
Please install needed packages like this:

pip install numpy
pip install matplotlib

# How to run the code
You can run project in this way:

python orion.py


# The tasks
(a) Calculate the max value, the min value, the mean value and the variance value of this 2D data set.

(b) Draw a profile line through the line with the maximum value of this 2D data set; you will need
coordinate axes to read off values.

(c) Display a histogram of this 2D data set (instead of bars you may use a line graph to link occurrences
along the x axis)

(d) Rescale values to range between 0 and 255 using your own transformation and display on your screen.
Add a legend showing the new maximum and minimum value.

(e) Carry out a Histogram equalization on each of the four bands and display on your screen (Note:
AllBands.png shows a Histogram Equalization).

(f) Combine the histo-equalized data set to an RGB-image (b4=r, b3=g, b1=b).

# The output
The allegate files are the outputs for each task.

task a)

i170b2h0_t0.txt

task b)

i170b2h0_t0-pline.png

task c)

i170b2h0_t0-hist.png

task d)

i170b2h0_t0-rescale.png

task e)

i170b1h0_t0-he.png

i170b2h0_t0-he.png

i170b3h0_t0-he.png

i170b4h0_t0-he.png

task f)

combine-RGB.png


