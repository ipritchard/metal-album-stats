import os
import pickle

import datetime
import metallum
import pandas as pd
import wikipedia

from BandSearchIds import metallumIndexLookup

os.chdir(os.path.dirname(__file__))

excelSheetFile = r"./bandlist.csv"
bandDictPickleDir = r'./metallum_pickles'
plotOutDir = r'./Plots'

def getMetallumBandInfo(bandName):

    noResults = []
    bandSearch = metallum.band_search(bandName)
    if len(bandSearch) == 1:
        bandInfo = bandSearch[0].get()
    elif len(bandSearch) == 0:
        noResults.append(bandName)
        bandInfo = None
    else:
        bandIndex = metallumIndexLookup[bandName]
        if bandIndex is None:
            bandInfo = None
        else:
            bandInfo = bandSearch[bandIndex].get()

    return bandInfo


def scrapeMetallumInfo(aBand, bandInfo):

    metallumBandDict = {}

    metallumBandDict['country'] = bandInfo.country
    metallumBandDict['formedIn'] = bandInfo.formed_in
    metallumBandDict['genres'] = bandInfo.genres
    metallumBandDict['recordLabel'] = bandInfo.label
    metallumBandDict['location'] = bandInfo.location
    metallumBandDict['status'] = bandInfo.status
    metallumBandDict['themes'] = bandInfo.themes

    metallumBandDict['albums'] = {}
    for album in bandInfo.albums:
        albumDict = {}
        albumDict['title'] = album.title
        albumDict['year'] = album.year
        albumDict['type'] = album.type
        albumDict['tracks'] = {}
        try:
            for track in album.tracks:
                trackDict = {}
                trackDict['title'] = track.title
                trackDict['fullTitle'] = track.full_title
                trackDict['durationSecs'] = track.duration
                trackDict['trackNumber'] = track.number
                try:
                    trackDict['lyrics'] = track.lyrics._content
                except:
                    pass
                albumDict['tracks'][track.title] = trackDict
        except:
            pass
        metallumBandDict['albums'][album.title] = albumDict

    return metallumBandDict


def getBandList(excelSheetFile):

    bandDf = pd.read_csv(excelSheetFile)
    bandList = sorted(list(set(bandDf.Band.values.tolist())))

    return bandList


def writePickleDict(aBand, metallumDict):

    with open(os.path.join(bandDictPickleDir, aBand + '.pickle'), 'wb') as f:
        pickle.dump(metallumDict, f, protocol=pickle.HIGHEST_PROTOCOL)

    return


def readPickleDict(aBand):

    with open(os.path.join(bandDictPickleDir, aBand + '.pickle'), 'rb') as f:
        metallumDict = pickle.load(f)

    return metallumDict


def collectMetallumInfo(bandList):

    noBandInfoList = []
    for aBand in bandList:
        if os.path.exists(os.path.join(bandDictPickleDir, aBand + '.pickle')):
            print(aBand, "pickle file found - skipping.")
            continue
        metallumDict = {}
        print("Processing", aBand)
        bandInfo = getMetallumBandInfo(aBand)
        if bandInfo is None:
            print("No band info found for", aBand, "- skipping.")
            noBandInfoList.append(aBand)
            continue
        metallumDict[aBand] = scrapeMetallumInfo(aBand, bandInfo)
        writePickleDict(aBand, metallumDict)

    return noBandInfoList


def buildMetallumBandDf(allBands):

    bandInfoList = []
    colNames = ['bandName', 'country', 'formedIn', 'genres', 'label',
                'location', 'status', 'themes', 'numTotalAlbums']
    for aBand in allBands:

        try:
            bandDict = readPickleDict(aBand)[aBand]
        except:
            continue
        country = bandDict['country']
        formationYear = bandDict['formedIn']
        genres = bandDict['genres']
        label = bandDict['recordLabel']
        location = bandDict['location']
        status = bandDict['status']
        themes = bandDict['themes']
        numTotalAlbums = len(bandDict['albums'])
        bandInfoList.append([aBand, country, formationYear, genres, label,
                             location, status, themes, numTotalAlbums])

    metallumDf = pd.DataFrame(bandInfoList, columns=colNames)

    return metallumDf


def plotCountryOfOriginHist(metallumDf):

    countryCounts = []
    countries = sorted(metallumDf.country.unique())
    for country in countries:
        countryDf = metallumDf.loc[metallumDf.country == country]
        numBandsInCountry = len(countryDf)
        countryCounts.append([country, numBandsInCountry])
    countryDf = pd.DataFrame(countryCounts, columns=['country', 'count'])
    countryDf.sort_values(by='count', ascending=False, inplace=True)
    countryDf.plot.bar(x='country', y='count')
    print('myass')
    
    return


def doPlots(metallumDf):

    plotCountryOfOriginHist(metallumDf)

    return


def main():

    if not os.path.exists(plotOutDir):
        os.makedirs(plotOutDir)

    allBands = getBandList(excelSheetFile)
    collectMetallumInfo(allBands)
    metallumDf = buildMetallumBandDf(allBands)
    doPlots(metallumDf)


    return


if __name__ == '__main__':

    main()

