


import sys,os,csv

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
# importing matplotlib library
import matplotlib.pyplot as plt
import numpy as np

dataPath = os.path.dirname(os.path.realpath(__file__))+'/../metric_generation/branch_metrics.csv'

class Branch(object):
    def __init__(self):
        self.name = None
        self.data = []
        self.x = []
        self.y = []

branches = []

# data = {}

with open(dataPath,'r') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    next(csvreader)
    for row in csvreader:
        branch = Branch()
        count = 0
        for c in row:
            if not branch.name:
                branch.name = c
                # data['branch'] = c
                continue
            branch.data.append((int(count),int(c)))
            branch.x.append(int(count))
            # data['seconds'] = count
            branch.y.append(int(c))
            # data['latency'] = c
            count += 60
        branches.append(branch)

data = {}

data['Time'] = branches[0].x

for branch in branches:
    data[branch.name] = branch.y

sourcedf = pd.DataFrame(data=data)

print(sourcedf)


tdataPath = os.path.dirname(os.path.realpath(__file__))+'/../branch_thresholds_multiply.csv'
tdf = pd.read_csv(tdataPath)
print(tdf)


pdataPath = os.path.dirname(os.path.realpath(__file__))+'/../branch_thresholds.csv'
pdf = pd.read_csv(pdataPath)
print(pdf)

fulldf = pd.merge(pd.merge(pdf,tdf,on='Time'),sourcedf,on='Time')

print(fulldf)

fig = go.Figure()

for i in fulldf.keys():
    if i == 'Time':
        continue
    fig.add_trace(go.Scatter(x = fulldf['Time'],
                                y = fulldf[i], 
                                name = i))


fig.update_xaxes(rangeslider_visible=True)
fig.update_layout(
    plot_bgcolor='GhostWhite'
)
# fig.show()
fig.write_html('all_branches_generated_graph.html')

j = []
for k in fulldf.keys():
    if 't' not in k and 'm' not in k and k != 'Time':
        j.append(k)

print(j)

dfs = {}
for name in j:
    d = {}
    for k in fulldf.keys():
        if k == 'Time':
            continue
        if str(name) in str(k):
            d[k] = fulldf[k].to_list()
    d['Time'] = fulldf['Time'].to_list()
    ws = pd.DataFrame(data=d)

    dfs[name] = ws
for df in dfs:
    print(dfs[df])


fig = go.Figure()

for i in dfs['9839'].keys():
    if i == 'Time':
        continue
    fig.add_trace(go.Scatter(x = fulldf['Time'],
                                y = fulldf[i], 
                                name = i))


fig.update_xaxes(rangeslider_visible=True,)
fig.update_layout(
    plot_bgcolor='GhostWhite'
)
# fig.show()
# fig.write_html('generated_graph.html')

cdf = fulldf.copy()

def fillcolc(label):
    if label >= 1:
        return 'red'
    else:
        return 'GhostWhite'

fig = go.Figure()

fulldf['label'] = np.where(fulldf['9839']>fulldf['9839_t'], 1, 0)
fulldf['group'] = fulldf['label'].ne(fulldf['label'].shift()).cumsum()
fulldf = fulldf.groupby('group')
dfz = []
for name, data in fulldf:
    dfz.append(data)
try:
    for df in dfz:
        print(df)
        fig.add_trace(go.Scatter(x = df['Time'], 
                                y = df['9839_t']
                                , name = '9839_t',
                                showlegend=False,
                                line = dict(color='red', width=0)))

        fig.add_trace(go.Scatter(x = df['Time'], 
                                y = df['9839'],
                                name = '9839',
                                line = dict(color='red', width=0),
                                showlegend=False,
                                fill='tonexty',
                                fillcolor= fillcolc(df['label'].iloc[0])))
except Exception as e:
    pass

fig.add_trace(go.Scatter(x = cdf['Time'], 
                        y = cdf['9839_t']
                        , name = 'Dynamically Generated Alert Threshold',
                        line = dict(color = 'DodgerBlue', width=3),
                        ))

fig.add_trace(go.Scatter(x = cdf['Time'], 
                        y = cdf['9839'],
                        name = 'Branch 9839 Webapp Response Time',
                        line = dict(color = 'Olive', width=3)))

fig.update_xaxes(rangeslider_visible=True)
# print(fulldf)
# print(fulldf['label'].iloc[0])
fig.update_layout(
    # showlegend=False,
    plot_bgcolor='GhostWhite',
    title="Response Time Anomaly Detection for Branch 9839",
    yaxis_title="Response Time for Branch 9839 Webapp",
    xaxis_title="Time",
    legend_title="DataType",
    font=dict(
        family="Arial",
        size=20,
        color="DarkSlateGray"))
fig.show()
fig.write_html('generated_graph.html')









# def line_intersection(line1, line2):
#     xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
#     ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

#     def det(a, b):
#         return a[0] * b[1] - a[1] * b[0]

#     div = det(xdiff, ydiff)
#     if div == 0:
#        raise Exception('lines do not intersect')

#     d = (det(*line1), det(*line2))
#     x = det(d, xdiff) / div
#     y = det(d, ydiff) / div
#     return x, y


# print(fulldf.query("Time=={}".format(60)))
# print(fulldf['Time'])

# time = dfs['9839']['Time'].to_list()
# arr1 = dfs['9839']['9839'].to_list()
# arr2 = dfs['9839']['9839_t'].to_list()

# previousT = None

# for i in range(len(time)):
#     print(time[i],arr1[i],arr2[i])
#     if previousT:
#         l1 = ((previousT[0],previousT[1])(time[i],arr1[i]))
#         l2 = ((previousT[0],previousT[2])(time[i],arr2[i]))
#         print(line_intersection(l1,l2))
#     previousT = (time[i],arr1[i],arr2[i])


# def if_intersect(line1, lin2):
#     xdiff = ( , )



# print line_intersection((A, B), (C, D))


























# lst0 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
# lst1 = [2,4,1,4,1,5,7,8,3,2,4,7,8,2,1]
# lst2 = [9,1,3,7,8,2,0,1,2,5,9,3,5,2,6]

# x = fulldf['Time'].to_numpy()
# y = fulldf['4873'].to_numpy()
# z = fulldf['6128'].to_numpy()

# # slopes and offsets lst1 vs lst0
# m = np.diff(y)/np.diff(x)
# n = y[1:] - m * x[1:]

# # slopes and offsets lst2 vs lst0
# k = np.diff(z)/np.diff(x)
# l = z[1:] - k * x[1:]

# # intersections
# with np.errstate(divide='ignore'):
#     xs = (n - l) / (k - m)
#     ys = m * xs + n

# # only take intersections that lie in the respective segment
# mask = (xs >= x[:-1]) & (xs <= x[1:])
# intersections = np.unique(np.row_stack((xs[mask], ys[mask])), axis=1)

# # display result
# ax = fulldf.set_index('Time').plot(legend=False)
# ax.plot(intersections[0], intersections[1], 'ro')


























# print(df.query("Branches=='4873'"))

# class TBranch(object):
#     def __init__(self):
#         self.name = None
#         self.data = []
#         self.x = []
#         self.y = []

# Tbranches = []

# with open(dataPath,'r') as csvfile:
#     csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
#     next(csvreader)
#     for row in csvreader:
#         branch = TBranch()
#         count = 0
#         for c in row:
#             if not branch.name:
#                 branch.name = c
#                 # data['branch'] = c
#                 continue
#             branch.data.append((int(count),int(c)))
#             branch.x.append(int(count))
#             # data['seconds'] = count
#             branch.y.append(int(c))
#             # data['latency'] = c
#             count += 60
#         branches.append(branch)



# data = {'Branches':[],'Seconds':[],'Metric':[]}
# # data = {}
# for branch in branches:
#     for d in branch.data:
#         data['Branches'].append(branch.name)
#         data['Seconds'].append(d[0])
#         data['Metric'].append(d[1])



# df = pd.DataFrame(data=data)
# df = df.sort_values(by='Seconds')


# dataframes = {}
# for branch in branches:
#     dataframes[branch.name] = pd.DataFrame(data={'Seconds':branch.x,'Metric':branch.y})

# fig = go.Figure()

# for i in dataframes:
#     fig.add_trace(go.Scatter(x = dataframes[i]["Seconds"],
#                                 y = dataframes[i]["Metric"], 
#                                 name = i))


# fig.update_xaxes(rangeslider_visible=True)
# fig.update_layout(
#     plot_bgcolor='GhostWhite'
# )
# fig.show()
























# print(pd.unique(df['Branches']))

# df = df.sort_values(by='Seconds')

# fig = px.line(df, x='Seconds',y='Metric', color="Branch")
# fig.update_xaxes(rangeslider_visible=True)
# # fig.update_layout(
# #     plot_bgcolor='white'
# # )
# fig.show()

# print(df['Branches'].loc['7157'])

# for branch in pd.unique(df['Branches']):








# # plot the data
# 

# # fig, ax = plt.subplots()

# # ax.plot(branches[0].x,branches[0].y)
# # fig.savefig('test.png')
# # plt.show()



# df = px.data.gapminder().query("continent=='Oceania'")
# print(df)
# # d = {}

# # for branch in branches:
# #     d[branch.name] = branch.y
# # df = pd.DataFrame(data=d)
# # print(df)

# # d = {'branch1':branches[0].x,'time':branches[0].y}

# # df = pd.DataFrame(data=data)
# # print(df)
# # input()

# # fig = px.line(df)
# # # fig.update_xaxes(rangeslider_visible=True,)
# # # fig.write_html('./test.html')
# # fig.show()

# # df = pd.read_csv('./test.csv')



# # # better = df.T
# # # better.to_csv('./test.csv')

# # print(df)

# # fig = px.line(df,x='time',y='7157')


# # fig.show()

# # import plotly.express as px
# # import pandas as pd

# df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')

# fig = px.line(df, x='Date', y='AAPL.High', title='Time Series with Rangeslider')

# fig.update_xaxes(rangeslider_visible=True)
# fig.show()



# # import pandas as pd

# # from plotly.offline import iplot

# # # dict for the dataframes and their names
# # dfs = {"df1" : df1, "df2": df2, "df3" : df3, "df4" : df4, "df5" : df5}

