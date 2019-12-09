[Xn, Fs] = audioread('../noise_reduction/00_samples/sample_1.wav');
Xn = Xn(:,1);
Xn = Xn';
Xn = Xn(:,[1:100000]);
n=0:4000;
x1=1.5*stepseq(0,0,4000)-0.2*stepseq(500,0,4000)+0.4*stepseq(1000,0,4000)-0.2*stepseq(1500,0,4000)+0.5*stepseq(2000,0,4000)-1*stepseq(2500,0,4000)+0.6*stepseq(3000,0,4000)-0.2*stepseq(3500,0,4000)-0.2*stepseq(4000,0,4000);
% stem(n,x1);
Hn = ifft(x1);

L=input('Enter length of each block L = ');

% Code to perform Convolution using Overlap Add Method
NXn=length(Xn);
M=length(Hn);
M1=M-1;
R=rem(NXn,L);
N=L+M1;
Xn=[Xn zeros(1,L-R)];
Hn=[Hn zeros(1,N-M)];
K=floor(NXn/L);
y=zeros(K+1,N);
z=zeros(1,M1);

for k=0:K
Xnp=Xn(L*k+1:L*k+L);
Xnk=[Xnp z];
y(k+1,:)=mycirconv(Xnk,Hn); %Call the mycirconv function.
end
p=L+M1;
for i=1:K
y(i+1,1:M-1)=y(i,p-M1+1:p)+y(i+1,1:M-1);
end
z1=y(:,1:L)';
y=(z1(:))';

audiowrite('overlapadd.wav', y, Fs);
% This is the function which i called in the baove code
function [x,n]=stepseq(n0,n1,n2)
n=n1:n2;
x=(n-n0>=0);
end

%Function of Circular Convolution for the Overlap Save Method.
function y=mycirconv(x,h)
lx=length(x);
lh=length(h); 
l=max(lx,lh); 
X=[x zeros(1,l-lx)]; 
H=zeros(l); 
H(1:lh)=h; 
for j=1:l-1 
for i=1:l-1 
H(i+1,j+1)=H(i,j); 
end 
H(1,j+1)=H(l,j); 
end 
y=H*X';
end
