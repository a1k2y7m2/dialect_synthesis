# dialect_synthesis
for graduation thesis about dialect_synthesis

## folder
JNAS:JNAS script data and JNAS wavfile.  
synthesis : the code from a professor and generated txtfile.  
subword_embedding.py : subword form sentencepiece to dialect synthesis.

## usage
### 1. wavfile to continuous F0  
  `cd JNAS`  
  `cat wav2script.txt | paralell -j8`  
  `cat wav2script2_2.txt | parallel -j8`  
  `cat wav2script3_2.txt | parallel -j8`  
    
  "pyworld_jnas1,2,3" is the python script to convert wavfiles to continuous F0 txt files. continuous F0 txt files are in JNAS_voicedata directory.

### 2. split txtfiles into sentences and move to JNAS raw_script directory
  `cd JNAS`  
  `ls /home/akiyama/JNAS/JNAS1/OriginalText/KANJI/NP_unlabeled/*.txt | xargs -i basename {} | xargs -L 1 python text_split.py`  
    
    This python script makes simultaneously Japanese-phoneme align data. But this phoneme align data is no longer used.
  
### 3. make Jananese-Katakana align files
  `cd JNAS`
  `ls /home/akiyama/JNAS/JNAS1/OriginalText/KANJI/NP_unlabeled/*.txt | xargs -i basename {} | xargs -L 1 python txt2wordalign.py`  
    
  Outfiles are saved into align_data directory. An example of saved align file's name is "001001.align".
    
### 4. fast_align
  `cd synthesis/fast_align/build/`  
  `ls /home/akiyama/JNAS/JNAS1/OriginalText/KANJI/NP_unlabeled/*.txt | xargs -i basename {} | xargs -L 1 python charalign.py`  
   
   Outfiles are saved into char_kat_align directory. An example of saved align file name is "001001.alignnum".
