import json

if __name__ == "__main__":
    train_input_path = "./Data/train.json"
    test_input_path = "./Data/test.json"
    train_output_path = "./Data/train2.txt"
    test_output_path = "./Data/test2.txt"
    train_data = []
    test_data = []
    with open(train_input_path, "r", encoding="utf-8") as inf and open(train_output_path, "w", encoding="utf-8") as outf:
        for line in inf.readlines():
            dic = json.loads(line)
            content = dic['originalText']
            entities = dic['entities']
            label = ['O' for i in range(5)]
            for entity in entities:
                