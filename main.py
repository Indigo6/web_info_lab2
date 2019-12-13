from Model.BertBilstmCrf import bert_bilstm_crf
from Model import DealWithData
import json


if __name__ == "__main__":
    in_web = False
    # 数据
    if not in_web:
        train_path = "./Data/train1.txt"
        test_path = "./Data/test.txt"
    else:
        train_path = "./Data/train2.txt"
        test_path = "./Data/test2.txt"
    train_data = DealWithData.PreProcessData(train_path)
    test_data = DealWithData.PreProcessData(test_path)

    # 模型
    max_seq_length = 80
    batch_size = 24
    epochs = 1
    lstmDim = 64
    model = bert_bilstm_crf(max_seq_length, batch_size, epochs, lstmDim)
    model.TrainModel(train_data, test_data)

    # 测试
    while 1:
        sentence = input('please input sentence:\n')
        tag = model.ModelPredict(sentence)
        print(tag)
