from FunkyFileFolder.FunkyFile import FunkyFile
import pathlib
from datetime import date, time
import os
from bs4 import BeautifulSoup as BSoup

class FunkyFolder(FunkyFile):

    def __init__(self, scrapper,  id, name, baseUrl):
        FunkyFile.__init__(self, scrapper,  id, name, baseUrl)
        self.fileList = []

    def download(self, savePath):
        path = savePath + "/" +  self.name
        pathlib.Path(path).mkdir(exist_ok=True)
        for file in self.fileList:
            file.download(path)

    def _get_downloadUrl(self):
        if not self.is_root():
            return FunkyFile._get_downloadUrl(self)
        else:
            return self.baseUrl



    def init_files(self):
        basePage = self.scrapper.get_page(self._get_downloadUrl())
        soup = BSoup(basePage, "html.parser")
        rows = soup.find_all("tr")
        rows.pop(0)
        for row in rows:


            try:
                columns = row.findAll("td")
                anchor = columns[0].find("a")
                title = anchor["title"]
                id = anchor["href"].split("id=")[1]
                """
                timeInfo = columns[len(columns)-1].text.split(' ')
                ftime = time.fromisoformat(timeInfo[len(timeInfo)-1])
                fdate = date.fromisoformat(timeInfo[len(timeInfo)-2])
                print(ftime)
                print(fdate)
                """
                if("folder" in anchor.find("img")["src"]):
                    newFolder = FunkyFolder(self.scrapper,id, title ,self.baseUrl)
                    newFolder.init_files()
                    self.fileList.append(newFolder)

                else:
                    newFile = FunkyFile(self.scrapper, id, title, self.baseUrl)
                    self.fileList.append(newFile)
            except (TypeError, IndexError) as e:

                None

                #print("WARN : empty or incomplete row")



    def is_root(self):
        return self.id==None

    def get_funkyFileList(self):
        funkyFileList = []
        for fileObj in self.fileList :
            if type(fileObj) == FunkyFile:
                funkyFileList.append(fileObj)
            else:
                newFileList = fileObj.get_funkyFileList()
                if newFileList != None:

                    funkyFileList.extend(newFileList)
        return funkyFileList