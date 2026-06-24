import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO

# ─────────────────────────────────────────────
# App Configuration
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="MGNREGA Schemes Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# Custom CSS – Professional Look
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* General background */
[data-testid="stAppViewContainer"] { background: #f0f2f6; }
[data-testid="stSidebar"] { background: #1a2340; }
[data-testid="stSidebar"] * { color: #e0e6f0 !important; }
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stTextInput label { color: #b0bcd4 !important; font-size: 0.8rem; text-transform: uppercase; letter-spacing: .05em; }

/* Metric cards */
div[data-testid="metric-container"] {
    background: white;
    border-radius: 12px;
    padding: 16px 20px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    border-left: 4px solid #3b6fd4;
}

/* Tab styling */
button[data-baseweb="tab"] { font-weight: 600; font-size: 0.82rem; }

/* Section headings */
h3 { color: #1a2340 !important; }
h4 { color: #2c3e6b !important; }

/* Table / dataframe */
[data-testid="stDataFrame"] { border-radius: 10px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }

/* Search highlight card */
.work-detail-card {
    background: white;
    border-radius: 14px;
    padding: 22px 28px;
    box-shadow: 0 4px 16px rgba(59,111,212,0.12);
    border-top: 4px solid #3b6fd4;
    margin-bottom: 20px;
}
.work-detail-card h4 { color: #1a2340; margin-bottom: 4px; }
.work-detail-card .subtitle { color: #6b7a99; font-size: 0.85rem; margin-bottom: 16px; }
.stat-row { display: flex; gap: 24px; flex-wrap: wrap; }
.stat-box { flex: 1; min-width: 120px; background: #f5f7fb; border-radius: 10px; padding: 12px 16px; text-align: center; }
.stat-box .val { font-size: 1.3rem; font-weight: 700; color: #3b6fd4; }
.stat-box .lbl { font-size: 0.72rem; color: #8898aa; text-transform: uppercase; letter-spacing: .06em; margin-top: 2px; }

/* Download button */
.stDownloadButton > button {
    background: linear-gradient(135deg, #1a2340, #3b6fd4);
    color: white !important;
    border: none;
    border-radius: 8px;
    padding: 8px 20px;
    font-weight: 600;
    letter-spacing: 0.03em;
}
.stDownloadButton > button:hover { opacity: 0.9; }

/* Divider */
hr { border-color: #dde3ee; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Header
# ─────────────────────────────────────────────
col_hd1, col_hd2 = st.columns([3, 1])
with col_hd1:
    st.markdown("## 📊 MGNREGA Schemes & Works Dashboard")
    st.caption("Upload your Excel / CSV report to generate professional, dynamic insights instantly.")
with col_hd2:
    uploaded_file = st.file_uploader("Upload Excel / CSV", type=["csv", "xlsx"], label_visibility="collapsed")


# ─────────────────────────────────────────────
# Helper: Format Indian Currency
# ─────────────────────────────────────────────
def fmt_inr(val):
    val = float(val)
    if val >= 1_00_00_000:
        return f"₹{val/1_00_00_000:.2f} Cr"
    elif val >= 1_00_000:
        return f"₹{val/1_00_000:.2f} L"
    else:
        return f"₹{val:,.0f}"


# ─────────────────────────────────────────────
# Helper: Progress badge color
# ─────────────────────────────────────────────
def progress_badge(p):
    if p == 0:
        return "🔴"
    elif p < 10:
        return "🟠"
    elif p < 50:
        return "🟡"
    elif p < 85:
        return "🟢"
    else:
        return "✅"


# ─────────────────────────────────────────────
# Helper: Export to formatted Excel
# ─────────────────────────────────────────────
def export_excel(dataframe: pd.DataFrame, sheet_name: str = "Report") -> bytes:
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        dataframe.to_excel(writer, index=False, sheet_name=sheet_name)
        workbook = writer.book
        worksheet = writer.sheets[sheet_name]

        # Formats
        header_fmt = workbook.add_format({
            "bold": True, "bg_color": "#1a2340", "font_color": "#FFFFFF",
            "border": 1, "align": "center", "valign": "vcenter", "font_size": 10
        })
        num_fmt = workbook.add_format({"num_format": "#,##0.00", "border": 1})
        pct_fmt = workbook.add_format({"num_format": "0.00\"%\"", "border": 1})
        text_fmt = workbook.add_format({"border": 1, "font_size": 9})
        alt_fmt = workbook.add_format({"border": 1, "font_size": 9, "bg_color": "#f0f4ff"})

        # Column widths
        col_widths = {
            "Work_Code": 18, "Panchayat": 20, "Work_Name": 40, "Work_Type": 22,
            "Fin_Year": 12, "Work_Status": 15, "Sanctioned_Amount": 18,
            "Wages_Paid": 15, "Material_Paid": 15, "Total_Paid": 15, "Progress_%": 14
        }
        for i, col in enumerate(dataframe.columns):
            w = col_widths.get(col, 16)
            worksheet.set_column(i, i, w)

        # Header row
        for col_num, col_name in enumerate(dataframe.columns):
            worksheet.write(0, col_num, col_name, header_fmt)
        worksheet.set_row(0, 22)

        # Data rows with alternating colour
        money_cols = {"Sanctioned_Amount", "Wages_Paid", "Material_Paid", "Total_Paid"}
        pct_cols = {"Progress_%"}
        col_list = list(dataframe.columns)
        for row_num, row in enumerate(dataframe.itertuples(index=False), start=1):
            base_fmt = alt_fmt if row_num % 2 == 0 else text_fmt
            for col_num, col_name in enumerate(col_list):
                val = row[col_num]   # positional – avoids getattr issues with special chars like %
                if col_name in money_cols:
                    worksheet.write_number(row_num, col_num, float(val), num_fmt)
                elif col_name in pct_cols:
                    worksheet.write_number(row_num, col_num, float(val), pct_fmt)
                else:
                    worksheet.write(row_num, col_num, str(val), base_fmt)

        # Freeze pane & autofilter
        worksheet.freeze_panes(1, 0)
        worksheet.autofilter(0, 0, len(dataframe), len(dataframe.columns) - 1)

    return output.getvalue()


# ─────────────────────────────────────────────
# Main App Logic
# ─────────────────────────────────────────────
if uploaded_file:
    with st.spinner("Data process ho raha hai..."):
        # Load
        if uploaded_file.name.endswith(".csv"):
            df_raw = pd.read_csv(uploaded_file, header=0)
        else:
            df_raw = pd.read_excel(uploaded_file, header=0)

        df_raw = df_raw.iloc[3:].copy()

        df = pd.DataFrame()
        df["Work_Code"]          = df_raw.iloc[:, 6].astype(str)
        df["Panchayat"]          = df_raw.iloc[:, 3].astype(str)
        df["Fin_Year"]           = df_raw.iloc[:, 4].astype(str)
        df["Work_Status"]        = df_raw.iloc[:, 5].astype(str)
        df["Work_Name"]          = df_raw.iloc[:, 7].astype(str)
        df["Work_Type"]          = df_raw.iloc[:, 11].astype(str)
        df["Sanctioned_Amount"]  = pd.to_numeric(df_raw.iloc[:, 15], errors="coerce").fillna(0)
        df["Wages_Paid"]         = pd.to_numeric(df_raw.iloc[:, 22], errors="coerce").fillna(0)
        df["Material_Paid"]      = pd.to_numeric(df_raw.iloc[:, 23], errors="coerce").fillna(0)
        df["Total_Paid"]         = df["Wages_Paid"] + df["Material_Paid"]
        df["Progress_%"]         = (df["Total_Paid"] / df["Sanctioned_Amount"].replace(0, float("nan")) * 100).fillna(0).round(2)

        columns_order = ["Work_Code", "Panchayat", "Work_Name", "Work_Type", "Fin_Year",
                         "Work_Status", "Sanctioned_Amount", "Wages_Paid", "Material_Paid",
                         "Total_Paid", "Progress_%"]
        df = df[columns_order].reset_index(drop=True)

    # ── Sidebar Filters ──────────────────────────────────────
    st.sidebar.markdown("## 🔍 Filters")

    selected_panchayat = st.sidebar.selectbox(
        "Panchayat", ["All"] + sorted(df["Panchayat"].unique().tolist())
    )
    selected_work_type = st.sidebar.selectbox(
        "Work Type / Scheme", ["All"] + sorted(df["Work_Type"].unique().tolist())
    )
    selected_fin_year = st.sidebar.selectbox(
        "Financial Year", ["All"] + sorted(df["Fin_Year"].unique().tolist(), reverse=True)
    )
    selected_status = st.sidebar.selectbox(
        "Work Status", ["All"] + sorted(df["Work_Status"].unique().tolist())
    )

    df_filtered = df.copy()
    if selected_panchayat != "All":
        df_filtered = df_filtered[df_filtered["Panchayat"] == selected_panchayat]
    if selected_work_type != "All":
        df_filtered = df_filtered[df_filtered["Work_Type"] == selected_work_type]
    if selected_fin_year != "All":
        df_filtered = df_filtered[df_filtered["Fin_Year"] == selected_fin_year]
    if selected_status != "All":
        df_filtered = df_filtered[df_filtered["Work_Status"] == selected_status]

    # ── Download Formatted Excel ──────────────────────────────
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📥 Export Report")
    excel_bytes = export_excel(df_filtered, sheet_name="Filtered_Report")
    st.sidebar.download_button(
        label="⬇️ Download Excel Report",
        data=excel_bytes,
        file_name="MGNREGA_Report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

    # ── KPIs ─────────────────────────────────────────────────
    st.markdown("### 📈 Key Performance Indicators")
    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("Total Works", f"{len(df_filtered):,}")
    k2.metric("Zero Paid Works", f"{len(df_filtered[df_filtered['Total_Paid'] == 0]):,}")
    k3.metric("Critical (< 10%)", f"{len(df_filtered[df_filtered['Progress_%'] < 10]):,}")
    k4.metric("Near Completion (> 85%)", f"{len(df_filtered[df_filtered['Progress_%'] > 85]):,}")
    k5.metric("Total Sanctioned", fmt_inr(df_filtered["Sanctioned_Amount"].sum()))

    st.markdown("---")

    # ── Charts Row 1 ─────────────────────────────────────────
    cc1, cc2 = st.columns(2)
    with cc1:
        st.markdown("#### 🏢 Work Types Distribution")
        wc = df_filtered["Work_Type"].value_counts().reset_index()
        wc.columns = ["Work_Type", "Count"]
        if len(wc) > 1:
            fig_pie = px.pie(
                wc, names="Work_Type", values="Count", hole=0.42,
                color_discrete_sequence=px.colors.qualitative.Pastel,
            )
            fig_pie.update_layout(margin=dict(t=10, b=10), legend_font_size=11)
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info(f"Only one type: **{wc['Work_Type'].iloc[0]}**")

    with cc2:
        st.markdown("#### 📅 Schemes by Financial Year")
        fy = df_filtered["Fin_Year"].value_counts().reset_index().sort_values("Fin_Year")
        fy.columns = ["Fin_Year", "Count"]
        fig_bar = px.bar(
            fy, x="Fin_Year", y="Count", text="Count",
            color="Fin_Year", color_discrete_sequence=px.colors.sequential.Blues_r,
        )
        fig_bar.update_layout(showlegend=False, margin=dict(t=10, b=10))
        st.plotly_chart(fig_bar, use_container_width=True)

    # ── Charts Row 2 ─────────────────────────────────────────
    cc3, cc4 = st.columns(2)
    with cc3:
        st.markdown("#### 📍 Panchayat-wise Works Count")
        pw = df_filtered.groupby("Panchayat").size().reset_index(name="Count").sort_values("Count", ascending=True)
        fig_pwh = px.bar(
            pw, x="Count", y="Panchayat", orientation="h", text="Count",
            color="Count", color_continuous_scale="Blues",
        )
        fig_pwh.update_layout(margin=dict(t=10, b=10), coloraxis_showscale=False)
        st.plotly_chart(fig_pwh, use_container_width=True)

    with cc4:
        st.markdown("#### 💰 Sanctioned vs Paid Amount (by Panchayat)")
        amt = df_filtered.groupby("Panchayat").agg(
            Sanctioned=("Sanctioned_Amount", "sum"),
            Paid=("Total_Paid", "sum")
        ).reset_index()
        fig_amt = go.Figure()
        fig_amt.add_trace(go.Bar(name="Sanctioned", x=amt["Panchayat"], y=amt["Sanctioned"], marker_color="#3b6fd4"))
        fig_amt.add_trace(go.Bar(name="Paid", x=amt["Panchayat"], y=amt["Paid"], marker_color="#43c59e"))
        fig_amt.update_layout(barmode="group", margin=dict(t=10, b=10), legend_font_size=11)
        st.plotly_chart(fig_amt, use_container_width=True)

    # ── Progress Distribution ─────────────────────────────────
    st.markdown("#### 🎯 Progress % Distribution Across Works")
    fig_hist = px.histogram(
        df_filtered, x="Progress_%", nbins=20,
        color_discrete_sequence=["#3b6fd4"],
        labels={"Progress_%": "Progress (%)"},
    )
    fig_hist.update_layout(margin=dict(t=10, b=10))
    st.plotly_chart(fig_hist, use_container_width=True)

    st.markdown("---")

    # ═══════════════════════════════════════════════════════════
    # 🔍 SEARCH SECTION – Work Name / Work Code
    # ═══════════════════════════════════════════════════════════
    st.markdown("### 🔎 Search Works — by Work Name or Work Code")

    search_query = st.text_input(
        "", placeholder="Type work name or work code (partial search works)...",
        label_visibility="collapsed"
    )

    if search_query.strip():
        q = search_query.strip().lower()
        mask = (
            df_filtered["Work_Name"].str.lower().str.contains(q, na=False) |
            df_filtered["Work_Code"].str.lower().str.contains(q, na=False)
        )
        search_results = df_filtered[mask].reset_index(drop=True)

        st.caption(f"**{len(search_results)}** result(s) found for `{search_query}`")

        if not search_results.empty:
            # Show shortlist as clickable table
            display_cols = ["Work_Code", "Panchayat", "Work_Name", "Work_Type",
                            "Work_Status", "Sanctioned_Amount", "Total_Paid", "Progress_%"]
            st.dataframe(
                search_results[display_cols].style.format({
                    "Sanctioned_Amount": "₹{:,.0f}",
                    "Total_Paid": "₹{:,.0f}",
                    "Progress_%": "{:.2f}%",
                }).background_gradient(subset=["Progress_%"], cmap="RdYlGn"),
                use_container_width=True,
            )

            st.markdown("---")
            # ── Individual Work Analytics ──────────────────────
            st.markdown("#### 📌 Individual Work Analytics")

            if len(search_results) == 1:
                selected_idx = 0
            else:
                work_options = [f"{r['Work_Code']} — {r['Work_Name'][:60]}" for _, r in search_results.iterrows()]
                sel = st.selectbox("Select a work to see its analytics:", work_options)
                selected_idx = work_options.index(sel)

            row = search_results.iloc[selected_idx]

            progress = float(row["Progress_%"])
            badge = progress_badge(progress)

            # Detail Card
            st.markdown(f"""
            <div class="work-detail-card">
                <h4>{badge} {row['Work_Name']}</h4>
                <div class="subtitle">
                    Work Code: <strong>{row['Work_Code']}</strong> &nbsp;|&nbsp;
                    Panchayat: <strong>{row['Panchayat']}</strong> &nbsp;|&nbsp;
                    FY: <strong>{row['Fin_Year']}</strong> &nbsp;|&nbsp;
                    Status: <strong>{row['Work_Status']}</strong>
                </div>
                <div class="stat-row">
                    <div class="stat-box">
                        <div class="val">{fmt_inr(row['Sanctioned_Amount'])}</div>
                        <div class="lbl">Sanctioned</div>
                    </div>
                    <div class="stat-box">
                        <div class="val">{fmt_inr(row['Wages_Paid'])}</div>
                        <div class="lbl">Wages Paid</div>
                    </div>
                    <div class="stat-box">
                        <div class="val">{fmt_inr(row['Material_Paid'])}</div>
                        <div class="lbl">Material Paid</div>
                    </div>
                    <div class="stat-box">
                        <div class="val">{fmt_inr(row['Total_Paid'])}</div>
                        <div class="lbl">Total Paid</div>
                    </div>
                    <div class="stat-box">
                        <div class="val">{progress:.1f}%</div>
                        <div class="lbl">Progress</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Mini analytics charts for the selected work
            wa1, wa2 = st.columns(2)

            with wa1:
                # Gauge / indicator for progress
                fig_gauge = go.Figure(go.Indicator(
                    mode="gauge+number+delta",
                    value=progress,
                    delta={"reference": 50, "increasing": {"color": "#43c59e"}},
                    gauge={
                        "axis": {"range": [0, 100], "tickwidth": 1},
                        "bar": {"color": "#3b6fd4"},
                        "steps": [
                            {"range": [0, 10],  "color": "#fee2e2"},
                            {"range": [10, 50], "color": "#fef9c3"},
                            {"range": [50, 85], "color": "#dcfce7"},
                            {"range": [85, 100],"color": "#bbf7d0"},
                        ],
                        "threshold": {"line": {"color": "red", "width": 3}, "value": 10},
                    },
                    title={"text": "Progress %"},
                ))
                fig_gauge.update_layout(height=280, margin=dict(t=30, b=10, l=10, r=10))
                st.plotly_chart(fig_gauge, use_container_width=True)

            with wa2:
                # Expenditure breakdown pie
                exp_labels = ["Wages Paid", "Material Paid", "Remaining Budget"]
                remaining = max(0, float(row["Sanctioned_Amount"]) - float(row["Total_Paid"]))
                exp_values = [float(row["Wages_Paid"]), float(row["Material_Paid"]), remaining]
                fig_exp = px.pie(
                    names=exp_labels, values=exp_values,
                    hole=0.4,
                    color_discrete_sequence=["#3b6fd4", "#43c59e", "#e2e8f0"],
                    title="Expenditure Breakdown",
                )
                fig_exp.update_layout(height=280, margin=dict(t=40, b=10))
                st.plotly_chart(fig_exp, use_container_width=True)

            # Compare with panchayat avg
            same_panchayat = df_filtered[df_filtered["Panchayat"] == row["Panchayat"]]
            avg_progress = same_panchayat["Progress_%"].mean()

            wa3, wa4 = st.columns(2)
            with wa3:
                # This work vs panchayat average bar
                fig_cmp = go.Figure()
                fig_cmp.add_trace(go.Bar(
                    x=["This Work", f"{row['Panchayat']} Avg"],
                    y=[progress, avg_progress],
                    marker_color=["#3b6fd4", "#94a3b8"],
                    text=[f"{progress:.1f}%", f"{avg_progress:.1f}%"],
                    textposition="outside",
                ))
                fig_cmp.update_layout(
                    title=f"Progress vs Panchayat Average",
                    yaxis_range=[0, max(progress, avg_progress) * 1.3 + 5],
                    margin=dict(t=40, b=10),
                    height=260,
                )
                st.plotly_chart(fig_cmp, use_container_width=True)

            with wa4:
                # Budget utilisation bar
                util_pct = min((float(row["Total_Paid"]) / float(row["Sanctioned_Amount"]) * 100)
                               if float(row["Sanctioned_Amount"]) > 0 else 0, 100)
                fig_util = go.Figure(go.Bar(
                    x=["Budget Utilisation"],
                    y=[util_pct],
                    marker_color="#43c59e" if util_pct >= 50 else "#f59e0b",
                    text=[f"{util_pct:.1f}%"],
                    textposition="outside",
                ))
                fig_util.update_layout(
                    title="Budget Utilisation %",
                    yaxis_range=[0, 120],
                    margin=dict(t=40, b=10),
                    height=260,
                )
                st.plotly_chart(fig_util, use_container_width=True)

        else:
            st.warning("Koi result nahi mila. Dusra keyword try karein.")
    else:
        st.caption("ℹ️ Upar search box mein Work Name ya Work Code ke kuch words type karein.")

    st.markdown("---")

    # ─────────────────────────────────────────────
    # Tabbed Detailed Reports – Professional Tables
    # ─────────────────────────────────────────────
    st.markdown("### 📋 Detailed Reports")

    tab_all, tab_zero, tab_low, tab_high, tab_old, tab_mat = st.tabs([
        "📄 All Schemes",
        "🔴 Zero Paid",
        "🟠 Low Progress (< 10%)",
        "✅ High Progress (> 85%)",
        "📆 Old Schemes",
        "🧱 Material Oriented",
    ])

    def styled_table(data: pd.DataFrame):
        if data.empty:
            st.info("Is category mein koi record nahi hai.")
            return
        st.caption(f"Total records: **{len(data)}**")
        money_cols = ["Sanctioned_Amount", "Wages_Paid", "Material_Paid", "Total_Paid"]
        fmt_dict = {c: "₹{:,.0f}" for c in money_cols if c in data.columns}
        if "Progress_%" in data.columns:
            fmt_dict["Progress_%"] = "{:.2f}%"
        st.dataframe(
            data.reset_index(drop=True).style
                .format(fmt_dict)
                .background_gradient(subset=["Progress_%"] if "Progress_%" in data.columns else [], cmap="RdYlGn"),
            use_container_width=True,
        )
        # Per-tab Excel download
        excel_tab = export_excel(data.reset_index(drop=True))
        st.download_button(
            "⬇️ Download this tab as Excel",
            data=excel_tab,
            file_name="report_export.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key=f"dl_{id(data)}",
        )

    with tab_all:
        styled_table(df_filtered)

    with tab_zero:
        styled_table(df_filtered[df_filtered["Total_Paid"] == 0])

    with tab_low:
        styled_table(df_filtered[(df_filtered["Progress_%"] > 0) & (df_filtered["Progress_%"] < 10)])

    with tab_high:
        styled_table(df_filtered[df_filtered["Progress_%"] > 85])

    with tab_old:
        recent_years = ["2023-2024", "2024-2025", "2025-2026", "2026-2027"]
        styled_table(df_filtered[~df_filtered["Fin_Year"].isin(recent_years)])

    with tab_mat:
        styled_table(df_filtered[df_filtered["Material_Paid"] > 0])

else:
    st.markdown("""
    <div style="text-align:center; padding: 60px 20px;">
        <h2 style="color:#3b6fd4;">📂 Upload your Excel / CSV file</h2>
        <p style="color:#6b7a99; font-size:1.1rem;">
            MGNREGA report upload karein — professional analytics instantly dikhega.<br>
            Supported formats: <strong>.xlsx</strong> &nbsp;|&nbsp; <strong>.csv</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)
