/* Classe zona_urbana
 *
 * Contiene i seguenti attributi:
 * - nome: Nome dell'area urbana monitorata
 * - punti_raccolta: Lista dei punti di monitoraggio dell’area
 * - livello_inquinamento: Indice medio di qualità dell'aria
 * - popolazione: Numero di abitanti dell’area monitorata
 */

/* Classe zona_urbana sottoclasse di area_geografica */
prop(zona_urbana, subClassOf, area_geografica).

/* Classe punto_raccolta_dati
 *
 * Contiene i seguenti attributi:
 * - id: Identificativo del punto di monitoraggio
 * - latitudine: Posizione del punto
 * - longitudine: Posizione del punto
 * - sensori: Lista dei sensori presenti nel punto di raccolta
 */

/* Un punto di raccolta dati fa parte di una zona urbana */
prop(punto_raccolta_dati, partOf, zona_urbana).

/* Un punto di raccolta ha dei sensori */
prop(punto_raccolta_dati, hasPart, sensore).
