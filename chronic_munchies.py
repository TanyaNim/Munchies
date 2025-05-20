import streamlit as st
st.set_page_config(layout="centered")  # <-- this must come FIRST

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from PIL import Image
import os
import base64
from io import BytesIO


# Data setup (same as you provided)
data = {
    "Year": [1960, 1965, 1970, 1975, 1980, 1985, 1990, 1995, 2000, 2005, 2010, 2015, 2020],
    "Veg Oils": [185.5, 310, 400, 480, 490, 520, 560, 550, 650, 690, 742, 825, 944],
    "Dairy": [400, 395, 390, 380, 380, 400, 395, 400, 400, 395, 390, 385, 390],
    "Animal Fat": [208, 190, 180, 135, 125, 118, 112, 95, 110, 112, 110, 108, 105],
    "Beef": [170, 172, 178, 190, 180, 165, 150, 130, 126, 120, 118, 118, 120],
    "Pork": [130, 117, 120, 100, 135, 145, 145, 138, 120, 138, 140, 120, 115]
}
df = pd.DataFrame(data)

obesity_years = list(range(1975, 2023))
obesity_percent = [
    11.7, 12.1, 12.4, 12.7, 13.1, 13.5, 13.9, 14.3, 14.8, 15.2, 15.8, 16.3, 16.9, 17.5, 18.1,
    19, 19.8, 20.6, 21.5, 22.4, 23.3, 24.2, 25.2, 26.1, 27.1, 28.1,
    29.1, 30.1, 31.0, 31.9, 32.8, 33.7, 34.5, 35.2, 35.9, 36.5, 37.1, 37.6, 38.1, 38.6, 39.2,
    39.7, 40.2, 40.7, 41.2, 41.7, 42.2, 42.7
]
interp_years = data["Year"]
interp_obesity = np.interp(interp_years, obesity_years, obesity_percent)

colors = {
    "Veg Oils": "#FFBF00",
    "Dairy": "#b2b3ff",
    "Animal Fat": "#d6a2f7",
    "Beef": "#bd6aac",
    "Pork": "#ffb6d3",
    "Obesity": "#333333"
}

# Create figure
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=df["Year"], y=df["Veg Oils"],
    mode='lines+markers',
    name='Veg Oils',
    line=dict(color=colors["Veg Oils"], width=3),
    marker=dict(size=6),
    hoverinfo='x+y'
))
for cat in ["Dairy", "Animal Fat", "Beef", "Pork"]:
    fig.add_trace(go.Bar(
        x=df["Year"],
        y=df[cat],
        name=cat,
        marker_color=colors[cat],
        opacity=0.95
    ))
fig.add_trace(go.Scatter(
    x=interp_years,
    y=interp_obesity,
    name='Obesity (%)',
    mode='lines+markers',
    line=dict(color=colors["Obesity"], width=2, dash='dot'),
    yaxis='y2',
    hoverinfo='x+y'
))
fig.update_layout(
    title=dict(
        text="Vegetable Oils and Obesity",
        x=1,                 # position at far right
        xanchor='right'      # anchor the right edge of the title text at x=1
    ),
    xaxis_title="Year",
    yaxis=dict(title="Calories per Person per Day", side='left'),
    yaxis2=dict(title="Obesity (%)", overlaying='y', side='right'),
    barmode='group',
    plot_bgcolor='white',
    paper_bgcolor='white',
    hovermode='x unified',
     legend=dict(
        title="Category",
        orientation='h',  # horizontal legend
        yanchor='top',
        y=-0.1,          # position below plot, adjust as needed
        x=0              # left align
    ),
    margin=dict(l=40, r=40, t=60, b=80)
)

st.markdown(
    """
    <h1 style='text-align: center; font-size: 35px; font-weight: 600; margin-top: 10px; margin-bottom: 2px;'>
        Cannabis, Munchies & Vegetable Oils
    </h1>
    """,
    unsafe_allow_html=True
)

st.plotly_chart(fig, use_container_width=True)

exp = st.expander("**How Food Consumption Patterns Have Shifted Over Time**", expanded=False)
exp.markdown("""
        <div style="font-size:15px; line-height:1.5;">                                                                                      
        This chart above shows how consumption of vegetable oils, dairy, animal fat, beef, and pork has changed over time (calories per person per day).  
        The dotted line represents obesity rates (%) over the years.  
        It highlights the dramatic rise of seed oils and its potential relation to obesity trends.
        </div>
        <br>     
        <div>
        One of the biggest shifts in modern nutrition is the dramatic rise in vegetable oil consumption.  
        Known as SEED OILS, they’re now the <strong>3rd most consumed food globally</strong> —after rice and wheat—and make up nearly <strong>20% of daily calories</strong> in many diets.
        
    </div>     
    """, unsafe_allow_html=True)

    # -------------------------------------------------------------------------
# === File paths ===

BASE_DIR = os.path.dirname(__file__)
spoon_path = os.path.join(BASE_DIR, "grey_spoon.png")

spoon_image = Image.open(spoon_path)

# pics_dir = os.path.join(os.getcwd(), "pics")
# spoon_path = os.path.join(pics_dir, "grey_spoon.png")
# spoon_image = Image.open(spoon_path)

# === Helper: convert image to base64 ===
def spoon_image_to_base64(img):
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode()
    return img_str

# === Consumption data ===
data = {
    "USA (8 tbs)": {"grams": 105, "tbs": 8},
    "Europe (5.5 tbs)": {"grams": 70, "tbs": 5.5},
    "World (3.7 tbs)": {"grams": 50, "tbs": 3.7},
}

st.markdown("<h3 style='text-align: center;'>Daily Vegetable Oil Consumption</h3>", unsafe_allow_html=True)

# === Row with 3 blocks ===
cols = st.columns(3)

for i, (label, info) in enumerate(data.items()):
    with cols[i]:
        st.markdown(f"###### {label}")
        
        # Create a horizontal container for donut + spoons
        donut_spoon_cols = st.columns([2, 2])  # donut narrower, spoons wider

        with donut_spoon_cols[0]:
            # Donut chart
            fig = go.Figure(data=[go.Pie(
                labels=["used", "remaining"],
                values=[1, 1],
                hole=0.65,
                marker_colors=["#bd6aac", "#ffffff"],
                textinfo="none"
            )])
            fig.update_layout(
                annotations=[dict(
                    text=f"{info['grams']}g",
                    x=0.5, y=0.5,
                    font=dict(size=18, color="black"),
                    showarrow=False
                )],
                showlegend=False,
                margin=dict(t=0, b=0, l=0, r=0),
                height=80, width=80
            )
            st.plotly_chart(fig, use_container_width=False)

        with donut_spoon_cols[1]:
            spoon_count = int(info["tbs"])
            fractional = info["tbs"] - spoon_count

            base64_img = spoon_image_to_base64(spoon_image)

            width, height = spoon_image.size
            right_half_box = (width // 2, 0, width, height)
            half_spoon_image = spoon_image.crop(right_half_box)
            base64_half_img = spoon_image_to_base64(half_spoon_image)

            spoon_html = ''.join([
                f'<img src="data:image/png;base64,{base64_img}" height="55" style="margin-right:0px;" />'
                for _ in range(spoon_count)
            ])

            if fractional >= 0.25:
                spoon_html += (
                    f'<img src="data:image/png;base64,{base64_half_img}" height="55" '
                    f'style="opacity:0.8; margin-right:-6px;" />'
                )

            st.markdown(f'<div style="display:flex; align-items:center;">{spoon_html}</div>', unsafe_allow_html=True)
exp = st.expander("**Daily Vegetable Oil Consumption**", expanded=False)

exp.markdown("""
<div style="font-size:15px; line-height:1.7; font-weight:normal;">

<div>
    These oils are found not only in chips, cookies, and fast food,  
    but also in “healthy” products like <strong>salad dressings</strong>,  
    <strong>protein bars</strong>, <strong>granola</strong>, and  
    <strong>plant-based meats</strong>—even in everyday staples like  
    <strong>mayonnaise</strong>, <strong>sauces</strong>, and <strong>roasted nuts</strong>.
</div>

<br>

<div>
    The rise in vegetable oil use has led to a massive increase in  
    <strong>LINOLEIC ACID</strong> intake — the main omega-6 fat in these oils.  
</div>

<br>
<div>
    Today, people consume more linoleic acid than at any point in human history.  
    As an unstable polyunsaturated fat, it oxidizes easily—during processing, cooking, and even inside the body.  
    Once absorbed, it embeds into cell membranes and can accumulate over time, fueling inflammation and cellular stress.  
    <br><br>
    Excess intake of Linoleic Acid has been linked to <strong>obesity</strong>, <strong>diabetes</strong>, 
    <strong>heart disease</strong>, <strong>neurological disorders</strong>, 
    <strong>migraines</strong>, and inflammatory diseases like <strong>ulcerative colitis</strong>,
    <strong>arthritis </strong>, <strong>asthma</strong>  and <strong>chronic pain</strong>.
</div>
""", unsafe_allow_html=True) 
st.markdown("<div style='margin-top: -60px;'></div>", unsafe_allow_html=True)
    # -----------------------------------------------------------------------------------------
# Chart data
oil_groups = {
    "10–29%": [("Palm oil", 10), ("Avocado oil", 17), ("Olive oil", 20), ("Canola (rapeseed) oil", 21)],
    "30%": [("Peanut oil", 30), ("Rice bran oil", 30)],
    "50–55%": [("Cottonseed oil", 53), ("Soybean oil", 55)],
    "60–71%": [("Corn oil", 60), ("Sunflower oil", 66), ("Safflower oil", 71), ("Grapeseed oil", 71)]
}
group_ranges = {"10–29%": 19, "30%": 2, "50–55%": 5, "60–71%": 11}
labels = list(oil_groups.keys())
values = [group_ranges[label] for label in labels]
colors = ['#ffeb3b', '#fbc02d', '#ba68c8', '#6a1b9a']

# Chart generation
fig = go.Figure(go.Pie(
    labels=labels, values=values, text=labels,
    textfont=dict(color='white'),
    textinfo='text',
    marker=dict(colors=colors, line=dict(color='white', width=1)),
    hole=0.5,
    sort=False, direction='clockwise', rotation=90,
    showlegend=False
))

# Annotations
annotations = []
left_groups = ["50–55%", "30%", "10–29%"]
right_groups = ["60–71%"]
start_y_left = 1.078
start_y_right = 0.9

for i, group in enumerate(left_groups):
    y_base = start_y_left - i * 0.28
    color = colors[labels.index(group)]
    annotations.append(dict(x=-0.01, y=y_base, xref='paper', yref='paper',
                            text=f"<b><span style='color:{color}'>●</span> {group}</b>", showarrow=False,
                            xanchor='left', align='left', font=dict(size=14, color='black')))
    for j, (oil, pct) in enumerate(oil_groups[group]):
        annotations.append(dict(x=0, y=y_base - (j + 1) * 0.045, xref='paper', yref='paper',
                                text=f"{oil}: {pct}%", showarrow=False,
                                xanchor='left', align='left', font=dict(size=13, color='black')))

for i, group in enumerate(right_groups):
    y_base = start_y_right - i * 0.28
    color = colors[labels.index(group)]
    annotations.append(dict(x=0.98, y=y_base, xref='paper', yref='paper',
                            text=f"<b><span style='color:{color}'>●</span> {group}</b>", showarrow=False,
                            xanchor='right', align='right', font=dict(size=14, color='black')))
    for j, (oil, pct) in enumerate(oil_groups[group]):
        annotations.append(dict(x=0.85, y=y_base - (j + 1) * 0.05, xref='paper', yref='paper',
                                text=f"{oil}: {pct}%", showarrow=False,
                                xanchor='left', align='left', font=dict(size=13, color='black')))

fig.update_layout(
    height=400,
    margin=dict(t=30, b=10, l=40, r=80),
    annotations=annotations + [dict(
        text="<b>Linoleic Acid % in Vegetable Oils</b>",
        x=0.5, y=0.45, font=dict(size=16, color='black'),
        showarrow=False)],
    shapes=[dict(
        type='rect', xref='paper', yref='paper',
        x0=0, y0=0, x1=1, y1=0.5,
        fillcolor='white', line=dict(width=0), layer='above'
    )]
)

# Two dropdowns side by side above the chart
col1, col2 = st.columns([1, 1.5])

with col1:
    with st.expander("🛢️ Linoleic Acid in Vegetable Oils"):
        st.markdown("""
        <span style="font-size: 14px;">
        - <strong>10–29%</strong>: Oils like olive and palm have lower linoleic acid and are more stable.<br>
        - <strong>30–55%</strong>: Soybean and peanut oils have moderate linoleic acid.<br>
        - <strong>60–71%</strong>: Sunflower, corn, grapeseed oils are high in omega-6 and may promote inflammation if overconsumed.
        </span>
        """, unsafe_allow_html=True)

with col2:
    with st.expander("🌿 **What about the munchies?! cannabis?!**"):
        st.markdown("""
        <span style="font-size: 14px;">
        Cannabis triggers munchies as THC activates brain receptors to boost appetite. Your body has a similar system powered by <strong>endocannabinoids</strong> made from arachidonic acid, which is derived from linoleic acid—a fat in many seed oils.<br>
        High linoleic acid intake may overstimulate hunger pathways, causing a constant, low-grade munchies effect.<br><br>
        <strong>Results:</strong><br>
        - Increased hunger<br>
        - Fat storage<br>
        - Inflammation<br>
        - Slower metabolism<br>
        - Higher risk of obesity and type 2 diabetes
        </span>
        """, unsafe_allow_html=True)

# Display the chart
st.plotly_chart(fig, use_container_width=True)
