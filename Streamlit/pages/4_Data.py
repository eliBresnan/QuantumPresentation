import streamlit as st
from PIL import Image

NBA_site_img = Image.open("images\Screenshot 2025-05-12 000858.png")
Json_img = Image.open("images\Screenshot 2025-05-12 001704.png")
Max_min_img = Image.open("images\Screenshot 2025-05-12 010648.png")
Encode_function_img = Image.open("images\Screenshot 2025-05-12 010154.png")

st.title("Data")
section = st.radio("Show section",("Overview","Limitations","Encoding"))
st.markdown("---")


if section == "Overview":

    st.subheader("What Data I Used")
    st.image(NBA_site_img, caption="Screenshot from ESPN game logs")
    st.markdown("---")
    st.write("""
    - I initially wanted to use individual player stats to predict a player's performance
        - Much too intricate, as each player would require their own lstm
    - Instead, I consolidated player stats into team stats
    - Each time-series step is a game, with 8 data fields...

         """)
    st.markdown("---")
    st.image(Json_img,caption="All data and states were stored as json")


elif section == "Limitations":

    st.subheader("Limitations")
    st.write("""
    - Consolidating player data was not easy
         - With a lot of programming acrobatics, I was able to automate the calculations
    - The specific data I needed was unavailable to download, so I was bottlenecked with manually entering data
    - I was also limited to how many dimensions I could have due to qubit requirement
         - I chose the stats that were most applicable to how many points were scored, as that would be the determining factor in predicting who won a game

         """)
    st.markdown("---")
    st.image(Json_img,caption="All data and states were stored as json")
    
else:
    st.subheader("Encoding")
    st.write("""
        - I initally thought I should use amplitude encoding
             - Sources said amplitude encoding was best for QLSTMs
             - That was very confusing, I never really figured out the concept or how to do it
        - The paper I was following deceptively used angle encoding by rotating qubits around the y and z axis
             - That was much simpler
    """)
    st.markdown("---")
    st.subheader("Step 1: Normalizing to [0,1]")
    st.write("""
        - My main source mentioned that this isn't necessary, but it's good practice
        - I hardcoded max and min values for each data field
            - I more or less chose these arbirtrarily, but with consideration for NBA records
             """)
    st.image(Max_min_img)
    st.markdown("---")
    st.subheader("Step 2: Encoding Layer")
    st.write("""
            - "We choose the arctan function here, as opposed to arcsin and arccos... becasue in general the input values are not in the interval of [-1,1], but in R, which is also the domain of arctan."
                - From *Quantum Long Short-Term Memory* by researchers at the Computational Science Initiative, Brookhaven National Laboratory
             """)
    st.image(Encode_function_img)

col1, col2, col3, col4, col5, col6 = st.columns(6)
with col1:
    if st.button("<< Prev"):
        st.switch_page("pages/3_Integrating_Quantum_Computing.py")
with col2:    
    if st.button("Next >>"):
        st.switch_page("pages/5_Optimization_and_The_Blocking_Issue.py")