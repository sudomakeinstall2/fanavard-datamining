% Solve an Input-Output Fitting problem with a Neural Network
% Script generated by NFTOOL
% Created Sat Nov 26 15:02:20 IRST 2016
%
% This script assumes these variables are defined:
%
%   x2 - input data.
%   price - target data.

load 3_data.txt
x = X3_data(:,1);
price = X3_data(:,3);
diff = X3_data(:,2);
x2 = [x diff];


inputs = x2';
targets = price';

% Create a Fitting Network
hiddenLayerSize = 10;
net = fitnet(hiddenLayerSize);


% Setup Division of Data for Training, Validation, Testing
net.divideParam.trainRatio = 70/100;
net.divideParam.valRatio = 15/100;
net.divideParam.testRatio = 15/100;


% Train the Network
[net,tr] = train(net,inputs,targets);

% Test the Network
outputs = net(inputs);
errors = gsubtract(targets,outputs);
performance = perform(net,targets,outputs)

% View the Network
% view(net)

% Plots
% Uncomment these lines to enable various plots.
%figure, plotperform(tr)
%figure, plottrainstate(tr)
%figure, plotfit(net,inputs,targets)
%figure, plotregression(targets,outputs)
%figure, ploterrhist(errors)

load 3_data_q.txt;
results = net(X3_data_q')

