# -*- coding: utf-8 -*-


lineNum = 2500
row = lineNum

        
if __name__ == "__main__":
    f_r = open('phone_paraphrase_sent_cut_OnePair_0.1_0.1','r')
    f_w = open('phone_paraphrase_sent_cut_' + str(1) + '-' + str(1 + lineNum),'w')
    size = len(f_r.readlines())
    f_r = open('phone_paraphrase_sent_cut_OnePair_0.1_0.1','r')
    for i, line in enumerate(f_r):
        if i == row:
            f_w.close()
            f_w = open('phone_paraphrase_sent_cut_' + str(i+1) + '-' + (str(i + lineNum) if (i+lineNum) < size else str(size)),'w')
            row += lineNum
        f_w.write(line)
            
    f_w.close()    
    f_r.close()
    print 'done!'