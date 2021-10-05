from flask import Flask, request, make_response, jsonify, send_file
import pandas
import pdfkit
import os
app = Flask(__name__)
MYSTYLE = ""
@app.route('/hello')
def hello():
    return 'Hello World'

@app.route("/api/csv_pdf", methods=["POST"])
def csv_pdf():
    if not request.files:
        return "{'message':'No files attached.'}", 400

    file = request.files["csv"]
    filename = file.filename.split(".")[0]
    df = pandas.read_csv(file) 
    res = "<style>{}</style>{}".format(MYSTYLE, df.to_html(classes="mystyle"))
    pdfkit.from_string(res, f"tmp/{filename}.pdf", options={"quiet": ""})
    return send_file(f"tmp/{filename}.pdf", download_name=f'{filename}.pdf')


@app.after_request
def delete_files(response):
    if request.endpoint=="csv_pdf": 
        os.remove("tmp/*")
    return response


if __name__ == "__main__":
    with open("mystyle.css", "r") as f:
        MYSTYLE = f.read()
    app.run(host='0.0.0.0', port=5000, debug=True)