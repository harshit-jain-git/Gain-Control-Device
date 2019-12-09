n=0:4000;
x1=1.5*stepseq(0,0,4000)-0.2*stepseq(500,0,4000)+0.4*stepseq(1000,0,4000)-0.2*stepseq(1500,0,4000)+0.5*stepseq(2000,0,4000)-1*stepseq(2500,0,4000)+0.6*stepseq(3000,0,4000)-0.2*stepseq(3500,0,4000)-0.2*stepseq(4000,0,4000);
stem(n,x1);
x2 = ifft(x1);

% This is the function which i called in the baove code
function [x,n]=stepseq(n0,n1,n2)
n=n1:n2;
x=(n-n0>=0);
end