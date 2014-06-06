

    v = dlmread('results1.txt', '\t', 1, 1);
    load fps.dat;
    load params-f.mat;
   
    
    for i = 1:size(p,1)
        %Plots the raw trace of the intensity vs. time, the interval chosen
        %for the fourier transform is indicated with red veritcal lines.
%         figure(1); 
%         subplot(2,3,1); plot(v); hold on;
%         ym = ylim;
%         linecoord = [repmat(p(i, :), 2, 1), linspace(ym(1), ym(2), 2)'];
%         line(linecoord(:, 1), linecoord(:, 3), 'Color', 'r');
%         line(linecoord(:, 2), linecoord(:, 3), 'Color', 'r');
%         title('Raw trace'); 
%         hold 'off';
        
        %Plots only the interval selected for the transform.
        vt = v(p(i, 1):p(i, 2));
%         subplot(2,3,2); plot(vt);
%         title('Selection for transform');
%         
%         legend(num2str(p(i, :)));
%         axis([0 length(vt) min(vt)-0.05*min(vt) max(vt)+0.05*max(vt)]);
%         set(gca, 'FontSize', 7);
        
            
        %Subtract the mean from the truncated signal and multiply by the
        %Hamming window (which tapers the signal to zero near the ends).
        vtc = hamming(length(vt),'periodic').*(vt - mean(vt));
%         subplot(2,3,3); plot(vtc);
%         title('Mean subtracted and Hamming multiplied'); 

        % Calculates and plots the DFT of the signal and normalizes it so
        % that the (first peak after the 0.4*length(vtc) point) is at 1.
        
        dftlength = 8000;
        b = abs(fft(vtc, dftlength));
        c = max(b(floor(0.1*dftlength):dftlength/2));
        vtc_nft = abs(fft(vtc,dftlength)/c);
        
        %vtc_nft = abs(fft(vtc,4*length(vtc)))/max(abs(fft(vtc, 4*length(vtc))));
%         subplot(2,3,4); 
%         plot(vtc_nft);
%         axis([0 4*length(vtc) 0 1]);
%         title('Normalized fourier transform'); 

        % Plots the first half of the normalized DFT. 

        vtc_nft_trunc = vtc_nft(1:dftlength/2); 
%         subplot(2,3,5);
%         plot(linspace(0, fps/2, length(vtc_nft)/2), vtc_nft(1:length(vtc_nft)/2));
%         axis([0 fps/2 0 1]);
%         title('Truncated'); 
%         xlabel('Hz');
             
        % Plots the unnormalized, truncated fourier transform
%         subplot(2,3,6);
        vtc_ft = abs(fft(vtc, 8000));
%         plot(linspace(0, fps/2, length(vtc_ft)/2), vtc_ft(1:length(vtc_ft)/2));
%         title('Unnormalized truncated transform');
%         xlabel('Hz');
        
        fsx = linspace(0, fps/2, 4000);
        fsy = vtc_nft(1:4000);
        fmat = [fsx' fsy];

        % Plots the first half of the DFT again in a separate figure. Also
        % shows the legend, which says which frames were used to calculate
        % this DFT.
        figure(1)
        plot(fsx, fsy, 'LineWidth', 1.5);
        xlabel('Hz');
        title('DFT');
        legend(num2str(p(i, :)));
        %figure(2); plot(linspace(0, fps/2, length(vtc_nft)/2),
        %vtc_nft(1:length(vtc_nft)/2))
        axis([0 fps/2 0 1]);
        xlabel('Hz');
        title('Frequency Spectrum');
    
%         % Plots spectrogram.
%         figure(3); 
%         x = 60; 
%         spectrogram(v, x, floor(0.95*x), 1200, fps);
%         refline(0, p(i,1)/fps); refline(0, p(i, 2)/fps);
%         ti = ['Spectrogram ' num2str(p(i, 1)) ' to ' num2str(p(i, 2))]; 
%         title(ti);
%         colorbar;
        
%         Saves the figures in the specified folder and with the
%         appropriate filename. Figure 1 is saved as (name of the
%         folder)_DFTsteps_(#) and Figure 2 is saved as (name of the
%         folder)_DFT_(#). Sometimes I initially choose several intervals
%         to calculate the DFT over; these are saved in the variable p. #
%         corresponds to which row in p was used to calculate the DFT. 
        
        [str, remain] = strtok(pwd, '\');
            while true
               [str, remain] = strtok(remain, '\');
               if isempty(str),  break;  end
               name = str;,
            end
        
        num = num2str(i);
        w = fullfile('C:\Users\Andrea\Documents\Lab\dtrpa1_freq\results_pw', name);
        if exist(w, 'dir') ~= 7, mkdir(w), end
        filenamefig1 = [w '\' name '_DFT_pw_' num '.fig'];
        filenamejpg1 = [w '\' name '_DFT_pw_' num '.jpg'];

        saveas(1, filenamefig1, 'fig');
        saveas(1, filenamejpg1, 'jpg');
%         
%         filenamefig2 = [w '\' name '_DFT_' num '.fig'];
%         filenamejpg2 = [w '\' name '_DFT_' num '.jpg'];
% 
%         saveas(2, filenamefig2, 'fig');
%         saveas(2, filenamejpg2,'jpg');
%         
%         filenamefig3 = [w '\' name '_Spect_' num '.fig'];
%         filenamejpg3 = [w '\' name '_Spect_' num '.jpg'];
% 
%         saveas(3, filenamefig3, 'fig');
%         saveas(3, filenamejpg3, 'jpg');
% 
        %Saves the workspace variables in a file titled 'filenamevar.mat'.
        filenamevar = [w '\' name '_variables_' num '.mat'],
        save(filenamevar);
% 
    end

