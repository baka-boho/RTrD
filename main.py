import streamlit as st
import numpy as np

def MCNO(demand, offre, cout):
    demand = demand.copy()
    offre = offre.copy()
    original_cout = [row.copy() for row in cout]
    cout = [row.copy() for row in cout]

    if sum(offre) != sum(demand):
        if sum(offre) > sum(demand):
            demand.append(sum(offre) - sum(demand))
            for row in cout:
                row.append(0)
            for row in original_cout:
                row.append(0)
        else:
            offre.append(sum(demand) - sum(offre))
            cout.append([0] * len(demand))
            original_cout.append([0] * len(demand))

    quantity = [[0 for j in range(len(demand))] for i in range(len(offre))]
    
    for i in range(len(offre)):  
        for j in range(len(demand)):
            if demand[j] > 0:
                if offre[i] >= demand[j]:
                    quantity[i][j] = demand[j]
                    offre[i] -= demand[j]
                    demand[j] = 0 
                else:
                    quantity[i][j] = offre[i]
                    demand[j] -= offre[i]
                    offre[i] = 0 

    total_cost = sum(quantity[i][j] * original_cout[i][j] for i in range(len(offre)) 
                    for j in range(len(demand)))

    return quantity, total_cost

def moindre_cout(demand, offre, cout):
    demand = demand.copy()
    offre = offre.copy()
    original_cout = [row.copy() for row in cout]
    cout = [row.copy() for row in cout]

    if sum(offre) != sum(demand):
        if sum(offre) > sum(demand):
            demand.append(sum(offre) - sum(demand))
            for row in cout:
                row.append(0)
            for row in original_cout:
                row.append(0)
        else:
            offre.append(sum(demand) - sum(offre))
            cout.append([0] * len(demand))
            original_cout.append([0] * len(demand))

    quantity = [[0 for j in range(len(demand))] for i in range(len(offre))]
    
    while sum(demand) > 0 and sum(offre) > 0:
        min_cout = float('inf')
        min_i = -1
        min_j = -1
        for i in range(len(offre)):
            for j in range(len(demand)):
                if cout[i][j] < min_cout:
                    min_cout = cout[i][j]
                    min_i = i
                    min_j = j
        
        if min_i == -1 or min_j == -1:
            break
            
        if offre[min_i] == 0 or demand[min_j] == 0:
            cout[min_i][min_j] = float('inf')
        elif offre[min_i] > demand[min_j]:
            quantity[min_i][min_j] = demand[min_j]
            offre[min_i] -= demand[min_j]
            demand[min_j] = 0
            cout[min_i][min_j] = float('inf')
        else:
            quantity[min_i][min_j] = offre[min_i]
            demand[min_j] -= offre[min_i]
            offre[min_i] = 0
            cout[min_i][min_j] = float('inf')

    total_cost = sum(quantity[i][j] * original_cout[i][j] for i in range(len(offre)) 
                    for j in range(len(demand)))

    return quantity, total_cost

def vogel(cout, offre, demande):
    original_cout = np.array(cout, dtype=float).copy()
    cout = np.array(cout, dtype=float).copy()
    offre = np.array(offre, dtype=float).copy()
    demande = np.array(demande, dtype=float).copy()

    if np.sum(offre) != np.sum(demande):
        if np.sum(offre) > np.sum(demande):
            demande = np.append(demande, np.sum(offre) - np.sum(demande))
            cout = np.column_stack((cout, np.zeros(len(offre))))
            original_cout = np.column_stack((original_cout, np.zeros(len(offre))))
        else:
            offre = np.append(offre, np.sum(demande) - np.sum(offre))
            cout = np.row_stack((cout, np.zeros(len(demande))))
            original_cout = np.row_stack((original_cout, np.zeros(len(demande))))

    quantity = np.zeros((len(offre), len(demande)))
    
    while np.sum(demande) > 0 and np.sum(offre) > 0:
        regret_ligne = []
        regret_col = []
        
        for i in range(len(cout)):
            if offre[i] <= 0:
                regret_ligne.append(-1)
                continue
                
            sorted_row = []
            for j in range(len(cout[i])):
                if cout[i][j] != float('inf') and demande[j] > 0:
                    sorted_row.append(cout[i][j])
            sorted_row.sort()
            
            if len(sorted_row) >= 2:
                regret_ligne.append(sorted_row[1] - sorted_row[0])
            elif len(sorted_row) == 1:
                regret_ligne.append(sorted_row[0])
            else:
                regret_ligne.append(-1)
        
        for j in range(len(cout[0])):
            if demande[j] <= 0:
                regret_col.append(-1)
                continue
                
            sorted_col = []
            for i in range(len(cout)):
                if cout[i][j] != float('inf') and offre[i] > 0:
                    sorted_col.append(cout[i][j])
            sorted_col.sort()
            
            if len(sorted_col) >= 2:
                regret_col.append(sorted_col[1] - sorted_col[0])
            elif len(sorted_col) == 1:
                regret_col.append(sorted_col[0])
            else:
                regret_col.append(-1)

        if max(regret_ligne) < 0 and max(regret_col) < 0:
            break
            
        if max(regret_ligne) >= max(regret_col):
            i_min = regret_ligne.index(max(regret_ligne))
            minimum = float('inf')
            j_min = -1
            for j in range(len(cout[i_min])):
                if cout[i_min][j] != float('inf') and demande[j] > 0:
                    if cout[i_min][j] < minimum:
                        minimum = cout[i_min][j]
                        j_min = j
            if j_min == -1:
                break
        else:
            j_min = regret_col.index(max(regret_col))
            minimum = float('inf')
            i_min = -1
            for i in range(len(offre)):
                if cout[i][j_min] != float('inf') and offre[i] > 0:
                    if cout[i][j_min] < minimum:
                        minimum = cout[i][j_min]
                        i_min = i
            if i_min == -1:
                break
        
        quantity_to_allocate = min(offre[i_min], demande[j_min])
        quantity[i_min][j_min] = quantity_to_allocate
        offre[i_min] -= quantity_to_allocate
        demande[j_min] -= quantity_to_allocate
        
        if offre[i_min] <= 0:
            cout[i_min, :] = float('inf')
        if demande[j_min] <= 0:
            cout[:, j_min] = float('inf')

    total_cost = np.sum(quantity * original_cout)
    return quantity.tolist(), total_cost

def create_matrix_input(rows, cols):
    matrix = []
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.write("Matrice des coûts:")
        with st.container():
            cols = st.columns(cols)
            for i in range(rows):
                row_values = []
                for j, col in enumerate(cols):
                    with col:
                        value = st.number_input(
                            label=f"",
                            key=f"matrix_{i}_{j}",
                            value=0.0,
                            step=1.0,
                            format="%.1f"
                        )
                        row_values.append(value)
                matrix.append(row_values)
    return matrix

st.title("Solveur de problème de transport")

method = st.selectbox("Méthode:", ["MCNO", "Moindre Cout", "Vogel"])

col1, col2 = st.columns(2)
with col1:
    demand = st.text_input("Demande (séparée par des virgules):")
with col2:
    offer = st.text_input("Offre (séparée par des virgules):")

if demand and offer:
    try:
        demand_list = list(map(float, demand.split(',')))
        offer_list = list(map(float, offer.split(',')))
        
        matrix = create_matrix_input(len(offer_list), len(demand_list))
        
        if st.button("Calculer"):
            if method == "MCNO":
                quantity, total_cost = MCNO(demand_list, offer_list, matrix)
            elif method == "Moindre Cout":
                quantity, total_cost = moindre_cout(demand_list, offer_list, matrix)
            else:
                quantity, total_cost = vogel(matrix, offer_list, demand_list)
            
            st.write("Matrice des quantités:")
            st.write(np.array(quantity))
            st.write(f"Coût total: {total_cost}")
            
    except ValueError as e:
        st.error("Veuillez entrer des nombres valides séparés par des virgules")
