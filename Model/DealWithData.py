#! -*- coding:utf-8 -*-
import json
import csv
import pdb
import time
import os
import re

label_list = ['O', 'B-LAB', 'I-LAB', 'B-RAY', 'I-RAY', 'B-OPE', 'I-OPE', 'B-DIS', 'I-DIS', 'B-MED',
              'I-MED', 'B-ANA', 'I-ANA']

def PreProcessData(path):
    sentences = []
    tags = []
    with open(path, encoding="utf-8") as data_file:
        for sentence in data_file.read().strip().split('\n\n'):
            if sentence is '' or sentence is '\n':
                continue
            if len(sentence) >(256*3):  # 网络最长接受 256
                shorter_sentences = sentence.split('， O')
            else:
                shorter_sentences = [sentence]
            for sentence in shorter_sentences:
                _sentence = ""
                tag = []
                if sentence is '' or sentence is '\n':
                    continue
                words = sentence.strip().split('\n')
                if '，' in words[0]:  # 数据清洗
                    words = words[1:]
                i = 0
                words_num = len(words)
                while i < words_num:
                    word = words[i]
                    if len(word) >= 3:
                        if word[2:] not in label_list:  # 数据清洗，处理'\n  tag'的数据
                            i += 1
                            _sentence += words[i][0]
                            tag.append(word)
                        else:
                            _sentence += word[0]
                            tag.append(word[2:])
                    i += 1
                if(len(_sentence)>2):  # 数据清洗
                    sentences.append(_sentence)
                    tags.append(tag)
    data = (sentences, tags)
    return data


def GenerateData(json_path, train_path, validate_path, only_period):
    datas = ["", ""]  # first for training data, second for validate data
    tag_map = {'疾病和诊断': 4, '影像检查': 2, '实验室检验': 1, '药物': 5, '手术': 3, '解剖部位': 6}
    _max_sentence = 0
    num = 0
    count = 0
    if only_period:
        split_sig = ['。']
    else:
        split_sig = ['。', '，', ',', '.']
    with open(json_path, encoding='utf-8') as f:
        for line in f:  # every line is a json object
            start_sentence = 0
            sentence_cur = 0
            ini_pos = 0
            count += 1
            element = json.loads(line, encoding='utf-8')
            entities = element['entities']  # entity array
            original_text = element['originalText']
            if count <= 300:
                choose_index = 0
            else:
                choose_index = 1
            for entity in entities:
                start_pos = entity['start_pos']
                end_pos = entity['end_pos']
                tag = tag_map[entity['label_type']]
                for i in range(ini_pos, start_pos):
                    sentence_cur += 1
                    if original_text[i] == ' ' or original_text[i] == '\t':
                        if datas[choose_index][-1] != '\n':
                            datas[choose_index] += '\n'
                        continue
                    datas[choose_index] += original_text[i]
                    datas[choose_index] += ' O\n'
                    if original_text[i] in split_sig:
                        datas[choose_index] += '\n'
                        if sentence_cur - start_sentence >= 256:
                            num += 1
                            _max_sentence = sentence_cur - start_sentence
                            print(_max_sentence)
                            print(original_text[start_sentence:sentence_cur])
                        start_sentence = sentence_cur
                datas[choose_index] += original_text[start_pos]
                datas[choose_index] += ' '
                datas[choose_index] += label_list[2 * tag - 1]
                datas[choose_index] += '\n'
                tmpstr = ' ' + label_list[2 * tag] + '\n'
                sentence_cur += 1
                for i in range(start_pos + 1, end_pos):
                    if original_text[i] == ' ' or original_text[i] == '\t':
                        continue
                    datas[choose_index] += original_text[i]
                    datas[choose_index] += tmpstr
                    sentence_cur += 1
                ini_pos = end_pos
            # append remaining data
            for i in range(ini_pos, len(original_text)):
                if original_text[i] == ' ' or original_text[i] == '\t':
                    if datas[choose_index][-1] != '\n':
                        datas[choose_index] += '\n'
                    continue
                datas[choose_index] += original_text[i]
                datas[choose_index] += ' O\n'
                if original_text[i] in split_sig:
                    datas[choose_index] += '\n'
                    if sentence_cur - start_sentence >= 256:
                        num += 1
                        _max_sentence = sentence_cur - start_sentence
                        print(_max_sentence)
                        print(original_text[start_sentence:sentence_cur])
                    start_sentence = sentence_cur
    with open(train_path, encoding='utf-8', mode='w') as f:
        f.write(datas[0])
    with open(validate_path, encoding='utf-8', mode='w') as f:
        f.write(datas[1])
    print("num: ", num)
    return _max_sentence


def MySplit(s, delimiters, start=0):
    last_pos = start
    cur_pos = start
    res = []
    while(s[last_pos] in ['，', '。', ',', '.', ';', '；']):
        last_pos += 1
        cur_pos += 1
    length = len(s)
    while cur_pos < length:
        if s[cur_pos] in delimiters:
            if cur_pos > last_pos:
                if (cur_pos + 1 - last_pos) > 255:
                    temp_res = MySplit(s[:cur_pos+1], ['，', '。', ',', '.', ';', '；'], last_pos)
                    res.extend(temp_res)
                else:
                    res.append((s[last_pos:cur_pos+1], last_pos))
            last_pos = cur_pos + 1
            while(last_pos < length and s[last_pos] in ['，', '。', ',', '.', ';', '；']):
                last_pos += 1
                cur_pos += 1
        cur_pos += 1
    return res

def fmt_time(dtime):
    if dtime <= 0:
        return '0:00.000'
    elif dtime < 60:
        return '0:%02d.%03d' % (int(dtime), int(dtime * 1000) % 1000)
    elif dtime < 3600:
        return '%d:%02d.%03d' % (int(dtime / 60), int(dtime) % 60, int(dtime * 1000) % 1000)
    else:
        return '%d:%02d:%02d.%03d' % (int(dtime / 3600), int((dtime % 3600) / 60), int(dtime) % 60,
                                      int(dtime * 1000) % 1000)


def GenerateSubmit(model, test_path, submit_path):
    print('Start Generate Submit')
    label_map = {'B-LAB': '实验室检验', 'I-LAB': '实验室检验', 'B-RAY': '影像检查', 'I-RAY': '影像检查',
                 'B-OPE': '手术', 'I-OPE': '手术', 'B-DIS': '疾病和诊断', 'I-DIS': '疾病和诊断',
                 'B-MED': '药物', 'I-MED': '药物', 'B-ANA': '解剖部位', 'I-ANA': '解剖部位'}
    with open(test_path, encoding='utf-8', mode='r') as reader:
        with open(submit_path, encoding='utf-8', mode='w', newline='') as writer:
            csv_writer = csv.writer(writer)
            csv_writer.writerow(['textId', 'label_type', 'start_pos', 'end_pos'])
            count = 0
            time_start = time.time()
            for line in reader:
                count += 1
                # if count == 2:
                #   break
                elapsed = time.time() - time_start
                eta = elapsed / count * (600-count)
                print('[%d/600] Elapsed: %s, ETA>> %s' % 
                        (count, fmt_time(elapsed), fmt_time(eta)))
                test_element = json.loads(line, encoding='utf-8')
                original_text = test_element['originalText']
                text_id = test_element['textId']
                sentences_with_index = MySplit(original_text, ['。'])
                for sentence in sentences_with_index:
                    # if len(sentence[0]) > 255:
                    #     print('%d is too long for mdoel, original sentence: %s' % (len(sentence[0]), sentence[0]))
                    # print(sentence[0])
                    tags = model.ModelPredict(sentence[0])
                    # print(tags)
                    i = 0
                    while i < len(tags):
                        if tags[i] == 'O':
                            i += 1
                            continue
                        j = i
                        label = label_map[tags[i]]
                        j += 1
                        while j < len(tags) and tags[j] != 'O' and tags[j][2:] == tags[i][2:] and tags[j][0] != 'B':
                            j += 1
                        # if tags[i][0] == 'I':
                        #     start_pos = sentence[1] + i - 1
                        # else:
                        start_pos = sentence[1] + i
                        end_pos = sentence[1] + j
                        csv_writer.writerow([text_id, label, start_pos, end_pos])
                        i = j

# test GenerateData
if __name__ == '__main__':
    json_path = '../Data/train.json'
    only_period = True
    train_path = '../Data/train.txt'
    validate_path = '../Data/validate.txt'
    max_length = GenerateData(json_path, train_path, validate_path, only_period)
    print(max_length)
