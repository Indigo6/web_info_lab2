from Model.BertBilstmCrf import bert_bilstm_crf
from Model import DealWithData
import json


if __name__ == "__main__":
    in_web = True
    if_train = False
    # 数据
    if not in_web:
        train_path = "./Data/train1.txt"
        test_path = "./Data/test.txt"
    else:
        train_path = "./Data/train.txt"
        test_path = "./Data/validate.txt"
    if if_train:
        train_data = DealWithData.PreProcessData(train_path)
        test_data = DealWithData.PreProcessData(test_path)

    # 模型
    max_seq_length = 200
    batch_size = 24
    epochs = 1
    lstmDim = 64
    if in_web:
        label_path = './Parameter/tag_dict.txt'
    else:
        label_path = './Parameter/tag_dict2.txt'
    model = bert_bilstm_crf(max_seq_length, batch_size,
                            epochs, lstmDim, label_path)
    if if_train:
        model.TrainModel(train_data, test_data)

    # 测试
    if in_web:
        # tag2label = {}
        # Btags = []
        # B2Itags = {}
        # with open('./Parameter/tag2label2.txt', 'r', encoding='utf-8') as f:
        #     for line in f.readlines():
        #         line = line.encode('utf-8').decode('utf-8-sig')
        #         temp = line.strip().split()
        #         if 'B-' in temp[0]:
        #             Btags.append(temp[0])
        #             tag2label[temp[0]] = temp[1]
        #             B2Itags[temp[0]] = 'I-' + temp[0][2:]               

        # with open('./Data/test2.json', 'r', encoding='utf-8') as f:
        #     for line in f.readlines():
        #         dic = json.loads(line)
        #         result = {}
        #         result['textId'] = dic['textId']
        #         content = dic['originalText']
        #         sentences = content.split('。')
        #         sentence_begin = 0
        #         entities = []
        #         for sentence in sentences:
        #             sentence = sentence[:60]
        #             tag = model.ModelPredict(sentence)
        #             i = 0
        #             while i < len(tag):
        #                 if tag[i] in Btags:
        #                     Btag_temp = tag[i]
        #                     start_pos = sentence_begin + i
        #                     end_pos = sentence_begin + i
        #                     label_type = tag2label[Btag_temp]
        #                     i += 1
        #                     entity = {}
        #                     while(tag[i] == B2Itags[Btag_temp]):
        #                         end_pos += 1
        #                         i += 1
        #                     entity['label_type'] = label_type
        #                     entity['start_pos'] = start_pos
        #                     entity['end_pos'] = end_pos
        #                     entities.append(entity)
        #                 else:
        #                     i += 1
        #             sentence_begin += len(sentence)
        #         result['entities'] = entities
        while 1:
            sentence = input('please input sentence:\n')
            tag = model.ModelPredict(sentence)
            print(tag)
                
    else:
        while 1:
            sentence = input('please input sentence:\n')
            tag = model.ModelPredict(sentence)
            print(tag)
