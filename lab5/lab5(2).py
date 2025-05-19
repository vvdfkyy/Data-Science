import numpy as np
from dash import Dash, dcc, html, Input, Output, State, ctx
import plotly.graph_objs as go

TIME = np.linspace( 0, 10, 1000 )

def generate_clean_signal( t, amp, freq, phase ) :
    return amp * np.sin( freq * t + phase )

def generate_noise_signal( mean, cov, size ) :
    return np.random.normal( mean, np.sqrt(cov), size=size )

def moving_average_filter( signal, window_size ) :
    if window_size < 1 :
        return signal
    kernel = np.ones( window_size ) / window_size
    return np.convolve( signal, kernel, mode='same' )

# Початкові значення
DEFAULTS = {
    'amp': 1.0,
    'freq': 1.0,
    'phase': 0.0,
    'noise_mean': 0.0,
    'noise_cov': 0.01,
    'window_size': 5,
    'noise_toggle': ['show'],
    'filter_select': 'moving_average'
}

app = Dash( __name__ )
app.title = "Візуалізація сигналу з шумом та фільтрацією"

app.layout = html.Div( style={'backgroundColor': '#2e2e2e', 'padding': '20px'}, children=[

    html.H1("Візуалізація сигналу з шумом та фільтрацією", style={ 'textAlign': 'center', 'color': 'white' }),

    dcc.Store(id='reset-store', data=DEFAULTS),

    html.Div([
        html.Label("Вибір фільтра", style={'color': 'white'}),
        dcc.Dropdown(
            id='filter-select',
            options=[
                {'label': 'Ковзне середнє', 'value': 'moving_average'},
            ],
            value=DEFAULTS['filter_select'],
            style={'width': '50%'}
        ),
    ], style={ 'marginBottom': '20px' }),

    html.Div([
        html.Div([dcc.Graph( id='original-signal' )], style={'width': '50%'}),
        html.Div([dcc.Graph( id='filtered-signal' )], style={'width': '50%'})
    ], style={'display': 'flex'}),

    html.Div([
        html.Div([
            html.Label( "Амплітуда", style={'color': 'white'} ),
            dcc.Slider( 0.1, 2.0, step=0.1, value=DEFAULTS['amp'], id='amp-slider', tooltip={"always_visible": False} ) 
        ]),
        html.Div([
            html.Label( "Частота", style={'color': 'white'} ),
            dcc.Slider( 0.1, 5.0, step=0.2, value=DEFAULTS['freq'], id='freq-slider', tooltip={"always_visible": False} )
        ]),
        html.Div([
            html.Label( "Фаза", style={'color': 'white'} ),
            dcc.Slider( 0, 2 * np.pi, step=np.pi/8, value=DEFAULTS['phase'], id='phase-slider', tooltip={"always_visible": False} )
        ]),
        html.Div([
            html.Label( "Середнє шуму", style={'color': 'white'} ),
            dcc.Slider( -1.0, 1.0, step=0.1, value=DEFAULTS['noise_mean'], id='noise-mean-slider', tooltip={"always_visible": False} )
        ]),
        html.Div([
            html.Label( "Дисперсія шуму", style={'color': 'white'} ),
            dcc.Slider( 0.01, 1.0, step=0.05, value=DEFAULTS['noise_cov'], id='noise-cov-slider', tooltip={"always_visible": False} )
        ]),
        html.Div([
            html.Label( "Розмір вікна фільтра", style={'color': 'white'} ),
            dcc.Slider( 1, 100, step=1, value=DEFAULTS['window_size'], id='window-size-slider', tooltip={"always_visible": False} )
        ]),
        html.Div([
            html.Label( "Показати шум", style={'color': 'white'} ),
            dcc.Checklist(
                options=[{'label': 'Увімк.', 'value': 'show'}],
                value=DEFAULTS['noise_toggle'],
                id='noise-toggle',
                style={'color': 'white'}
            )
        ]),
        html.Button( "Скинути", id='reset-button', n_clicks=0, style={'marginTop': '20px'})
    ], style={ 'marginTop': '20px' })
])

@app.callback(
    Output('amp-slider', 'value'),
    Output('freq-slider', 'value'),
    Output('phase-slider', 'value'),
    Output('noise-mean-slider', 'value'),
    Output('noise-cov-slider', 'value'),
    Output('window-size-slider', 'value'),
    Output('noise-toggle', 'value'),
    Output('filter-select', 'value'),
    Input('reset-button', 'n_clicks'),
    State('reset-store', 'data'),
    prevent_initial_call=True
)
def reset_values( n_clicks, defaults ) :
    return (
        defaults['amp'],
        defaults['freq'],
        defaults['phase'],
        defaults['noise_mean'],
        defaults['noise_cov'],
        defaults['window_size'],
        defaults['noise_toggle'],
        defaults['filter_select']
    )

@app.callback(
    Output('original-signal', 'figure'),
    Output('filtered-signal', 'figure'),
    Input('amp-slider', 'value'),
    Input('freq-slider', 'value'),
    Input('phase-slider', 'value'),
    Input('noise-mean-slider', 'value'),
    Input('noise-cov-slider', 'value'),
    Input('noise-toggle', 'value'),
    Input('window-size-slider', 'value'),
    Input('filter-select', 'value')
)
def update_graph( amp, freq, phase, noise_mean, noise_cov, noise_toggle, window_size, filter_method ) :
    np.random.seed( 42 )
    clean = generate_clean_signal( TIME, amp, freq, phase )
    noise = generate_noise_signal( noise_mean, noise_cov, TIME.shape )
    noisy_signal = clean + noise

    if filter_method == 'moving_average' :
        filtered = moving_average_filter( noisy_signal, window_size )
    else :
        filtered = noisy_signal

    fig_clean = go.Figure( )
    fig_clean.add_trace( go.Scatter(
        x=TIME, y=clean,
        name='Чистий сигнал',
        line=dict(color='#1abc9c')
    ) )
    fig_clean.update_layout(
        title='Чистий сигнал',
        plot_bgcolor='#2e2e2e',
        paper_bgcolor='#2e2e2e',
        font_color='white',
        xaxis_title="Час",
        yaxis_title="Амплітуда",
        xaxis=dict(range=[0, 10]),
        yaxis=dict(range=[-2, 2]),
        showlegend=True
    )

    fig_filt = go.Figure( )

    fig_filt.add_trace( go.Scatter(
        x=TIME, y=noisy_signal,
        name='Сигнал з шумом',
        line=dict(color='#e67e22'),
        visible=True if 'show' in noise_toggle else 'legendonly'
    ) )

    fig_filt.add_trace( go.Scatter(
        x=TIME, y=filtered,
        name='Фільтрований сигнал',
        line=dict(color='#9b59b6')
    ) )

    fig_filt.update_layout(
        title='Фільтрований сигнал',
        plot_bgcolor='#2e2e2e',
        paper_bgcolor='#2e2e2e',
        font_color='white',
        xaxis_title="Час",
        yaxis_title="Амплітуда",
        xaxis=dict(range=[0, 10]),
        yaxis=dict(range=[-2, 2])
    )

    return fig_clean, fig_filt

if __name__ == '__main__' :
    app.run( debug=True )
