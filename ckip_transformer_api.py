from ckip_transformers.nlp import CkipNerChunker
from pprint import pprint


def load_ner_driver(model_name="bert-base"):
    # 幫你下載 or 讀取模型
    ner_driver = CkipNerChunker(model=model_name)
    return ner_driver


def get_ner(ner_driver, text):
    ner = ner_driver([text])

    result = list()
    for entity in ner[0]:
        result.append((entity.word, entity.ner))

    # comprehension
    # result = [
    # (entity.word, entity.ner) for entity in ner[0]
    # ]

    return result


if __name__ == '__main__':
    text = "您好，我是來自台中的一位。曾在台中的ABC公司和XYZ組織擔任過不同的職位，從中獲得豐富的工作經驗與專業知識。對這個城市充滿熱情與認同，期待能夠繼續在台中這塊土地上發展並為地方社區與組織帶來更多正面影響。"

    driver = load_ner_driver()
    result = get_ner(driver, text)

    print(result)
