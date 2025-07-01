import streamlit as st
import ast
from analyzer import CodeAnalyzer
import pandas as pd
import altair as alt

st.set_page_config(page_title="Code Complexity Analyzer", layout="centered")
st.write("Upload Python files to analyze their structure and estimate code complexity. Get tips to improve your code!")
st.title("🧠 Code Complexity Analyzer")
st.markdown("Upload your Python `.py` files to analyze their complexity.")

# Upload Python files
uploaded_files = st.file_uploader("📁 Upload one or more Python files", type="py", accept_multiple_files=True)

if uploaded_files:
    st.success(f"{len(uploaded_files)} file(s) uploaded successfully.")

    report_data = []

    for file in uploaded_files:
        source_code = file.read().decode("utf-8")  # Read and decode the file
        try:
            tree = ast.parse(source_code)  # Convert to AST (code tree)
        except SyntaxError:
            st.error(f"❌ Syntax error in file: {file.name}")
            continue

        analyzer = CodeAnalyzer()         # Create analyzer object
        analyzer.visit(tree)              # Analyze the AST

        is_recursive = bool(analyzer.recursive_functions)

        score = (
            analyzer.functions * 2 +
            analyzer.loops * 3 +
            analyzer.ifs * 2 +
            analyzer.max_depth * 1 +
            (5 if is_recursive else 0)
        )

        level = (
            "Easy" if score <= 10 else
            "Medium" if score <= 20 else
            "Hard"
        )

        report_data.append({
            "Filename": file.name,
            "Functions": analyzer.functions,
            "Loops": analyzer.loops,
            "Ifs": analyzer.ifs,
            "Recursion": "Yes" if is_recursive else "No",
            "Nesting Depth": analyzer.max_depth,
            "Score": score,
            "Difficulty": level
        })

    # Show table
    df = pd.DataFrame(report_data)
    st.subheader("📊 Code Complexity Report")
    st.dataframe(df)
    df = df.sort_values("Score", ascending=False)

    st.markdown("### 🧾 Code Complexity Report")
    st.dataframe(df)

# Bar Chart
    st.markdown("### 📊 Visual Complexity Chart")
    st.subheader("📈 Score Comparison Chart")
    st.markdown("### 📥 Download Report")
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('Filename', sort='-y'),
        y='Score',
        color=alt.Color('Difficulty', scale=alt.Scale(scheme='set2')),
        tooltip=['Filename', 'Score', 'Difficulty']
    ).properties(
        width=700,
        height=400
    )

    st.altair_chart(chart, use_container_width=True)
    csv = df.to_csv(index=False).encode('utf-8')

    st.download_button(
        label="📥 Download CSV Report",
        data=csv,
        file_name='code_complexity_report.csv',
        mime='text/csv')
    
else:
    st.info("⏳ Upload at least one Python file to begin analysis.")
