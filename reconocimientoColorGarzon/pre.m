clear all, close all, clc
%foto=imread('fire.jpg');
cam=webcam;

for i=1:200
    snap=snapshot(cam);
    b=pic2bc(snap);
    figure(1);imshow([snap;b]);
    pause(0.0001)
end


