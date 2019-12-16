# 用于 WEB_INFO 课程实验 2 的 keras_bert_ner

[Orginal source](https://github.com/UmasouTTT/keras_bert_ner)  
基于keras和keras_bert的中文命名实体识别，搭建的网络为bert+bilstm_crf
运行main函数即可训练并使用模型

## Dpendencies

+ use `pip install -r requirements.txt` to install python dependencies
+ 需要下载中文预训练模型[chinese_L-12_H-768_A-12](https://storage.googleapis.com/bert_models/2018_11_03/chinese_L-12_H-768_A-12.zip)放到Parameter文件夹下

## 排查可能的疏漏

- [x] 训练数据的格式化问题
- [x] 预测时句子分割时的句子开始位置保存(分割之后存为tuple[stnce_str,start_pos])，已确定对齐
  - [x] 需要再分割的长句也修复了，并测试了 `textId=531` 样例的分割对齐和 csv 输出对齐
- [x] 在 Predict 函数外加载参数也可行，而且会加快运行
