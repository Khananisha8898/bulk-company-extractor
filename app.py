import streamlit as st
import pandas as pd
import requests
from urllib.parse import quote
import re

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="Nexora AI",
    page_icon="🚀",
    layout="wide"
)

# =========================
# NEON FUTURISTIC UI
# =========================

st.markdown("""
<style>

/* MAIN BACKGROUND */
.stApp {
    background: linear-gradient(
        135deg,
        #020617,
        #0f172a,
        #111827
    );
    color: white;
}

/* TITLE */
.main-title {
    text-align: center;
    font-size: 65px;
    font-weight: bold;
    color: #38bdf8;

    text-shadow:
        0 0 10px #38bdf8,
        0 0 20px #38bdf8,
        0 0 40px #0ea5e9;

    margin-top: 20px;
}

.sub-title {
    text-align: center;
    color: #94a3b8;
    font-size: 20px;
    margin-bottom: 40px;
}

/* GLASS CARD */
.glass-card {

    background: rgba(255,255,255,0.05);

    border: 1px solid rgba(255,255,255,0.1);

    padding: 30px;

    border-radius: 25px;

    backdrop-filter: blur(10px);

    box-shadow:
        0 0 20px rgba(56,189,248,0.2);
}

/* BUTTON */
.stButton button {

    width: 100%;

    border-radius: 15px;

    border: none;

    padding: 14px;

    font-size: 18px;

    font-weight: bold;

    color: white;

    background: linear-gradient(
        90deg,
        #2563eb,
        #7c3aed
    );

    box-shadow:
        0 0 10px #2563eb,
        0 0 20px #7c3aed;

    transition: 0.3s;
}

.stButton button:hover {

    transform: scale(1.03);

    box-shadow:
        0 0 20px #38bdf8,
        0 0 40px #7c3aed;
}

/* FILE UPLOADER */
section[data-testid="stFileUploader"] {

    background: rgba(255,255,255,0.05);

    padding: 20px;

    border-radius: 20px;

    border: 1px solid rgba(255,255,255,0.1);

    box-shadow:
        0 0 20px rgba(56,189,248,0.15);
}

/* TABLE */
[data-testid="stDataFrame"] {

    border-radius: 20px;

    overflow: hidden;

    box-shadow:
        0 0 20px rgba(56,189,248,0.2);
}

/* SUCCESS */
.stSuccess {

    border-radius: 15px;

    box-shadow:
        0 0 20px rgba(34,197,94,0.4);
}

/* FOOTER */
.footer {

    text-align: center;

    margin-top: 50px;

    color: #94a3b8;

    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================

st.markdown("""
<div class="main-title">
 Nexora AI
</div>

<div class="sub-title">
Next Generation Bulk Company Intelligence Dashboard
</div>
""", unsafe_allow_html=True)

# GLASS CARD START
st.markdown(
    '<div class="glass-card">',
    unsafe_allow_html=True
)

# =========================
# INFO
# =========================



# =========================
# FILE UPLOAD
# =========================

uploaded_file = st.file_uploader(
    "📂 Upload CSV File",
    type=["csv"]
)

# =========================
# MAIN PROCESS
# =========================

if uploaded_file:

    # READ CSV
    df_input = pd.read_csv(uploaded_file)

    st.write("### 📄 Uploaded Companies")

    st.dataframe(df_input)

    # START BUTTON
    if st.button(" Start Extraction"):

        results = []

        progress = st.progress(0)

        # LOOP THROUGH COMPANIES
        for index, row in df_input.iterrows():

            company = str(row["company"])

            # DEFAULT VALUES
            overview = "Not Available"
            headquarters = "Not Available"
            industry = "Not Available"
            services = "Not Available"

            # SIMPLE WEBSITE GENERATION
            website = f"https://www.{company.lower().replace(' ', '')}.com"

            try:

                # =========================
                # SPECIAL COMPANY FIXES
                # =========================

                special_companies = {
                    "tcs": "Tata Consultancy Services",
                    "infosys": "Infosys",
                    "apple": "Apple Inc.",
                    "tesla": "Tesla, Inc.",
                    "microsoft": "Microsoft",
                    "google": "Google",
                    "youtube": "YouTube"
                }

                company_lower = company.lower()

                search_company = company

                if company_lower in special_companies:
                    search_company = special_companies[company_lower]

                # =========================
                # WIKIPEDIA SEARCH
                # =========================

                search_url = (
                    "https://en.wikipedia.org/w/api.php"
                    f"?action=query&list=search"
                    f"&srsearch={quote(search_company)}"
                    "&format=json"
                )

                search_response = requests.get(
                    search_url,
                    headers={"User-Agent": "Mozilla/5.0"}
                )

                search_data = search_response.json()

                # SEARCH RESULTS FOUND
                if len(search_data["query"]["search"]) > 0:

                    best_match = search_data["query"]["search"][0]["title"]

                    # SUMMARY API
                    summary_url = (
                        "https://en.wikipedia.org/api/rest_v1/page/summary/"
                        f"{quote(best_match)}"
                    )

                    summary_response = requests.get(
                        summary_url,
                        headers={"User-Agent": "Mozilla/5.0"}
                    )

                    summary_data = summary_response.json()

                    # OVERVIEW
                    if "extract" in summary_data:

                        overview = summary_data["extract"]

                        text = overview.lower()

                        # =========================
                        # HEADQUARTERS EXTRACTION
                        # =========================

                        patterns = [
                            r'headquartered in ([A-Za-z,\s]+)',
                            r'based in ([A-Za-z,\s]+)',
                            r'located in ([A-Za-z,\s]+)'
                        ]

                        for pattern in patterns:

                            match = re.search(
                                pattern,
                                overview,
                                re.IGNORECASE
                            )

                            if match:

                                headquarters = match.group(1).strip()

                                headquarters = headquarters.split(".")[0]

                                headquarters = headquarters.split(" and ")[0]

                                break

                        # =========================
                        # INDUSTRY DETECTION
                        # =========================

                        if "technology" in text:
                            industry = "Technology"

                        elif "software" in text:
                            industry = "Software"

                        elif "automotive" in text:
                            industry = "Automotive"

                        elif "e-commerce" in text:
                            industry = "E-Commerce"

                        elif "bank" in text:
                            industry = "Banking"

                        elif "artificial intelligence" in text:
                            industry = "Artificial Intelligence"

                        # =========================
                        # SERVICES DETECTION
                        # =========================

                        service_keywords = [
                            "software",
                            "cloud",
                            "AI",
                            "technology",
                            "consulting",
                            "e-commerce",
                            "banking",
                            "automotive",
                            "analytics",
                            "data",
                            "cybersecurity",
                            "electric vehicles",
                            "search engine",
                            "consumer electronics"
                        ]

                        found_services = []

                        for keyword in service_keywords:

                            if keyword.lower() in text:
                                found_services.append(keyword)

                        if len(found_services) > 0:

                            services = ", ".join(found_services)

            except Exception:
                pass

            # SAVE RESULT
            results.append({
                "Company Name": company,
                "Overview": overview,
                "Headquarters": headquarters,
                "Industry": industry,
                "Products & Services": services,
                "Official Website": website
            })

            # UPDATE PROGRESS
            progress.progress(
                (index + 1) / len(df_input)
            )

        # FINAL DATAFRAME
        result_df = pd.DataFrame(results)

        st.success("✅ Extraction Completed Successfully")

        # SHOW DATA
        st.write("## 📊 Extracted Company Data")

        st.dataframe(
            result_df,
            use_container_width=True
        )

        # CSV EXPORT
        csv = result_df.to_csv(index=False)

        st.download_button(
            label="⬇ Download Final CSV",
            data=csv,
            file_name="bulk_company_data.csv",
            mime="text/csv"
        )

        # RAW CSV VIEW
        with st.expander("👀 View Raw CSV Data"):

            st.code(csv, language="csv")

# GLASS CARD END
st.markdown(
    "</div>",
    unsafe_allow_html=True
)

# FOOTER
st.markdown("""
<div class="footer">
⚡ Powered by Nexora AI
</div>
""", unsafe_allow_html=True)