import time
def measure(x):
    print(x+" has been measured")
    time.sleep(1)
def mixIngredients():
    print("Batter is mixed")
    time.sleep(1)
def pourBatter():
    print("Batter is poured")
    time.sleep(1)
def setOvenTempTo(x):
    print("Setting oven temp")
    time.sleep(0.2)
    print("Heating up..")
    print("Ready in:")
    for y in range(0,3):
        print(str(3-y)+"hours")
        time.sleep(1)
    print("Oven temperature is set to " + str(x) + " degrees")
    time.sleep(1)
def bakeBatter():
    print("Baking first layer....")
    time.sleep(1)
    print("Baking second layer....")
    time.sleep(1)
    print("Baking third layer....")
    time.sleep(1)
    print("All layers are baked!")
    time.sleep(1)
def assembleCake():
    time.sleep(1)
    print("Cake is assembled and ready to be iced!")
    time.sleep(1)
def iceCake():
    print("Cake is iced")
    time.sleep(1)
def bakeACake(*args):
    for i in args:
        measure(i)
    mixIngredients()
    pourBatter()
    setOvenTempTo(500)
    bakeBatter()
    assembleCake()
    iceCake()
    print("Congradulations! You made a cake!")
bakeACake("flour", "water", "eggs", "sugar")
