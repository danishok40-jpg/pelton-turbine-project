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
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Styling for Vibrant High-Contrast Light Mode
st.markdown(
    """
    <style>
    /* Main Background & Text Setup */
    .stApp {
        background-color: #F8FAFC;
        color: #0F172A;
    }
    
    /* Headers Styling */
    h1 {
        color: #1E3A8A !important;
        font-weight: 800 !important;
        font-size: 2.3rem !important;
    }
    h2, h3 {
        color: #0369A1 !important;
        font-weight: 700 !important;
    }
    
    /* Welcome Hero Banner */
    .hero-box {
        background: linear-gradient(135deg, #1E3A8A 0%, #0284C7 100%);
        color: #FFFFFF;
        padding: 28px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        margin-bottom: 25px;
    }
    .hero-title {
        font-size: 2.1rem;
        font-weight: 800;
        color: #FFFFFF !important;
        margin-bottom: 8px;
    }
    .hero-sub {
        font-size: 1.15rem;
        color: #E0F2FE;
        font-weight: 500;
    }
    
    /* Content Cards */
    .feature-card {
        background-color: #FFFFFF;
        border-left: 6px solid #0284C7;
        border-radius: 8px;
        padding: 18px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        margin-bottom: 15px;
    }
    
    /* High Contrast Metrics */
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem !important;
        font-weight: 800 !important;
        color: #0F172A !important;
    }
    div[data-testid="stMetricLabel"] {
        font-weight: 700 !important;
        color: #334155 !important;
        font-size: 0.95rem !important;
    }
    
    /* Tab Headers Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        font-weight: 700 !important;
        font-size: 1rem !important;
        padding: 12px 20px !important;
        background-color: #E2E8F0 !important;
        border-radius: 8px 8px 0 0 !important;
        color: #334155 !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #0284C7 !important;
        color: #FFFFFF !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Constants
RHO = 1000.0  # Water density (kg/m3)
G = 9.81  # Acceleration due to gravity (m/s2)
DEFAULT_R = 0.030  # Radius of brake drum (m) from lab formula sheet

# -----------------------------------------------------------------------------
# MAIN NAVIGATION TABS
# -----------------------------------------------------------------------------
tab_welcome, tab_lab, tab_sim, tab_theory = st.tabs([
    "🏠 Welcome & Overview",
    "📝 Laboratory Data Calculator",
    "⚙️ Interactive Nozzle & Speed Optimizer",
    "📖 Governing Formulas & Theory",
])


# =============================================================================
# TAB 1: WELCOME & LANDING INTERFACE
# =============================================================================
with tab_welcome:
    st.markdown(
        """
    <div class="hero-box">
        <div class="hero-title">🌊 Pelton Impulse Turbine & Nozzle Jet Optimizer</div>
        <div class="hero-sub">Interactive Hydrodynamics Platform for Experimental Analysis & Performance Optimization</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("### 🎯 What Does This Web Application Help You Do?")
    st.write(
        "This application is a complete fluid dynamics software tool designed to bridge physical bench tests with theoretical hydrodynamic modeling."
    )

    col_w1, col_w2 = st.columns(2)

    with col_w1:
        st.markdown(
            """
        <div class="feature-card">
            <h4 style="color: #0284C7; margin-top: 0;">1. Process Physical Lab Test Data</h4>
            <p><b>Target Use:</b> Enter experimental readings directly from your lab apparatus (tachometer RPM, spring balance forces <i>w₁</i> & <i>w₂</i>, water collection time, inlet pressure).</p>
            <p><b>Output:</b> Automatically calculates flow rate (<i>Q<sub>v</sub></i>), inlet head (<i>H<sub>i</sub></i>), brake power (<i>P<sub>b</sub></i>), hydraulic power (<i>P<sub>h</sub></i>), and overall efficiency (<i>E<sub>t</sub></i>).</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
        <div class="feature-card">
            <h4 style="color: #0284C7; margin-top: 0;">2. Interactive Nozzle & Speed Optimization</h4>
            <p><b>Target Use:</b> Adjust operating head, nozzle diameter, runner diameter, and deflection angles using live sliders.</p>
            <p><b>Output:</b> Generates real-time efficiency curves, determines the Best Efficiency Point (BEP), and computes optimal speed ratios (<i>ϕ</i>).</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col_w2:
        st.markdown(
            """
        <div class="feature-card">
            <h4 style="color: #0284C7; margin-top: 0;">3. Formula Verification & Reference</h4>
            <p><b>Target Use:</b> Review governing impulse-momentum equations, unit conversions, and symbol definitions used in standard fluid mechanics experiments.</p>
            <p><b>Output:</b> Provides complete mathematical derivations and step-by-step definition tables.</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
        <div class="feature-card">
            <h4 style="color: #0284C7; margin-top: 0;">4. Export & Report Data</h4>
            <p><b>Target Use:</b> Generate dynamic color plots, loss distribution pie charts, and comparative performance tables for report submissions.</p>
        </div>
        """,
            unsafe_allow_html=True,
        )


# =============================================================================
# TAB 2: LABORATORY DATA CALCULATOR (DIRECT FROM FORMULA SHEET)
# =============================================================================
with tab_lab:
    st.header("📝 Laboratory Data & Efficiency Calculator")
    st.markdown(
        "Enter your physical measurements from the laboratory bench apparatus to compute parameters based on standard experiment formulas."
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

    # --- Calculations (According to exact formula sheet) ---
    N_hz = rpm_in / 60.0  # Rotor speed in Hz
    w1_N = w1_kg * G  # Force 1 in N
    w2_N = w2_kg * G  # Force 2 in N
    f_b = abs(w2_N - w1_N)  # Net Brake Force Fb = |W2 - W1|

    v_m3 = vol_liters / 1000.0  # Volume in m3
    q_v = v_m3 / time_sec if time_sec > 0 else 0.0  # Flow rate Qv (m3/s)

    h_i = p_in_N / (RHO * G)  # Inlet head Hi = Pi / (rho * g)
    p_h = RHO * G * h_i * q_v  # Hydraulic Power Ph = rho * g * Hi * Qv

    torque = f_b * r_drum  # Torque T = Fb * r
    p_b = 2 * np.pi * N_hz * torque * 60.0 / 60.0  # Brake power Pb = 2 * pi * N * T
    # Note: Using Hz: Pb = 2 * pi * N_hz * T

    e_t = (p_b / p_h * 100.0) if p_h > 0 else 0.0  # Overall efficiency Et (%)

    st.markdown("---")
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
    st.sidebar.header("⚙️ Simulation Inputs")

    s_head = st.sidebar.slider("Net Head, H (m)", 10.0, 100.0, 40.0, 1.0)
    s_cv = st.sidebar.slider("Velocity Coeff., Cv", 0.90, 0.99, 0.97, 0.01)
    s_d_nozzle = (
        st.sidebar.slider("Nozzle Diameter, d (mm)", 10.0, 50.0, 22.0, 1.0)
        / 1000.0
    )
    s_d_runner = st.sidebar.slider(
        "Runner Pitch Diameter, D (m)", 0.20, 1.00, 0.40, 0.02
    )

    # Physics calculations
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

    st.header("⚙️ Nozzle Jet & Speed Optimization")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Jet Velocity (Vj)", f"{v_jet:.2f} m/s")
    m2.metric("Discharge (Q)", f"{q_sim * 1000:.2f} L/s")
    m3.metric("Hydraulic Input Power", f"{p_hyd_sim / 1000.0:.2f} kW")
    m4.metric("Max Efficiency (BEP)", f"{opt_eta:.1f} %")

    st.markdown("---")

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
        * **Optimal Speed Ratio ($\phi$):** `{opt_phi:.2f}`
        * **Recommended Speed:** `{opt_rpm:.0f} RPM`
        * **Optimal Power Output:** `{opt_pmech / 1000.0:.2f} kW`
        * **Jet Ratio ($D/d$):** `{s_d_runner / s_d_nozzle:.1f}`
        """)

        # Losses Breakdown Chart
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
    st.header("📖 Formulas, Symbols & Definitions Reference")
    st.markdown(
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
