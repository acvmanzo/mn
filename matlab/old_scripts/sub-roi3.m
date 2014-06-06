%top blue trace is roi2
%top cyan trace is c
%top green trace is the difference between roi2 and c
%bottom blue trace is the normalized roi2
%
%Things to assign manually:
%A, pre1, pre2(=slice right before stimulation)

A = dlmread('results1.txt', '\t', 1, 0);
r1 = A(:,2)';
r2 = A(:,3)';
r3 = A(:,4)';
c = A(:,5)';
pre = 23;
pre1 = 23;
pre2 = 23;
%remember that r1 must be in the first column, r2 in the second column, and
%c in the third column

figure(1);
subplot(2,1,1);
plot(r1);
hold on;
plot(c,'c');
dr1c = mean(r1(1:pre))-mean(c(1:pre));
r1_dr1c = r1 - dr1c;
plot(r1_dr1c,'g');
r1norm = r1_dr1c./c;
[mmr1, amr1] = max(r1norm);
subplot(2,1,2);
plot(r1norm);
text(10,1.5,['Coordinates for maximum (',num2str(amr1),', ',num2str(mmr1),')']);
saveas(1,'roi1.fig','fig');
saveas(1,'roi1.jpg','jpg');

figure(2);
subplot(2,1,1);
plot(r2);
hold on;
plot(c,'c');
dr2c = mean(r2(1:pre2))-mean(c(1:pre2));
r2_dr2c = r2 - dr2c;
plot(r2_dr2c,'g');
r2norm = r2_dr2c./c;
[mmr2, amr2] = max(r2norm);
subplot(2,1,2);
plot(r2norm);
text(10,1.5,['Coordinates for maximum (',num2str(amr2),', ',num2str(mmr2),')']);
saveas(2,'roi2.fig','fig');
saveas(2,'roi2.jpg','jpg');

figure(3);
subplot(2,1,1);
plot(r3);
hold on;
plot(c,'c');
dr3c = mean(r3(1:pre))-mean(c(1:pre));
r3_dr3c = r3 - dr3c;
plot(r3_dr3c,'g');
r3norm = r3_dr3c./c;
[mmr3, amr3] = max(r3norm);
subplot(2,1,2);
plot(r3norm);
text(10,1.5,['Coordinates for maximum (',num2str(amr3),', ',num2str(mmr3),')']);
saveas(3,'roi3.fig','fig');
saveas(3,'roi3.jpg','jpg');

figure(4);
r1l = plot(r1norm,'-ob');
set(r1l,'LineWidth',1.5);
text(45,1.4,['Max for ROI 1 = ',num2str(mmr1)]);
hold on;
r2l = plot(r2norm,'-sc');
set(r2l,'LineWidth',1.5);
text(45,1.35,['Max for ROI 2 = ',num2str(mmr2)]);
r3l = plot(r3norm,'-xg');
set(r3l,'LineWidth',1.5);
text(45,1.30,['Max for ROI 3 = ',num2str(mmr3)]);
axis([0  100  0.6 1.6]);
saveas(4,'roi1+2+3pres.fig','fig');
saveas(4,'roi1+2+3pres.jpg','jpg');
hold off


[FileName,PathName] = uiputfile(.avi);
title = strrep(FileName, '.avi', '');
save(title);

plot(A);
plot(



