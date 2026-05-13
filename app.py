import streamlit as st
import os

from openai import OpenAI
apiKey = os.environ.get("DEEPSEEK_API_KEY")
client = OpenAI(api_key=apiKey, base_url="https://api.deepseek.com")

# ---------- PAGE CONFIG ----------

st.set_page_config(
    page_title="Telco Incident Assistant",
    page_icon="📡",
    layout="centered"
)

# ---------- TITLE ----------

st.title("📡 Telco Incident Assistant")

st.write(
    "AI-assisted prototype for telecom incident triage and workflow automation."
)

# ---------- ANALYSIS FUNCTION ----------

def analyze_incident(text):

    text = text.lower()

    category = "General Incident"
    severity = "Medium"

    causes = []
    actions = []

    # CATEGORY DETECTION

    if "internet" in text or "network" in text:
        category = "Network Issue"

    elif "billing" in text or "invoice" in text:
        category = "Billing Issue"

    elif "mobile" in text or "signal" in text:
        category = "Mobile Service Issue"

    # SEVERITY

    if "down" in text or "critical" in text:
        severity = "High"

    elif "slow" in text or "unstable" in text:
        severity = "Medium"

    else:
        severity = "Low"

    # POSSIBLE CAUSES

    if category == "Network Issue":
        causes = [
            "Network congestion",
            "Router failure",
            "Recent configuration change"
        ]

    elif category == "Mobile Service Issue":
        causes = [
            "Cell tower congestion",
            "Signal interference",
            "Backhaul issue"
        ]

    elif category == "Billing Issue":
        causes = [
            "Invoice generation error",
            "Account synchronization issue"
        ]

    else:
        causes = [
            "Unknown root cause"
        ]

    # ACTIONS

    actions = [
        "Check monitoring dashboards",
        "Validate recent changes",
        "Escalate if issue persists"
    ]

    return category, severity, causes, actions

# ---------- USER INPUT ----------

incident = st.text_area(
    "Describe the telecom incident",
    height=200,
    placeholder="Example: Users report unstable mobile data after maintenance."
)

# ---------- BUTTON ----------

if st.button("Analyze Incident"):

    if incident.strip() == "":
        st.warning("Please enter an incident description.")

    else:

        category, severity, causes, actions = analyze_incident(incident)

        # RESULTS
        response = client.chat.completions.create(
        model="deepseek-v4-flash",
        messages=[
        {
            "role": "system",
            "content": """
                You are a telecom incident analyst.

                Your task is to:
                - summarize the incident
                - explain possible causes
                - recommend next steps

                Keep the response concise and operational.
                """
                    },
                    {
                        "role": "user",
                        "content": f"""
                Incident Description:
                {incident}

                Category:
                {category}

                Severity:
                {severity}

                Possible Causes:
                {chr(10).join(causes)}

                Recommended Actions:
                {chr(10).join(actions)}
                """
                    }
                ]
        )

        analysis = response.choices[0].message.content

        # st.subheader("Incident Analysis")

        # st.write(f"**Category:** {category}")
        # st.write(f"**Severity:** {severity}")

        # # CAUSES

        # st.subheader("Possible Causes")

        # for cause in causes:
        #     st.write(f"- {cause}")

        # # ACTIONS

        # st.subheader("Recommended Actions")

        # for action in actions:
        #     st.write(f"- {action}")
            
        #LLM Analysis
        
        st.success("Incident analyzed successfully")
        
        st.metric("Severity", severity)
        
        
        st.subheader("LLM Analysis")
        st.write(f"**LLM Analysis:**  {analysis}")

        # REPORT

        st.subheader("Generated Report")

        report = f"""
        
        
        
Incident Category: {category}

Severity: {severity}

Possible Causes:
- {"\n- ".join(causes)}

Recommended Actions:
- {"\n- ".join(actions)}
"""

        st.code(report)
        
        
