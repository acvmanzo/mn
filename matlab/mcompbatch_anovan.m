function mcompbatch_anovan(pdir, alpha)
%MCOMPBATCH_ANOVAN(PDIR, ALPHA)
%   Batch version of mcomp. Performs 'multcompare' on the data using a two-way anova in the
%   directory PDIR at a significance level of ALPH. Loads files named
%   'peakfm.txt'.

dirfiles = dir('*.txt');

for l = 1:length(dirfiles)
    file = dirfiles(l).name
    mcomp_anovan(file, alpha)
    close all
end
end