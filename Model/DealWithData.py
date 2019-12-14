#! -*- coding:utf-8 -*-
import json


def PreProcessData(path):
    sentences = []
    tags = []
    with open(path, encoding="utf-8") as data_file:
        for sentence in data_file.read().strip().split('\n\n'):
            _sentence = ""
            tag = []
            for word in sentence.strip().split('\n'):
                content = word.strip().split()
                _sentence += content[0]
                tag.append(content[1])
            sentences.append(_sentence)
            tags.append(tag)
    data = (sentences, tags)
    return data


def GenerateData(json_path, train_path, validate_path):
    datas = ["", ""]  # first for training data, second for validate data
    tag_map = {'疾病和诊断': 4, '影像检查': 2, '实验室检验': 1, '药物': 5, '手术': 3, '解剖部位': 6}
    _max_sentence = 0
    num = 0
    label_list = ['O','B-LAB', 'I-LAB', 'B-RAY', 'I-RAY', 'B-OPE', 'I-OPE', 'B-DIS', 'I-DIS', 'B-MED',
                  'I-MED', 'B-ANA', 'I-ANA']
    count = 0
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
                        datas[choose_index] += '\n'
                        continue
                    datas[choose_index] += original_text[i]
                    datas[choose_index] += ' O\n'
                    if original_text[i] == '。' or original_text[i] == '，' or original_text[i] == ',' or original_text[i] == '.':
                        datas[choose_index] += '\n'
                        if sentence_cur - start_sentence >= 80:
                            num += 1
                            _max_sentence = sentence_cur - start_sentence
                            print(_max_sentence)
                            print(original_text[start_sentence:sentence_cur])
                        start_sentence = sentence_cur
                datas[choose_index] += original_text[start_pos]
                datas[choose_index] += ' '
                datas[choose_index] += label_list[2*tag-1]
                datas[choose_index] += '\n'
                tmpstr = ' ' + label_list[2*tag] + '\n'
                sentence_cur += 1
                for i in range(start_pos+1, end_pos):
                    datas[choose_index] += original_text[i]
                    datas[choose_index] += tmpstr
                    sentence_cur += 1
                ini_pos = end_pos
            # append remaining data
            for i in range(ini_pos, len(original_text)):
                if original_text[i] == ' ' or original_text[i] == '\t':
                    datas[choose_index] += '\n'
                    continue
                datas[choose_index] += original_text[i]
                datas[choose_index] += ' O\n'
                if original_text[i] == '。' or original_text[i] == '，'or original_text[i] == ',' or original_text[i] == '.':
                    datas[choose_index] += '\n'
                    if sentence_cur - start_sentence >= 80:
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


# test GenerateData
if __name__ == '__main__':
    max_sentence = GenerateData('../Data/train.json', '../Data/train.txt', '../Data/validate.txt')
    print(max_sentence)



