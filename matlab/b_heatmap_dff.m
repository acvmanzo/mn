dirfiles = dir;

for l = 3:length(dirfiles)
    cd('e:\gcamp_hm\data');
    cd(dirfiles(l).name);
    if exist('imaging_params.m') == 0, continue; end
         
    imaging_params;
    
    % Opens avi file as an mmreader object.
    subdirfiles = dir('*.avi');
        
    rawmovie = mmreader(subdirfiles(1).name);
    

    %Assigns the baseline frames into the variable "bframes".
    bframes = read(rawmovie, [bg_frame, stim_frame-1]);
    
    %Takes only the green channel and deletes the rest of the frames.
    bframesg = bframes(:, :, 2, :);

    
    %Averages all the baseline frames.
    avg_bframesg = sum(bframesg, 4)./size(bframesg,4);
 
    %Creates string from the filename of the first .avi file in the directory;
    % deletes '.avi'. 
    filename = strrep(subdirfiles(1).name, '.avi', '');
    disp(filename);
    
    %Moves to folder where heatmap movie files are to be saved, and creates
    %a filename for the movie specific to each file.
    cd('e:\gcamp_hm\hm_movies');
    filenametxt = [filename '_heatmapmovie'];
    
    %Subtracts averaged baseline frame from each frame and filters it using 
    %medfilt2 with specified parameters. Displays each frame
    %using imagesc with specified parameters, and adds the scaled frame to
    %the avi file "heatmap_movie", which is saved in the heatmap_movie
    %directory.
    numFrames = get(rawmovie, 'numberOfFrames');
    
    aviobj = avifile(filenametxt, 'compression', 'None', 'fps', 20);
    
    for i = 1:numFrames
        f = read(rawmovie, i);
        f = double(f(:,:,2));
        f = (f-avg_bframesg)./(avg_bframesg);
        f_fil = medfilt2(f,[3,3]);
        imagesc(f_fil, [-0.1,2]);
        frame = getframe;
        aviobj = addframe(aviobj, frame);
        
    end
    
   aviobj = close(aviobj); 
   
   
    
end

      