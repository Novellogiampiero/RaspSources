#try:
import psycopg2
#except:
#import psycopg3
import time
'''
connection = psycopg2.connect(
        user = "postgres",
        password = "novello",
        host = "10.16.1.208",
        port = "5432",
        database = "novello"
    )
'''

class db():
    def __init__(self,hosts="10.16.1.166",database="lab1",user='lab1',password='postgres',ports='5432'):
        self.hosts=hosts
        self.database=database
        self.user=user
        self.password=password
        self.port=ports
        self.conn = psycopg2.connect(database=self.database, user=self.user, password=self.password, host=self.hosts, port= self.port)
        self.cursor = self.conn.cursor()
        print(self.conn.get_dsn_parameters(),"\n")
        self.cursor.execute("SELECT version();")
        record =self.cursor.fetchone()
        self.sql=""
        print("You are connected into the - " ,record)
        print("Database Init Done")
        
	
    def __del__(self):
        #Closing the connection
        self.conn.close()

    def SaveA2d(self,idn,data):
        try:
            binary = psycopg2.Binary(data)
            self.cursor.execute("INSERT INTO DataTable(id,canale,bits, data) VALUES (%d, %s)", i,(binary,) )
            self.conn.commit()
        except:
            if self.conn:
                conn.rollback()
                print('Error ')    
        finally:
            print(" finita connessione con scrittura")

    '''
    CREATE TABLE table_name(
    column1 datatype,
    column2 datatype,
    column3 dataty
    .....
    columnN datatype,
    );
    
    Example
    Following example creates a table with name CRICKETERS in PostgreSQL.

    postgres=# CREATE TABLE TestsGiuliano (
    NomeTest VARCHAR(16),
    DataeOra VARCHAR(16),
    NomeArticolo VARCHAR(16),
    NomeRaspberry VARCHAR(16),
    NumeroBitDiQ  INT,
    Banda INT,
    FrequenzaCamp INT,
    TestNumber INT;

    CREATE TABLE
    postgres=#
    '''
    def MakeRefTable(self,TableName):
        self.conn = psycopg2.connect(database=self.database, user=self.user, password=self.password, host=self.hosts, port= self.port)
        self.cursor = self.conn.cursor()
        cmd=("DROP TABLE IF EXISTS %s;"%TableName)
        print(cmd)
        #self.cursor.execute(cmd) NON USO IL COMANDO:::: NON CANCELLO
        self.sql =("CREATE TABLE %s(NomeTest CHAR(16),Data CHAR(16),NomeArticolo CHAR(16),NomeRaspberry CHAR(16),NumeroBit INT,Banda INT,FrequenzaCamp INT,TestNr INT);" %TableName)
        print(self.sql)
        self.cursor.execute(self.sql)
    '''
        Data=[NomeTest,Data,NomeArticolo,NomeRasp,NumeroBit,Banda,Frequeza,TestNR]
    '''
    def InsertDataInRefTable(self,TableName,Res):
        self.sql = ("INSERT INTO %s (NomeTest,Data, NomeArticolo,NomeRaspberry,NumeroBit,Banda,FrequenzaCamp, TestNr) VALUES (%s, %s, %s, %s, %s,%s, %s, %s);"%(TableName,Res[0],Res[1],Res[2],Res[3],Res[4],Res[5],Res[6],Res[7]))
        print(self.sql)
        self.cursor.execute(self.sql)
    
       # Doping EMPLOYEE table if already exists.
       #     cursor.execute("DROP TABLE IF EXISTS EMPLOYEE")
       #     sql = '''CREATE TABLE EMPLOYEE(
       #     FIRST_NAME CHAR(20) NOT NULL,
       #     LAST_NAME CHAR(20),
       #     AGE INT,
       #     SEX CHAR(1),
       #     INCOME FLOAT)'''
       #  cursor.execute(sql)
       # '''
    '''

    ATTENZIONE QUESTA TABELLA IS quella che mi fa la gestione...dei dati che arrivano dal Analog device
    numero ciclo
    numero di ingresso char(16)
    stato misura char(16)
    Dati Array di float
    '''
    def MakeDataTable(self,TableName):
        #self.conn = psycopg2.connect(database=self.database, user=self.user, password=self.password, host=self.hosts, port= self.port)
        #self.cursor = self.conn.cursor()
        #print(self.conn.get_dsn_parameters(),"\n")
        self.cursor.execute("DROP TABLE IF EXISTS %s;"%TableName)
        self.sql =("CREATE TABLE %s( NUMEROCICLO INT,INGRESSO CHAR(16),STATOMISURA CHAR(16) ,analog float ARRAY[16000]);" %TableName)
        print(self.sql)
        self.cursor.execute(self.sql)
       
    def InsertDataInDataTable(self,TableName, ciclo,ingresso ,statomisura,analog):
        self.sql = ("INSERT INTO %s (NUMEROCICLO ,INGRESSO, STATIMISURA,analog) VALUES (%s, %s, %s, %s, %s,%s, %s, %s);"%(TableName,ciclo,ingresso,statomisura,analog))
        print(self.sql)
        self.cursor.execute(self.sql)

    def GetAllFromtable(self,TableName):
        #Creating a cursor object using the cursor() method
        self.sql=("SELECT * from %s ;"%TableName)
        #Retrieving data
        print(self.sql)
        self.cursor.execute(self.sql)
        #Fetching 1st row from the table
        result = self.cursor.fetchall();
        print(result)
        return result

    def GetoneFromtable(self,TableName):
        #Setting auto commit false
        #Creating a cursor object using the cursor() method
        self.sql="SELECT * from %s;"%TableName
        #Retrieving data
        self.cursor.execute(self.sql)
        #Fetching 1st row from the table
        result = self.cursor.fetchone();
        print(result)
        return result
    

    




    def DeleteData(self,Data,Soglia):
        pass
        #cursor.execute('''DELETE FROM EMPLOYEE WHERE AGE > 25''')
    
    def InsertData(self,Data):
        pass
        #INSERT INTO exampleTable(exampleArray[3]) VALUES('{1, 2, 3}');
        #INSERT INTO contacts (name, phones)
        #VALUES('John Doe',ARRAY [ '(408)-589-5846','(408)-589-5555' ]);





   
def main():
    print("Start")
    D=db()
    return 
    D.MakeRefTable(TableName="AutecTestType")
    D.InsertDataInRefTable(TableName="AutecTestType",Res=[1,2,3,4,5,6,7,8])
    D.InsertDataInRefTable(TableName="AutecTestType",Res=[10,11,11,11,11,11,11,11])
    D.GetAllFromtable(TableName="AutecTestType")
    D.GetoneFromtable(TableName="AutecTestType")
    D.MakeDataTable(TableName="AAAA")
    global ts
    k=0
    #print(Py.Up())
    #print(Py.Down())
    while(k<10000000):
        print(" k is",k)
        time.sleep(1)
        if((k%10)==0):
            ts=k
        k=k+1
        #print("Ciclo is",k)
    print("Fine")
     #######
if __name__ == '__main__':
    main()
