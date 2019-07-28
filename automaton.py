import PIL.ImageGrab
import PIL.ImageOps
import PIL.ImageStat
from PIL import Image
import pytesseract
import numpy
import os
import time
import win32api, win32con
import skimage
import msvcrt


## IF SOMETHING GOES WRONG IT PROBABLY BECAUSE YOU LEVELED AND EMPTY TILE NO LONGER READ 'ae'

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract'

EMPTY_POS = (970,50)
SHOP_BUTTON_POS = (1750, 980)

#camDistance is 874
#camPitch is 66
#outline on
#maximumGraphic

KNIGHT_COMP = ['OMNIKNIGHT','LUNA','ABADDON','DRAGONKNIGHT','CHAOSKNIGH','BATRIDER','NECROPHOS','VIPER']

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
    "roundStateBound" : (1495,68,1495+233,68+42),
    "unitStarBound" : (371,35,372,36),
    "unitNameBound" : (260,53,260+230,53+37)
}

REFERENCE_DICT = {
	"oneStar" : (45000,46000),
	"twoStar" : 74407,
	"threeStar" : (59000,61000)
}

BOARD_POS = {	1 : {1:(629,443), 2:(723,443), 3:(815,443), 4:(908,443), 5:(1007,443), 6:(1102,443), 7:(1197,443), 8:(1292,443)},
				2 : {1:(612,545), 2:(706,545), 3:(811,545), 4:(910,545), 5:(1005,545), 6:(1113,545), 7:(1211,545), 8:(1307,545)},
				3 : {1:(591,642), 2:(696,645), 3:(803,646), 4:(904,645), 5:(1009,646), 6:(1113,645), 7:(1226,645), 8:(1324,645)},
        		4 : {1:(568,745), 2:(678,752), 3:(794,755), 4:(905,754), 5:(1012,751), 6:(1129,757), 7:(1244,750), 8:(1353,747)}}

BENCH_POS = {	1: (438,998),
				2: (587,998),
				3: (738,998),
				4: (886,998),
				5: (1026,998),
				6: (1185,998),
				7: (1325,998),
				8: (1478,998)}


SHOP_POS = {	1: (323,460),
				2: (650,460),
				3: (950,460),
				4: (1287,460),
				5: (1600,460),
				6: (1828,614)}


currentBoardHeroes = {	1 : {1:['',1], 2:['',1], 3:['',1], 4:['',1], 5:['',1], 6:['',1], 7:['',1], 8:['',1]},
						2 : {1:['',1], 2:['',1], 3:['',1], 4:['',1], 5:['',1], 6:['',1], 7:['',1], 8:['',1]},
						3 : {1:['',1], 2:['',1], 3:['',1], 4:['',1], 5:['',1], 6:['',1], 7:['',1], 8:['',1]},
        				4 : {1:['',1], 2:['',1], 3:['',1], 4:['',1], 5:['',1], 6:['',1], 7:['',1], 8:['',1]}}

currentBenchHeroes = {
	1 : ['',1],
	2 : ['',1],
	3 : ['',1],
	4 : ['',1],
	5 : ['',1],
	6 : ['',1],
	7 : ['',1],
	8 : ['',1]
}

currentShopHeroes = {
	1 : '',
	2 : '',
	3 : '',
	4 : '',
	5 : ''
}

gameState = {
	'fourItemChoices' : 'False',
	'isShopOpen' : True,
	'goldBound' : 1,
	'levelBound' : 1,
	'roundBound' : 1,
	'healthBound' : 100,
	'roundStateBound' : ''
}

def buyUnit(slot):
	openShop()
	time.sleep(0.2)
	mousePos(SHOP_POS[slot])
	print('BUYING A UNIT IN SLOT ' + str(slot))
	leftClick()

def buyCompUnit(comp):
	grabWholeShop()
	for i in currentShopHeroes.keys():		
		if currentShopHeroes[i] in comp:
			print(currentShopHeroes[i] + ' in slot ' + str(i) + ' is in comp')
			buyUnit(i)		
		else:
			print(currentShopHeroes[i] + ' in slot ' + str(i) + ' is NOT in comp')

def buyExp():
	openShop()
	time.sleep(0.01)
	mousePos(SHOP_POS[6])
	leftClick()

def isLootUIOpen():
	grabUI('roundStateBound')
	if(gameState['roundStateBound'] == 'LOOTING'):
		return True
	return False


def imgToText(filename):    
    text = pytesseract.image_to_string(PIL.Image.open(filename))  
    return text

def imgToTextUniform(filename):    
    text = pytesseract.image_to_string(PIL.Image.open(filename), config='--psm 10 -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')  
    return text

def imgToNumber(filename):    
    text = pytesseract.image_to_string(PIL.Image.open(filename), config='--psm 10 -c tessedit_char_whitelist=0123456789')  
    return text   

def imgToNumberUniform(filename):    
    text = pytesseract.image_to_string(PIL.Image.open(filename), config='--psm 10')  
    return text   

def openShop():
	gameState['isShopOpen'] = True 
	mousePos(EMPTY_POS)
	leftClick()
	mousePos(SHOP_BUTTON_POS)
	leftClick()
	mousePos(EMPTY_POS)
	time.sleep(0.01)

def closeShop():
	gameState['isShopOpen'] = False	
	mousePos(EMPTY_POS)
	leftClick()
	time.sleep(0.01)
	

def compareImages(i1, i2):
	#i1 = PIL.Image.open(image1 + ".jpg")
	#i2 = PIL.Image.open(image2 + ".jpg")
	assert i1.mode == i2.mode, "Different kinds of images."
	assert i1.size == i2.size, "Different sizes."

	pairs = zip(i1.getdata(), i2.getdata())
	if len(i1.getbands()) == 1:
	    # for gray-scale jpegs
	    dif = sum(abs(p1-p2) for p1,p2 in pairs)	    
	else:
	    dif = sum(abs(c1-c2) for p1,p2 in pairs for c1,c2 in zip(p1,p2))	  
	 
	ncomponents = i1.size[0] * i1.size[1] * 3
	return (dif / 255.0 * 100) / ncomponents

def grabBench(slot):
	print('in bench slot ' + str(slot))
	closeShop()	
	bench_select(slot)
	info = grabSelectedUnitInfo()
	currentBenchHeroes[slot][0] = info[0]
	currentBenchHeroes[slot][1] = info[1]

def board_select(row, col):
	closeShop()
	mousePos(BOARD_POS[row][col])
	#time.sleep(0.01)
	leftClick()
	

def grabBoard(row, col):
	print('in board tile [' + str(row) + '][' + str(col) + ']')
	closeShop()
#	time.sleep(0.05)
	board_select(row, col)
	info = grabSelectedUnitInfo()
	currentBoardHeroes[row][col][0] = info[0]
	currentBoardHeroes[row][col][1] = info[1]

def grabWholeBoard():
	grabUI('roundStateBound')
	if gameState['roundStateBound'] == 'LOOTING':
		print("ERROR: TRIED TO GRAB BOARD WHILE ITEM SCREEN IS UP")
		exit()
	for r in range(1,5):
		for c in range(1,9):
			grabBoard(r,c)


def grabSelectedUnitInfo():
	if(gameState['isShopOpen']):
		return ('EMPTY',1)
	#bench_select(slot)
	closeShop()
	#time.sleep(0.1)
	box = UI_BOUND["unitStarBound"]
	im = PIL.ImageGrab.grab(box)

	im = im.resize([(box[2] - box[0]) * 2, (box[3]-box[1]) * 2],PIL.Image.ANTIALIAS)	

	im.save(os.getcwd() + '\\selectedUnitStar.jpg', 'JPEG', quality=95)
	
	threeStar = PIL.Image.open('threeStar.jpg')	
	oneStar = PIL.Image.open('oneStar.jpg')

	if(compareImages(im, oneStar) < 1):
		#print(compareImages(im, oneStar))
		print("there is a 1 stars")
		star = 1

	elif(compareImages(im, threeStar) < 1):
		#print(compareImages(im, threeStar))
		print("there a 3 stars")
		star = 3

	else:		
		print('there is a 2 star')
		star = 2

	box = UI_BOUND["unitNameBound"]
	im = PIL.ImageOps.grayscale(PIL.ImageGrab.grab(box))
	im = im.resize([(box[2] - box[0]) * 5, (box[3]-box[1]) * 5],PIL.Image.ANTIALIAS)

	thresh = 150
	fn = lambda x : 255 if x > thresh else 0
	im = im.convert('L').point(fn, mode='1')

	im.save(os.getcwd() + '\\selectedUnitName.jpg', 'JPEG', quality=95)
	name = imgToTextUniform("selectedUnitName.jpg")
	if(name == 'pye' or name == 'pys' or name == 'Dye'):
		name = 'Axe'
	elif(name == 'ae'):
		name = 'EMPTY'
	print(name)
	return (name, star)


def grabWholeBench():
	for i in range(1,9):
		grabBench(i)		

def grabUI(element):
	if(element != 'roundStateBound' and element != 'goldBound' and element != 'roundBound' and element != 'healthBound'):
		return
	closeShop()
	#time.sleep(0.01)
	box = UI_BOUND[element]
	im = PIL.ImageOps.grayscale(PIL.ImageGrab.grab(box))
	im = im.resize([(box[2] - box[0]) * 2, (box[3]-box[1]) * 2],PIL.Image.ANTIALIAS)    
	a = numpy.array(im.getcolors())
	a = a.sum()
	#print(a)
	
	# thresh = 120
	# fn = lambda x : 255 if x > thresh else 0
	# im = im.convert('L').point(fn, mode='1')

	im.save(os.getcwd() + '\\ui_' + element + '.jpg', 'JPEG', quality=95)

	filename = 'ui_' + element + '.jpg'

	result = imgToText(filename)
    

	gameState[element] = result
	print(element + ' : ' + result)

def grabLevel():
	openShop()
	#time.sleep(0.03)
	box = UI_BOUND['levelBound']
	im = PIL.ImageOps.grayscale(PIL.ImageGrab.grab(box))
	im = im.resize([(box[2] - box[0]) * 2, (box[3]-box[1]) * 2],PIL.Image.ANTIALIAS)    
	
	thresh = 120
	fn = lambda x : 255 if x > thresh else 0
	im = im.convert('L').point(fn, mode='1')

	im.save(os.getcwd() + '\\ui_levelBound.jpg', 'JPEG', quality=95)
	filename = 'ui_levelBound.jpg'    
	result = imgToNumberUniform(filename)
	if(result == 'i'):
		result = 1
	gameState['levelBound'] = result
	print('Level is : ' + result)

def grabWholeUI():	
	for element in gameState.keys():
		grabUI(element)
	grabLevel()	

def grabShop(slot):
	openShop()
	#time.sleep(0.03)
	box = (SHOP_BOUND[slot],195,SHOP_BOUND[slot]+184,195+60)
	im = PIL.ImageOps.grayscale(PIL.ImageGrab.grab(box))
	im = im.resize([213*4,68*4],PIL.Image.ANTIALIAS)


	thresh = 150
	fn = lambda x : 255 if x > thresh else 0
	im = im.convert('L').point(fn, mode='1')
	im.save(os.getcwd() + '\\shop_' + str(slot) + '.jpg', 'JPEG', quality=95)	

	filename = 'shop_' + str(slot) + '.jpg'
	print('in shop slot ' + str(slot) + ' there is ' + imgToTextUniform(filename))
	currentShopHeroes[slot] = imgToTextUniform(filename)


def grabWholeShop():
    for i in range(1,6):
        grabShop(i)        

def bench_select(slot):
	closeShop()
	mousePos(BENCH_POS[slot])
	#time.sleep(0.01)
	leftClick()
	

def leftClick():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    #print('left clicked')

def leftDown():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(0.01)
    #print('left Down')

def leftUp():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)    
    time.sleep(0.01)
    #print('left release')

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

def countBoard():
	count = 0
	for r in range(1,5):
		for c in range(1,9):
			if currentBoardHeroes[r][c][0] != 'EMPTY':
				count += 1
	print('board has ' + str(count) + ' heroes')
	return count

def countBench():
	count = 0;
	for i in range(1,9):
		if(currentBenchHeroes[i][0] != 'EMPTY'):
			count += 1
	print('bench has ' + str(count) + ' heroes')
	return count

def getFirstEmptyBoardTile():
	for r in range(1,5):
		for c in range(1,9):
			if currentBoardHeroes[r][c][0] == 'EMPTY':
				return (r,c)

def fillBoard():	
	grabWholeUI()
	grabWholeBoard()
	if countBoard() < int(gameState['levelBound']):
		closeShop()
		#time.sleep(0.01)
		for z in range(int(gameState['levelBound']) - countBoard()):
			bestBenchUnitIndex = 0
			grabWholeBench()
			for i in range(1,9):
				if(currentBenchHeroes[i][0] != 'EMPTY'):
					bestBenchUnitIndex = i
					break

			if bestBenchUnitIndex == 0:
				return False

			for i in range(1,9):
				if(currentBenchHeroes[i][0] != 'EMPTY'):
					if(currentBenchHeroes[i][1] > currentBenchHeroes[bestBenchUnitIndex][1]):
						bestBenchUnitIndex = i

			grabWholeBoard()
			tile = getFirstEmptyBoardTile()
			mousePos(BENCH_POS[bestBenchUnitIndex])
			print('moving mouse to bench slot ' + str(bestBenchUnitIndex))

			leftDown()		

			print('clicking down on bench slot ' + str(bestBenchUnitIndex))		

			mousePos(BOARD_POS[(tile[0])][(tile[1])])

			print('moving mouse to board tile ' + str(tile))

			leftUp()
			print('releasing mouse on board tile ' + str(tile))	


			print('MOVED HERO FROM BENCH SLOT ' + str(bestBenchUnitIndex) + ' TO BOARD TILE ' + str(tile))
			return True
	else:
		return False


def logicKnights():
	
	while True:
		print('SLEEPING NOW NOW NOW NOW')
		time.sleep(2) 		
		if(isLootUIOpen() is False):
			while fillBoard() is True:
				next
			grabWholeBench()
			if(countBench() < 8):			
				buyCompUnit(KNIGHT_COMP)
			closeShop()


def main():
    pass
 
if __name__ == '__main__':
    main()
