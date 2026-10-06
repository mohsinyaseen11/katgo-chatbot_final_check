from flask import Flask,request,render_template,session
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import os
from langchain_core.vectorstores import InMemoryVectorStore
from google import genai
from flask_cors import CORS

app=Flask(__name__)
CORS(app, origins=["https://katgo.store"],supports_credentials=True)







#                                 Document Loaders
loader=PyPDFLoader("Zahra_Stores_Business_Data.pdf")
document=loader.load()








#                                    Chunking
splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=100)
chunk=splitter.split_documents(document)







#                                  Embedding
load_dotenv()
api_key=os.getenv("GEMINI_API_KEY")
embedding=GoogleGenerativeAIEmbeddings(model="gemini-embedding-001",google_api_key=api_key)











#                                    Vector database
#vector_database=Chroma.from_documents(chunk,embedding)
vector_database=InMemoryVectorStore.from_documents(chunk,embedding)








app.secret_key=os.getenv("Secret_Key")


system_prompt = """
Tum ZahraStores.pk ke liye ek helpful customer support assistant ho.
Sirf diye gaye document ki information ke base par jawab do.

Rules:
- Sirf diye gaye context se jawab do, khud se price ya policy mat banao
- Agar jawab na mile to bolo: "Ye information available nahi hai, hamare support team se WhatsApp par contact karein: +92 312-2255552"
- Friendly aur professional tone rakho
- Roman Urdu mein jawab do jab tak user English na likhe
- Agar customer order place karna chahe, bolo "Aap hamari website se order kar sakte hain ya WhatsApp par bata sakte hain"


CONVERSATION STYLE (bohat zaroori):
- Agar customer sirf "categories dikhao" ya "kya available hai" jaisa general sawal poochhe, to SIRF category ke naam list karo (jaise "Kids Wear, Bags & Accessories, Men's T-Shirts..."), koi products ya prices mat do. Phir poocho: "Kis category mein interested hain?"
- Sirf jab customer ek SPECIFIC category naam le (jaise "Kids Wear dikhao"), tab us category ke products aur prices do — aur agar us category mein 5 se zyada items hon, sirf top 5-6 dikhao aur bolo "aur bhi options hain, kisi specific style ya price range mein interested hain?"
- Kabhi bhi ek message mein 10 se zyada items mat do, chahe customer ne poori list maangi ho.
- Markdown symbols (**, -, #) kabhi mat use karo, sirf plain text likho. Products ko comma ya naye line se separate karo, bullet symbols mat likho khud se (formatting widget khud karega).
"""








client=genai.Client(api_key=api_key)



































#                                   Route JSON WALA


@app.route("/json",methods=["POST"])
def chat_json():
    if "history" not in session:
        session["history"]=[]
    
    message=request.json.get("message")
    session["history"].append({"role":"user","reply":message})
    result=vector_database.similarity_search(message,k=4)
    
    prompt="\n\n".join(
        r.page_content for r in result
        )
    final_prompt=f"context:{prompt} history:{session['history']} query:{message}"
    try:
        response=client.models.generate_content(
            model="gemini-3.5-flash-lite",
            config={
                "system_instruction":system_prompt
                },
            contents=final_prompt
            )
        bot_reply=response.text
    except Exception as e:
        print(e)
        bot_reply="Maazrat, abhi jawab dene mein masla aa raha hai. Dobara try karein"
        
    session["history"].append({"role":"bot","reply":bot_reply})
    session.modified = True 
    return {"reply":bot_reply}









































































@app.route("/widget")
def widget():
    return render_template("test.html")

























if __name__=="__main__":
    app.run(debug=False)





















