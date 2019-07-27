import PIL.ImageGrab
import PIL.ImageOps
from PIL import Image
import pytesseract
from numpy import *
import os
import time
import win32api, win32con

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract'

EMPTY_POS = (970,50)
SHOP_BUTTON_POS = (1750, 980)

#camDistance is 874
#camPitch is 66
#outline on
#maximumGraphic

SHOP_BOUND = {
    ## width is 213, height is 68
    ## y is 192
    1 : 175,
    2 : 495,
    3 : 816,
    4 : 1135,
    5 : 1455
    }

UI_BOUND = {
    "shopButtonBound" : (1717,954,1717+64,954+60),
    "goldBound" : (1640,953,1640+50,953+53),
    "levelBound" : (1807,592,1807+46,592+51),
    "roundBound" : (1490,20,1490+240,20+45),    
    "healthBound" : (340,230,340+70,230+33),
    "roundStateBound" : (1495,68,1495+233,68+42)
}

REFERENCE_DICT = {
	"shopOpened" : 72474,
	"shopClosed" : 74407
}

currentShopHeroes = {
	1 : '',
	2 : '',
	3 : '',
	4 : '',
	5 : '',
}

gameState = {
	'isShopOpen' : True,
	'gold' : 1,
	'level' : 1,
	'round' : 1,
	'health' : 100
}

def imgToText(filename):    
    text = pytesseract.image_to_string(PIL.Image.open(filename))  
    return text

def imgToNumber(filename):    
    text = pytesseract.image_to_string(PIL.Image.open(filename), config='--psm 10 -c tessedit_char_whitelist=0123456789')  
    return text   

def imgToNumberUniform(filename):    
    text = pytesseract.image_to_string(PIL.Image.open(filename), config='--psm 6 -c tessedit_char_whitelist=0123456789')  
    return text   

def openShop():
	mousePos(EMPTY_POS)
	leftClick()
	mousePos(SHOP_BUTTON_POS)
	leftClick()
	mousePos(EMPTY_POS)
	gameState['isShopOpen'] = True 

def closeShop():
	mousePos(EMPTY_POS)
	leftClick()
	gameState['isShopOpen'] = False	

def updateShopHeroes():
	grabWholeShop()
	for i in range(1,6):
		filename = 'shop_' + str(i) + '.jpg'
		print(imgToText(filename))
		currentShopHeroes[i] = imgToText(filename)

def updateUIElements():
	grabWholeUI()		
	GOLD = 'ui_' + 'goldBound' + '.jpg'
	LEVEL = 'ui_' + 'levelBound' + '.jpg'
	HEALTH = 'ui_' + 'healthBound' + '.jpg'
	ROUND = 'ui_' + 'roundBound' + '.jpg'
	ROUND_STATE = 'ui_' + 'roundStateBound' + '.jpg'
	
	print(GOLD + ' : ' + imgToNumber(GOLD))
	print(LEVEL + ' : ' + imgToNumberUniform(LEVEL))
	print(HEALTH + ' : ' + imgToNumber(HEALTH))
	print(ROUND + ' : ' + imgToNumber(ROUND))
	print(ROUND_STATE + ' : ' + imgToText(ROUND_STATE))




def grabUI(element):
    box = UI_BOUND[element]
    im = PIL.ImageOps.grayscale(PIL.ImageGrab.grab(box))
    im = im.resize([(box[2] - box[0]) * 2, (box[3]-box[1]) * 2],PIL.Image.ANTIALIAS)    
    a = array(im.getcolors())
    a = a.sum()
    #print(a)

    thresh = 100
    fn = lambda x : 255 if x > thresh else 0
    im = im.convert('L').point(fn, mode='1')

    im.save(os.getcwd() + '\\ui_' + element + '.jpg', 'JPEG', quality=95)
    return a   

def grabWholeUI():
	openShop()
	closeShop()
	time.sleep(0.2)
	for element in UI_BOUND.keys():
 		grabUI(element)
	openShop()
	time.sleep(0.2)
	grabUI("levelBound")
	closeShop()

def grabShop(slot):
    box = (SHOP_BOUND[slot],195,SHOP_BOUND[slot]+184,195+60)
    im = PIL.ImageOps.grayscale(PIL.ImageGrab.grab(box))
    im = im.resize([213*2,68*2],PIL.Image.ANTIALIAS)
    a = array(im.getcolors())
    a = a.sum()
    #print(a)
    im.save(os.getcwd() + '\\shop_' + str(slot) + '.jpg', 'JPEG', quality=95)
    return a  

def grabWholeShop():
    for i in range(1,6):
        grabShop(i)

def bench_select(slot):
    #mousePos(bench[slot])
    leftClick()
    time.sleep(0.1)

def leftClick():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    print('left clicked')

def leftDown():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(.1)
    print('left Down')

def leftUp():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    time.sleep(.1)
    print('left release')

def mousePos(cord):
    win32api.SetCursorPos((cord[0], cord[1]))

def get_cords():
    x,y = win32api.GetCursorPos()
    x = x
    y = y
    print(x,y)

def startGame():
    #location of first menu
    mousePos((355, 917))
    leftClick()
    time.sleep(.1)
     
    #location of second menu
    mousePos((963, 562))
    leftClick()
    time.sleep(.1)
     
    #location of third menu
    mousePos((1469, 417))
    leftClick()
    time.sleep(.1)

 
def main():
    pass
 
if __name__ == '__main__':
    main()
