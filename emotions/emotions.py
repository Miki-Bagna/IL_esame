from transformers import RobertaTokenizerFast, TFRobertaForSequenceClassification, pipeline

tokenizer = RobertaTokenizerFast.from_pretrained("arpanghoshal/EmoRoBERTa")
model = TFRobertaForSequenceClassification.from_pretrained("arpanghoshal/EmoRoBERTa")

emotion = pipeline('sentiment-analysis', model='arpanghoshal/EmoRoBERTa')
# def process_emotion(sentences):
#     emotion_labels = [emotion(sentence) for sentence in sentences if emotion(sentence)['label'] != 'neutral']
#     return emotion_labels

def process_emotion(sentences):
    emotion_labels = []
    for sentence in sentences:
        emotions = emotion(sentence)
        if emotions and emotions[0]['label'] != 'neutral':
            emotion_labels.append(emotions[0])
    return emotion_labels