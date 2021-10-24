<h1>Sprint 2</h1>
<b>Medical Visual Question Answering</b><br>
<b>Group: Ruiling Zhang, Yuko Ishikawa, Zihao Shen</b><br>

<h2>Overall:</h2>
We duplicate and test an open-source python project, which is based on pytorch.<br>
https://github.com/tbmoon/basic_vqa

<h2>The project architecture:</h2><br>
These are important modules and their usage of the project

<h3>Resize picture:</h3>
Module: PIL.image<br>
Method: image.resize([224,224],Image.ANTIALIAS)<br>
Output: The 224*224 picture with the same content, but maybe change aspect ratio.<br>

<h3>Make vocabulary for question and answer:</h3>
<b>Questions:</b><br>
&ensp;&ensp;Data structure: set<br>
&ensp;&ensp;Method: split a question and update the set.<br>
&ensp;&ensp;Output: All tokens used in question dataset<br>
<b>Answers:</b><br>
&ensp;&ensp;Data structure: defaultdict(lambda: 0)<br>
&ensp;&ensp;Dictionary keys: content of answers<br>
&ensp;&ensp;Dictionary values: times of use<br>
&ensp;&ensp;Method: Increase the value of the key by 1 when find the key used. Reverse sort the dictionary and pick the top 1000 answers.<br>
&ensp;&ensp;Output: the top 1000 answers.<br>

<h3>Build VQA inputs:</h3>
&ensp;&ensp;Data Structure: list and dictionary<br>
&ensp;&ensp;Dictionary keys: [image_name, image_path, question_id, question_str, question_tokens], and may also have [all_answers, valid_answers] if the answer is given. All answers are all possible answer for this question, and valid answers are answers in both ‘All answers’ and ‘Answer vocabulary’ built before.<br>
&ensp;&ensp;Output: a list of dictionaries, store it as .npy file.<br>

<h3>Train/valid Dataset:</h3>
&ensp;&ensp;vqa: the list of dictionaries built by ‘build vqa inputs.py’<br>
&ensp;&ensp;qst_vocab/ans_vocab: class, which read question/answer vocabulary file created before, and make the content as list and dictionary.<br>
&ensp;&ensp;transform: ToTensor() and Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)). The parameters are mean and standard derivation, and the value is referring ImageNet. But the value may only be used in "natural scenes" (people, buildings, animals, varied lighting/ angles/ backgrounds, etc.)<br>

<h3>Data loader:</h3>
&ensp;&ensp;Method: torch.utils.data.DataLoader<br>
&ensp;&ensp;Random choose #batch_size data from dataset built before.<br>

<h3>ImgEncoder:</h3>
&ensp;&ensp;Using pretrained vgg19 model. Removing the last full connect layer, and using Linear to convert the output of the edited vgg19 network to a 1024 feature vector of the image<br>

![vgg19](https://user-images.githubusercontent.com/55321300/138577656-e6c0a752-49d9-4358-92af-9265ffd54e6e.png)

&ensp;&ensp;When forward propagation, calulate the norm of the output of the network. We cannot sure what the usage of this part.<br>

<h3>QstEncoder:</h3>
&ensp;&ensp;Using LSTM model. Input size is 300, which is a word and it will be picked from the dictionary/ matrix built by pytorch.nn Embedding function. Hidden size is 512, which can be customized. And there are two layers, it can be recognized as depth in this picture.<br>

<div align="center">

![LSTM](https://user-images.githubusercontent.com/55321300/138577696-7aaeb898-09d8-4b1e-a260-7163eba575e9.jpg)

</div>

&ensp;&ensp;Also using Linear to convert the parameters of LSTM to a 1024 feature vector of the sentence.<br>
&ensp;&ensp;When forward propagation, the question will convert to the format of LSTM input and activate by tanh. And use the parameters of hidden and cell, we think that is the output and the long memory state. And the last Linear layer will convert the 2(hidden and cell) * 2(layers) * 512(hidden size) vector to a 1024 feature vector of the sentence.<br>

<h3>VQAModel:</h3>
&ensp;&ensp;Using ImgEncoder and QstEncoder. Multiplying the two outputs of the two models, and two full connected layers to convert the 1024 vector to a 1000 vector.<br>

<img width="1053" alt="basic_model" src="https://user-images.githubusercontent.com/55321300/138577725-086f373d-e68e-4386-9b86-8a261dc722d2.png">

<h3>Train:</h3>
&ensp;&ensp;Loss function: CrossEntropyLoss()<br>
&ensp;&ensp;Optimizer: Adam()<br>
&ensp;&ensp;Change learn rate: StepLR()<br>
&ensp;&ensp;Use the VQAModel to predict, the output will be a 1000 vector, which indicate the possibility of the answer depend on the answer vocabulary built before. Then pick the max possibility to calculate the accuracy.<br>

<h2>Technology:</h2>
&ensp;&ensp;Tool: Pytorch<br>
&ensp;&ensp;Model: VGG19, LSTM<br>
&ensp;&ensp;And some necessary functions to train and evaluate.<br>

<h2>Our duplicate project output:</h2>
<div align="center">

![Project_sprint2_overview](https://user-images.githubusercontent.com/55321300/138577760-fd9f73e6-b613-45b9-9388-7c2f5ee0a5ea.JPG)

</div>
<h2>Use the model to predict:</h2>
The architecture of our code is simple. Firstly, convert the picture and the question to tensor that fit the input size of the model. Then, load the checkpoint file which saved by the open-source project. After that, change the model to evaluate mode and feed the input into the model to get the output. Finally, pick the answer depends on the output possibility of the model.<br>

<div align="center">
<img src="https://user-images.githubusercontent.com/55321300/138578425-c078ac86-a4c9-4522-9cc5-974ba1bbcf75.JPG" style="width:70%" />
<img src="https://user-images.githubusercontent.com/55321300/138577776-9e77e7c8-def4-4d7f-ae54-1e80c3447220.JPG" style="width:70%" />
<img src="https://user-images.githubusercontent.com/55321300/138577779-1fd1cfad-fcaf-43a7-8836-eb061bff4408.JPG" style="width:70%" />
<img src="https://user-images.githubusercontent.com/55321300/138577783-261fe3bb-85b9-4025-adab-09275e58ae34.JPG" style="width:70%" />
</div>

So, as we mentioned before, the answers always are picked in the top 1000 answers, we are not sure why the author of the open-source project planned to implement like this.

<h2>Future work:</h2>
&ensp;&ensp;Convert the model to medical input<br>
&ensp;&ensp;Maybe increase the answer field
