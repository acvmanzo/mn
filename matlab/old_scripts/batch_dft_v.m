%For use with videos of flies sucking blue liquid. Calculates the discrete
%fourier transform of the intensity measurements of an ROI.
%
%Batch version -  most updated. As with all other batch version, this
%script assumes a specific file structure in which a parent directory
%(indicated in the first line of the script) contains a directory for each
%movie being analyzed.
%
%Requires that the following files are present in each directory:
%params.mat, results1.txt, fps.dat.
%
cd('C:\Users\Andrea\Documents\Lab\dtrpa1_freq\data');
dirfiles = dir;

for l = 3:length(dirfiles)
    
 cd('C:\Users\Andrea\Documents\Lab\dtrpa1_freq\data');
    cd(dirfiles(l).name);
    if exist('params.mat') == 0, continue; end
    
    v = dlmread('results1.txt', '\t', 1, 1);
    load fps.dat;
    load params.mat;
    
    for i = 1:size(p,1)
        %Plots the raw trace of the intensity vs. time, the interval chosen
        %for the fourier transform is indicated with red veritcal lines.
        figure(1); 
        subplot(2,3,1); plot(v); hold on;
        ym = ylim;
        linecoord = [repmat(p(i, :), 2, 1), linspace(ym(1), ym(2), 2)'];
        line(linecoord(:, 1), linecoord(:, 3), 'Color', 'r');
        line(linecoord(:, 2), linecoord(:, 3), 'Color', 'r');
        title('Raw trace'); 
        hold 'off';
        
        %Plots only the interval selected for the transform.
        vt = v(p(i, 1):p(i, 2));
        subplot(2,3,2); plot(vt);
        title('Selection for transform');
        
        legend(num2str(p(i, :)));
        axis([0 length(vt) min(vt)-0.05*min(vt) max(vt)+0.05*max(vt)]);
        set(gca, 'FontSize', 7);
        
            
        %Subtract the mean from the truncated signal and multiply by the
        %Hamming window (which tapers the signal to zero near the ends).
        vtc = hamming(length(vt),'periodic').*(vt - mean(vt));
        subplot(2,3,3); plot(vtc);
        title('Mean subtracted and Hamming multiplied'); 

        % Calculates and plots the DFT of the signal and normalizes it so that the
        % peak is at 1.

        vtc_nft = abs(fft(vtc))/max(abs(fft(vtc)));
        subplot(2,3,4); plot(vtc_nft);
        title('Normalized fourier transform'); 

        % Plots the first half of the DFT. 

        subplot(2,3,5);
        plot(linspace(0, fps/2, length(vtc_nft)/2), vtc_nft(1:length(vtc_nft)/2));
        title('Truncated'); 
        xlabel('Hz');

        fsx = linspace(0, fps/2, length(vtc_nft)/2);
        fsy = vtc_nft(1:length(vtc_nft)/2);

        % Plots the first half of the DFT again in a separate figure. Also
        % shows the legend, which says which frames were used to calculate
        % this DFT.
        figure(2); plot(fsx, fsy, 'LineWidth', 1.5);
        xlabel('Hz');
        title('DFT');
        legend(num2str(p(i, :)));
        %figure(2); plot(linspace(0, fps/2, length(vtc_nft)/2),
        %vtc_nft(1:length(vtc_nft)/2))
        xlabel('Hz');
        title('Frequency Spectrum');
    
        % Saves the figures in the specified folder and with the
        % appropriate filename. Figure 1 is saved as (name of the
        % folder)_DFTsteps_(#) and Figure 2 is saved as (name of the
        % folder)_DFT_(#). Sometimes I initially choose several intervals
        % to calculate the DFT over; these are saved in the variable p. #
        % corresponds to which row in p was used to calculate the DFT. 
        name = dirfiles(l).name;
        num = num2str(i);
        w = fullfile('C:\Users\Andrea\Documents\Lab\dtrpa1_freq\results', name);
        filenamefig1 = [w '\' name '_DFTsteps_' num '.fig'];
        filenamejpg1 = [w '\' name '_DFTsteps_' num '.jpg'];

        saveas(1, filenamefig1, 'fig');
        saveas(1, filenamejpg1, 'jpg');
        
        filenamefig2 = [w '\' name '_DFT_' num '.fig'];
        filenamejpg2 = [w '\' name '_DFT_' num '.jpg'];

        saveas(2, filenamefig2, 'fig');
        saveas(2, filenamejpg2,'jpg');

        % Plots spectrogram and saves it in the same manner as described
        % above.
        figure(3); 
        x = 60; 
        spectrogram(v, x, floor(0.95*x), 256, fps);
        refline(0, p(i,1)/fps); refline(0, p(i, 2)/fps);
        title('Spectrogram');
        colorbar;
        filenamefig3 = [w '\' name '_Spect_' num '.fig'];
        filenamejpg3 = [w '\' name '_Spect_' num '.jpg'];

        saveas(3, filenamefig3, 'fig');
        saveas(3, filenamejpg3, 'jpg');

        %Saves the workspace variables in a file titled 'filenamevar.mat'.
        filenamevar = [w '\' name '_variables_' num '.mat'],
        save(filenamevar);

    end
    
end
