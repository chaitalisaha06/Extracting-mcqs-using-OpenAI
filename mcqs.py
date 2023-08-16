# Installing Openai and Python-MongoDB Connectivity Library
pip install openai
pip install pymongo

# Importing Packages
import pymongo
import openai
import datetime
import pytz

# Connecting MongoDB database using Python Script
client = pymongo.MongoClient("mongodb+srv://chaitalisaha:chaitalisaha@cluster0.lz7jjja.mongodb.net/?retryWrites=true&w=majority")
db=client.question_bank
collection=db.mcqs

#To print the records of database
result=collection.find()
for results in result:
  print(results)

# To delete any unwanted records from the database
collection.delete_many({'question': 'Q. Which of the following is not a variable data type?'})

# Extracting MCQS on a Particular Topic using Openai API
import openai
openai.api_key = "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"

# Function to generate MCQs using OpenAI API
def generate_mcqs(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100
    )
    return response.choices[0].text

# Function to insert MCQs into MongoDB
def insert_mcqs_to_db(mcqs):
        list_of_mcqs = mcqs.split('\n')
        print(list_of_mcqs)
        for index in range(len(list_of_mcqs)):
          if list_of_mcqs[index]=='':
            continue
          elif list_of_mcqs[index][0]=='Q':
            question=list_of_mcqs[index][9:]

          elif (list_of_mcqs[index][:2]=="A." or list_of_mcqs[index][:2]=="a." or list_of_mcqs[index][:2]=="a)" or list_of_mcqs[index][:2]=="A)" or list_of_mcqs[index][:2]=="a:" or list_of_mcqs[index][:2]=="A:") :
            options=list_of_mcqs[index:index+4]

          elif (list_of_mcqs[index][:6]=="Answer" or list_of_mcqs[index][:6]=="answer") :
            answer=list_of_mcqs[index][7:]

          elif (list_of_mcqs[index][:5]=="level" or list_of_mcqs[index][:5]=="Level"):
            level=list_of_mcqs[index][6:]
          
          elif (list_of_mcqs[index][:5]=="topic" or list_of_mcqs[index][:5]=="Topic"):
            topic=list_of_mcqs[index][6:]
          
          current_datetime = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
          date=f'{current_datetime.day}/{current_datetime.month}/{current_datetime.year}'
          time=f'{current_datetime.hour}.{current_datetime.minute}'
        
        mcq_document = {
             "Catagory":"Software Engineering",
             "Created date": date,
             "Created Time":time,
             "Topic":topic,
             "Question Type":"text",
             "Question": question,
             "Option Type":"text",
             "Options": options,
             "Correct answer": answer,
             "Level": level,
             "Source":"ChatGPT"
            }
        
        collection.insert_one(mcq_document)
        print("MCQ inserted successfully!")



prompt = f'Generate a multiple-choice question on software Enginnering with one question(as Question) and four options(A,B,C,D)and its answer(as Answer) and its level(as level) and its specific topic (as topic) in consecutive different lines.'

# Generate MCQs using OpenAI API
generated_mcqs = generate_mcqs(prompt)
print(generated_mcqs)


# Insert generated MCQs into MongoDB
insert_mcqs_to_db(generated_mcqs)



