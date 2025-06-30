from flask import Flask, render_template, request
import pandas as pd

from utils import (
    filter_data,
    calculate_total_production,
    calculate_avg_production,
    count_unique_states,
    count_unique_regions,
    generate_top5_states_chart,
    generate_bottom5_states_chart,
    generate_oiltype_donut_chart, generate_regionwise_donut_chart_ocean_gradient,
    generate_production_trend_area_chart,generate_professional_stacked_chart)

app = Flask(__name__)

# Load data once
df = pd.read_csv(r"S:\Aditya\Projects\Oil Production Flask Dashboard\Datasets\Oil_Production_PowerBI_Ready.csv")
df.dropna()

@app.route("/", methods=["GET", "POST"])
def index():
    state = sorted(df['STATE/UT'].unique())
    region = sorted(df['Region'].unique())

    # Default selections
    selected_state = None
    selected_region = None
    filtered_df = df.copy()

    if request.method == "POST":
        selected_state = request.form.get('state')
        selected_region = request.form.get('region')

        # Apply filters
        filtered_df = filter_data(df, selected_state, selected_region)

    # Calculate metrics
    total_production = f"{calculate_total_production(filtered_df)} KL"
    avg_production = f"{calculate_avg_production(filtered_df)} KL"
    state_count = count_unique_states(filtered_df)
    region_count = count_unique_regions(filtered_df)
    barchart = generate_top5_states_chart(df)
    barchart1 = generate_bottom5_states_chart(df)
    donutChart = generate_oiltype_donut_chart(df)
    donutChart1 = generate_regionwise_donut_chart_ocean_gradient(df)
    areaChart = generate_production_trend_area_chart(df)
    stackedColumnChart = generate_professional_stacked_chart(df)

    return render_template("index.html",
                           total_production=total_production,
                           avg_production=avg_production,
                           state_count=state_count,
                           region_count=region_count,
                           selected_state=selected_state,
                           selected_region=selected_region,
                           states=state,
                           regions=region,
                           generate_top5_states_chart=generate_top5_states_chart,
                           barchart=barchart,
                           barchart1 = barchart1,
                           donutChart = donutChart,
                           donutChart1 = donutChart1,
                           areaChart=areaChart,
                           stackedColumnChart=stackedColumnChart)

if __name__ == "__main__":
    app.run(debug=True)
