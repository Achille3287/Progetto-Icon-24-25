import math
import numpy as np
import copy
from src.models.markov_chain.HMM import HMM, simulate

seconds = 5  # Intervallo temporale per la discretizzazione delle previsioni

def get_transition_probability(seq1, seq2, time_offset, velocity=0):
    """
    Calcola la probabilità di transizione tra due sequenze basate su una catena di Markov.

    Args:
        seq1 (list): Prima sequenza di stati.
        seq2 (list): Seconda sequenza di stati.
        time_offset (int): Differenza temporale tra le due sequenze.
        velocity (float): Fattore di velocità per il calcolo della transizione.

    Returns:
        float: Probabilità di transizione tra gli stati.
    """

    chain1 = create_chain(seq1, velocity)
    chain2 = create_chain(seq2, velocity)

    total_chain1 = len(chain1.states) * seconds
    total_chain2 = len(chain2.states) * seconds

    lcm_val = math.lcm(total_chain1, total_chain2)
    num_cycles1 = int(lcm_val / total_chain1)
    num_cycles2 = int(lcm_val / total_chain2)

    states_seq1, obs_seq1 = simulate(chain1, int(num_cycles1 * (total_chain1 / seconds)))
    states_seq2, obs_seq2 = simulate(chain2, int(num_cycles2 * (total_chain2 / seconds)))

    transition_points = []
    for i in range(len(obs_seq1)):
        if obs_seq1[i]['high_pollution'] == 1 and obs_seq1[(i + 1) % len(obs_seq1)]['high_pollution'] == 0:
            transition_points.append((i + 1) % len(obs_seq1))

    time_offset = time_offset % total_chain2
    offset_cycles = int(time_offset / seconds)

    for i in range(len(transition_points)):
        transition_points[i] = (transition_points[i] + offset_cycles) % len(obs_seq2)

    count = 0
    for item in transition_points:
        if obs_seq2[(item - 1) % len(obs_seq2)]["low_pollution"] == 1:
            count += 0.5
        if obs_seq2[item]["low_pollution"] == 1:
            count += 1
        if obs_seq2[(item + 1) % len(obs_seq2)]["low_pollution"] == 1:
            count += 0.5

    if len(transition_points) == 0:
        return 0

    prob = count / (len(transition_points) * (0.5 + 1 + 0.5))
    return prob

def optimize_sequence(seq1, seq2, cycle_2, time_offset, velocity):
    """
    Ottimizza la sequenza temporale di inquinamento per ridurre la sovrapposizione di eventi critici.

    Args:
        seq1 (list): Prima sequenza di stati ambientali.
        seq2 (list): Seconda sequenza di stati ambientali.
        cycle_2 (dict): Ciclo temporale della seconda sequenza.
        time_offset (int): Differenza temporale tra le sequenze.
        velocity (float): Fattore di velocità.

    Returns:
        tuple: Sequenza ottimizzata e ciclo aggiornato.
    """
    cycle1 = sum(value['time'] for value in seq1)
    cycle2 = sum(value['time'] for value in seq2)

    if cycle1 == cycle2:
        max_iterations = cycle2 / seconds
        adjustment_function = shift_sequence
    else:
        max_iterations = math.ceil(cycle2 / (seconds * 10)) * seconds
        adjustment_function = extend_pollution_period

    i = 0
    threshold = get_transition_probability(seq1, seq2, time_offset, velocity)
    best_seq = copy.deepcopy(seq2)
    best_cycle = copy.deepcopy(cycle_2)
    max_threshold = threshold

    while threshold < 1 and i < max_iterations:
        seq2 = adjustment_function(seq2, cycle_2)
        threshold = get_transition_probability(seq1, seq2, time_offset, velocity)

        if max_threshold < threshold:
            max_threshold = threshold
            best_cycle = copy.deepcopy(cycle_2)
            best_seq = copy.deepcopy(seq2)
        i += 1

    return best_seq, best_cycle

def extend_pollution_period(seq2, cycle_2):
    for i in range(len(seq2)):
        if seq2[i]['status'] == 'low_pollution':
            pos_low = i
        if seq2[i]['status'] == 'high_pollution':
            pos_high = i

    seq2[pos_low]['time'] += 1
    seq2[pos_high]['time'] -= 1

    for region, cycle_region in cycle_2.items():
        for i in range(len(cycle_region)):
            if cycle_region[i]['status'] == 'low_pollution':
                pos_low = i
            if cycle_region[i]['status'] == 'high_pollution':
                pos_high = i

        cycle_region[pos_low]['time'] -= 1 / len(cycle_2)
        cycle_region[pos_high]['time'] += 1 / len(cycle_2)

    return seq2

def shift_sequence(seq2, cycle_2=[]):
    i = len(seq2) - 1
    t = 0
    while t < seconds:
        t += seq2[i]['time']
        i -= 1

    if t > seconds:
        i += 1
        diff = t - seconds
        copy_segment = copy.deepcopy(seq2[i])
        seq2.insert(i, copy_segment)
        seq2[i]['time'] = diff
        seq2[i + 1]['time'] -= diff

    shift_pos = len(seq2) - (i + 1)

    if len(cycle_2) > 0:
        for region, cycle in cycle_2.items():
            cycle_2[region] = shift_sequence(cycle)

    return np.roll(seq2, shift_pos).tolist()

def create_chain(sequence, velocity=0):
    """
    Crea una catena di Markov basata sui dati di qualità dell'aria.

    Args:
        sequence (list): Sequenza di stati.
        velocity (float): Parametro opzionale di velocità.

    Returns:
        HMM: Modello di Markov Hidden per la sequenza.
    """
    total_time = sum(value['time'] for value in sequence)
    num_states = int(total_time / seconds)

    states = {'state_' + str(i) for i in range(num_states)}
    observations = {'low_pollution', 'moderate_pollution', 'high_pollution'}

    transition_prob = 1

    if velocity > 0:
        mu, sigma = velocity, 3.76
        sample = np.random.normal(mu, sigma, 1)[0]
        sample = max(sample, 0)  # Assicura che non sia negativo
        transition_prob = sample / velocity

    transitions = {state: {st: 0 for st in states} for state in states}
    
    # Assegna le probabilità di transizione
    for state in states:
        idx = int(state.split('_')[1])
        transitions[state]['state_' + str((idx + 1) % num_states)] = transition_prob
        transitions[state][state] = 1 - transition_prob

    return HMM(states, observations, transitions)
