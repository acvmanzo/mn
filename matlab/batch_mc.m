%Must load dipimage first! run('C:\Program Files\DIPimage\dipstart.m') Can
%just type 'dipstart' into matlab.
%Motion compensation of gcamp movies.
function batch_mc(fps)
%BATCH_MC(FPS)
%   Applies the dipimage function 'correctshift' to avi files in current
%   directory to implement motion compensation. FPS is the sampling rate of
%   the movie (round to nearest integer.)

cd('E:\imaging\data')
subdirfiles = dir('*.avi');
for l = 1:length(subdirfiles)
    
    cd('E:\imaging\data')
    
    %Creates string from the filename of the first .avi file in the directory;
    % deletes '.avi'. 
    
    avifile = subdirfiles(l).name;
    disp(avifile)
    filename = strrep(subdirfiles(l).name, '.avi', '');
    disp(filename);
    
    %Loads avi file and performs motion compensation.
    startmovie = readavi(avifile,[]);
    disp(datestr(clock));
    % Aligns to frame before stimulation. Averages 1 second's worth of
    % frames to get reference frame.
    [mc_movie, s, crib] = correctshift(startmovie, fps*8, fps);
    disp(datestr(clock));
    %CD to mc directory and saves shift coordinates as 'filename_s.dat'
    %and crib estimates as 'filename_crib.dat' in the 'shifts' and 'cribs'
    %folders respectively. Saves the motion-compensated avi file into the
    %parent 'mc' folder, with no compression and at 12 fps.
    
    w = 'E:\imaging\results'     
        
    filename_mc = fullfile(w, [filename '_mc']);
    writeavi(mc_movie, filename_mc, 12, 'None');
    
    filename_s = fullfile(w, [filename '_s.dat']);
    filename_crib = fullfile(w, [filename '_crib.dat']);
      
    save(filename_s,'s','-ascii');  
    save(filename_crib,'crib','-ascii');
    clear mc_movie;
    clear startmovie;
end
