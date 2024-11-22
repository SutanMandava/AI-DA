import numpy as np

P_A = {"yes": 0.8, "no": 0.2}
P_C = {"yes": 0.5, "no": 0.5}
P_G_given_A_C = {
    ("Good", "yes", "yes"): 0.9,
    ("Good", "yes", "no"): 0.7,
    ("Good", "no", "yes"): 0.6,
    ("Good", "no", "no"): 0.3,
    ("OK", "yes", "yes"): 0.1,
    ("OK", "yes", "no"): 0.3,
    ("OK", "no", "yes"): 0.4,
    ("OK", "no", "no"): 0.7,
}
P_J_given_G = {"Good": {"yes": 0.8, "no": 0.2}, "OK": {"yes": 0.2, "no": 0.8}}
P_S_given_G = {"Good": {"yes": 0.7, "no": 0.3}, "OK": {"yes": 0.3, "no": 0.7}}

def monte_carlo_simulation(num_samples=10000):
    count_j_yes_given_a_c = 0
    count_a_c = 0
    for _ in range(num_samples):
        a = np.random.choice(["yes", "no"], p=[P_A["yes"], P_A["no"]])
        c = np.random.choice(["yes", "no"], p=[P_C["yes"], P_C["no"]])
        g_probs = [
            P_G_given_A_C[(g, a, c)]
            for g in ["Good", "OK"]
        ]
        g_probs /= np.sum(g_probs)
        g = np.random.choice(["Good", "OK"], p=g_probs)
        j = np.random.choice(["yes", "no"], p=[P_J_given_G[g]["yes"], P_J_given_G[g]["no"]])
        if a == "yes" and c == "yes":
            count_a_c += 1
            if j == "yes":
                count_j_yes_given_a_c += 1
    if count_a_c == 0:
        return 0
    return count_j_yes_given_a_c / count_a_c

estimated_probability = monte_carlo_simulation()
print(f"Estimated P(J=yes | A=yes, C=yes): {estimated_probability}")



