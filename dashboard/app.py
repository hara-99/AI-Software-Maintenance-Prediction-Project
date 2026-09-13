import os
import sys
import json

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

if PROJECT_ROOT not in sys.path:

    sys.path.insert(
        0,
        PROJECT_ROOT
    )


import streamlit as st

from project_analyzer.zip_handler import extract_project
from project_analyzer.file_scanner import scan_files
from project_analyzer.language_detector import detect_languages
from project_analyzer.feature_extractor import extract_project_features
from project_analyzer.hotspot_detector import detect_hotspots
from project_analyzer.dependency_analyzer import analyze_dependencies

from prediction.effort_prediction import predict_effort
from prediction.cost_estimation import estimate_cost
from prediction.risk_scoring import calculate_risk
from prediction.uncertainty_analysis import estimate_uncertainty

from anomaly.anomaly_detector import detect_anomaly

from gemini.code_analyzer import analyze_project_with_gemini
from gemini.maintenance_recommender import (
    generate_maintenance_recommendations
)

from reports.report_generator import generate_all_reports


st.set_page_config(
    page_title="AI Software Maintenance",
    page_icon="🤖",
    layout="wide"
)


st.title(
    "🤖 AI-Based Intelligent Multi-Language "
    "Software Maintenance Prediction"
)

st.write(
    "Upload a project ZIP file. "
    "The complete maintenance analysis will be "
    "performed automatically using Machine Learning "
    "and Gemini 3.5 Flash."
)


uploaded_file = st.file_uploader(
    "Upload Project ZIP",
    type=["zip"]
)


if uploaded_file:

    if st.button(
        "🚀 Analyze Project Automatically",
        type="primary"
    ):

        try:

            # =====================================================
            # 1. SAVE ZIP
            # =====================================================

            uploaded_directory = os.path.join(
                PROJECT_ROOT,
                "uploaded_projects"
            )

            os.makedirs(
                uploaded_directory,
                exist_ok=True
            )

            zip_path = os.path.join(
                uploaded_directory,
                uploaded_file.name
            )

            with open(
                zip_path,
                "wb"
            ) as file:

                file.write(
                    uploaded_file.getbuffer()
                )


            # =====================================================
            # 2. EXTRACT PROJECT
            # =====================================================

            st.info(
                "Extracting project..."
            )

            project_path = extract_project(
                zip_path,
                os.path.join(
                    uploaded_directory,
                    "extracted"
                )
            )


            # =====================================================
            # 3. SCAN PROJECT
            # =====================================================

            st.info(
                "Scanning source files..."
            )

            files = scan_files(
                project_path
            )


            # =====================================================
            # 4. DETECT LANGUAGES
            # =====================================================

            st.info(
                "Detecting programming languages..."
            )

            languages = detect_languages(
                files
            )


            # =====================================================
            # 5. AUTOMATIC PROJECT FEATURES
            # =====================================================

            st.info(
                "Calculating software metrics..."
            )

            project_features = (
                extract_project_features(
                    files
                )
            )


            # =====================================================
            # 6. HOTSPOT DETECTION
            # =====================================================

            hotspots = detect_hotspots(
                project_features[
                    "file_metrics"
                ]
            )


            # =====================================================
            # 7. DEPENDENCY ANALYSIS
            # =====================================================

            dependencies = (
                analyze_dependencies(
                    project_path
                )
            )


            # =====================================================
            # 8. AUTOMATIC ML FEATURE GENERATION
            # =====================================================

            ml_features = (
                project_features[
                    "dataset_features"
                ]
            )


            # =====================================================
            # 9. MAINTENANCE EFFORT PREDICTION
            # =====================================================

            st.info(
                "Running trained ML maintenance model..."
            )

            effort = predict_effort(
                ml_features
            )


            # =====================================================
            # 10. COST
            # =====================================================

            cost = estimate_cost(
                effort
            )


            # =====================================================
            # 11. RISK
            # =====================================================

            risk = calculate_risk(
                effort
            )


            # =====================================================
            # 12. UNCERTAINTY
            # =====================================================

            uncertainty = (
                estimate_uncertainty(
                    effort
                )
            )


            # =====================================================
            # 13. GEMINI AI ANALYSIS
            # =====================================================

            st.info(
                "Gemini 3.5 Flash is analyzing the source code..."
            )


            source_files = []

            for file_path in files:

                extension = os.path.splitext(
                    file_path
                )[1].lower()

                if extension not in [
                    ".py",
                    ".java",
                    ".js",
                    ".jsx",
                    ".ts",
                    ".tsx",
                    ".c",
                    ".h",
                    ".cpp",
                    ".hpp",
                    ".cc",
                    ".cxx",
                    ".cs",
                    ".php"
                ]:

                    continue

                try:

                    with open(
                        file_path,
                        "r",
                        encoding="utf-8",
                        errors="ignore"
                    ) as source_file:

                        content = (
                            source_file.read()
                        )

                    source_files.append(
                        (
                            os.path.relpath(
                                file_path,
                                project_path
                            ),
                            content
                        )
                    )

                except Exception:

                    continue


            gemini_analysis = (
                analyze_project_with_gemini(
                    source_files,
                    project_features,
                    languages
                )
            )


            # =====================================================
            # 14. GEMINI MAINTENANCE RECOMMENDATIONS
            # =====================================================

            ai_recommendations = (
                generate_maintenance_recommendations(
                    project_features,
                    effort,
                    risk,
                    gemini_analysis.get(
                        "errors",
                        []
                    )
                )
            )


            # =====================================================
            # 15. ANOMALY DETECTION
            # =====================================================

            anomaly_values = [
                ml_features[
                    feature
                ]
                for feature in [
                    "N_effort",
                    "Enquiry",
                    "Interface",
                    "File",
                    "Input",
                    "AFP",
                    "Added",
                    "Duration",
                    "PDR_AFP",
                    "Output"
                ]
            ]

            anomaly = detect_anomaly(
                anomaly_values
            )


            # =====================================================
            # SAVE RESULTS
            # =====================================================

            results_directory = os.path.join(
                PROJECT_ROOT,
                "analysis_results"
            )

            os.makedirs(
                results_directory,
                exist_ok=True
            )


            report_data = {

                "Project":
                    uploaded_file.name,

                "Languages":
                    languages,

                "Project Metrics":
                    project_features,

                "Automatic ML Features":
                    ml_features,

                "Predicted Effort":
                    effort,

                "Estimated Cost":
                    cost,

                "Risk":
                    risk,

                "Prediction Range":
                    uncertainty,

                "Maintenance Hotspots":
                    hotspots[:20],

                "Dependencies":
                    dependencies,

                "Gemini AI Analysis":
                    gemini_analysis,

                "AI Maintenance Recommendations":
                    ai_recommendations,

                "Anomaly Detection":
                    anomaly
            }


            json_path = os.path.join(
                results_directory,
                "latest_analysis.json"
            )

            with open(
                json_path,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    report_data,
                    file,
                    indent=4,
                    default=str
                )


            # =====================================================
            # DASHBOARD
            # =====================================================

            st.success(
                "✅ Complete AI maintenance analysis finished."
            )


            # =====================================================
            # PROJECT OVERVIEW
            # =====================================================

            st.header(
                "📊 Project Overview"
            )

            col1, col2, col3, col4 = (
                st.columns(4)
            )

            col1.metric(
                "Files",
                project_features[
                    "total_files"
                ]
            )

            col2.metric(
                "Lines of Code",
                project_features[
                    "total_loc"
                ]
            )

            col3.metric(
                "Functions",
                project_features[
                    "total_functions"
                ]
            )

            col4.metric(
                "Classes",
                project_features[
                    "total_classes"
                ]
            )


            # =====================================================
            # LANGUAGES
            # =====================================================

            st.header(
                "🌐 Detected Languages"
            )

            st.json(
                languages
            )


            # =====================================================
            # ML FEATURES
            # =====================================================

            st.header(
                "🤖 Automatically Generated ML Features"
            )

            st.dataframe(
                [
                    {
                        "Feature": key,
                        "Value": value
                    }

                    for key, value
                    in ml_features.items()
                ],
                use_container_width=True
            )


            # =====================================================
            # PREDICTION
            # =====================================================

            st.header(
                "📈 Maintenance Prediction"
            )

            col1, col2, col3 = (
                st.columns(3)
            )

            col1.metric(
                "Predicted Effort",
                f"{effort:,.2f}"
            )

            col2.metric(
                "Estimated Cost",
                f"₹{cost:,.2f}"
            )

            col3.metric(
                "Risk",
                risk
            )


            st.subheader(
                "Prediction Range"
            )

            st.write(
                f"{uncertainty['lower']:,.2f}"
                f" - "
                f"{uncertainty['upper']:,.2f}"
            )


            # =====================================================
            # GEMINI
            # =====================================================

            st.header(
                "🧠 Gemini 3.5 Flash AI Analysis"
            )

            summary = gemini_analysis.get(
                "summary",
                {}
            )

            st.subheader(
                "Overall Assessment"
            )

            st.write(
                summary.get(
                    "overall_assessment",
                    "No assessment available."
                )
            )


            col1, col2 = (
                st.columns(2)
            )

            col1.metric(
                "AI Quality Score",
                summary.get(
                    "quality_score",
                    0
                )
            )

            col2.metric(
                "Technical Debt Score",
                summary.get(
                    "technical_debt_score",
                    0
                )
            )


            # =====================================================
            # ERRORS
            # =====================================================

            st.subheader(
                "🐛 Errors and Bugs Detected"
            )

            errors = gemini_analysis.get(
                "errors",
                []
            )

            if errors:

                for index, error in enumerate(
                    errors,
                    start=1
                ):

                    with st.expander(
                        f"Error {index}: "
                        f"{error.get('type', 'Issue')}"
                    ):

                        st.write(
                            f"**Severity:** "
                            f"{error.get('severity', '')}"
                        )

                        st.write(
                            f"**File:** "
                            f"{error.get('file', '')}"
                        )

                        st.write(
                            f"**Line:** "
                            f"{error.get('line', '')}"
                        )

                        st.write(
                            f"**Problem:** "
                            f"{error.get('problem', '')}"
                        )

                        st.write(
                            f"**Explanation:** "
                            f"{error.get('explanation', '')}"
                        )

                        st.write(
                            f"**Recommended Solution:** "
                            f"{error.get('solution', '')}"
                        )

                        st.write(
                            f"**Maintenance Action:** "
                            f"{error.get('maintenance_action', '')}"
                        )

            else:

                st.success(
                    "No confirmed code errors were detected by Gemini."
                )


            # =====================================================
            # SECURITY
            # =====================================================

            st.subheader(
                "🔐 Security Issues"
            )

            security_issues = (
                gemini_analysis.get(
                    "security_issues",
                    []
                )
            )

            if security_issues:

                st.dataframe(
                    security_issues,
                    use_container_width=True
                )

            else:

                st.success(
                    "No security issues were identified."
                )


            # =====================================================
            # CODE QUALITY
            # =====================================================

            st.subheader(
                "🧹 Code Quality Issues"
            )

            quality_issues = (
                gemini_analysis.get(
                    "code_quality_issues",
                    []
                )
            )

            if quality_issues:

                st.dataframe(
                    quality_issues,
                    use_container_width=True
                )

            else:

                st.success(
                    "No major code quality issues were identified."
                )


            # =====================================================
            # AI MAINTENANCE RECOMMENDATIONS
            # =====================================================

            st.header(
                "🛠️ AI Maintenance Recommendations"
            )

            st.markdown(
                ai_recommendations
            )


            # =====================================================
            # HOTSPOTS
            # =====================================================

            st.header(
                "🔥 Maintenance Hotspots"
            )

            st.dataframe(
                hotspots[:20],
                use_container_width=True
            )


            # =====================================================
            # ANOMALY
            # =====================================================

            st.header(
                "🚨 Anomaly Detection"
            )

            if anomaly["is_anomaly"]:

                st.error(
                    "Anomalous project characteristics detected."
                )

            else:

                st.success(
                    "Project characteristics appear normal."
                )

            st.write(
                f"Anomaly score: "
                f"{anomaly['score']:.4f}"
            )


            # =====================================================
            # DEPENDENCIES
            # =====================================================

            st.header(
                "📦 Dependencies"
            )

            st.write(
                dependencies
            )


            # =====================================================
            # CHANGE IMPACT
            # =====================================================

            st.header(
                "🔄 Change Impact Analysis"
            )

            change_impact = (
                gemini_analysis.get(
                    "change_impact",
                    {}
                )
            )

            st.write(
                "**High Impact Areas**"
            )

            st.write(
                change_impact.get(
                    "high_impact_areas",
                    []
                )
            )

            st.write(
                "**Affected Components**"
            )

            st.write(
                change_impact.get(
                    "affected_components",
                    []
                )
            )

            st.write(
                "**Recommendation**"
            )

            st.write(
                change_impact.get(
                    "recommendation",
                    ""
                )
            )


            # =====================================================
            # REPORTS
            # =====================================================

            st.header(
                "📄 Automated Maintenance Reports"
            )

            report_files = (
                generate_all_reports(
                    report_data
                )
            )

            for format_name, path in (
                report_files.items()
            ):

                try:

                    with open(
                        path,
                        "rb"
                    ) as file:

                        st.download_button(
                            label=(
                                f"Download "
                                f"{format_name}"
                            ),
                            data=file,
                            file_name=os.path.basename(
                                path
                            ),
                            key=(
                                "download_"
                                + format_name
                            )
                        )

                except Exception as error:

                    st.warning(
                        f"Could not create "
                        f"{format_name} report: "
                        f"{error}"
                    )


        except Exception as error:

            st.error(
                "❌ Analysis failed"
            )

            st.exception(
                error
            )