import scipy.stats as stats
import mn.plot.genplotlib as gpl


x = gpl.gendict('peakf_roi1.txt')
print(x)

tstat, prob = stats.ttest_ind(x['762-GAL4'], x['762 x TNT'])
print(prob)
probstr = str(prob)

with open('ttest_results.txt', 'w') as f:
    f.write('prob\t' + probstr)
