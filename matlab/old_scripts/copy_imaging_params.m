%Copy imaging_params.m file from data folder to the mc folder.

dirfiles = dir;

for l = 3:length(dirfiles)
    cd('c:\Users\Andrea\Documents\Lab\762\data');
    cd(dirfiles(l).name);
    if exist('imaging_params.m') == 0, continue; end
    
    subdirfiles = dir('*.avi');
    aviname = strrep(subdirfiles(1).name, '.avi', '');
    disp(aviname);
    
    vdir = fullfile('c:\Users\Andrea\Documents\Lab\762\mc', aviname);
    mkdir(vdir);
    v = fullfile('c:\Users\Andrea\Documents\Lab\762\mc', aviname, 'imaging_params.m');
    
    copyfile('imaging_params.m', v);
    
end
    
    