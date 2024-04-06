import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Load participant data
data = {
    'Participant': ['Participant 1'] * 14 + ['Participant 2'] * 14 + ['Participant 3'] * 14,
    'Date': ['3/5/24', '3/6/24', '3/7/24', '3/8/24', '3/9/24', '3/10/24', '3/11/24', '3/12/24', '3/13/24', '3/14/24', '3/15/24', '3/16/24', '3/17/24', '3/18/24'] * 3,
    'Num_Steps': [4242, 3090, 4869, 5181, 2104, 3717, 5116, 5087, 3202, 4875, 3216, 6219, 3404, 4679, 2156, 2059, 1523,
                  2449, 3757, 3290, 2271, 2154, 2125, 2355, 2371, 3152, 2281, 1855, 4402, 6384, 5574, 7676, 5714, 6017,
                  5180, 5941, 6265, 6481, 6187, 2370, 5594, 6203],
    'Active_Hours': [13, 12, 14, 15, 7, 4, 13, 15, 13, 14, 13, 13, 12, 13,
                     9, 11, 9, 9, 12, 9, 11, 12, 13, 12, 14, 8, 12, 10,
                     10, 14, 14, 16, 12, 12, 15, 14, 16, 12, 13, 6, 13, 14],
    'Calories_Burned': [620, 673, 950, 861, 576, 552, 753, 738, 802, 966, 824, 689, 765, 864,
                        167, 160, 118, 190, 292, 256, 228, 167, 165, 183, 184, 245, 201, 144,
                        1405, 1464, 1952, 1866, 1439, 1084, 1870, 1695, 1695, 1948, 1612, 1159,1249, 1348],
    'Distance_Walked_Mi': [1.6, 1.11, 1.76, 1.88, 0.81, 1.46, 1.9, 1.92, 1.17, 1.79, 1.16, 2.43,
                           1.12, 1.45, 0.97, 0.92, 0.68, 1.1, 1.69, 1.48, 1.02, 0.97, 0.95, 1.06,
                           1.06, 1.42, 1.3, 0.83, 1.65, 2.38, 2.06, 2.94, 2.26, 2.42, 2.34, 2.25,
                           2.33, 2.46, 2.3, 0.89, 2.45, 2.23]
}

df = pd.DataFrame(data)

# Create app
app = dash.Dash(__name__, external_stylesheets=['https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css'])
server = app.server

# Define app layout
app.layout = html.Div([
    html.H1("Elderly Smartwatch Usage Participant Data"),
    dcc.Dropdown(
        id='participant-dropdown',
        options=[{'label': participant, 'value': participant} for participant in df['Participant'].unique()],
        value=['Participant 1'],
        multi=True
    ),
    dcc.Checklist(
        id='data-toggle',
        options=[
            {'label': 'step count', 'value': 'Num_Steps'},
            {'label': 'active hours', 'value': 'Active_Hours'},
            {'label': 'calories burned', 'value': 'Calories_Burned'},
            {'label': 'distance walked (mi)', 'value': 'Distance_Walked_Mi'}
        ],
        value=['Num_Steps']
    ),
    dcc.Graph(id='line-plot'),
])

# Define callback to update the line plot
@app.callback(
    Output('line-plot', 'figure'),
    [Input('participant-dropdown', 'value'),
     Input('data-toggle', 'value')]
)
def update_line_plot(selected_participants, selected_data):
    filtered_df = df[df['Participant'].isin(selected_participants)]
    fig = px.line(filtered_df, x='Date', y=selected_data, color='Participant', title='Participant Data Comparison')
    fig.update_xaxes(title='Date')
    fig.update_yaxes(title='Value')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
