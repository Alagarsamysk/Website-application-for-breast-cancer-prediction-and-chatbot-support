#Import necessary libraries
from flask import Flask, render_template, request
from keras.models import model_from_json
import numpy as np
import os

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import os
import spacy

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model

##filepath = 'model.h5'
##model = load_model(filepath)
##print(model)




json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)
model.load_weights("model.h5")
print("Loaded model from disk")

print("Model Loaded Successfully")

def pred_tomato_dieas(tomato_plant):
  test_image = load_img(tomato_plant, target_size = (512, 512)) # load image 
  print("@@ Got Image for prediction")
  
  test_image = img_to_array(test_image)/255 # convert image to np array and normalize
  test_image = np.expand_dims(test_image, axis = 0) # change dimention 3D to 4D
  
  result = model.predict(test_image) # predict diseased palnt or not
  print('@@ Raw result = ', result)
  
  pred = np.argmax(result, axis=1)
  print(pred)
  if pred==0:
      return "AFFECTED", 'AFFECTED.html'
       
  elif pred==1:
      return "NORMAL", 'NORMAL.html'
        
  
    

# Create flask instance
app = Flask(__name__)


# render index.html page
@app.route("/", methods=['GET', 'POST'])
def home():
        return render_template('index1.html')

# render index.html page
@app.route("/home2", methods=['GET', 'POST'])
def home2():
        return render_template('index.html')


@app.route("/home3", methods=['GET', 'POST'])
def home3():
        return render_template('chat.html')
    
 
# get input image from client then predict class and render respective .html page for solution
@app.route("/predict", methods = ['GET','POST'])
def predict():
     if request.method == 'POST':
        file = request.files['image'] # fet input
        filename = file.filename        
        print("@@ Input posted = ", filename)
        
        file_path = os.path.join('C:/Users/Acer/Desktop/BREAST_CANCER_CHAT/static/upload', filename)
        file.save(file_path)

        print("@@ Predicting class......")
        pred, output_page = pred_tomato_dieas(tomato_plant=file_path)
              
        return render_template(output_page, pred_output = pred, user_image = file_path)


@app.route("/get")
def get_bot_response():
    filenumber=int(os.listdir('saved_conversations')[-1])
    filenumber=filenumber+1
    file= open('saved_conversations/'+str(filenumber),"w+")
    file.write('bot : Hi There! I am a career chatbot. You can begin conversation by typing in a message and pressing enter.\n')
    file.close()



    english_bot = ChatBot('Bot',
                 storage_adapter='chatterbot.storage.SQLStorageAdapter',
                 logic_adapters=[
       {
           'import_path': 'chatterbot.logic.BestMatch'
       },
       
    ],
    trainer='chatterbot.trainers.ListTrainer')
    english_bot.set_trainer(ListTrainer)

    userText = request.args.get('msg')
    response = str(english_bot.get_response(userText))

    appendfile=os.listdir('saved_conversations')[-1]
    appendfile= open('saved_conversations/'+str(filenumber),"a")
    appendfile.write('user : '+userText+'\n')
    appendfile.write('bot : '+response+'\n')
    appendfile.close()

    return response

    
# For local system & cloud
if __name__ == "__main__":
    app.run(debug=True) 
    
    
