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
        background-color: #0B1329;
        color: #F8FAFC;
    }
    
    /* Centered Hero Header Box */
    .hero-container {
        text-align: center;
        padding: 35px 20px 25px 20px;
        background: linear-gradient(180deg, #111C38 0%, #0B1329 100%);
        border: 1px solid #1E293B;
        border-radius: 16px;
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.6);
        margin-bottom: 30px;
    }
    
    .hero-title {
        font-size: 2.8rem;
        font-weight: 900;
        color: #38BDF8;
        margin-top: 15px;
        margin-bottom: 8px;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        text-shadow: 0 0 20px rgba(56, 189, 248, 0.3);
    }
    
    .hero-subtitle {
        font-size: 1.15rem;
        color: #94A3B8;
        font-weight: 500;
        max-width: 850px;
        margin: 0 auto;
    }
    
    /* Custom SVG Logo Banner Graphic */
    .logo-graphic {
        display: inline-block;
        width: 140px;
        height: 140px;
        margin: 0 auto;
    }
    
    /* Feature Highlight Cards */
    .card-box {
        background-color: #111C38;
        border: 1px solid #1E293B;
        border-left: 5px solid #38BDF8;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
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
# HERO HEADER WITH EMBEDDED GRAPHIC LOGO
# -----------------------------------------------------------------------------
st.markdown(
    """
    <div class="hero-container">
        <svg class="logo-graphic" viewBox="0 0 200 200" fill="none" xmlns="http://www.w3.org/2000/svg">
            <!-- Hexagon Shield Outer Frame -->
            <polygon points="100,10 175,50 175,150 100,190 25,150 25,50" stroke="#38BDF8" stroke-width="6" fill="#0B1329"/>
            <polygon points="100,20 165,58 165,142 100,180 35,142 35,58" stroke="#1E293B" stroke-width="3" fill="#111C38"/>
            
            <!-- Pelton Runner Wheel Bucket Details -->
            <circle cx="100" cy="100" r="45" stroke="#38BDF8" stroke-width="5" stroke-dasharray="12 8"/>
            <circle cx="100" cy="100" r="22" stroke="#0284C7" stroke-width="4"/>
            <circle cx="100" cy="100" r="8" fill="#38BDF8"/>
            
            <!-- High-Pressure Water Jet Spray -->
            <path d="M 20 160 C 50 150, 70 120, 95 105" stroke="#0284C7" stroke-width="12" stroke-linecap="round"/>
            <path d="M 25 170 C 55 160, 75 130, 100 115" stroke="#38BDF8" stroke-width="6" stroke-linecap="round"/>
            
            <!-- Electric Power Lightning Bolt -->
            <polygon points="110,40 85,95 105,95 80,150 125,85 102,85" fill="#F59E0B" stroke="#FDE047" stroke-width="1.5"/>
            
            <!-- Performance Characteristic Curve Overlay -->
            <path d="M 50 130 Q 100 60 150 110" stroke="#F59E0B" stroke-width="5" fill="none" stroke-linecap="round"/>
            <polygon points="150,110 142,102 144,115" fill="#F59E0B"/>
        </svg>
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
        "Performance Curves & Analytics",
        "Green Energy & Carbon Impact",
        "Governing Formulas Reference",
    ],
)


# =============================================================================
# SECTION 1: PLATFORM OVERVIEW
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
            <div class="card-title">3. Comprehensive Characteristic Curves</div>
            <div class="card-text">Visualize multi-graph interactions including Brake Power vs. Efficiency, Torque vs. RPM, and Shaft Power across speed ratios under variable heads and nozzle geometries.</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
        <div class="card-box">
            <div class="card-title">4. Green Energy & Carbon Savings Estimation</div>
            <div class="card-text">Translate turbine power output into clean electricity potential. Evaluate how micro-hydro installations replace fossil-fuel power generation and calculate estimated metric tons of CO₂ offset per year.</div>
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
            paper_bgcolor="#111C38",
            plot_bgcolor="#111C38",
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
            paper_bgcolor="#111C38",
            height=250,
            margin=dict(t=30, b=10, l=10, r=10),
        )
        st.plotly_chart(fig_pie, use_container_width=True)


# =============================================================================
# SECTION 4: PERFORMANCE CURVES & ANALYTICS (NEW DETAILED PLOTS)
# =============================================================================
elif nav_choice == "Performance Curves & Analytics":
    st.title("📈 Performance Characteristic Curves & Analytics")
    st.write(
        "Analyze multi-variable relationships governing Pelton turbine operation, including Brake Power vs. Efficiency, Torque vs. Speed, and Head Sensitivity."
    )

    st.sidebar.markdown("### ⚙️ Operating Baseline")
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
    p_hyd_val = RHO * G * q_val * p_head  # Watts

    phi_arr = np.linspace(0.05, 0.90, 80)
    u_arr = phi_arr * v_j
    rpm_arr = (u_arr * 60.0) / (np.pi * p_d_runner)

    p_brake_arr = (
        RHO * q_val * u_arr * (v_j - u_arr) * (1 + 0.90 * 0.96) * 0.92
    )  # Watts
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
                mode="lines+markers",
                name="Efficiency vs. Power",
                line=dict(color="#10B981", width=3.5),
                marker=dict(size=5),
            )
        )
        fig_bp_eff.update_layout(
            title="Brake Power (kW) vs. Overall Efficiency (%)",
            xaxis_title="Brake Power Output (kW)",
            yaxis_title="Overall Efficiency (%)",
            template="plotly_dark",
            paper_bgcolor="#111C38",
            plot_bgcolor="#111C38",
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
                line=dict(color="#F59E0B", width=3.5),
            )
        )
        fig_torque.update_layout(
            title="Brake Torque (N·m) vs. Rotational Speed (RPM)",
            xaxis_title="Runner Rotational Speed (RPM)",
            yaxis_title="Brake Torque (N·m)",
            template="plotly_dark",
            paper_bgcolor="#111C38",
            plot_bgcolor="#111C38",
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
                line=dict(color="#38BDF8", width=3.5),
            )
        )
        fig_bp_rpm.update_layout(
            title="Brake Power (kW) vs. Rotational Speed (RPM)",
            xaxis_title="Runner Rotational Speed (RPM)",
            yaxis_title="Brake Power Output (kW)",
            template="plotly_dark",
            paper_bgcolor="#111C38",
            plot_bgcolor="#111C38",
            height=380,
        )
        st.plotly_chart(fig_bp_rpm, use_container_width=True)

        # 4. Multi-Head Parametric Comparison (Power curves across Heads)
        fig_heads = go.Figure()
        heads_test = [20.0, 35.0, 50.0, 65.0]
        for h_t in heads_test:
            v_t = 0.97 * np.sqrt(2 * G * h_t)
            q_t = (np.pi / 4.0) * (p_d_nozzle**2) * v_t
            p_b_t = RHO * q_t * (phi_arr * v_t) * (v_t - phi_arr * v_t) * 1.78 / 1000.0
            rpm_t = (phi_arr * v_t * 60.0) / (np.pi * p_d_runner)
            fig_heads.add_trace(
                go.Scatter(
                    x=rpm_t, y=p_b_t, mode="lines", name=f"Head H = {h_t:.0f} m"
                )
            )

        fig_heads.update_layout(
            title="Power Curves across Operating Heads (H)",
            xaxis_title="Runner Rotational Speed (RPM)",
            yaxis_title="Brake Power (kW)",
            template="plotly_dark",
            paper_bgcolor="#111C38",
            plot_bgcolor="#111C38",
            height=380,
        )
        st.plotly_chart(fig_heads, use_container_width=True)


# =============================================================================
# SECTION 5: GREEN ENERGY & CARBON IMPACT
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
# SECTION 6: GOVERNING FORMULAS REFERENCE
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
