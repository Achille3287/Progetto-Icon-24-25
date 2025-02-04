% Importazione delle classi
:- include('setup.pl').

%%  Regole della base di conoscenza

/**
 * Calcola la distanza tra due stazioni di monitoraggio X e Y
 *
 * @param X: prima stazione di monitoraggio
 * @param Y: seconda stazione di monitoraggio
 * @param S: distanza tra le due stazioni (viene restituito il risultato)
 */
distanza_stazioni(X, Y, S) :- prop(X, latitudine, L1), prop(Y, latitudine, L2), 
                              prop(X, longitudine, G1), prop(Y, longitudine, G2), 
                              S is abs(L1 - L2 + G1 - G2).


/**
 * Restituisce le stazioni di monitoraggio immediatamente vicine a una data stazione.
 * Due stazioni sono vicine se appartengono alla stessa zona urbana.
 *
 * @param Stazione: Stazione di cui si vogliono conoscere le vicine
 * @param Vicine: lista di stazioni vicine (viene restituito il risultato)
 */
stazioni_vicine(Stazione, Vicine) :- prop(Stazione, type, stazione_monitoraggio), 
                                     prop(Stazione, zona_monitorata, Zona), 
                                     stazioni_nella_zona(Stazione, Zona, Vicine).

stazioni_nella_zona(Stazione, [], Vicine) :- prop(Stazione, type, stazione_monitoraggio), Vicine = [].
stazioni_nella_zona(Stazione, [Z1|Z2], Vicine) :- prop(Z1, punti_monitoraggio, P1),
                                                  suddividi_prefisso_suffisso(Stazione, P1, Prefisso, Suffisso),
                                                  inverti(Prefisso, Prefisso1),
                                                  find_first(Prefisso1, Vicina1),
                                                  find_first(Suffisso, Vicina2),
                                                  stazioni_nella_zona(Stazione, Z2, Vicine3),
                                                  append(Vicine3, [Vicina1|Vicina2], Vicine).


/**
 * Restituisce la latitudine e la longitudine di una stazione di monitoraggio
 *
 * @param X: Stazione di cui si vogliono conoscere le coordinate
 * @param L: latitudine 
 * @param G: longitudine 
 */
lat_lon(X, Latitudine, Longitudine) :- prop(X, latitudine, Latitudine), 
                                       prop(X, longitudine, Longitudine).
