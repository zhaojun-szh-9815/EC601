<h1>Sprint 4</h1>
<b>Medical Visual Question Answering</b><br>
<b>Group: Ruiling Zhang, Yuko Ishikawa, Zihao Shen</b><br>

<h2>Overall:</h2>
We built and tested a simple model for medical vqa based on the basic vqa project (https://github.com/tbmoon/basic_vqa).<br>
The dataset is Med-RED (https://osf.io/89kps/).<br>

<h2>Our project architecture:</h2>
data_loader.py:<br>
&ensp;&ensp;generate data according to batch size, use new normalization value<br>
medical_models.py:<br>
&ensp;&ensp;use convolution instead of multiplication when fusing features from image and question, still use LSTM and pre-trained vgg-19<br>
medical_train.py:<br>
&ensp;&ensp;train the vqa model, add continue training option<br>
preprocessing.py:<br>
&ensp;&ensp;download images, resize images, build question / answer vocabulary<br>
text_helper.py:<br>
&ensp;&ensp;split sentences to tokens, and build dictionary for question tokens and answers<br>
vqa_predict.py:<br>
&ensp;&ensp;predict by specific saved model, plot accuracy by logs<br>

<h2>Outputs:</h2>
<div align="center">
<img alt="med_model_plot_1" src="https://user-images.githubusercontent.com/55321300/144171195-9c8a41aa-d67a-42c3-a8e6-c161be86690e.png">
</div>

Before training, calculate mean value and standard deviation for the 314 pictures in dataset.<br> 
&ensp;&ensp;mean = [0.2539457, 0.2538943, 0.25384054]<br>
&ensp;&ensp;std= [0.048477963, 0.048473958, 0.04845482]<br>
&ensp;&ensp;It performs better than using value for natural pictures from ImageNet.<br>
Batch size has great influence on the result. When tested by batch size 2 and 16, the result is very bad, but it looks good when batch size is 1. Maybe it is related to the size of the dataset.<br>
We trained 20 epoches, using new normalization value, and batch size is 1. The accuracy is nearly 100% in the end. It is overfitting. The prediction made by the last model is really bad.<br>
Finally, we choose the model made by the 10th epoch.<br><br>

<table align="center">
<tr>
<td align="center">synpic27142.jpg<img width="292" alt="synpic27142" src="https://user-images.githubusercontent.com/55321300/144185050-50af1d5b-3ff4-456d-b2a7-01c64b8729b3.jpg"></td>
<td align="center">synpic19114.jpg<img width="292" alt="synpic19114" src="https://user-images.githubusercontent.com/55321300/144185051-1bb736d6-2ca4-40ae-8588-43955a4d621a.jpg"></td>
<td align="center">test.jpg<img width="292" alt="test" src="https://user-images.githubusercontent.com/55321300/144185181-2ecd7356-a5a4-44bb-b37a-0f03f8687700.jpg"></td>
</tr>
<tr>
<td align="center"><img width="292" alt="med_model_predictions1" src="https://user-images.githubusercontent.com/55321300/144170429-77ba5142-b92a-4bd7-8bf4-5ce594c824fe.png"></td>
<td align="center"><img width="292" alt="med_model_predictions2" src="https://user-images.githubusercontent.com/55321300/144174668-fde2ffec-3b38-46ea-818d-a48c56662840.png"></td>
<td align="center"><img width="292" alt="test_prediction" src="https://user-images.githubusercontent.com/55321300/144174576-a0ff3022-e878-44dc-9eb3-7df1cf4d857a.PNG"></td>
</tr>
</table><br>

In our test, 'what' question performed well. So we paied more attention on 'Yes/No' question.<br><br>

<table align="center">
<tr>
<td align="center"><img width="185" alt="dataset_analyze_answers_frequency" src="https://user-images.githubusercontent.com/55321300/144177156-b4bd4aa4-ddbe-4ac3-aaee-0f5d59c20a2f.PNG"></td>
<td align="center"><img width="333" alt="dataset_analyze_yes_no_percentage" src="https://user-images.githubusercontent.com/55321300/144176395-a173ce2c-9b35-46dc-b14a-44709fb1eeb2.PNG"></td>
<td align="center"><img width="333" alt="dataset_analyze_frequency" src="https://user-images.githubusercontent.com/55321300/144175259-d791f367-4460-43cb-b27b-5b127529f8dd.PNG"></td>
</tr>
</table><br>

There are 2248 objects, 1019 kinds of questions, 517 kinds of answers.<br>
In this 517 kinds of answers, 'yes' appears 587 times, 'no' appears 606 times, almost 1:1. The yes/no answer rate is also almost 1:1 in each organ.<br>
But in this 1019 kinds of questions, only 90 kinds of questions appear more than once.<br>
Our simple model can not deal with these limited samples.<br>
In the test case, the question "Is this the brain/chest" and "Is brain/chest pictured" performed bad. "Is this the brain/chest" only appears once in dataset. "Is brain/chest pictured" is the paraphrase by ourselves.<br>
The question "Is the heart enlarged" and "Is this an MRI" performed well. "Is the heart enlarged" appears 14 times, and "Is this an MRI" appears 4 times.<br>

<h2>Challenges:</h2>
blurred images: The pictures we downloaded are 100*75 pixels. Compared with natural pictures we used before, they are very small and unclear.<br>
synonyms: The answers have many different expression of the same meaning. In the test case, we can see "xray", "x-ray", "xray-plain film" in answer field.<br>

<h2>Future work:</h2>
We still want to build an efficient model to deal with this dataset, since some data is hard to collected.<br>
Here are some possible solutions for this problem:<br>
&ensp;&ensp;Data augmentation: use generative adversarial networks (GAN), but maybe generate invalid inputs since the medical dataset is rigorous.<br>
&ensp;&ensp;Paraphrase: use NLP modules to detect and deal with synonyms, paraphrase to a standard format. But some medical terms may not contain in the module.<br>
&ensp;&ensp;Concentration: apply attention models to question encoder, perhaps also image encoder.<br>
