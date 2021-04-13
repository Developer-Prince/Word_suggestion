#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
from collections import Counter
import re


# In[2]:


def process_data(file_name):
    
    words = []
    
    with open(file_name) as f:
        text = f.read()
    text = text.lower()
    words = re.findall(r'\w+' , text)
    
    return words


# In[3]:


word_l = process_data('./shakespeare.txt')

vocab = set(word_l)
print("\033[94m")
print('The first 10 Words in the Shakespeare.txt are : ', word_l[0:10])
print("\033[92m")
print('The number of unique words in the vocab is :',len(vocab))


# In[4]:


def get_count(text):
    
    word_count_dictionary = {}
    word_count_dictionary = Counter(text)
    
    return word_count_dictionary


# In[5]:


def get_prob(word_count_dict):
    
    probs = {}
    
    vocab_size = sum(word_count_dict.values())
    
    for k in word_count_dict.keys():
        probs[k] = word_count_dict[k]/vocab_size
        
    return probs
    
    


# In[6]:


def delete_letter(word,verbose = False):
    
    split_l = []
    
    for i in range(len(word)):
        split_l.append((word[:i], word[i:]))
    
    delete_l = [L + R[1:] for L,R in split_l if R]
    if verbose: print(f"input word : {word} , \nsplit words : {split_l}, \ndelete letter : {delete_l}")
    return delete_l


# In[7]:


def switch_letter(word , verbose = False):
    split_l  = []
    
    for i in range(len(word)):
        split_l.append((word[:i], word[i:]))
    
    switch_l = [L+R[1]+R[0]+R[2:] for L,R in split_l if len(R)>=2]
    
    if verbose:
        print(f"input word : {word}, \nsplit words : {split_l}, \nswitch words : {switch_l}")
    
    return switch_l


# In[8]:


def replace_letter(word , verbose = False):
    
    split_l  = []
    replace_l = []
    letters = 'abcdefghijklmnopqrstuvwxyz'
    for i in range(len(word)):
        split_l.append((word[0:i], word[i:]))
        
    replace_l = [L+l+(R[1:] if len(R)>1 else '') for L,R in split_l if R for l in letters]
    replace_set = set(replace_l)
    replace_set.remove(word)
    
    replace_l = sorted(list(replace_set))
    
    if verbose:
        print(f"input word :{word}, \nsplit words : {split_l}, \nreplace words :{replace_l} ")
        
    return replace_l


# In[9]:


def insert_letter(word , verbose = False):
    
    split_l = []
    letters = 'abcdefghijklmnopqrstuvwxyz'
    for i in range(len(word)+1):
        split_l.append((word[:i] , word[i:]))
        
    insert_l  = [L+l+R for L, R in split_l for l in letters]
    
    if verbose: print(f"Input word {word} \nsplit_l = {split_l} \ninsert_l = {insert_l}")
        
    return insert_l


# In[10]:


def one_word_edit(word, allow_switches = True):
    
    edit_one_words = set()
    
    edit_one_words.update(delete_letter(word))
    if allow_switches:
        edit_one_words.update(switch_letter(word))
    edit_one_words.update(replace_letter(word))
    edit_one_words.update(insert_letter(word))
        
    return edit_one_words


# In[11]:


def two_word_edit(word , allow_switches=True):
    
    edit_two_word = set()
    
    edit_one = one_word_edit(word , allow_switches=allow_switches)
    for w in edit_one:
        edit_two = one_word_edit(w , allow_switches=allow_switches)
        edit_two_word.update(edit_two)
    
    return edit_two_word


# In[12]:


def get_suggestion(word , probs ,vocab , n = 2 , verbose = False):
    
    suggestion = list((word in vocab and word) or one_word_edit(word).intersection(vocab) or two_word_edit(word).intersection(vocab))
    n_best = [[s , probs[s]] for s in list(reversed(suggestion))]
    if verbose: print("suggestions = ", suggestion)
    return n_best


# In[13]:


def minimum_edit_distance(source ,target , ins_cost = 1 , del_cost = 1 , repl_cost = 2):
    
    m = len(source)
    n = len(target)
    
    D = np.zeros((m+1 , n+1) , dtype = int)
    
    for row in range(1,m+1):
        D[row , 0] = D[row-1,0] + del_cost
        
    for col in range(1,n+1):
        D[0,col] = D[0 , col-1] + ins_cost
        
    for row in range(1,m+1):
        for col in range(1,n+1):
            
            rep_cost = repl_cost
            
            if source[row-1] == target[col-1]:
                rep_cost = 0
            
            D[row ,col] = min(D[row-1 , col]+del_cost , D[row , col-1]+ins_cost , D[row-1 ,col-1]+rep_cost)
            
    med = D[m,n]
    
    return med , D


# In[ ]:





# In[ ]:




