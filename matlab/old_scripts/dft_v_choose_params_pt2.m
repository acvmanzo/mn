%Use this script to generate the params.m file for analyzing dye ingestion
%videos. Makes sure the params are odd.


r = rem(p(:, 2) - p(:, 1), 2);

for i = 1:length(r)
    if r(i) == 0
      p(i, 2) = p(i, 2) - 1  
    end
end

p,
save params p; 
close


