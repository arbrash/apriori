import itertools

class Apriori:
    def __init__(self, min_sup, dataDic = {}): #Initialization,set the Min.support
        self.data = dataDic
        self.size = len(dataDic)
        self.min_sup = min_sup
        self.min_sup_val = min_sup * self.size

    def find_frequent_1_itemsets(self):
        FreqDic = {}
        for itemset in self.data:
            for item in self.data[itemset]:
                if item in FreqDic:
                    FreqDic[item] += 1
                else:
                    FreqDic[item] = 1
        #print 'Scan:', FreqDic
        L1 = [] #store itemsets
        L2 = [] #store frequent
        for itemset in FreqDic:
            if FreqDic[itemset] >= self.min_sup_val:
                L1.append([itemset])
                L2.append(FreqDic[itemset])
        return L1, L2

    def has_infrequent_subset(self,c,L_last,k):
        subsets = list(itertools.combinations(c,k-1))
        for each in subsets:
            each = list(each)
            if each not in L_last:
                return True
        return False

    def apriori_gen(self,L_last):
        k = len(L_last[0]) + 1
        Ck = []
        for itemset1 in L_last:
            for itemset2 in L_last:
                flag = 0
                for i in range(k-2):
                    if itemset1[i] != itemset2[i]:
                        flag = 1
                        break;
                if flag == 1:continue
                if itemset1[k-2] < itemset2[k-2]:
                    c = itemset1 + [itemset2[k-2]]
                else:
                    continue
                if self.has_infrequent_subset(c,L_last,k):
                    continue
                else:
                    Ck.append(c)
        return Ck

    def do(self):
        L_last, L_count = self.find_frequent_1_itemsets()
        #print 'L:', L_last
        L = L_last
        i = 0
        while L_last != []:
            Ck = self.apriori_gen(L_last)
            if Ck == []:
                break
            #print 'C:', Ck
            FreqDic = {}
            for itemset in self.data:
                for c in Ck:
                    if set(c) <= set(self.data[itemset]):
                        if tuple(c) in FreqDic:
                            FreqDic[tuple(c)]+=1
                        else:
                            FreqDic[tuple(c)]=1
           # print 'Scan:',FreqDic
            Lk = [] #store itemsets
            Lc = [] #store frequent
            for c in FreqDic:
                if FreqDic[c] >= self.min_sup_val:
                    Lk.append(list(c))
                    Lc.append(FreqDic[c])
            L_last = Lk
            #print 'L:', Lk
            L += Lk
            L_count += Lc
        return L, L_count
print 'This is the midterm project!'
flag = 1
while(flag > 0):
    Data = {}
    print 'Please choose a dataset:'
    print '1:GameStop'
    print '2:Logitech'
    print '3:Adidas'
    print '4:Apple'
    print '5:Books'
    print '6:Sample1'
    print '7:Sample2'
    datano = input()
    if datano == 1:
        f = open('G:/GameStop.txt', 'r')
    if datano == 2:
        f = open('G:/Logitech.txt', 'r')
    if datano == 3:
        f = open('G:/Adidas.txt', 'r')
    if datano == 4:
        f = open('G:/Apple.txt', 'r')
    if datano == 5:
        f = open('G:/Books.txt', 'r')
    if datano == 6:
        f = open('G:/test.txt', 'r')
    if datano == 7:
        f = open('G:/test1.txt', 'r')
    print 'Please input Min.support(0-1)'
    min_sup = input()
    print 'Please input Min.confidence(0-1)'
    min_con = input()
    for line in f:
        key, val = line.rstrip().split('|')
        Data[key] = val.split(',')
    print 'DataSet:', Data
    a=Apriori(min_sup=min_sup,dataDic=Data)
    L_freq,L_count = a.do()
    for item in L_freq:
        sorted(item)
    print '\nFrequent itemsets:',L_freq

    def isinFreqitem(list1,list2): #compare the combined list with subset of frequent itemsets
        for item in list2:
            if sorted(item) == sorted(list1):
                return True
        return False

    print '\nAssociation rules:'

    for i in range(len(L_freq)):
        for j in range(i+1,len(L_freq)):
            listE = L_freq[i] + L_freq[j]
            if not isinFreqitem(listE, L_freq):
                continue
            else:
                c1 = L_freq.index(sorted(listE))
                if float(L_count[c1])/L_count[i]>=min_con:
                    print L_freq[i],'-->',L_freq[j],'support=',round(float(L_count[c1])/len(Data),2),'confidence=',round(float(L_count[c1])/L_count[i],2)
                if float(L_count[c1])/L_count[j]>=min_con:
                    print L_freq[j],'-->',L_freq[i],'support=',round(float(L_count[c1])/len(Data),2),'confidence=',round(float(L_count[c1])/L_count[j],2)

    print '\nDo you want to choose another dataset?'
    print 'Please choose: 1:continue'
    print '               2:end'
    choose = input()
    if choose == 1:
        continue
    if choose == 2:
        flag = 0

