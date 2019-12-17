# 用于 WEB_INFO 课程实验 2 的 keras_bert_ner

[Orginal source](https://github.com/UmasouTTT/keras_bert_ner)  
基于keras和keras_bert的中文命名实体识别，搭建的网络为bert+bilstm_crf
运行main函数即可训练并使用模型

## Dpendencies

+ use `pip install -r requirements.txt` to install python dependencies
+ 需要下载中文预训练模型 [chinese_L-12_H-768_A-12](https://storage.googleapis.com/bert_models/2018_11_03/chinese_L-12_H-768_A-12.zip) 放到Parameter文件夹下

## 数据处理与清洗

### 1. 输入格式化(将 json 内容转换成模型接受的 格式)



### 2. 一些数据处理

+ 尝试句子长度的影响，发现按 `'。'` 分句得到的句子长度分布过于分散，长的长达 300，短的不到 10

  + 最后采取训练时和预测时均按 `['，', '。', ',', '.', ';', '；']` 进行短分

+ 对句与句中间的冗余标点进行处理（因为看到预测错误的结果有很多把开头的标点符号也预测为实体的）

  + 输入处理

    ```python
    # Model/DealWithData
    trouble = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~！？｡＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘\'‛“”„‟…‧﹏.'
    
    # Model/DealWithData/PreProcessData
    while i < words_num and words[i][0] in trouble: # 数据清洗,去除句首多余标点符号
        i += 1
    ```

  + 预测处理

    ```python
    # Model/DealWithData/MySplit
    ···
    while(s[last_pos] in trouble): # 数据清洗,去除句首多余标点符号
        last_pos += 1
        cur_pos += 1
    ```

+ 对于`' 胃癌'` 类样本的处理
  
  ```python
  # Model/DealWithData
  label_list = ['O', 'B-LAB', 'I-LAB', 'B-RAY', 'I-RAY', 'B-OPE', 'I-OPE', 'B-DIS', 'I-DIS', 'B-MED',
                'I-MED', 'B-ANA', 'I-ANA']
  
  # Model/DealWithData
  # word类似于 '胃 B-ANA'，要处理的是'  tag' 型数据
  if word[2:] not in label_list:  # 数据清洗，处理'\n  tag'的数据
      i += 1
      _sentence += words[i][0]	# 将输入数据记录为下一个word的输入
      tag.append(word)			# 将结果(tag)数据记录为当前word的tag
  ```

## 模型

采用 [Orginal source](https://github.com/UmasouTTT/keras_bert_ner)  提供的开源代码作为主要的框架，模型结构为 BERT + Bi-LSTM + CRF，具体参数如下

```python
__________________________________________________________________________________________________
Layer (type)                    Output Shape         Param #     Connected to                     
==================================================================================================
input_1 (InputLayer)            (None, None)         0                                            
__________________________________________________________________________________________________
input_2 (InputLayer)            (None, None)         0                                            
__________________________________________________________________________________________________
model_2 (Google_bert)                 multiple             101480448   input_1[0][0]                    
                                                                 input_2[0][0]                    
__________________________________________________________________________________________________
bidirectional_lstm (Bidirectional) (None, None, 128)    426496      model_2[1][0]                    
__________________________________________________________________________________________________
crf_1 (CRF)                     (None, None, 13)     1872        bidirectional_1[0][0]            
==================================================================================================
Total params: 101,908,816
Trainable params: 101,908,816
Non-trainable params: 0
```

在 Colab 上使用 `Tesla K80 GPU`  训练 

## 测试样例

+ 单句测试

  ```python
  患者因“直肠癌放疗后”于2017-2-22在全麻上行腹腔镜辅助直肠癌低位前切除
  ['O', 'O', 'O', 'O', 'B-DIS', 'I-DIS', 'I-DIS', 'O', 'O', 'I-DIS', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'B-OPE', 'I-OPE', 'I-OPE', 'I-OPE', 'I-OPE', 'I-OPE', 'I-OPE', 'I-OPE', 'I-OPE', 'O', 'O', 'O']
  ```

+ 运行 main.py, 调用 Mdeol/DealWithData/GenerateSubmit 会产生 submit.csv，并同时产生如下的 test_submit.csv

  ```python
  287,解剖部位,423,426,咽鼻咽
  287,影像检查,440,441,颈
  287,影像检查,441,445,部淋巴结
  287,手术,444,447,结穿刺
  287,影像检查,492,495,，超：
  287,解剖部位,495,502,右颈根至锁骨下
  287,解剖部位,503,507,发淋巴结
  287,解剖部位,515,517,腹盆
  287,影像检查,517,520,，CT
  288,手术,37,49,腔镜右半结肠切除术+DI
  288,解剖部位,62,67,降结肠中段
  288,解剖部位,83,86,腹盆腔
  288,解剖部位,87,88,肝
  288,解剖部位,99,101,左肝
  288,疾病和诊断,126,127,（
  288,疾病和诊断,127,141,降结肠大体）中至低分化腺癌，
  288,解剖部位,149,150,肠
  288,疾病和诊断,176,186,息肉管状-绒毛状腺瘤
  288,疾病和诊断,259,267,降结肠癌伴肝转移
  ```

## 排查可能的疏漏

- [x] 训练数据的格式化问题
- [x] 预测时句子分割时的句子开始位置保存(分割之后存为tuple[stnce_str,start_pos])，已确定对齐
  - [x] 需要再分割的长句也修复了，并测试了 `textId=531` 样例的分割对齐和 csv 输出对齐
- [x] 在 Predict 函数外加载参数也可行，而且会加快运行