/* Classe zona_urbana
 *
 * Contiene i seguenti attributi:
 * - nome: Nome dell'area urbana monitorata
 * - punti_monitoraggio: Lista dei punti di raccolta dati presenti nell’area
 * - indice_inquinamento: Indice medio di qualità dell'aria della zona
 * - densita_popolazione: Numero di abitanti per km²
 */

/* Definizione delle zone urbane */
prop(zona_urbana, subClassOf, area_geografica).

/* Zone urbane con punti di monitoraggio e caratteristiche ambientali */
prop(centro_citta,type,zona_urbana).
prop(centro_citta,nome,centro_citta).
prop(centro_citta,densita_popolazione,8000).
prop(centro_citta,indice_inquinamento,70).
prop(centro_citta,punti_monitoraggio,[stazione_001,stazione_002,stazione_003,stazione_004]).

prop(zona_residenziale,type,zona_urbana).
prop(zona_residenziale,nome,zona_residenziale).
prop(zona_residenziale,densita_popolazione,5000).
prop(zona_residenziale,indice_inquinamento,40).
prop(zona_residenziale,punti_monitoraggio,[stazione_005,stazione_006,stazione_007,stazione_008]).

prop(parco_centrale,type,zona_urbana).
prop(parco_centrale,nome,parco_centrale).
prop(parco_centrale,densita_popolazione,1000).
prop(parco_centrale,indice_inquinamento,15).
prop(parco_centrale,punti_monitoraggio,[stazione_009,stazione_010,stazione_011]).

prop(zona_industriale,type,zona_urbana).
prop(zona_industriale,nome,zona_industriale).
prop(zona_industriale,densita_popolazione,2000).
prop(zona_industriale,indice_inquinamento,90).
prop(zona_industriale,punti_monitoraggio,[stazione_012,stazione_013,stazione_014,stazione_015]).

prop(zona_costiera,type,zona_urbana).
prop(zona_costiera,nome,zona_costiera).
prop(zona_costiera,densita_popolazione,3500).
prop(zona_costiera,indice_inquinamento,30).
prop(zona_costiera,punti_monitoraggio,[stazione_016,stazione_017,stazione_018,stazione_019]).
