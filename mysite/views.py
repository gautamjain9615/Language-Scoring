import json
from django.shortcuts import render
from .forms import InputForm
from .models import Input, Data
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import InputSerializer
from .models import Input
from django.http import JsonResponse


class InputViewSet(viewsets.ModelViewSet):
    # queryset = Input.objects.all().order_by('link')
    serializer_class = InputSerializer

# Create your views here.

import os
import sys
import time
import wave
# import azure.cognitiveservices.speech as speechsdk
import pandas as pd
import numpy as np
import re
import librosa
import language_tool_python
import requests
import math



def convert(json_input):
    data1 = json_input
    
    data = data1['useranswer']


    # time_duration = float(librosa.get_duration(filename=audioFile)/60)
    time_duration = int(data1['duration'])/60
    print(time_duration, "minutes")

    # textPath = "textt16.txt"
    # with open(textPath) as infile:
    #     data = infile.read()

    sentence_pat = re.compile(r""" \b ([^.!?]+[.!?]+)   """, re.X)
    word_pat = re.compile(r""" (\S+) """, re.X)

    sentences = sentence_pat.findall(data)
    words = word_pat.findall(data)

    average_sentence_length = sum([len(sentence) for sentence in sentences])/len(sentences)
    average_word_length = sum([len(word) for word in words])/len(words)
    sentences_count = len(sentences)
    print("The number of sentences spoken by the user: ", sentences_count)
    words_per_minute = len(words)/time_duration
    print("Words per minute: ", words_per_minute)
    def count_occurences(word, sentence):
        return sentence.lower().split().count(word)

    def analyzeText(text):
        filler_words = ["like", "so", "basically", "i mean", "actually", "yeah", "stuff"]
        splittedText = text.split()
        length = len(filler_words)
        totalFillerWords = 0
        for i in filler_words:
            p=count_occurences(i, text)
            totalFillerWords = totalFillerWords + p
        return totalFillerWords

    # text = "textt16.txt"
    # with open(text) as f:
        # contents = f.read()
    contents = data
    total_filler_words = analyzeText(contents)
    fw_pm = total_filler_words/time_duration
    print("Filler words per minute: ", fw_pm)
    tool = language_tool_python.LanguageTool('en-US')
    i = 0

    #textPath = "textt16.txt"
    #with open(textPath, 'r') as fin:      
    #for line in fin:
    matches = tool.check(data)
    i = len(matches)   
    #pass

    gc = i
    ge_ps = i/sentences_count
    print("Grammatical errors per sentence: ", ge_ps)
    #from string import punctuation
    punctuation = ['!','.','?','|']
    print(punctuation)
    from collections import Counter
    #with open('textt16.txt') as f:

    c = Counter(c for line in data for c in line if c in punctuation)
    pauses_total = sum(c.values())
    p_pm = pauses_total/time_duration
    print("Pauses per minute =", p_pm)
    [i for i,j in zip(data.split(),data.split()[1:]) if i!=j]
    data_ = " ".join([i for i,j in zip(data.split(),data.split()[1:]) if i!=j]+[data.split()[-1]])
    w =  word_pat.findall(data_)
    # print(w)
    #repeated words
    RW = len(words)-len(w)
    rw_tw = RW/len(words)
    #repeated words per total words
    print("Repeated words per total words: ", rw_tw)

    total_length = 0
    for i in range(len(sentences)):
        wor = word_pat.findall(sentences[i])
        total_length += len(wor)
        
    average_length = total_length/len(sentences)
    #print(average_length)
    variation_sentence_length_per_minute = average_length/time_duration
    vsl_pm = variation_sentence_length_per_minute
    print("Variation in sentence length per minute: ", vsl_pm)

    
    ls = data1['keywords']
    words_list = []
    weight_list= []
    for i in range(len(ls)):
        words_list.append(ls[i]['name'])
        weight_list.append(ls[i]['value'])
    

    contentScore = 0
    for i in range(len(words_list)):
        if(re.search(r'\b' + words_list[i] + '\W', data)):
            print("word found: ",words_list[i])
            contentScore += weight_list[i]

    print("total score: ",contentScore)

    obj = Data(ref_id=data1['referenceid'], words=round(words_per_minute), filler_words=round(fw_pm), grammatical_errors=round(ge_ps), pauses=round(p_pm), repeated_words=round(rw_tw), variation=round(vsl_pm))
    obj.save()

    fetched_obj = Data.objects.filter(ref_id=data1['personalityid'])[0]

    if not fetched_obj:
        return {'Celebrity not found': 404}



    wpm_target = fetched_obj.words
    fw_target = fetched_obj.filler_words
    gc_target = fetched_obj.grammatical_errors
    pm_target = fetched_obj.pauses
    rw_target = fetched_obj.repeated_words
    v_target = fetched_obj.variation

    pacing = abs(wpm_target - words_per_minute)
    polish = math.sqrt(math.pow(fw_target - fw_pm, 2) + math.pow(gc_target - ge_ps, 2))
    power = math.sqrt(math.pow(pm_target - p_pm, 2) + math.pow(rw_target - rw_tw , 2) + math.pow(v_target - vsl_pm , 2))
    overall_score = (pacing*4 + polish*2 + power)/7

    print("Pacing Distance =", pacing)
    print("Polish Distance =", polish)
    print("Power Distance =", power)
    print("Overall Score =", overall_score)

    return {"referenceid":data1['referenceid'], 'total' : round(overall_score),'content': round(contentScore), 'pacing' : round(pacing), 'polish' : round(polish), 'power' : round(power), "celebrity": {"personalityid": data1['personalityid'], 'pacing' : round(pacing), 'polish' : round(polish), 'power' : round(power)}}

class MainView(APIView):
    def post(self, request):
        new_dict = convert(request.data)
        return Response(new_dict)
