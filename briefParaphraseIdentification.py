# -*- coding: utf-8 -*-
import codecs
import math
import sys

def loadEmbedding(WEfile_in, wedic):
    file = codecs.open(WEfile_in,encoding='utf8')
    for line in file:
        temp = line.split()
        word = temp[0]
        vaList = []
        for value in temp[1:]:
            vaList.append(float(value))
        wedic[word] = vaList
        #print key.encode('GBK', 'ignore');
    file.close()
    print len(wedic)
    print 'WordEmbedding loading done!'

    
def cosine(firstAttr,secondAttr,we_dic):
    if we_dic.has_key(firstAttr) and we_dic.has_key(secondAttr):
        vec1 = we_dic[firstAttr]
        vec2 = we_dic[secondAttr]
    else:
        return 0
    fz = 0.0;
    A = 0.0;
    B = 0.0;
    fm = 0.0;
    for i in range(len(vec1)):
        fz += vec1[i]*vec2[i]
        A  += vec1[i]*vec1[i]
        B  += vec2[i]*vec2[i]
    fm = math.sqrt(A)*math.sqrt(B)
    return fz/fm

def jaccard(firstAttr, secondAttr):
    firstSet = set(firstAttr)
    secondSet = set(secondAttr)
    inter_num = len(firstSet & secondSet)
    union_num = len(firstSet | secondSet)
#    print inter_num,union_num
#    print firstAttr,secondAttr
#    print inter_num/float(union_num)
#    raw_input()
    return inter_num/float(union_num)

def jaccard_vec(firstvec,secondvec):
    firstSet = set(firstvec)
    secondSet = set(secondvec)
    inter_num = len(firstSet & secondSet)
    union_num = len(firstSet | secondSet)
    if union_num==0:
        return 0
    else:
        return inter_num/float(union_num)
    
    
def loadClusterClass(classfile_in, WordToIddic,IdToWordsdic):
    file = codecs.open(classfile_in, encoding = 'utf8')
    for line in file:
        vec = line.split()
        WordToIddic[vec[0]] = int(vec[1])
    for word in WordToIddic:
        id = WordToIddic[word]
        if IdToWordsdic.has_key(id):
            IdToWordsdic[id].append(word)
        else:
            wordlist = []
            wordlist.append(word)
            IdToWordsdic[id] = wordlist
    file.close()
    print 'wToi ' + str(len(WordToIddic))
    print 'iTow ' + str(len(IdToWordsdic))
    print 'classfile loading done!'    
    
#Tag    id1    id2    sentence1    sentence2
#Id（0）    极性（1）    句子（2）    属性1（3）    评价1（4）    极性1（5）（属性评价对）    属性2    评价2    极性2（属性评价对）    
    
    
def ParaphsIdentify(file_in, domain_class_dic, domain_WE_dic, ALPHA, THETA, file_out):
    fr = codecs.open(file_in, encoding = 'utf8')    
    fw = codecs.open(file_out+'_cut1_'+str(ALPHA)+'_'+str(THETA), 'w', encoding = 'utf8')
    fw.write("##################################################################################" +'\n')
    fw.write('ALPHA= ' + str(ALPHA) + '  THETA ' + str(THETA) + '\n')
    print file_in, 'ALPHA= ' + str(ALPHA) + '  THETA ' + str(THETA)
    review_list = [ line.strip().split('\t') for line in fr ]
    scale = len(review_list)
    i = -1
    while(i < len(review_list) - 1 ):    
        i += 1        
        if len(review_list[i]) < 4  or review_list[i][3] == "NULL":
            continue
        for j in range(i+1, len(review_list)):
        
            review_i = review_list[i]
            review_j = review_list[j]
            if review_i[1] != review_j[1]:
                continue
            if len(review_j) < 4 or review_j[3] == "NULL":               
                continue
            if len(review_i) != len(review_j):
                continue
            
            corefrence_attr_num = 0
            corfre_attr_pair = ''
            
            for attr_i_index in range(3, len(review_i), 3):
                is_same_attr = -1
                attr_sim_max = -1
                
                for attr_j_index in range(3, len(review_j), 3):
                    attr_i = review_i[attr_i_index]
                    attr_j = review_j[attr_j_index]
                    pola_i = review_i[attr_i_index + 2]
                    pola_j = review_j[attr_j_index + 2]
                    ####print "----------------------------------",attr_i_index,attr_i,pola_i,attr_j_index,attr_j,pola_j
                    in_same_class = 0
                    
                    if attr_i == attr_j :
                        is_same_attr = 1
                        corfre_attr_pair += attr_i + '-' + attr_j + 'SAME'+ '\t'
                        ###print 'attr',attr_i,attr_j
                        continue
                    if domain_class_dic.has_key(attr_i) and domain_class_dic.has_key(attr_j):
                        if domain_class_dic[attr_i] == domain_class_dic[attr_j] and pola_i == pola_j:
                            in_same_class = 0.1                            
                            ###print "#################"+'\n',review_i[2]+'\n',review_j[2]+'\n',attr_i,attr_j,'in the same class','\n'+"#################"
                    if pola_i == pola_j:
                        ####we_sim = 0.5+0.5*cosine(attr_i,attr_j,domain_WE_dic) #使cosine值保持在0~1
                        jac_sim = jaccard(attr_i,attr_j)
                        we_sim = cosine(attr_i,attr_j,domain_WE_dic)   
                        new_alpha = ALPHA * 1 #字数越少，字符相似度越不可靠
                        sim = new_alpha * jac_sim + (0.9 - new_alpha) * we_sim + in_same_class
                        if sim > attr_sim_max:
                            attr_sim_max = sim
                        if sim > THETA :
                            is_same_attr = 1
                            corfre_attr_pair += attr_i + '-' +attr_j + '\t' + str(jac_sim) + ' ' + str(we_sim) + ' ' +str(sim)
                        ###print "#################"+'\n',review_i[2]+'\n',review_j[2]+'\n',attr_i,attr_j,jac_sim,we_sim,in_same_class,sim,'\n'+"#################"
                        ###print attr_i,attr_j,jac_sim,we_sim,sim,'\n'
                        ###fw.write(attr_i + '-' + attr_j + '\t' + str(jac_sim) + ' ' + str(we_sim) + ' ' +str(sim) + '\n')
                        ###raw_input()
                        ####if attr_i == attr_j:
                            ####raw_input()
                            
                if is_same_attr == 1:
                    corefrence_attr_num += 1
                    ###print attr_sim_max
            ###print corefrence_attr_num,len(review_i)/3-1
            ###raw_input()
            attr_review_i = ''
            attr_review_j = ''
            ###print review_i[0], review_j[0], corefrence_attr_num,len(review_i)/3-1
            if corefrence_attr_num == len(review_i)/3 -1 :
                for atr_index in range(3, len(review_i), 3):
                    attr_review_i +=review_i[atr_index] + '  '
                for atr_index in range(3, len(review_j), 3):
                    attr_review_j +=review_j[atr_index] + '  '
                out_paraphrase = str(1) + '\t' + review_i[0] + '\t' + review_j[0] + '\n' + review_i[2] + '\n' + 'attr: '+ attr_review_i + '\n' + review_j[2] + '\n' + 'attr: ' +attr_review_j +'\n'
                fw.write(out_paraphrase)
                #fw.write('attr_sim: '+corfre_attr_pair + '\n')  
                del review_list[j]
                break
            ###raw_input
        ###print i/float(scale)
        sys.stdout.write(str(i/float(scale)) + '%'+ '\r')
    fr.close()
    fw.close()
    
if __name__ == '__main__':
    
    car_we_dic = {}
    car_we_file_in = 'data/veccar_skip200.skip200'
    phone_we_dic = {}
    phone_we_file_in = 'data/vecphone_skip200.skip200'
    loadEmbedding(car_we_file_in,car_we_dic)
    loadEmbedding(phone_we_file_in,phone_we_dic)
    
    car_class_file_in = 'data/carclass_dic.txt'
    car_wordToid_dic = {}
    car_idToword_dic = {}
    phone_class_file_in = 'data/phoneclass_dic.txt'
    phone_wordToid_dic = {}
    phone_idToword_dic = {}
    loadClusterClass(car_class_file_in, car_wordToid_dic, car_idToword_dic)
    loadClusterClass(phone_class_file_in, phone_wordToid_dic, phone_idToword_dic)
    
    alpha = 0.5
    theta = 0.45
    car_corpus_file_in = 'data/car.txt'
    phone_corpus_file_in = 'data/phone.txt'
    car_paraphrase_file_out = 'output/car_paraphrase_sent'
    phone_paraphrase_file_out = 'output/phone_paraphrase_sent'
    
    car_bug_file_in = 'bug/car_bugtest.txt'
    car_bug_file_out = 'bug/car_bug.txt'
    
    
    for alpha in range(10,40,5):
        alpha *= 0.01
        for theta in range(10,30,5):
            theta *= 0.01
            ParaphsIdentify(car_corpus_file_in, car_wordToid_dic, car_we_dic, alpha, theta, car_paraphrase_file_out)
            ParaphsIdentify(phone_corpus_file_in, phone_wordToid_dic, phone_we_dic, alpha, theta, phone_paraphrase_file_out)
    
    #ParaphsIdentify(car_corpus_file_in, car_wordToid_dic, car_we_dic, alpha, theta, car_paraphrase_file_out)
    #ParaphsIdentify(phone_corpus_file_in, phone_wordToid_dic, phone_we_dic, alpha, theta, phone_paraphrase_file_out)
    
    #ParaphsIdentify(car_corpus_file_in, car_wordToid_dic, car_we_dic, alpha, theta, car_bug_file_out)
    
    print 'done!'
    
    
    
    