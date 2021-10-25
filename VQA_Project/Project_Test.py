import os
import torch
import torch.nn as nn
import torchvision.transforms as transforms
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import text_helper                              # this module import from the base-vqa project
from resize_images import main as main_resize   # this module import from the base-vqa project
from models import VqaModel                     # this module import from the base-vqa project

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
transform = {transforms.Compose([transforms.ToTensor(),transforms.Normalize((0.485, 0.456, 0.406),(0.229, 0.224, 0.225))])}

def predict(image_path, question):

    img = Image.open(image_path)
    image = img.resize([224,224], Image.ANTIALIAS)
    image = image.convert('RGB')
    for trans in transform:
        image = trans(image)
    image = image.view(1,3,224,224)
    
    qst_vocab = text_helper.VocabDict('./Data/vocab_questions.txt') # the question vocabulary built by base-vqa project
    ans_vocab = text_helper.VocabDict('./Data/vocab_answers.txt')   # the question vocabulary built by base-vqa project
    qst = question.lower().split()
    qst2idc = np.array([qst_vocab.word2idx('<pad>')] * 30)
    qst2idc[:len(qst)] = [qst_vocab.word2idx(w) for w in qst]
    qst2idc = qst2idc.reshape(1,30)

    checkpoint = torch.load('./model/model-epoch-30.ckpt')          # the checkpoint file saved by base-vqa project
    model = VqaModel(
        embed_size=1024,
        qst_vocab_size=qst_vocab.vocab_size,
        ans_vocab_size=ans_vocab.vocab_size,
        word_embed_size=300,
        num_layers=2,
        hidden_size=512)
    model.load_state_dict(checkpoint['state_dict'])
    model_ = model.to(device)
    model_.eval()
    torch.no_grad()
    img_ = image.to(device)
    qst_ = torch.from_numpy(qst2idc).to(device)

    output = model_(img_,qst_)
    _, pred = torch.max(output, 1)
    index = pred.item()
    ans = ans_vocab.idx2word(index)
    print(ans)

    # these commends are for show the top five possible answers
    # _, pred = torch.sort(output,1,True)
    # index_arr = pred.cpu().detach().numpy()
    # pos_ans = index_arr[0][0:5]
    # ans = ''
    # for idx in pos_ans:
        # ans = ans + ' ' + ans_vocab.idx2word(idx)
    # print(ans)

    plt.figure("test_pic")
    plt.imshow(img)
    plt.show()

class inf():
    def __init__(self,phase, epoch,loss, acc1, acc2):
        self.phase = phase
        self.epoch = epoch
        self.loss = loss
        self.acc_exp1 = acc1
        self.acc_exp2 = acc2

    def __str__(self):
        return self.phase+' '+self.epoch+' '+self.loss+' '+self.acc_exp1+' '+self.acc_exp2


# check_output function is for checking loss and accuarcy
def check_output():
    inf_list = []
    for i in range(30):
        for phase in ['train', 'valid']:
            with open(os.path.join('.\logs', '{}-log-epoch-{:02}.txt').format(phase, i+1), 'r') as f:
                line = f.readline()
                words = line.split()
                information = inf(phase,words[0],words[1],words[2],words[3])
                inf_list.append(information)
    loss_list_t = []
    loss_list_v = []
    acc1_list_t = []
    acc1_list_v = []
    acc2_list_t = []
    acc2_list_v = []
    epoch = np.arange(1,31)
    for i in range(60):
        if inf_list[i].phase=='train':
            loss_list_t.append(round(float(inf_list[i].loss),4))
            acc1_list_t.append(round(float(inf_list[i].acc_exp1),4))
            acc2_list_t.append(round(float(inf_list[i].acc_exp2),4))
        if inf_list[i].phase=='valid':
            loss_list_v.append(round(float(inf_list[i].loss),4))
            acc1_list_v.append(round(float(inf_list[i].acc_exp1),4))
            acc2_list_v.append(round(float(inf_list[i].acc_exp2),4))
    
    fig = plt.figure(1)
    ax1 = plt.subplot(2,2,1)
    plt.plot(epoch,loss_list_t,label='train')
    plt.plot(epoch,loss_list_v,label='valid')
    ax2 = plt.subplot(2,2,3)
    plt.plot(epoch,acc1_list_t)
    plt.plot(epoch,acc1_list_v)
    ax3 = plt.subplot(2,2,4)
    plt.plot(epoch,acc2_list_t)
    plt.plot(epoch,acc2_list_v)
    fig.legend()
    plt.show()

if __name__=='__main__':
    predict('./Data/test.jpg','what is in the picture ?')
    predict('./Data/test_searched_pic.jpg','what is in the picture ?')
    predict('./Data/test_elephant.jpg','what is in the picture ?')
    # check_output()
