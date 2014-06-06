% Use after vsub to save files.

% Saves workspace.
save(filename);

% Saves maxima in a file named maxima.txt, maxima.dat and in a file named
% after the stimulation.
filenametxt = [filename '_maxima.txt'];
filenamedat = [filename '_maxima.dat'];
save(filenametxt,'maxima','-ASCII');
save maxima.dat maxima /ascii;
save maxima.txt maxima /ascii;

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

% Saves Figure 2 (Offset Traces).
saveas(2,[filename '_offset.fig']);
saveas(2,[filename '_offset.jpg'],'jpg');

% Saves Figure 3 (DeltaF/F ratio) with maxima/minima labeled.
saveas(3,[filename '_ratio.fig']);

% Saves Figure 4 (DeltaF/F ratio) with no maxima/minima labeled.
saveas(4,[filename '_ratio_notext.fig']);
saveas(4,[filename '_ratio_notext.jpg'],'jpg');

%Saves .jpg of the labeled ratio plot in the indicated folder.
y = fullfile('c:\Users\Andrea\Documents\Lab\analysis\summary',filename);
saveas(3,[y '_ratio.jpg'],'jpg');


