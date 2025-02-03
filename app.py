from flask import Flask, request, render_template, send_from_directory, redirect, url_for, send_file, jsonify, flash
from flask_socketio import SocketIO
import os
import socket
import zipfile
import io
import secrets
import qrcode
from PIL import Image

app = Flask(__name__)
app.secret_key = os.urandom(24)
socketio = SocketIO(app)

# Create uploads folder if it doesn't exist
UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Create static folder if it doesn't exist
STATIC_FOLDER = "static"
if not os.path.exists(STATIC_FOLDER):
    os.makedirs(STATIC_FOLDER)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def allowed_file(filename):
    # In a trusted environment, you may allow all files.
    return True

# Homepage (Upload Form + File List)
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        
        files = request.files.getlist("file")
        for file in files:
            if file.filename == "":
                flash("No selected file")
                return redirect(request.url)
            
            try:
                # Generate a secure filename
                secure_name = secrets.token_urlsafe(8) + "_" + file.filename
                filepath = os.path.join(app.config["UPLOAD_FOLDER"], secure_name)
                file.save(filepath)
                flash("File uploaded successfully")
                # Emit an update so connected clients add the new file in real time
                socketio.emit('file_uploaded', {'filename': secure_name})
            except Exception as e:
                flash(f"Error uploading file: {str(e)}")
                return redirect(request.url)
        return redirect(url_for("index"))
    
    # List files in the upload folder
    files = os.listdir(app.config["UPLOAD_FOLDER"])
    file_infos = []
    for file in files:
        file_infos.append({
            "name": file,
            "type": "image" if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')) else "file"
        })
    return render_template("index.html", files=file_infos)

# File Download Route
@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename, as_attachment=True)

# Download all files as a ZIP archive
@app.route("/download_all", methods=["GET", "POST"])
def download_all():
    zip_filename = "all_files.zip"
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for file in os.listdir(app.config["UPLOAD_FOLDER"]):
            zip_file.write(os.path.join(app.config["UPLOAD_FOLDER"], file), file)
    
    zip_buffer.seek(0)
    return send_file(zip_buffer, as_attachment=True, download_name=zip_filename, mimetype="application/zip")

# File Deletion Route
@app.route("/delete/<filename>")
def delete_file(filename):
    try:
        os.remove(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        flash("File deleted successfully")
        socketio.emit('file_deleted', {'filename': filename})
        return redirect(url_for("index"))
    except Exception as e:
        flash(f"Error deleting file: {str(e)}")
        return redirect(url_for("index"))

# Get the local IP address (useful for generating the QR code)
def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "127.0.0.1"

# QR Code generation route (returns an in-memory PNG image)
@app.route("/qr")
def generate_qr():
    local_ip = get_local_ip()
    url = f"http://{local_ip}:3733"
    
    # Generate QR code directly to bytes
    img = qrcode.make(url)
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return send_file(buf, mimetype='image/png')

# Error handlers for common issues
@app.errorhandler(413)
def too_large(e):
    return jsonify({"error": "File is too large"}), 413

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Resource not found"}), 404

# Run the server
if __name__ == "__main__":
    local_ip = get_local_ip()
    print(f"Server running at: http://{local_ip}:3733")
    
    # Use socketio.run instead of waitress
    socketio.run(app, host="0.0.0.0", port=3733, allow_unsafe_werkzeug=True)
