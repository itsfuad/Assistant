import random
import json
import torch
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('intents-v2.json', 'r', encoding='utf8') as f:
    intents = json.load(f)

FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]
model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

prev_tag = ""

defaults = [
                "Sorry, I didn't get that😢",
                "Please try again☕",
                "I don't understand😐😐",
                "I'm sorry, I don't understand😞",
                "Bujhi nai😕",
                "Bujhlam na😭"
            ]

last_message = ''
my_last_reply = ''

def getReplyFromTag(tag):
    #print(intents['intents'])
    if tag == 'default':
        my_last_reply = random.choice(defaults)
        return my_last_reply
    
    for intent in intents['intents']:
        if intent['tag'] == tag:
            my_last_reply = random.choice(intent['responses'])
            return my_last_reply
        


def getTag(message):
    
    sentence = tokenize(message)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]

    if prob.item() > 0.80:
        return tag
    else:
        return "default"