from matplotlib import pyplot as plt
from functools import singledispatch
from ipamd.public.models.data import *
from ipamd.public.utils.output import warning
from ipamd.public.utils.plugin_manager_v1 import PluginBase

@singledispatch
def plot(data):
    pass

@plot.register
def _(data: Vector):
    pass

@plot.register
def _(data: Scalar):
    warning("Scalar data cannot be plotted.")
    PluginBase.call('print', data)

@plot.register
def _(data: Matrix):
    plt.imshow(data.data, cmap='viridis', origin='lower')
    plt.colorbar()
    plt.title(data.meta['title'])
    plt.xlabel(data.meta['x_label'])
    plt.xticks(data.meta['x_axis'])
    plt.ylabel(data.meta['y_label'])
    plt.yticks(data.meta['y_axis'])

def func(data, style=None, save_figure=True):
    with plt.rc_context(style):
        plot(data)
        plt.show()
        if save_figure:
            plt.savefig(f"{data.meta['title']}.png")

def f(slf, ref=None, style={}, save=False):

    match slf.type:
        case AnalysisResult.Type.SCALAR:
            warning('Scalar data is not suitable for plotting')
            output(f'But the value of {slf.title} is {slf.data}')
        case AnalysisResult.Type.VECTOR:
            data_x = []
            data_y = []
            for x in slf.data.keys():
                data_x.append(x)
                data_y.append(slf.data[x])
            if len(data_x) > 20:
                plt.gca().xaxis.set_major_locator(ticker.AutoLocator())
                plt.gca().xaxis.set_minor_locator(ticker.AutoMinorLocator(4))
            plt.plot(data_x, data_y, color)
            if ref:
                auto_generated_legend = ['data']
                for d in ref:
                    ref_data = d.data
                    y_ref = []
                    if d.type == AnalysisResult.Type.SCALAR:
                        y_ref = [ref_data] * len(data_x)
                    elif d.type == AnalysisResult.Type.VECTOR:
                        for x in ref_data.keys():
                            y_ref.append(ref_data[x])
                        auto_generated_legend.append(d.title)
                    else:
                        error('Data type not suitable for plotting ref fig')
                    plt.plot(data_x, y_ref)
                plt.legend(
                    auto_generated_legend if legend is None else legend,
                    frameon=False,
                    prop = {'size': 16}
                )

        case AnalysisResult.Type.MATRIX:
            data = []
            title_x = []
            title_y = []
            for x in slf.data.keys():
                row = []
                title_y.append(x)
                row_length = len(slf.data[x].keys())
                for y in slf.data[x].keys():
                    if len(title_x) < row_length:
                        title_x.append(y)
                    row.append(slf.data[x][y])
                data.append(row)
            n_x = len(title_x)
            n_y = len(title_y)
            if n_x > 20:
                label_interval_x = len(title_x) // 8
            else:
                label_interval_x = 1
            if n_y > 20:
                label_interval_y = len(title_y) // 8
            else:
                label_interval_y = 1
            plt.xticks(np.arange(0, n_x, label_interval_x), title_x[::label_interval_x])
            plt.yticks(np.arange(0, n_y, label_interval_y), title_y[::label_interval_y])
            plt.imshow(data)
            cbar = plt.colorbar()
            cbar.ax.tick_params(labelsize=16)
        case AnalysisResult.Type.DISTRIBUTION:
            data = []
            for group in slf.data.keys():
                for v in slf.data[group]:
                    data.append(v)
            plt.hist(data, bins=len(slf.data.keys()), edgecolor='black', linewidth=1.5)

        case AnalysisResult.Type.RATIO:
            labels = []
            sizes = []
            for group in slf.data.keys():
                labels.append(group)
                sizes.append(slf.data[group])
            plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, shadow=True)

        case _:
            error('Unknown data type')
            return
    plt.tight_layout()
    if save:
        plt.savefig(f'{slf.title}.png')

    plt.show()