
info = imfinfo('objects.png');
info.BitDepth 

I = imread('objects.png');
BW = imbinarize(rgb2gray(I));

BWConv = bwconvhull(~BW);
BW = BW & BWConv;


figure()
h = imshow(BW); 