from Model.BertBilstmCrf import bert_bilstm_crf
from Model import DealWithData
import json


if __name__ == "__main__":
    in_web = True
    if_train = False
    if_longer = True
    # 数据
    if not in_web:
        train_path = "./Data/train1.txt"
        test_path = "./Data/test.txt"
        if if_longer:
          save_model_path = 'keras_bert_200'
        else:
          save_model_path = 'keras_bert'
    else:
        train_path = "./Data/train.txt"
        test_path = "./Data/validate.txt"
        save_model_path = 'keras_bert_web'
    if if_train:
        train_data = DealWithData.PreProcessData(train_path)
        test_data = DealWithData.PreProcessData(test_path)

    # 模型
    if if_longer:
        max_seq_length = 256
    else:
        max_seq_length = 80
    batch_size = 24
    epochs = 10
    lstmDim = 64
    if in_web:
        label_path = './Parameter/tag_dict.txt'
    else:
        label_path = './Parameter/tag_dict2.txt'
    model = bert_bilstm_crf(max_seq_length, batch_size, epochs,
                 lstmDim, label_path, save_model_path)
    if if_train:
        model.TrainModel(train_data, test_data)

    # 测试
    sentence = input('please input sentence:\n')
    while sentence:
        tag = model.ModelPredict(sentence)
        print(tag)
        sentence = input('please input sentence:\n')
    if in_web:
        model = None
        DealWithData.GenerateSubmit(model,'./Data/test.json','./Data/submit.csv')
