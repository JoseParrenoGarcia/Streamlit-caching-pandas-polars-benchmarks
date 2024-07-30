import plotly.express as px


axis_line_colour = 'rgb(213, 219, 219)'
axis_line_width = 2


def _yaxis_primary_basic_formatting(fig, feature):
    fig.update_yaxes(title=dict(text=feature), linecolor=axis_line_colour, linewidth=axis_line_width,)


def _xaxis_primary_basic_formatting(fig, feature):
    fig.update_xaxes(title=dict(text=feature), linecolor=axis_line_colour, linewidth=axis_line_width, showgrid=False)


def _format_number_of_rows(num_str):
    num = int(num_str)
    if num >= 1_000_000:
        return f"{num / 1_000_000:.0f}m"
    elif num >= 1_000:
        return f"{num / 1_000:.0f}k"
    else:
        return str(num)

def plot_execution_time_bar_charts(df):
    df['nrows_string'] = df['Number of rows'].astype(int).apply(_format_number_of_rows)

    fig = px.bar(
        df,
        x='nrows_string',
        y='Execution Time',
        color='Data format',
        barmode='group',
        # title='Execution Time by Number of Rows and Data Format',
        # labels={'number_of_rows': 'Number of Rows', 'execution_time': 'Execution Time (seconds)', 'data_format': 'Data Format'}
    )

    _xaxis_primary_basic_formatting(fig=fig, feature='Number of rows')
    _yaxis_primary_basic_formatting(fig=fig, feature='Execution time (s)')

    fig.update_layout(title=dict(text=''), template='plotly_white')

    return fig
