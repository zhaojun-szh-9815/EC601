import json
import urllib.request
import os
import re
import numpy as np
from tqdm import trange
from collections import defaultdict
from PIL import Image
import text_helper

SAVE_PATH = './img'
RESIZE_PATH = './Resize_img'
DATA_PATH = './Data'
DATASET = './VQA_RAD Dataset Public.json'
PIC_SIZE = [224, 224]

# save pictures from json
def save_pic():
    j = open(DATASET)
    info = json.load(j)
    unable_link = []
    for i in trange(len(info)):
        tag = download_image(info[i]['image_name'],info[i]['image_case_url'])
        if tag == 0:
            unable_link.append(i)
    print("\nUnable links: ",unable_link) # [584, 992, 1351, 1376, 1394, 1406, 1407, 1414, 1415, 1725, 1972]

# download by url
def download_image(name, url):
    if not os.path.exists(SAVE_PATH):
        os.mkdir(SAVE_PATH)
    request = urllib.request.Request(url)
    request.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36')
    try:
        response = urllib.request.urlopen(url)
    except urllib.error.HTTPError as e:
        # print("status code", e.code)
        # print("reson", e.reason)
        # print("header", e.headers)
        return 0
    buf = response.read()
    buf = str(buf, encoding='utf-8')
    listurl = re.findall(r'http.+\.jpg', buf)

    req = urllib.request.urlopen(listurl[0])
    buf = req.read()
    if not os.path.exists(SAVE_PATH + '/' + name):
        with open(SAVE_PATH + '/' + name, 'wb') as f:
            f.write(buf)
    return 1

# make dictionary for question tokens
def make_question_vocabulary():
    vocab_set = set()
    SENTENCE_SPLIT_REGEX = re.compile(r'(\W+)')
    question_length = []
    j = open(DATASET)
    info = json.load(j)
    set_question_length = [None]*len(info)
    for i, infomation in enumerate(info):
        words = SENTENCE_SPLIT_REGEX.split(infomation['question'].lower())
        words = [w.strip() for w in words if len(w.strip()) > 0]
        vocab_set.update(words)
        set_question_length[i] = len(words)
    question_length += set_question_length

    vocab_list = list(vocab_set)
    vocab_list.sort()
    vocab_list.insert(0, '<pad>')
    vocab_list.insert(1, '<unk>')
    
    if not os.path.exists(DATA_PATH):
        os.mkdir(DATA_PATH)

    with open(DATA_PATH+'/medical_questions_vocab.txt', 'w') as f:
        f.writelines([w+'\n' for w in vocab_list])
    
    print('Make vocabulary for questions')
    print('The number of total words of questions: %d' % len(vocab_set))
    print('Maximum length of question: %d' % np.max(question_length))

# make dictionary for answers
def make_answer_vocabulary():
    answers = defaultdict(lambda: 0)
    j = open(DATASET)
    info = json.load(j)
    for information in info:
        word = information['answer']
        if type(word) == type('a'):
            word = word.lower()
        answers[word] += 1
                
    answers = sorted(answers, key=answers.get, reverse=True)
    assert('<unk>' not in answers)
    answers = ['<unk>'] + answers
    
    if not os.path.exists(DATA_PATH):
        os.mkdir(DATA_PATH)

    with open(DATA_PATH+'/medical_answers_vocab.txt', 'w') as f:
        f.writelines([str(w)+'\n' for w in answers])

    print('Make vocabulary for answers')
    print('The number of total words of answers: %d' % len(answers))

# resize the picture to [224, 224]
def resize_images():
    if not os.path.exists(RESIZE_PATH):
        os.mkdir(RESIZE_PATH)
    images = os.listdir(SAVE_PATH)
    failed_images = []

    for iimage, image in enumerate(images):
        try:
            with open(os.path.join(SAVE_PATH + '/', image), 'r+b') as f:
                with Image.open(f) as img:
                    # img = img.resize([min_edge,min_edge], Image.ANTIALIAS)
                    img = img.resize(PIC_SIZE, Image.ANTIALIAS)
                    img.save(os.path.join(RESIZE_PATH + '/', image), img.format)
        except(IOError, SyntaxError) as e:
            failed_images.append(iimage)

# build inputs
def build_medical_input():
    j = open(DATASET)
    info = json.load(j)
    dataset = [None]*len(info)
    for n_info, information in enumerate(info):
        image_name=information['image_name']
        image_path=os.path.join(RESIZE_PATH + '/', image_name)
        question_id=information['qid']
        question_str=information['question']
        question_tokens=text_helper.tokenize(question_str)
        all_answers = [str(information['answer'])]
        iminfo = dict(
            image_name = image_name,
            image_path = image_path,
            question_id = question_id,
            question_str = question_str,
            question_tokens = question_tokens,
            all_answers = all_answers,
            valid_answers = all_answers)

        dataset[n_info] = iminfo
    data_array = np.array(dataset)
    # np.savetxt("./med_input.txt",data_array, fmt='%s')
    length = len(data_array)
    train_arr = data_array
    valid_arr = data_array[int(length*0.9)+1:length]
    
    if not os.path.exists(DATA_PATH):
        os.mkdir(DATA_PATH)
    np.save(DATA_PATH+'/train.npy', train_arr)
    np.save(DATA_PATH+'/valid.npy', valid_arr)
    np.save(DATA_PATH+'/train_valid.npy', data_array)

# calculate normalization of these medical images
# mean = [0.2539457, 0.2538943, 0.25384054]
# std= [0.048477963, 0.048473958, 0.04845482]
def look_for_normalization():
    images = os.listdir(RESIZE_PATH)
    images_list = []
    for i, image in enumerate(images):
        img = Image.open(RESIZE_PATH + '/' +image).convert('RGB')
        transf = transforms.ToTensor()
        images_list.append(transf(img).numpy())
    images_array = np.array(images_list)
    images_array.resize(len(images),3,224*224)
    img_mean = np.mean(images_array,axis=0)
    img_std = np.std(images_array,axis=0)
    mean = [0,0,0]
    std = [0,0,0]
    for i in range(3):
        mean[i] = np.mean(img_mean[i],axis=0)
        std[i] = np.std(img_std[i],axis=0)
    print(mean, std, sep='\n')

if __name__ == '__main__':

    # save_pic()
    make_question_vocabulary()
    make_answer_vocabulary()
    resize_images()
    build_medical_input()
    # look_for_normalization()