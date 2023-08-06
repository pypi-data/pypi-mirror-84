import pandas as pd
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import statistics


def extract(textlines):
    # normalizing the line gaps to get an average gap for detetcting the paraagarphs
    line_gap_list = [line.space_above for line in textlines if line.space_above != -1]
    if len(line_gap_list)<len(textlines):
        line_gap_list.insert(0,max(line_gap_list) if len(line_gap_list) else 0)
    #	curr_line=[line.Text for line in textlines]

    if len(line_gap_list) <= 3:
        return [textlines]

    # Now we need the 2nd order derivative so that we can  get the
    # global maxima to get the paragraphs
    # 2nd order derivative is defined as :
    # f(x+1,y) + f(x-1,y) -2*f(x,y) ----> in the x direction
    # f(x,y+1) + f(x,y-1) -2*f(x,y) ----> in the y direction
    # we only need the derivative in the y direction here

    derivative_line_gap = line_gap_list
    for i in range(0, len(line_gap_list) - 1):
        derivative_line_gap[i] = line_gap_list[i] + line_gap_list[i + 1] - 2 * line_gap_list[i]

    # removing outliers
    outlier_cut_off = statistics.stdev(derivative_line_gap)
    derivative_line_gap2 = [d for d in derivative_line_gap if abs(d) < outlier_cut_off]
    cut_off = statistics.stdev(derivative_line_gap2)

    #	cut_off=statistics.stdev(derivative_line_gap)

    derivative_line_gap = list(map(lambda x: 0 if abs(x) < cut_off else x, derivative_line_gap))

    zero_crossings = np.where(np.diff(np.sign(derivative_line_gap)) == -2)[0]+1
    zero_crossings = zero_crossings.tolist()

    # checkjing how many are there with a line gap of less than 1
    # forming the paragraph:
    if len(zero_crossings) == 0:
        return [textlines]

    # split array in ranges
    for i in range(len(zero_crossings)):
        if zero_crossings[i] == i:
            zero_crossings[i] = i + 1
    zero_crossings.insert(0, 0)
    zero_crossings.insert(len(zero_crossings), len(textlines))

    paragraph_ranges = [(zero_crossings[i], zero_crossings[i + 1]) for i in range(len(zero_crossings) - 1)]
    paragraphs= [textlines[i:j] for i, j in paragraph_ranges]

    return paragraphs
# paragraph = []
# sub_elements = [textlines[0]]
# j=0
# for i in range(0,len(textlines)-1):
# 	if j < len(zero_crossings):
# 		if i <= zero_crossings[j]:
# 			sub_elements.append(textlines[i+1])
# 		else:
# 			paragraph.append(sub_elements)
# 			sub_elements=[textlines[i+1]]
# 			j+=1
# 	else:
# 		sub_elements.append(textlines[i+1])
# paragraph.append(sub_elements)
#
# return paragraph
