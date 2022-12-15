from random import randint
from pandas import DataFrame

# Presentation: Graphs

class Data:
    def __init__(self, title=None, values=None, xAxis=None, legend=None, unit=None, special=None):
        self.title = title
        self.values = values
        self.xAxis = xAxis
        self.legend = legend
        self.unit = unit
        self.special = special


def earning_line(earning_pd: DataFrame):
    data = Data()
    data.title = 'Earnings'
    if earning_pd is None:
        return data

    x_axis = earning_pd.index.values.tolist()
    if earning_pd.empty:
        revenues = []
        earnings = []
    else:
        revenues = earning_pd['Revenue'].values.tolist()
        earnings = earning_pd['Earnings'].values.tolist()

    data.values = [
        {
            'name': 'Revenue',
            'values': [i / 1000000 for i in revenues]
        },
        {
            'name': 'Earning',
            'values': [i / 1000000 for i in earnings]
        }
    ]
    data.legend = [key['name'] for key in data.values]
    data.xAxis = x_axis
    data.unit = '$1000,000'
    return data


def holders_pie(holders: DataFrame):
    data = Data()
    data.title = 'Known Share Holders'
    if holders is None:
        return data

    cols = holders.columns.values.tolist()
    holder_names = [h for h in holders[cols[0]].to_list()]
    holder_shares = [s for s in holders[cols[1]].to_list()]

    data.values = []
    for n in range(len(holder_names)):
        data.values.append({'name': holder_names[n], 'value': holder_shares[n]})

    data.legend = holder_names
    data.unit = 'shares'
    return data

