%Use this script to choose the frames over which to calculate the fourier
%transform.

%Plots the intensity vs. time and the spectrogram for the selected ROI.

load fps.dat;
v = dlmread('results1.txt', '\t', 1, 1); 
figure('Position', [78    41   903   928]);  subplot(2, 1, 1);
plot(v);
title('Raw trace'); 

subplot(2, 1, 2); x = 60; spectrogram(v, x, floor(0.95*x), 4*length(v), fps);

[str, remain] = strtok(pwd, '\');

while true
   [str, remain] = strtok(remain, '\');
   if isempty(str),  break;  end
   disp(sprintf('%s', str))
   name = str;,
end

%Saves this graph in a folder in the path specified in 'w', in a folder
%with the same name as the current folder.
w = fullfile('C:\Users\Andrea\Documents\Lab\dtrpa1_freq\results_long_dft', name);
if exist(w, 'dir') ~=7, mkdir(w), end

filenamefig = [w '\' name '_raw+spect.fig'];
filenamejpg = [w '\' name '_raw+spect.jpg'];

saveas(gcf, filenamejpg,'jpg');


%Use the plots and the .avi file to determine what frames to perform the
%fourier transform on, and save these frame numbers in the variable 'p'.
%'P' can be an n x 2 matrix where each row corresponds to one frame interval of
%the video. For instance, the matrix [0 10; 10 20] corresponds to the
%selection of two intervals to fourier transform, one from frame 0 to 10,
%and one from frame 10 to 20.
%
%After p has been defined, run the following command:
%save params p; close