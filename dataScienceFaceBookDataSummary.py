import os
import pdfplumber
from transformers import BartForConditionalGeneration, BartTokenizer


directory_path = "H://BSEReports//announcements//02032025//122117"
model_name = "facebook/bart-large-cnn"
model = BartForConditionalGeneration.from_pretrained(model_name)
tokenizer = BartTokenizer.from_pretrained(model_name)

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

def summarize_text(text, max_length=130):
    inputs = tokenizer.encode("summarize: " + text, return_tensors="pt", max_length=1024, truncation=True)
    summary_ids = model.generate(inputs, max_length=max_length, min_length=30, length_penalty=2.0, num_beams=4, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

def summarize_pdfs_from_directory(directory_path, max_length=130):
    summaries = {}
    for filename in os.listdir(directory_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(directory_path, filename)
            text = extract_text_from_pdf(pdf_path)
            summary = summarize_text(text, max_length=max_length)
            fullFileName = directory_path+ "//" + filename; 
            summaries[fullFileName] = summary
    return summaries

def save_summary(text_summary, html_summary, filename):
    txt_filename = filename + ".txt"
    with open(txt_filename, "w") as txt_file:
        txt_file.write(text_summary)
    print(f"Summary saved as {txt_filename}")

    html_filename = filename + ".html"
    with open(html_filename, "w") as html_file:
        html_file.write(f"<html><body>{html_summary}</body></html>")
    print(f"Summary saved as {html_filename}")

def execute_pdf_summaries(directory_path):
    pdf_summaries = summarize_pdfs_from_directory(directory_path)
    text_summaries = '';
    html_summaries = '';

    for filename, summary in pdf_summaries.items():
        onlineFileName = "https://www.bseindia.com/xml-data/corpfiling/AttachLive/" +getFileNameFromPath(filename)
        print(f"Summary for {filename}:\n{summary}\n")
        text_summaries = text_summaries + "Summary for offline-filename = " + filename + "\n online-filename = " + onlineFileName + "\n "+summary +"\n For more you can check the details in the file section \n"
        html_summaries = html_summaries + "<strong>Summary for  offline-filename = <a href = "+filename+" target='_blank'>"+filename + "</a></strong> </br> online-filename = <a href = "+onlineFileName+" target='_blank'>"+onlineFileName + "</a></strong>   </br><p> "+summary+ "</p><br><p>For more you can check the details in the file section </p></br>"
    
    save_summary(text_summaries, html_summaries,directory_path+ "//" + "pdf_facebook_model_summary")


def executePdfSummary(pdfFilesDirectoryPath):
    execute_pdf_summaries(pdfFilesDirectoryPath)

def getFileNameFromPath(file_path):
    file_name = file_path.split("//")[-1]
    split_file_name = file_name.split("_")
    last_element = split_file_name[-1]
    print("The last element is:", last_element)
    return last_element;


# executePdfSummary(directory_path);