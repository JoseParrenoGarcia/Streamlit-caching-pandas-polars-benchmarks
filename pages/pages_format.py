from st_pages import Page, Section, add_indentation, show_pages


def pages_format():
    show_pages(
        [
            Page("streamlit_app.py", "Home", "🏠", in_section=False),
            Page("pages/speed_comparisons.py", "Speed comparisons", "🕒", in_section=False)

        ]
    )
    add_indentation()   # Function that looks at the in_section parameter
