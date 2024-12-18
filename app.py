from flask import Flask, render_template, request, session, send_file
from git_repo import *
from sql_operations import *
from io import BytesIO
import mimetypes
import os
import time
import requests
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)


@app.route('/')
def main():
    return render_template('key.html')

@app.route('/check_shit', methods=['POST', 'GET'])
def check_shit():
    session['username'] = request.form['key']
    print(session['username'])
    
    data = retrive(session['username'])
    if data == 'new':
        return render_template('index.html', user=session['username'])
    
    return render_template('index.html', user=session['username'], data=data)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if 'username' in session:
        print("Session username:", session['username'])
    else:
        print("No username in session")
    
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part in the form!'
        
        file = request.files['file']
        
        if file.filename == '':
            return 'No selected file!'
        
        # Check the file size (100MB = 100 * 1024 * 1024 bytes)
        file_size = len(file.read())
        file.seek(0)  # Reset file pointer after reading size

        if file_size > 100 * 1024 * 1024:
            return 'File exceeds the maximum allowed size of 100MB!'
        
        file_content = file.read()
        file_name = file.filename
        success, file_name = upload_to_github(file_content, file_name)

        print("File upload success:", success)
        
        if success:
            insert(session['username'], file_name)
            return render_template('index.html', status='uploaded', user=session['username'], data=retrive(session['username']))
        else:
            return render_template('index.html', status='Not uploaded/File Name Already exists', user=session['username'], data=retrive(session['username']))


@app.route('/download', methods=['POST'])
def download_file():
    if 'username' not in session:
        return render_template('key.html', status='Session expired. Please log in again.')

    file_name = request.form["file_name"]
    print("Attempting to download file:", file_name)
    
    # Ensure the URL is correct
    file_url = f"https://raw.githubusercontent.com/Bskn1411/files/main/hell/{file_name}"

    try:
        response = requests.get(file_url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        filename = os.path.basename(file_name)
        mime_type, _ = mimetypes.guess_type(filename)
        mime_type = mime_type or 'application/octet-stream'

        file_content = BytesIO(response.content)
        return send_file(file_content, mimetype=mime_type, as_attachment=True, download_name=filename)

    except requests.RequestException as e:
        print(f"Error fetching file: {e}")
        return render_template(
            'index.html',
            status='Unable to Download. Ensure the file exists in the repository.',
            user=session['username'],
            data=retrive(session['username'])
        )

# @app.route('/download', methods=['GET', 'POST'])
# def download_file():
#     file_name = request.form["file_name"]
#     print("entered to download file:", file_name)
#     file_url = f"https://raw.githubusercontent.com/Bskn1411/files/main/hell/{file_name}"
#     # file_url = f"https://raw.githubusercontent.com/Bskn1411/files/contents/hell/{file_name}"
#     try:
#         response = requests.get(file_url)
#         response.raise_for_status()
            
#         filename = os.path.basename(file_url)
#         mime_type, _ = mimetypes.guess_type(filename)
#         if mime_type is None:
#             mime_type = 'application/octet-stream'
            
#         file_content = BytesIO(response.content)
#         return send_file(file_content, mimetype=mime_type, as_attachment=True, download_name=filename)
        
#     except requests.RequestException as e:
#         print(f"Error fetching file: {e}")
#         return render_template('index.html', status='Unable to Download', user=session['username'], data=retrive(session['username']))


@app.route('/view', methods=['GET', 'POST'])
def view():
    file_name = request.form["file_name"]
    file_url = f"https://raw.githubusercontent.com/Bskn1411/files/main/hell/{file_name}"
    
    response = requests.get(file_url)

    if response.status_code == 200:
        mime_type, _ = mimetypes.guess_type(file_name)
        if mime_type is None:
            mime_type = 'application/pdf'

        # Return the PDF content directly
        return Response(response.content, mimetype=mime_type)
    else:
        print(f"Failed to retrieve the PDF. Status code: {response.status_code}")
        return render_template('index.html', status='Failed to retrieve PDF', user=session['username'], data=retrive(session['username']))
# @app.route('/view', methods=['GET', 'POST'])
# def view():
#     file_name = request.form["file_name"]
#     file_url = f"https://raw.githubusercontent.com/Bskn1411/files/main/hell/{file_name}"
    
#     response = requests.get(file_url)

#     if response.status_code == 200:
#         # Save the PDF temporarily
#         temp_pdf_path = 'temp_pdf.pdf'
#         with open(temp_pdf_path, 'wb') as f:
#             f.write(response.content)
#         return render_template('view_pdf.html', pdf_path=temp_pdf_path)
#     else:
#         return "Failed to retrieve the PDF."

# @app.route('/display/<path:pdf_path>')
# def display_pdf(pdf_path):
#     return send_file(pdf_path, as_attachment=False)


@app.route('/fuck_off', methods=['POST'])
def delete_file_route():
    if 'username' not in session:
        return render_template('key.html', status='Session expired. Please log in again.')

    file_name = request.form["file_name"]
    print("Attempting to delete file:", file_name)
    
    # First delete from your SQL database
    db_result = delete_file(session['username'], file_name)
    
    # Then delete from GitHub
    if db_result:
        github_result = delete_from_github(f"hell/{file_name}")
        
        if github_result:
            return render_template(
                'index.html',
                status=f'File "{file_name}" successfully removed.',
                user=session['username'],
                data=retrive(session['username'])
            )
        else:
            return render_template(
                'index.html',
                status=f'Error: File "{file_name}" removed locally but failed to delete from GitHub.',
                user=session['username'],
                data=retrive(session['username'])
            )

    return render_template(
        'index.html',
        status=f'Error: Unable to remove file "{file_name}".',
        user=session['username'],
        data=retrive(session['username'])
    )

# @app.route('/fuck_off', methods=['GET', 'POST'])
# def fuck_off():
#     file_name = request.form["file_name"]
#     print("Deleting file" + file_name)
#     result = delete_file(session['username'], file_name)
#     if result:
        
#         result = delete_from_github(file_name)
        
#         if result:
#             return render_template('index.html', status='Removed', user=session['username'], data=retrive(session['username']))
    
#     return render_template('index.html', status='Unable to Remove', user=session['username'], data=retrive(session['username']))


if __name__ == '__main__':
        app.run()
