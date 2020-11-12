import pandas as pd
import matplotlib.pyplot as plt
import time
import seaborn as sns

sns.set()
path = 'C:/Users/User/PycharmProjects/facebook'

t0 = time.time()
df = pd.read_csv(f'{path}/data/pseudo_facebook.csv')


def line_chart(y1_data, y2_data, x_data,
               y1_label, y2_label, x_label,
               y_label, title, save_path):
    plt.plot(x_data, y1_data, label=y1_label)
    plt.plot(x_data, y2_data, label=y2_label)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.legend()
    plt.savefig(save_path)


def scatter_chart(y1_data, y2_data, x_data,
                  y1_label, y2_label, x_label,
                  y_label, title, save_path):
    plt.scatter(x_data, y1_data, label=y1_label)
    plt.scatter(x_data, y2_data, label=y2_label)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.legend()
    plt.savefig(save_path)


def demography(df: pd.DataFrame, plot: bool = True):
    demo = []
    m = df[df['gender'] == 'male']
    f = df[df['gender'] == 'female']
    for i in range(13, 114):
        demo.append((i, m[m['age'] == i].shape[0], f[f['age'] == i].shape[0]))
    demo = pd.DataFrame(demo, columns=['age', 'male', 'female'])
    if plot:
        line_chart(
                x_data=demo['age'], y1_data=demo['male'], y2_data=demo['female'],
                y1_label='male', y2_label='female',
                x_label='age', y_label='population',
                title='Demographic', save_path=f'{path}/figs/demographic(plot).jpeg'
        )
    elif not plot:
        scatter_chart(
                x_data=demo['age'], y1_data=demo['male'], y2_data=demo['female'],
                y1_label='male', y2_label='female',
                x_label='age', y_label='population',
                title='Demographic', save_path=f'{path}/figs/demographic(scatter).jpeg'
        )
    plt.show()


def factors(df: pd.DataFrame, y_factor:str, plot: bool = True, measure: bool = True):
    fc = []
    x=[]
    m = df[df['gender'] == 'male']
    f = df[df['gender'] == 'female']
    for i in range(13, 114):
        if measure:
            fc.append((i, m[m['age'] == i][y_factor].std(), f[f['age'] == i][y_factor].std()))
        if not measure:
            fc.append((i, m[m['age'] == i][y_factor].std(), f[f['age'] == i][y_factor].std()))
    fc = pd.DataFrame(fc, columns=['age', 'male', 'female'])
    if measure:
        info= f'{y_factor} (mean'
    elif not measure:
        info= f'{y_factor} (sd'

    if plot:
        line_chart(
                x_data=fc['age'], y1_data=fc['male'], y2_data=fc['female'],
                y1_label='male', y2_label='female',
                x_label='age', y_label=y_factor,
                title=f'{info})', save_path=f'{path}/figs/{info} plot).jpeg'
        )
    elif not plot:
        scatter_chart(
                x_data=fc['age'], y1_data=fc['male'], y2_data=fc['female'],
                y1_label='male', y2_label='female',
                x_label='age', y_label=y_factor,
                title=f'{info})', save_path=f'{path}/figs/{info} scatter).jpeg'
        )
    time.sleep(1)
    plt.close()


for i in True, False:
    for col in list(df.columns[7:]):
        for x in True, False:
            factors(df, col, i, x)

