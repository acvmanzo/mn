function mcompbatch(pdir)
%MCOMPBATCH(PDIR, ALPHA)
%   Batch version of mcomp. Performs 'multcompare' on the data in the
%   directory PDIR at a significance level of ALPH. Loads files named
%   'peakfm.txt'.


dirfiles = dir('*mc.txt');

for l = 1:length(dirfiles)
    file = dirfiles(l).name
    alphas = [0.05, 0.01, 0.001]
    for i = 1:3
        mcomp(file, alphas(i))
    close all
end
end