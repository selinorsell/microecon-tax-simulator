import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="Supply–Demand Simulator")

st.title("Microeconomic Supply–Demand Simulator")

# SIDEBAR INPUTS
st.sidebar.header("Parameters")

a = st.sidebar.number_input("Demand intercept a", value=100.0)
b = st.sidebar.number_input("Demand slope b", value=2.0)
c = st.sidebar.number_input("Supply intercept c", value=10.0)
d = st.sidebar.number_input("Supply slope d", value=1.5)
tax = st.sidebar.number_input("Per-unit tax", value=10.0, min_value=0.0)

# PRICE GRID
P = np.linspace(0, 80, 500)

# CURVES
Qd = a - b * P
Qs = c + d * P

# EQUILIBRIUM (NO TAX)
Pe = (a - c) / (b + d)
Qe = a - b * Pe

# WITH TAX
Pp = (a - c - b * tax) / (b + d)
Pc = Pp + tax
Qt = a - b * Pc

# WELFARE
P_max = a / b
P_min = -c / d

CS = 0.5 * Qe * (P_max - Pe)
PS = 0.5 * Qe * (Pe - P_min)

CS_tax = 0.5 * Qt * (P_max - Pc)
PS_tax = 0.5 * Qt * (Pp - P_min)

DWL = 0.5 * (Qe - Qt) * tax

# TAX IMPACT
tax_revenue = tax * Qt
consumer_burden = Pc - Pe
producer_burden = Pe - Pp

if tax > 0:
    consumer_share = 100 * consumer_burden / tax
    producer_share = 100 * producer_burden / tax
else:
    consumer_share = producer_share = 0.0

# METRICS
st.subheader("Equilibrium")
st.write(f"No Tax: Q = {Qe:.2f}, P = {Pe:.2f}")
st.write(f"With Tax: Q = {Qt:.2f}, Pc = {Pc:.2f}, Pp = {Pp:.2f}")

st.subheader("Welfare")
st.write(f"Consumer Surplus (No Tax): {CS:.2f}")
st.write(f"Producer Surplus (No Tax): {PS:.2f}")
st.write(f"Deadweight Loss: {DWL:.2f}")

st.subheader("Tax Impact")
st.write(f"Tax Revenue: {tax_revenue:.2f}")
st.write(f"Consumer burden: {consumer_share:.1f}%")
st.write(f"Producer burden: {producer_share:.1f}%")

# PLOT
fig, ax = plt.subplots()

ax.plot(Qd, P, label="Demand")
ax.plot(Qs, P, label="Supply")

ax.scatter(Qe, Pe, label="Equilibrium")
ax.scatter(Qt, Pc, label="Consumer Price")
ax.scatter(Qt, Pp, label="Producer Price")

ax.vlines(Qt, Pp, Pc, linestyles="dashed")

ax.fill_betweenx([Pe, Pc], Qt, Qe, alpha=0.3)

ax.set_xlabel("Quantity")
ax.set_ylabel("Price")
ax.legend()

st.pyplot(fig)
