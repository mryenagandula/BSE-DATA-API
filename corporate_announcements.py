from bse import BSE
import csv
import logging as log
from constants import ANNOUNCEMENTS_HEADERS
from bse_utils import getDictkeyAndValue

def loadBSEAnnouncements(filePath):
    print("Started Fetching BSE announcements..")
    bse = BSE(download_folder='./')
    bse_announcements = bse.announcements();
    print("Type announcements data is ",type(bse_announcements));
    for key, value in bse_announcements.items():
        list_length = len(value)
        print("Type of key is ",type(key), " and type of value is ",type(value));
        print('items in table with key and length of value is',key,list_length);

        if(list_length > 1) :
            writeDataToCSV(filePath, value);
    print("Completed Fetching BSE announcements..")
    pass



def writeDataToCSV(fileName: str, result) :
    with open(fileName, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f);
        log.info("Started writing data to CSV");
        writer.writerow(ANNOUNCEMENTS_HEADERS);
        
        for data in result :
            writer.writerow([
                getDictkeyAndValue("NEWSID",data),
                getDictkeyAndValue("SCRIP_CD",data),
                getStockSymbol(getDictkeyAndValue("SCRIP_CD",data)),
                getDictkeyAndValue("XML_NAME",data),
                getDictkeyAndValue("NEWSSUB",data),
                getDictkeyAndValue("DT_TM",data),
                getDictkeyAndValue("NEWS_DT",data),
                getDictkeyAndValue("CRITICALNEWS",data),
                getDictkeyAndValue("ANNOUNCEMENT_TYPE",data),
                getDictkeyAndValue("QUARTER_ID",data),
                getDictkeyAndValue("FILESTATUS",data),
                getFullAttachmentUrl(getDictkeyAndValue("ATTACHMENTNAME",data)),
                getDictkeyAndValue("MORE",data),
                getDictkeyAndValue("HEADLINE",data),
                getDictkeyAndValue("CATEGORYNAME",data),
                getDictkeyAndValue("OLD",data),
                getDictkeyAndValue("RN",data),
                getDictkeyAndValue("PDFFLAG",data),
                getDictkeyAndValue("NSURL",data),
                getDictkeyAndValue("SLONGNAME",data),
                getDictkeyAndValue("AGENDA_ID",data),
                getDictkeyAndValue("TotalPageCnt",data),
                getDictkeyAndValue("News_submission_dt",data),
                getDictkeyAndValue("DissemDT",data),
                getDictkeyAndValue("TimeDiff",data),
                getDictkeyAndValue("Fld_Attachsize",data),
                getDictkeyAndValue("SUBCATNAME",data),
                getDictkeyAndValue("AUDIO_VIDEO_FILE", data)
            ]);
        log.info("Completed writing data to CSV")
        log.info(f"Successfully Saved the file to specified directory {fileName}")


def getFullAttachmentUrl(attachmentName):
    if not attachmentName:
        return "";
    url = 'https://www.bseindia.com/xml-data/corpfiling/AttachLive/'+attachmentName;
    return url;

def getStockSymbol(scriptCode):
    if isinstance(scriptCode, str):
        if not scriptCode:
            return "";

    if scriptCode is None:
        return '';

    scriptName = '';
    try:
        bse = BSE(download_folder='./')
        scriptName = bse.getScripName(scriptCode);
    except ValueError as v:
        print("type of scriptCode", type(scriptCode))
        print(v)
    return scriptName;