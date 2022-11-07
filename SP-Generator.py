import mysql.connector

mydb = mysql.connector.connect(
  host="arpudhacheck.online",
  user="apqurufmu_arpudha",
  password="arpudha@123",
  database="apqurufmu_world"
)

databaseName = "apqurufmu_world"

mycursor = mydb.cursor()




def dataSpliter(data):
     data = str(data)
     data=  data.replace('(' , '')
     data=data.replace(")" , "")
     data=data.replace("," , "")
     data=data.replace("'" , "")
     return data



def getTableData():
        getTableListQuery =   '''SELECT table_name FROM information_schema.tables WHERE table_schema ="''' + databaseName +'''"'''
        mycursor.execute(getTableListQuery)
        UnSortedTableList = mycursor.fetchall()
        TempTableList = []
        for x in UnSortedTableList:
           #splittedTablleList = dataSpliter(x)
           splittedTablleList = x[0]
           TempTableList.append(splittedTablleList)
        return TempTableList

        
        #print(splittedTablleList)

def getColumnName(tableName):
    getColumnListQuery = f'''
                            SELECT `COLUMN_NAME` 
                        FROM `INFORMATION_SCHEMA`.`COLUMNS` 
                        WHERE `TABLE_SCHEMA`='{databaseName}' 
                            AND `TABLE_NAME`='{tableName}';
                            '''
    mycursor.execute(getColumnListQuery)
    UnSortedColumnList = mycursor.fetchall()
    
    TempColumnList = []
    for x in UnSortedColumnList:
           #splittedColumnList = dataSpliter(x)
           splittedColumnList = x[0]
           TempColumnList.append(splittedColumnList)

    return TempColumnList

def generateInsertSP(tableName):
    
    SP = "("
    getTableNameandTyeQuery = f'''select COLUMN_NAME , COLUMN_TYPE from information_schema.columns 
         where table_schema = '{databaseName}'
          and Table_name = '{tableName}'  '''

    mycursor.execute(getTableNameandTyeQuery)
    UnSortedTableList = mycursor.fetchall()
    for x in UnSortedTableList:
        columnName = x[0]
        columnDataType = x[1]
        #print(columnDataType)
        SP = SP + 'p'+ columnName + ' '+ columnDataType + ','
    SP = SP[:len(SP) - 1]
    SP = SP + ')'
    SP = SP + f'''\n BEGIN \n INSERT INTO  {tableName} ('''

    for x in UnSortedTableList:
        columnName = x[0]
        columnDataType = x[1]
        SP = SP + columnName + ','
    SP = SP[:len(SP) - 1]
    SP = SP + ')'
    SP = SP + 'VALUES ('
    for x in UnSortedTableList:
        columnName = x[0]
        columnDataType = x[1]
        SP = SP + 'p'+columnName + ','
    SP = SP[:len(SP) - 1]
    SP = SP+')'
    SP = SP+ ' \nEND'
    print(SP)  
    f = open(f"INSERT_SP_{tableName}.txt", "a")
    f.write(SP)
    f.close()

    return 1

def generateUpdateSP(tableName):
    SP = "("
    getTableNameandTyeQuery = f'''select COLUMN_NAME , COLUMN_TYPE from information_schema.columns 
         where table_schema = '{databaseName}'
          and Table_name = '{tableName}'  '''

    mycursor.execute(getTableNameandTyeQuery)
    UnSortedTableList = mycursor.fetchall()
    for x in UnSortedTableList:
        columnName = x[0]
        columnDataType = x[1]
        #print(columnDataType)
        SP = SP + 'p'+ columnName + ' '+ columnDataType + ','
    SP = SP[:len(SP) - 1]
    SP = SP+') BEGIN UPDATE ' +tableName + ' SET '
    for x in UnSortedTableList:
        columnName = x[0]
        columnDataType = x[1]
        #print(columnDataType)
        #SP = SP + 'p'+ columnName + ' '+ columnDataType + ','
        SP = ' '+SP + columnName + ' = ' + 'p'+ columnName + ' ,'
    SP = SP[:len(SP) - 1]
    print(SP)
    f = open(f"UPDATE_SP_{tableName}.txt", "a")
    f.write(SP)
    f.close()
    

    return 1

switchNumber = int(input(''' Enter 1 for list Table from Database\n
Enter 2 for column list for a Table\n
Enter 3 to generate Insert SP for Table\n
ENter 4 to generate Update SP for Table'''))
if(switchNumber ==1):
    tableList = getTableData();
    for x in tableList:
        print(x)
        f = open("TableList.txt", "a")
        f.write(x+"\n")
        f.close()
        
elif(switchNumber == 2):
    tableName = input("Enter Table Name: ")
    columnList = getColumnName(tableName);
    for x in columnList:
        print(x)
        f = open(f"ColumnList_{tableName}.txt", "a")
        f.write(x+"\n")
        f.close()

elif(switchNumber == 3):
    tableName = input("Enter Table Name: ")
    
    generateInsertSP(tableName);

elif(switchNumber == 4):
    tableName = input("Enter Table Name: ")
    generateUpdateSP(tableName)
    



  



