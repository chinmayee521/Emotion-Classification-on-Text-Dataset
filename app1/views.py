from django.shortcuts import render
from django.http import HttpResponse
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem.porter import PorterStemmer
import joblib
import re

# Create your views here.
def home(req):
    
    

    if req.method=="POST":
        print("POST")
        
        text = req.POST["review"]      
      
        op_svm,op_lr,op_rf,op_kernelsvm,op_naive = predict_result(text)
        

        
        return render(req ,'home.html',{'op_svm':op_svm ,'op_lr':op_lr,'op_rf':op_rf,'op_kernelsvm':op_kernelsvm,'op_naive':op_naive,'h':1,'text':text})
    else:
        #return render(req,'home.html',{'h':h,'reviews':reviews ,'ops':ops ,'reviews':reviews} )
        
      
        return render(req,'home.html',{'h':0})
    #=============================================================================================================
def predict_result(text):
    
    nltk.download('stopwords')
    from nltk.corpus import stopwords
    stopwrds = stopwords.words('english')

    to_be_removed =['not' ,'no' ,'nor' ,"wasn't" ,"wouldn't","weren't","doesn't" ,"didn't" ,"haven't" ]
    for w in to_be_removed:
        stopwrds.remove(w)

    ps2 = PorterStemmer()
    new_review = re.sub('[^a-zA-Z]' ," " ,text)
    new_review = new_review.lower()
    new_review = new_review.split()
    new_review = [ps2.stem(x) for x in new_review if not x in set(stopwrds)]
    new_review = " ".join(new_review)
    #print(new_review)
    new_corpus =[new_review]


    cvmodel = joblib.load('app1/MyModel/cv_model')
    corpus2 =cvmodel.transform(new_corpus).toarray()
    svmModel = joblib.load('app1/MyModel/svm_model')
    lr_model = joblib.load('app1/MyModel/lr_model')
    randomforest_model = joblib.load('app1/MyModel/randomforest_model')
    kernelsvm_model = joblib.load('app1/MyModel/kernelsvm_model')
    naive = joblib.load('app1/MyModel/naive_model')
    
    LabelEncoder = joblib.load('app1/MyModel/LabelEncoder')
    
    outputs=[]
    op_svm =(LabelEncoder.inverse_transform(svmModel.predict(corpus2))[0])
    op_lr = (LabelEncoder.inverse_transform(lr_model.predict(corpus2))[0])
    op_rf = (LabelEncoder.inverse_transform(randomforest_model.predict(corpus2))[0])
    op_kernelsvm = (LabelEncoder.inverse_transform(kernelsvm_model.predict(corpus2))[0])
    op_naive = (LabelEncoder.inverse_transform(naive.predict(corpus2))[0])
    
    return op_svm,op_lr,op_rf,op_kernelsvm,op_naive
    