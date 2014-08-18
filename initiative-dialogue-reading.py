import os, fnmatch, re, csv, pprint, shutil, sys,subprocess
import re
from string import punctuation
from cStringIO import StringIO
from tokenize import generate_tokens            

def find_files(directory, pattern):
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                filename = os.path.join(root, basename)
                #print filename
                yield filename
directory ='F:\\ICT\\NIFR\\CrossCultural Data\\CartoonData_US_China\\'

for filename in find_files(directory,'*.csv'):

    infile = open(filename)
    outfile = open(filename[:-4]+'cleaned.csv', 'w')

    replacements = {'"':'','<':'\n<','bir':'','ir':''}

    lines = (line.strip() for line in infile.readlines()) # All lines including the blank ones
    lines = (line for line in lines if line) # Non-blank lines

    for line in lines:
        #print line
        if line.find('New Material') ==-1:
            for src, target in replacements.iteritems():
                line = line.replace(src, target)
                line=line.replace("What?s", "What is");
                line=line.replace("what?s", "what is");
                line=line.replace("How?s", "How is");
                line=line.replace("how?s", "how is");
                line=line.replace("I?m", "I am");
                line=line.replace("I'm", "I am");
                line=line.replace("it's", "it is");
                line=line.replace("doesn't", "does not");
                line=line.replace("that's", "that is");
                line=line.replace("That's", "that is");
                line=line.replace("don't", "do not");
                line=line.replace("aren't", "are not");
                line=line.replace("I'll", "I will");
                line=line.replace("you'll", "you will");
                line=line.replace("You'll", "you will");
                line=line.replace("there's", "there is");
                line=line.replace("There's", "there is");
                line=line.replace(",000", "000");
                line=line.replace(",500", "500");            
            outfile.write(line+'\n')
    infile.close()
    outfile.close()

FILE_all = open(directory+'\\all-initiative-tags.csv',"w")
FILE_all.write('filename'+'\t,'
               +'total_N_count'+'\t,'+'total_I_count'+'\t,'+'total_count'+'\t,'+'total_count'+'\t,'+'total_speakers'+'\t,'+'total_words'+'\t,'+'total_turns'+'\t,'
               +'speaker_1_N_count'+'\t,'+'speaker_1_I_count'+'\t,'+'speaker_1_F_count'+'\t,'+'speaker_1_R_count'+'\t,'+'speaker_1_name'+'\t,'+'speaker_1_words'+'\t,'+'speaker_1_turns'+'\t,'
               +'speaker2_N_count'+'\t,'+'speaker2_I_count'+'\t,'+'speaker2_F_count'+'\t,'+'speaker2_R_count'+'\t,'+'speaker2_name'+'\t,'+'speaker2_words'+'\t,'+'speaker2_turns'+'\t,'
               +'speaker3_N_count'+'\t,'+'speaker3_I_count'+'\t,'+'speaker3_F_count'+'\t,'+'speaker3_R_count'+'\t,'+'speaker3_name'+'\t,'+'speaker3_words'+'\t,'+'speaker3_turns'+'\t,'
               +'speaker4_N_count'+'\t,'+'speaker4_I_count'+'\t,'+'speaker4_F_count'+'\t,'+'speaker4_R_count'+'\t,'+'speaker4_name'+'\t,'+'speaker4_words'+'\t,'+'speaker4_turns'+'\t,'
               +'speaker5_N_count'+'\t,'+'speaker5_I_count'+'\t,'+'speaker5_F_count'+'\t,'+'speaker5_R_count'+'\t,'+'speaker5_name'+'\t,'+'speaker5_words'+'\t,'+'speaker5_turns'+'\t,'
               +'\n')
import csv
import sys

for filename in find_files(directory,'*cleaned.csv'):
    FILE_all.write(filename+'\t,')

    print 'Found files source:', filename

    speaker_list = []
    
    conversation_turn = []
    conversation_N = []
    conversation_I = []
    conversation_F = []
    conversation_R = []
    conversation_speaker = []
    conversation_utterance = []

    tc=0
    f_in= open(filename)
    try:
        reader = csv.reader(f_in)
        for row in reader:
            #print row
            #print '\n'
            tc=tc+1
            conversation_turn.append(tc)
            conversation_N.append(row[0])
            conversation_I.append(row[1])
            conversation_F.append(row[2])
            conversation_R.append(row[3])
            conversation_speaker.append(row[4])
            sentence=row[5:2000]
            sentence=' '.join(sentence)
            sentence=' '.join(sentence.split())
            conversation_utterance.append(sentence)
            if row[4] not in speaker_list:
                speaker_list.append(row[4])
    finally:
        f_in.close()

    #print conversation_turn
    #print speaker_list

    #print conversation_N
    #print conversation_I
    #print conversation_F
    #print conversation_R
    #print conversation_speaker
    #print conversation_utterance

######### TOTAL STAT ##########    
    total_word_count=0; total_turn_count=0;
    total_I_count=0; total_R_count=0; total_F_count=0; total_N_count=0;
    #### WITHIN PATTERNS #####  
    total_pattern_no_R =0;#    
    total_pattern_just_R =0; total_pattern_just_I =0; total_pattern_just_N =0; total_pattern_just_F =0;
    total_pattern_I_N =0;    total_pattern_R_I =0;    total_pattern_R_N =0;    total_pattern_R_F =0;    total_pattern_I_F =0;    total_pattern_N_F =0;
    total_pattern_R_I_N =0;    total_pattern_R_I_F =0;    total_pattern_R_F_N =0;    total_pattern_I_F_N =0;
    total_pattern_R_F_N_I=0;    
    #### VERTICAL PATTERNS ####
    total_vertical_I_I=0;    total_vertical_I_no_F=0;    total_vertical_I_F=0;    total_vertical_I_R=0; total_vertical_I_N=0;
    total_vertical_N_N=0;   total_vertical_N_I=0;    total_vertical_N_R=0;    total_vertical_N_F=0    
    total_vertical_F_N=0;    total_vertical_F_I=0;    total_vertical_F_R=0;    total_vertical_F_F=0;
    total_vertical_R_N=0;    total_vertical_R_I=0;    total_vertical_R_R=0;     total_vertical_R_F=0
#### PATTERNS #####

    for tindex,sp in enumerate(conversation_speaker):           
        r = re.compile(r'[{}]'.format(punctuation))
        new_strs = r.sub(' ',conversation_utterance[tindex])
        lt2= len(new_strs.split())
        total_word_count=total_word_count+lt2
        total_turn_count=total_turn_count+1
        if conversation_N[tindex]=='N':
            total_N_count=total_N_count+1
        if conversation_R[tindex]=='R':
            total_R_count=total_R_count+1
        else:
            total_pattern_no_R=total_pattern_no_R+1
        if conversation_I[tindex]=='I':
            total_I_count=total_I_count+1
        if conversation_F[tindex]=='F':
            total_F_count=total_F_count+1
        #####Match Patterns######  
        if (conversation_R[tindex]=='R') and (conversation_I[tindex]!='I') and (conversation_F[tindex]!='F') and (conversation_N[tindex]!='N') :
            total_pattern_just_R=total_pattern_just_R+1    
        if (conversation_R[tindex]!='R') and (conversation_I[tindex]=='I') and (conversation_F[tindex]!='F') and (conversation_N[tindex]!='N') :
            total_pattern_just_I=total_pattern_just_I+1    
        if (conversation_R[tindex]!='R') and (conversation_I[tindex]!='I') and (conversation_F[tindex]!='F') and (conversation_N[tindex]=='N') :
            total_pattern_just_N=total_pattern_just_N+1
        if (conversation_R[tindex]!='R') and (conversation_I[tindex]!='I') and (conversation_F[tindex]=='F') and (conversation_N[tindex]!='N') :
            total_pattern_just_F=total_pattern_just_F+1
        if (conversation_R[tindex]!='R') and (conversation_I[tindex]=='I') and (conversation_F[tindex]!='F') and (conversation_N[tindex]=='N') :
            total_pattern_I_N=total_pattern_I_N+1    
        if (conversation_R[tindex]=='R') and (conversation_I[tindex]=='I') and (conversation_F[tindex]!='F') and (conversation_N[tindex]!='N') :
            total_pattern_R_I=total_pattern_R_I+1    
        if (conversation_R[tindex]=='R') and (conversation_I[tindex]!='I') and (conversation_F[tindex]!='F') and (conversation_N[tindex]=='N') :
            total_pattern_R_N=total_pattern_R_N+1    
        if (conversation_R[tindex]=='R') and (conversation_I[tindex]!='I') and (conversation_F[tindex]=='F') and (conversation_N[tindex]!='N') :
            total_pattern_R_F=total_pattern_R_F+1
        if (conversation_R[tindex]!='R') and (conversation_I[tindex]=='I') and (conversation_F[tindex]=='F') and (conversation_N[tindex]!='N') :
            total_pattern_I_F=total_pattern_I_F+1
        if (conversation_R[tindex]!='R') and (conversation_I[tindex]!='I') and (conversation_F[tindex]=='F') and (conversation_N[tindex]=='N') :
            total_pattern_N_F=total_pattern_N_F+1                    
                      ###  
        if (conversation_R[tindex]=='R') and (conversation_I[tindex]=='I') and (conversation_F[tindex]!='F') and (conversation_N[tindex]=='N') :
            total_pattern_R_I_N=total_pattern_R_I_N+1
        if (conversation_R[tindex]=='R') and (conversation_I[tindex]=='I') and (conversation_F[tindex]=='F') and (conversation_N[tindex]!='N') :
            total_pattern_R_I_F=total_pattern_R_I_F+1
        if (conversation_R[tindex]=='R') and (conversation_I[tindex]!='I') and (conversation_F[tindex]=='F') and (conversation_N[tindex]=='N') :
            total_pattern_R_F_N=total_pattern_R_F_N+1
        if (conversation_R[tindex]!='R') and (conversation_I[tindex]=='I') and (conversation_F[tindex]=='F') and (conversation_N[tindex]=='N') :
            total_pattern_I_F_N=total_pattern_I_F_N+1
                     ###
        if (conversation_R[tindex]=='R') and (conversation_I[tindex]=='I') and (conversation_F[tindex]=='F') and (conversation_N[tindex]=='N') :
            total_pattern_R_F_N_I=total_pattern_R_F_N_I+1

        #####Match Patterns######

        if((tindex+1)<len(conversation_speaker)):
            if ((conversation_I[tindex]=='I') and (conversation_I[tindex+1]=='I')):
                total_vertical_I_I=total_vertical_I_I+1
            if ((conversation_I[tindex]=='I') and (conversation_F[tindex+1]=='F')):
                total_vertical_I_no_F=total_vertical_I_no_F+1
            if ((conversation_I[tindex]=='I') and (conversation_F[tindex+1]=='F')):
                total_vertical_I_F=total_vertical_I_F+1
            if ((conversation_I[tindex]=='I') and (conversation_R[tindex+1]=='R')):
                total_vertical_I_R=total_vertical_I_R+1
            if ((conversation_I[tindex]=='I') and(conversation_N[tindex+1]=='N')):
                total_vertical_I_N=total_vertical_I_N+1
            if ((conversation_N[tindex]=='N') and (conversation_N[tindex+1]=='N')):
                total_vertical_N_N=total_vertical_N_N+1
            if ((conversation_N[tindex]=='N') and (conversation_I[tindex+1]=='I')):
                total_vertical_N_I=total_vertical_N_I+1
            if ((conversation_N[tindex]=='N') and (conversation_R[tindex+1]=='R')):
                total_vertical_N_R=total_vertical_N_R+1
            if ((conversation_N[tindex]=='N') and(conversation_F[tindex+1]=='F')):
                total_vertical_N_F=total_vertical_N_F+1
            if ((conversation_F[tindex]=='F') and(conversation_N[tindex+1]=='N')):
                total_vertical_F_N=total_vertical_F_N+1
            if ((conversation_F[tindex]=='F') and (conversation_I[tindex+1]=='I')):
                total_vertical_F_I=total_vertical_F_I+1
            if ((conversation_F[tindex]=='F') and (conversation_R[tindex+1]=='R')):
                total_vertical_F_R=total_vertical_F_R+1
            if ((conversation_F[tindex]=='F') and (conversation_F[tindex+1]=='F')):
                total_vertical_F_F=total_vertical_F_F+1
            if ((conversation_R[tindex]=='R') and (conversation_N[tindex+1]=='N')):
                total_vertical_R_N=total_vertical_R_N+1
            if ((conversation_R[tindex]=='R') and (conversation_I[tindex+1]=='I')):
                total_vertical_R_I=total_vertical_R_I+1
            if ((conversation_R[tindex]=='R') and (conversation_R[tindex+1]=='R')):
                total_vertical_R_R=total_vertical_R_R+1
            if ((conversation_R[tindex]=='R') and (conversation_F[tindex+1]=='F')):
                total_vertical_R_F=total_vertical_R_F+1                
                #####Match Patterns######

    FILE_all.write(str(total_N_count)+'\t,'+str(total_I_count)+'\t,'+str(total_F_count)+'\t,'+str(total_R_count)+'\t,'+str(len(speaker_list))+'\t,'+str(total_word_count)+'\t,'+str(total_turn_count)+'\t,')        

    for index,speaker_current in enumerate(speaker_list):  
        FILE_speaker_1 = open(filename[:-4]+'-raw-speaker-'+speaker_current+'.csv',"w")
        FILE_speaker_1_stat = open(filename[:-4]+'-stat-speaker-'+speaker_current+'.csv',"w")

        FILE_speaker_1_stat.write('filename'+'\t,'
                +'total_N_count'+'\t,'+'total_I_count'+'\t,'+'total_F_count'+'\t,'+'total_R_count'+'\t,'+'total_name'+'\t,'+'total_words'+'\t,'+'total_turns'+'\t,'
                +'total_pattern_no_R'+'\t,'+'total_pattern_just_R'+'\t,'+'total_pattern_just_I'+'\t,'+'total_pattern_just_N'+'\t,'+'total_pattern_just_F'+'\t,'
                +'total_pattern_I_N'+'\t,'+'total_pattern_R_I'+'\t,'+'total_pattern_R_N'+'\t,'+'total_pattern_R_F'+'\t,'+'total_pattern_I_F'+'\t,'+'total_pattern_N_F'+'\t,'
                +'total_pattern_R_I_N'+'\t,'+'total_pattern_R_I_F'+'\t,'+'total_pattern_R_F_N'+'\t,'+'total_pattern_I_F_N'+'\t,'
                +'total_pattern_R_F_N_I'+'\t,'
                +'total_vertical_I_I'+'\t,'+'total_no_F_to_I'+'\t,'+'total_vertical_I_F'+'\t,'+'total_vertical_I_R'+'\t,'+'total_vertical_I_N'+'\t,'
                +'total_vertical_N_N'+'\t,'+'total_vertical_N_I'+'\t,'+'total_vertical_N_R'+'\t,'+'total_vertical_N_F'+'\t,'
                +'total_vertical_F_N'+'\t,'+'total_vertical_F_I'+'\t,'+'total_vertical_F_R'+'\t,'+'total_vertical_F_F'+'\t,'
                +'total_vertical_R_N'+'\t,'+'total_vertical_R_I'+'\t,'+'total_vertical_R_R'+'\t,'+'total_vertical_R_F'+'\t,'

                +'speaker_1_N_count'+'\t,'+'speaker_1_I_count'+'\t,'+'speaker_1_F_count'+'\t,'+'speaker_1_R_count'+'\t,'+'speaker_1_name'+'\t,'+'speaker_1_words'+'\t,'+'speaker_1_turns'+'\t,'
                +'speaker_1_pattern_no_R'+'\t,'+'speaker_1_pattern_just_R'+'\t,'+'speaker_1_pattern_just_I'+'\t,'+'speaker_1_pattern_just_N'+'\t,'+'speaker_1_pattern_just_F'+'\t,'
                +'speaker_1_pattern_I_N'+'\t,'+'speaker_1_pattern_R_I'+'\t,'+'speaker_1_pattern_R_N'+'\t,'+'speaker_1_pattern_R_F'+'\t,'+'speaker_1_pattern_I_F'+'\t,'+'speaker_1_pattern_N_F'+'\t,'
                +'speaker_1_pattern_R_I_N'+'\t,'+'speaker_1_pattern_R_I_F'+'\t,'+'speaker_1_pattern_R_F_N'+'\t,'+'speaker_1_pattern_I_F_N'+'\t,'
                +'speaker_1_pattern_R_F_N_I'+'\t,'
                +'vertical_speaker_1_I_I'+'\t,'+'speaker_1_no_F_to_I'+'\t,'+'vertical_speaker_1_I_F'+'\t,'+'vertical_speaker_1_I_R'+'\t,'+'vertical_speaker_1_I_N'+'\t,'
                +'vertical_speaker_1_N_N'+'\t,'+'vertical_speaker_1_N_I'+'\t,'+'vertical_speaker_1_N_R'+'\t,'+'vertical_speaker_1_N_F'+'\t,'
                +'vertical_speaker_1_F_N'+'\t,'+'vertical_speaker_1_F_I'+'\t,'+'vertical_speaker_1_F_R'+'\t,'+'vertical_speaker_1_F_F'+'\t,'
                +'vertical_speaker_1_R_N'+'\t,'+'vertical_speaker_1_R_I'+'\t,'+'vertical_speaker_1_R_R'+'\t,'+'vertical_speaker_1_R_F'+'\t,'
                                 
               +'\n')


        speaker_1_word_count=0;        speaker_1_turn_count=0;
        speaker_1_I_count=0;        speaker_1_R_count=0;        speaker_1_F_count=0;        speaker_1_N_count=0;

        #### WITHIN PATTERNS #####   
        speaker_1_pattern_no_R =0;#    
        speaker_1_pattern_just_R =0;    speaker_1_pattern_just_I =0;    speaker_1_pattern_just_N =0;    speaker_1_pattern_just_F =0;        
        speaker_1_pattern_I_N =0;       speaker_1_pattern_R_I =0;      speaker_1_pattern_R_N =0;        speaker_1_pattern_R_F =0;    speaker_1_pattern_I_F =0;   speaker_1_pattern_N_F =0;
        speaker_1_pattern_R_I_N =0;     speaker_1_pattern_R_I_F =0;     speaker_1_pattern_R_F_N =0;     speaker_1_pattern_I_F_N =0;
        speaker_1_pattern_R_F_N_I=0;
        ## VERTICAL PATTERNS
        vertical_speaker_1_I_I=0;        vertical_speaker_1_I_no_F=0;   vertical_speaker_1_I_F=0;     vertical_speaker_1_I_R=0;     vertical_speaker_1_I_N=0
        vertical_speaker_1_N_N=0;        vertical_speaker_1_N_I=0;        vertical_speaker_1_N_R=0;        vertical_speaker_1_N_F=0;
        vertical_speaker_1_F_N=0;        vertical_speaker_1_F_I=0;        vertical_speaker_1_F_R=0;        vertical_speaker_1_F_F=0;    
        vertical_speaker_1_R_N=0;        vertical_speaker_1_R_I=0;        vertical_speaker_1_R_R=0;        vertical_speaker_1_R_F=0;
        ###################    

        for spindex,sp in enumerate(conversation_speaker):           
            if sp == speaker_current:
                r = re.compile(r'[{}]'.format(punctuation))
                new_strs = r.sub(' ',conversation_utterance[spindex])
                lt2= len(new_strs.split())
                #lt1= re.split(r'[^0-9A-Za-z]+',conversation_utterance[spindex])
                #speaker_1_word_count=speaker_1_word_count+len(lt1)
                
                speaker_1_word_count=speaker_1_word_count+lt2
                speaker_1_turn_count=speaker_1_turn_count+1

                if conversation_N[spindex]=='N':
                    speaker_1_N_count=speaker_1_N_count+1
                if conversation_R[spindex]=='R':
                    speaker_1_R_count=speaker_1_R_count+1
                else:
                    speaker_1_pattern_no_R=speaker_1_pattern_no_R+1
                if conversation_I[spindex]=='I':
                    speaker_1_I_count=speaker_1_I_count+1
                if conversation_F[spindex]=='F':
                    speaker_1_F_count=speaker_1_F_count+1
                #####Match Patterns######  
                if (conversation_R[spindex]=='R') and (conversation_I[spindex]!='I') and (conversation_F[spindex]!='F') and (conversation_N[spindex]!='N') :
                    speaker_1_pattern_just_R=speaker_1_pattern_just_R+1    
                if (conversation_R[spindex]!='R') and (conversation_I[spindex]=='I') and (conversation_F[spindex]!='F') and (conversation_N[spindex]!='N') :
                    speaker_1_pattern_just_I=speaker_1_pattern_just_I+1    
                if (conversation_R[spindex]!='R') and (conversation_I[spindex]!='I') and (conversation_F[spindex]!='F') and (conversation_N[spindex]=='N') :
                    speaker_1_pattern_just_N=speaker_1_pattern_just_N+1
                if (conversation_R[spindex]!='R') and (conversation_I[spindex]!='I') and (conversation_F[spindex]=='F') and (conversation_N[spindex]!='N') :
                    speaker_1_pattern_just_F=speaker_1_pattern_just_F+1
                 ###  
                if (conversation_R[spindex]!='R') and (conversation_I[spindex]=='I') and (conversation_F[spindex]!='F') and (conversation_N[spindex]=='N') :
                    speaker_1_pattern_I_N=speaker_1_pattern_I_N+1    
                if (conversation_R[spindex]=='R') and (conversation_I[spindex]=='I') and (conversation_F[spindex]!='F') and (conversation_N[spindex]!='N') :
                    speaker_1_pattern_R_I=speaker_1_pattern_R_I+1    
                if (conversation_R[spindex]=='R') and (conversation_I[spindex]!='I') and (conversation_F[spindex]!='F') and (conversation_N[spindex]=='N') :
                    speaker_1_pattern_R_N=speaker_1_pattern_R_N+1    
                if (conversation_R[spindex]=='R') and (conversation_I[spindex]!='I') and (conversation_F[spindex]=='F') and (conversation_N[spindex]!='N') :
                    speaker_1_pattern_R_F=speaker_1_pattern_R_F+1
                if (conversation_R[spindex]!='R') and (conversation_I[spindex]=='I') and (conversation_F[spindex]=='F') and (conversation_N[spindex]!='N') :
                    speaker_1_pattern_I_F=speaker_1_pattern_I_F+1
                if (conversation_R[spindex]!='R') and (conversation_I[spindex]!='I') and (conversation_F[spindex]=='F') and (conversation_N[spindex]=='N') :
                    speaker_1_pattern_N_F=speaker_1_pattern_N_F+1                    
                  ###  
                if (conversation_R[spindex]=='R') and (conversation_I[spindex]=='I') and (conversation_F[spindex]!='F') and (conversation_N[spindex]=='N') :
                    speaker_1_pattern_R_I_N=speaker_1_pattern_R_I_N+1
                if (conversation_R[spindex]=='R') and (conversation_I[spindex]=='I') and (conversation_F[spindex]=='F') and (conversation_N[spindex]!='N') :
                    speaker_1_pattern_R_I_F=speaker_1_pattern_R_I_F+1
                if (conversation_R[spindex]=='R') and (conversation_I[spindex]!='I') and (conversation_F[spindex]=='F') and (conversation_N[spindex]=='N') :
                    speaker_1_pattern_R_F_N=speaker_1_pattern_R_F_N+1
                if (conversation_R[spindex]!='R') and (conversation_I[spindex]=='I') and (conversation_F[spindex]=='F') and (conversation_N[spindex]=='N') :
                    speaker_1_pattern_I_F_N=speaker_1_pattern_I_F_N+1
                 ###
                if (conversation_R[spindex]=='R') and (conversation_I[spindex]=='I') and (conversation_F[spindex]=='F') and (conversation_N[spindex]=='N') :
                    speaker_1_pattern_R_F_N_I=speaker_1_pattern_R_F_N_I+1

                #####Match Patterns######

                if((spindex+1)<len(conversation_speaker)):

                    if ((conversation_I[spindex]=='I') and (conversation_I[spindex+1]=='I')):
                        vertical_speaker_1_I_I=vertical_speaker_1_I_I+1
                        #total_vertical_I_I=total_vertical_I_I+1
                    if ((conversation_I[spindex]=='I') and (conversation_F[spindex+1]=='F')):
                        vertical_speaker_1_I_no_F=vertical_speaker_1_I_no_F+1
                        #total_vertical_I_no_F=total_vertical_I_no_F+1
                    if ((conversation_I[spindex]=='I') and (conversation_F[spindex+1]=='F')):
                        vertical_speaker_1_I_F=vertical_speaker_1_I_F+1
                        #total_vertical_I_F=total_vertical_I_F+1
                    if ((conversation_I[spindex]=='I') and (conversation_R[spindex+1]=='R')):
                        vertical_speaker_1_I_R=vertical_speaker_1_I_R+1
                        #total_vertical_I_R=total_vertical_I_R+1
                    if ((conversation_I[spindex]=='I') and(conversation_N[spindex+1]=='N')):
                        vertical_speaker_1_I_N=vertical_speaker_1_I_N+1
                        #total_vertical_I_N=total_vertical_I_N+1
                    if ((conversation_N[spindex]=='N') and (conversation_N[spindex+1]=='N')):
                        vertical_speaker_1_N_N=vertical_speaker_1_N_N+1
                        #total_vertical_N_N=total_vertical_N_N+1
                    if ((conversation_N[spindex]=='N') and (conversation_I[spindex+1]=='I')):
                        vertical_speaker_1_N_I=vertical_speaker_1_N_I+1
                        #total_vertical_N_I=total_vertical_N_I+1
                    if ((conversation_N[spindex]=='N') and (conversation_R[spindex+1]=='R')):
                        vertical_speaker_1_N_R=vertical_speaker_1_N_R+1
                        #total_vertical_N_R=total_vertical_N_R+1
                    if ((conversation_N[spindex]=='N') and(conversation_F[spindex+1]=='F')):
                        vertical_speaker_1_N_F=vertical_speaker_1_N_F+1
                        #total_vertical_N_F=total_vertical_N_F+1
                    if ((conversation_F[spindex]=='F') and(conversation_N[spindex+1]=='N')):
                        vertical_speaker_1_F_N=vertical_speaker_1_F_N+1
                        #total_vertical_F_N=total_vertical_F_N+1
                    if ((conversation_F[spindex]=='F') and (conversation_I[spindex+1]=='I')):
                        vertical_speaker_1_F_I=vertical_speaker_1_F_I+1
                        #total_vertical_F_I=total_vertical_F_I+1
                    if ((conversation_F[spindex]=='F') and (conversation_R[spindex+1]=='R')):
                        vertical_speaker_1_F_R=vertical_speaker_1_F_R+1
                        #total_vertical_F_R=total_vertical_F_R+1
                    if ((conversation_F[spindex]=='F') and (conversation_F[spindex+1]=='F')):
                        vertical_speaker_1_F_F=vertical_speaker_1_F_F+1
                        #total_vertical_F_F=total_vertical_F_F+1
                    if ((conversation_R[spindex]=='R') and (conversation_N[spindex+1]=='N')):
                        vertical_speaker_1_R_N=vertical_speaker_1_R_N+1
                        #total_vertical_R_N=total_vertical_R_N+1
                    if ((conversation_R[spindex]=='R') and (conversation_I[spindex+1]=='I')):
                        vertical_speaker_1_R_I=vertical_speaker_1_R_I+1
                        #total_vertical_R_I=total_vertical_R_I+1
                    if ((conversation_R[spindex]=='R') and (conversation_R[spindex+1]=='R')):
                        vertical_speaker_1_R_R=vertical_speaker_1_R_R+1
                        #total_vertical_R_R=total_vertical_R_R+1
                    if ((conversation_R[spindex]=='R') and (conversation_F[spindex+1]=='F')):
                        vertical_speaker_1_R_F=vertical_speaker_1_R_F+1
                        #total_vertical_R_F=total_vertical_R_F+1                
                #####Match Patterns######
        
                FILE_speaker_1.write(conversation_N[spindex]); FILE_speaker_1.write(',\t')
                FILE_speaker_1.write(conversation_I[spindex]); FILE_speaker_1.write(',\t')
                FILE_speaker_1.write(conversation_F[spindex]); FILE_speaker_1.write(',\t')
                FILE_speaker_1.write(conversation_R[spindex]); FILE_speaker_1.write(',\t')
                FILE_speaker_1.write(conversation_speaker[spindex]); FILE_speaker_1.write(',\t')
                FILE_speaker_1.write(conversation_utterance[spindex]); FILE_speaker_1.write(',\n')

        #total_word_count=total_word_count+speaker_1_word_count;
        #total_turn_count=total_turn_count+speaker_1_turn_count;
        #total_I_count=total_I_count+speaker_1_I_count;
        #total_R_count=total_R_count+speaker_1_R_count;
        #total_F_count=total_F_count+speaker_1_F_count;
        #total_N_count=total_N_count+speaker_1_N_count;

        FILE_speaker_1_stat.write(filename+'\t,'
                +str(total_N_count)+'\t,'+str(total_I_count)+'\t,'+str(total_F_count)+'\t,'+str(total_R_count)+'\t,'+str(len(speaker_list))+'\t,'+str(total_word_count)+'\t,'+str(total_turn_count)+'\t,'
                +str(total_pattern_no_R)+'\t,'+str(total_pattern_just_R)+'\t,'+str(total_pattern_just_I)+'\t,'+str(total_pattern_just_N)+'\t,'+str(total_pattern_just_F)+'\t,'
                +str(total_pattern_I_N)+'\t,'+str(total_pattern_R_I)+'\t,'+str(total_pattern_R_N)+'\t,'+str(total_pattern_R_F)+'\t,'+str(total_pattern_I_F)+'\t,'+str(total_pattern_N_F)+'\t,'
                +str(total_pattern_R_I_N)+'\t,'+str(total_pattern_R_I_F)+'\t,'+str(total_pattern_R_F_N)+'\t,'+str(total_pattern_I_F_N)+'\t,'
                +str(total_pattern_R_F_N_I)+'\t,'
                +str(total_vertical_I_I)+'\t,'+str(total_vertical_I_no_F)+'\t,'+str(total_vertical_I_F)+'\t,'+str(total_vertical_I_R)+'\t,'+str(total_vertical_I_N)+'\t,'
                +str(total_vertical_N_N)+'\t,'+str(total_vertical_N_I)+'\t,'+str(total_vertical_N_R)+'\t,'+str(total_vertical_N_F)+'\t,'
                +str(total_vertical_F_N)+'\t,'+str(total_vertical_F_I)+'\t,'+str(total_vertical_F_R)+'\t,'+str(total_vertical_F_F)+'\t,'
                +str(total_vertical_R_N)+'\t,'+str(total_vertical_R_I)+'\t,'+str(total_vertical_R_R)+'\t,'+str(total_vertical_R_F)+'\t,'

                +str(speaker_1_N_count)+'\t,'+str(speaker_1_I_count)+'\t,'+str(speaker_1_F_count)+'\t,'+str(speaker_1_R_count)+'\t,'+str(speaker_current)+'\t,'+str(speaker_1_word_count)+'\t,'+str(speaker_1_turn_count)+'\t,'                +str(speaker_1_pattern_no_R)+'\t,'+str(speaker_1_pattern_just_R)+'\t,'+str(speaker_1_pattern_just_I)+'\t,'+str(speaker_1_pattern_just_N)+'\t,'+str(speaker_1_pattern_just_F)+'\t,'
                +str(speaker_1_pattern_I_N)+'\t,'+str(speaker_1_pattern_R_I)+'\t,'+str(speaker_1_pattern_R_N)+'\t,'+str(speaker_1_pattern_R_F)+'\t,'+str(speaker_1_pattern_I_F)+'\t,'+str(speaker_1_pattern_N_F)+'\t,'
                +str(speaker_1_pattern_R_I_N)+'\t,'+str(speaker_1_pattern_R_I_F)+'\t,'+str(speaker_1_pattern_R_F_N)+'\t,'+str(speaker_1_pattern_I_F_N)+'\t,'
                +str(speaker_1_pattern_R_F_N_I)+'\t,'
                +str(vertical_speaker_1_I_I)+'\t,'+str(vertical_speaker_1_I_no_F)+'\t,'+str(vertical_speaker_1_I_F)+'\t,'+str(vertical_speaker_1_I_R)+'\t,'+str(vertical_speaker_1_I_N)+'\t,'
                +str(vertical_speaker_1_N_N)+'\t,'+str(vertical_speaker_1_N_I)+'\t,'+str(vertical_speaker_1_N_R)+'\t,'+str(vertical_speaker_1_N_F)+'\t,'
                +str(vertical_speaker_1_F_N)+'\t,'+str(vertical_speaker_1_F_I)+'\t,'+str(vertical_speaker_1_F_R)+'\t,'+str(vertical_speaker_1_F_F)+'\t,'
                +str(vertical_speaker_1_R_N)+'\t,'+str(vertical_speaker_1_R_I)+'\t,'+str(vertical_speaker_1_R_R)+'\t,'+str(vertical_speaker_1_R_F)+'\t,'
                                 
               +'\n')


        FILE_all.write(str(speaker_1_N_count)+'\t,'+str(speaker_1_I_count)+'\t,'+str(speaker_1_F_count)+'\t,'+str(speaker_1_R_count)+'\t,'+str(speaker_current)+'\t,'+str(speaker_1_word_count)+'\t,'+str(speaker_1_turn_count)+'\t,') 
    FILE_all.write('\n')      
print "done"
FILE_all.close()
    
