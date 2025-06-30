import plotly.express as px
import plotly.graph_objects as go
import math
from babel.numbers import format_number
from math import ceil

def filter_data(df, state=None, region=None):
    filtered = df.copy()
    if state:
        filtered = filtered[filtered['STATE/UT'] == state]
    if region:
        filtered = filtered[filtered['Region'] == region]
    return filtered

def calculate_total_production(filtered_df):
    total = ceil(filtered_df['Production'].sum())
    return format_number(total, locale='en_IN')

def calculate_avg_production(filtered_df):
    total = ceil(filtered_df['Production'].mean())
    return format_number(total, locale='en_IN')


def count_unique_states(filtered_df):
    return filtered_df['STATE/UT'].nunique()

def count_unique_regions(filtered_df):
    return filtered_df['Region'].nunique()



def generate_top5_states_chart(df):
    # Group by state and sum production
    state_prod = df.groupby('STATE/UT')['Production'].sum().reset_index()

    # Get top 5
    top5 = state_prod.sort_values(by='Production', ascending=False).head(5)

    # Create a bar chart
    fig = px.bar(top5,
                 x='STATE/UT',
                 y='Production',
                 color='Production',
                 color_continuous_scale='Blues',
                 text=top5['Production'].round(2),
                 labels={'STATE/UT': 'State/UT', 'Production': 'Production (KL)'}
                )

    fig.update_layout(
        title={
            'text': 'Best Performing States',
            'y': 0.95,
            'x': 0.42,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 18, 'color': '#2c3e50'}
        },
        title_x=0.5,
        xaxis_title='State',
        yaxis_title='Total Production (KL)',
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    fig.update_traces(textposition='outside')
    config = {
        'displayModeBar': False,
        'staticPlot': True
    }

    return fig.to_html(full_html=False, config=config)


def generate_bottom5_states_chart(df):
    # Group by state and sum production
    state_prod = df.groupby('STATE/UT')['Production'].sum().reset_index()

    # Get bottom 5
    bottom5 = state_prod.sort_values(by='Production', ascending=True).head(5)

    # Create a bar chart
    fig = px.bar(
        bottom5,
        x='STATE/UT',
        y='Production',
        color='Production',
        color_continuous_scale='Reds',
        text=bottom5['Production'].round(2),
        labels={'STATE/UT': 'State/UT', 'Production': 'Production (KL)'}
    )

    fig.update_layout(
        title={
            'text': 'Least Performing States',
            'y': 0.95,
            'x': 0.42,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 18, 'color': '#2c3e50'}
        },
        title_x=0.5,
        xaxis_title='State',
        yaxis_title='Total Production (KL)',
        plot_bgcolor='white',
        paper_bgcolor='white',
        width=880,
        height=450,
    )
    fig.update_traces(textposition='outside')

    config = {
        'displayModeBar': False,
        'staticPlot': True
    }

    return fig.to_html(full_html=False, config=config)


def generate_oiltype_donut_chart(df):
    # Group by oil type and sum production
    oiltype_prod = df.groupby('Oil_type')['Production'].sum().reset_index()

    # Custom color palette - modern, vibrant colors
    custom_colors = [
        '#08306b',  # Coral Red
        '#a9cfe5',  # Turquoise
        '#45B7D1',  # Sky Blue
        '#96CEB4',  # Mint Green
        '#FFEAA7',  # Warm Yellow
        '#DDA0DD',  # Plum
        '#98D8C8',  # Seafoam
        '#F7DC6F',  # Light Gold
        '#BB8FCE',  # Lavender
        '#85C1E9'  # Light Blue
    ]

    # Create a donut chart with enhanced styling
    fig = go.Figure(data=[go.Pie(
        labels=oiltype_prod['Oil_type'],
        values=oiltype_prod['Production'],
        hole=0.45,  # Slightly larger hole for modern look
        marker=dict(
            colors=custom_colors[:len(oiltype_prod)],
            line=dict(color='white', width=3)  # White borders between slices
        ),
        textinfo='percent+label',
        textfont=dict(size=13, color='white', family='Arial Black'),
        pull=[0.05] * len(oiltype_prod),  # More pronounced pull
        hovertemplate='<b>%{label}</b><br>' +
                      'Production: %{value:,.0f}<br>' +
                      'Percentage: %{percent}<br>' +
                      '<extra></extra>',  # Custom hover template
        rotation=90  # Rotate the chart for better visual balance
    )])

    # Enhanced layout with gradient background and better typography
    fig.update_layout(
        title={
            'text': 'Total Production by Oil Type',
            'y': 0.95,
            'x': 0.42,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 18, 'color': '#2c3e50'}
        },
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.86,
            xanchor="right",
            x=0.2,
            font=dict(size=8, color='#34495E'),
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='#BDC3C7',
            borderwidth=1
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        width=530,
        height=560,
        margin=dict(t=15, b=75, l=33, r=130),
        annotations=[
            dict(
                text='<b>Oil Production<br>Analysis</b>',
                x=0.5, y=0.5,
                font=dict(size=16, color='#7F8C8D', family='Arial'),
                showarrow=False
            )
        ]
    )

    # Add a subtle shadow effect
    fig.update_traces(
        marker=dict(
            line=dict(color='rgba(255,255,255,0.8)', width=2)
        )
    )

    return fig.to_html(full_html=False)


def generate_regionwise_donut_chart_ocean_gradient(df):
    # Group by Region and sum production
    region_prod = df.groupby('Region')['Production'].sum().reset_index()

    # Ocean-inspired blue gradient with teal accents
    donut_chart_colors = [
    '#08306b',  # Soft Navy Blue
    '#084e97',  # Orange
    '#80bfbf',  # Coral Red
    '#a9cfe5',  # Teal
    '#d4e4f4',
    '#a9cfe5'
    ]

    # Create donut chart
    fig = px.pie(
        region_prod,
        names='Region',
        values='Production',
        hole=0.4,
        color_discrete_sequence=donut_chart_colors
    )

    # Ocean-themed styling
    fig.update_traces(
        textinfo='percent+label',
        textfont_size=11,
        textfont_color='white',  # Dark teal text
        textfont_family='Segoe UI',
        pull=[0.02] * len(region_prod),
        marker=dict(
            line=dict(color='white', width=3)
        )
    )

    fig.update_layout(
        title={
            'text': 'Region Wise Production',
            'y': 0.95,
            'x': 0.45,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 18, 'color': '#2c3e50'}
        },
        paper_bgcolor='rgba(225,225,225,0)',  # Very light green background
        showlegend=False,
        width=530,
        height=560,
        margin=dict(l=50, r=120, t=20, b=120)
    )

    return fig.to_html(full_html=False)


def generate_production_trend_area_chart(df):
    # Group by Year and sum production
    yearly_trend = df.groupby('Year')['Production'].sum().reset_index()

    # Create area chart
    fig = px.area(
        yearly_trend,
        x='Year',
        y='Production',
        labels={'Production': 'Total Production (KL)'},
        color_discrete_sequence=['#008080']  # Teal color
    )

    # Customize layout
    fig.update_layout(
        title={
            'text': 'Year Wise Production Total by Oil Type',
            'x': 0.5,
            'xanchor': 'center',
            'font': {
                'size': 18,  # ✅ Change size here
                'color': '#2c3e50'
            }
        },
        width=800,
        height=390,
        title_x=0.5,
        xaxis_title='Year',
        yaxis_title='Production (KL)',
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=80, r=150, t=75, b=69),
        hovermode='x unified',
        yaxis=dict(
            gridcolor='#d3d3d3',
            gridwidth=1,
            griddash='dot',
            zeroline=False,
            range=[30000, yearly_trend['Production'].max() + 50000]


        )
    )

    # Smooth lines and filled area
    fig.update_traces(mode='lines', line_shape='spline', fill='tozeroy')

    return fig.to_html(full_html=False)


def generate_professional_stacked_chart(df):
    # Group by Year and Oil_type, then sum Production
    grouped = df.groupby(['Year', 'Oil_type'])['Production'].sum().reset_index()

    # Professional color palette - modern and accessible
    professional_colors = [
        '#a9cfe5',  # Deep blue
        '#08306b',  # Red
        '#0C1117',  # Amber
        '#FCBF49',  # Yellow
        '#003566',  # Navy
        '#BC6C25'  # Brown
    ]

    # Create the chart
    fig = px.bar(
        grouped,
        x='Year',
        y='Production',
        color='Oil_type',
        labels={
            'Production': 'Production Volume (KL)',
            'Oil_type': 'Oil Type',
            'Year': 'Year'
        },
        color_discrete_sequence=professional_colors
    )

    # Enhanced professional styling
    fig.update_layout(

        title={
            'text': 'Production Trends Over Years',
            'y': 0.95,
            'x': 0.45,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 18, 'color': '#2c3e50'}
        },
        # Chart structure
        barmode='stack',

        # Axes styling
        xaxis={
            'title': {
                'text': 'Year',
                'font': {'size': 12, 'color': '#2c3e50'}
            },
            'tickfont': {'size': 12, 'color': '#34495e'},
            'showgrid': False,
            'linecolor': '#bdc3c7',
            'linewidth': 1
        },

        yaxis={
            'title': {
                'text': 'Production Volume (KL)',
                'font': {'size': 12, 'color': '#2c3e50'}
            },
            'tickfont': {'size': 12, 'color': '#34495e'},
            'gridcolor': '#ecf0f1',
            'gridwidth': 1,
            'zeroline': False,
            'linecolor': '#bdc3c7',
            'linewidth': 1,
            'tickformat': ',.0f'  # Format numbers with commas
        },

        # Legend styling
        legend={
            'title': {
                'text': '<b>Oil Type</b>',
                'font': {'size': 8, 'color': '#2c3e50'}
            },
            'font': {'size': 8, 'color': '#34495e'},
            'bgcolor': 'rgba(255,255,255,0.8)',
            'bordercolor': '#bdc3c7',
            'borderwidth': 1,
            'x': 0.02,
            'y': 1.3,
            'xanchor': 'right'
        },

        # Background and margins
        plot_bgcolor='rgba(255,255,255,0)',
        paper_bgcolor='rgba(255,255,255,0)',
        margin=dict(l=80, r=150, t=75, b=85),

        # Dimensions
        width=780,
        height=410,

        # Hover styling
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="Arial"

        )
    )

    # Enhance bar styling
    fig.update_traces(
        marker_line_width=0.5,
        marker_line_color='white',
        hovertemplate='<b>%{fullData.name}</b><br>' +
                      'Year: %{x}<br>' +
                      'Production: %{y:,.0f} KL<br>' +
                      '<extra></extra>'
    )

    # Add subtle shadow effect
    fig.update_traces(
        marker=dict(
            line=dict(width=0.5, color='rgba(255,255,255,0.8)')
        )
    )

    return fig.to_html(full_html=False)