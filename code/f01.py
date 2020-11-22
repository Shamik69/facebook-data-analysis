# TODO: check interdependencies between friends(initiated), likes (received), mobile and www likes (received)


import pandas as pd
import matplotlib.pyplot as plt
import time
import seaborn as sns
import statsmodels.api as sm

sns.set()
path = 'C:/Users/User/PycharmProjects/facebook'

t0 = time.time()
df = pd.read_csv(f'{path}/data/pseudo_facebook.csv')


# line and scatter plotting
def sub_fn01(y1_data, x_data,
             y1_label, x_label, y_label, title, save_path, info_text: str,
             y2_data=None, y2_label=None, plot: bool = True):
    if plot:
        plt.plot(x_data, y1_data, label=y1_label)
        if y2_data is not None:
            plt.plot(x_data, y2_data, label=y2_label)
        else:
            pass
        output = 'line'
    elif not plot:
        plt.scatter(x_data, y1_data, label=y1_label)
        if y2_data is not None:
            plt.scatter(x_data, y2_data, label=y2_label)
        else:
            pass
        output = 'scatter'
    plt.xlabel(x_label)
    if y2_data is None:
        plt.ylabel(y1_label)
    else:
        plt.ylabel(y_label)
    plt.title(title)
    plt.legend()
    plt.savefig(f'{save_path}/{info_text} {output}.jpeg')
    print(f'filename: {save_path}/{info_text} {output}.jpeg\n')


def main_fn01(df: pd.DataFrame, plot: bool = True):  # demographic distribution of data
    demo = []

    # separating the demographics
    m = df[df['gender'] == 'male']
    f = df[df['gender'] == 'female']
    for i in range(13, 114):
        demo.append((i, m[m['age'] == i].shape[0], f[f['age'] == i].shape[0]))
    demo = pd.DataFrame(demo, columns=['age', 'male', 'female'])

    # scatter and line chart plotting
    sub_fn01(
            x_data=demo['age'], y1_data=demo['male'], y2_data=demo['female'],
            y1_label='male', y2_label='female',
            x_label='age', y_label='population',
            title='Demographic', save_path=f'{path}/figs',
            plot=plot, info_text='demography'
    )
    time.sleep(0.5)

    # plotting
    plt.close()

    # saving processed data
    demo.to_csv(f'{path}/processed data/demography.csv', index=False)
    print(f'filename: {path}/processed data/demography.csv\n')


# interdependencies between age and other factors
def main_fn02(df: pd.DataFrame, y_factor: str, plot: bool = True, measure: bool = True):
    fc = []

    # separating the demographics
    m = df[df['gender'] == 'male']
    f = df[df['gender'] == 'female']

    # generalizing for multiple factors
    for i in range(13, 114):

        # different methods for better data stitching
        if measure:
            fc.append((i, round(m[m['age'] == i][y_factor].mean(), 2), round(f[f['age'] == i][y_factor].mean(), 2)))
        if not measure:
            fc.append((i, round(m[m['age'] == i][y_factor].var(), 2), round(f[f['age'] == i][y_factor].var(), 2)))
    fc = pd.DataFrame(fc, columns=['age', 'male', 'female'])

    # label prep
    if measure:
        info = f'{y_factor} mean'
    elif not measure:
        info = f'{y_factor} sd'

    # plot prep
    sub_fn01(
            x_data=fc['age'], y1_data=fc['male'], y2_data=fc['female'],
            y1_label='male', y2_label='female',
            x_label='age', y_label='population',
            title='Demographic', save_path=f'{path}/figs',
            info_text=f'age and {info}', plot=plot

    )

    # plotting
    time.sleep(1)
    plt.close()
    fc.to_csv(f'{path}/processed data/{info}.csv', index=False)
    print(f'filename: {path}/processed data/{info}.csv\n')


def main_fn03(df: pd.DataFrame, x_factor: str, y_factor: str, plot: bool = True):
    info= f'{x_factor} and {y_factor}'
    sub_fn01(
            x_data=df[x_factor], y1_data=df[y_factor],
            x_label=x_factor, y1_label=y_factor,
            title=f'{x_factor} and {y_factor}',
            plot=plot, y_label=y_factor, save_path=f'{path}/figs',
            info_text=info
    )
    time.sleep(1)
    plt.close()
    shitstain= df[[x_factor, y_factor]]
    shitstain.to_csv(f'{path}/processed data/{info}.csv', index=False)
    print(f'filename: {path}/processed data/{info}.csv\n')


def call(call_run: int):
    for i in True, False:
        # looping for both line and scatter graph
        if call_run == 0:
            main_fn01(df, i)
        elif call_run == 1:
            for col in list(df.columns[7:]):
                # loops for age and factor separation:
                for x in True, False:
                    main_fn02(df, col, i, x)
        elif call_run == 2:
            for fuck in ['friend_count', 'friendships_initiated'], ['likes', 'likes_received'], \
                        ['mobile_likes', 'www_likes']:
                main_fn03(df=df, x_factor=fuck[0], y_factor=fuck[1], plot=i)


def reg():
    demo = pd.read_csv(f'{path}/processed data/demography.csv')
    y= demo['age']
    x= sm.add_constant(demo[['male', 'female']])
    model= sm.OLS(y, x).fit()
    summary= model.summary()
    html= summary.tables[1].as_html()
    df= pd.read_html(html, header=0, index_col=0)[0]
    x= list(df['coef'])
    sign= ['+', '', '+']
    for i in x:
        if i<0:
            sign[x.index(i)]= ''
    return f'\ny= {sign[1]}{x[1]}x0{sign[2]}{x[2]}x1{sign[0]}{x[0]}'


print(reg())