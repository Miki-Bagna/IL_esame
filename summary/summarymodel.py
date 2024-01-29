
from transformers import pipeline, AutoTokenizer
import re
import pickle

pegasum=pickle.load(open('/Users/david/OneDrive/Desktop/esame_IL/IL_esame/summary/pegsum_pkl','rb'))
tokenizer= AutoTokenizer.from_pretrained('/Users/david/OneDrive/Desktop/esame_IL/IL_esame/summary/tokenizer')

gen_kwargs = {"length_penalty": 0.8, "num_beams":8, "max_length": 125}

pipe = pipeline("summarization", model=pegasum,tokenizer=tokenizer)

def clean4sum(script_text):
    # Split the script into scenes based on changes in location or time of day
    scenes = re.split(r'\n(?=\s{0,}\b(?:INT\.|EXT\.)\s{0,}.*\n|\s{0,}(?:DAY|NIGHT)\s{0,}.*\n)', script_text)
    scenes = [scene.strip() for scene in scenes if scene.strip()]
    
   # if isinstance(script_text, str):
    #    scenes = split_script_into_scenes(script_text)
    #else:
    #    print("Error: script_text is not a string.")
    
    num_b = int(len(script_text) / 1024)

    batches = [""] * num_b

    i = 0
    for scene in scenes:
     if len(batches[i]) + len(scene) <= 1024:
        batches[i] += scene
     else:
        i += 1

    batches = [batch for batch in batches if batch]  # Remove empty batches

    while any(not element for element in batches):
        new_batches = []
        lines_deleted = False
        i = 0

        while i < len(batches):
            if len(batches[i]) == 0:
                lines_deleted = True
            elif i < len(batches) - 1 and len(batches[i]) + len(batches[i + 1]) <= 1024:
                batches[i] += batches[i + 1]
                lines_deleted = True
                i += 1
            else:
                new_batches.append(batches[i])
            i += 1

        batches = new_batches

        if not lines_deleted:
            break
    return batches

def summarize(batches):
    output=''
    for i in batches:
        output+=pipe(i,**gen_kwargs)[0]["summary_text"]
    
    return output
