from flask import Flask, request, jsonify
import requests
from ruamel.yaml import YAML
import socket

IP_ADDRESS = socket.gethostbyname(socket.gethostname()).rstrip()  # Get the local IP address
print(f"Local IP Address: {IP_ADDRESS}")  # Print the local IP address for debugging

app = Flask(__name__)
PORT = 8000  # Default port for the application

def get_contacts_from_yaml(file_path: str = "config/known_contacts.yaml") -> dict[str, str]:
    """
    Load contacts from a YAML file.
    """
    yaml = YAML()
    with open(file_path, 'r') as file:
        contacts = yaml.load(file)
    # The contacts will be in the format {ip: name}
    return contacts

@app.route("/")
def home():
    return "Welcome to ChatLAN! It is currently under development for the GUI."

@app.route("/message", methods=["POST"])
def receive_message():
    message = request.form.get("message", "No message was provided.")
    sender_ip = request.remote_addr  # Get the sender's IP address
    sender_ip = get_contacts_from_yaml().get(sender_ip, sender_ip)  # Get the name from contacts or use IP as fallback
    # For now, just return the status and print the message along with sender details
    print(f"Received message: {message} from {sender_ip}")
    return jsonify({"status": "success", "sender_ip": sender_ip})

def send_message(message: str, ip: str) -> str:
    """
    Send a message to the specified IP address.
    """
    # Placeholder for sending message logic
    print(f"Sending message: {message} to IP: {ip}")
    return requests.post(f'http://{ip}:{PORT}/message', data={"message": message}).text

@app.route("/send_message", methods=["POST"])
def send_message_route():
    """
    Endpoint to send a message to a specified IP address.
    """
    allowed_addresses = ['127.0.0.1', 'localhost', IP_ADDRESS]  # Add your allowed IP addresses here
    if not request.remote_addr.rstrip() in allowed_addresses:
        return jsonify({"status": "error", "message": "Unauthorized access."}), 403

    message = request.form.get("message", None)
    ip = request.form.get("ip", None)

    if not message or not ip:
        return jsonify({"status": "error", "message": "Message and IP are required."}), 400

    response = send_message(message, ip)
    return jsonify({"status": "success", "response": response})

if __name__ == '__main__':
    app.run(debug=True, port=PORT, host='0.0.0.0')