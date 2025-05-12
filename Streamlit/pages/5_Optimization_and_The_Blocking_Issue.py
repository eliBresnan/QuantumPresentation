import streamlit as st

from images import QLSTM_code


st.header("Optimization")
st.markdown("---")

st.subheader("Parameter Shifting")
st.write("""
        - Each qubit has 3 rotational weights for every layer of depth on the circuit
            - These must be optimized during training
        - Classical LSTMS can use an optimization procedure called Back Propogation, however, QLSTMs are incapable of this becuase of their probabilistic outputs
        - Parameter Shifting is an alternative, in which the cell is ran twice for each weight, or parameter at a time step
            - The parameter in question is shifted an equal amount in both directions
            - The outputted predictions for each are evaluated by their accuracy, then a new parameter is calculated accordingly
 
         
         """)
st.write("This is where I got stuck...")

st.markdown("---")
show_code = st.toggle("Show Parameter Shift Code")
if show_code:
    st.code(QLSTM_code.ps_code)
st.markdown("---")

st.subheader("The Blocking Issue")
st.write("""
        So here's my problem...
        - With 8 data points in a time step, there are 80 qubits per lstm cell
        - I set my variational layer to the minimal depth of 1, so there are 3 parameters for each qubit
        - That means 240 parameters must be shifted per input...
        - ... which means the cell has to be run 480 times, simulating 2880 quantum circuits for just one time step
         """)
st.image("Streamlit/images/Main.py - Quantum - Visual Studio Code 2025-05-12 04-14-02 (online-video-cutter.com).gif")
st.write("""
        - As you can see, it takes about a minute to optimize just one qubit
        - So if I wanted to predict the outcome of the timberwolves game tonight using the past season as training data...
         """)
st.write("**...It would take OVER A WEEK straight of computing to make a prediction**")
st.markdown("---")

st.subheader("Potential Solutions")
st.write("I had to ask myself where the hell I went wrong. I gave up on the coding after this, because I realized I still had a presentation and 6 page paper to write about it, but I still wanted to theorize some potential solutions.")

st.write("I knew I couldn't use multiple processes because all the calculations are sequential, so I had to come up with ideas to decrease the number of parameters...")
st.write("""
        - Decrease the amount of statistics I have in an input
        - Decrease the parameters per qubit, like only rotating around one axis instead of all three
        - Share parameters across the circuits
        - Compressing data dimensions with classical projection
         
        Maybe these will be future trials in my quest to become a professional gambler
         """)
st.write("... or a machine learning expert, whichever one works out better")



if st.button("<< Prev"):
    st.switch_page("pages/4_Data.py")
