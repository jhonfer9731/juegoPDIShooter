function [c]=pic2bc(snap)

lab=rgb2lab(snap);
b=lab(:,:,3);
b=double(b);
b=b/max(b(:));
b=uint8(b*255);
b2=b;
b2(b2<175)=0;b2(b2>0)=255;
c(:,:,1)=b2;
c(:,:,2)=b2;
c(:,:,3)=b2;

end