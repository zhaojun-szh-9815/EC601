import numpy as np
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from PIL import Image
import text_helper
from medical_models import VqaModel

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
transform = {transforms.Compose([transforms.ToTensor(),transforms.Normalize((0.2539457, 0.2538943, 0.25384054),(0.048477963, 0.048473958, 0.04845482))])}

PIC_SIZE = [224, 224]

def predict(image_name, question):

    img = Image.open('./Resize_img/' + image_name)
    image = img.resize(PIC_SIZE, Image.ANTIALIAS)
    image = image.convert('RGB')
    for trans in transform:
        image = trans(image)
    image = image.view(1,3,224,224)
    
    qst_vocab = text_helper.VocabDict('./Data/medical_questions_vocab.txt')
    ans_vocab = text_helper.VocabDict('./Data/medical_answers_vocab.txt')
    qst = question.lower().split()
    qst2idc = np.array([qst_vocab.word2idx('<pad>')] * 30)
    qst2idc[:len(qst)] = [qst_vocab.word2idx(w) for w in qst]
    qst2idc = qst2idc.reshape(1,30)

    checkpoint = torch.load('./models/model-epoch-10.ckpt')
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

    v, pred = torch.sort(output,1,True)
    index_arr = pred.cpu().detach().numpy()
    value_arr = v.cpu().detach().numpy()
    print('image:'.ljust(15),image_name)
    print('question:'.ljust(15), question)
    print('answers'.ljust(40),'possibility')
    for i in range(5):
        print(ans_vocab.idx2word(index_arr[0][i]).ljust(40),value_arr[0][i])
    print('\n')

class inf():
    def __init__(self,phase, epoch,loss, acc1, acc2):
        self.phase = phase
        self.epoch = epoch
        self.loss = loss
        self.acc_exp1 = acc1
        self.acc_exp2 = acc2

    def __str__(self):
        return self.phase+' '+self.epoch+' '+self.loss+' '+self.acc_exp1+' '+self.acc_exp2

def check_output():
    inf_list = []
    epoch = 20
    for i in range(epoch):
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
    for i in range(epoch * 2):
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
    plt.plot(range(epoch),loss_list_t,label='train')
    plt.plot(range(epoch),loss_list_v,label='valid')
    ax2 = plt.subplot(2,2,3)
    plt.plot(range(epoch),acc1_list_t)
    plt.plot(range(epoch),acc1_list_v)
    ax3 = plt.subplot(2,2,4)
    plt.plot(range(epoch),acc2_list_t)
    plt.plot(range(epoch),acc2_list_v)
    fig.legend()
    plt.show()

if __name__ == '__main__':

    #check_output()
    # qid: 17
    predict('synpic27142.jpg','What organ system is pictured ?')
    predict('synpic19114.jpg','What organ system is pictured ?')
    # qid: 24
    predict('synpic27142.jpg','Is this the brain ?')
    predict('synpic27142.jpg','Is this the chest ?')
    predict('synpic27142.jpg','Is brain pictured ?')
    predict('synpic27142.jpg','Is chest pictured ?')

    predict('synpic27142.jpg','Is the heart enlarged ?')
    predict('synpic27142.jpg','Is this an MRI ?')
    predict('synpic19114.jpg','Is this an MRI ?')
    # qid: 16
    predict('synpic27142.jpg','What type of imaging is this ?')
    predict('synpic19114.jpg','What type of imaging is this ?')