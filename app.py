import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from streamlit_plotly_events import plotly_events

st.set_page_config(page_title="PlayerFrame XY Tagging Tool", layout="wide")
st.title("PlayerFrame XY Tagging Tool (FotMob Version)")

# Initialize session state
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["x", "y", "event"])

# Event type selection
event_type = st.selectbox("Select Event Type", ["Pass", "Shot", "Goal", "Other"])

# Create FotMob-style pitch (105 x 68)
fig = go.Figure()

# Pitch outline
fig.add_shape(type="rect", x0=0, y0=0, x1=105, y1=68, line=dict(color="black", width=3))

# Halfway line
fig.add_shape(type="line", x0=52.5, y0=0, x1=52.5, y1=68, line=dict(color="black", width=2))

# Penalty boxes
fig.add_shape(type="rect", x0=0, y0=(68-44.3)/2, x1=16.5, y1=(68+44.3)/2, line=dict(color="black"))
fig.add_shape(type="rect", x0=105-16.5, y0=(68-44.3)/2, x1=105, y1=(68+44.3)/2, line=dict(color="black"))

# Six-yard boxes
fig.add_shape(type="rect", x0=0, y0=(68-18.32)/2, x1=5.5, y1=(68+18.32)/2, line=dict(color="black"))
fig.add_shape(type="rect", x0=105-5.5, y0=(68-18.32)/2, x1=105, y1=(68+18.32)/2, line=dict(color="black"))

# Center circle
fig.add_shape(type="circle", x0=52.5-9.15, y0=34-9.15, x1=52.5+9.15, y1=34+9.15, line=dict(color="black"))

# Penalty & center spots
fig.add_trace(go.Scatter(
    x=[11, 105-11, 52.5],
    y=[34, 34, 34],
    mode="markers",
    marker=dict(color="black", size=5),
    showlegend=False
))

# Layout settings
fig.update_layout(
    xaxis=dict(range=[0, 105], showgrid=False, zeroline=False, visible=False),
    yaxis=dict(range=[0, 68], showgrid=False, zeroline=False, visible=False),
    height=600,
    width=900,
    plot_bgcolor="#f5f5dc"
)
fig.update_xaxes(scaleanchor="y", scaleratio=1)

# ✅ Capture clicks with debug output
clicked_points = plotly_events(
    fig,
    click_event=True,
    hover_event=False,
    select_event=False,
    key="pitch"
)

# ✅ Debugging: Show raw click data so we can confirm clicks are being captured
st.write("### DEBUG: Raw Click Data")
st.write(clicked_points)

# Store clicked points in session state
if clicked_points:
    x, y = clicked_points[0]["x"], clicked_points[0]["y"]
    st.session_state.data.loc[len(st.session_state.data)] = [x, y, event_type]

# Show tagged events
st.subheader("Tagged Events")
st.write(st.session_state.data)

# Download CSV
if not st.session_state.data.empty:
    csv = st.session_state.data.to_csv(index=False).encode("utf-8")
    st.download_button("Download Tagged Events CSV", csv, "tagged_events.csv", "text/csv")


