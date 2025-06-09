import streamlit as st

# Define the pages
main_page = st.Page("pages/home_page.py", title="Home Page", icon="🏠")
page_2 = st.Page("pages/window_metrics.py", title="Aggregate Window Correlations", icon="🧮")
page_3 = st.Page("pages/two_stock_correlations.py", title="Two Stock Correlations", icon="🟰")
page_4 = st.Page("pages/readme_page.py", title="README", icon="📚")

# Set up navigation
pg = st.navigation([main_page, page_2, page_3, page_4])

# Run the selected page
pg.run()