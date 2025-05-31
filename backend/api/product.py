class Product:
    def __init__(self, name, qty,price,description):
        self.name = name
        self.qty = qty
        self.price = price
        self.description = description
    def getProductName(self):
        return self.name

p=Product("ladyfinger",20,100,"Good")
p.getProductName()


#api (application programming interface )