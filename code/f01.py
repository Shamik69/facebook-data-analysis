# TODO: check interdependencies between friends, likes (received), mobile and www likes (received)
# TODO: use reg for (to be) found interdependencies


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


def demography(df: pd.DataFrame, plot: bool = True):  # demographic distribution of data
    demo = []

    # separating the demographics
    m = df[df['gender'] == 'male']
    f = df[df['gender'] == 'female']
    for i in range(13, 114):
        demo.append((i, m[m['age'] == i].shape[0], f[f['age'] == i].shape[0]))
    demo = pd.DataFrame(demo, columns=['age', 'male', 'female'])

    # scatter and line chart plotting
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
    time.sleep(1)

    # plotting
    plt.close()

    # saving processed data
    demo.to_csv(f'{path}/processed data/demography.csv', index=False)


# interdependencies between age and other factors
def factors(df: pd.DataFrame, x_factor: str, y_factor: str, plot: bool = True, measure: bool = True):
    global info
    fc = []

    # separating the demographics
    m = df[df['gender'] == 'male']
    f = df[df['gender'] == 'female']

    # generalizing for multiple factors
    for i in range(13, 114):

        # different methods for better data stitching
        if measure:
            fc.append((i, round(m[m[x_factor] == i][y_factor].mean(), 2),
                       round(f[f[x_factor] == i][y_factor].mean(), 2)))
        if not measure:
            fc.append((i, round(m[m[x_factor] == i][y_factor].var(), 2),
                       round(f[f[x_factor] == i][y_factor].var(), 2)))
    fc = pd.DataFrame(fc, columns=['age', 'male', 'female'])

    # label prep
    if measure:
        info = f'{x_factor} and {y_factor} (mean'
    elif not measure:
        info = f'{x_factor} and {y_factor} (sd'

    # plot prep
    if plot:
        line_chart(
                x_data=fc[x_factor], y1_data=fc['male'], y2_data=fc['female'],
                y1_label='male', y2_label='female',
                x_label=x_factor, y_label=y_factor,
                title=f'{info})', save_path=f'{path}/figs/{info} plot).jpeg'
        )
    elif not plot:
        scatter_chart(
                x_data=fc[x_factor], y1_data=fc['male'], y2_data=fc['female'],
                y1_label='male', y2_label='female',
                x_label=x_factor, y_label=y_factor,
                title=f'{info})', save_path=f'{path}/figs/{info} scatter).jpeg'
        )

    # plotting
    time.sleep(1)
    plt.close()
    fc.to_csv(f'{path}/processed data/{info}).csv', index=False)


def call():
    for i in True, False:
        # looping for both line and scatter graph
        demography(df, i)
        for col in list(df.columns[7:]):
            # loops for age and factor separation:
            for x in True, False:
                factors(df=df, x_factor='age', y_factor=col, plot=i, measure=x)


call()