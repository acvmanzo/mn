
%Script for normalization of fluorescence traces obtained in imaging experiments. 
%
% It takes the A matrix (generated from the 'results1.txt' file from the  
% ImageJ script "1_mm"),
         
imaging_params;

% Loads results file and plots raw fluorescence traces and movie .jpg.
A = dlmread('results1.txt', '\t', 1, 1);

figure(1); 
subplot(2,2,1); plot(A,'LineWidth',1.5); 
title('Raw plots'); 
set(gca,'FontSize',7);
set(1,'Units','pixels','Position',[0 0 1000 1000]);
A_leg=[1:1:size(A,2)]'; legend(num2str(A_leg), 'Orientation', 'horizontal', 'Location', 'SouthOutside'); 

figure(1); subplot(2,2,4); image(imread('slice30label.jpg', 'jpeg'));

figure(2); image(imread('slice30label.jpg', 'jpeg'));


% Creates string from the filename of the first .avi file in the directory;
% deletes *.avi. 
files = dir('*.avi');
filename = strrep(files(1).name, '.avi', '');
disp(filename);


% Creates a string ('control_dir') that is identical to the name of the
% directory containing the no stimulus traces. Changes current directory to that directory.
% Creates a matrix "C" that contains the control traces. Returns to the
% previous directory with the stimulus traces.

[matchstr splitstr] = regexp(filename, '\_', 'match', 'split');
control_name = [splitstr; [matchstr {''}]];
nostim = 'nostim';
control_dir = [control_name{1:8} nostim];

cd('C:\Users\Andrea\Documents\Lab\515\515_imaging\nostims');
cd(control_dir);

C = dlmread('results1.txt', '\t', 1, 1);

cd('C:\Users\Andrea\Documents\Lab\515\515_imaging\data');
cd(filename);

% Creates the matrix 'control' containing the data from the control
% ROI.
clear control;
for j = 1: length(control_is)
    control(:, j) = C(:, control_is(j));
end


% Creates the matrix 'traces' containing the stimulus traces.
clear traces;
for j = 1: length(roi_is)
    traces(:,j) = A(:,roi_is(j));
end

% number of rows
n_frames = size(traces, 1);
% number of columns
n_traces = size(traces, 2);

% make sure the control and stim vectors are the right size
%assert(size(control) == n_frames)
%assert(size(traces) == n_traces)

%Divides the mean of the prestimulus control trace from the stimulus
%traces and then divides the stimulus traces by the control trace.

ps_trace_means = mean(traces(1:stim_frame, :));
ps_ctrl_mean = mean(control(1:stim_frame, :));

ps_mean_ratios = ps_trace_means./ps_ctrl_mean;

scaled_traces = traces./repmat(ps_mean_ratios, n_frames, 1);

ratio_traces = scaled_traces./control(1:length(scaled_traces), :);

% Generates a matrix containing the normalized traces after the 'stim_frame'
% frame. This matrix is used to calculate the maxima. The frames can be
% specified by changing the parameters below.
ratio_traces_stim = ratio_traces(stim_frame:end, :);

% Identifies the max deltaF/F and the frames in which the maxima occured 
% (only in the frames between 'stim_frame' and 'end-19'),
% and generates two vectors, maxima and maxima_indices, respectively. Note
% that maxima_indices refers to the indices of the array containing only
% the frames after 'stim_frame_frame'.
[maxima maxima_indices] = max(ratio_traces_stim(1:end-19, :));

% Generates a row vector where the column entries are the averaged maxima
% of the corresponding column entries in the ratio_traces matrix. The
% maxima are averaged by taking the mean of the three frames around the
% frame with the maximum deltaF. If the maxima occurs in the first or last
% frame, only two frames are averaged.
clear avg_max_3frames;

for m = 1:size(ratio_traces_stim,2)

    if maxima_indices(m) == 1, 
        n2 = ratio_traces_stim(maxima_indices(m), m);
        n3 = ratio_traces_stim((maxima_indices(m)+1), m);
        n = [n2; n3];
        avg_max_3frames(m) = mean(n);

    end

    if maxima_indices(m) == length(ratio_traces_stim),
        n1 = ratio_traces_stim((maxima_indices(m)-1), m);
        n2 = ratio_traces_stim(maxima_indices(m), m);
        n = [n1; n2];
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

%Plots figures and labels the subtracted traces with the averaged maxima.
%Color order is: blue, green, red, cyan, magenta, yellow, black. 
%Maxima and maxima indices are shown as an array, where the column index
%matches the color order.

figure(1); set(1,'Visible', 'off'); 
subplot(2,2,2); plot(scaled_traces,'LineWidth',1.5); 
title('Scaled Traces'); hold on;
plot(control, '--', 'LineWidth',1.5); 
set(gca,'FontSize',7)
legend(num2str([roi_is linspace(1, size(control, 2), size(control,2))]'), 'Orientation', 'horizontal', 'Location', 'SouthOutside')

figure(3); 
plot(ratio_traces,'LineWidth',1.5); 
title('DeltaF/F (Ratio)');
axis([0 100 0.7 1.75]);
set(gca, 'FontSize',7);
f_text = num2str([roi_is; maxima_indices+stim_frame; avg_max_3frames]);
text(5, 1.7, f_text, 'FontSize', 8);
legend(num2str((roi_is)'));


figure(1); subplot(2,2,3); 
plot(ratio_traces,'LineWidth',1.5); title('DeltaF/F ratio');
axis([0 100 0.7 1.75]);


% Asks user if files should be saved.
s = input('Save? 1 = yes, 0 = no ');

if s == 1, 

    % Saves files
    w = fullfile('C:\Users\Andrea\Documents\Lab\515\515_imaging\results',filename);
    mkdir(w);
    cd(w);

    % Saves workspace.
    save(filename);

    % Saves maxima in a file named maxima.txt, maxima.dat and in a file named
    % after the stimulation. Also saves the stimulation frame.
    filenametxt = [filename '_maxima.txt'];
    filenamedat = [filename '_maxima.dat'];
    save(filenametxt,'maxima','-ASCII');
    save maxima.dat maxima /ascii;
    save maxima.txt maxima /ascii;


    % Saves maxima in the folder specified below.
    x = fullfile('C:\Users\Andrea\Documents\Lab\515\515_imaging\results\summary\maxima',filenamedat);
    save(x,'maxima','-ascii');

    % Saves averaged maxima in a file named avg_maxima.txt, avg_maxima.dat and in a file named
    % after the stimulation.
    filenametxtavg = [filename '_avg_max_3frames.txt'];
    filenamedatavg = [filename '_avg_max_3frames.dat'];
    save(filenametxtavg,'avg_max_3frames','-ASCII');
    save avg_max_3frames.dat avg_max_3frames /ascii;
    save avg_max_3frames.txt avg_max_3frames /ascii;

    % Saves averaged maxima in the folder specified below.
    z = fullfile('C:\Users\Andrea\Documents\Lab\515\515_imaging\results\summary\avg_max_3frames',filenamedatavg);
    save(z,'avg_max_3frames','-ascii');

    % Saves Figure 1 
    set(1,'Units','pixels','Position',[100 -500 1200 1200]);
    saveas(1,[filename '_traces.fig']);
    saveas(1,[filename '_traces.jpg'],'jpg');

    % Saves Figure 3 (DeltaF/F ratio) with maxima/minima labeled.
    saveas(3,[filename '_ratio.fig']);

    %Saves .jpg of the labeled ratio plot to the indicated folder.
    y = fullfile('C:\Users\Andrea\Documents\Lab\515\515_imaging\results\summary\ratioplots',filename);
    saveas(3,[y '_ratio.jpg'],'jpg');

    %Saves .jpg of the traces plot to the indicated folder.
    y = fullfile('C:\Users\Andrea\Documents\Lab\515\515_imaging\results\summary\traces',filename);
    saveas(1,[y '_traces.jpg'],'jpg');
    
end

% Asks user if figures should be closed.
t = input('Close figures? 1 = yes, 0 = no ');

if t == 1, 
    close all;
end

% Asks user if figures should be closed.
u = input('Clear worksheet? 1 = yes, 0 = no ');

if u == 1, 
    clear;
end

    



  
