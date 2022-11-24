
import os
import tomli
import tomli_w
import pandas as pd



# list all mods toml file names and load them in 
def listLoadTomls(modTomlFolder):
    fileNames = os.listdir(modTomlFolder)
    fileNames.sort()
    allTomls = {} 
    for fn in fileNames:
        tomlPath = os.path.join(modTomlFolder, fn)
        with open(tomlPath, "rb") as f:
            tomlDict = tomli.load(f)
            allTomls.update({fn: tomlDict})
            f.close()
    print("Loaded", len(allTomls), "mods toml", sep=" ")
    return (fileNames, allTomls)



def genLoadExcel(excelPath, fileNames, allTomls, url):
    if os.path.exists(excelPath):
        df = pd.read_excel(excelPath) 
        print("Read existing excel file: " + excelPath)
    else:
        dict = {"name":[], "filename":[], "url":[], "side":[]}
        df = pd.DataFrame(dict)
        print("No existing excel file, generating")
    df = df[df["filename"].isin(fileNames)] # remove removed mods from excel
    fnIsMember = pd.DataFrame(fileNames)
    fnIsMember = fnIsMember[~fnIsMember[0].isin(df["filename"])]
    newFileNames = fnIsMember[0].values.tolist() # get list of newly added mods that is not in excel

    for fn in newFileNames:
        toml = allTomls[fn]
        fullUrl = url + str(toml["update"]["curseforge"]["project-id"])
        newRow = {
            "name":[toml["name"]], 
            "filename":[fn],
            "url":[f"=HYPERLINK(\"{fullUrl}\",\"{fullUrl}\")"],
            "side":[toml["side"]]
        }
        df = pd.concat([df, pd.DataFrame(newRow)])
    df.to_excel(excelPath, index=False)
    print(f"Updated excel file containing {len(df)} mods")
    return df

def applyChangesToFile(dataframe, modTomlFolder, allTomls):
    for i in range(len(dataframe)):
        side = dataframe.iloc[i, :]["side"]
        filename = dataframe.iloc[i, :]["filename"]
        toml = allTomls[filename] 
        # only update when change needed
        if toml["side"] != side:
            toml["side"] = side
            tomlPath = os.path.join(modTomlFolder, filename)
            with open(tomlPath, "wb") as f:
                tomli_w.dump(toml, f)
                print("Applied changes: " + filename)



CURSEFORGE_URL = "https://www.curseforge.com/projects/"
SPREADSHEET_FILE = os.path.join(".", "modlist.xlsx")
MOD_PATH = os.path.join(".","mods")

(fileNames, allTomls) = listLoadTomls(MOD_PATH)
dataframe = genLoadExcel(SPREADSHEET_FILE, fileNames, allTomls, CURSEFORGE_URL)
pd.set_option('display.max_rows', None)
print(dataframe)
print()
applyChangesToFile(dataframe, MOD_PATH, allTomls)
