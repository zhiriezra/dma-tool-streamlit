import streamlit as st
import plotly.graph_objects as go

survey_config = {
    "Category 1": {
        "description": "Digital Business Strategy",
        "questions": [
            {"name": "Q1ai", "label": "Question 1: Already Invested (count)", "type": "number", "default": 0},
            {"name": "Q1pi", "label": "Question 1: Plan to Invest (count)", "type": "number", "default": 0},
            {"name": "Q2_cat1", "label": "Question 2: Preparedness Score (0-10)", "type": "number", "default": 0}
        ]
    },
    "Category 2": {
        "description": "Digital Readiness",
        "questions": [
            {"name": "Q3", "label": "Question 3: Count of Digital Technologies Already Being Used", "type": "number", "default": 0},
            {"name": "Simulation", "label": "Question 4: Simulation & Digital Twins", "type": "slider", "min": 0, "max": 5, "default": 0},
            {"name": "VR_AR", "label": "Question 4: Virtual/Augmented Reality", "type": "slider", "min": 0, "max": 5, "default": 0},
            {"name": "CAD_CAM", "label": "Question 4: Computer Aided Design & Manufacturing", "type": "slider", "min": 0, "max": 5, "default": 0},
            {"name": "MES", "label": "Question 4: Manufacturing Execution Systems", "type": "slider", "min": 0, "max": 5, "default": 0},
            {"name": "IoT", "label": "Question 4: Internet of Things (IoT) and Industrial Internet of Things (I-IoT)", "type": "slider", "min": 0, "max": 5, "default": 0},
            {"name": "Blockchain", "label": "Question 4: Blockchain Technology", "type": "slider", "min": 0, "max": 5, "default": 0},
            {"name": "Additive", "label": "Question 4: Additive Manufacturing", "type": "slider", "min": 0, "max": 5, "default": 0}
        ]
    },
    "Category 3": {
        "description": "Human-centric Digitilisation",
        "questions": [
            {"name": "Q5_cat3", "label": "Question 5: Re-skilling and up-skilling of staff for digitalisation", "type": "number", "default": 0},
            {"name": "Q6_cat3", "label": "Question 6:  Adoption of new digital solutions", "type": "number", "default": 0}
        ]
    },
    "Category 4": {
        "description": "Data Management & Security",
        "questions": [
            {"name": "Q5_cat4", "label": "Question 7: How is data managed?", "type": "number", "default": 0},
            {"name": "Q6_cat4", "label": "Question 8: Is data secured?", "type": "number", "default": 0}
        ]
    }
}

def calc_category1(data):
    """
    Category 1: Score = (Q1ai + Q1pi + Q2_cat1) * 3.33
    """
    return (data["Q1ai"] * 3.33) + (data["Q1pi"] * 3.33) + (data["Q2_cat1"] * 3.33)

def calc_category2(data):
    """
    Category 2: Score = (Q3 * 5) + (sum of advanced technology responses converted to [0,1] * 5)
    Conversion: each slider value is multiplied by 0.2.
    """
    adv_keys = ["Simulation", "VR_AR", "CAD_CAM", "MES", "IoT", "Blockchain", "Additive"]
    adv_sum = sum(data[k] for k in adv_keys)
    return (data["Q3"] * 5) + ((adv_sum * 0.2) * (10/7) * 5)

def calc_category3(data):
    """
    Category 3: Score = (Q5_cat3 + Q6_cat3) * 5
    """
    return (data["Q5_cat3"] * 5) + (data["Q6_cat3"] * 5)

def calc_category4(data):
    """
    Category 4: Score = (Q5_cat4 + Q6_cat4) * 5
    """
    return (data["Q5_cat4"] * 5) + (data["Q6_cat4"] * 5)

def calc_overall(cat1, cat2, cat3, cat4):
    """
    Overall Digital Maturity = Average of the four category scores.
    """
    return (cat1 + cat2 + cat3 + cat4) / 4


def create_gauge_chart(value, title, half_donut=False):
    """
    Returns a Plotly gauge chart.
    """
    domain_y = [0, 0.5] if half_donut else [0, 1]
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        number={'suffix': " %"},
        title={'text': title},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkgray"},
            'bar': {'color': "darkblue", 'thickness': 0.3},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 25], 'color': "red"},
                {'range': [25, 50], 'color': "orange"},
                {'range': [50, 75], 'color': "yellow"},
                {'range': [75, 100], 'color': "green"}
            ],
        },
        domain={'x': [0, 1], 'y': domain_y}
    ))
    fig.update_layout(height=300, margin={'t': 50, 'b': 0})
    return fig


st.set_page_config(page_title="Digital Maturity Calculator", layout="wide")
st.title("Digital Maturity Survey Calculator")
st.markdown("""
This tool calculates your enterprise’s digital maturity based on your survey responses.
""")

# Sidebar: Input method selection
st.sidebar.header("Input Options")
input_method = st.sidebar.radio("Choose input method:", options=["Manual Input", "Use Dummy Data"])

# Initialize response storage
user_data = {}


if input_method == "Use Dummy Data":
    st.info("Using default dummy data. Click the button below to calculate scores.")
    for category, config in survey_config.items():
        st.subheader(f"{category} — {config['description']}")
        with st.expander("View Data", expanded=True):
            for q in config["questions"]:
                key = q["name"]
                default = q.get("default", 0)
                user_data[key] = default
                st.write(f"**{q['label']}:** {default}")
    calculate = st.button("Calculate Digital Maturity")
    if not calculate:
        st.stop()
else:
    with st.form("survey_form"):
        st.markdown("### Enter Your Survey Responses")
        for category, config in survey_config.items():
            st.subheader(f"{category} — {config['description']}")
            with st.expander("Fill in responses", expanded=True):
                for q in config["questions"]:
                    key = q["name"]
                    label = q["label"]
                    default = q.get("default", 0)
                    if q["type"] == "number":
                        user_data[key] = st.number_input(label, min_value=0.0, max_value=1000.0, value=float(default), key=key)
                    elif q["type"] == "slider":
                        user_data[key] = st.slider(label, min_value=q.get("min", 0), max_value=q.get("max", 5), value=int(default), key=key)
                    else:
                        st.error(f"Unsupported input type for {label}")
        submitted = st.form_submit_button("Calculate Digital Maturity")
        if not submitted:
            st.stop()


category1_score = calc_category1(user_data)
category2_score = calc_category2(user_data)
category3_score = calc_category3(user_data)
category4_score = calc_category4(user_data)
overall_score = calc_overall(category1_score, category2_score, category3_score, category4_score)

# Rounding scores for display
cat1_disp = round(category1_score, 1)
cat2_disp = round(category2_score, 1)
cat3_disp = round(category3_score, 1)
cat4_disp = round(category4_score, 1)
overall_disp = round(overall_score, 1)

st.header("Digital Maturity Scores")
col1, col2 = st.columns(2)
with col1:
    st.metric("Category 1: Digital Business Strategy Score", f"{cat1_disp} %")
    st.metric("Category 2: Digital Readiness Score", f"{cat2_disp} %")
with col2:
    st.metric("Category 3: Human-centric Digitilisation Score", f"{cat3_disp} %")
    st.metric("Category 4: Data Management & Security Score", f"{cat4_disp} %")
st.markdown(f"### Overall Digital Maturity: **{overall_disp} %**")

st.header("Maturity Gauges")
# st.subheader("Overall Digital Maturity")
overall_fig = create_gauge_chart(overall_disp, "Overall Maturity", half_donut=True)
st.plotly_chart(overall_fig, use_container_width=True)

st.subheader("Category Breakdown")
cat_cols = st.columns(2)
with cat_cols[0]:
    st.plotly_chart(create_gauge_chart(cat1_disp, "Category 1: Digital Business Strategy"), use_container_width=True)
    st.plotly_chart(create_gauge_chart(cat3_disp, "Category 3: Human-centric Digitilisation"), use_container_width=True)
with cat_cols[1]:
    st.plotly_chart(create_gauge_chart(cat2_disp, "Category 2: Digital Readiness"), use_container_width=True)
    st.plotly_chart(create_gauge_chart(cat4_disp, "Category 4: Data Management & Security"), use_container_width=True)


# with st.expander("Show Raw Data & Calculations"):
#     st.write("#### User Input Data")
#     st.json(user_data)
#     st.write("#### Calculated Scores", {
#         "Category 1": cat1_disp,
#         "Category 2": cat2_disp,
#         "Category 3": cat3_disp,
#         "Category 4": cat4_disp,
#         "Overall Digital Maturity": overall_disp
#     })
