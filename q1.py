import random

CATEGORIES = ('Hygiene', 'Health', 'Staples', 'Sports', 'Fashion')


class Utils:
    def getInt(*args):
        while True:
            try:
                val = int(input(*args))
            except:
                print('Invalid Input')
            else:
                return val
                
    def getFloat(*args):
        while True:
            try:
                val = float(input(*args))
            except:
                print('Invalid Input')
            else:
                return val


class Category:
    __categories = {}
    def __init__(self, name, capacity) -> None:
        self.capacity = capacity
        self.name = name
        self.current = 0
    
    @staticmethod
    def init_cat(cats, cap):
        for cat in cats:
            Category.__categories[cat.lower()] = Category(cat, cap)
    
    @staticmethod
    def getCat(cat):
        if cat.lower() in Category.__categories.keys():
            if Category.__categories[cat.lower()].current < Category.__categories[cat.lower()].capacity:
                Category.__categories[cat.lower()].current += 1
                return Category.__categories[cat.lower()].name
            else:
                raise Exception('Category limit exceeded')
        else:
            raise Exception('Category not found')


Category.init_cat(CATEGORIES, Utils.getInt('Enter category limit: '))


class Product:
    products = {}

    def __init__(self, name, code, category, tax) -> None:
        self.__name = name
        self.__category = Category.getCat(category)
        self.__code = code
        self.__basicPrice = 0
        self.__tax = tax
        self.__mrp = 0
    
    @property
    def name(self):
        return self.__name
    
    @property
    def category(self):
        return self.__category
    
    @property
    def code(self):
        return self.__code

    @property
    def basicPrice(self):
        return self.__basicPrice
    
    @property
    def discount(self):
        return self.__discount
    
    @property
    def tax(self):
        return self.__tax
    
    @property
    def mrp(self):
        return self.__mrp
    
    @basicPrice.setter
    def basicPrice(self, val):
        self.__basicPrice = val
        self.__mrp = self.__basicPrice + self.__basicPrice * self.__tax / 100
    
    @mrp.setter
    def mrp(self, val):
        self.__mrp = val
        self.__basicPrice = self.__mrp * 100 / (self.__tax + 100)
    
    def setDiscountRate(self, rate):
        self.__discount = rate
        self.__dicsRate = True
    
    def setDiscountAmount(self, amt):
        self.__discount = amt
        self.__dicsRate = False
    
    @property
    def discountAmount(self):
        if self.__dicsRate:
            return self.__mrp * self.__discount / 100
        else:
            return self.__discount
    
    @property
    def sellingPrice(self):
        return self.__mrp - self.discountAmount
    
    def display(self):
        print('\nCode:', self.code)
        print('Name:', self.name)
        print('Category:', self.category)
        print('Basic Price:', self.basicPrice)
        print('Tax:', self.tax)
        print('MRP:', self.mrp)
        print('Discount:', self.discount)
        print('Discount Amount:', self.discountAmount)
        print('Selling Price:', self.sellingPrice)
    
    @staticmethod
    def addProduct():
        name = input('Enter Product name: ')
        while True:
            for i, cat in enumerate(CATEGORIES):
                print(f'{i+1}. {cat}')
            opt = Utils.getInt('> ')
            if 1 <= opt <= len(CATEGORIES):
                break
            print('Invalid option')
        category  = CATEGORIES[opt]

        tax = Utils.getFloat('Enter tax rate: ')
        codes = [i[:4] for i in Product.products.keys()]
        tmpCode = category[:2].upper() + name[:2].upper()
        code = tmpCode + str(codes.count(tmpCode)) + str(random.randrange(1000)).zfill(3)

        try:
            p = Product(name, code, category, tax)
        except Exception as e:
            print('Failed to add Product', e)
        else:
            while True:
                opt = input('Input (M)RP or (B)asic Price: ').upper()
                if opt in ('M', 'B'):
                    match opt:
                        case 'M': p.mrp = Utils.getFloat('Enter MRP: ')
                        case 'B': p.basicPrice = Utils.getFloat('Enter Basic Price: ')
                    break
                print('Invalid input')
            
            while True:
                opt = input('Input Discount (R)ate or Discount (A)mount: ').upper()
                if opt in ('R', 'A'):
                    match opt:
                        case 'R': p.setDiscountRate(Utils.getFloat('Enter Discount Rate: '))
                        case 'A': p.setDiscountAmount(Utils.getFloat('Enter Discount Amount: '))
                    break
                print('Invalid input')
            
            Product.products[code] = p
            p.display()
    
    @staticmethod
    def listProducts():
        for _, product in Product.products.items():
            product.display()


while True:
    opt = Utils.getInt('''
    1. Add
    2. List
    0. Exit
    > ''')
    match opt:
        case 1: Product.addProduct()
        case 2: Product.listProducts()
        case 0: break
        case _: print('Invalid input')