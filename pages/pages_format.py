from st_pages import Page, Section, add_indentation, show_pages


def pages_format():
    show_pages(
        [
            Page("streamlit_app.py", "Home", "🏠", in_section=False),
            Page("pages/data_read.py", "Reading data", "📖", in_section=False),
            Page("pages/filtering_operations.py", "Filtering data", "✂️", in_section=False),
            Page("pages/aggregation_operations.py", "Aggregating data", "📦", in_section=False),
            Page("pages/join_operations.py", "Joining data", "🤝", in_section=False),
            Page("pages/polars_to_pandas.py", "Polars to pandas (and viceversa)", "🔄", in_section=False),
            Page("pages/functools_operations.py", "Functools specific", "🛠️", in_section=False),

        ]
    )
    add_indentation()   # Function that looks at the in_section parameter
