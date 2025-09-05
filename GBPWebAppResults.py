import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import itertools
import numpy as np

st.set_page_config(layout="wide")

df_1 = pd.read_csv("YouGov Data - May.csv")
df_2 = pd.read_csv("YouGov Data - June.csv")
df_3 = pd.read_csv("YouGov Data - July.csv")
df_4 = pd.read_csv("YouGov Data - August.csv")
df_5 = pd.read_csv("YouGov Data - September.csv")

# Load data
may_df = pd.read_csv("YouGov Data - May.csv")
june_df = pd.read_csv("YouGov Data - June.csv")
july_df = pd.read_csv("YouGov Data - July.csv")
august_df = pd.read_csv("YouGov Data - August.csv")
september_df = pd.read_csv("YouGov Data - September.csv")

may_df["Month"] = "May"
june_df["Month"] = "June"
july_df["Month"] = "July"
august_df["Month"] = "August"
september_df["Month"] = "September"
combined = pd.concat([may_df, june_df, july_df, august_df, september_df])


import streamlit as st

# Your proposal dictionary (numbered per category)
proposal_dictionary = {
    "Economic Mobility and Growth": [
        "Provide community colleges, employers, unions and other programs with incentives to train workers for higher paying jobs, particularly in fast-growing industries",
        "Reduce regulations that restrict construction of new affordable housing and infrastructure",
        "Support rural communities and low-income urban areas with education, training, broadband access, and investment incentives to promote entrepreneurship and job creation",
        "Increase child-care subsidies to low-income families so parents can choose whether to work or stay home with young children",
        "Expand the earned income tax credit and other earning subsidies to low wage workers",
        "Support workers’ rights to form, join and contribute to unions, and their rights not to",
        "Double federal spending on basic research to $200 billion a year, and improve the pipeline from publicly funded research to commercialization"
    ],
    "Energy Policy": [
        "Repeal energy subsidies, regulations and legislation whose costs exceed the benefits",
        "Place a price on carbon emissions of at least $51 per ton, and cut income taxes accordingly on low-income and rural families",
        "To level the playing field with countries that do not put a price on carbon emissions, create a $51 per ton tariff on their products",
        "To reduce methane emissions, support reuse technologies and hold current and former owners of abandoned fossil fuel wells liable for capping those wells",
        "To send energy across the country efficiently, increase Federal agencies’ authority to plan and issue permits for transmission lines and other energy infrastructure across state lines"
    ],
    "Federal Spending & Debt": [
        "Federal Spending & Debt Overall Proposal"
    ],
    "Healthcare": [
        "Expand community support systems for overall health, especially in distressed and rural areas, where private providers lack incentives to provide services.",
        "Coordinate public education for healthier lifestyles and prevention, especially about obesity and nutrition, and increase funding for good nutrition through existing Federal programs",
        "Require each Medicare and Medicaid plan to - measurably - reduce costs and improve their patients’ health outcomes, and stop paying providers for each test and procedure they perform",
        "Expand support for public and private Accountable Care Organizations (e.g. Kaiser Permanente), which provide services to patients based on which yield better health outcomes at lower cost",
        "Expand free meals to low-income schools, including in the summer, to ensure that low-income children have access to nutritious foods",
        "Prevent any business from acquiring a monopoly of health care providers in any region",
        "Expand the use of federal price negotiations to manage the cost of pharmaceuticals and prescription drugs"
    ],
    "K-12 Education": [
        "Revise educational goals and standards to include both academic and life skills, such as teamwork and resilience",
        "Reform teacher training and professional development to boost teachers’ performance",
        "Increase teacher and school accountability for students’ performance",
        "Significantly increase pay for more effective teachers",
        "Develop programs to increase lower income parents’ support for their children’s learning",
        "Expand family choice among public and charter schools",
        "Increase per-student support for under-resourced schools",
        "Provide adequate funding for school facilities and universal broadband",
        "Help state and local education agencies build up their evaluation and research capabilities"
    ],
    "Taxes": [
        "Sharply reduce deductions, exclusions and credits that mostly help high-income families",
        "To reduce evasion and promote exports, tax the value added by each producer in the supply chain, and rebate this value-added tax (VAT) to low-income consumers",
        "Make Social Security more cost-effective by raising benefits for low earners; reducing growth of benefits for high earners; and raising the retirement age, but only for those who can work.",
        "Allow businesses to deduct all expenses, including capital investments, but excluding interest, in the year paid",
        "End taxation distinctions between corporate and non-corporate businesses",
        "Tax the gains on capital assets when they are inherited, ending the ability to avoid such taxes",
        "Lower the size of estates exempt from tax (currently $27 million per couple)"
    ]
}

# Sidebar display
with st.sidebar.expander("Proposal Dictionary", expanded=True):
    for category, proposals in proposal_dictionary.items():
        st.markdown(f"### {category}")
        for idx, title in enumerate(proposals, start=1):
            st.markdown(f"**{idx}.** {title}")

# Group and format

selected_months = st.multiselect(
    "Select month(s) Party Breakdown",
    options=["May", "June", "July", "August", "September"],
    default=["May", "June", "July", "August", "September"]
)

filtered = combined[combined["Month"].isin(selected_months)]
grouped = (
    combined.groupby(["Month", "Grand Bargain or Current Direction?"])
    .size()
    .reset_index(name="Count")
)
total = grouped.groupby("Month")["Count"].transform("sum")
grouped["Percent"] = (grouped["Count"] / total * 100).round(1)
grouped["Label"] = grouped["Percent"].astype(str) + "%"

# Chart
fig = px.bar(
    grouped,
    x="Month",
    y="Percent",
    color="Grand Bargain or Current Direction?",
    text="Label",
    barmode="group",
    title="Would you rather the Grand Bargain OR Current Direction",
    category_orders={"Month": ["May", "June", "July", "August", "September"]}
)

# Fix y-axis to clean 0–100% and improve text
fig.update_traces(
    textposition="outside",
    textfont=dict(size=16, color="black")
)
fig.update_layout(
    yaxis=dict(
        title="Percent",
        range=[0, 100],
        tickformat=".0f"
    )
)

st.plotly_chart(fig)

def party_chart(df, party_label, color_map):
    group = df[df["pid3"] == party_label]
    group = group[group["Month"].isin(party_selected_months)] 
    

    grouped = (
        group.groupby(["Month", "Grand Bargain or Current Direction?"])
        .size()
        .reset_index(name="Count")
    )
    total = grouped.groupby("Month")["Count"].transform("sum")
    grouped["Percent"] = (grouped["Count"] / total * 100).round(1)
    grouped["Label"] = grouped["Percent"].astype(str) + "%"

    fig = px.bar(
        grouped,
        x="Month",
        y="Percent",
        color="Grand Bargain or Current Direction?",
        text="Label",
        barmode="group",
        title=party_label,
        category_orders={"Month": ["May", "June", "July", "August", "September"]},
        color_discrete_map=color_map
    )

    fig.update_traces(
        textposition="outside",
        textfont=dict(size=16, color="black")
    )

    fig.update_layout(
        legend_title_text="",
        yaxis=dict(
            title="Percent",
            range=[0, 100],
            tickformat=".0f"
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="center",
            x=0.5
        )
    )

    return fig

# Calculate totals per party and month, sorted by month order
month_order = ["May", "June", "July", "August", "September"]
totals_per_party = (
    combined[combined["Month"].isin(selected_months)]
    .groupby(["pid3", "Month"])
    .size()
    .reset_index(name="Total Voters")
)
totals_per_party["Month"] = pd.Categorical(totals_per_party["Month"], categories=month_order, ordered=True)
totals_per_party = totals_per_party.sort_values(["pid3", "Month"])

def format_totals(party, months):
    rows = totals_per_party[(totals_per_party["pid3"] == party) & (totals_per_party["Month"].isin(months))]
    return " | ".join([f"{row['Month']}: {row['Total Voters']}" for _, row in rows.iterrows()])

# Create 3 side-by-side columns
col1, col2, col3 = st.columns(3)

with st.expander("Party Affiliation Results (All Breakdowns)", expanded=False):

    party_selected_months = st.multiselect(
        "Select month(s) - Party Affiliation",
        options=["May", "June", "July", "August", "September"],
        default=["May", "June", "July", "August", "September"],
        key="party_months"
    )
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"### Republican\n**Total voters:** {format_totals('Republican', party_selected_months)}")
        st.plotly_chart(
            party_chart(combined, "Republican", {
                "Current Direction": "#8B0000",
                "Grand Bargain": "#FFA07A"
            }), use_container_width=True
        )
    with col2:
        st.markdown(f"### Democrat\n**Total voters:** {format_totals('Democrat', party_selected_months)}")
        st.plotly_chart(
            party_chart(combined, "Democrat", {
                "Current Direction": "#00008B",
                "Grand Bargain": "#87CEFA"
            }), use_container_width=True
        )
    with col3:
        st.markdown(f"### Independent\n**Total voters:** {format_totals('Independent', party_selected_months)}")
        st.plotly_chart(
            party_chart(combined, "Independent", {
                "Current Direction": "#006400",
                "Grand Bargain": "#90EE90"
            }), use_container_width=True
        )

    st.markdown("---")

    # Helper function now takes party_selected_months, not selected_months
    def pid7_facet_chart(party_name, pid7_color_map, legend_loc="right"):
        party_df = combined[(combined["pid3"] == party_name) & (combined["Month"].isin(party_selected_months))].copy()
        party_df["pid7"] = party_df["pid7"].astype(str).str.strip()
        party_df["Grand Bargain or Current Direction?"] = party_df["Grand Bargain or Current Direction?"].astype(str).str.strip()
        pid7_vals = party_df["pid7"].dropna().unique().tolist()

        all_combos = pd.DataFrame(itertools.product(
            party_selected_months, pid7_vals, ["Grand Bargain", "Current Direction"]
        ), columns=["Month", "pid7", "Grand Bargain or Current Direction?"])

        actual = (
            party_df.groupby(["Month", "pid7", "Grand Bargain or Current Direction?"])
            .size()
            .reset_index(name="Count")
        )
        grouped_pid7 = all_combos.merge(
            actual, how="left",
            on=["Month", "pid7", "Grand Bargain or Current Direction?"]
        )
        grouped_pid7["Count"] = grouped_pid7["Count"].fillna(0)

        total_pid7 = grouped_pid7.groupby(["Month", "pid7"])["Count"].transform("sum")
        grouped_pid7["Percent"] = (grouped_pid7["Count"] / total_pid7.replace(0, 1) * 100).round(1)
        grouped_pid7["Label"] = grouped_pid7["Percent"].astype(str) + "%"

        totals_per_month_pid7 = (
            party_df.groupby(["Month", "pid7"])
            .size()
            .reset_index(name="Total Voters")
        )

        fig = px.bar(
            grouped_pid7,
            x="Month",
            y="Percent",
            color="Grand Bargain or Current Direction?",
            text="Label",
            barmode="group",
            facet_col="pid7",
            category_orders={
                "Month": party_selected_months,
                "pid7": pid7_vals
            },
            color_discrete_map=pid7_color_map,
            title=f"{party_name} Support by Strength of Affiliation (PID7)"
        )
        fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
        fig.update_traces(textposition="outside", textfont=dict(size=14, color="black"))
        fig.update_layout(yaxis=dict(title="Percent", range=[0, 120], tickformat=".0f"), margin=dict(t=140))
        for i, pid7_val in enumerate(pid7_vals, start=1):
            rows = totals_per_month_pid7[totals_per_month_pid7["pid7"] == pid7_val]
            for _, row in rows.iterrows():
                fig.add_annotation(
                    x=row["Month"],
                    y=108,
                    text=f"Total: {row['Total Voters']}",
                    showarrow=False,
                    font=dict(size=12, color="black"),
                    xanchor="center",
                    row=1,
                    col=i
                )
        return fig

    st.markdown("#### Republican Support by Strength of Affiliation (PID7)")
    st.plotly_chart(pid7_facet_chart("Republican", {
        "Current Direction": "#8B0000",
        "Grand Bargain": "#FFA07A"
    }), use_container_width=True)

    st.markdown("#### Democrat Support by Strength of Affiliation (PID7)")
    st.plotly_chart(pid7_facet_chart("Democrat", {
        "Current Direction": "#00008B",
        "Grand Bargain": "#87CEFA"
    }), use_container_width=True)

    pid7_order_inds = ["Lean Republican", "Independent", "Lean Democrat"]
    st.markdown("#### Independent Support by Strength of Affiliation (PID7)")
    inds_df = combined[(combined["pid3"] == "Independent") & (combined["Month"].isin(party_selected_months))].copy()
    inds_df["pid7"] = inds_df["pid7"].astype(str).str.strip()
    inds_df["Grand Bargain or Current Direction?"] = inds_df["Grand Bargain or Current Direction?"].astype(str).str.strip()
    all_combos_inds = pd.DataFrame(itertools.product(
        party_selected_months, pid7_order_inds, ["Grand Bargain", "Current Direction"]
    ), columns=["Month", "pid7", "Grand Bargain or Current Direction?"])
    actual_inds = (
        inds_df.groupby(["Month", "pid7", "Grand Bargain or Current Direction?"])
        .size()
        .reset_index(name="Count")
    )
    grouped_pid7_inds = all_combos_inds.merge(
        actual_inds, how="left",
        on=["Month", "pid7", "Grand Bargain or Current Direction?"]
    )
    grouped_pid7_inds["Count"] = grouped_pid7_inds["Count"].fillna(0)
    total_pid7_inds = grouped_pid7_inds.groupby(["Month", "pid7"])["Count"].transform("sum")
    grouped_pid7_inds["Percent"] = (grouped_pid7_inds["Count"] / total_pid7_inds.replace(0, 1) * 100).round(1)
    grouped_pid7_inds["Label"] = grouped_pid7_inds["Percent"].astype(str) + "%"

    totals_per_month_pid7 = (
        inds_df.groupby(["Month", "pid7"])
        .size()
        .reset_index(name="Total Voters")
    )

    fig_pid7_inds = px.bar(
        grouped_pid7_inds,
        x="Month",
        y="Percent",
        color="Grand Bargain or Current Direction?",
        text="Label",
        barmode="group",
        facet_col="pid7",
        category_orders={
            "Month": party_selected_months,
            "pid7": pid7_order_inds
        },
        color_discrete_map={
            "Current Direction": "#006400",  # dark green
            "Grand Bargain": "#90EE90"      # light green
        },
        title="Independent Support by Strength of Affiliation (PID7)"
    )

    fig_pid7_inds.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    fig_pid7_inds.update_traces(textposition="outside", textfont=dict(size=14, color="black"))
    fig_pid7_inds.update_layout(
        yaxis=dict(title="Percent", range=[0, 120], tickformat=".0f"),
        margin=dict(t=140),
        legend=dict(
            orientation="v",
            yanchor="top",
            y=0.9,
            xanchor="left",
            x=1.02
        )
    )
    for i, pid7_val in enumerate(pid7_order_inds, start=1):
        rows = totals_per_month_pid7[totals_per_month_pid7["pid7"] == pid7_val]
        for _, row in rows.iterrows():
            fig_pid7_inds.add_annotation(
                x=row["Month"],
                y=108,
                text=f"Total: {row['Total Voters']}",
                showarrow=False,
                font=dict(size=12, color="black"),
                xanchor="center",
                row=1,
                col=i
            )

    st.plotly_chart(fig_pid7_inds, use_container_width=True)

   
def demographic_chart(df, filter_column, filter_value, color_map, title, months):
    group = df[df[filter_column] == filter_value]
    group = group[group["Month"].isin(months)]

    grouped = (
        group.groupby(["Month", "Grand Bargain or Current Direction?"])
        .size()
        .reset_index(name="Count")
    )
    total = grouped.groupby("Month")["Count"].transform("sum")
    grouped["Percent"] = (grouped["Count"] / total.replace(0, 1) * 100).round(1)
    grouped["Label"] = grouped["Percent"].astype(str) + "%"

    totals = (
        group.groupby("Month")
        .size()
        .reindex(["May", "June", "July", "August", "September"], fill_value=0)
        .reset_index(name="Total Voters")
    )

    fig = px.bar(
        grouped,
        x="Month",
        y="Percent",
        color="Grand Bargain or Current Direction?",
        text="Label",
        barmode="group",
        title=title,
        category_orders={"Month": ["May", "June", "July", "August", "September"]},
        color_discrete_map=color_map
    )

    fig.update_traces(textposition="outside", textfont=dict(size=16, color="black"))
    fig.update_layout(
        legend_title_text="",
        yaxis=dict(title="Percent", range=[0, 120], tickformat=".0f"),
        margin=dict(t=120),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="center",
            x=0.5
        )
    )

    for _, row in totals.iterrows():
        fig.add_annotation(
            x=row["Month"],
            y=108,
            text=f"Total: {row['Total Voters']}",
            showarrow=False,
            font=dict(size=12, color="black"),
            xanchor="center"
        )

    return fig
   
import datetime

# Load data
may_df = pd.read_csv("YouGov Data - May.csv")
june_df = pd.read_csv("YouGov Data - June.csv")
july_df = pd.read_csv("YouGov Data - July.csv")
august_df = pd.read_csv("YouGov Data - August.csv")
september_df = pd.read_csv("YouGov Data - September.csv")

may_df["Month"] = "May"
june_df["Month"] = "June"
july_df["Month"] = "July"
august_df["Month"] = "August"
september_df["Month"] = "September"

combined = pd.concat([may_df, june_df, july_df, august_df, september_df])


# ✅ Add age and age_group columns
current_year = datetime.datetime.now().year
combined["birthyr"] = pd.to_numeric(combined["birthyr"], errors="coerce")
combined["age"] = current_year - combined["birthyr"]

def get_age_group(age):
    if age < 30:
        return "18–29"
    elif age < 45:
        return "30–44"
    elif age < 60:
        return "45–59"
    elif age < 75:
        return "60–74"
    else:
        return "75+"

combined["age_group"] = combined["age"].apply(get_age_group)



with st.expander("Demographic Breakdown (Single Selection)"):
    # Mapping of nice display labels
    column_labels = {
        "gender": "Gender",
        "age_group": "Age Group",
        "educ": "Education",
        "race": "Race",
        "employ": "Employment",
        "faminc_new": "Earnings",
        "ideo5": "Ideology"
    }

    # Month toggle for this section ONLY
    demo_selected_months = st.multiselect(
        "Select month(s) - Demographic Breakdown",
        options=["May", "June", "July", "August", "September"],
        default=["May", "June", "July", "August", "September"],
        key="demo_months"
    )

    # Show dropdown with nice labels
    selected_label = st.selectbox(
        "Choose a demographic:",
        options=list(column_labels.values())
    )

    # Map back to real column name
    demo_column = [key for key, value in column_labels.items() if value == selected_label][0]

    # Define sorted order for certain columns
    if demo_column == "ideo5":
        order = [
            "Very conservative",
            "Conservative",
            "Moderate",
            "Liberal",
            "Very liberal"
        ]
    else:
        order = sorted([x for x in combined[demo_column].dropna().unique()])

    # Dropdown for demographic value
    demo_value = st.selectbox(
        f"Choose a value for {selected_label}:",
        options=order
    )

    # FULLY UPDATED FUNCTION CALL
    fig_demo = demographic_chart(
        combined,
        filter_column=demo_column,
        filter_value=demo_value,
        color_map={"Current Direction": "#8B0000", "Grand Bargain": "#FFA07A"},
        title=f"{demo_value} ({selected_label})",
        months=demo_selected_months
    )

    st.plotly_chart(fig_demo, use_container_width=True)

with st.expander("Advanced: Combine Multiple Demographics"):
    # Month toggle for advanced filter
    multi_selected_months = st.multiselect(
        "Select month(s) for Advanced Demographics",
        options=["May", "June", "July", "August", "September"],
        default=["May", "June", "July", "August", "September"],
        key="multi_months"
    )

    # Multi-filter UI
    party = st.selectbox("Party", options=["All", "Republican", "Democrat", "Independent"], key="multi_party")
    gender = st.selectbox("Gender", options=["All", "Male", "Female"], key="multi_gender")
    age_group = st.selectbox("Age Group", options=["All", "18–29", "30–44", "45–59", "60–74", "75+"], key="multi_age")
    employ = st.selectbox("Employment", options=["All"] + sorted(combined["employ"].dropna().unique()), key="multi_employ")
    income = st.selectbox("Earnings", options=["All"] + sorted(combined["faminc_new"].dropna().unique()), key="multi_income")
    ideology = st.selectbox("Ideology", options=["All"] + sorted(combined["ideo5"].dropna().unique()), key="multi_ideo")
    state = st.selectbox("State", options=["All"] + sorted(combined["inputstate"].dropna().unique()), key="multi_state")

    # Filter dataset dynamically
    filtered_df = combined.copy()
    if party != "All":
        filtered_df = filtered_df[filtered_df["pid3"] == party]
    if gender != "All":
        filtered_df = filtered_df[filtered_df["gender"] == gender]
    if age_group != "All":
        filtered_df = filtered_df[filtered_df["age_group"] == age_group]
    if employ != "All":
        filtered_df = filtered_df[filtered_df["employ"] == employ]
    if income != "All":
        filtered_df = filtered_df[filtered_df["faminc_new"] == income]
    if ideology != "All":
        filtered_df = filtered_df[filtered_df["ideo5"] == ideology]
    if state != "All":
        filtered_df = filtered_df[filtered_df["inputstate"] == state]

    # Build dynamic title
    title_parts = []
    for label, value in [
        ("Party", party), ("Gender", gender), ("Age", age_group),
        ("Employment", employ), ("Income", income),
        ("Ideology", ideology), ("State", state)
    ]:
        if value != "All":
            title_parts.append(f"{value}")
    title_text = " | ".join(title_parts) if title_parts else "All Respondents"

    # Group by Month and answer, filtered by the selected months
    grouped = (
        filtered_df[filtered_df["Month"].isin(multi_selected_months)]
        .groupby(["Month", "Grand Bargain or Current Direction?"])
        .size()
        .reset_index(name="Count")
    )

    total = grouped.groupby("Month")["Count"].transform("sum")
    grouped["Percent"] = (grouped["Count"] / total.replace(0, 1) * 100).round(1)
    grouped["Label"] = grouped["Percent"].astype(str) + "%"

    # Totals per month
    totals = (
        filtered_df[filtered_df["Month"].isin(multi_selected_months)]
        .groupby("Month")
        .size()
        .reindex(["May", "June", "July", "August", "September"], fill_value=0)
        .reset_index(name="Total Voters")
    )

    # Build chart
    fig_multi = px.bar(
        grouped,
        x="Month",
        y="Percent",
        color="Grand Bargain or Current Direction?",
        text="Label",
        barmode="group",
        title=title_text,
        category_orders={"Month": ["May", "June", "July", "August", "September"]},
        color_discrete_map={"Current Direction": "#8B0000", "Grand Bargain": "#FFA07A"}
    )

    fig_multi.update_traces(textposition="outside", textfont=dict(size=16, color="black"))
    fig_multi.update_layout(
        legend_title_text="",
        yaxis=dict(title="Percent", range=[0, 120], tickformat=".0f"),
        margin=dict(t=120),
        legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5)
    )

    # Add total voter annotations
    for _, row in totals.iterrows():
        fig_multi.add_annotation(
            x=row["Month"],
            y=108,
            text=f"Total: {row['Total Voters']}",
            showarrow=False,
            font=dict(size=12, color="black"),
            xanchor="center"
        )

    st.plotly_chart(fig_multi, use_container_width=True)

with st.expander("Policy Area Support/Oppose Breakdown by Party (All Months, 3×2 Grid)", expanded=False):
    vote_map = {
        "Hate It": 1,
        "Dislike It": 2,
        "Not Sure": 3,
        "Good Idea": 4,
        "Critical to Me & Others": 5
    }

    issues = {
        'Economic Mobility & Growth': [col for col in combined.columns if col.startswith('Economic')],
        'K-12 Education': [col for col in combined.columns if col.startswith('Education')],
        'Healthcare': [col for col in combined.columns if col.startswith('Healthcare')],
        'Energy Policy': [col for col in combined.columns if col.startswith('Energy')],
        'Taxes': [col for col in combined.columns if col.startswith('Taxes')],
        'Federal Spending & Debt': [col for col in combined.columns if col.startswith('Fed')]
    }

    month_pairs = [("May", "June"), ("July", "August"),("September", )]
    st.markdown("#### Policy Area Support Breakdown by Party")
    for row_pair in month_pairs:
        cols = st.columns(len(row_pair))  # 2 for pairs, 1 for single
        for i, month in enumerate(row_pair):
            month_df = combined[combined["Month"] == month]

            summary_data = []
            for issue, cols_ in issues.items():
                if not cols_:
                    continue
                for party in ['Democrat', 'Republican', 'Independent']:
                    party_df = month_df[month_df['pid3'] == party]
                    if party_df.empty:
                        continue
                    issue_votes = party_df[cols_].replace(vote_map)
                    issue_votes = issue_votes.apply(pd.to_numeric, errors='coerce')
                    issue_votes = issue_votes.replace(3, np.nan)
                    support = (issue_votes >= 4).sum().sum()
                    oppose = (issue_votes <= 2).sum().sum()
                    total = support + oppose
                    if total > 0:
                        support_pct = support / total * 100
                        summary_data.append({
                            'Issue': issue,
                            'pid3': party,
                            'Support %': support_pct
                        })

            plot_df = pd.DataFrame(summary_data)

            with cols[i]:
                st.markdown(f"#### {month}")
                if not plot_df.empty:
                    fig = px.bar(
                        plot_df,
                        x='Issue',
                        y='Support %',
                        color='pid3',
                        barmode='group',
                        orientation='v',
                        color_discrete_map={
                            'Republican': '#d73027',
                            'Democrat': '#4575b4',
                            'Independent': '#008000'
                        },
                        category_orders={'Issue': list(issues.keys())}
                    )
                    fig.update_layout(
                        xaxis_title='Policy Issue',
                        yaxis_title='Support Percentage',
                        title=None,
                        uniformtext_minsize=8,
                        uniformtext_mode='hide',
                        margin=dict(l=10, r=10, t=30, b=10),
                        legend=dict(font=dict(size=10)),
                        height=330
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.write("No data.")


    vote_map = {
        "Hate It": 1,
        "Dislike It": 2,
        "Not Sure": 3,
        "Good Idea": 4,
        "Critical to Me & Others": 5
    }

    issues = {
        'Economic Mobility & Growth': [col for col in combined.columns if col.startswith('Economic')],
        'K-12 Education': [col for col in combined.columns if col.startswith('Education')],
        'Healthcare': [col for col in combined.columns if col.startswith('Healthcare')],
        'Energy Policy': [col for col in combined.columns if col.startswith('Energy')],
        'Taxes': [col for col in combined.columns if col.startswith('Taxes')],
        'Federal Spending & Debt': [col for col in combined.columns if col.startswith('Fed')]
    }

    month_pairs = [("May", "June"), ("July", "August"),("September", )]
    st.markdown("#### Policy Area Oppose Breakdown by Party")
    for row_pair in month_pairs:
        cols = st.columns(len(row_pair))  # 2 for pairs, 1 for single
        for i, month in enumerate(row_pair):
            month_df = combined[combined["Month"] == month]

            summary_data = []
            for issue, cols_ in issues.items():
                if not cols_:
                    continue
                for party in ['Democrat', 'Republican', 'Independent']:
                    party_df = month_df[month_df['pid3'] == party]
                    if party_df.empty:
                        continue
                    issue_votes = party_df[cols_].replace(vote_map)
                    issue_votes = issue_votes.apply(pd.to_numeric, errors='coerce')
                    issue_votes = issue_votes.replace(3, np.nan)  # Remove "Not Sure"
                    oppose = (issue_votes <= 2).sum().sum()
                    support = (issue_votes >= 4).sum().sum()
                    total = support + oppose
                    if total > 0:
                        oppose_pct = oppose / total * 100
                        summary_data.append({
                            'Issue': issue,
                            'pid3': party,
                            'Oppose %': oppose_pct
                        })

            plot_df = pd.DataFrame(summary_data)

            with cols[i]:
                st.markdown(f"#### {month}")
                if not plot_df.empty:
                    fig = px.bar(
                        plot_df,
                        x='Issue',
                        y='Oppose %',
                        color='pid3',
                        barmode='group',
                        orientation='v',
                        title=None,
                        color_discrete_map={
                            'Republican': '#d73027',
                            'Democrat': '#4575b4',
                            'Independent': '#008000'
                        },
                        category_orders={'Issue': list(issues.keys())}
                    )
                    fig.update_layout(
                        xaxis_title='Policy Issue',
                        yaxis_title='Oppose Percentage',
                        uniformtext_minsize=8,
                        uniformtext_mode='hide',
                        margin=dict(l=10, r=10, t=30, b=10),
                        legend=dict(font=dict(size=10)),
                        height=330
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.write("No data.")

with st.expander("Policy Area Oppose Breakdown by Party — Current Direction Only (All Months, 2×2 Grid)", expanded=False):
    vote_map = {
        "Hate It": 1,
        "Dislike It": 2,
        "Not Sure": 3,
        "Good Idea": 4,
        "Critical to Me & Others": 5
    }

    issues = {
        'Economic Mobility & Growth': [col for col in combined.columns if col.startswith('Economic')],
        'K-12 Education': [col for col in combined.columns if col.startswith('Education')],
        'Healthcare': [col for col in combined.columns if col.startswith('Healthcare')],
        'Energy Policy': [col for col in combined.columns if col.startswith('Energy')],
        'Taxes': [col for col in combined.columns if col.startswith('Taxes')],
        'Federal Spending & Debt': [col for col in combined.columns if col.startswith('Fed')]
    }

    month_pairs = [("May", "June"), ("July", "August"),("September", )]

    for row_pair in month_pairs:
        cols = st.columns(len(row_pair))  # 2 for pairs, 1 for single
        for i, month in enumerate(row_pair):
            # Only keep 'Current Direction' respondents for this month
            month_df = combined[
                (combined["Month"] == month) &
                (combined["Grand Bargain or Current Direction?"] == "Current Direction")
            ]

            summary_data = []
            for issue, cols_ in issues.items():
                if not cols_:
                    continue
                for party in ['Democrat', 'Republican', 'Independent']:
                    party_df = month_df[month_df['pid3'] == party]
                    if party_df.empty:
                        continue
                    issue_votes = party_df[cols_].replace(vote_map)
                    issue_votes = issue_votes.apply(pd.to_numeric, errors='coerce')
                    issue_votes = issue_votes.replace(3, np.nan)  # Remove "Not Sure"
                    oppose = (issue_votes <= 2).sum().sum()
                    support = (issue_votes >= 4).sum().sum()
                    total = support + oppose
                    if total > 0:
                        oppose_pct = oppose / total * 100
                        summary_data.append({
                            'Issue': issue,
                            'pid3': party,
                            'Oppose %': oppose_pct
                        })

            plot_df = pd.DataFrame(summary_data)

            with cols[i]:
                st.markdown(f"#### {month}")
                if not plot_df.empty:
                    fig = px.bar(
                        plot_df,
                        x='Issue',
                        y='Oppose %',
                        color='pid3',
                        barmode='group',
                        orientation='v',
                        title=None,
                        color_discrete_map={
                            'Republican': '#d73027',
                            'Democrat': '#4575b4',
                            'Independent': '#008000'
                        },
                        category_orders={'Issue': list(issues.keys())}
                    )
                    fig.update_layout(
                        xaxis_title='Policy Issue',
                        yaxis_title='Oppose Percentage',
                        uniformtext_minsize=8,
                        uniformtext_mode='hide',
                        margin=dict(l=10, r=10, t=30, b=10),
                        legend=dict(font=dict(size=10)),
                        height=330
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.write("No data.")

with st.expander("Top Proposals Supported/Opposed by Party (All Months, 2×2 Grid)", expanded=False):
    vote_map = {
        "Hate It": 1,
        "Dislike It": 2,
        "Not Sure": 3,
        "Good Idea": 4,
        "Critical to Me & Others": 5
    }

    # Proposal columns for your data
    proposal_cols = [col for col in combined.columns if
                     col.startswith('Economic Mobility') or
                     col.startswith('Education') or
                     col.startswith('Healthcare') or
                     col.startswith('Energy') or
                     col.startswith('Fed Spending & Debt') or
                     col.startswith('Taxes')]

    month_pairs = [("May", "June"), ("July", "August"),("September", )]
    st.markdown("#### Top Proposals Supported by Party")
    for row_pair in month_pairs:
        cols = st.columns(len(row_pair))  # 2 for pairs, 1 for single
        for i, month in enumerate(row_pair):
            month_df = combined[combined["Month"] == month]
            df_long = month_df[month_df['pid3'].isin(['Democrat', 'Republican', 'Independent'])].melt(
                id_vars=['pid3'],
                value_vars=proposal_cols,
                var_name='Proposal',
                value_name='Vote'
            )
            df_long['Vote'] = df_long['Vote'].replace(vote_map)
            df_long['Vote'] = pd.to_numeric(df_long['Vote'], errors='coerce')
            df_long = df_long[df_long['Vote'] != 3]  # Drop "Not Sure"

            df_long['Support'] = df_long['Vote'] >= 4
            support_summary = (
                df_long.groupby(['Proposal', 'pid3'])['Support']
                .agg(['sum', 'count'])
                .reset_index()
            )
            support_summary['Support %'] = 100 * support_summary['sum'] / support_summary['count']

            # Find top 5 proposals per party, get their union
            top5_republican = (
                support_summary[support_summary['pid3'] == 'Republican']
                .sort_values(by='Support %', ascending=False)
                .head(5)['Proposal']
            )
            top5_democrat = (
                support_summary[support_summary['pid3'] == 'Democrat']
                .sort_values(by='Support %', ascending=False)
                .head(5)['Proposal']
            )
            top_proposals = list(set(top5_republican).union(set(top5_democrat)))

            filtered_df = support_summary[
                (support_summary['Proposal'].isin(top_proposals)) &
                (support_summary['pid3'].isin(['Democrat', 'Republican', 'Independent']))
            ]

            with cols[i]:
                st.markdown(f"#### {month}")
                if not filtered_df.empty:
                    # ---- SORT BY OVERALL MEAN SUPPORT ----
                    mean_support = (
                        filtered_df.groupby('Proposal')['Support %']
                        .mean()
                        .sort_values(ascending=False)
                        .index
                        .tolist()
                    )
                    fig = px.bar(
                        filtered_df,
                        x='Proposal',
                        y='Support %',
                        color='pid3',
                        barmode='group',
                        orientation='v',
                        color_discrete_map={
                            'Republican': '#d73027',
                            'Democrat': '#4575b4',
                            'Independent': '#008000'
                        },
                        category_orders={'Proposal': mean_support}
                    )
                    fig.update_layout(
                        xaxis_title='Proposal',
                        yaxis_title='Support Percentage',
                        title=None,
                        uniformtext_minsize=8,
                        uniformtext_mode='hide',
                        margin=dict(l=10, r=10, t=30, b=10),
                        legend=dict(font=dict(size=10)),
                        height=330
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.write("No data.")

    vote_map = {
        "Hate It": 1,
        "Dislike It": 2,
        "Not Sure": 3,
        "Good Idea": 4,
        "Critical to Me & Others": 5
    }

    proposal_cols = [col for col in combined.columns if
                     col.startswith('Economic Mobility') or
                     col.startswith('Education') or
                     col.startswith('Healthcare') or
                     col.startswith('Energy') or
                     col.startswith('Fed Spending & Debt') or
                     col.startswith('Taxes')]

    month_pairs = [("May", "June"), ("July", "August"),("September", )]
    st.markdown("#### Top Proposals Opposed by Party")
    for row_pair in month_pairs:
        cols = st.columns(len(row_pair))  # 2 for pairs, 1 for single
        for i, month in enumerate(row_pair):
            month_df = combined[combined["Month"] == month]
            df_long = month_df[month_df['pid3'].isin(['Democrat', 'Republican', 'Independent'])].melt(
                id_vars=['pid3'],
                value_vars=proposal_cols,
                var_name='Proposal',
                value_name='Vote'
            )
            df_long['Vote'] = df_long['Vote'].replace(vote_map)
            df_long['Vote'] = pd.to_numeric(df_long['Vote'], errors='coerce')
            df_long = df_long[df_long['Vote'].notna()]  # Keep valid votes

            df_long['Oppose'] = df_long['Vote'] <= 2
            oppose_summary = (
                df_long.groupby(['Proposal', 'pid3'])['Oppose']
                .agg(['sum', 'count'])
                .reset_index()
            )
            oppose_summary['Oppose %'] = 100 * oppose_summary['sum'] / oppose_summary['count']

            # Find top 5 least supported proposals per party (highest "Oppose %" per party)
            top5_republican = (
                oppose_summary[oppose_summary['pid3'] == 'Republican']
                .sort_values(by='Oppose %', ascending=False)
                .head(5)['Proposal']
            )
            top5_democrat = (
                oppose_summary[oppose_summary['pid3'] == 'Democrat']
                .sort_values(by='Oppose %', ascending=False)
                .head(5)['Proposal']
            )
            top_proposals = list(set(top5_republican).union(set(top5_democrat)))

            filtered_df = oppose_summary[
                (oppose_summary['Proposal'].isin(top_proposals)) &
                (oppose_summary['pid3'].isin(['Democrat', 'Republican', 'Independent']))
            ]

            with cols[i]:
                st.markdown(f"#### {month}")
                if not filtered_df.empty:
                    # ---- SORT BY OVERALL MEAN OPPOSE ----
                    mean_oppose = (
                        filtered_df.groupby('Proposal')['Oppose %']
                        .mean()
                        .sort_values(ascending=False)
                        .index
                        .tolist()
                    )
                    fig = px.bar(
                        filtered_df,
                        x='Proposal',
                        y='Oppose %',
                        color='pid3',
                        barmode='group',
                        orientation='v',
                        color_discrete_map={
                            'Republican': '#d73027',
                            'Democrat': '#4575b4',
                            'Independent': '#008000'
                        },
                        category_orders={'Proposal': mean_oppose}
                    )
                    fig.update_layout(
                        xaxis_title='Proposal',
                        yaxis_title='Oppose Percentage',
                        title=None,
                        uniformtext_minsize=8,
                        uniformtext_mode='hide',
                        margin=dict(l=10, r=10, t=30, b=10),
                        legend=dict(font=dict(size=10)),
                        height=330
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.write("No data.")

with st.expander("Top 5 Least Supported Proposals by Party — Current Direction Only (All Months, 2×2 Grid)", expanded=False):
    vote_map = {
        "Hate It": 1,
        "Dislike It": 2,
        "Not Sure": 3,
        "Good Idea": 4,
        "Critical to Me & Others": 5
    }

    proposal_cols = [col for col in combined.columns if
                     col.startswith('Economic Mobility') or
                     col.startswith('Education') or
                     col.startswith('Healthcare') or
                     col.startswith('Energy') or
                     col.startswith('Fed Spending & Debt') or
                     col.startswith('Taxes')]

    month_pairs = [("May", "June"), ("July", "August"),("September", )]

    for row_pair in month_pairs:
        cols = st.columns(len(row_pair))  # 2 for pairs, 1 for single
        for i, month in enumerate(row_pair):
            # Only 'Current Direction' respondents for this month
            month_df = combined[
                (combined["Month"] == month) &
                (combined["Grand Bargain or Current Direction?"] == "Current Direction")
            ]
            df_long = month_df[month_df['pid3'].isin(['Democrat', 'Republican', 'Independent'])].melt(
                id_vars=['pid3'],
                value_vars=proposal_cols,
                var_name='Proposal',
                value_name='Vote'
            )
            df_long['Vote'] = df_long['Vote'].replace(vote_map)
            df_long['Vote'] = pd.to_numeric(df_long['Vote'], errors='coerce')
            df_long = df_long[df_long['Vote'].notna()]  # Only valid votes

            df_long['Oppose'] = df_long['Vote'] <= 2
            oppose_summary = (
                df_long.groupby(['Proposal', 'pid3'])['Oppose']
                .agg(['sum', 'count'])
                .reset_index()
            )
            oppose_summary['Oppose %'] = 100 * oppose_summary['sum'] / oppose_summary['count']

            # Top 5 least supported proposals per party (highest Oppose % per party)
            top5_republican = (
                oppose_summary[oppose_summary['pid3'] == 'Republican']
                .sort_values(by='Oppose %', ascending=False)
                .head(5)['Proposal']
            )
            top5_democrat = (
                oppose_summary[oppose_summary['pid3'] == 'Democrat']
                .sort_values(by='Oppose %', ascending=False)
                .head(5)['Proposal']
            )
            top_proposals = list(set(top5_republican).union(set(top5_democrat)))

            filtered_df = oppose_summary[
                (oppose_summary['Proposal'].isin(top_proposals)) &
                (oppose_summary['pid3'].isin(['Democrat', 'Republican', 'Independent']))
            ]

            with cols[i]:
                st.markdown(f"#### {month}")
                if not filtered_df.empty:
                    # ---- SORT BY OVERALL MEAN OPPOSE ----
                    mean_oppose = (
                        filtered_df.groupby('Proposal')['Oppose %']
                        .mean()
                        .sort_values(ascending=False)
                        .index
                        .tolist()
                    )
                    fig = px.bar(
                        filtered_df,
                        x='Proposal',
                        y='Oppose %',
                        color='pid3',
                        barmode='group',
                        orientation='v',
                        color_discrete_map={
                            'Republican': '#d73027',
                            'Democrat': '#4575b4',
                            'Independent': '#008000'
                        },
                        category_orders={'Proposal': mean_oppose}
                    )
                    fig.update_layout(
                        xaxis_title='Proposal',
                        yaxis_title='Oppose Percentage',
                        title=None,
                        uniformtext_minsize=8,
                        uniformtext_mode='hide',
                        margin=dict(l=10, r=10, t=30, b=10),
                        legend=dict(font=dict(size=10)),
                        height=330
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.write("No data.")

with st.expander("Top 5 Supported & Opposed Proposals — Per Party & Month (24 charts, Single Party Each)", expanded=False):
    vote_map = {
        "Hate It": 1,
        "Dislike It": 2,
        "Not Sure": 3,
        "Good Idea": 4,
        "Critical to Me & Others": 5
    }

    proposal_cols = [col for col in combined.columns if
                     col.startswith('Economic Mobility') or
                     col.startswith('Education') or
                     col.startswith('Healthcare') or
                     col.startswith('Energy') or
                     col.startswith('Fed Spending & Debt') or
                     col.startswith('Taxes')]

    months = ["May", "June", "July", "August", "September"]
    parties = ["Democrat", "Republican", "Independent"]
    color_map = {
        'Republican': '#d73027',
        'Democrat': '#4575b4',
        'Independent': '#008000'
    }

    # --- SUPPORT CHARTS ---
    st.markdown("### Top 5 Supported Proposals — Per Party, Per Month")
    for party in parties:
        st.markdown(f"#### {party}")
        cols = st.columns(5)
        for i, month in enumerate(months):
            month_df = combined[(combined["Month"] == month) & (combined["pid3"] == party)]
            df_long = month_df.melt(
                id_vars=['pid3'],
                value_vars=proposal_cols,
                var_name='Proposal',
                value_name='Vote'
            )
            df_long['Vote'] = df_long['Vote'].replace(vote_map)
            df_long['Vote'] = pd.to_numeric(df_long['Vote'], errors='coerce')
            df_long = df_long[df_long['Vote'].notna()]

            df_long['Support'] = df_long['Vote'] >= 4
            support_summary = (
                df_long.groupby(['Proposal'])['Support']
                .agg(['sum', 'count'])
                .reset_index()
            )
            support_summary['Support %'] = 100 * support_summary['sum'] / support_summary['count']

            # Top 5 by this party for this month
            top5 = (
                support_summary
                .sort_values(by='Support %', ascending=False)
                .head(5)['Proposal']
            ).tolist()

            filtered_df = support_summary[support_summary['Proposal'].isin(top5)]

            with cols[i]:
                st.markdown(f"**{month}**")
                if not filtered_df.empty:
                    mean_support = (
                        filtered_df.set_index('Proposal')['Support %']
                        .sort_values(ascending=False)
                        .index
                        .tolist()
                    )
                    fig = px.bar(
                        filtered_df,
                        x='Proposal',
                        y='Support %',
                        color_discrete_sequence=[color_map[party]],
                        orientation='v',
                        category_orders={'Proposal': mean_support}
                    )
                    fig.update_layout(
                        xaxis_title='Proposal',
                        yaxis_title='Support Percentage',
                        showlegend=False,
                        uniformtext_minsize=8,
                        uniformtext_mode='hide',
                        margin=dict(l=10, r=10, t=30, b=10),
                        height=320
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.write("No data.")

    # --- OPPOSE CHARTS ---
    st.markdown("### Top 5 Opposed Proposals — Per Party, Per Month")
    for party in parties:
        st.markdown(f"#### {party}")
        cols = st.columns(5)
        for i, month in enumerate(months):
            month_df = combined[(combined["Month"] == month) & (combined["pid3"] == party)]
            df_long = month_df.melt(
                id_vars=['pid3'],
                value_vars=proposal_cols,
                var_name='Proposal',
                value_name='Vote'
            )
            df_long['Vote'] = df_long['Vote'].replace(vote_map)
            df_long['Vote'] = pd.to_numeric(df_long['Vote'], errors='coerce')
            df_long = df_long[df_long['Vote'].notna()]

            df_long['Oppose'] = df_long['Vote'] <= 2
            oppose_summary = (
                df_long.groupby(['Proposal'])['Oppose']
                .agg(['sum', 'count'])
                .reset_index()
            )
            oppose_summary['Oppose %'] = 100 * oppose_summary['sum'] / oppose_summary['count']

            # Top 5 opposed by this party for this month
            top5 = (
                oppose_summary
                .sort_values(by='Oppose %', ascending=False)
                .head(5)['Proposal']
            ).tolist()

            filtered_df = oppose_summary[oppose_summary['Proposal'].isin(top5)]

            with cols[i]:
                st.markdown(f"**{month}**")
                if not filtered_df.empty:
                    mean_oppose = (
                        filtered_df.set_index('Proposal')['Oppose %']
                        .sort_values(ascending=False)
                        .index
                        .tolist()
                    )
                    fig = px.bar(
                        filtered_df,
                        x='Proposal',
                        y='Oppose %',
                        color_discrete_sequence=[color_map[party]],
                        orientation='v',
                        category_orders={'Proposal': mean_oppose}
                    )
                    fig.update_layout(
                        xaxis_title='Proposal',
                        yaxis_title='Oppose Percentage',
                        showlegend=False,
                        uniformtext_minsize=8,
                        uniformtext_mode='hide',
                        margin=dict(l=10, r=10, t=30, b=10),
                        height=320
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.write("No data.")

import streamlit as st
import pandas as pd
import plotly.express as px
import us  # pip install us


# Load CSVs
may_df = pd.read_csv("YouGov Data - May.csv")
june_df = pd.read_csv("YouGov Data - June.csv")
july_df = pd.read_csv("YouGov Data - July.csv")
august_df = pd.read_csv("YouGov Data - August.csv")
september_df = pd.read_csv("YouGov Data - September.csv")


# Add month column
may_df["Month"] = "May"
june_df["Month"] = "June"
july_df["Month"] = "July"
august_df["Month"] = "August"
september_df["Month"] = "September"

# Combine
df = pd.concat([may_df, june_df, july_df, august_df, september_df])

"""In states with the fewest residents, the sample size is too small to rely on. Future polls will focus on these states to get more precise data.
"""

# US state name to abbreviation mapping
us_state_abbrev = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR',
    'California': 'CA', 'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE',
    'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI', 'Idaho': 'ID',
    'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS',
    'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
    'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS',
    'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV',
    'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY',
    'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK',
    'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC',
    'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT',
    'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV',
    'Wisconsin': 'WI', 'Wyoming': 'WY', 'District of Columbia': 'DC'
}

# Add state abbreviations
df['inputstate'] = df['inputstate'].map(us_state_abbrev)

# Visualize who voted for the "Grand Bargain" vs. the "Current Direction" by US state

# 1. Map Yes/No to readable labels
df['GBP Label'] = df['Grand Bargain or Current Direction?']

# 2. Add state abbreviations
df['State Abbr'] = df['inputstate'].apply(lambda x: us.states.lookup(x).abbr if us.states.lookup(x) else None)

# 3. Make labels categorical to control legend order
df['GBP Label'] = pd.Categorical(df['GBP Label'], categories=['Grand Bargain', 'Current Direction'], ordered=True)

# Month toggle
month = st.radio("Select Month", ["May", "June", "July", "August", "September"], horizontal=True)
month_df = df[df["Month"] == month]

# 4) Compute % choosing Grand Bargain and total participants per state
support_counts = (
    month_df.groupby(['State Abbr', 'GBP Label'])
    .size()
    .unstack(fill_value=0)
    .reset_index()
)

support_counts['Total Participants'] = (
    support_counts.get('Grand Bargain', 0) + support_counts.get('Current Direction', 0)
)
support_counts['Percent'] = (
    support_counts.get('Grand Bargain', 0) / support_counts['Total Participants'].replace(0, np.nan)
)

# --- Make low-N states white without breaking the color scale ---
low_n = support_counts['Total Participants'] <= 5
support_counts['Percent_color'] = support_counts['Percent'].mask(low_n)  # NaN => white

# Hover label: show N/A for low N, otherwise 0–100%
support_counts['Grand Bargain %'] = np.where(
    low_n,
    'N/A',
    (support_counts['Percent'] * 100).round(0).astype('Int64').astype(str) + '%'
)

# 5) Plot choropleth (lock the color range!)
fig = px.choropleth(
    support_counts,
    locations='State Abbr',
    locationmode='USA-states',
    scope='usa',
    color='Percent_color',
    hover_name='State Abbr',
    hover_data={
        'Percent_color': False,          # hide raw 0–1 in hover
        'Grand Bargain %': True,         # show formatted %
        'Total Participants': True
    },
    color_continuous_scale='RdYlGn',
    title="Which would you choose:<br>The Grand Bargain or <br>The current direction?"
)

# Lock scale 0→1 and keep your horizontal colorbar + ticks
fig.update_layout(
    geo=dict(bgcolor='rgba(0,0,0,0)'),
    plot_bgcolor='white',
    margin=dict(l=0, r=0, t=50, b=120),
    coloraxis=dict(cmin=0, cmax=1),   # <-- keep legend consistent
    coloraxis_colorbar=dict(
        orientation='h',
        yanchor='bottom',
        y=-0.3,
        xanchor='center',
        x=0.5,
        tickmode='array',
        tickvals=[i/10 for i in range(0, 11)],
        ticktext=[str(i*10) for i in range(0, 11)]
    ),
    annotations=[
        dict(
            x=0.78, y=-0.33, xref='paper', yref='paper',
            text='Grand Bargain', showarrow=False, font=dict(size=15)
        ),
        dict(
            x=0.02, y=-0.33, xref='paper', yref='paper',
            text='White = ≤ 5 respondents', showarrow=False, font=dict(size=12)
        )
    ]
)

st.plotly_chart(fig, use_container_width=True)
