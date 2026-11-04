import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Space Debris Planner", layout="wide")
st.title("🌌 Space Debris Collision Avoidance & Trajectory Planner")
st.caption("Developed by Harshit Singh | Independent Aerospace Data Science Project")

# 1. Simulation Controls
st.sidebar.header("📡 Simulation Controls")
safety_perimeter = st.sidebar.slider("Customizable Safety Perimeter (km)", 1.0, 20.0, 5.0, 0.5)
steps = st.sidebar.slider("Simulation Time Steps", 50, 500, 200, 10)

# 2. Generate Mock Trajectories (Satellite vs Debris)
t = np.linspace(0, 10, steps)
sat_x = 300 * np.cos(t)
sat_y = 300 * np.sin(t)
sat_z = 50 * np.sin(t * 0.5)

deb_x = 310 * np.cos(t + 0.2) + 5
deb_y = 290 * np.sin(t + 0.1) - 5
deb_z = 45 * np.cos(t * 0.5)

# 3. Continuous Euclidean Matrix Distance Calculation
distances = np.sqrt(((sat_x - deb_x)2 + (sat_y - deb_y)2 + (sat_z - deb_z)**2))
min_distance = np.min(distances)
min_idx = np.argmin(distances)

# 4. Diagnostic Alert & Corrective Delta-V Burn Automation
st.header("🛠️ Proximity Monitoring & Automation Diagnostics")

if min_distance < safety_perimeter:
    st.error(f"🚨 CRITICAL ALERT: Conjunction Event Detected! Minimum distance: {min_distance:.2f} km (Threshold: {safety_perimeter} km)")
    required_deltav = (safety_perimeter - min_distance) * 0.15
    st.warning(f"⚡ Suggested Corrective Action: Apply Delta-V Impulse Burn of {required_deltav:.3f} m/s at step {min_idx}.")
else:
    st.success(f"🟢 Orbit Clear: Minimum distance tracking safely at {min_distance:.2f} km.")

# 5. Interactive 3D Vector Visualization Engine
st.header("🛰️ 6-DOF Interactive 3D Vector Visualization Engine")

fig = go.Figure()
fig.add_trace(go.Scatter3d(x=sat_x, y=sat_y, z=sat_z, mode='lines', name='Active Satellite', line=dict(color='cyan', width=4)))
fig.add_trace(go.Scatter3d(x=deb_x, y=deb_y, z=deb_z, mode='lines', name='Space Debris', line=dict(color='red', width=3, dash='dash')))
fig.add_trace(go.Scatter3d(x=[sat_x[min_idx]], y=[sat_y[min_idx]], z=[sat_z[min_idx]], mode='markers', name='Closest Approach', marker=dict(size=8, color='yellow')))

fig.update_layout(
    margin=dict(l=0, r=0, b=0, t=0),
    scene=dict(xaxis_title="X (km)", yaxis_title="Y (km)", zaxis_title="Z (km)"),
    template="plotly_dark"
)

st.plotly_chart(fig, use_container_width=True)
