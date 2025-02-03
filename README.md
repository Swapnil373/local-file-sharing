# Local File Sharing Server 🚀

A simple, local file sharing server built with **Flask** and **Socket.IO**. Share files with your friends on the same network without relying on external services. Enjoy features like drag-and-drop file uploads, live updates, file previews, and LAN discovery via QR code or network broadcast.

## Features ✨

- **File Upload:** Easily drag and drop files or use the file picker.
- **File Download:** Download files individually or as a ZIP archive.
- **File Deletion:** Remove unwanted files quickly.
- **LAN Discovery:** Automatically share your server via QR code or network discovery.
- **Real-Time Updates:** Live notifications for uploads and deletions using Socket.IO.

## Requirements 📦

- **Python 3.x**
- **Flask**
- **Flask-SocketIO**
- **Pillow** (for image previews)
- **qrcode** (for QR Code generation)

## Installation 🔧

1. **Clone the repository:**

    ```bash
    git clone https://github.com/Swapnil373/local-file-sharing.git
    cd local-file-sharing
    ```

2. **Install the required Python libraries:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Run the Flask server:**

    ```bash
    python app.py
    ```

    The server will start on `http://<your_local_ip>:3733`. You can access it from any device on the same local network.

## Usage 💡

### Upload Files

- Visit the homepage (`http://<your_local_ip>:3733`) and drag & drop your files into the upload area, or select files via the file picker.

### Download Files

- Files are displayed on the homepage. Click the download button next to any file to download it.

### Delete Files

- Click the trash icon next to a file to delete it.

### Download All Files as ZIP

- Click the **Download All as ZIP** button to download all files in one archive.

### QR Code for Easy Access

- Scan the QR code on the homepage 📱 to quickly connect to the server from your mobile device.

## Releases
- [Version 1.0.0](https://github.com/yourusername/yourproject/releases/tag/v1.0.0) - First stable release

## Installation
1. Clone the repo: `git clone https://github.com/yourusername/yourproject.git`
2. Install dependencies: `pip install -r requirements.txt`

## Running Locally
To start the server, run:
```bash
python app.py
```

## Security 🔒

This server is designed for use in a trusted, private network and does not include advanced security measures. For safety, only use it within a secure, private environment.

## License 📄

This project is open-source and available under the [MIT License](LICENSE).

## Acknowledgements 🙏

- **Chat GPT-4o & Claude 3.5 sonnet:**
