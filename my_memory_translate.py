
from translate import Translator
import pickle

BASE_URL = 'https://dict.youdao.com/w/'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
}
SKIP_WORDS = ['the', 'of', 'that', 'this', 'to']


def load_dict():
    try:
        with open('./my_memory_dict.pkl', 'rb') as f:
            youdao_dict = pickle.load(f)
    except Exception as e:
        print('Translation cache not found, creating a new one.')
        youdao_dict = {}
    return youdao_dict


def save_dict(youdao_dict):
    with open('./my_memory_dict.pkl', 'wb') as f:
        pickle.dump(youdao_dict, f)


def get_cn(en):
    youdao_dict = load_dict()
    if en in youdao_dict:
        return youdao_dict[en]

    # 翻译
    translator = Translator(from_lang="english", to_lang="chinese")
    result = translator.translate(en)

    youdao_dict[en] = result
    save_dict(youdao_dict)

    return result


if __name__ == '__main__':
    test_cases = ['Additional Operation',
                  'Apple',
                  'I wan to eat chicken',
                  'Target Issue Size'
                  ]
    for each in test_cases:
        print("""Test Case: {0}, Output: {1}.""".format(each, str(get_cn(each))))
