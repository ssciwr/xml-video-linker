 

from dash import Dash, Input, Output, State, callback, dash_table, dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import base64
import io

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    'Load an xml file.',

    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '40%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlimport base64ign': 'center',
            'margin': '10px'
        },
     
    ),
    html.Div(
     dash_table.DataTable( id='tbl_xml'),       
                            style={"with":"30%"}),
    dbc.Alert(id='tbl_out'),
])

@callback(Output('tbl_out', 'children'), Input('tbl_xml', 'active_cell'))
def update_graphs(active_cell):
    return str(active_cell) if active_cell else "Click the table"


@callback(
    Output("tbl_xml","data" ),
    Output("tbl_xml","columns"),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
    prevent_initial_call=True
    )
def update_output(content, name):
    if content is None:
        return None

    content_type, content_string = content.split(",")
    decoded = base64.b64decode(content_string)
    
    df = pd.read_xml(io.StringIO(decoded.decode("utf-8")), xpath="./recording/turn")

    return df.to_dict('records'), [{"name": i, "id": i} for i in df.columns]