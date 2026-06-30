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
/* Force light theme regardless of system/deployment settings */
html, body, [class*="css"] { color-scheme: light !important; }

/* General background - Light Theme */
[data-testid="stAppViewContainer"] { background: #f5f7fa !important; }
[data-testid="stHeader"] { background: #f5f7fa !important; }
[data-testid="stMainBlockContainer"] { background: #f5f7fa !important; }
[data-testid="stMain"] { background: #f5f7fa !important; }
.main .block-container { background: #f5f7fa !important; }

/* Main area default text color */
[data-testid="stAppViewContainer"] p,
[data-testid="stAppViewContainer"] span:not([data-testid="stSidebar"] span),
[data-testid="stAppViewContainer"] div { color: #1e293b; }

[data-testid="stSidebar"] { background: linear-gradient(180deg, #1e3a8a 0%, #1e40af 100%) !important; }

/* Sidebar – headings, plain text, labels → white */
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] h4,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stMarkdown { color: #ffffff !important; }

/* Sidebar filter labels uppercase */
[data-testid="stSidebar"] label {
    font-size: 0.78rem !important;
    font-weight: 700 !important;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #dbeafe !important;
}

/* Selectbox & multiselect input box – white background, dark text */
[data-testid="stSidebar"] [data-baseweb="select"] > div,
[data-testid="stSidebar"] [data-baseweb="select"] input {
    background-color: #ffffff !important;
    color: #1e293b !important;
    border-radius: 8px !important;
    border: none !important;
}

/* The currently selected value inside selectbox */
[data-testid="stSidebar"] [data-baseweb="select"] [data-testid="stMarkdownContainer"] p,
[data-testid="stSidebar"] [data-baseweb="select"] span,
[data-testid="stSidebar"] [data-baseweb="select"] div[class*="placeholder"],
[data-testid="stSidebar"] [data-baseweb="select"] div[class*="singleValue"] {
    color: #1e293b !important;
}

/* Multiselect tags (selected items chips) */
[data-testid="stSidebar"] [data-baseweb="tag"] {
    background-color: #dbeafe !important;
    border-radius: 6px !important;
}
[data-testid="stSidebar"] [data-baseweb="tag"] span {
    color: #1e3a8a !important;
    font-weight: 600 !important;
}
[data-testid="stSidebar"] [data-baseweb="tag"] svg {
    fill: #1e3a8a !important;
}

/* Dropdown arrow icon */
[data-testid="stSidebar"] [data-baseweb="select"] svg { fill: #1e293b !important; }

/* Metric cards */
div[data-testid="metric-container"] {
    background: white;
    border-radius: 12px;
    padding: 16px 20px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    border-left: 4px solid #1e40af;
}
div[data-testid="metric-container"] label { color: #64748b !important; font-size: 0.78rem !important; font-weight: 600 !important; text-transform: uppercase; letter-spacing: 0.05em; }
div[data-testid="metric-container"] div[data-testid="stMetricValue"] { color: #1e3a8a !important; font-size: 1.8rem !important; font-weight: 700 !important; }

/* Tab styling */
button[data-baseweb="tab"] { font-weight: 600; font-size: 0.82rem; }

/* Section headings */
h3 { color: #1e3a8a !important; }
h4 { color: #1e40af !important; }

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
    background: linear-gradient(135deg, #1e3a8a, #1e40af);
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
    st.markdown(
        '<h2 style="color:#1e3a8a;">📊 MGNREGA Schemes & Works Dashboard</h2>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p style="color:#64748b; margin-top:-10px;">Upload your Excel / CSV report to generate professional, dynamic insights instantly.</p>',
        unsafe_allow_html=True,
    )
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
    # Add S.No. column
    df_export = dataframe.reset_index(drop=True).copy()
    df_export.insert(0, "S.No.", range(1, len(df_export) + 1))

    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df_export.to_excel(writer, index=False, sheet_name=sheet_name)
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
        sno_fmt = workbook.add_format({"border": 1, "align": "center", "font_size": 9, "bold": True})
        sno_alt_fmt = workbook.add_format({"border": 1, "align": "center", "font_size": 9, "bold": True, "bg_color": "#f0f4ff"})

        # Column widths
        col_widths = {
            "S.No.": 6,
            "Work_Code": 18, "Panchayat": 20, "Work_Name": 40, "Work_Type": 22,
            "Fin_Year": 12, "Work_Status": 15, "Sanctioned_Amount": 18,
            "Wages_Paid": 15, "Material_Paid": 15, "Total_Paid": 15, "Progress_%": 14
        }
        for i, col in enumerate(df_export.columns):
            w = col_widths.get(col, 16)
            worksheet.set_column(i, i, w)

        # Header row
        for col_num, col_name in enumerate(df_export.columns):
            worksheet.write(0, col_num, col_name, header_fmt)
        worksheet.set_row(0, 22)

        # Data rows with alternating colour
        money_cols = {"Sanctioned_Amount", "Wages_Paid", "Material_Paid", "Total_Paid"}
        pct_cols = {"Progress_%"}
        col_list = list(df_export.columns)
        for row_num, row in enumerate(df_export.itertuples(index=False), start=1):
            is_alt = row_num % 2 == 0
            for col_num, col_name in enumerate(col_list):
                val = row[col_num]
                if col_name == "S.No.":
                    worksheet.write_number(row_num, col_num, int(val), sno_alt_fmt if is_alt else sno_fmt)
                elif col_name in money_cols:
                    worksheet.write_number(row_num, col_num, float(val), num_fmt)
                elif col_name in pct_cols:
                    worksheet.write_number(row_num, col_num, float(val), pct_fmt)
                else:
                    worksheet.write(row_num, col_num, str(val), alt_fmt if is_alt else text_fmt)

        # Freeze pane & autofilter
        worksheet.freeze_panes(1, 0)
        worksheet.autofilter(0, 0, len(df_export), len(df_export.columns) - 1)

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

    all_panchayats = sorted(df["Panchayat"].unique().tolist())
    selected_panchayat = st.sidebar.multiselect(
        "Panchayat (multiple select kar sakte ho)",
        options=all_panchayats,
        default=[],
        placeholder="All Panchayats",
    )

    selected_work_type = st.sidebar.selectbox(
        "Work Type / Scheme", ["All"] + sorted(df["Work_Type"].unique().tolist())
    )

    all_fin_years = sorted(df["Fin_Year"].unique().tolist(), reverse=True)
    selected_fin_year = st.sidebar.multiselect(
        "Financial Year (multiple select kar sakte ho)",
        options=all_fin_years,
        default=[],
        placeholder="All Financial Years",
    )

    selected_status = st.sidebar.selectbox(
        "Work Status", ["All"] + sorted(df["Work_Status"].unique().tolist())
    )

    df_filtered = df.copy()
    if selected_panchayat:  # list non-empty means filter applied
        df_filtered = df_filtered[df_filtered["Panchayat"].isin(selected_panchayat)]
    if selected_work_type != "All":
        df_filtered = df_filtered[df_filtered["Work_Type"] == selected_work_type]
    if selected_fin_year:  # list non-empty means filter applied
        df_filtered = df_filtered[df_filtered["Fin_Year"].isin(selected_fin_year)]
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
            fig_pie.update_traces(
                texttemplate="<b>%{label}</b><br>%{value} works<br>(%{percent})",
                textposition="outside",
                hovertemplate="<b>%{label}</b><br>Count: %{value}<br>Share: %{percent}<extra></extra>",
            )
            fig_pie.update_layout(margin=dict(t=10, b=10), legend_font_size=11, showlegend=True)
            st.plotly_chart(fig_pie, width='stretch')
        elif len(wc) == 1:
            st.info(f"Only one type: **{wc['Work_Type'].values[0]}**")
        else:
            st.info("No data available for selected filters.")

    with cc2:
        st.markdown("#### 📅 Schemes by Financial Year")
        fy = df_filtered["Fin_Year"].value_counts().reset_index().sort_values("Fin_Year")
        fy.columns = ["Fin_Year", "Count"]
        if not fy.empty:
            fig_bar = px.bar(
                fy, x="Fin_Year", y="Count", text="Count",
                color="Fin_Year", color_discrete_sequence=px.colors.sequential.Blues_r,
            )
            fig_bar.update_layout(showlegend=False, margin=dict(t=10, b=10))
            st.plotly_chart(fig_bar, width='stretch')
        else:
            st.info("No data for selected filters.")

    # ── Charts Row 2 ─────────────────────────────────────────
    cc3, cc4 = st.columns(2)
    with cc3:
        st.markdown("#### 📍 Panchayat-wise Works Count")
        pw = df_filtered.groupby("Panchayat").size().reset_index(name="Count").sort_values("Count", ascending=True)
        if not pw.empty:
            fig_pwh = px.bar(
                pw, x="Count", y="Panchayat", orientation="h", text="Count",
                color="Count", color_continuous_scale="Blues",
            )
            fig_pwh.update_layout(margin=dict(t=10, b=10), coloraxis_showscale=False)
            st.plotly_chart(fig_pwh, width='stretch')
        else:
            st.info("No data for selected filters.")

    with cc4:
        st.markdown("#### 💰 Sanctioned vs Paid Amount (by Panchayat)")
        amt = df_filtered.groupby("Panchayat").agg(
            Sanctioned=("Sanctioned_Amount", "sum"),
            Paid=("Total_Paid", "sum")
        ).reset_index()
        if not amt.empty:
            fig_amt = go.Figure()
            fig_amt.add_trace(go.Bar(name="Sanctioned", x=amt["Panchayat"], y=amt["Sanctioned"], marker_color="#3b6fd4"))
            fig_amt.add_trace(go.Bar(name="Paid", x=amt["Panchayat"], y=amt["Paid"], marker_color="#43c59e"))
            fig_amt.update_layout(barmode="group", margin=dict(t=10, b=10), legend_font_size=11)
            st.plotly_chart(fig_amt, width='stretch')
        else:
            st.info("No data for selected filters.")

    # ── Progress Distribution ─────────────────────────────────
    st.markdown("#### 🎯 Progress % Distribution Across Works")
    if not df_filtered.empty:
        fig_hist = px.histogram(
            df_filtered, x="Progress_%", nbins=20,
            color_discrete_sequence=["#3b6fd4"],
            labels={"Progress_%": "Progress (%)"},
        )
        fig_hist.update_layout(margin=dict(t=10, b=10))
        st.plotly_chart(fig_hist, width='stretch')
    else:
        st.info("No data for selected filters.")

    st.markdown("---")

    # ═══════════════════════════════════════════════════════════
    # 🔍 SEARCH SECTION – Work Name / Work Code
    # ═══════════════════════════════════════════════════════════
    st.markdown("### 🔎 Search Works — by Work Name or Work Code")

    search_query = st.text_input(
        "Search Works", placeholder="Type work name or work code (partial search works)...",
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
                width='stretch',
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

            # ── Mandays & Material Calculations ───────────────────
            RATE_PER_MANDAY          = 282   # ₹ per manday (wage rate)
            DAYS_PER_WEEK            = 6     # MR generated for 6 days
            MAX_LABOUR_PER_WK        = 15    # max 15 labour per yojana per week
            wage_per_week_per_labour = RATE_PER_MANDAY * DAYS_PER_WEEK  # ₹1,692

            sanctioned    = float(row["Sanctioned_Amount"])
            wages_paid    = float(row["Wages_Paid"])
            material_paid = float(row["Material_Paid"])
            total_paid    = float(row["Total_Paid"])
            remaining     = max(0.0, sanctioned - total_paid)

            # ── Wages calculations ─────────────────────────────
            wages_budget_total     = sanctioned * 0.60           # ~60% of sanctioned is wages
            budget_for_wages_remaining = max(0.0, wages_budget_total - wages_paid)
            total_remaining_mandays    = int(budget_for_wages_remaining / RATE_PER_MANDAY) if budget_for_wages_remaining > 0 else 0

            cost_1wk_max = MAX_LABOUR_PER_WK * wage_per_week_per_labour  # 15×1692 = ₹25,380
            if budget_for_wages_remaining >= cost_1wk_max:
                feasible_labour_this_week = MAX_LABOUR_PER_WK
            elif budget_for_wages_remaining >= wage_per_week_per_labour:
                feasible_labour_this_week = int(budget_for_wages_remaining / wage_per_week_per_labour)
            else:
                feasible_labour_this_week = 0

            # ── Material calculations ──────────────────────────
            material_budget_total     = sanctioned * 0.40        # ~40% of sanctioned is material
            material_remaining        = max(0.0, material_budget_total - material_paid)
            material_utilisation_pct  = (material_paid / material_budget_total * 100) if material_budget_total > 0 else 0
            has_material              = material_paid > 0 or material_budget_total > 0

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

            # ── Mandays & Labour Demand Card ───────────────────
            st.markdown("""
            <style>
            .manday-card {
                background: linear-gradient(135deg, #eef4ff 0%, #f0fdf4 100%);
                border-radius: 14px;
                padding: 22px 28px;
                box-shadow: 0 4px 16px rgba(59,111,212,0.10);
                border-top: 4px solid #16a34a;
                margin-bottom: 20px;
            }
            .manday-card h4 { color: #14532d; margin-bottom: 6px; font-size: 1.05rem; }
            .manday-card .note { color: #6b7a99; font-size: 0.82rem; margin-bottom: 14px; }
            .material-card {
                background: linear-gradient(135deg, #fff7ed 0%, #fef3c7 100%);
                border-radius: 14px;
                padding: 22px 28px;
                box-shadow: 0 4px 16px rgba(234,179,8,0.10);
                border-top: 4px solid #d97706;
                margin-bottom: 20px;
            }
            .material-card h4 { color: #92400e; margin-bottom: 6px; font-size: 1.05rem; }
            .material-card .note { color: #6b7a99; font-size: 0.82rem; margin-bottom: 14px; }
            .md-row { display: flex; gap: 20px; flex-wrap: wrap; margin-bottom: 14px; }
            .md-box { flex: 1; min-width: 130px; background: white; border-radius: 10px;
                      padding: 12px 14px; text-align: center;
                      box-shadow: 0 1px 4px rgba(0,0,0,0.07); }
            .md-box .mval { font-size: 1.25rem; font-weight: 700; color: #1e40af; }
            .md-box .mlbl { font-size: 0.70rem; color: #8898aa; text-transform: uppercase;
                            letter-spacing: .05em; margin-top: 2px; }
            .md-box-amber .mval { font-size: 1.25rem; font-weight: 700; color: #b45309; }
            .warn-box { background: #fefce8; border-left: 4px solid #eab308;
                        border-radius: 8px; padding: 10px 14px; font-size: 0.83rem;
                        color: #713f12; margin-top: 10px; }
            .ok-box   { background: #f0fdf4; border-left: 4px solid #16a34a;
                        border-radius: 8px; padding: 10px 14px; font-size: 0.83rem;
                        color: #14532d; margin-top: 10px; }
            .info-box  { background: #eff6ff; border-left: 4px solid #3b82f6;
                        border-radius: 8px; padding: 10px 14px; font-size: 0.83rem;
                        color: #1e3a8a; margin-top: 10px; }
            </style>
            """, unsafe_allow_html=True)

            # ── Labour status message ──────────────────────────
            if feasible_labour_this_week == 0:
                status_box = '<div class="warn-box">⚠️ <strong>Wages budget exhausted</strong> — Is yojana mein is hafte labour demand nahi kiya ja sakta. Sanctioned amount review karein.</div>'
            elif feasible_labour_this_week < MAX_LABOUR_PER_WK:
                status_box = f'<div class="warn-box">⚠️ <strong>Partial demand possible</strong> — Remaining wages budget ke hisab se sirf <strong>{feasible_labour_this_week} labour</strong> hi is hafte demand kiye ja sakte hain (max 15 se kam).</div>'
            else:
                status_box = f'<div class="ok-box">✅ <strong>Full demand possible</strong> — Is hafte <strong>15 labour (max cap)</strong> demand kiye ja sakte hain.</div>'

            # ── Wages Card ─────────────────────────────────────
            st.markdown(f"""
            <div class="manday-card">
                <h4>👷 Mandays &amp; Labour Demand Analysis</h4>
                <div class="note">
                    Wage Rate: ₹282/manday &nbsp;|&nbsp; MR: 6 days/week &nbsp;|&nbsp;
                    1 labour/week = 6 × ₹282 = <strong>₹1,692</strong> &nbsp;|&nbsp;
                    Max labour per yojana/week = <strong>15</strong>
                </div>
                <div class="md-row">
                    <div class="md-box">
                        <div class="mval">{fmt_inr(wages_budget_total)}</div>
                        <div class="mlbl">Total Wages Budget<br><span style="font-size:0.65rem;">(~60% of Sanctioned)</span></div>
                    </div>
                    <div class="md-box">
                        <div class="mval">{fmt_inr(wages_paid)}</div>
                        <div class="mlbl">Wages Paid So Far</div>
                    </div>
                    <div class="md-box">
                        <div class="mval">{fmt_inr(budget_for_wages_remaining)}</div>
                        <div class="mlbl">Wages Budget Left</div>
                    </div>
                    <div class="md-box">
                        <div class="mval">{total_remaining_mandays:,}</div>
                        <div class="mlbl">Remaining Mandays<br><span style="font-size:0.65rem;">(Wages Left ÷ ₹282)</span></div>
                    </div>
                    <div class="md-box">
                        <div class="mval">{feasible_labour_this_week}</div>
                        <div class="mlbl">Labour Demand This Week<br><span style="font-size:0.65rem;">(Max cap: 15)</span></div>
                    </div>
                </div>
                {status_box}
            </div>
            """, unsafe_allow_html=True)

            # ── Material Card (only if material is applicable) ──
            if has_material:
                if material_remaining <= 0:
                    mat_status = '<div class="warn-box">⚠️ <strong>Material budget exhausted</strong> — Material ka poora budget kharach ho chuka hai.</div>'
                elif material_utilisation_pct < 10:
                    mat_status = f'<div class="warn-box">⚠️ <strong>Material barely started</strong> — Sirf {material_utilisation_pct:.1f}% material budget use hua hai. Kaam shuru karna hoga.</div>'
                elif material_utilisation_pct >= 85:
                    mat_status = f'<div class="ok-box">✅ <strong>Material near completion</strong> — {material_utilisation_pct:.1f}% material budget utilize ho gaya hai.</div>'
                else:
                    mat_status = f'<div class="info-box">🧱 Material kaam chal raha hai — {material_utilisation_pct:.1f}% utilize hua, {fmt_inr(material_remaining)} abhi baaki hai.</div>'

                st.markdown(f"""
                <div class="material-card">
                    <h4>🧱 Material Budget Analysis</h4>
                    <div class="note">
                        Material component = ~40% of Sanctioned Amount &nbsp;|&nbsp;
                        Jis yojana mein material nahi hota wahan ye section relevant nahi hoga
                    </div>
                    <div class="md-row">
                        <div class="md-box">
                            <div class="mval" style="color:#b45309;">{fmt_inr(material_budget_total)}</div>
                            <div class="mlbl">Total Material Budget<br><span style="font-size:0.65rem;">(~40% of Sanctioned)</span></div>
                        </div>
                        <div class="md-box">
                            <div class="mval" style="color:#b45309;">{fmt_inr(material_paid)}</div>
                            <div class="mlbl">Material Paid So Far</div>
                        </div>
                        <div class="md-box">
                            <div class="mval" style="color:#b45309;">{fmt_inr(material_remaining)}</div>
                            <div class="mlbl">Material Budget Left</div>
                        </div>
                        <div class="md-box">
                            <div class="mval" style="color:#b45309;">{material_utilisation_pct:.1f}%</div>
                            <div class="mlbl">Material Utilisation</div>
                        </div>
                    </div>
                    {mat_status}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="background:#f8fafc; border-radius:10px; padding:12px 18px;
                            border-left:4px solid #cbd5e1; margin-bottom:16px; color:#64748b; font-size:0.85rem;">
                    🧱 <strong>Material N/A</strong> — Is yojana mein abhi tak koi material expenditure nahi hua hai.
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
                st.plotly_chart(fig_gauge, width='stretch')

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
                st.plotly_chart(fig_exp, width='stretch')

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
                st.plotly_chart(fig_cmp, width='stretch')

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
                st.plotly_chart(fig_util, width='stretch')

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

    def styled_table(data: pd.DataFrame, tab_key: str):
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
            width='stretch',
        )
        # Per-tab Excel download
        excel_tab = export_excel(data.reset_index(drop=True))
        st.download_button(
            "⬇️ Download this tab as Excel",
            data=excel_tab,
            file_name=f"report_{tab_key}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key=f"dl_{tab_key}",
        )

    with tab_all:
        styled_table(df_filtered, "all")

    with tab_zero:
        styled_table(df_filtered[df_filtered["Total_Paid"] == 0], "zero_paid")

    with tab_low:
        styled_table(df_filtered[(df_filtered["Progress_%"] > 0) & (df_filtered["Progress_%"] < 10)], "low_progress")

    with tab_high:
        styled_table(df_filtered[df_filtered["Progress_%"] > 85], "high_progress")

    with tab_old:
        recent_years = ["2023-2024", "2024-2025", "2025-2026", "2026-2027"]
        styled_table(df_filtered[~df_filtered["Fin_Year"].isin(recent_years)], "old_schemes")

    with tab_mat:
        styled_table(df_filtered[df_filtered["Material_Paid"] > 0], "material")

else:
    st.markdown("""
    <div style="text-align:center; padding: 60px 20px;">
        <h2 style="color:#3b6fd4 !important;">📂 Upload your Excel / CSV file</h2>
        <p style="color:#6b7a99 !important; font-size:1.1rem;">
            MGNREGA report upload karein — professional analytics instantly dikhega.<br>
            Supported formats: <strong>.xlsx</strong> &nbsp;|&nbsp; <strong>.csv</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)
