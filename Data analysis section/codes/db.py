import firebase_admin
from firebase_admin import credentials,firestore

cred = credentials.Certificate("C:\\Users\\gaurav.khatri\\Demo Projects\\VScode\\abc.py\\Data analysis section\\codes\\pvtkey.json")
firebase_admin.initialize_app(cred)

db =firestore.client()


class scrip():
    def __init__(self, Company, Transactions, TotalSharesTraded, TotalAmount,MaxPrice,MinPrice,ClosePrice):
        self.Company = Company
        self.Transactions = Transactions
        self.TotalSharesTraded = TotalSharesTraded
        self.TotalAmount = TotalAmount
        self.MaxPrice = MaxPrice
        self.MinPrice = MinPrice
        self.ClosePrice = ClosePrice

    
        
    def __repr__(self):
        return(
            u'scrip(Company={}, Transactions={}, TotalSharesTraded={}, TotalAmount={},MaxPrice={},MinPrice={},ClosePrice={})'.format(self.Company,  self.Transactions, self.TotalSharesTraded, self.TotalAmount,self.MaxPrice,self.MinPrice,self.ClosePrice))
    
    # @staticmethod
    # def to_dict(self):
    #     # ...    


db_ref = db.collection('adbl')
day_data = scrip('ADBL',233,51446.00,20980918.00,416.00,400.00,405.00)
db_ref.collection(u'adbl').document(u'2020-03-05').set(day_data)