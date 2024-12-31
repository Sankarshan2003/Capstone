
info = imfinfo('objects.png');
info.BitDepth 

I = imread('objects.png');
BW = imbinarize(rgb2gray(I));

BWConv = (~BW);
BW = BWConv;


figure()
h = imshow(BW); 
axis on
stats = regionprops('table',BW,'Centroid','MajorAxisLength','Orientation');
% How many objects were detected?
nObjects = size(stats,1);  % = 74
% take a look at the results
head(stats) %first few objects
% Continuing with the figure created above, add the center points
hold on
ph1 = plot(stats.Centroid(:,1), stats.Centroid(:,2), 'rs'); 
% using orientation, compute slope and y-intercept of each major axis
% Note the reversal of the sign of the orientation!  This is to account 
% for the reversed y axis!            
%           here---v
stats.Slope = atan(-stats.Orientation*pi/180); 
% Compute y interceps
stats.Intercep = stats.Centroid(:,2) - stats.Slope.*stats.Centroid(:,1); 
% Now that we've got the linear eq for each line, compute the bounds of each
% object along its major axis line. Add some extra length so we can see more of the lines. 
% To use the exact major axis lenght, divide by 2 instead of 1.6 (both lines below)
stats.EndpointX = stats.Centroid(:,1) + [-1,1].* (stats.MajorAxisLength/1.6 .* sqrt(1./(1+stats.Slope.^2))); 
stats.EndpointY = stats.Centroid(:,2) + [-1,1].* (stats.Slope .* stats.MajorAxisLength/1.6 .* sqrt(1./(1+stats.Slope.^2))); 
% Plot major axis of each object that spans the length of the obj
mah = plot(stats.EndpointX.', stats.EndpointY.', 'r-');