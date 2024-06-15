#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from flask import Flask, render_template, request, send_file, redirect, url_for
import cv2
import os
import rembg
import tempfile
from pytube import YouTube
import re


# In[ ]:


app = Flask(__name__)


# In[ ]:


#BACKGROUND REMOVER HELPER FUNC


# In[ ]:


def check_image_loaded(image_path):
    # Check if the image was loaded successfully
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Unable to load image '{image_path}'.")
        return False
    return True

def remove_background(image_path, output_path):
    # Read the input image
    with open(image_path, "rb") as f:
        img = rembg.remove(f.read())

    # Write the background removed image to the output path
    with open(output_path, "wb") as f:
        f.write(img)

    print(f"Background removed. Result saved as {output_path}")


# In[ ]:


#YOUTUBE 2 MP3 CONVERT HELPER FUNC


# In[ ]:


def download_progress(stream, chunk, bytes_remaining):
    # Calculate the percentage of downloaded bytes
    bytes_downloaded = stream.filesize - bytes_remaining
    percent = (bytes_downloaded / stream.filesize) * 100
    print(f"\r{percent:.1f}% downloaded", end="", flush=True)

def download_youtube_audio(video_url):
    yt = YouTube(video_url)
    stream = yt.streams.filter(only_audio=True).first()
    stream.download(output_path='.')
    stream.register_on_progress_callback(download_progress)
    print("\n")  # Add a newline after download completion

def is_youtube_url(url):
    # Regular expression pattern for matching YouTube video URLs
    youtube_pattern = r'^(https?://)?(www\.)?youtube\.com/'
    # Check if the URL matches the pattern
    if re.match(youtube_pattern, url):
        return True
    else:
        return False


# In[ ]:


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    # Check if the file is a valid image
    filename = file.filename
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    if '.' not in filename or filename.split('.')[-1].lower() not in allowed_extensions:
        return 'Invalid file format. Only PNG, JPG, JPEG, and GIF files are allowed.'
    # Save the uploaded image to a temporary location
    upload_folder = 'uploads'
    os.makedirs(upload_folder, exist_ok=True)
    upload_path = os.path.join(upload_folder, filename)
    file.save(upload_path)
    # Process the uploaded image to remove background
    output_folder = 'background_removal_result'
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}_background_removed.png")
    # Check if the image was loaded successfully
    is_loaded = check_image_loaded(upload_path)
    if is_loaded:
        # Remove background and save the result
        remove_background(upload_path, output_path)
        # Return the background-removed image for download
        return send_file(output_path, as_attachment=True)
    else:
        return 'Error processing uploaded image'
    

@app.route('/convert', methods=['POST'])
def convert():
    youtube_url = request.form.get('youtube_url')
     # Check if youtube_url is empty or not provided
    if not youtube_url:
        return 'Error: YouTube URL is missing or empty'
    if is_youtube_url(youtube_url):
        print ("VALID")
    else:
        print("Invalad url")
    
    # Process the YouTube URL, e.g., perform conversion to MP3
    # Add your logic here based on what you want to do with the URL
    # For now, let's just print it
    print(f"Received YouTube URL: {youtube_url}")
    # Redirect back to the homepage or another page after processing
    return "Under construction"        #redirect(url_for('index.html'))


# In[ ]:


if __name__ =="__main__":
    #app.run()
    app.run(debug=True, port=5000, use_reloader=False) # Set port to 5000
    
    #https://www.youtube.com/watch?v=SF-Q9ucn9ko <-- Example url


# In[ ]:




