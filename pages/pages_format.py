from st_pages import Page, Section, add_indentation, show_pages


def pages_format():
    show_pages(
        [
            Page("streamlit_app.py", "Home", "🏠", in_section=False),
            Page("pages/data_read.py", "Reading data", "📖", in_section=False),
            Page("pages/polars_to_pandas.py", "Polars to pandas (and viceversa)", "🔄", in_section=False),
            # Section(name="Highlights", icon="⭐"),  # Non-clickable section
            # Page("pages/changes_at_market_and_silo_level.py", "Market and silo changes", "🌎"),  # Idented section
            # Page("pages/guardrails.py", "Guardrails", "🛡️"),  # Idented section
            # Page("pages/elasticities.py", "Elasticities", "🌀"),  # Idented section
        ]
    )
    add_indentation()   # Function that looks at the in_section parameter