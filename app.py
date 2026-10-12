import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Pelton Turbine Performance & Optimizer",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Constants
RHO = 1000.0  # Water density (kg/m3)
G = 9.81  # Acceleration due to gravity (m/s2)

# -----------------------------------------------------------------------------
# MAIN NAVIGATION TABS (Clean, Fully Visible Labels)
# -----------------------------------------------------------------------------
tab_welcome, tab_lab, tab_sim, tab_theory = st.tabs([
    "Welcome & Overview",
    "Laboratory Data Calculator",
    "Nozzle & Speed Optimizer",
    "Governing Formulas & Theory",
])


# =============================================================================
# TAB 1: WELCOME & LANDING INTERFACE
# =============================================================================
with tab_welcome:
    st.title("Pelton Impulse Turbine & Nozzle Jet Optimizer")
    st.subheader(
        "Interactive Hydrodynamics Platform for Experimental Analysis & Performance Optimization"
    )

    st.divider()

    st.markdown("### What Does This Web Application Help You Do?")
    st.write(
        "This application is a complete fluid dynamics software tool designed to bridge physical bench tests with theoretical hydrodynamic modeling."
    )

    st.write("")

    col_w1, col_w2 = st.columns(2)

    with col_w1:
        st.markdown("#### 1. Process Physical Lab Test Data")
        st.write(
            "Enter experimental readings directly from your lab apparatus (tachometer RPM, spring balance forces w₁ and w₂, water collection time, inlet pressure)."
        )
        st.write(
            "Automatically calculates flow rate (Qv), inlet head (Hi), brake power (Pb), hydraulic power (Ph), and overall efficiency (Et)."
        )

        st.write("")

        st.markdown("#### 2. Interactive Nozzle & Speed Optimization")
        st.write(
            "Adjust operating head, nozzle diameter, runner diameter, and deflection angles using live sliders."
        )
        st.write(
            "Generates real-time efficiency curves, determines the Best Efficiency Point (BEP), and computes optimal speed ratios (ϕ)."
        )

    with col_w2:
        st.markdown("#### 3. Formula Verification & Reference")
        st.write(
            "Review governing impulse-momentum equations, unit conversions, and symbol definitions used in standard fluid mechanics experiments."
        )
        st.write(
            "Provides complete mathematical derivations and step-by-step definition tables."
        )

        st.write("")

        st.markdown("#### 4. Export & Report Data")
        st.write(
            "Generate dynamic color plots, loss distribution pie charts, and comparative performance tables for report submissions."
        )


# =============================================================================
# TAB 2: LABORATORY DATA CALCULATOR (EXACT LAB FORMULAS)
# =============================================================================
with tab_lab:
    st.header("Laboratory Data & Efficiency Calculator")
    st.write(
        "Enter physical measurements from the laboratory bench apparatus to compute parameters based on standard experiment formulas."
    )

    st.subheader("1. Experimental Input Parameters")

    col_in1, col_in2, col_in3 = st.columns(3)

    with col_in1:
        r_drum = st.number_input(
            "Radius of Brake Drum, R (m)",
            value=0.030,
            step=0.001,
            format="%.3f",
            help="Constant: r = 0.030 m",
        )
        rpm_in = st.number_input(
            "Tachometer Reading (RPM)", value=750.0, step=10.0
        )
        p_in_N = st.number_input(
            "Inlet Pressure, Pi (N/m² or Pa)",
            value=150000.0,
            step=5000.0,
            help="Pressure measured by Bourdon gauge",
        )

    with col_in2:
        w1_kg = st.number_input(
            "Spring Balance Reading 1, w1 (kg)", value=1.5, step=0.1
        )
        w2_kg = st.number_input(
            "Spring Balance Reading 2, w2 (kg)", value=5.2, step=0.1
        )

    with col_in3:
        vol_liters = st.number_input(
            "Volume Collected, V (Litres)", value=10.0, step=0.5
        )
        time_sec = st.number_input(
            "Time to Collect, T (seconds)", value=25.0, step=0.5
        )

    # Core Lab Formula Calculations
    N_hz = rpm_in / 60.0  # Rotor speed in Hz
    w1_N = w1_kg * G  # Force 1 in N
    w2_N = w2_kg * G  # Force 2 in N
    f_b = abs(w2_N - w1_N)  # Net Brake Force Fb = |W2 - W1|

    v_m3 = vol_liters / 1000.0  # Volume in m3
    q_v = v_m3 / time_sec if time_sec > 0 else 0.0  # Flow rate Qv (m3/s)

    h_i = p_in_N / (RHO * G)  # Inlet Head Hi = Pi / (rho * g)
    p_h = RHO * G * h_i * q_v  # Hydraulic Power Ph = rho * g * Hi * Qv

    torque = f_b * r_drum  # Torque T = Fb * r
    p_b = 2 * np.pi * N_hz * torque  # Brake Power Pb = 2 * pi * N * T

    e_t = (p_b / p_h * 100.0) if p_h > 0 else 0.0  # Overall Efficiency Et (%)

    st.divider()

    st.subheader("2. Calculated Hydrodynamic Results")

    res1, res2, res3, res4 = st.columns(4)
    res1.metric("Net Brake Force (Fb)", f"{f_b:.2f} N")
    res2.metric("Flow Rate (Qv)", f"{q_v * 1000:.2f} L/s")
    res3.metric("Inlet Head (Hi)", f"{h_i:.2f} mH₂O")
    res4.metric("Brake Torque (T)", f"{torque:.3f} N·m")

    res5, res6, res7, res8 = st.columns(4)
    res5.metric("Rotor Speed (N)", f"{N_hz:.2f} Hz ({rpm_in:.0f} RPM)")
    res6.metric("Hydraulic Power (Ph)", f"{p_h:.1f} W")
    res7.metric("Brake Power (Pb)", f"{p_b:.1f} W")
    res8.metric("Overall Efficiency (Et)", f"{e_t:.2f} %")


# =============================================================================
# TAB 3: INTERACTIVE OPTIMIZER & SIMULATOR
# =============================================================================
with tab_sim:
    st.sidebar.header("Simulation Inputs")

    s_head = st.sidebar.slider("Net Head, H (m)", 10.0, 100.0, 40.0, 1.0)
    s_cv = st.sidebar.slider("Velocity Coeff., Cv", 0.90, 0.99, 0.97, 0.01)
    s_d_nozzle = (
        st.sidebar.slider("Nozzle Diameter, d (mm)", 10.0, 50.0, 22.0, 1.0)
        / 1000.0
    )
    s_d_runner = st.sidebar.slider(
        "Runner Pitch Diameter, D (m)", 0.20, 1.00, 0.40, 0.02
    )

    # Hydrodynamic calculations
    v_jet = s_cv * np.sqrt(2 * G * s_head)
    a_nozzle = (np.pi / 4.0) * (s_d_nozzle**2)
    q_sim = a_nozzle * v_jet
    p_hyd_sim = RHO * G * q_sim * s_head  # Watts

    phi_range = np.linspace(0.01, 0.95, 100)
    u_range = phi_range * v_jet
    rpm_sim_range = (u_range * 60.0) / (np.pi * s_d_runner)

    p_mech_sim = (
        RHO * q_sim * u_range * (v_jet - u_range) * (1 + 0.90 * 0.96) * 0.92
    )
    eta_sim = (p_mech_sim / p_hyd_sim) * 100.0

    bep_idx = np.argmax(eta_sim)
    opt_phi = phi_range[bep_idx]
    opt_eta = eta_sim[bep_idx]
    opt_pmech = p_mech_sim[bep_idx]
    opt_rpm = rpm_sim_range[bep_idx]

    st.header("Nozzle Jet & Speed Optimization")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Jet Velocity (Vj)", f"{v_jet:.2f} m/s")
    m2.metric("Discharge (Q)", f"{q_sim * 1000:.2f} L/s")
    m3.metric("Hydraulic Input Power", f"{p_hyd_sim / 1000.0:.2f} kW")
    m4.metric("Max Efficiency (BEP)", f"{opt_eta:.1f} %")

    st.divider()

    col_chart1, col_chart2 = st.columns([1.6, 1])

    with col_chart1:
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=phi_range,
                y=eta_sim,
                mode="lines",
                name="Efficiency (%)",
                line=dict(color="#0284C7", width=4),
            )
        )
        fig.add_trace(
            go.Scatter(
                x=[opt_phi],
                y=[opt_eta],
                mode="markers+text",
                name="Best Efficiency Point",
                text=[f"BEP ({opt_phi:.2f}, {opt_eta:.1f}%)"],
                textposition="top center",
                marker=dict(color="#DC2626", size=14, symbol="star"),
            )
        )
        fig.update_layout(
            title="Overall Efficiency vs. Speed Ratio (ϕ = u / Vj)",
            xaxis_title="Speed Ratio (ϕ)",
            yaxis_title="Efficiency (%)",
            template="plotly_white",
            height=420,
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_chart2:
        st.subheader("Optimal Conditions")
        st.info(f"""
        * **Optimal Speed Ratio (ϕ):** `{opt_phi:.2f}`
        * **Recommended Speed:** `{opt_rpm:.0f} RPM`
        * **Optimal Power Output:** `{opt_pmech / 1000.0:.2f} kW`
        * **Jet Ratio (D/d):** `{s_d_runner / s_d_nozzle:.1f}`
        """)

        # Power Distribution Pie Chart
        loss_hyd = (p_hyd_sim - opt_pmech) * 0.4
        loss_mech = (p_hyd_sim - opt_pmech) * 0.6

        fig_pie = px.pie(
            names=["Useful Power", "Hydraulic Losses", "Mechanical Losses"],
            values=[opt_pmech, loss_hyd, loss_mech],
            color_discrete_sequence=["#16A34A", "#DC2626", "#F59E0B"],
            title="Power Distribution at BEP",
        )
        fig_pie.update_layout(height=260, margin=dict(t=30, b=10, l=10, r=10))
        st.plotly_chart(fig_pie, use_container_width=True)


# =============================================================================
# TAB 4: GOVERNING FORMULAS & THEORY TABLE
# =============================================================================
with tab_theory:
    st.header("Formulas, Symbols & Definitions Reference")
    st.write(
        "Below is the exact reference table for all parameters used in the laboratory experiment and software calculations."
    )

    formula_data = [
        {
            "Name": "Radius of Brake Drum",
            "Unit": "m",
            "Symbol": "r / R",
            "Type": "Constant",
            "Definition": "Radius of drum on which brake band operates (r = 0.030 m)",
        },
        {
            "Name": "Tachometer Reading",
            "Unit": "RPM",
            "Symbol": "RPM",
            "Type": "Measured",
            "Definition": "Rotor speed measured in RPM.",
        },
        {
            "Name": "Rotor Speed",
            "Unit": "Hz",
            "Symbol": "N",
            "Type": "Calculated",
            "Definition": "Rotational speed converted to Hertz (divide RPM by 60).",
        },
        {
            "Name": "Force 1",
            "Unit": "N",
            "Symbol": "w1",
            "Type": "Measured",
            "Definition": "Force reading from spring balance 1 (Note: F = Reading in kg × 9.81).",
        },
        {
            "Name": "Force 2",
            "Unit": "N",
            "Symbol": "w2",
            "Type": "Measured",
            "Definition": "Force reading from spring balance 2 (Note: F = Reading in kg × 9.81).",
        },
        {
            "Name": "Brake Force",
            "Unit": "N",
            "Symbol": "Fb",
            "Type": "Calculated",
            "Definition": "Difference between Forces 1 and 2 i.e. Fb = |W2 - W1|.",
        },
        {
            "Name": "Volume Collected",
            "Unit": "m³",
            "Symbol": "V",
            "Type": "Measured",
            "Definition": "Volume of water collected in a known time period (t). Convert Litres by dividing by 1000.",
        },
        {
            "Name": "Time to Collect",
            "Unit": "s",
            "Symbol": "T / t",
            "Type": "Measured",
            "Definition": "Time taken to collect a known volume of water (V).",
        },
        {
            "Name": "Volume Flow Rate",
            "Unit": "m³/s",
            "Symbol": "Qv",
            "Type": "Calculated",
            "Definition": "Qv = V / t",
        },
        {
            "Name": "Inlet Pressure",
            "Unit": "N/m²",
            "Symbol": "Pi",
            "Type": "Measured",
            "Definition": "Pressure at inlet measured by Bourdon gauge.",
        },
        {
            "Name": "Inlet Head",
            "Unit": "mH₂O",
            "Symbol": "Hi",
            "Type": "Calculated",
            "Definition": "Hi = Pi / (ρ * g)",
        },
        {
            "Name": "Hydraulic Power",
            "Unit": "Watts",
            "Symbol": "Ph",
            "Type": "Calculated",
            "Definition": "Ph = ρ * g * Hi * Qv (Available power from fluid).",
        },
        {
            "Name": "Torque",
            "Unit": "Nm",
            "Symbol": "T",
            "Type": "Calculated",
            "Definition": "T = Fb * r",
        },
        {
            "Name": "Brake Power",
            "Unit": "Watts",
            "Symbol": "Pb",
            "Type": "Calculated",
            "Definition": "Power absorbed by brake: Pb = 2 * π * N * T",
        },
        {
            "Name": "Overall Turbine Efficiency",
            "Unit": "%",
            "Symbol": "Et",
            "Type": "Calculated",
            "Definition": "Et = (Pb / Ph) × 100% = (2 * π * N * T) / (ρ * g * Hi * Qv) × 100%",
        },
    ]

    df_formula = pd.DataFrame(formula_data)
    st.table(df_formula)
