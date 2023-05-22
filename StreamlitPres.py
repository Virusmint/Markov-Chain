import streamlit as st
import numpy as np
import pandas as pd
import altair as alt

header = st.container()
restaurants = st.container()
gambler = st.container()
latest_iteration = st.empty() 
plot_spot = st.empty()
plot_spot2 = st.empty()

with header:
    st.title('Introduction to Markov Chains')

with restaurants:
    st.header('Restaurant Simulation')
    col_o, col_a, col_b, col_c = st.columns(4)
    with col_o:
        st.text("")
        st.text("")
        st.text("")
        st.text("")
        st.text("")
        st.write('Chinese')
        st.text("")
        st.text("")
        st.text("")
        st.write('Italian')
        st.text("")
        st.text("")
        st.text("")
        st.text("")
        st.write('Mexican')
    with col_a:
        st.write('Chinese')
        p11 = st.number_input('p11', value=0.5)
        p21 = st.number_input('p21', value=0.6)
        p31 = st.number_input('p31', value=0.4)
    with col_b:
        st.write('Italian')
        p12 = st.number_input('p12', value=0.2)
        p22 = st.number_input('p22', value=0.3)
        p32 = st.number_input('p32', value=0.5)
    with col_c:
        st.write('Mexican')
        p13 = st.number_input('p13', value=0.3)
        p23 = st.number_input('p23', value=0.1)
        p33 = st.number_input('p33', value=0.1)

    col1, col2 = st.columns(2)
    with col1:
        reset = st.button("Rerun")

    # ----------------------------------------------

    initial = st.selectbox('Initial State',
        ('Chinese', 'Italian', 'Mexican'))
    p = np.array([
    [p11, p12, p13],
    [p21, p22, p23],
    [p31, p32, p33]
    ])
    cuisine = ['Chinese', 'Italian', 'Mexican']

    def getSequence(steps):
        '''
        Generate sequence of states based on probability distribution of X_i
        '''
        sequence = []
        if initial == 'Chinese':
            x = np.array([1,0,0])
        elif initial == 'Italian':
            x = np.array([0,1,0])
        elif initial == 'Mexican':
            x = np.array([0,0,1])
        for i in range(steps):
            randomResto = np.random.choice(cuisine, p=x)
            sequence.append(randomResto)
            if randomResto == 'Chinese':
                x = np.array([1,0,0])
            elif randomResto == 'Italian':
                x = np.array([0,1,0])
            elif randomResto == 'Mexican':
                x = np.array([0,0,1])
            x = x@p
        return sequence

    def steadyStateVector():
        '''
        Find the eigenvector with corresponding eigenvalue 1. 
        The eigenvector is scaled such that the sum of its entries is equal to 1
        '''
        e_vals, e_vecs = np.linalg.eig(p.T)
        v = e_vecs[:,0].real
        return v/v.sum()

    # Initialize Variables
    n = int(st.number_input('Number of steps ', min_value=0))
    seq = getSequence(n)
    steadyVec = steadyStateVector()
    counts = pd.DataFrame.from_dict(
        {'Chinese':0, 'Italian':0, 'Mexican':0}, 
        orient='index',
        columns=[0])

    # Loop through state sequence and construct graph
    for i in range(len(seq)):
        latest_iteration.text(f"Appended value : {seq[i]}")
        counts[0][seq[i]] += 1
        data = pd.DataFrame(
            [['Chinese', steadyVec[0], 'theoretical'],
            ['Italian', steadyVec[1], 'theoretical'],
            ['Mexican', steadyVec[2], 'theoretical'],
            ['Chinese', counts[0]['Chinese']/int(counts.sum()), 'observed'],
            ['Italian', counts[0]['Italian']/int(counts.sum()), 'observed'],
            ['Mexican', counts[0]['Mexican']/int(counts.sum()), 'observed']],
            columns=['resto', 'freq', 'type']) 
            
        with plot_spot:
            gp_chart = alt.Chart(data).mark_bar().encode(
            alt.Column('resto'),
            alt.X('type', axis=alt.Axis(title='')),
            alt.Y('freq', axis=alt.Axis(grid=False), scale=alt.Scale(domain=[0, 1])),
            alt.Color('type')
            )
            st.write(gp_chart)


# ----------------------------------------------------------------
# GAMBLER

with gambler:
    st.header("Gambler's ruin")
    col_a, col_b, col_c, col_d = st.columns(4)
    with col_a:
        pstep = st.number_input('Winning Probability', value=0.5)
    with col_b:
        wealth = int(st.number_input('Initial Wealth', min_value=1))
    with col_c:
        target = int(st.number_input('Target Wealth', min_value=wealth))


    # Works only for 1 walk. Cannot plot several walks simultaneously yet.
    stack = [wealth]
    while wealth > 0 and wealth < target:
        wealth = wealth + np.random.choice([1,-1], p=[pstep,1-pstep]) 
        stack.append(wealth)
        resto_df = pd.DataFrame(stack, columns=['wealth'])
        resto_df["step"] = list(resto_df.index)
        with plot_spot2:
            stepChart = alt.Chart(resto_df).mark_line(interpolate='step-after').encode(
                x='step',
                y='wealth')
            stepChart

    # Work in progress

    # Initialize Variables
    # pathDict = {}
    # for i in range(sampleSize):
    #     pathDict[f'walk{i}'] = initial_wealth
    # gambler_df = pd.DataFrame.from_dict(
    #     pathDict, 
    #     index=[0]
    #     )
    # gambler_df['steps']=0
    # j = 1
    #
    # # Simulate Runs
    # while all(value!=0 or value!=target for value in pathDict.values()):
    #     prevStep = gambler_df.iloc[j-1].to_numpy()
    #     for i in range(sampleSize):
    #         if prevStep[i] > 0 or prevStep[i] < target:
    #             prevStep[i] += np.random.choice([1,-1], p=[pstep,1-pstep])
    #     prevStep.append(j)
    #     newStep = prevStep
    #     gambler_df.append(newStep)
    
    #         with plot_spot2:
    #         stepChart = alt.Chart(gambler_df).mark_line(interpolate='step-after').encode(
    #             x='step',
    #             y='wealth')
    #         stepChart
    #     j+=1