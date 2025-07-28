import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="PlayerFrame XY Tagging Tool", layout="wide")
st.title("PlayerFrame XY Tagging Tool (Matplotlib Clickable Version)")

# Initialize session state
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["x", "y", "event"])

# Event type selection
event_type = st.selectbox("Select Event Type", ["Pass", "Shot", "Goal", "Other"])

# Create pitch figure
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlim(0, 105)
ax.set_ylim(0, 68)
ax.set_facecolor("#f5f5dc")  # cream color

# Pitch outline
plt.plot([0, 0, 105, 105, 0], [0, 68, 68, 0, 0], color="black", linewidth=2)

# Halfway line
plt.plot([52.5, 52.5], [0, 68], color="black", linewidth=1)

# Penalty boxes
plt.plot([16.5, 16.5, 0, 0, 16.5], [(68-44.3)/2, (68+44.3)/2, (68+44.3)/2, (68-44.3)/2, (68-44.3)/2], color="black")
plt.plot([105-16.5, 105-16.5, 105, 105, 105-16.5],
         [(68-44.3)/2, (68+44.3)/2, (68+44.3)/2, (68-44.3)/2, (68-44.3)/2], color="black")

# Center circle
circle = plt.Circle((52.5, 34), 9.15, color="black", fill=False)
ax.add_patch(circle)

plt.axis('off')

# Display clickable pitch
click = st.pyplot(fig)

# Get click coordinates
if "click_x" not in st.session_state:
    st.session_state.click_x = None
if "click_y" not in st.session_state:
    st.session_state.click_y = None

coords = st.experimental_get_query_params()

# Simulate clicking: Streamlit doesn’t natively pass click events for Matplotlib,
# so we’ll use a manual input for now (but pre-filled for quick logging)
x = st.number_input("X Coordinate (click simulation)", min_value=0.0, max_value=105.0, step=0.1)
y = st.number_input("Y Coordinate (click simulation)", min_value=0.0, max_value=68.0, step=0.1)

if st.button("Log Event"):
    st.session_state.data.loc[len(st.session_state.data)] = [x, y, event_type]
    st.success(f"Logged {event_type} at ({x}, {y})")

# Show tagged events
st.subheader("Tagged Events")
st.write(st.session_state.data)

# Download CSV
if not st.session_state.data.empty:
    csv = st.session_state.data.to_csv(index=False).encode("utf-8")
    st.download_button("Download Tagged Events CSV", csv, "tagged_events.csv", "text/csv")



