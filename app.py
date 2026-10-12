import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="HydroVirtual Labs | Pelton Turbine Performance Suite",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for Virtual Labs Style Layout
st.markdown(
    """
    <style>
    /* Top Accent Bar */
    .top-bar {
        background-color: #E65100;
        height: 6px;
        width: 100%;
        margin-bottom: 15px;
        border-radius: 2px;
    }
    
    /* Header Container */
    .vlab-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background-color: #FFFFFF;
        padding: 12px 20px;
        border-bottom: 2px solid #E2E8F0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.04);
        margin-bottom: 20px;
    }
    .vlab-logo {
        font-size: 1.8rem;
        font-weight: 800;
        color: #0284C7;
        letter-spacing: -0.5px;
    }
    .vlab-sublogo {
        font-size: 0.85rem;
        color: #E65100;
        font-weight: 700;
    }
    .vlab-breadcrumb {
        font-size: 0.95rem;
        color: #0284C7;
        font-weight: 600;
        margin-bottom: 15px;
    }
    
    /* Section Cards */
    .content-box {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 22px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.03);
        margin-bottom: 20px;
    }
    
    /* Metric Card Styling */
    div[data-testid="stMetricValue"] {
        font-size: 1.7rem !important;
        font-weight: 800 !important;
        color: #1E3A8A !important;
    }
    div[data-testid="stMetricLabel"] {
        font-weight: 700 !important;
        color: #475569 !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Constants
RHO = 1000.0  # Water density (kg/m3)
G = 9.81  # Gravity acceleration (m/s2)

# Top Bar Accent
st.markdown('<div class="top-bar"></div>', unsafe_allow_html=True)

# Top Brand Header
st.markdown(
    """
    <div class="vlab-header">
        <div>
            <span class="vlab-logo">🌊 HydroVirtual Labs</span><br>
            <span class="vlab-sublogo">An Interactive Fluid Machinery & Sustainable Hydro-Power Platform</span>
        </div>
    </div>
""",
    unsafe_allow_html=True,
)

# Breadcrumb Trail
st.markdown(
    '<div class="vlab-breadcrumb">Fluid Machinery Lab &gt; Impulse Turbines &gt; Pelton Turbine Performance Analysis</div>',
    unsafe_allow_html=True,
)

# Sidebar Navigation (Virtual Labs Style)
st.sidebar.markdown("### 📌 Navigation Menu")
nav_choice = st.sidebar.radio(
    "Select Lab Section:",
    [
        "Aim & Overview",
        "Theory & Governing Formulas",
        "Interactive Simulation & BEP",
        "Laboratory Data Calculator",
        "Green Energy & Sustainability",
        "References & Formula Table",
    ],
)


# =============================================================================
# SECTION 1: AIM & OVERVIEW
# =============================================================================
if nav_choice == "Aim & Overview":
    st.title("Performance Characteristics of Pelton Turbine")

    st.markdown('<div class="content-box">', unsafe_allow_html=True)
    st.markdown("### 🎯 Aim of the Experiment")
    st.write(
        "To conduct performance tests on a Pelton impulse turbine under various heads, flow rates, and brake loads, evaluate jet dynamics, and plot operating characteristic curves to determine the Best Efficiency Point (BEP)."
    )
    st.markdown("</div>", unsafe_allow_html=True)

    col_a1, col_a2 = st.columns(2)

    with col_a1:
        st.markdown('<div class="content-box">', unsafe_allow_html=True)
        st.markdown(
            '<h4 style="color: #E65100;">1. Laboratory Test Evaluation</h4>',
            unsafe_allow_html=True,
        )
        st.write(
            "Processes physical data (tachometer RPM, spring balance forces w₁ and w₂, water volume, collection time, inlet pressure) to compute flow rate, brake power, hydraulic power, and overall efficiency."
        )
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="content-box">', unsafe_allow_html=True)
        st.markdown(
            '<h4 style="color: #E65100;">2. Jet Kinematics & Optimization</h4>',
            unsafe_allow_html=True,
        )
        st.write(
            "Simulates speed ratio variations (ϕ = u / Vj) to identify optimal runner rotational speeds and nozzle discharge settings."
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with col_a2:
        st.markdown('<div class="content-box">', unsafe_allow_html=True)
        st.markdown(
            '<h4 style="color: #E65100;">3. Clean Energy Impact Analysis</h4>',
            unsafe_allow_html=True,
        )
        st.write(
            "Translates turbine efficiency metrics into renewable electrical power potential, run-of-river applicability, and metric tons of CO₂ offset."
        )
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="content-box">', unsafe_allow_html=True)
        st.markdown(
            '<h4 style="color: #E65100;">4. Parametric Comparison</h4>',
            unsafe_allow_html=True,
        )
        st.write(
            "Generates real-time interactive plots for loss distribution, power output vs. speed, and efficiency vs. speed ratio."
        )
        st.markdown("</div>", unsafe_allow_html=True)


# =============================================================================
# SECTION 2: THEORY & GOVERNING FORMULAS
# =============================================================================
elif nav_choice == "Theory & Governing Formulas":
    st.title("Hydrodynamic Theory & Impulse Principles")

    col_t1, col_t2 = st.columns([1.2, 1])

    with col_t1:
        st.markdown('<div class="content-box">', unsafe_allow_html=True)
        st.markdown("### 1. Impulse-Momentum Principle")
        st.write(
            "The Pelton turbine utilizes high head potential energy, converting it entirely into kinetic energy in a high-velocity free water jet using a convergent nozzle:"
        )
        st.latex(r"V_{jet} = C_v \sqrt{2gH_i}")
        st.write(
            "Where $C_v$ is the nozzle velocity coefficient (typically $0.95 - 0.98$), $g = 9.81\\text{ m/s}^2$, and $H_i$ is net inlet head."
        )

        st.markdown("### 2. Work Done and Power Transfer")
        st.write(
            "The rate of momentum change of water striking the bucket splitters imparts dynamic force onto the runner:"
        )
        st.latex(
            r"P_{brake} = 2 \pi N T = 2 \pi N (F_b \cdot r)"
        )
        st.latex(
            r"P_{hyd} = \rho \cdot g \cdot H_i \cdot Q_v"
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with col_t2:
        st.markdown('<div class="content-box">', unsafe_allow_html=True)
        st.markdown("### 3. Speed Ratio Optimization")
        st.write(
            "The dimensionless Speed Ratio (ϕ) dictates maximum energy extraction efficiency:"
        )
        st.latex(r"\phi = \frac{u}{V_{jet}} = \frac{\pi D N}{60 \cdot V_{jet}}")
        st.info(
            "Theoretically, maximum power occurs at ϕ = 0.50. In real practice, bucket surface friction and windage reduce the optimum operating point to ϕ ≈ 0.45 - 0.48."
        )
        st.markdown("</div>", unsafe_allow_html=True)


# =============================================================================
# SECTION 3: INTERACTIVE SIMULATION & BEP
# =============================================================================
elif nav_choice == "Interactive Simulation & BEP":
    st.title("Interactive Simulation & BEP Optimizer")

    st.sidebar.markdown("### ⚙️ Simulation Controls")
    s_head = st.sidebar.slider("Net Inlet Head, H (m)", 10.0, 120.0, 45.0, 1.0)
    s_cv = st.sidebar.slider("Velocity Coefficient, Cv", 0.90, 0.99, 0.97, 0.01)
    s_d_nozzle = (
        st.sidebar.slider("Nozzle Diameter, d (mm)", 10.0, 50.0, 24.0, 1.0)
        / 1000.0
    )
    s_d_runner = st.sidebar.slider(
        "Runner Pitch Diameter, D (m)", 0.20, 1.20, 0.45, 0.02
    )

    # Hydrodynamic calculations
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
                line=dict(color="#0284C7", width=4),
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
                marker=dict(color="#E65100", size=14, symbol="star"),
            )
        )
        fig.update_layout(
            title="Turbine Efficiency vs. Speed Ratio (ϕ)",
            xaxis_title="Speed Ratio (ϕ = u / Vj)",
            yaxis_title="Overall Efficiency (%)",
            template="plotly_white",
            height=420,
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_c2:
        st.markdown('<div class="content-box">', unsafe_allow_html=True)
        st.markdown("### Optimal Conditions")
        st.write(f"**Optimum Speed Ratio (ϕ):** `{opt_phi:.2f}`")
        st.write(f"**Recommended Speed:** `{opt_rpm:.0f} RPM`")
        st.write(f"**Shaft Power Output:** `{opt_pmech / 1000.0:.2f} kW`")
        st.write(f"**Jet Ratio (D/d):** `{s_d_runner / s_d_nozzle:.1f}`")
        st.markdown("</div>", unsafe_allow_html=True)

        loss_hyd = (p_hyd_sim - opt_pmech) * 0.4
        loss_mech = (p_hyd_sim - opt_pmech) * 0.6

        fig_pie = px.pie(
            names=["Useful Power", "Hydraulic Loss", "Mechanical Loss"],
            values=[opt_pmech, loss_hyd, loss_mech],
            color_discrete_sequence=["#16A34A", "#E65100", "#F59E0B"],
            title="Energy Distribution at BEP",
        )
        fig_pie.update_layout(height=250, margin=dict(t=30, b=10, l=10, r=10))
        st.plotly_chart(fig_pie, use_container_width=True)


# =============================================================================
# SECTION 4: LABORATORY DATA CALCULATOR
# =============================================================================
elif nav_choice == "Laboratory Data Calculator":
    st.title("📝 Physical Laboratory Data Calculator")
    st.write(
        "Enter physical test measurements from your laboratory bench setup to calculate hydrodynamics and efficiency."
    )

    st.markdown('<div class="content-box">', unsafe_allow_html=True)
    st.markdown("### 1. Experimental Input Parameters")

    col_in1, col_in2, col_in3 = st.columns(3)

    with col_in1:
        r_drum = st.number_input(
            "Radius of Brake Drum, r (m)",
            value=0.030,
            step=0.005,
            format="%.3f",
            help="Radius of drum on which brake band operates",
        )
        rpm_in = st.number_input(
            "Tachometer Reading (RPM)", value=750.0, step=10.0
        )
        p_in_N = st.number_input(
            "Inlet Pressure, Pi (N/m² or Pa)", value=150000.0, step=5000.0
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

    st.markdown("</div>", unsafe_allow_html=True)

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

    st.markdown('<div class="content-box">', unsafe_allow_html=True)
    st.markdown("### 2. Experimental Calculated Results")

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
    st.markdown("</div>", unsafe_allow_html=True)


# =============================================================================
# SECTION 5: GREEN ENERGY & SUSTAINABILITY
# =============================================================================
elif nav_choice == "Green Energy & Sustainability":
    st.title("🌱 Green Energy & Clean Hydro-Power Impact")

    st.markdown('<div class="content-box">', unsafe_allow_html=True)
    st.markdown("### Role of Pelton Turbines in Renewable Energy")
    st.write(
        "Pelton impulse turbines are vital components in micro and mini **run-of-river hydroelectric schemes**. "
        "Unlike large dam projects that flood natural ecosystems, high-head Pelton installations divert a portion of mountain stream water through penstocks to generate clean, zero-emission electricity without creating massive reservoirs."
    )
    st.markdown("</div>", unsafe_allow_html=True)

    col_g1, col_g2 = st.columns(2)

    with col_g1:
        st.markdown('<div class="content-box">', unsafe_allow_html=True)
        st.markdown(
            '<h4 style="color: #16A34A;">1. Zero Greenhouse Gas Emissions</h4>',
            unsafe_allow_html=True,
        )
        st.write(
            "Every kilowatt-hour (kWh) produced by optimizing impulse turbine efficiency replaces fossil-fuel thermal power generation. High efficiency directly lowers carbon intensity."
        )

        # Environmental offsets calculator
        est_power_kw = st.number_input(
            "Turbine Power Output (kW)", value=25.0, step=5.0
        )
        annual_kwh = est_power_kw * 24 * 365 * 0.70  # 70% capacity factor
        co2_saved_tons = (
            annual_kwh * 0.82
        ) / 1000.0  # ~0.82 kg CO2 per kWh grid average

        st.success(
            f"⚡ **Annual Clean Energy Generation:** `{annual_kwh:,.0f} kWh/year`"
        )
        st.success(
            f"🌿 **Estimated CO₂ Offset:** `{co2_saved_tons:,.1f} Metric Tons CO₂/year`"
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with col_g2:
        st.markdown('<div class="content-box">', unsafe_allow_html=True)
        st.markdown(
            '<h4 style="color: #16A34A;">2. Grid Stability & Peak Power Generation</h4>',
            unsafe_allow_html=True,
        )
        st.write(
            "Pelton turbines feature rapid start-up and shut-down capabilities (via nozzle spear valves and jet deflectors). "
            "This makes them ideal for grid balancing and supporting intermittent renewable energy sources like solar and wind power."
        )
        st.markdown("</div>", unsafe_allow_html=True)


# =============================================================================
# SECTION 6: REFERENCES & FORMULA TABLE
# =============================================================================
elif nav_choice == "References & Formula Table":
    st.title("References & Parameter Definitions")
    st.write(
        "Standard reference table for parameters, units, and symbols used in Pelton turbine performance testing."
    )

    formula_data = [
        {
            "Name": "Radius of Brake Drum",
            "Unit": "m",
            "Symbol": "r / R",
            "Type": "Constant/Measured",
            "Definition": "Radius of drum on which brake band operates (measured variable).",
        },
        {
            "Name": "Tachometer Reading",
            "Unit": "RPM",
            "Symbol": "RPM",
            "Type": "Measured",
            "Definition": "Rotor speed measured in revolutions per minute.",
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
            "Definition": "Volume of water collected in a known time period (t). Convert Litres to m³ by dividing by 1000.",
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
