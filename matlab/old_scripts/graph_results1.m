% This macro is for use with the ImageJ script '1_mm.txt'. It plots the
% columns of the results1.txt output file (showing the fluorescence vs.
% frame number), and then saves the resulting graph to the current
% directory. Color order is: blue, green, red, cyan, magenta, yellow,
% black. 

A = dlmread('results1.txt', '\t', 1, 1);
figure(1); plot(A,'LineWidth',1.5); title('Raw plots: roi order = b, g, r, c, m, y, k, b');

% Creates string from the filename of the first .avi file in the directory;
% deletes *.avi. Saves figure 1.
files = dir('*.avi');
filename = strrep(files(1).name, '.avi', '');

saveas(1,[filename '_raw.fig']);
saveas(1,[filename '_raw.jpg'],'jpg');