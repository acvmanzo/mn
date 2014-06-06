function mcomp_anovan(fname, alpha)
%MCOMP_ANOVAN(FNAME, ALPHA)
%   Imports data from file 'fname', performs a two-way anova and executes 'multcompare' using a
%   significance level of 'alpha'.
%   Data in 'fname' must be in the format where the first column contains
%   data labels and the second column contains numeric values.

% Imports the file.
x = importdata(fname, '\t')
data = x.data
textdata = x.textdata

% Specifies the vectors for anovan.
sized = size(data)

y = data(:,2)
g1 = data(:,1)
g2 = textdata

f0name = regexprep(fname, '.txt', '');
ffname = strcat(f0name, '_', num2str(alpha));

mkdir(ffname)
cd(ffname)

% Performs an n-way anova to produce the stats table for use in
% 'multcompare'.
[p,table,stats, terms] = anovan(y, {g1, g2}, 'model','full','varnames',{'Temp','Genotype'});
saveas(1, strcat(ffname, '_anovan.png'))
close(1)

% Performs 'multcompare' and saves the resulting matrices and figures as
% noted.
[c, m, h, gnames] = multcompare(stats, 'alpha', alpha, 'dimension',[1 2]);

fid = fopen(strcat(ffname, '_gnames.txt'), 'w');

for i = 1:length(gnames)
    x = char(gnames(i));
    fprintf(fid, '%s\n', x);
end

fclose(fid);

saveas(1, strcat(ffname,'_mcfig.fig'));
saveas(1, strcat(ffname,'_mcfig.png'));
save(strcat(ffname, '_mc_c_table.txt'), 'c', '-ascii');
save(strcat(ffname,'_mean_stderr.txt'), 'm', '-ascii');
save(strcat(ffname,'_alpha.txt'), 'alpha', '-ascii');
close(1)

cd('../')
end