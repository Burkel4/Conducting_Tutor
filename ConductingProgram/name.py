import cv2

def initializeVideo():
    videoFileName = '4-4stacatto(3).mp4'
    return videoFileName

def videoPlotName():
    videoFileName = initializeVideo()
    plotName = videoFileName + '_Full_coordinates_plot'
    return plotName

def videoSwayPlotName():
    videoFileName = initializeVideo()
    swayPlotName = videoFileName + '_Full_Sway_plot'
    return swayPlotName

def videoHandsPlot_XName():
    videoFileName = initializeVideo()
    handsPlotName_X = videoFileName + '_Full_Hands_plot_X'  
    return handsPlotName_X

def videohandsPlotName_YName():
    videoFileName = initializeVideo()
    handsPlotName_Y = videoFileName + '_Full_Hands_plot_Y'
    return handsPlotName_Y

def videoBeatPlotName(): #beats name
    videoFileName = initializeVideo()
    beatPlotName = videoFileName + '_Full_coordinates_plot'
    return beatPlotName

def videoConductPathName():
    videoFileName = initializeVideo()
    conductPath = videoFileName + '_Full_conducting_path' 
    return conductPath

        