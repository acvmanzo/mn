function ci_binomial(fname, alpha)
%CI_BINOMIAL(FNAME, ALPHA)
%   Calculates the Clopper-Pearson binomial confidence interval at
%   significance level ALPHA from data in file FNAME. Format of fname
%   should be 'condition \t number of successes \t total'.

x = importdata(fname, '\t');
data = x.data;
rowheaders = x.rowheaders;

f0name = regexprep(fname, '.txt', '');
ffname = strcat(f0name, '_alpha', num2str(alpha));

outfile = sprintf(ffname)

fid = fopen(outfile, 'w');
fprintf(fid, 'Condition,proportion,CI(lower),CI(upper),Successes,Total\n');
fclose(fid);

for i = 1:length(rowheaders)
    
    condition = char(rowheaders(i))
    r = data(i,:)
    pump = r(1)
    sum = r(2)
    
    [phat, pci] = binofit(pump, sum, alpha)
    fid = fopen(outfile, 'a');
    fprintf(fid, '%s,%0.2f,%0.2f,%0.2f,%0.2f,%0.2f\n', condition, phat, pci(1), pci(2),pump,sum);
    clear phat pci;
    fclose(fid)

end
end