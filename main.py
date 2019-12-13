from Model.BertBilstmCrf import bert_bilstm_crf
from Model import DealWithData
import json


if __name__ == "__main__":
    in_web = True
    # 数据
    if not in_web:
        train_path = "./Data/train1.txt"
        test_path = "./Data/test.txt"
        train_data = DealWithData.PreProcessData(train_path)
        test_data = DealWithData.PreProcessData(test_path)
    else:
        train_path = "./Data/train.json"
        test_path = "./Data/test.json"
        train_data = []
        test_data = []
        with open(train_path, "r", encoding="utf-8") as f:
            sentence_data = []
            label_data = []
            for line in f.readlines():
                dic = json.loads(line)
                sentences = dic['originalText'].split('。')
                sentence_data.extend(sentences)
                train_data.append(dic)
        with open(test_path, "r", encoding="utf-8") as f:
            for line in f.readlines():
                dic = json.loads(line)
                test_data.append(dic)

    # 模型
    max_seq_length = 80
    batch_size = 24
    epochs = 100
    lstmDim = 64
    model = bert_bilstm_crf(max_seq_length, batch_size, epochs, lstmDim)
    model.TrainModel(train_data, test_data)

    # 测试
    while 1:
        sentence = input('please input sentence:\n')
        tag = model.ModelPredict(sentence)
        print(tag)
