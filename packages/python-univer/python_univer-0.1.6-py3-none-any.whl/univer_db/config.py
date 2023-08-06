class DRIVER:
    FREETDS = 'FreeTDS'
    ODBC_17 = 'ODBC+Driver+17+for+SQL+Server'

class Config:
    def __init__(self, host, user, password, driver=DRIVER.FREETDS):
        self.host = host
        self.user = user
        self.password = password
        self.driver = driver