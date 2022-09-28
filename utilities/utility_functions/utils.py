"""
Elyse's Functions
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



def read_data(filename):
    #read first line of file
    header = pd.read_csv(filename, sep ='\t', nrows=1, encoding='latin1')
    
    #extract number of lines to skip
    word = str(header).split() #turn first line into string then break up into a string array
    num = int(word[8])       #find the last number in the string and convert to integer
    #read the data chunk of the file by skipping the header-1 lines
    df = pd.read_csv(filename, sep ='\t', skiprows=num-1, encoding='latin1')    
    return df

def read_ftir(filename):
    
    #read the data chunk of the file by skipping 2 lines
    df = pd.read_csv(filename, names =['wavelength','transmittance'])    
    return df

def read_press(file):
    
    #read pressure data file
    df_p = pd.read_csv(file, sep ='\t', names =['time/min','voltage/V', 'current/mA','pressure/torr','temperature/C'])
    df_p['time/min']=df_p['time/min']*60
    df_p.columns=['time/s','voltage/V', 'current/mA', 'pressure/torr','temperature/C']
    
    #normalize time function
    df_p['time/s'] = df_p['time/s']-df_p['time/s'].iloc[0]
    return df_p



def plot_press(pfile):
    import matplotlib.pyplot as plt
    plt.figure()
    plt.plot(pfile['time/s'], pfile['pressure/torr'])
    plt.xlabel('Time(s)')
    plt.ylabel('Pressure (torr)')
    plt.show()      
    return    
    
    
    
def getnearpos(array,value):
    idx = np.argmin((np.abs(array-value)).values)
    #print ('The ' + str(idx) +'th value of this array is: ' + str(array[idx]))
    
    return idx

def folder_files(folder_dir):
    import os
    #print(os.getcwd())
    files = os.listdir(folder_dir)

    import re 
    regex = 'mpt'
    
    mpts = [folder_dir + f for f in files if re.search(regex, f)]
    mpts.sort()
    
    #read in the mpts as dataframes and put in list ls
    ls=[]
    for i in range(len(mpts)):
        ls.append(read_data(mpts[i]))
        

    #normalize all the dataframes by time zero in first dataframe
#     for i in range(len(ls)):
#         ls[i]['time/s']= ls[i]['time/s']-ls[0]['time/s'].iloc[0]
    
    return(ls)


def headspace(num_ch): #, filedate):
    def channel_vol(ch): #, filedate):
        if ch==1:
#             chan1 = [1656.5,1691.5]
#             if filename < 190211:
#                 channel_vol=chan1[0]
#             else:
#                 channel_vol=chan1[1]
            channel_vol=1691.5
        elif ch==2:
            channel_vol=1676.5
        elif ch==3:
             channel_vol = 1669.4
        elif ch==4:
            channel_vol=1640.6
            channel_vol=1671 # as of 6/2022


        elif ch==5:
            channel_vol=1671.8
        elif ch=='dems1':
            channel_vol= 1284 # +499
        elif ch== 'dems2':
            channel_vol=1292 # +499
        
        
        
        return (channel_vol)
    
    
    
    
    cell_vol = 422.5
    elyte = 80 
    headspace = channel_vol(num_ch) + cell_vol - elyte   #in uL
    
    return headspace

def read_dems(file):
    df = pd.read_csv(file, sep ='\t')
    df = df.rename(columns=lambda x: x.replace('.00000', ''))
    df.rename(columns={'0':'time/min', '0.1':'temperature/C', '0.2': 'pressure/torr', '0.3':'current/mA', '0.4':'voltage/V'}, inplace= True)
    #normalize time function
    df['time/min'] = df['time/min']-df['time/min'].iloc[0]
    
    return df
