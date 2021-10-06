from flask import Flask, request, make_response, jsonify, send_file, after_this_request
import pandas
import pdfkit
import htmlmin
import os
import datetime
app = Flask(__name__)
MYSTYLE = ""
PATH_TO_PDF = "/root/pdf_reports" if os.name != 'nt' else "tmp"
@app.route('/hello')
def hello():
    return 'Hello World'

@app.route("/api/csv_pdf", methods=["POST"])
def csv_pdf():
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    if not request.files:
        return "{'message':'No files attached.'}", 400
    
    file = request.files["csv"]
    if not file:
        return "{'message':'No files attached.'}", 400
    filename, extension = file.filename.split(".")
    if extension.lower() != 'csv':
        return f"{{'message':'Wrong file type `{extension}`.'}}"
    
    df = pandas.read_csv(file) 
    
    html = htmlmin.minify(f"<style>{MYSTYLE}</style><p>Report generated at : {current_time}</p>\
        {df.to_html(classes='mystyle')}<p>Report generated by Accops Reporting Server.</p>")
    pdfkit.from_string(html, f"{PATH_TO_PDF}/temp.pdf", options={"quiet": ""})
    return jsonify({"message":"File generated.", "path":PATH_TO_PDF+'/temp.pdf'}), 200





if __name__ == "__main__":
    with open("mystyle.css", "r") as f:
        MYSTYLE = f.read()
    app.run(host='0.0.0.0', port=5000, debug=True)