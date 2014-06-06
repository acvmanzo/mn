import scipy.stats as stats
import mn.plot.genplotlib as gpl
import mn.gof.gfplot as gfp


x, y = gfp.gendictgf('2010-0709_dtrpa1_pc_pooled.txt')
print(x)
print(x['721 x dTRPA1'])

tstat, prob = stats.ttest_ind(x['721-GAL4'], x['721 x dTRPA1'])
print(prob)
probstr1 = str(prob)

tstat, prob = stats.ttest_ind(x['UAS-dTRPA1'], x['721 x dTRPA1'])
print(prob)
probstr2 = str(prob)

tstat, prob = stats.ttest_ind(x['721 x dTRPA1 (25)'], x['721 x dTRPA1'])
print(prob)
probstr3 = str(prob)


with open('ttest_results.txt', 'w') as f:
    f.write('prob 721-gal4 vs 721 x dtrpa1\t' + probstr1 + '\n')
    f.write('prob uas-dtrpa1 vs 721 x dtrpa1\t' + probstr2 + '\n')
    f.write('prob 721 x dtrpa1 (25) vs 721 x dtrpa1\t' + probstr3 + '\n')
