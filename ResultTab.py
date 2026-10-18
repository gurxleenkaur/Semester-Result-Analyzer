
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression

from pathlib import Path

# PAGE CONFIGURATION

st.set_page_config(
    page_title="ResultIQ | Student Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

SEMESTERS = {
    "Semester 1": "Semester1.csv",
    "Semester 2": "Semester2.csv",
    "Semester 3": "Semester3.csv",
}

COLORS = ["#C084FC", "#F472B6", "#818CF8",
          "#2DD4BF", "#FBBF24", "#FB7185"]

# GLASSMORPHISM + LIQUIDMORPHISM CSS

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');

:root {
    --bg: #100C18;
    --glass: rgba(255,255,255,0.055);
    --border: rgba(255,255,255,0.12);
    --text: #F7F0FF;
    --muted: #B9ACC9;
    --pink: #F472B6;
    --purple: #C084FC;
}

.stApp {
    background:
        radial-gradient(ellipse at 8% 5%, rgba(126,34,206,.23), transparent 35%),
        radial-gradient(ellipse at 92% 20%, rgba(190,24,93,.16), transparent 34%),
        radial-gradient(ellipse at 50% 95%, rgba(79,70,229,.15), transparent 40%),
        var(--bg);
    color: var(--text);
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stHeader"] {
    background: rgba(16,12,24,.45);
}

[data-testid="stSidebar"] {
    background: rgba(26,17,38,.92);
    border-right: 1px solid var(--border);
}

[data-testid="stSidebar"] * {
    color: var(--text);
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1600px;
}

h1, h2, h3 {
    font-family: 'Manrope', sans-serif !important;
    color: #FFF7FF !important;
    letter-spacing: -0.6px;
}

p, label, .stMarkdown, [data-testid="stCaptionContainer"] {
    color: var(--muted);
}

.hero {
    padding: 30px 32px;
    border: 1px solid rgba(255,255,255,.16);
    border-radius: 26px;
    background:
        radial-gradient(circle at 95% 10%, rgba(244,114,182,.20), transparent 30%),
        radial-gradient(circle at 5% 100%, rgba(192,132,252,.20), transparent 35%),
        rgba(255,255,255,.055);
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    box-shadow: 0 18px 60px rgba(0,0,0,.22),
                inset 0 1px 0 rgba(255,255,255,.12);
    margin-bottom: 25px;
}

.eyebrow {
    text-transform: uppercase;
    letter-spacing: 3px;
    font-size: 11px;
    font-weight: 700;
    color: #E9B8FF;
}

.hero-title {
    font-family: 'Manrope', sans-serif;
    font-size: clamp(28px, 4vw, 44px);
    line-height: 1.15;
    font-weight: 800;
    margin: 10px 0;
    color: white;
}

.gradient-text {
    background: linear-gradient(100deg, #F9A8D4, #C4B5FD, #A5F3FC);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}

.hero-subtitle {
    font-size: 14px;
    color: #C9BDD7;
    line-height: 1.8;
}

.glass-card {
    background: linear-gradient(135deg,
        rgba(255,255,255,.085),
        rgba(255,255,255,.025));
    border: 1px solid rgba(255,255,255,.12);
    border-radius: 20px;
    padding: 22px;
    backdrop-filter: blur(20px);
    box-shadow: 0 12px 36px rgba(0,0,0,.13),
                inset 0 1px 0 rgba(255,255,255,.06);
    margin-bottom: 12px;
}

.metric-label {
    color: #BFB0D1;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
}

.metric-value {
    color: #FFFFFF;
    font-family: 'Manrope', sans-serif;
    font-size: clamp(23px, 2.2vw, 34px);
    font-weight: 800;
    margin: 9px 0 4px;
}

.metric-note {
    color: #C4B5FD;
    font-size: 12px;
}

.section-caption {
    color: #BCAECC;
    font-size: 13px;
    margin-top: -8px;
    margin-bottom: 20px;
}

div[data-testid="stPlotlyChart"] {
    background: rgba(255,255,255,.035);
    border: 1px solid rgba(255,255,255,.09);
    border-radius: 20px;
    padding: 10px;
}

div[data-testid="stTabs"] button {
    border-radius: 12px;
    padding: 10px 18px;
}

div[data-testid="stTabs"] button[aria-selected="true"] {
    background: rgba(192,132,252,.15);
    color: #F0D5FF;
    border-bottom: 2px solid #C084FC;
}

.stButton > button, .stDownloadButton > button {
    background: linear-gradient(110deg, #A855F7, #DB2777);
    color: white;
    border: 1px solid rgba(255,255,255,.15);
    border-radius: 12px;
    padding: 10px 18px;
    font-weight: 700;
    transition: .2s ease;
}

.stButton > button:hover, .stDownloadButton > button:hover {
    border-color: #E9B8FF;
    box-shadow: 0 0 22px rgba(192,132,252,.25);
    transform: translateY(-1px);
    color: white;
}

[data-testid="stMetric"] {
    background: rgba(255,255,255,.045);
    border: 1px solid rgba(255,255,255,.10);
    border-radius: 16px;
    padding: 15px;
}

[data-testid="stMetricLabel"] {
    color: #C9BDD7;
}

[data-testid="stMetricValue"] {
    color: white;
}

.stAlert {
    border-radius: 14px;
}

hr {
    border-color: rgba(255,255,255,.10);
}

footer {
    visibility: hidden;
}

@media (max-width: 768px) {
    .hero {
        padding: 22px;
    }
    .glass-card {
        padding: 16px;
    }
}
</style>
""", unsafe_allow_html=True)


# DATA LOADING

@st.cache_data
def read_csv_data(file_bytes):
    import io
    return pd.read_csv(io.BytesIO(file_bytes))


def prepare_data(df, semester_name):
    df = df.copy()
    df.columns = df.columns.str.strip()

    if not {"Subject", "Percentage"}.issubset(df.columns):
        raise ValueError(
            f"{semester_name} must contain Subject and Percentage columns."
        )

    df["Subject"] = df["Subject"].astype(str).str.strip()
    df["Percentage"] = pd.to_numeric(
        df["Percentage"], errors="coerce"
    )

    df = df.dropna(subset=["Subject", "Percentage"])
    df = df[df["Subject"] != ""]

    if df.empty:
        raise ValueError(f"{semester_name} has no valid subject records.")

    if not df["Percentage"].between(0, 100).all():
        raise ValueError(
            f"{semester_name}: percentages must be between 0 and 100."
        )

    if df["Subject"].duplicated().any():
        raise ValueError(
            f"{semester_name}: duplicate subject names were found."
        )

    df["Semester"] = semester_name
    return df


# SIDEBAR

with st.sidebar:
    st.markdown("## ✦ ResultIQ")
    st.caption("Student performance intelligence")
    st.divider()

    st.markdown("### 📂 Your result files")
    st.caption("Upload a CSV to replace its local file for this session.")

    uploaded_files = {}

    for sem, filename in SEMESTERS.items():
        uploaded_files[sem] = st.file_uploader(
            f"{sem} · {filename}",
            type=["csv"],
            key=f"upload_{sem}"
        )

    st.divider()

    st.markdown("### 🎨 Dashboard settings")
    chart_theme = st.selectbox(
        "Visualization style",
        ["Dark", "Light"],
        index=0
    )

    show_values = st.toggle("Show chart values", value=True)

    st.divider()
    st.caption("ResultIQ • Academic Analytics")


# LOAD ALL SEMESTERS

semester_data = {}
load_errors = []

for sem, filename in SEMESTERS.items():
    try:
        uploaded = uploaded_files[sem]

        if uploaded is not None:
            df = read_csv_data(uploaded.getvalue())
        else:
            path = Path(__file__).resolve().parent / filename
            if not path.exists():
                continue
            df = pd.read_csv(path)

        semester_data[sem] = prepare_data(df, sem)

    except Exception as exc:
        load_errors.append(f"{sem}: {exc}")

if load_errors:
    for error in load_errors:
        st.error(error)

if not semester_data:
    st.markdown("""
    <div class="hero">
        <div class="eyebrow">WELCOME TO RESULTIQ</div>
        <div class="hero-title">Your grades.<br>
        <span class="gradient-text">Your growth story.</span></div>
        <div class="hero-subtitle">
        Upload your Semester 1, Semester 2 and Semester 3 CSV files
        in the sidebar to explore your academic performance.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.info(
        "Each CSV needs two columns: Subject and Percentage. "
        "You can also place the three CSV files beside app.py."
    )
    st.stop()


# PREPARE ANALYTICS
semester_order = list(SEMESTERS.keys())
available_semesters = [
    sem for sem in semester_order if sem in semester_data
]

all_data = pd.concat(
    [semester_data[sem] for sem in available_semesters],
    ignore_index=True
)

summary = (
    all_data.groupby("Semester", sort=False)
    .agg(
        Average=("Percentage", "mean"),
        Highest=("Percentage", "max"),
        Lowest=("Percentage", "min"),
        Subjects=("Subject", "count")
    )
    .reset_index()
)

summary["SemesterNumber"] = summary["Semester"].map({
    "Semester 1": 1,
    "Semester 2": 2,
    "Semester 3": 3
})

summary = summary.sort_values("SemesterNumber")

overall_average = all_data["Percentage"].mean()
best_subject_row = all_data.loc[all_data["Percentage"].idxmax()]
weak_subject_row = all_data.loc[all_data["Percentage"].idxmin()]

if len(summary) >= 2:
    previous_average = summary["Average"].iloc[-2]
    latest_average = summary["Average"].iloc[-1]
    improvement = latest_average - previous_average
else:
    improvement = None

# HERO
st.markdown("""
<div class="hero">
    <div class="eyebrow">✦ YOUR PERSONAL ACADEMIC INTELLIGENCE</div>
    <div class="hero-title">
        Understand your results.<br>
        <span class="gradient-text">Unlock your potential.</span>
    </div>
    <div class="hero-subtitle">
        Track semester performance, discover subject-level insights,
        compare progress and explore a simple ML-based forecast.
    </div>
</div>
""", unsafe_allow_html=True)


# TOP KPI CARDS

st.markdown("### 📌 Performance at a glance")

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""
    <div class="glass-card">
        <div class="metric-label">Overall Average</div>
        <div class="metric-value">{overall_average:.2f}%</div>
        <div class="metric-note">Across loaded subjects</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="glass-card">
        <div class="metric-label">Semesters Loaded</div>
        <div class="metric-value">{len(summary)} / 3</div>
        <div class="metric-note">Academic history</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    improvement_text = (
        f"{improvement:+.2f} pp"
        if improvement is not None else "N/A"
    )
    st.markdown(f"""
    <div class="glass-card">
        <div class="metric-label">Latest Change</div>
        <div class="metric-value">{improvement_text}</div>
        <div class="metric-note">Percentage-point change</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="glass-card">
        <div class="metric-label">Subjects Analysed</div>
        <div class="metric-value">{len(all_data)}</div>
        <div class="metric-note">Across all loaded semesters</div>
    </div>
    """, unsafe_allow_html=True)

# CHART THEME

if chart_theme == "Dark":
    template = "plotly_dark"
    paper_bg = "rgba(0,0,0,0)"
    plot_bg = "rgba(0,0,0,0)"
    font_color = "#EDE4F7"
else:
    template = "plotly_white"
    paper_bg = "rgba(0,0,0,0)"
    plot_bg = "rgba(255,255,255,0.45)"
    font_color = "#35233E"


def style_chart(fig, height=360):
    fig.update_layout(
        template=template,
        paper_bgcolor=paper_bg,
        plot_bgcolor=plot_bg,
        font=dict(
            family="DM Sans",
            color=font_color,
            size=12
        ),
        height=height,
        margin=dict(l=15, r=15, t=55, b=20),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0
        ),
        hoverlabel=dict(font_size=13)
    )
    return fig


# DASHBOARD TABS

tab_overview, tab_semester, tab_subjects, tab_prediction, tab_data = (
    st.tabs([
        "✦ Overview",
        "📚 Semester Analysis",
        "🎯 Subject Insights",
        "🔮 Prediction Lab",
        "📁 Data & Export"
    ])
)


# TAB 1: OVERVIEW

with tab_overview:
    st.markdown("### 📈 Your academic journey")
    st.markdown(
        '<div class="section-caption">A quick visual summary of your results.</div>',
        unsafe_allow_html=True
    )

    left, right = st.columns([1.5, 1])

    with left:
        fig = px.line(
            summary,
            x="Semester",
            y="Average",
            markers=True,
            text=summary["Average"].map(lambda x: f"{x:.1f}%"),
            title="Semester Average Trend",
            color_discrete_sequence=["#C084FC"]
        )

        fig.update_traces(
            line=dict(width=4),
            marker=dict(size=11, line=dict(width=2, color="#FFFFFF")),
            textposition="top center"
        )
        fig.update_yaxes(title="Average percentage", range=[0, 105])
        fig.update_xaxes(title="")
        style_chart(fig)
        st.plotly_chart(fig, use_container_width=True)

    with right:
        fig = px.bar(
            summary,
            x="Semester",
            y="Average",
            color="Semester",
            text=summary["Average"].map(lambda x: f"{x:.2f}%")
                if show_values else None,
            title="Semester Comparison",
            color_discrete_sequence=COLORS
        )

        fig.update_traces(
            textposition="outside",
            cliponaxis=False
        )
        fig.update_yaxes(title="Average percentage", range=[0, 110])
        fig.update_xaxes(title="")
        style_chart(fig)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 💡 Performance highlights")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("**🏆 Highest recorded score**")
        st.metric(
            str(best_subject_row["Subject"]),
            f'{best_subject_row["Percentage"]:.2f}%',
            str(best_subject_row["Semester"])
        )

    with c2:
        st.markdown("**🎯 Needs more attention**")
        st.metric(
            str(weak_subject_row["Subject"]),
            f'{weak_subject_row["Percentage"]:.2f}%',
            str(weak_subject_row["Semester"])
        )

    with c3:
        st.markdown("**📊 Semester direction**")
        if improvement is None:
            st.write("Load another semester to compare progress.")
        elif improvement > 0:
            st.success(f"Average increased by {improvement:.2f} percentage points.")
        elif improvement < 0:
            st.warning(f"Average decreased by {abs(improvement):.2f} percentage points.")
        else:
            st.info("The latest and previous semester averages are equal.")


# TAB 2: SEMESTER ANALYSIS

with tab_semester:
    st.markdown("### 📚 Explore individual semesters")

    selected_sem = st.selectbox(
        "Choose a semester",
        available_semesters,
        key="semester_analysis"
    )

    sem_df = semester_data[selected_sem]
    sem_average = sem_df["Percentage"].mean()

    a, b, c = st.columns(3)
    a.metric("Semester Average", f"{sem_average:.2f}%")
    b.metric("Highest Subject", f'{sem_df["Percentage"].max():.2f}%')
    c.metric("Lowest Subject", f'{sem_df["Percentage"].min():.2f}%')

    fig = px.bar(
        sem_df.sort_values("Percentage", ascending=True),
        x="Percentage",
        y="Subject",
        orientation="h",
        color="Percentage",
        color_continuous_scale=["#F472B6", "#A78BFA", "#2DD4BF"],
        text=sem_df.sort_values("Percentage", ascending=True)["Percentage"]
            .map(lambda x: f"{x:.1f}%") if show_values else None,
        title=f"{selected_sem}: Subject-wise Performance"
    )

    fig.update_traces(textposition="outside", cliponaxis=False)
    fig.update_xaxes(title="Percentage", range=[0, 110])
    fig.update_yaxes(title="")
    style_chart(fig, height=max(360, len(sem_df) * 42))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### 📋 Semester result table")
    st.dataframe(
        sem_df[["Subject", "Percentage"]].sort_values(
            "Percentage", ascending=False
        ),
        use_container_width=True,
        hide_index=True
    )

# TAB 3: SUBJECT INSIGHTS
with tab_subjects:
    st.markdown("### 🎯 Understand your subject performance")

    subject_semesters = st.multiselect(
        "Semesters to compare",
        available_semesters,
        default=available_semesters,
        key="subject_comparison"
    )

    compare_df = all_data[
        all_data["Semester"].isin(subject_semesters)
    ].copy()

    if compare_df.empty:
        st.info("Select at least one semester.")
    else:
        fig = px.bar(
            compare_df,
            x="Subject",
            y="Percentage",
            color="Semester",
            barmode="group",
            color_discrete_sequence=COLORS,
            text=compare_df["Percentage"].map(lambda x: f"{x:.0f}%")
                if show_values else None,
            title="Subject-wise Semester Comparison"
        )
        fig.update_traces(textposition="outside", cliponaxis=False)
        fig.update_yaxes(title="Percentage", range=[0, 115])
        fig.update_xaxes(title="", tickangle=-25)
        style_chart(fig, height=450)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("#### 🕸️ Subject performance radar")

        radar_sem = st.selectbox(
            "Choose semester for radar chart",
            available_semesters,
            key="radar_semester"
        )

        radar_df = semester_data[radar_sem]

        radar = go.Figure()
        radar.add_trace(go.Scatterpolar(
            r=radar_df["Percentage"].tolist(),
            theta=radar_df["Subject"].tolist(),
            fill="toself",
            name=radar_sem,
            line=dict(color="#C084FC", width=3),
            fillcolor="rgba(192,132,252,0.22)"
        ))

        radar.update_layout(
            polar=dict(
                bgcolor="rgba(255,255,255,0.025)",
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    gridcolor="rgba(255,255,255,0.12)"
                ),
                angularaxis=dict(
                    gridcolor="rgba(255,255,255,0.12)"
                )
            ),
            showlegend=False
        )
        style_chart(radar, height=480)
        st.plotly_chart(radar, use_container_width=True)

        st.markdown("#### 🧠 Suggested focus areas")

        latest_sem = available_semesters[-1]
        latest_df = semester_data[latest_sem]
        threshold = st.slider(
            "Flag subjects below this percentage",
            min_value=30,
            max_value=90,
            value=60
        )

        focus_df = latest_df[
            latest_df["Percentage"] < threshold
        ].sort_values("Percentage")

        if focus_df.empty:
            st.success(
                f"All subjects in {latest_sem} are at or above {threshold}%."
            )
        else:
            for _, row in focus_df.iterrows():
                st.warning(
                    f'**{row["Subject"]}** — {row["Percentage"]:.1f}%. '
                    "Prioritize revision, practice questions and error review."
                )


# TAB 4: ML PREDICTION
with tab_prediction:
    st.markdown("### 🔮 Semester 4 prediction lab")
    st.markdown(
        '<div class="section-caption">'
        'A simple Linear Regression demonstration using your semester averages.'
        '</div>',
        unsafe_allow_html=True
    )

    if len(summary) < 2:
        st.warning(
            "At least two semester averages are needed to fit a regression line. "
            "Upload more semester files to enable prediction."
        )
    else:
        X = summary[["SemesterNumber"]]
        y = summary["Average"]

        model = LinearRegression()
        model.fit(X, y)

        next_sem_number = int(summary["SemesterNumber"].max()) + 1
        next_prediction = float(
            model.predict(pd.DataFrame({
                "SemesterNumber": [next_sem_number]
            }))[0]
        )

        # A percentage must stay between 0 and 100.
        displayed_prediction = float(np.clip(next_prediction, 0, 100))

        pcol1, pcol2 = st.columns([1, 1])

        with pcol1:
            st.markdown(f"""
            <div class="glass-card">
                <div class="metric-label">Estimated Semester {next_sem_number}</div>
                <div class="metric-value">{displayed_prediction:.2f}%</div>
                <div class="metric-note">Linear Regression estimate</div>
            </div>
            """, unsafe_allow_html=True)

        with pcol2:
            st.markdown("#### How to interpret this")
            st.write(
                "The model fits a straight line through the available semester "
                "averages and extends it to the next semester."
            )
            st.caption(
                "This is not a confidence interval or a guarantee of future "
                "performance. With only two or three semesters, the estimate "
                "is highly uncertain."
            )

        historical = summary[["SemesterNumber", "Average"]].copy()
        historical["Type"] = "Actual"

        future = pd.DataFrame({
            "SemesterNumber": [
                int(summary["SemesterNumber"].max()),
                next_sem_number
            ],
            "Average": [
                float(summary["Average"].iloc[-1]),
                displayed_prediction
            ],
            "Type": ["Forecast", "Forecast"]
        })

        prediction_chart = go.Figure()

        prediction_chart.add_trace(go.Scatter(
            x=historical["SemesterNumber"],
            y=historical["Average"],
            mode="lines+markers+text",
            text=historical["Average"].map(lambda x: f"{x:.1f}%"),
            textposition="top center",
            name="Actual",
            line=dict(color="#C084FC", width=3),
            marker=dict(size=10)
        ))

        prediction_chart.add_trace(go.Scatter(
            x=future["SemesterNumber"],
            y=future["Average"],
            mode="lines+markers",
            name="Estimated trend",
            line=dict(color="#F472B6", width=3, dash="dash"),
            marker=dict(size=10)
        ))

        prediction_chart.update_layout(
            title="Actual Performance vs Estimated Trend",
            xaxis_title="Semester number",
            yaxis_title="Average percentage",
            xaxis=dict(
                tickmode="array",
                tickvals=list(range(1, next_sem_number + 1)),
                ticktext=[
                    f"Semester {i}"
                    for i in range(1, next_sem_number + 1)
                ]
            ),
            yaxis=dict(range=[0, 105])
        )
        style_chart(prediction_chart)
        st.plotly_chart(
            prediction_chart,
            use_container_width=True
        )

        st.info(
            "Project improvement idea: once you have several historical "
            "semesters and more relevant student data, compare regression "
            "models using a time-aware evaluation. Do not report accuracy "
            "from this tiny dataset as if it were validated."
        )

# TAB 5: DATA AND EXPORT
with tab_data:
    st.markdown("### 📁 Your academic data")

    st.markdown("#### Semester summary")
    st.dataframe(
        summary[
            ["Semester", "Average", "Highest", "Lowest", "Subjects"]
        ].round(2),
        use_container_width=True,
        hide_index=True
    )

    st.markdown("#### All subject records")
    st.dataframe(
        all_data[["Semester", "Subject", "Percentage"]],
        use_container_width=True,
        hide_index=True
    )

    csv_bytes = all_data[
        ["Semester", "Subject", "Percentage"]
    ].to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇️ Download all results as CSV",
        data=csv_bytes,
        file_name="resultiq_all_semesters.csv",
        mime="text/csv"
    )

    report = [
        "RESULTIQ - STUDENT PERFORMANCE SUMMARY",
        "=" * 42,
        f"Overall average: {overall_average:.2f}%",
        f"Semesters analysed: {len(summary)}",
        f"Subjects analysed: {len(all_data)}",
        "",
        "SEMESTER SUMMARY",
        "-" * 42,
    ]

    for _, row in summary.iterrows():
        report.append(
            f'{row["Semester"]}: average {row["Average"]:.2f}%, '
            f'highest {row["Highest"]:.2f}%, '
            f'lowest {row["Lowest"]:.2f}%'
        )

    report += [
        "",
        f'Highest recorded subject: {best_subject_row["Subject"]} '
        f'({best_subject_row["Percentage"]:.2f}%, '
        f'{best_subject_row["Semester"]})',
        f'Lowest recorded subject: {weak_subject_row["Subject"]} '
        f'({weak_subject_row["Percentage"]:.2f}%, '
        f'{weak_subject_row["Semester"]})',
        "",
        "Note: Semester averages are unweighted means of subject percentages."
    ]

    st.download_button(
        label="⬇️ Download performance report",
        data="\n".join(report),
        file_name="resultiq_performance_report.txt",
        mime="text/plain"
    )


# FOOTER

st.divider()
st.markdown(
    """
    <div style="text-align:center; padding:16px 0; color:#9B8BAE;">
        <b style="color:#D8B4FE;">ResultIQ</b> · Student Result Analytics
        <br><small>Visualize your progress. Identify your strengths. Plan your growth.</small>
    </div>
    """,
    unsafe_allow_html=True
)
