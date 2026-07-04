"""
AI SEASON — DAY 2 TASK
Travel Planner App (25-Minute Production Build)

Applies the Golden Formula from the Day 2 deck:
  ROLE -> TASK -> CONSTRAINTS -> OUTPUT FORMAT
plus structured-output enforcement and negative constraints (guardrails).

Run with:  streamlit run travel_planner_app.py
"""

import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DO_API_KEY"),
    base_url=os.getenv("DO_BASE_URL"),
)
MODEL = os.getenv("MODEL")

st.set_page_config(page_title="AI Travel Planner", page_icon="🧭", layout="centered")

st.title("🧭 AI Travel Planner")
st.caption("AI Season Bootcamp — Day 2 Production Build")

with st.form("planner_form"):
    col1, col2 = st.columns(2)
    with col1:
        destination = st.text_input("Destination", placeholder="e.g. Istanbul, Turkey")
        days = st.number_input("Number of days", min_value=1, max_value=30, value=4)
    with col2:
        budget = st.selectbox("Budget level", ["Budget", "Mid-range", "Luxury"])
        interests = st.text_input("Interests", placeholder="e.g. history, food, hiking")

    travel_style = st.selectbox("Pace", ["Relaxed", "Balanced", "Packed / Fast-paced"])
    submitted = st.form_submit_button("Generate Itinerary")

if submitted:
    if not destination:
        st.error("Please enter a destination.")
    else:
        # --- THE GOLDEN FORMULA (Role + Task + Constraints + Output) ---
        system_prompt = (
            "You are an expert travel itinerary planner with deep knowledge of "
            "global destinations, local logistics, and realistic daily pacing.\n\n"
            "TASK: Produce a complete, day-by-day travel itinerary for the trip described "
            "by the user.\n\n"
            "CONSTRAINTS:\n"
            "- Match the stated budget level and pace exactly.\n"
            "- Each day must include: Morning, Afternoon, Evening activities.\n"
            "- Include one realistic local food recommendation per day.\n"
            "- Do not invent nonexistent places; only reference plausible, well-known "
            "or generic local options if unsure.\n"
            "- Do not include conversational filler, disclaimers, or apologies.\n\n"
            "OUTPUT FORMAT: Markdown, with '## Day N' headers, and bullet points under "
            "each Morning/Afternoon/Evening. End with a short 'Packing Tips' section."
        )

        user_prompt = (
            f"Destination: {destination}\n"
            f"Duration: {days} days\n"
            f"Budget: {budget}\n"
            f"Pace: {travel_style}\n"
            f"Interests: {interests or 'general sightseeing'}"
        )

        with st.spinner("Building your itinerary..."):
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.7,
            )
            itinerary = response.choices[0].message.content

        st.markdown("---")
        st.markdown(itinerary)
        st.download_button("Download itinerary (.md)", itinerary, file_name=f"{destination}_itinerary.md")

st.markdown("---")
st.caption("Built with prompt engineering: Role • Task • Constraints • Output format")
