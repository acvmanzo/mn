function ci_binomial_batch(pdir, alpha)
%CI_BINOMIAL_BATCH(PDIR, ALPHA)
%   Batch version of mcomp. Performs 'ci_binomial' on the data in the
%   directory PDIR at a significance level of ALPH. 

dirfiles = dir('*.txt');

for l = 1:length(dirfiles)
    file = dirfiles(l).name
    ci_binomial(file, alpha)
    close all
end
end