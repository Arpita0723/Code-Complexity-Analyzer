import streamlit as st
import ast
import pandas as pd
import altair as alt
from analyzer import CodeAnalyzer

# ── Page config & header ─────────────────────────────────────────────────────
st.set_page_config(page_title="Code Complexity Analyzer", layout="centered")
st.title("🧠 Code Complexity Analyzer")
st.write(
    "Upload Python files to analyze their structure and estimate code complexity. "
    "Get tips to improve your code!"
)
st.markdown("---")

# ── File uploader ─────────────────────────────────────────────────────────────
st.markdown("### 📁 Upload Your Python Files")
uploaded_files = st.file_uploader(
    "Choose one or more `.py` files", type="py", accept_multiple_files=True
)

if not uploaded_files:
    st.info("⏳ Upload at least one Python file to begin analysis.")
    st.stop()

# ── Analyze each file ──────────────────────────────────────────────────────────
report_data = []

for file in uploaded_files:
    source = file.read().decode("utf-8")
    try:
        tree = ast.parse(source)
    except SyntaxError:
        st.error(f"❌ Syntax error in {file.name}, skipping")
        continue

    analyzer = CodeAnalyzer()
    analyzer.visit(tree)

    is_rec = bool(analyzer.recursive_functions)
    score = (
        analyzer.functions * 2
        + analyzer.loops * 3
        + analyzer.ifs * 2
        + analyzer.max_depth
        + (5 if is_rec else 0)
    )
    level = "Easy" if score <= 10 else "Medium" if score <= 20 else "Hard"
    tip = (
        "✅ Clean code! Keep it up."
        if score <= 10
        else "🧪 Moderate complexity; consider simplifying loops or conditions."
        if score <= 20
        else "⚠️ High complexity; consider refactoring or reducing recursion."
    )

    report_data.append({
        "Filename": file.name,
        "Functions": analyzer.functions,
        "Loops": analyzer.loops,
        "Ifs": analyzer.ifs,
        "Recursion": "Yes" if is_rec else "No",
        "Nesting Depth": analyzer.max_depth,
        "Score": score,
        "Difficulty": level,
        "Tip": tip
    })

# ── Build DataFrame & display ─────────────────────────────────────────────────
df = pd.DataFrame(report_data).sort_values("Score", ascending=False)

st.markdown("### 🧾 Code Complexity Report")
st.dataframe(df, use_container_width=True)

# ── CSV Download ───────────────────────────────────────────────────────────────
csv = df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="📥 Download CSV Report",
    data=csv,
    file_name="code_complexity_report.csv",
    mime="text/csv",
)
st.markdown("---")

# ── Bar Chart ─────────────────────────────────────────────────────────────────
st.markdown("### 📊 Score Comparison Chart")
chart = (
    alt.Chart(df)
    .mark_bar()
    .encode(
        x=alt.X("Filename", sort="-y"),
        y="Score",
        color=alt.Color("Difficulty", scale=alt.Scale(scheme="set2")),
        tooltip=["Filename", "Score", "Difficulty", "Tip"],
    )
    .properties(width=700, height=400)
)
st.altair_chart(chart, use_container_width=True)
