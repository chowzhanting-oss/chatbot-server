import os
from flask import Flask, request, jsonify #Flask is used to create web server, request is to allow access to incoming HTTP request data like student's question, jsonify is to return a JSON response to the client (Moodle or browser)
from flask_cors import CORS #Import CORS support - Cross-Origin Resource Sharing (Allow Javascript from moodle or other websites to call this flask server without being blocked by the browser)
from openai import OpenAI #Import OpenAI client library to send request to OPENAI API (This is what connects this python cide to OPENAI models) 

app = Flask(__name__) #app represents the web server to define routes that respond to requests, handle incoming HTTP requests and start the server
CORS(app)  # allow requests from Moodle (browser)

# Create OpenAI client with your API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/chat", methods=["POST"]) #define a route called /chat and POST means the server expects data sent in the body of the request (JSON with the student's question)
def chat(): #define the function that runs whenever a request is sent to /chat
    data = request.json #Gets JSON data sent in the POST request
    question = data.get("message", "") #extract the message from JSON, if message dont exist, return ""

    if not question:
        return jsonify({"error": "No message received"}), 400 #checks if student didn't send a question, returns JSON error message and HTTP status 400 (Bad Request)

    try:
        response = client.responses.create(
            model="gpt-5-mini", #specify which AI model to use
            input=[ #list of instructions to define the chatbot's behaviour and personality
                {"role": "system", "content": "You are a patient tutor. Always explain step by step."},
                {"role": "system", "content": "Answer questions about Integrated Electronics only. If asked about unrelated topic, ONLY reply: Sorry I cannot help you with that, I can only answer questions about Integrated Electronics."},
                {"role": "user", "content": question} #the question of the student will be input here
            ]
        )
        return jsonify({"reply": response.output_text}) #Send the answer back to client (Moodle) as JSON
    except Exception as e:
        return jsonify({"error": str(e)}), 500 #if anything goes wrong with the reply, it returns error message in JSON with HTTP status 500 (server error)

if __name__ == "__main__":
    # host='0.0.0.0' makes it accessible from other devices, not just localhost
    app.run(host="0.0.0.0", port=5000, debug=True) #port=5000 is the port number to access the server 
    
    #debug=true is to show detailed error message and reloads the server automatically when code changes