from flask import Flask, render_template, request, redirect, url_for, jsonify
import pgpy

app = Flask(__name__)

#Load PGP Keys
with open("private_key.asc","r") as f:
    private_key,_ = pgpy.PGPKey.from_blob(f.read())

with open("public_key.asc","r") as f:
    public_key,_ = pgpy.PGPKey.from_blob(f.read())

@app.route("/encrypt", methods=['POST'])
def encrypt_message():
    try:
        #Get JSON data from request
        data = request.get_json()
        message = str(data)

        #Encrypt using public key
        pgp_message = pgpy.PGPMessage.new(message)
        encrypted_message = public_key.encrypt(pgp_message)

        return jsonify({"encrypted_message":str(encrypted_message)})

    except Exception as e:
        return jsonify({"error":str(e)}), 500

@app.route("/decrypt", methods=['POST'])
def decrypt_message():
    try:
        #Get encrypted message from request
        encrypted_message_str = request.json.get("encrypted_message")

        #Load encrypted message
        encrypted_message = pgpy.PGPMessage.from_blob(encrypted_message_str)

        # Unlock private key (if it has a passphrase, use `.unlock("your-passphrase")`)
        with private_key.unlock("your-passphrase") as unlocked_key:
            decrypted_message = unlocked_key.decrypt(encrypted_message)

        return jsonify({"decrypted_message":str(decrypted_message.message)})

    except Exception as e:
        return jsonify({"error":str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)