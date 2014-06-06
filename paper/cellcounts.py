
import glob
import mn.plot.genplotlib as gpl
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats


# Counts are from file ~/Documents/lab/motor_neurons/expression/cellcounts_doublegal4.gnumeric
# Updated data 9/15/2011.

counts = glob.glob('counts/*')
left = {}
right = {}
sum = {}

# Loads data from text files of cell counts.
for count in counts:
    with open(count) as f:
        
        m = f.next()
        cond = m.split(',')[0]
        left[cond] = []
        right[cond] = []
        sum[cond] = []
        
        f.next()
        for l in f:
            k, r, s = map(str.strip, l.split(','))
            k, r, s = map(float, [k, r, s])
            left[cond].append(k)
            right[cond].append(r)
            sum[cond].append(s)

# Generates dictionaries listing the mean values, etc. for these counts.
mleft = gpl.genlist(left)
mright = gpl.genlist(right)
msum = gpl.genlist(sum)


k = ['112648', '112204', '423', '112648 + 112204', '112648 + 423', '112204 + 423']

# Writes the mean values, etc. for the sum of the count data into summary files.
with open('2011-0915_cellcounts_sum.txt', 'w') as g:
    g.write('Condition\t[Mean, StdDev, StdErr, n, label]\n')
    for j in k:
        g.write('{0} \t {1} \n'.format(j, msum[j]))

with open('2011-0915_cellcounts_left.txt', 'w') as g:
    g.write('Condition\t[Mean, StdDev, StdErr, n, label]\n')
    for j in k:
        g.write('{0} \t {1} \n'.format(j, mleft[j]))

with open('2011-0915_cellcounts_right.txt', 'w') as g:
    g.write('Condition\t[Mean, StdDev, StdErr, n, label]\n')
    for j in k:
        g.write('{0} \t {1} \n'.format(j, mright[j]))

# Compares genotypes to see if the differences in summed cell count are statistically significant.
x = stats.ttest_ind(sum['112648'], sum['112648 + 423'])
y = stats.ttest_ind(sum['112648'], sum['112648 + 112204'])
z = stats.ttest_ind(sum['112204'], sum['112204 + 423'])
w = stats.ttest_ind(sum['423'], sum['112204 + 423'])

# Writes these t-test results into a file.
with open('2011-0915_ttest_results.txt', 'w') as f:
    f.write('Comparison\tT-statistic\tP-value\n')
    f.write('112648 vs. 112648 + 423 \t {0} \t {1} \n'.format(x[0], x[1]))
    f.write('112648 vs. 112648 + 112204 \t {0} \t {1}\n'.format(y[0], y[1]))
    f.write('112204 vs. 423 + 112204 \t {0} \t {1}\n'.format(z[0], z[1]))
    f.write('423 vs. 423 + 112204 \t {0} \t {1}\n'.format(w[0], w[1]))

#Compares genotypes to see if the differences in cell counts from the left side of the brain are statistically significant.
x = stats.ttest_ind(left['112648'], left['112648 + 423'])
y = stats.ttest_ind(left['112648'], left['112648 + 112204'])
z = stats.ttest_ind(left['112204'], left['112204 + 423'])
w = stats.ttest_ind(left['423'], left['112204 + 423'])    

with open('2011-0915_ttest_results_left.txt', 'w') as f:
    f.write('Comparison\tT-statistic\tP-value\n')
    f.write('112648 vs. 112648 + 423 \t {0} \t {1} \n'.format(x[0], x[1]))
    f.write('112648 vs. 112648 + 112204 \t {0} \t {1}\n'.format(y[0], y[1]))
    f.write('112204 vs. 423 + 112204 \t {0} \t {1}\n'.format(z[0], z[1]))
    f.write('423 vs. 423 + 112204 \t {0} \t {1}\n'.format(w[0], w[1]))

#Compares genotypes to see if the differences in cell counts from the right side of the brain are statistically significant.
x = stats.ttest_ind(right['112648'], right['112648 + 423'])
y = stats.ttest_ind(right['112648'], right['112648 + 112204'])
z = stats.ttest_ind(right['112204'], right['112204 + 423'])
w = stats.ttest_ind(right['423'], right['112204 + 423'])

with open('2011-0915_ttest_results_right.txt', 'w') as f:
    f.write('Comparison\tT-statistic\tP-value\n')
    f.write('112648 vs. 112648 + 423 \t {0} \t {1} \n'.format(x[0], x[1]))
    f.write('112648 vs. 112648 + 112204 \t {0} \t {1}\n'.format(y[0], y[1]))
    f.write('112204 vs. 423 + 112204 \t {0} \t {1}\n'.format(z[0], z[1]))
    f.write('423 vs. 423 + 112204 \t {0} \t {1}\n'.format(w[0], w[1]))

# Compares genotypes to see if the differences in cell counts between the left and right side of the brain of the same genotypes are statstically different.
x = stats.ttest_ind(left['112648'], right['112648'])
y = stats.ttest_ind(left['112204'], right['112204'])
z = stats.ttest_ind(left['423'], right['423'])

with open('2011-0915_ttest_left_right.txt', 'w') as f:
    f.write('Comparison\tT-statistic\tP-value\n')
    f.write('left vs. right 112648  \t {0} \t {1} \n'.format(x[0], x[1]))
    f.write('left vs. right 112204 \t {0} \t {1}\n'.format(y[0], y[1]))
    f.write('left vs. right 423 \t {0} \t {1}\n'.format(z[0], z[1]))


#fig1 = gpl.plotdata(sum, msum, k, 'b', 'Number of cells', 'Cell Counts', ylim = 8, xd=4, xlabelsize=12)
#fig1.subplots_adjust(bottom=0.2)
#plt.savefig('2011-0915_cellcounts.png')

# Generates a dictionary where I pool the counts from the left and right side of the brains.
pooled = left

for j in k:
    pooled[j].extend(right[j])

mpooled = gpl.genlist(pooled)

# Writes a file with the means of these pooled counts.
with open('2011-0915_cellcounts_pooled_leftright.txt', 'w') as g:
    g.write('Condition\t[Mean, StdDev, StdErr, n, label]\n')
    for j in k:
        g.write('{0} \t {1} \n'.format(j, mpooled[j]))

#Compares genotypes to see if the differences in pooled cell counts are statistically significant.
x = stats.ttest_ind(pooled['112648'], pooled['112648 + 423'])
y = stats.ttest_ind(pooled['112648'], pooled['112648 + 112204'])
z = stats.ttest_ind(pooled['112204'], pooled['112204 + 423'])
w = stats.ttest_ind(pooled['423'], pooled['112204 + 423'])
v = stats.ttest_ind(pooled['112204'], pooled['112648 + 112204'])
u = stats.ttest_ind(pooled['112648'], pooled['112204 + 423'])





with open('2011-0915_ttest_results_pooled_leftright.txt', 'w') as f:
    f.write('Comparison\tT-statistic\tP-value\n')
    f.write('112648 vs. 112648 + 423 \t {0} \t {1} \n'.format(x[0], x[1]))
    f.write('112648 vs. 112648 + 112204 \t {0} \t {1}\n'.format(y[0], y[1]))
    f.write('112204 vs. 112648 + 112204 \t {0} \t {1}\n'.format(v[0], v[1]))
    f.write('112204 vs. 423 + 112204 \t {0} \t {1}\n'.format(z[0], z[1]))
    f.write('423 vs. 423 + 112204 \t {0} \t {1}\n'.format(w[0], w[1]))
    f.write('112648 vs. 423 + 112204 \t {0} \t {1}\n'.format(u[0], u[1]))
    
    
