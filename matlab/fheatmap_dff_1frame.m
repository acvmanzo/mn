function fheatmap_dff_1frame(avimovie, bg_frame, stim_frame, max_frame)
% FHEATMAP_DFF_1FRAME(AVIMOVIE, BG_FRAME, STIM_FRAME, MAX_FRAME)
% Makes a deltaf/f heatmap image from the MAX_FRAME of file AVIMOVIE. Frames BG_FRAME to STIM_FRAME-1
% are averaged and used as the baseline frame. Alter imagesc (line 50) to
% change the colormapping.


% Opens avi file as an mmreader object.
rawmovie = mmreader(avimovie);

%Assigns the baseline frames into the variable "bframes".
bframes = read(rawmovie, [bg_frame, stim_frame-1]);

%Takes only the green channel and deletes the rest of the frames.
bframesg = bframes(:, :, 2, :);

%Averages all the baseline frames.
avg_bframesg = sum(bframesg, 4)./size(bframesg,4);
disp(size(avg_bframesg));


%Creates string from the filename of the avifile and deletes '.avi'.
filename = strrep(avimovie, '.avi', '');
disp(filename);

% Creates a filename for the movie specific to each file.
filenametxt = [filename '_heatmapmovie_avg.png'];

%Subtracts averaged baseline frame from each frame and filters it using
%medfilt2 with specified parameters. Displays each frame
%using imagesc with specified parameters, and adds the scaled frame to
%the avi file "heatmap_movie", which is saved in the heatmap_movie
%directory.

i = max_frame;
%Reads in 3 frames: max frame and two surrounding frames.
maxframes = read(rawmovie, [i-1, i+1]);
disp(size(maxframes));
maxframesg = maxframes(:, :, 2, :);
disp(size(maxframesg));
% Averages the max frames.
avg_maxframesg = sum(maxframesg, 4)./size(maxframesg,4);
disp(size(avg_maxframesg));
f = avg_maxframesg;

%imshow(avg_bframesg);
%Converts values in the frame from integers to double-precision floating
%point numbers.
f = double(f);

%Subtracts averaged baseline frame from current frame then divides by the averaged baseline frame (deltaF/F)
fdelta = (f-avg_bframesg)./(avg_bframesg);


%Filters the image; replaces each pixel with the median of the [3,3] neighborhood around it.
f_fil = medfilt2(fdelta,[3,3]);


%Maps the pixel values of the image to a color, such that values 
% below the first number are mapped to blue and values above the second
% number are mapped to red.
imagesc(f_fil, [-0.1, 2]);

colorbar;

saveas(1, filenametxt)

end
