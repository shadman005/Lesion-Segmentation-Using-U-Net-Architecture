clear all;
close all;
clc;

folderPath = 'C:\Users\DELL\Box\Ultrasound';
files = dir(folderPath);
feature_set=zeros(437,7);
patient = {};
%feature_set = table('Size', [210, 7])

%feature_set(1,:) = ['Patient','lesion_area','lesion_aspect_ratio','irregularityIndex','lesion_mean','lesion_std','target_variable']
for i=1:1:437
fileName = strcat('benign (',num2str(i),').png');   
I = imread(fileName); 
fileName = strcat('benign (',num2str(i),')_pred.png');   
M = imread(fileName); %Masked Image (M)
M=double(M);
M=M/255;
I = rgb2gray(I);
I = im2double(I);
L= I.*M; %Lesion Segmented Image (L)
%Morphometric Features - Depend on the shape and size of the lesion
cc = bwconncomp(M); %Finding the boundary of the Binary Masked Image
props = regionprops(cc, 'BoundingBox', 'Area');
A = [props.Area]; %Making a matrix out of all the areas
max_area_index = find(A == max(A)); %Finding the maximum area, this is to remove all the small areas falsely detected
%by the ML algorithms
props=props(max_area_index);%Changed this line
%Feature 1
lesion_area(i)=props.Area/numel(I); 
%Feature 2
lesion_aspect_ratio(i) = props.BoundingBox(4)/props.BoundingBox(3); %Depth (or height) divided by Width

boundaries = bwboundaries(M);
boundary = boundaries{max_area_index}; %Changed this line
try
    [k, v] = convhull(boundary(:,2), boundary(:,1));
    perimeterOriginal = sum(sqrt(sum(diff(boundary([1:end,1],:)).^2,2)));
    boundaryHull = boundary(k, :); % Points on the convex hull
    perimeterConvexHull = sum(sqrt(sum(diff(boundaryHull).^2, 2)));
    %Feature 3
    irregularityIndex(i) = perimeterOriginal / perimeterConvexHull;
catch
    irregularityIndex(i) = mean(irregularityIndex)
end
%Quantitative Features - Depend on the pixel values of the lesion
[row,col]=find(L>0 & L<.8);
pixelValues = L(sub2ind(size(L), row, col));
%Feature 4
lesion_mean(i) = sum(pixelValues)/length(pixelValues);
%Feature 5
lesion_std(i) = std(pixelValues);
patient{i} = cellstr(strcat('B_',num2str(i)));
target_variable{i} = 0;

end
patient =string(patient);
target_variable=string(target_variable);

feature_set = table(patient',lesion_area',lesion_aspect_ratio',irregularityIndex',lesion_mean',lesion_std',target_variable','VariableNames',{'Patient','lesion_area','lesion_aspect_ratio','irregularityIndex','lesion_mean','lesion_std','target_variable'})


% Specify the filename
filename = 'feature_set_benign.xlsx';
% Write the table to an Excel file
writetable(feature_set, filename);