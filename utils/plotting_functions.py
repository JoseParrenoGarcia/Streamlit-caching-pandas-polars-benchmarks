import plotly.express as px
import plotly.graph_objects as go

color_mapping = {
    'pandas': px.colors.qualitative.Plotly[0],
    'pandas_to_polars': px.colors.qualitative.Plotly[0],
    'pandas_cached': px.colors.qualitative.Plotly[1],
    'pandas_to_polars_cached': px.colors.qualitative.Plotly[1],
    'polars': px.colors.qualitative.Plotly[2],
    'polars_to_pandas': px.colors.qualitative.Plotly[2],
    'polars_cached': px.colors.qualitative.Plotly[3],
}

axis_line_colour = 'rgb(213, 219, 219)'
axis_line_width = 2


def _yaxis_primary_basic_formatting(fig, feature, manual_minor_dtick=0.2):
    fig.update_yaxes(title=dict(text=feature), linecolor=axis_line_colour, linewidth=axis_line_width,
                     minor=dict(ticklen=4,
                                tickwidth=1,
                                tickcolor="grey",
                                showgrid=True,
                                gridcolor='rgb(248, 249, 249)',
                                dtick=manual_minor_dtick,)
                     )


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


def _calculate_minor_dtick(max_value):
    ranges = [
        (0, 1, 0.05),
        (1, 10, 0.2),
        (10, 20, 0.5),
        (20, 100, 5),
    ]

    for lower, upper, dtick in ranges:
        if lower <= max_value < upper:
            return dtick


def plot_execution_time_bar_charts(df, chart_title=''):
    df['nrows_string'] = df['Number of rows'].astype(int).apply(_format_number_of_rows)

    fig = px.bar(
        df,
        x='nrows_string',
        y='Execution Time',
        color='Data format',
        barmode='group',
        text_auto=True,
        color_discrete_map=color_mapping,
    )

    # Update the layout to format text labels
    fig.update_traces(texttemplate='%{y:.2f}', textposition='outside')

    # Update text color to match bar color
    fig.for_each_trace(lambda trace: trace.update(textfont_color=trace.marker.color))

    _xaxis_primary_basic_formatting(fig=fig, feature='Number of rows')
    _yaxis_primary_basic_formatting(fig=fig, feature='Execution time (s)', manual_minor_dtick=_calculate_minor_dtick(df['Execution Time'].max()))

    fig.update_layout(title=dict(text=chart_title), template='plotly_white', height=420)

    # Convert to a graph objects figure
    fig = go.Figure(fig)

    # Sort the traces based on their names
    sorted_data = sorted(fig.data, key=lambda x: x.name)

    # Update the figure with sorted traces
    fig.data = sorted_data

    return fig


def plot_execution_time_comparison_bar_charts(df, selected_baseline, chart_title=''):
    df['nrows_string'] = df['Number of rows'].astype(int).apply(_format_number_of_rows)

    fig = px.bar(
        df,
        x='nrows_string',
        y='Ratio',
        color='Data format',
        barmode='group',
        text_auto=True,
        color_discrete_map=color_mapping,
    )

    # Update the layout to format text labels
    fig.update_traces(texttemplate='%{y:.1f}', textposition='outside')

    # Update text color to match bar color
    fig.for_each_trace(lambda trace: trace.update(textfont_color=trace.marker.color))

    _xaxis_primary_basic_formatting(fig=fig, feature='Number of rows')
    _yaxis_primary_basic_formatting(fig=fig, feature=f'Ratio of {selected_baseline} / other formats', manual_minor_dtick=_calculate_minor_dtick(df['Ratio'].max()))

    fig.update_layout(title=dict(text=chart_title), template='plotly_white', height=420)

    return fig
