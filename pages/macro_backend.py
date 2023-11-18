import pandas as pd

def reminder(macro, column, number, operation):
    # df = pd.read_csv(f'macro data/{macro}.csv')
    # df = pd.read_csv('macro data/Inflation Rate.csv')
    data = df[column]
    print(data[0])
    # if operation == '1':
    # if operation == '2':
    # if operation == '3':
    # if operation == '4':
    # if operation == '5':
    # if operation == '6':
    
df = pd.read_csv('macro data/Inflation Rate.csv')

ticker_list = [
    'EMSBF US Equity',
    'JPMIF US Equity',
    'JPUHF US Equity',
    'JPEIF US Equity',
    'JPGLF US Equity',
    'JPBBF US Equity',
    'JIREF US Equity',
    'BBAG US Equity',
    'BBMC US Equity',
    'JEPI US Equity',
    'BBSC US Equity',
    'JSCP US Equity',
    'JAVA US Equity',
    'JPIE US Equity',
    'JMEE US Equity',
    'JPRE US Equity',
    'JIRE US Equity',
    'JGRO US Equity',
    'JMSI US Equity',
    'JMHI US Equity',
    'JBND US Equity',
    'JPIN US Equity',
    'JPEM US Equity',
    'JPUS US Equity',
    'JPME US Equity',
    'JPSE US Equity',
    'JPST US Equity',
    'JMOM US Equity',
    'JQUA US Equity',
    'JVAL US Equity',
    'JPMB US Equity',
    'JEPQ US Equity',
    'JPEF US Equity',
    'JGLO US Equity',
    'JCPB US Equity',
    'BBUS US Equity',
    'JEMA US Equity',
    'BBIN US Equity',
    'BBRE US Equity',
    'BBEU US Equity',
    'BBJP US Equity',
    'JCPI US Equity',
    'BBAX US Equity',
    'BBCA US Equity',
    'BBHY US Equity',
    'BBEM US Equity',
    'JMUB US Equity',
    'JMST US Equity',
    'JPLD US Equity',
    'JPIB US Equity',
    'BBUS* MM Equity',
    'JPMB* MM Equity',
    'BBRE* MM Equity',
    'BBTRN MM Equity',
    'BBILN MM Equity',
    'JPIN* MM Equity',
    'JPME* MM Equity',
    'JPEM* MM Equity',
    'JPGLN MM Equity',
    'BBIN* MM Equity',
    'JMABN MM Equity',
    'JPSE* MM Equity',
    'MBILN MM Equity',
    'JPUS* MM Equity',
    'JGHYN MM Equity',
    'JHYMN MM Equity',
    'JMBMN MM Equity',
    'JPCTN MM Equity',
    'BBSC* MM Equity',
    'BBMC* MM Equity',
    'MB3MN MM Equity',
    'BB3MN MM Equity',
    'BBAX* MM Equity',
    'BBJP* MM Equity',
    'BBCA* MM Equity',
    'BBEU* MM Equity',
    'JQUA* MM Equity',
    'JMOM* MM Equity',
    'JVAL* MM Equity',
    'BBHY* MM Equity',
    'BBAG* MM Equity',
    'BBEM* MM Equity',
    'JCHAN MM Equity'
]

macro_list = [
    'Commodities',
    'CPI',
    'currencies',
    'GDP Growth Rate',
    'Inflation Rate',
    'Interest Rate',
    'Major Bond Yeilds'
]

