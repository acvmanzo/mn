% This script takes the maxima from individual imaging files and puts them
% into a single matrix, and then saves that matrix to a .dat file. Takes
% the average of all the entries in the matrix as 'avg.dat'. Saves the
% workspace as 'sum_maxima_workspace.dat'.
%
% The assumptions/caveats are:
% a- The current directory must contain all the maxima files in .dat
% format, and must only contain files from the same experimental
% conditions.
% b- There must be fewer than 10 rois/file (pretty probable).
% c- Obviously, each column should correspond to the same neuron.
% d- Clear all variables before proceeding.
% e- Delete the old sum_maxima file before proceeding, or the matrix will
% be repeated.


clear s;
clear A;

files = dir('*.dat');
A = zeros(1,10);

for i=1:length(files)

    r = load(files(i).name);
    B = zeros(1,size(A,2)-length(r));
    s = [r B];
    A = [A; s];

end

response_table = A(2:end,:)
save('response_table.dat','response_table','-ascii');

% Finds the nonzero entries in A and returns the row and col indices (as
% the vectors 'row' and 'col'), and the nonzero entries (as the vector 'v').
[row,col,v] = find(A);

points = v;


avg = mean(v),
save('points.dat', 'points', '-ascii');
save('avg.dat','avg','-ascii');
save('sum_maxima_workspace.dat');