from Cut import *
class RunCut:
    def __init__(self):
        pass

    def inputOutTxt(self, inputfile, outputfile):
        cut = Cut(3)
        inf = open(inputfile, 'r', encoding='UTF-8')
        outf = open(outputfile, 'w', encoding='UTF-8')

        for row in inf:
            row = row.strip('\n')
            print(row)
            temp1 = cut.maxMatch(row) # 正向最大匹配法分词
            temp2 = cut.reMaxMatch(row) # 逆向最大匹配法分词
            temp3 = cut.maxP(row) # 最大概率分词
            outf.write(row+'\n'+'正向最大匹配法分词：'+temp1+'\n'+'逆向最大匹配法分词：'+temp2+'\n'+'最大概率分词：'+temp3+'\n\n')
            # outf.write(temp2+'\n') # 导出一种分词方法的结果到txt文件

if __name__ == '__main__':
    runCut = RunCut()
    runCut.inputOutTxt('./corpus/test.txt', './corpus/output.txt')

