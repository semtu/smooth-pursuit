#pip install scipy pandas seaborn matplotlib
import scipy.io
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

FILE_PATH='SPtest.mat'

def load_file(FILE_PATH):
    '''Loading the data file to the Python environment'''
    mat = scipy.io.loadmat(FILE_PATH)
    return mat

mat=load_file(FILE_PATH)

def preprocess_data(mat):
    '''Process the datasets from the matlab arrays to pandas dataframe to carry out the analysis'''
    diction=dict()
    keys=['fft_list','pft_list','fst_list','pst_list','ftt_list','ptt_list','ffot_list','pfot_list']

    for key in keys:
        diction[key]=list()

    for i in range(0,1000):
        diction['fft_list'].append(mat['DATsp'][0][0][i])
        diction['pft_list'].append(mat['DATsp'][0][1][i])
        diction['fst_list'].append(mat['DATsp'][1][0][i])
        diction['pst_list'].append(mat['DATsp'][1][1][i])
        diction['ftt_list'].append(mat['DATsp'][2][0][i])
        diction['ptt_list'].append(mat['DATsp'][2][1][i])
        diction['ffot_list'].append(mat['DATsp'][3][0][i])
        diction['pfot_list'].append(mat['DATsp'][3][1][i])

    df=pd.DataFrame([])

    for index,key in enumerate(keys):
        df_name=key[:-5]
        df_name=pd.DataFrame(data=diction[key])
        if key[0]=='f':
            df_name['event']='fixation'
        else:
            df_name['event']='pursuit'
        trial=0
        if index==0 or index==1:
            trial+=1
            df_name['trial']=trial
        elif index==2 or index==3:
            trial+=2
            df_name['trial']=trial
        elif index==4 or index==5:
            trial+=3
            df_name['trial']=trial
        else:
            trial+=4
            df_name['trial']=trial

        df=df.append(df_name, ignore_index=True)
        df=df.drop(2,1) #dropping all null values in second column
    return df

def stimuli_dataframe(mat):
    df2=pd.DataFrame(mat['Pdeg'], columns=['Pdeg'])
    df2['tlist']=mat['tlist']
    df2['V']=mat['V']
    return df2

def generate_plots():
    '''Run the function to generate plots'''
    df=preprocess_data(mat)
    df2=stimuli_dataframe(mat)
    sns.scatterplot(x='tlist',y='Pdeg',data=df2)
    plt.savefig('position_time.png')
    plt.clf()
    sns.scatterplot(x='tlist',y='V',data=df2,color='red')
    plt.savefig('velocity_time.png')
    plt.clf()
    ax=df2.plot(x='tlist',y='Pdeg',legend=False)
    ax2=ax.twinx()
    df2.plot(x='tlist',y='V',ax=ax2, legend=False,color='red')
    ax.figure.legend()
    plt.savefig('twin_plot.png')
    plt.clf()
    ax=sns.lineplot(x=df[0],y=df[1],data=df[0:1000])
    ax.set(xlabel='X-axis',ylabel='Y-axis')
    plt.savefig('Fixation_first_trial.png')
    plt.clf()
    ax=sns.lineplot(x=df[0],y=df[1],data=df[1000:2000])
    ax.set(xlabel='X-axis',ylabel='Y-axis')
    plt.savefig('pursuit_first_trial.png')
    return


generate_plots()