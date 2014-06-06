% Script for background subtraction
%
% It takes the A matrix (generated from the 'results1.txt' file from the  
% ImageJ script "1_mm", performs background subtraction, calculates and 
% plots the deltaF/F, saves the ratio plot as a .jpg and a .fig, and saves the 
% max deltaF/F of each ROI as a .dat and a .txt file. It also calculates the
% mean max of each ROI by averaging the deltaf/f values of 3 frames
% around the max and saves that as a .dat and a .txt file. The average max
% values and their corresponding frames are shown on the figures.
%
% POSSIBLE PROBLEMS
% 1. The matrix A = results1.txt
% 2. When calculating the average max, this code assumes that the max
% occurs in the middle of the trace, not during the first or last frame. If
% the code quits, check this.
 
% Later I will put in assert functions or whatever to make the code
% terminate if certain conditions aren't true.

A = dlmread('results1.txt', '\t', 1, 1);
figure(1); subplot(2,2,1); plot(A,'LineWidth',1.5); title('Raw plots: roi order = b, g, r, c, m, y, k, b');
figure(1); subplot(2,2,4); image(imread('slice30label.jpg', 'jpeg'));

% Creates string from the filename of the first .avi file in the directory;
% deletes *.avi. 
files = dir('*.avi');
filename = strrep(files(1).name, '.avi', '');

% traces - array whose columns are the traces
% control - column vector of the control trace
% stim - scalar specifying the frame in which the stimulus occurs
%
% Choose which columns are control and which are stim.

n_control = input('Which column of A is the control? ');

control = A(:,n_control);
% Choose which columns are the stimulus traces and generates a matrix =
% [A(:,1) A(:,2) A(:,3)].
% In future analysis with a movie with an empty frame, the control will be
% the same for each movie from the same fly.

n_rois = input('Columns of the ROIs? ex. [1 2 3 4] ');

    for j = 1: length(n_rois)
        traces(:,j) = A(:,n_rois(j));
    end
    
stim = input('In what frame did the stimulation occur (usually 20)? ');

% number of rows
n_frames = size(traces, 1);
% number of columns
n_traces = size(traces, 2);


% make sure the control and stim vectors are the right size
%assert(size(control) == n_frames)
%assert(size(traces) == n_traces)

%Subtracts the mean of the prestimulus control trace from the stimulus
%traces and then divides the stimulus traces by the control trace.

ps_trace_means = mean(traces(1:stim, :));
ps_ctrl_mean = mean(control(1:stim));

ps_mean_diffs = ps_trace_means - ps_ctrl_mean;

offset_traces = traces - repmat(ps_mean_diffs, n_frames, 1);

ratio_traces = offset_traces./repmat(control, 1, n_traces);

ratio_traces_stim = ratio_traces(stim:end, :);

% Identifies the max deltaF/F and the frames in which the maxima occured 
% (only in the frames after 'stim'),
% and generates two vectors, maxima and maxima_indices, respectively. Note
% that maxima_indices refers to the indices of the array containing only
% the frames after 'stim'.
[maxima maxima_indices] = max(ratio_traces_stim);

% Generates a row vector where the column entries are the averaged maxima
% of the corresponding column entries in the ratio_traces matrix. The
% maxima are averaged by taking the mean of the three frames around the
% frame with the maximum deltaF. If the maxima occurs in the first or last
% frame, only two frames are averaged.

for m = 1:size(ratio_traces_stim,2)

    if maxima_indices(m) == 1, 
        n2 = ratio_traces_stim(maxima_indices(m), m);
        n3 = ratio_traces_stim((maxima_indices(m)+1), m);
        n = [n2; n3],
        avg_max_3frames(m) = mean(n);
       
    end
    
    if maxima_indices(m) == length(ratio_traces_stim),
        n1 = ratio_traces_stim((maxima_indices(m)-1), m);
        n2 = ratio_traces_stim(maxima_indices(m), m);
        n = [n1; n2],
        avg_max_3frames(m) = mean(n);
    end
    
    if maxima_indices(m) ~= 1 && maxima_indices(m) ~= length(ratio_traces_stim),
        n1 = ratio_traces_stim((maxima_indices(m)-1), m);
        n2 = ratio_traces_stim(maxima_indices(m), m);
        n3 = ratio_traces_stim((maxima_indices(m)+1), m);
        n = [n1; n2; n3];
        avg_max_3frames(m) = mean(n);
    end
    
end

% Displays coordinates of max. deltaF/F and the averaged max deltaF/F.
[(maxima_indices+stim); (avg_max_3frames)],

%Plots figures and labels the subtracted traces with the averaged maxima.
%Color order is: blue, green, red, cyan, magenta, yellow, black. 
%Maxima and maxima indices are shown as an array, where the column index
%matches the color order.

figure(1); subplot(2,2,2); plot(offset_traces,'LineWidth',1.5); title('Offset Traces'); hold on;
plot(control, '--', 'LineWidth',1.5); 

figure(3); 
% set(3,'Units','normalized')
plot(ratio_traces,'LineWidth',1.5); title('DeltaF/F (Ratio)');
text(0.5,1.2,[num2str([maxima_indices+stim; avg_max_3frames])]);
text(0.5,1.1,'top = frames, bottom = averaged max');

figure(1); subplot(2,2,3); 
plot(ratio_traces,'LineWidth',1.5); title('DeltaF/F ratio');
set(1,'Units','pixels','Position',[30 30 800 800]);

% Asks user if files should be saved.
s = input('Save? 1 = yes, 0 = no ');

if s == 1, 
    % Saves workspace.
    save(filename);

    % Saves maxima in a file named maxima.txt, maxima.dat and in a file named
    % after the stimulation. Also saves the stimulation frame.
    filenametxt = [filename '_maxima.txt'];
    filenamedat = [filename '_maxima.dat'];
    save(filenametxt,'maxima','-ASCII');
    save maxima.dat maxima /ascii;
    save maxima.txt maxima /ascii;
    save stim.dat stim /ascii;

    % Saves maxima in the folder specified below.
    x = fullfile('c:\Users\Andrea\Documents\Lab\analysis\maxima',filenamedat);
    save(x,'maxima','-ascii');

    % Saves averaged maxima in a file named avg_maxima.txt, avg_maxima.dat and in a file named
    % after the stimulation.
    filenametxtavg = [filename '_avg_max_3frames.txt'];
    filenamedatavg = [filename '_avg_max_3frames.dat'];
    save(filenametxtavg,'avg_max_3frames','-ASCII');
    save avg_max_3frames.dat avg_max_3frames /ascii;
    save avg_max_3frames.txt avg_max_3frames /ascii;

    % Saves averaged maxima in the folder specified below.
    z = fullfile('c:\Users\Andrea\Documents\Lab\analysis\avg_max_3frames',filenamedatavg);
    save(z,'avg_max_3frames','-ascii');

    % Saves Figure 1 
    saveas(1,[filename '_traces.fig']);
    saveas(1,[filename '_traces.jpg'],'jpg');

    % Saves Figure 3 (DeltaF/F ratio) with maxima/minima labeled.
    saveas(3,[filename '_ratio.fig']);

    %Saves .jpg of the labeled ratio plot to the indicated folder.
    y = fullfile('c:\Users\Andrea\Documents\Lab\analysis\summary',filename);
    saveas(3,[y '_ratio.jpg'],'jpg');

end


%The problem now is, how do I match the maxima to the right regions? I may
%have to just circle the same region with the same ROI each time. However,
%saving the maxima to their own files will probably still be useful.