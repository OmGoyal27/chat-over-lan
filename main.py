from flask import Flask, request, jsonify

app = Flask(__name__)
PORT = 8000  # Default port for the application

@app.route("/")
def home():
    return "Welcome to ChatLAN! It is currently under development for the GUI."

@app.route("/message", methods=["POST"])
def receive_message():
    message = request.form.get("message", "No message was provided.")
    sender_ip = request.remote_addr  # Get the sender's IP address

    # For now, just return the status and print the message along with sender details
    print(f"Received message: {message} from IP: {sender_ip}")
    return jsonify({"status": "success", "sender_ip": sender_ip})


if __name__ == '__main__':
    app.run(debug=True, port=PORT, host='0.0.0.0')