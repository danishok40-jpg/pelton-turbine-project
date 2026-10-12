import numpy as np
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="Pelton Turbine & Nozzle Optimizer", layout="wide"
)

st.title("Pelton Impulse Turbine Performance & Nozzle Jet Optimizer")
st.markdown("Interactive Fluid Dynamics Web Tool | **Lab Experiments 1 & 10**")

# Sidebar Inputs
st.sidebar.header("Operating Parameters")
head = st.sidebar.slider("Net Head, H (m)", 10.0, 100.0, 50.0)
cv = st.sidebar.slider("Velocity Coefficient, Cv", 0.90, 0.99, 0.97)
d_nozzle = (
    st.sidebar.slider("Nozzle Diameter (mm)", 10.0, 50.0, 25.0) / 1000.0
)  # Convert mm to m
d_runner = st.sidebar.slider("Runner Diameter (m)", 0.20, 1.00, 0.40)

# Fluid Mechanics Calculations
g = 9.81
rho = 1000.0
v_jet = cv * np.sqrt(2 * g * head)  # Theoretical jet velocity (m/s)
a_nozzle = (np.pi / 4) * (d_nozzle**2)
q = a_nozzle * v_jet  # Flow rate (m3/s)
p_hyd = (rho * g * q * head) / 1000.0  # Hydraulic Power (kW)

# Speed ratio range (u / V_jet)
phi_range = np.linspace(0.01, 0.95, 100)
u_range = phi_range * v_jet
p_mech = (rho * q * u_range * (v_jet - u_range) * (1 + 0.90 * 0.96) * 0.92) / 1000.0
eta = (p_mech / p_hyd) * 100.0  # Overall efficiency %

# Metric displays
col1, col2, col3, col4 = st.columns(4)
col1.metric("Jet Velocity (Vj)", f"{v_jet:.2f} m/s")
col2.metric("Discharge (Q)", f"{q * 1000:.2f} L/s")
col3.metric("Hydraulic Power", f"{p_hyd:.2f} kW")
col4.metric("Max Efficiency", f"{np.max(eta):.1f} %")

st.divider()

# Chart
fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=phi_range,
        y=eta,
        mode="lines",
        name="Efficiency (%)",
        line=dict(color="#1f77b4", width=3),
    )
)
fig.update_layout(
    title="Pelton Turbine Efficiency vs Speed Ratio (phi = u / Vj)",
    xaxis_title="Speed Ratio (phi)",
    yaxis_title="Overall Efficiency (%)",
    template="plotly_white",
)
st.plotly_chart(fig, use_container_width=True)
