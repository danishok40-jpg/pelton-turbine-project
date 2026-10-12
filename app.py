import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION & REALISTIC SOFTWARE THEME
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="HYDRO-JET | Impulse Turbine Analysis Suite",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    /* Dark Engineering Theme */
    .stApp {
        background-color: #0F172A;
        color: #E2E8F0;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Header Bar */
    .app-header {
        display: flex;
        align-items: center;
        gap: 18px;
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 16px 24px;
        margin-bottom: 25px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    .app-header-title {
        font-size: 1.8rem;
        font-weight: 800;
        color: #38BDF8;
        margin: 0;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    .app-header-sub {
        font-size: 0.95rem;
        color: #94A3B8;
        margin: 0;
        font-weight: 500;
    }
    
    /* Content Cards */
    .card-box {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 18px 22px;
        margin-bottom: 20px;
    }
    .card-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #38BDF8;
        margin-bottom: 6px;
    }
    .card-text {
        font-size: 0.95rem;
        color: #CBD5E1;
        line-height: 1.5;
    }
    
    /* Metric Cards Override */
    div[data-testid="stMetricValue"] {
        font-size: 1.6rem !important;
        font-weight: 700 !important;
        color: #38BDF8 !important;
    }
    div[data-testid="stMetricLabel"] {
        font-weight: 600 !important;
        color: #94A3B8 !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Constants
RHO = 1000.0  # Density of water (kg/m3)
G = 9.81  # Gravity acceleration (m/s2)

# -----------------------------------------------------------------------------
# MERGED INTEGRATED HEADER WITH LOGO
# -----------------------------------------------------------------------------
st.markdown(
    """
    <div class="app-header">
        <svg width="52" height="52" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="50" cy="50" r="46" fill="#0F172A" stroke="#38BDF8" stroke-width="4"/>
            <circle cx="50" cy="50" r="28" stroke="#0284C7" stroke-width="4" stroke-dasharray="8 4"/>
            <circle cx="50" cy="50" r="10" fill="#38BDF8"/>
            <path d="M 12 75 C 30 70, 40 55, 50 50" stroke="#38BDF8" stroke-width="6" stroke-linecap="round"/>
            <path d="M 50 15 L 50 25 M 85 50 L 75 50 M 50 85 L 50 75 M 15 50 L 25 50" stroke="#F59E0B" stroke-width="4" stroke-linecap="round"/>
        </svg>
        <div>
            <div class="app-header-title">HYDRO-JET OPTIMIZER</div>
            <div class="app-header-sub">Fluid Dynamics Performance Analysis & Hydro-Turbine Simulation Platform</div>
        </div>
    </div>
""",
    unsafe_allow_html=True,
)

# Sidebar Navigation Menu
st.sidebar.markdown("### 🎛️ System Navigation")
nav_choice = st.sidebar.radio(
    "Select Interface Section:",
    [
        "Platform Overview",
        "Laboratory Data Calculator",
        "Interactive Turbine Simulator",
        "Performance Curves & Analytics",
        "Green Energy & Carbon Impact",
        "Governing Formulas Reference",
    ],
)


# =============================================================================
# SECTION 1: PLATFORM OVERVIEW
# =============================================================================
if nav_choice == "Platform Overview":
    st.markdown("### Application Capabilities & Workflow")
    st.write(
        "HYDRO-JET provides engineering calculations and real-time numerical modeling for Pelton impulse hydro-turbines."
    )

    st.write("")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
        <div class="card-box">
            <div class="card-title">1. Automated Laboratory Data Processing</div>
            <div class="card-text">Processes physical readings (tachometer speed, spring balance loads, water collection volume, and inlet pressure) to compute net brake force, volumetric flow rate, torque, shaft power, and overall conversion efficiency.</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
        <div class="card-box">
            <div class="card-title">2. Hydrodynamic Nozzle & Speed Optimizer</div>
            <div class="card-text">Simulates operating head, nozzle diameter, pitch diameter, and jet coefficients to determine peak efficiency points and optimal speed ratios.</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
        <div class="card-box">
            <div class="card-title">3. Characteristic Performance Curves</div>
            <div class="card-text">Generates interactive plots including Power vs. Efficiency, Torque vs. RPM, and multi-head parametric curves.</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
        <div class="card-box">
            <div class="card-title">4. Renewable Energy Impact Modeling</div>
            <div class="card-text">Calculates estimated annual electrical energy yields and carbon emission offsets for run-of-river micro-hydro installations.</div>
        </div>
        """,
            unsafe_allow_html=True,
        )


# =============================================================================
# SECTION 2: LABORATORY DATA CALCULATOR
# =============================================================================
elif nav_choice == "Laboratory Data Calculator":
    st.title("Physical Test Data Calculator")
    st.write(
        "Input measured experimental parameters to calculate turbine performance metrics."
    )

    st.write("")

    col_in1, col_in2, col_in3 = st.columns(3)

    with col_in1:
        r_drum = st.number_input(
            "Brake Drum Radius, r (m)",
            value=0.030,
            step=0.005,
            format="%.3f",
            help="Measured radius of drum",
        )
        rpm_in = st.number_input(
            "Tachometer Speed (RPM)", value=750.0, step=10.0
        )
        p_in_N = st.number_input(
            "Inlet Pressure, Pi (N/m² or Pa)", value=150000.0, step=5000.0
        )

    with col_in2:
        w1_kg = st.number_input(
            "Spring Balance 1, w1 (kg)", value=1.5, step=0.1
        )
        w2_kg = st.number_input(
            "Spring Balance 2, w2 (kg)", value=5.2, step=0.1
        )

    with col_in3:
        vol_liters = st.number_input(
            "Volume Collected, V (Litres)", value=10.0, step=0.5
        )
        time_sec = st.number_input(
            "Collection Time, T (seconds)", value=25.0, step=0.5
        )

    # Core Calculations
    N_hz = rpm_in / 60.0
    w1_N = w1_kg * G
    w2_N = w2_kg * G
    f_b = abs(w2_N - w1_N)

    v_m3 = vol_liters / 1000.0
    q_v = v_m3 / time_sec if time_sec > 0 else 0.0

    h_i = p_in_N / (RHO * G)
    p_h = RHO * G * h_i * q_v

    torque = f_b * r_drum
    p_b = 2 * np.pi * N_hz * torque

    e_t = (p_b / p_h * 100.0) if p_h > 0 else 0.0

    st.divider()

    st.markdown("### Calculated Experimental Results")

    res1, res2, res3, res4 = st.columns(4)
    res1.metric("Net Brake Force (Fb)", f"{f_b:.2f} N")
    res2.metric("Flow Rate (Qv)", f"{q_v * 1000:.2f} L/s")
    res3.metric("Inlet Head (Hi)", f"{h_i:.2f} mH₂O")
    res4.metric("Brake Torque (T)", f"{torque:.3f} N·m")

    st.write("")

    res5, res6, res7, res8 = st.columns(4)
    res5.metric("Rotor Speed (N)", f"{N_hz:.2f} Hz ({rpm_in:.0f} RPM)")
    res6.metric("Hydraulic Power (Ph)", f"{p_h:.1f} W")
    res7.metric("Brake Power (Pb)", f"{p_b:.1f} W")
    res8.metric("Overall Efficiency (Et)", f"{e_t:.2f} %")


# =============================================================================
# SECTION 3: INTERACTIVE TURBINE SIMULATOR
# =============================================================================
elif nav_choice == "Interactive Turbine Simulator":
    st.title("Interactive Turbine & Jet Simulator")

    st.sidebar.markdown("### ⚙️ Operating Variables")
    s_head = st.sidebar.slider("Net Inlet Head, H (m)", 10.0, 120.0, 45.0, 1.0)
    s_cv = st.sidebar.slider("Velocity Coefficient, Cv", 0.90, 0.99, 0.97, 0.01)
    s_d_nozzle = (
        st.sidebar.slider("Nozzle Diameter, d (mm)", 10.0, 50.0, 24.0, 1.0)
        / 1000.0
    )
    s_d_runner = st.sidebar.slider(
        "Runner Pitch Diameter, D (m)", 0.20, 1.20, 0.45, 0.02
    )

    # Physics Calculations
    v_jet = s_cv * np.sqrt(2 * G * s_head)
    a_nozzle = (np.pi / 4.0) * (s_d_nozzle**2)
    q_sim = a_nozzle * v_jet
    p_hyd_sim = RHO * G * q_sim * s_head

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

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Jet Velocity (Vj)", f"{v_jet:.2f} m/s")
    m2.metric("Discharge (Qv)", f"{q_sim * 1000:.2f} L/s")
    m3.metric("Hydraulic Input Power", f"{p_hyd_sim / 1000.0:.2f} kW")
    m4.metric("Peak Efficiency (BEP)", f"{opt_eta:.1f} %")

    st.divider()

    col_c1, col_c2 = st.columns([1.6, 1])

    with col_c1:
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=phi_range,
                y=eta_sim,
                mode="lines",
                name="Efficiency (%)",
                line=dict(color="#38BDF8", width=3.5),
            )
        )
        fig.add_trace(
            go.Scatter(
                x=[opt_phi],
                y=[opt_eta],
                mode="markers+text",
                name="BEP Point",
                text=[f"  BEP ({opt_phi:.2f}, {opt_eta:.1f}%)"],
                textposition="top right",
                marker=dict(color="#F43F5E", size=12, symbol="star"),
            )
        )
        fig.update_layout(
            title="Overall Efficiency vs. Speed Ratio (ϕ)",
            xaxis_title="Speed Ratio (ϕ = u / Vj)",
            yaxis_title="Overall Efficiency (%)",
            template="plotly_dark",
            paper_bgcolor="#1E293B",
            plot_bgcolor="#1E293B",
            height=420,
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_c2:
        st.markdown(
            f"""
        <div class="card-box">
            <div class="card-title">Optimal Operating Point (BEP)</div>
            <div class="card-text">
                • <b>Optimum Speed Ratio (ϕ):</b> {opt_phi:.2f}<br>
                • <b>Recommended Speed:</b> {opt_rpm:.0f} RPM<br>
                • <b>Shaft Power Output:</b> {opt_pmech / 1000.0:.2f} kW<br>
                • <b>Jet Ratio (D/d):</b> {s_d_runner / s_d_nozzle:.1f}
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        loss_hyd = (p_hyd_sim - opt_pmech) * 0.4
        loss_mech = (p_hyd_sim - opt_pmech) * 0.6

        fig_pie = px.pie(
            names=["Useful Power", "Hydraulic Loss", "Mechanical Loss"],
            values=[opt_pmech, loss_hyd, loss_mech],
            color_discrete_sequence=["#10B981", "#F43F5E", "#F59E0B"],
            title="Energy Distribution at BEP",
        )
        fig_pie.update_layout(
            template="plotly_dark",
            paper_bgcolor="#1E293B",
            height=250,
            margin=dict(t=30, b=10, l=10, r=10),
        )
        st.plotly_chart(fig_pie, use_container_width=True)


# =============================================================================
# SECTION 4: PERFORMANCE CURVES & ANALYTICS
# =============================================================================
elif nav_choice == "Performance Curves & Analytics":
    st.title("Performance Curves & Parametric Analytics")
    st.write(
        "Analyze relationships between brake power, rotational speed, torque, and efficiency under varying conditions."
    )

    st.sidebar.markdown("### ⚙️ Baseline Settings")
    p_head = st.sidebar.slider("Net Head, H (m)", 10.0, 100.0, 45.0, 5.0)
    p_d_nozzle = (
        st.sidebar.slider("Nozzle Diameter, d (mm)", 10.0, 50.0, 24.0, 2.0)
        / 1000.0
    )
    p_d_runner = st.sidebar.slider(
        "Runner Diameter, D (m)", 0.20, 1.00, 0.45, 0.05
    )

    v_j = 0.97 * np.sqrt(2 * G * p_head)
    q_val = (np.pi / 4.0) * (p_d_nozzle**2) * v_j
    p_hyd_val = RHO * G * q_val * p_head

    phi_arr = np.linspace(0.05, 0.90, 80)
    u_arr = phi_arr * v_j
    rpm_arr = (u_arr * 60.0) / (np.pi * p_d_runner)

    p_brake_arr = (
        RHO * q_val * u_arr * (v_j - u_arr) * (1 + 0.90 * 0.96) * 0.92
    )
    eff_arr = (p_brake_arr / p_hyd_val) * 100.0
    torque_arr = p_brake_arr / (2 * np.pi * (rpm_arr / 60.0))

    col_g1, col_g2 = st.columns(2)

    with col_g1:
        # 1. Brake Power vs Efficiency Plot
        fig_bp_eff = go.Figure()
        fig_bp_eff.add_trace(
            go.Scatter(
                x=p_brake_arr / 1000.0,
                y=eff_arr,
                mode="lines",
                name="Efficiency vs. Power",
                line=dict(color="#10B981", width=3),
            )
        )
        fig_bp_eff.update_layout(
            title="Brake Power Output (kW) vs. Efficiency (%)",
            xaxis_title="Brake Power (kW)",
            yaxis_title="Overall Efficiency (%)",
            template="plotly_dark",
            paper_bgcolor="#1E293B",
            plot_bgcolor="#1E293B",
            height=380,
        )
        st.plotly_chart(fig_bp_eff, use_container_width=True)

        # 2. Torque vs Rotational Speed (RPM)
        fig_torque = go.Figure()
        fig_torque.add_trace(
            go.Scatter(
                x=rpm_arr,
                y=torque_arr,
                mode="lines",
                name="Torque (N·m)",
                line=dict(color="#F59E0B", width=3),
            )
        )
        fig_torque.update_layout(
            title="Brake Torque (N·m) vs. Speed (RPM)",
            xaxis_title="Rotational Speed (RPM)",
            yaxis_title="Torque (N·m)",
            template="plotly_dark",
            paper_bgcolor="#1E293B",
            plot_bgcolor="#1E293B",
            height=380,
        )
        st.plotly_chart(fig_torque, use_container_width=True)

    with col_g2:
        # 3. Brake Power Output vs Rotational Speed (RPM)
        fig_bp_rpm = go.Figure()
        fig_bp_rpm.add_trace(
            go.Scatter(
                x=rpm_arr,
                y=p_brake_arr / 1000.0,
                mode="lines",
                name="Brake Power (kW)",
                line=dict(color="#38BDF8", width=3),
            )
        )
        fig_bp_rpm.update_layout(
            title="Brake Power Output (kW) vs. Speed (RPM)",
            xaxis_title="Rotational Speed (RPM)",
            yaxis_title="Brake Power (kW)",
            template="plotly_dark",
            paper_bgcolor="#1E293B",
            plot_bgcolor="#1E293B",
            height=380,
        )
        st.plotly_chart(fig_bp_rpm, use_container_width=True)

        # 4. Multi-Head Parametric Comparison
        fig_heads = go.Figure()
        heads_test = [20.0, 35.0, 50.0, 65.0]
        for h_t in heads_test:
            v_t = 0.97 * np.sqrt(2 * G * h_t)
            q_t = (np.pi / 4.0) * (p_d_nozzle**2) * v_t
            p_b_t = RHO * q_t * (phi_arr * v_t) * (v_t - phi_arr * v_t) * 1.78 / 1000.0
            rpm_t = (phi_arr * v_t * 60.0) / (np.pi * p_d_runner)
            fig_heads.add_trace(
                go.Scatter(
                    x=rpm_t, y=p_b_t, mode="lines", name=f"H = {h_t:.0f} m"
                )
            )

        fig_heads.update_layout(
            title="Brake Power Output across Net Heads (H)",
            xaxis_title="Rotational Speed (RPM)",
            yaxis_title="Brake Power (kW)",
            template="plotly_dark",
            paper_bgcolor="#1E293B",
            plot_bgcolor="#1E293B",
            height=380,
        )
        st.plotly_chart(fig_heads, use_container_width=True)


# =============================================================================
# SECTION 5: GREEN ENERGY & CARBON IMPACT
# =============================================================================
elif nav_choice == "Green Energy & Carbon Impact":
    st.title("Green Energy & Carbon Impact")
    st.write(
        "Evaluation of Pelton impulse turbines in micro-hydro installations for zero-emission clean power generation."
    )

    st.write("")

    col_g1, col_g2 = st.columns(2)

    with col_g1:
        st.markdown(
            """
        <div class="card-box">
            <div class="card-title">Clean Electricity Generation</div>
            <div class="card-text">High-head micro-hydro plants provide predictable renewable baseload power with minimal land footprint.</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        est_power_kw = st.number_input(
            "Estimated System Power Output (kW)",
            value=25.0,
            step=5.0,
        )
        annual_kwh = est_power_kw * 24 * 365 * 0.70
        co2_saved_tons = (annual_kwh * 0.82) / 1000.0

        st.info(f"⚡ **Annual Generation:** `{annual_kwh:,.0f} kWh/year`")
        st.success(
            f"🌿 **Estimated CO₂ Offset:** `{co2_saved_tons:,.1f} Metric Tons CO₂/year`"
        )

    with col_g2:
        st.markdown(
            """
        <div class="card-box">
            <div class="card-title">Run-of-River Hydro Schemes</div>
            <div class="card-text">Pelton turbines allow power extraction from mountain streams without constructing massive storage reservoirs, preserving river ecosystems.</div>
        </div>
        """,
            unsafe_allow_html=True,
        )


# =============================================================================
# SECTION 6: GOVERNING FORMULAS REFERENCE
# =============================================================================
elif nav_choice == "Governing Formulas Reference":
    st.title("Formulas, Symbols & Definitions Reference")
    st.write(
        "Standard definitions and unit reference table for Pelton turbine calculations."
    )

    formula_data = [
        {
            "Name": "Radius of Brake Drum",
            "Unit": "m",
            "Symbol": "r / R",
            "Type": "Variable",
            "Definition": "Radius of drum on which brake band operates.",
        },
        {
            "Name": "Tachometer Reading",
            "Unit": "RPM",
            "Symbol": "RPM",
            "Type": "Measured",
            "Definition": "Rotor rotational speed measured in RPM.",
        },
        {
            "Name": "Rotor Speed",
            "Unit": "Hz",
            "Symbol": "N",
            "Type": "Calculated",
            "Definition": "Rotational speed in Hertz (N = RPM / 60).",
        },
        {
            "Name": "Force 1",
            "Unit": "N",
            "Symbol": "w1",
            "Type": "Measured",
            "Definition": "Reading from spring balance 1 (Force = kg × 9.81).",
        },
        {
            "Name": "Force 2",
            "Unit": "N",
            "Symbol": "w2",
            "Type": "Measured",
            "Definition": "Reading from spring balance 2 (Force = kg × 9.81).",
        },
        {
            "Name": "Brake Force",
            "Unit": "N",
            "Symbol": "Fb",
            "Type": "Calculated",
            "Definition": "Net braking force Fb = |W2 - W1|.",
        },
        {
            "Name": "Volume Collected",
            "Unit": "m³",
            "Symbol": "V",
            "Type": "Measured",
            "Definition": "Volume of water collected (Litres / 1000).",
        },
        {
            "Name": "Collection Time",
            "Unit": "s",
            "Symbol": "T / t",
            "Type": "Measured",
            "Definition": "Time taken to collect volume V.",
        },
        {
            "Name": "Volumetric Flow Rate",
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
            "Definition": "Water pressure at nozzle inlet measured by gauge.",
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
            "Definition": "Ph = ρ * g * Hi * Qv",
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
            "Definition": "Et = (Pb / Ph) × 100%",
        },
    ]

    df_formula = pd.DataFrame(formula_data)
    st.table(df_formula)
