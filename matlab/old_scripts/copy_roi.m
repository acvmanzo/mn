%Copy roi.zip file from data folder to the movies folder.

cd('C:\Users\Andrea\Documents\Lab\dtrpa1_freq\data');
dirfiles = dir;

for l = 3:length(dirfiles)
    cd('C:\Users\Andrea\Documents\Lab\dtrpa1_freq\data');
    cd(dirfiles(l).name);
    if exist('roi1.zip') == 0, continue; end
    
     
    roiname = sprintf('%s%s', dirfiles(l).name, '_roi1.zip');
    v = fullfile('C:\Users\Andrea\Documents\Lab\Motor neurons\GOF\dtrpa1-videos\2010-0326_dtrpa1_gof_VIDEO_DATA\2010-0326_wb_dtrpa1', roiname);
   
    copyfile('roi1.zip', v);
    
end
    
    