import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="HydroSim | Pelton Turbine Optimization Suite",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for polished styling
st.markdown(
    """
    <style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #475569;
        margin-bottom: 20px;
    }
    .metric-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 15px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 48px;
        white-space: pre-wrap;
        background-color: #F1F5F9;
        border-radius: 6px 6px 0 0;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1E3A8A !important;
        color: white !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Header Section
st.markdown(
    '<div class="main-header">HydroSim: Pelton Impulse Turbine & Nozzle Jet Optimizer</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="sub-header">Advanced Hydrodynamic Performance Modeling, Jet Kinematics, and Parametric Analysis</div>',
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# NAVIGATION TABS
# -----------------------------------------------------------------------------
tab_theory, tab_sim, tab_param, tab_bench = st.tabs([
    "📖 Theory & Fundamentals",
    "⚙️ Interactive Optimizer & Simulator",
    "📊 Parametric Performance Matrix",
    "📝 Laboratory Benchmarking",
])

# Constant definitions
RHO = 1000.0  # Density of water (kg/m3)
G = 9.81  # Gravitational acceleration (m/s2)


# -----------------------------------------------------------------------------
# TAB 1: THEORY & FUNDAMENTALS
# -----------------------------------------------------------------------------
with tab_theory:
    st.header("Fundamental Hydrodynamic Principles")

    col_t1, col_t2 = st.columns([1.2, 1])

    with col_t1:
        st.subheader("1. Impulse-Momentum Principle")
        st.write("""
        The **Pelton turbine** is an impulse hydro-turbine operating under free jet conditions. High-pressure potential energy from a reservoir head ($H$) is converted entirely into kinetic energy through a convergent spear nozzle before entering atmospheric pressure.
        """)
        st.latex(r"V_{jet} = C_v \sqrt{2gH}")
        st.write("""
        Where $C_v$ is the nozzle coefficient of velocity (typically $0.97 - 0.99$), accounting for hydraulic friction losses in the nozzle tip.
        """)

        st.subheader("2. Work Done and Power Transfer")
        st.write("""
        As high-velocity water strikes the double-hemispherical bucket, force is imparted onto the runner through rate of momentum change:
        """)
        st.latex(
            r"F_x = \rho Q (V_{jet} - u)(1 + k \cdot \cos(\theta))"
        )
        st.latex(
            r"P_{mech} = \rho Q u (V_{jet} - u)(1 + k \cdot \cos(\theta)) \cdot \eta_m"
        )
        st.write("""
        * **$u$**: Runner peripheral velocity ($\frac{\pi D N}{60}$)
        * **$k$**: Bucket friction factor ($V_{r2} = k \cdot V_{r1}$, typically $0.85 - 0.95$)
        * **$\theta$**: Bucket deflection angle relative to incoming stream ($\theta = 180^\circ - \beta$)
        * **$\eta_m$**: Mechanical conversion efficiency (accounting for bearing friction and windage)
        """)

    with col_t2:
        st.subheader("3. Speed Ratio Optimization")
        st.write("""
        The dimensionless **Speed Ratio ($\phi$)** governs energy extraction efficiency:
        """)
        st.latex(r"\phi = \frac{u}{V_{jet}}")
        st.info("""
        **Theoretical Optimum:** In an ideal frictionless system ($k = 1.0$), maximum power transfer occurs when the runner speed is exactly half the jet speed ($\phi = 0.50$). 
        
        **Real-World Operating Point:** Due to fluid friction along the bucket surfaces and windage resistance, maximum efficiency drops slightly to **$\phi \approx 0.45 - 0.48$**.
        """)

        st.subheader("4. Key Dimensionless Variables")
        st.markdown("""
        * **Jet Ratio ($m = D/d$):** Ratio of pitch circle diameter to jet diameter (optimal range: $6$ to $12$).
        * **Volumetric Discharge ($Q$):** $Q = A_{nozzle} \cdot V_{jet} = \frac{\pi d^2}{4} C_v \sqrt{2gH}$
        * **Hydraulic Input Power ($P_{hyd}$):** $P_{hyd} = \rho \cdot g \cdot Q \cdot H$
        """)


# -----------------------------------------------------------------------------
# TAB 2: INTERACTIVE OPTIMIZER & SIMULATOR
# -----------------------------------------------------------------------------
with tab_sim:
    st.sidebar.header("🕹️ Turbine Operating Controls")

    head = st.sidebar.slider(
        "Net Operating Head, H (m)",
        min_value=10.0,
        max_value=150.0,
        value=50.0,
        step=1.0,
        help="Net available fluid head at nozzle inlet",
    )
    cv = st.sidebar.slider(
        "Nozzle Velocity Coefficient, Cv",
        min_value=0.85,
        max_value=0.99,
        value=0.97,
        step=0.01,
    )
    d_nozzle_mm = st.sidebar.slider(
        "Nozzle Jet Diameter, d (mm)",
        min_value=5.0,
        max_value=60.0,
        value=25.0,
        step=1.0,
    )
    d_runner = st.sidebar.slider(
        "Runner Pitch Diameter, D (m)",
        min_value=0.15,
        max_value=1.50,
        value=0.45,
        step=0.05,
    )
    bucket_angle = st.sidebar.slider(
        "Bucket Deflection Angle, β (deg)",
        min_value=140,
        max_value=175,
        value=165,
        step=1,
        help="Deflection angle of bucket splitters",
    )
    k_friction = st.sidebar.slider(
        "Bucket Friction Factor, k",
        min_value=0.75,
        max_value=0.98,
        value=0.90,
        step=0.01,
        help="Ratio of relative velocity at outlet to inlet",
    )

    # Conversions
    d_nozzle = d_nozzle_mm / 1000.0  # mm to m
    jet_ratio = d_runner / d_nozzle

    # Core Fluid Calculations
    v_jet = cv * np.sqrt(2 * G * head)
    a_nozzle = (np.pi / 4.0) * (d_nozzle**2)
    q_discharge = a_nozzle * v_jet
    p_hydraulic = (RHO * G * q_discharge * head) / 1000.0  # kW

    # Velocity and Efficiency Vectors
    phi_range = np.linspace(0.01, 0.95, 120)
    u_range = phi_range * v_jet
    rpm_range = (u_range * 60.0) / (np.pi * d_runner)

    beta_rad = np.radians(180.0 - bucket_angle)
    p_mech_range = (
        RHO
        * q_discharge
        * u_range
        * (v_jet - u_range)
        * (1 + k_friction * np.cos(beta_rad))
        * 0.92
        / 1000.0
    )
    eta_range = (p_mech_range / p_hydraulic) * 100.0

    # Best Efficiency Point (BEP)
    bep_idx = np.argmax(eta_range)
    opt_phi = phi_range[bep_idx]
    opt_eta = eta_range[bep_idx]
    opt_pmech = p_mech_range[bep_idx]
    opt_rpm = rpm_range[bep_idx]

    # Metrics Summary Bar
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Jet Velocity (Vj)", f"{v_jet:.2f} m/s")
    m2.metric("Discharge (Q)", f"{q_discharge * 1000:.2f} L/s")
    m3.metric("Hydraulic Input Power", f"{p_hydraulic:.2f} kW")
    m4.metric("Optimal Output Power", f"{opt_pmech:.2f} kW")
    m5.metric("Peak Efficiency (BEP)", f"{opt_eta:.1f} %")

    st.markdown("---")

    col_sim1, col_sim2 = st.columns([1.5, 1])

    with col_sim1:
        st.subheader("Performance Characteristics Curve")

        # Plotly Interactive Performance Curve
        fig_perf = go.Figure()

        # Efficiency Curve
        fig_perf.add_trace(
            go.Scatter(
                x=phi_range,
                y=eta_range,
                mode="lines",
                name="Overall Efficiency (%)",
                line=dict(color="#1E3A8A", width=3.5),
            )
        )

        # BEP Star Marker
        fig_perf.add_trace(
            go.Scatter(
                x=[opt_phi],
                y=[opt_eta],
                mode="markers+text",
                name="Best Efficiency Point (BEP)",
                text=[f"  BEP ({opt_phi:.2f}, {opt_eta:.1f}%)"],
                textposition="top right",
                marker=dict(color="#DC2626", size=14, symbol="star"),
            )
        )

        fig_perf.update_layout(
            title="Overall Efficiency vs. Speed Ratio (ϕ)",
            xaxis_title="Speed Ratio (ϕ = u / Vj)",
            yaxis_title="Overall Efficiency (%)",
            hovermode="x unified",
            template="plotly_white",
            height=450,
        )
        st.plotly_chart(fig_perf, use_container_width=True)

    with col_sim2:
        st.subheader("Optimal Operating Point Summary")

        st.markdown(f"""
        * **Optimal Speed Ratio ($\phi_{{opt}}$):** `{opt_phi:.2f}`
        * **Recommended Runner Speed:** `{opt_rpm:.0f} RPM`
        * **Jet Ratio ($m = D/d$):** `{jet_ratio:.1f}`
        """)

        if jet_ratio < 6:
            st.warning(
                "⚠️ **Jet Ratio Warning:** Jet ratio is under 6. Jet may hit adjacent buckets prematurely."
            )
        elif jet_ratio > 14:
            st.info(
                "ℹ️ **Jet Ratio Notice:** High jet ratio (>14) reduces bucket utilization density."
            )
        else:
            st.success(
                "✅ **Optimal Jet Ratio:** $m$ is within the ideal manufacturing range ($6 - 12$)."
            )

        st.subheader("Power Loss Distribution at BEP")
        loss_nozzle = p_hydraulic * (1 - cv**2)
        loss_bucket = (
            (RHO * q_discharge * (v_jet - opt_phi * v_jet) ** 2 * (1 - k_friction**2))
            / 2
            / 1000.0
        )
        loss_mechanical = opt_pmech * (1 - 0.92) / 0.92
        useful_power = opt_pmech

        fig_pie = go.Figure(
            data=[
                go.Pie(
                    labels=[
                        "Useful Power",
                        "Nozzle Hydraulic Loss",
                        "Bucket Friction Loss",
                        "Mechanical Windage/Friction",
                    ],
                    values=[
                        useful_power,
                        loss_nozzle,
                        loss_bucket,
                        loss_mechanical,
                    ],
                    hole=0.4,
                    marker=dict(
                        colors=["#16A34A", "#DC2626", "#F59E0B", "#64748B"]
                    ),
                )
            ]
        )
        fig_pie.update_layout(
            margin=dict(t=20, b=20, l=10, r=10), height=250
        )
        st.plotly_chart(fig_pie, use_container_width=True)


# -----------------------------------------------------------------------------
# TAB 3: PARAMETRIC PERFORMANCE MATRIX
# -----------------------------------------------------------------------------
with tab_param:
    st.header("Multi-Variable Parametric Analysis")
    st.write(
        "Evaluate how varying operating head and jet nozzle diameter impacts mechanical power output."
    )

    col_p1, col_p2 = st.columns(2)

    with col_p1:
        # Sensitivity to Head
        heads_test = np.linspace(10, 120, 6)
        fig_head = go.Figure()

        for h_val in heads_test:
            v_j = cv * np.sqrt(2 * G * h_val)
            q_val = a_nozzle * v_j
            p_h = (RHO * G * q_val * h_val) / 1000.0
            p_m = (
                RHO
                * q_val
                * (phi_range * v_j)
                * (v_j - phi_range * v_j)
                * (1 + k_friction * np.cos(beta_rad))
                * 0.92
                / 1000.0
            )
            fig_head.add_trace(
                go.Scatter(
                    x=phi_range * v_j * 60 / (np.pi * d_runner),
                    y=p_m,
                    mode="lines",
                    name=f"H = {h_val:.0f} m",
                )
            )

        fig_head.update_layout(
            title="Power Output vs. Runner Speed across Varying Net Heads",
            xaxis_title="Runner Speed (RPM)",
            yaxis_title="Mechanical Shaft Power (kW)",
            template="plotly_white",
            height=400,
        )
        st.plotly_chart(fig_head, use_container_width=True)

    with col_p2:
        # Sensitivity to Nozzle Diameter
        nozzles_test = np.array([15, 20, 25, 30, 35]) / 1000.0
        fig_nozzle = go.Figure()

        for d_v in nozzles_test:
            a_n = (np.pi / 4) * (d_v**2)
            q_v = a_n * v_jet
            p_m = (
                RHO
                * q_v
                * u_range
                * (v_jet - u_range)
                * (1 + k_friction * np.cos(beta_rad))
                * 0.92
                / 1000.0
            )
            eta_v = (
                p_m / ((RHO * G * q_v * head) / 1000.0)
            ) * 100.0
            fig_nozzle.add_trace(
                go.Scatter(
                    x=phi_range,
                    y=p_m,
                    mode="lines",
                    name=f"d = {d_v * 1000:.0f} mm",
                )
            )

        fig_nozzle.update_layout(
            title="Power Output vs. Speed Ratio across Nozzle Diameters",
            xaxis_title="Speed Ratio (ϕ)",
            yaxis_title="Mechanical Shaft Power (kW)",
            template="plotly_white",
            height=400,
        )
        st.plotly_chart(fig_nozzle, use_container_width=True)


# -----------------------------------------------------------------------------
# TAB 4: LABORATORY BENCHMARKING
# -----------------------------------------------------------------------------
with tab_bench:
    st.header("Physical Benchmarking & Validation")
    st.write(
        "Compare experimental data collected from physical laboratory testing against theoretical model predictions."
    )

    st.subheader("Input Experimental Test Runs")

    # Sample dataframe initialization
    sample_data = pd.DataFrame({
        "Run": [1, 2, 3, 4, 5],
        "Head_m": [30.0, 30.0, 30.0, 30.0, 30.0],
        "RPM": [450, 600, 750, 900, 1050],
        "Brake_Torque_Nm": [18.2, 22.4, 24.1, 21.0, 15.3],
        "Flow_Lps": [12.5, 12.5, 12.5, 12.5, 12.5],
    })

    edited_df = st.data_editor(
        sample_data, num_rows="dynamic", use_container_width=True
    )

    # Calculations on edited dataframe
    edited_df["Exp_Power_kW"] = (
        2 * np.pi * edited_df["RPM"] * edited_df["Brake_Torque_Nm"]
    ) / 60000.0
    edited_df["Exp_Hyd_Power_kW"] = (
        RHO * G * (edited_df["Flow_Lps"] / 1000.0) * edited_df["Head_m"]
    ) / 1000.0
    edited_df["Exp_Efficiency_%"] = (
        edited_df["Exp_Power_kW"] / edited_df["Exp_Hyd_Power_kW"]
    ) * 100.0

    st.subheader("Validation Plot")
    fig_val = go.Figure()

    fig_val.add_trace(
        go.Scatter(
            x=edited_df["RPM"],
            y=edited_df["Exp_Efficiency_%"],
            mode="markers+lines",
            name="Experimental Bench Data",
            marker=dict(size=10, color="#DC2626"),
        )
    )

    fig_val.update_layout(
        title="Experimental Efficiency Curve Comparison",
        xaxis_title="Runner Speed (RPM)",
        yaxis_title="Efficiency (%)",
        template="plotly_white",
        height=400,
    )
    st.plotly_chart(fig_val, use_container_width=True)
