import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
st.set_page_config(
    page_title="Missile Defense Dashboard",
    layout="wide"
)

st.title(
    "Layered Missile Defense Analysis Tool"
)

st.sidebar.header(
    "Model Parameters"
)

raid_size = st.sidebar.slider(
    "Raid Size",
    1,
    1000,
    400
)

aegis_pk = st.sidebar.slider(
    "Aegis SSPK",
    0.50,
    0.99,
    0.82
)

thaad_pk = st.sidebar.slider(
    "THAAD SSPK",
    0.50,
    0.99,
    0.87
)

patriot_pk = st.sidebar.slider(
    "Patriot SSPK",
    0.50,
    0.99,
    0.92
)
aegis_inv = st.sidebar.slider(
    "Aegis Inventory",
    0,
    300,
    80
)

thaad_inv = st.sidebar.slider(
    "THAAD Inventory",
    0,
    300,
    60
)

patriot_inv = st.sidebar.slider(
    "Patriot Inventory",
    0,
    500,
    120
)
# -------------------
# LEAK CURVE
# -------------------

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    [
        "Leak Probability",
        "Cost Exchange",
        "Magazine Exhaustion",
        "Monte Carlo",
        "Sensitivity",
        "Assumptions"
    ]
)
with tab1:

    data = []

    for raid in range(1,1001):

        leakers = max(
            raid - (
                40*aegis_pk +
                30*thaad_pk +
                120*patriot_pk
            ),
            0
        )

        data.append(
            {
                "Raid Size": raid,
                "Expected Leakers": leakers
            }
        )

    df = pd.DataFrame(data)

    fig = px.line(
        df,
        x="Raid Size",
        y="Expected Leakers",
        title="Leak Probability vs Raid Size"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
with tab2:
   with tab2:

    st.subheader("Cost Exchange Analysis")

    st.markdown("### Iranian Missile Inventory")

    col1, col2 = st.columns(2)

    missile_costs = {

        "Shahed-136": 0.03,
        "Fateh-110": 0.50,
        "Zolfaghar": 0.75,
        "Dezful": 1.25,
        "Qiam": 1.00,
        "Emad": 1.00,
        "Ghadr": 3.00,
        "Haj Qasem": 2.00,
        "Kheibar Shekan": 2.50,
        "Fattah-1": 5.00,
        "Sejjil": 5.00,
        "Khorramshahr": 8.00

    }

    missile_counts = {}

    with col1:

        missile_counts["Shahed-136"] = st.number_input(
            "Shahed-136",
            0,
            1000,
            0
        )

        missile_counts["Fateh-110"] = st.number_input(
            "Fateh-110",
            0,
            1000,
            100
        )

        missile_counts["Zolfaghar"] = st.number_input(
            "Zolfaghar",
            0,
            1000,
            100
        )

        missile_counts["Dezful"] = st.number_input(
            "Dezful",
            0,
            1000,
            0
        )

        missile_counts["Qiam"] = st.number_input(
            "Qiam",
            0,
            1000,
            0
        )

        missile_counts["Emad"] = st.number_input(
            "Emad",
            0,
            1000,
            50
        )

    with col2:

        missile_counts["Ghadr"] = st.number_input(
            "Ghadr",
            0,
            1000,
            30
        )

        missile_counts["Haj Qasem"] = st.number_input(
            "Haj Qasem",
            0,
            1000,
            0
        )

        missile_counts["Kheibar Shekan"] = st.number_input(
            "Kheibar Shekan",
            0,
            1000,
            0
        )

        missile_counts["Fattah-1"] = st.number_input(
            "Fattah-1",
            0,
            1000,
            0
        )

        missile_counts["Sejjil"] = st.number_input(
            "Sejjil",
            0,
            1000,
            0
        )

        missile_counts["Khorramshahr"] = st.number_input(
            "Khorramshahr",
            0,
            1000,
            20
        )

    # --------------------------
    # ATTACK COST
    # --------------------------

    attack_cost = 0

    total_missiles = 0

    for missile, count in missile_counts.items():

        attack_cost += (
            count *
            missile_costs[missile]
        )

        total_missiles += count

    # --------------------------
    # DEFENSE COST
    # --------------------------

    defense_cost = (

        aegis_inv * 12.5

        +

        thaad_inv * 15.0

        +

        patriot_inv * 3.73

    )

    # --------------------------
    # COST EXCHANGE
    # --------------------------

    if attack_cost > 0:

        exchange_ratio = (
            defense_cost /
            attack_cost
        )

    else:

        exchange_ratio = 0

    # --------------------------
    # METRICS
    # --------------------------

    m1, m2, m3, m4 = st.columns(4)

    m1.metric(
        "Total Missiles",
        f"{total_missiles:,}"
    )

    m2.metric(
        "Attack Cost",
        f"${attack_cost:,.1f}M"
    )

    m3.metric(
        "Defense Cost",
        f"${defense_cost:,.1f}M"
    )

    m4.metric(
        "Cost Exchange",
        f"{exchange_ratio:.2f}:1"
    )

    # --------------------------
    # BAR CHART
    # --------------------------

    chart_data = []

    for missile, count in missile_counts.items():

        if count > 0:

            chart_data.append({

                "Missile": missile,

                "Cost ($M)": (
                    count *
                    missile_costs[missile]
                )

            })

    if len(chart_data) > 0:

        chart_df = pd.DataFrame(
            chart_data
        )

        fig = px.bar(

            chart_df,

            x="Missile",

            y="Cost ($M)",

            title=
            "Attack Cost Contribution by Missile Type"

        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

with tab3:

    st.subheader("Magazine Exhaustion")

    # ----------------------------------
    # INITIAL INVENTORIES
    # ----------------------------------

    aegis_start = aegis_inv
    thaad_start = thaad_inv
    patriot_start = patriot_inv

    # ----------------------------------
    # SIMULATE INVENTORY DEPLETION
    # ----------------------------------

    aegis_remaining = aegis_inv
    thaad_remaining = thaad_inv
    patriot_remaining = patriot_inv

    for missile in range(1, raid_size + 1):

        if aegis_remaining >= 2:
            aegis_remaining -= 2

        if thaad_remaining >= 2:
            thaad_remaining -= 2

        if patriot_remaining >= 1:
            patriot_remaining -= 1

    # ----------------------------------
    # METRICS
    # ----------------------------------

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Aegis Remaining",
        f"{aegis_remaining}"
    )

    col2.metric(
        "THAAD Remaining",
        f"{thaad_remaining}"
    )

    col3.metric(
        "Patriot Remaining",
        f"{patriot_remaining}"
    )

    st.divider()

    # ----------------------------------
    # EXHAUSTION POINTS
    # ----------------------------------

    aegis_capacity = aegis_start // 2
    thaad_capacity = thaad_start // 2
    patriot_capacity = patriot_start

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Aegis Exhaustion Point",
        f"Missile {aegis_capacity}"
    )

    col2.metric(
        "THAAD Exhaustion Point",
        f"Missile {thaad_capacity}"
    )

    col3.metric(
        "Patriot Exhaustion Point",
        f"Missile {patriot_capacity}"
    )

    st.divider()

    # ----------------------------------
    # USED VS REMAINING
    # ----------------------------------

    inventory_status = pd.DataFrame({

        "System": [
            "Aegis",
            "THAAD",
            "Patriot"
        ],

        "Used": [
            aegis_start - aegis_remaining,
            thaad_start - thaad_remaining,
            patriot_start - patriot_remaining
        ],

        "Remaining": [
            aegis_remaining,
            thaad_remaining,
            patriot_remaining
        ]

    })

    fig = px.bar(

        inventory_status,

        x="System",

        y=[
            "Used",
            "Remaining"
        ],

        barmode="stack",

        title="Magazine Status"

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    
with tab4:

    st.subheader("Monte Carlo Leaker Distribution")

    runs = st.slider(
        "Monte Carlo Runs",
        100,
        10000,
        5000,
        100
    )

    results = []

    aegis_eff = 1 - (1 - aegis_pk)**2
    thaad_eff = 1 - (1 - thaad_pk)**2
    patriot_eff = patriot_pk

    for _ in range(runs):

        missiles = int(
            np.random.normal(
                raid_size,
                raid_size * 0.05
            )
        )

        missiles = max(
            missiles,
            1
        )

        leakers = 0

        aegis_remaining = aegis_inv
        thaad_remaining = thaad_inv
        patriot_remaining = patriot_inv

        for missile in range(missiles):

            killed = False

            if aegis_remaining >= 2:

                aegis_remaining -= 2

                if np.random.random() < aegis_eff:

                    killed = True

            if (not killed) and thaad_remaining >= 2:

                thaad_remaining -= 2

                if np.random.random() < thaad_eff:

                    killed = True

            if (not killed) and patriot_remaining >= 1:

                patriot_remaining -= 1

                if np.random.random() < patriot_eff:

                    killed = True

            if not killed:

                leakers += 1

        results.append(leakers)

    # ---------------------------
    # RESULTS PAGE
    # ---------------------------

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Average Leakers",
        round(np.mean(results), 2)
    )

    col2.metric(
        "Worst Case",
        max(results)
    )

    col3.metric(
        "Best Case",
        min(results)
    )

    st.divider()

    results_df = pd.DataFrame({
        "Leakers": results
    })

    fig = px.histogram(
        results_df,
        x="Leakers",
        nbins=40,
        title="Distribution of Leakers"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    st.subheader("Simulation Statistics")

    st.dataframe(
        pd.DataFrame({
            "Metric": [
                "Mean",
                "Median",
                "Standard Deviation",
                "Minimum",
                "Maximum"
            ],
            "Value": [
                round(np.mean(results),2),
                round(np.median(results),2),
                round(np.std(results),2),
                min(results),
                max(results)
            ]
        }),
        use_container_width=True
    )
with tab5:

    st.subheader(
        "SSPK Sensitivity Analysis"
    )

    sensitivity_data = []

    pk_values = np.arange(
        0.50,
        1.00,
        0.01
    )

    # -------------------
    # AEGIS VARIED
    # -------------------

    for pk in pk_values:

        aegis_eff = (
            1 -
            (1 - pk)**2
        )

        remaining = raid_size

        remaining -= (
            min(
                remaining,
                aegis_inv // 2
            )
            * aegis_eff
        )

        remaining -= (
            min(
                remaining,
                thaad_inv // 2
            )
            * (
                1 -
                (1 - thaad_pk)**2
            )
        )

        remaining -= (
            min(
                remaining,
                patriot_inv
            )
            * patriot_pk
        )

        sensitivity_data.append({

            "System":
            "Aegis",

            "PK":
            pk,

            "Expected Leakers":
            max(
                remaining,
                0
            )

        })

    # -------------------
    # THAAD VARIED
    # -------------------

    for pk in pk_values:

        thaad_eff = (
            1 -
            (1 - pk)**2
        )

        remaining = raid_size

        remaining -= (
            min(
                remaining,
                aegis_inv // 2
            )
            * (
                1 -
                (1 - aegis_pk)**2
            )
        )

        remaining -= (
            min(
                remaining,
                thaad_inv // 2
            )
            * thaad_eff
        )

        remaining -= (
            min(
                remaining,
                patriot_inv
            )
            * patriot_pk
        )

        sensitivity_data.append({

            "System":
            "THAAD",

            "PK":
            pk,

            "Expected Leakers":
            max(
                remaining,
                0
            )

        })

    # -------------------
    # PATRIOT VARIED
    # -------------------

    for pk in pk_values:

        remaining = raid_size

        remaining -= (
            min(
                remaining,
                aegis_inv // 2
            )
            * (
                1 -
                (1 - aegis_pk)**2
            )
        )

        remaining -= (
            min(
                remaining,
                thaad_inv // 2
            )
            * (
                1 -
                (1 - thaad_pk)**2
            )
        )

        remaining -= (
            min(
                remaining,
                patriot_inv
            )
            * pk
        )

        sensitivity_data.append({

            "System":
            "Patriot",

            "PK":
            pk,

            "Expected Leakers":
            max(
                remaining,
                0
            )

        })

    sensitivity_df = pd.DataFrame(
        sensitivity_data
    )

    fig = px.line(

        sensitivity_df,

        x="PK",

        y="Expected Leakers",

        color="System",

        title=
        "Leakage Sensitivity to SSPK"

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
with tab6:

    st.header("Model Assumptions")

    st.write("General Assumptions")

    st.write("- Raid size is user-defined.")
    st.write("- Incoming missiles are treated as independent targets.")
    st.write("- Interceptor probabilities are independent till exhaustion.")
    st.write("- Aegis engages first.")
    st.write("- THAAD engages second.")
    st.write("- Patriot engages last.")
    st.write("- Aegis uses a 2-shot doctrine.")
    st.write("- THAAD uses a 2-shot doctrine.")
    st.write("- Patriot uses a 1-shot doctrine.")
    st.write("- Magazine limits are enforced.")
    st.write("- Raid size variation uses a 5% Gaussian distribution.")
    st.write("- Missile costs are open-source estimates.")
    st.write("- The model is not a physics-based trajectory simulation.")
    st.write("- The model is not an operational fire-control model.")