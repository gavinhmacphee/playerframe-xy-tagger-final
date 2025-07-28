import streamlit as st
import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, TapTool
from bokeh.events import Tap

st.set_page_config(page_title="PlayerFrame Bokeh Tagging Tool", layout="wide")
st.title("PlayerFrame XY Tagging Tool (Bokeh Version)")

# Initialize session state
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["x", "y", "event"])

# Event type selection
event_type = st.selectbox("Select Event Type", ["Pass", "Shot", "Goal", "Other"])

# Create pitch figure
p = figure(title="Click to tag location", width=900, height=600,
           x_range=(0, 105), y_range=(0, 68), tools="tap", toolbar_location=None)
p.background_fill_color = "#f5f5dc"
p.outline_line_color = "black"

# Draw pitch outline and lines
p.line([0, 0, 105, 105, 0], [0, 68, 68, 0, 0], line_width=2, color="black")  # Outline
p.line([52.5, 52.5], [0, 68], line_width=1, color="black")  # Halfway line

# Penalty boxes
p.line([0, 16.5, 16.5, 0, 0], [(68-44.3)/2, (68-44.3)/2, (68+44.3)/2, (68+44.3)/2, (68-44.3)/2], color="black")
p.line([105, 105-16.5, 105-16.5, 105, 105], [(68-44.3)/2, (68-44.3)/2, (68+44.3)/2, (68+44.3)/2, (68-44.3)/2], color="black")

# Center circle (approximated)
p.circle([52.5], [34], radius=9.15, fill_color=None, line_color="black")

# Event dots source
dot_source = ColumnDataSource(data=dict(x=[], y=[], label=[]))
p.circle('x', 'y', source=dot_source, size=10, color='red', alpha=0.6)

# Handle click
def on_tap(event):
    x, y = event.x, event.y
    new_row = pd.DataFrame([[x, y, event_type]], columns=["x", "y", "event"])
    st.session_state.data = pd.concat([st.session_state.data, new_row], ignore_index=True)
    dot_source.stream(dict(x=[x], y=[y], label=[event_type]))
    st.experimental_rerun()

p.on_event(Tap, on_tap)

# Show pitch
st.bokeh_chart(p)

# Table of tagged events
st.subheader("Tagged Events")
st.dataframe(st.session_state.data)

# Download
if not st.session_state.data.empty:
    csv = st.session_state.data.to_csv(index=False).encode("utf-8")
    st.download_button("Download Tagged Events CSV", csv, "tagged_events.csv", "text/csv")
