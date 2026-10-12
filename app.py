import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION & CUSTOM DARK THEME CSS
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="HYDRO-JET | Pelton Turbine Optimization Suite",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    /* Dark Theme Background */
    .stApp {
        background-color: #0F172A;
        color: #F8FAFC;
    }
    
    /* Centered Hero Header Box */
    .hero-container {
        text-align: center;
        padding: 30px 20px;
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        border: 1px solid #334155;
        border-radius: 16px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
        margin-bottom: 30px;
    }
    
    .hero-title {
        font-size: 2.8rem;
        font-weight: 900;
        background: linear-gradient(90deg, #38BDF8 0%, #818CF8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
        letter-spacing: -0.5px;
    }
    
    .hero-subtitle {
        font-size: 1.25rem;
        color: #94A3B8;
        font-weight: 500;
        max-width: 800px;
        margin: 0 auto;
    }
    
    /* Feature Highlight Cards */
    .card-box {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-left: 5px solid #38BDF8;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }
    
    .card-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #38BDF8;
        margin-bottom: 8px;
    }
    
    .card-text {
        font-size: 0.98rem;
        color: #E2E8F0;
        line-height: 1.5;
    }
    
    /* Metric Card Styling Override */
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem !important;
        font-weight: 800 !important;
        color: #38BDF8 !important;
    }
    div[data-testid="stMetricLabel"] {
        font-weight: 700 !important;
        color: #94A3B8 !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Constants
RHO = 1000.0  # Density of water (kg/m3)
G = 9.81  # Acceleration due to gravity (m/s2)

# -----------------------------------------------------------------------------
# CENTERED HERO HEADER & BRANDING
# -----------------------------------------------------------------------------
st.markdown(
    """
    <div class="hero-container">
        <div style="font-size: 3.5rem; margin-bottom: 5px;">⚡🌊</div>
        <div class="hero-title">HYDRO-JET OPTIMIZER</div>
        <div class="hero-subtitle">Interactive Pelton Impulse Turbine Simulator & Renewable Hydro-Power Analytics Suite</div>
    </div>
""",
    unsafe_allow_html=True,
)

# Sidebar Navigation Menu
st.sidebar.markdown("### 🎛️ Navigation Menu")
nav_choice = st.sidebar.radio(
    "Select Interface Section:",
    [
        "Platform Overview",
        "Laboratory Data Calculator",
        "Interactive Turbine Simulator",
        "Green Energy & Carbon Impact",
        "Governing Formulas Reference",
    ],
)


# =============================================================================
# SECTION 1: PLATFORM OVERVIEW (CLEAR & ACCESSIBLE)
# =============================================================================
if nav_choice == "Platform Overview":
    st.markdown("### What This Application Helps You Achieve")
    st.write(
        "HYDRO-JET is a professional fluid mechanics simulation software designed to model, analyze, and optimize Pelton impulse hydro-turbines."
    )

    st.write("")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
        <div class="card-box">
            <div class="card-title">1. Automated Experimental Data Processing</div>
            <div class="card-text">Input raw physical measurements from your testing rig (RPM, spring balance weights, water volume, collection time, inlet pressure). The platform instantly computes net brake forces, volumetric flow rates, brake torque, shaft power, and overall conversion efficiency.</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
        <div class="card-box">
            <div class="card-title">2. Real-Time Nozzle & Speed Optimization</div>
            <div class="card-text">Adjust head pressure, nozzle diameter, runner pitch diameter, and velocity coefficients via live controls. The app automatically plots efficiency curves and calculates your Best Efficiency Point (BEP).</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
        <div class="card-box">
            <div class="card-title">3. Green Energy & Carbon Savings Estimation</div>
            <div class="card-text">Translate turbine power output into clean electricity potential. Evaluate how micro-hydro installations replace fossil-fuel power generation and calculate estimated metric tons of CO₂ offset per year.</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
        <div class="card-box">
            <div class="card-title">4. Parametric Loss Breakdown</div>
            <div class="card-text">Visualize where energy is lost across the system—separating hydraulic nozzle friction, bucket deflection losses, and mechanical windage into interactive pie charts.</div>
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
        "Enter physical test measurements from your experimental bench setup to compute efficiency and power values."
    )

    st.write("")

    col_in1, col_in2, col_in3 = st.columns(3)

    with col_in1:
        r_drum = st.number_input(
            "Brake Drum Radius, r (m)",
            value=0.030,
            step=0.005,
            format="%.3f",
            help="Radius of drum on which brake band operates",
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

    st.sidebar.markdown("### ⚙️ Live Operating Controls")
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
                line=dict(color="#38BDF8", width=4),
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
                marker=dict(color="#F43F5E", size=14, symbol="star"),
            )
        )
        fig.update_layout(
            title="Turbine Efficiency vs. Speed Ratio (ϕ)",
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
            <div class="card-title">Optimal BEP Summary</div>
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
            title="Energy Loss Distribution at BEP",
        )
        fig_pie.update_layout(
            template="plotly_dark",
            paper_bgcolor="#1E293B",
            height=250,
            margin=dict(t=30, b=10, l=10, r=10),
        )
        st.plotly_chart(fig_pie, use_container_width=True)


# =============================================================================
# SECTION 4: GREEN ENERGY & CARBON IMPACT
# =============================================================================
elif nav_choice == "Green Energy & Carbon Impact":
    st.title("🌱 Green Energy & Clean Hydro-Power Impact")

    st.write(
        "High-head Pelton impulse turbines play a central role in micro and mini **run-of-river hydro schemes**, generating zero-emission electricity without large dams."
    )

    st.write("")

    col_g1, col_g2 = st.columns(2)

    with col_g1:
        st.markdown(
            """
        <div class="card-box">
            <div class="card-title">Greenhouse Gas Reduction</div>
            <div class="card-text">Every kilowatt-hour generated by optimizing Pelton turbine efficiency offsets fossil-fuel generation from coal or gas power plants.</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        est_power_kw = st.number_input(
            "Estimated System Power Output (kW)",
            value=25.0,
            step=5.0,
        )
        annual_kwh = est_power_kw * 24 * 365 * 0.70  # 70% capacity factor
        co2_saved_tons = (annual_kwh * 0.82) / 1000.0

        st.info(f"⚡ **Annual Clean Electricity:** `{annual_kwh:,.0f} kWh/year`")
        st.success(
            f"🌿 **Estimated CO₂ Offset:** `{co2_saved_tons:,.1f} Metric Tons CO₂/year`"
        )

    with col_g2:
        st.markdown(
            """
        <div class="card-box">
            <div class="card-title">Grid Stability & Fast Response</div>
            <div class="card-text">Pelton turbines feature instant start-up and precise needle-valve control, making them essential for balancing fluctuating solar and wind power grids.</div>
        </div>
        """,
            unsafe_allow_html=True,
        )


# =============================================================================
# SECTION 5: GOVERNING FORMULAS REFERENCE
# =============================================================================
elif nav_choice == "Governing Formulas Reference":
    st.title("Formulas, Symbols & Definitions Table")
    st.write(
        "Comprehensive reference table for parameters, units, and symbols used in Pelton turbine calculations."
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
