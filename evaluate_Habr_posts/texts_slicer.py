import os
import io

path = "D:/repos/TEXTS_ml/"
import re
import nltk.tokenize as tok
import nltk
import re
import pandas as pd
# nltk.download()

class File_Slicer():

    def __init__(self):
        self.tokenizer = nltk.data.load('tokenizers/punkt/russian.pickle')

    def count_par(self, pth):
        for filename in os.listdir(pth):
            with open(os.path.join(pth, filename), 'r', encoding='utf8') as f:

                paragraphcount = 1
                empty = True
                for i in f:
                    if '\n' in i:
                        # linecount += 1
                        if len(i) < 2:
                            empty = True
                        elif len(i) > 2 and empty is True:
                            paragraphcount = paragraphcount + 1
                            empty = False

            print(filename, "N: ", paragraphcount)
            f.close()


    def slice_paragr(self, pth):
        for filename in os.listdir(path):
            with open(os.path.join(path, filename), 'r', encoding='utf8') as f:
                txt = f.read()
                splat = txt.split("\n\n")
                splat2 = []
                for sp in splat:
                    sp = sp.replace("\n", "")
                    splat2.append(sp)
                array1 = splat2[:int(len(splat2) / 5)]
                array2 = splat2[int(len(splat2) / 5):int(len(splat2) / 5 * 2)]
                array3 = splat2[int(len(splat2) / 5 * 2):int(len(splat2) / 5 * 3)]
                array4 = splat2[int(len(splat2) / 5 * 3):int(len(splat2) / 5 * 4)]
                array5 = splat2[int(len(splat2) / 5 * 4):int(len(splat2))]

            with open('D:/repos/mining_texts_ML_split/{}_part_{}'.format(1, filename), 'w', encoding='utf8') as output:
                for item in array1:
                    output.write("%s\n" % item)
            output.close()
            with open('D:/repos/mining_texts_ML_split/{}_part_{}'.format(2, filename), 'w', encoding='utf8') as output:
                for item in array2:
                    output.write("%s\n" % item)
            output.close()
            with open('D:/repos/mining_texts_ML_split/{}_part_{}'.format(3, filename), 'w', encoding='utf8') as output:
                for item in array3:
                    output.write("%s\n" % item)
            output.close()
            with open('D:/repos/mining_texts_ML_split/{}_part_{}'.format(4, filename), 'w', encoding='utf8') as output:
                for item in array4:
                    output.write("%s\n" % item)
            output.close()
            with open('D:/repos/mining_texts_ML_split/{}_part_{}'.format(5, filename), 'w', encoding='utf8') as output:
                for item in array5:
                    output.write("%s\n" % item)
            output.close()

    def slice_sentences(self,pth):

        for filename in os.listdir(path):
            with open(os.path.join(path, filename), 'r', encoding='utf8') as f:
                txt = f.read()

                txt = self.tokenizer.tokenize(txt)
                splat2 = []
                for sp in txt:
                    sp = sp.replace("\n", "")
                    splat2.append(sp)
                array1 = splat2[:int(len(splat2) / 5)]
                array2 = splat2[int(len(splat2) / 5):int(len(splat2) / 5 * 2)]
                array3 = splat2[int(len(splat2) / 5 * 2):int(len(splat2) / 5 * 3)]
                array4 = splat2[int(len(splat2) / 5 * 3):int(len(splat2) / 5 * 4)]
                array5 = splat2[int(len(splat2) / 5 * 4):int(len(splat2))]
            with open('D:/repos/TEXTS_ml_SPLIT/{}_part_{}'.format(1, filename), 'w', encoding='utf8') as output:
                for item in array1:
                    output.write("%s\n" % item)
            output.close()
            with open('D:/repos/TEXTS_ml_SPLIT/{}_part_{}'.format(2, filename), 'w', encoding='utf8') as output:
                for item in array2:
                    output.write("%s\n" % item)
            output.close()
            with open('D:/repos/TEXTS_ml_SPLIT/{}_part_{}'.format(3, filename), 'w', encoding='utf8') as output:
                for item in array3:
                    output.write("%s\n" % item)
            output.close()
            with open('D:/repos/TEXTS_ml_SPLIT/{}_part_{}'.format(4, filename), 'w', encoding='utf8') as output:
                for item in array4:
                    output.write("%s\n" % item)
            output.close()
            with open('D:/repos/TEXTS_ml_SPLIT/{}_part_{}'.format(5, filename), 'w', encoding='utf8') as output:
                for item in array5:
                    output.write("%s\n" % item)
            output.close()

    def clean_tabs(self,path):
        for filename in os.listdir(path):
            with open(os.path.join(path, filename), 'r+', encoding='utf8') as f:
                txt = f.read()
                # Removes all blank lines
                txt = re.sub(r'\n\s*\n', '\n', txt)
                # Adds two blanks between all paragraphs
                txt = re.sub(r'\n', '\n\n\n', txt)
                # Removes the blank lines from the EOF
                txt = re.sub(r'\n*\Z', '', txt)
                f.close()
            # Writes to file and closes
            with open(os.path.join(path, filename), 'w', encoding='utf8') as fo:
                # fo = open('D:/repos/mining_texts/blank{}.txt'.format(237), 'w',encoding='utf8')
                fo.write(txt)
                fo.close()

    def get_mark_word_list(self,path):
        result = []
        for filename in os.listdir(path):
            with open(os.path.join(path, filename), 'r+', encoding='utf8') as f:
                sy = f.read().split()
                sign = self.mysplit(sy[-1])
                if sign[0] == '+':
                    mark = int(sign[1])
                else:
                    mark = - int(sign[1])
                l = [filename[:-4], mark]
                result.append(l)
        return result


    def mysplit(self,s):
        head = s.rstrip('0123456789')
        tail = s[len(head):]
        return head, tail


if __name__ == "__main__":

    file_sl=File_Slicer()

    ls = file_sl.get_mark_word_list(path)

    df = pd.DataFrame(ls)
    df.columns = ['File', 'Mark']
    df.to_csv('D:/repos/files_marks.csv',index=False)

