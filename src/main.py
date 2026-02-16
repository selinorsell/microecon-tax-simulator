import numpy as np
import matplotlib.pyplot as plt


def read_float(prompt: str, default: float) -> float:
    """
    Lets user press Enter to accept a default value.
    """
    s = input(f"{prompt} [{default}]: ").strip()
    return default if s == "" else float(s)


def main():
    print("Microeconomic Supply–Demand Simulator (with Tax & DWL)")
    print("Press Enter to use defaults.\n")

    # PARAMETERS (defaults)
    a = read_float("Demand intercept a (Qd=a-bP)", 100.0)
    b = read_float("Demand slope b", 2.0)
    c = read_float("Supply intercept c (Qs=c+dP)", 10.0)
    d = read_float("Supply slope d", 1.5)
    tax = read_float("Per-unit tax", 10.0)

    # Price grid for plotting
    P = np.linspace(0, 80, 500)

    # Curves (Q as a function of P)
    Qd = a - b * P
    Qs = c + d * P

    # Equilibrium (no tax): a - bPe = c + dPe
    Pe = (a - c) / (b + d)
    Qe = a - b * Pe

    # With tax: Pc = Pp + tax and a - bPc = c + dPp
    Pp = (a - c - b * tax) / (b + d)   # producer price received
    Pc = Pp + tax                      # consumer price paid
    Qt = a - b * Pc                    # traded quantity with tax

    # Welfare calculations (linear triangles)
    P_max = a / b        # choke price on demand (Q=0)
    P_min = -c / d       # supply intercept price (Q=0)

    CS = 0.5 * Qe * (P_max - Pe)
    PS = 0.5 * Qe * (Pe - P_min)

    CS_tax = 0.5 * Qt * (P_max - Pc)
    PS_tax = 0.5 * Qt * (Pp - P_min)

    DWL = 0.5 * (Qe - Qt) * tax

    # Print results BEFORE showing the plot (so you see them immediately)
    print("---- RESULTS ----")
    print(f"No Tax Equilibrium: Q={Qe:.2f}, P={Pe:.2f}")
    print(f"With Tax: Quantity={Qt:.2f}, Consumer Price={Pc:.2f}, Producer Price={Pp:.2f}")
    print(f"Consumer Surplus (No Tax): {CS:.2f}")
    print(f"Producer Surplus (No Tax): {PS:.2f}")
    print(f"Consumer Surplus (Tax): {CS_tax:.2f}")
    print(f"Producer Surplus (Tax): {PS_tax:.2f}")
    print(f"Deadweight Loss: {DWL:.2f}")

    # Plot
    plt.figure(figsize=(8, 6))
    plt.plot(Qd, P, label="Demand")
    plt.plot(Qs, P, label="Supply")

    plt.scatter(Qe, Pe, label="Equilibrium (No Tax)")
    plt.scatter(Qt, Pc, label="Consumer Price (Tax)")
    plt.scatter(Qt, Pp, label="Producer Price (Tax)")

    # tax wedge line
    plt.vlines(Qt, Pp, Pc, linestyles="dashed")

    # DWL shading (triangle between Qe and Qt, between Pe and Pc)
    plt.fill_betweenx(
        [Pe, Pc],
        Qt,
        Qe,
        alpha=0.3,
        label="Deadweight Loss"
    )

    plt.xlabel("Quantity (Q)")
    plt.ylabel("Price (P)")
    plt.title("Supply & Demand with Tax")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()


if __name__ == "__main__":
    main()
