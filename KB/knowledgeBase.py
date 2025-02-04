import copy
from math import atan2, cos, radians, sin, sqrt
import random
import time
import pickle
import numpy as np
from pyswip import Prolog

class KnowledgeBase():

    def __init__(self):
        '''
        Metodo init
        -----------------
        Inizializza il motore Prolog e carica i modelli di machine learning.
        '''
        self.prolog = Prolog()
        self.prolog.consult("KB/prolog/knowledge_base.pl", catcherrors=False)

        # Caricamento modelli ML
        with open('supervised_learning/models/knn.sav', 'rb') as pickle_file:
            self.knn = pickle.load(pickle_file)

        with open('supervised_learning/models/scaler_knn.sav', 'rb') as pickle_file:
            self.scaler = pickle.load(pickle_file)

        # Dati predefiniti per previsione inquinamento
        self.dic = {
            "zona_urbana_densa": self.predizione_inquinamento(1),
            "zona_residenziale": self.predizione_inquinamento(2),
            "zona_periferica": self.predizione_inquinamento(3)
        }

        # Stazioni di monitoraggio attive
        self.stazioni_attive = []
        query_stazioni = "prop(Stazione, sensori, 1)"
        for atom in self.prolog.query(query_stazioni):
            self.stazioni_attive.append(atom["Stazione"])

        # Mappatura cicli di raccolta dati
        self.dict_zone = {}
        for stazione in self.stazioni_attive:
            self.ciclo_monitoraggio(stazione)

    def ciclo_monitoraggio(self, stazione):
        '''
        Metodo ciclo_monitoraggio
        -------------------------
        Assegna un ciclo di raccolta dati alle stazioni di monitoraggio.

        Dati di input
        -------------
        stazione: Stazione di monitoraggio di cui si vogliono conoscere le zone urbane monitorate.
        '''
        tempo_totale = 0
        zone = []
        query_stazione = f"prop({stazione}, zone_monitorate, Zone)"
        
        for atom in self.prolog.query(query_stazione):
            zone = atom["Zone"]

        array_periodo = []
        periodo_minimo = 10  # Minimo tempo di campionamento

        for zona in zone:
            query_zona = f"prop({zona.value}, type, TipoZona)"
            tipo_zona = list(self.prolog.query(query_zona))[0]["TipoZona"]

            indice_inquinamento = self.dic[tipo_zona]
            tempo_raccolta = max(10, int((indice_inquinamento * 20) * 2))
            array_periodo.append(tempo_raccolta)
            tempo_totale += tempo_raccolta
        
        # Adatta il tempo per mantenere uniformità
        resto = 5 - (tempo_totale % 5)
        if resto != 0:
            zona_random = random.randint(0, len(zone) - 1)
            array_periodo[zona_random] += resto

        dict_zone = {}
        for i, zona in enumerate(zone):
            lista_zona = []

            # Periodo di inattività prima della raccolta
            if i > 0:
                periodo_inattivo = sum(array_periodo[:i])
                lista_zona.append({"tempo": periodo_inattivo, "stato": "inattivo"})
            
            lista_zona.append({"tempo": array_periodo[i], "stato": "raccolta_dati"})

            if i < len(zone) - 1:
                periodo_inattivo = sum(array_periodo[(i + 1):])
                lista_zona.append({"tempo": periodo_inattivo, "stato": "inattivo"})

            dict_zone[zona.value] = lista_zona

        self.dict_zone[stazione] = dict_zone

    def predizione_inquinamento(self, tipo_zona):
        '''
        Metodo predizione_inquinamento
        -------------------------------
        Predice il livello di inquinamento basato sul tipo di zona e l'orario.

        Dati di input
        -------------
        tipo_zona: Tipo della zona urbana.

        Dati di output
        --------------
        indice_inquinamento: Livello stimato di inquinamento.
        '''
        data = time.localtime()
        
        if data.tm_wday > 4:
            is_weekend = 1
        else:
            is_weekend = 0

        X = np.array([[data.tm_mday, data.tm_mon, data.tm_hour, is_weekend, tipo_zona]])
        X = self.scaler.transform(X)

        return self.knn.predict(X)[0]

    def distanza_stazioni_secondi(self, X, Y):
        '''
        Metodo distanza_stazioni
        ------------------------
        Calcola la distanza in secondi tra due stazioni di monitoraggio.

        Dati di input
        -------------
        X: Prima stazione di monitoraggio.
        Y: Seconda stazione di monitoraggio.

        Dati di output
        --------------
        secondi: Tempo stimato di spostamento tra le due stazioni.
        '''
        distanza = 0
        radius = 6371

        query_X = f"lat_lon({X}, L, G)"
        for atom in self.prolog.query(query_X):
            lat1, lon1 = atom["L"], atom["G"]

        query_Y = f"lat_lon({Y}, L, G)"
        for atom in self.prolog.query(query_Y):
            lat2, lon2 = atom["L"], atom["G"]

        dlat = radians(lat2 - lat1)
        dlon = radians(lon2 - lon1)
        a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distanza = radius * c * 1000

        velocita_media = 20  # Velocità media spostamento (m/s)
        secondi = distanza / velocita_media

        return secondi

    def lista_zone(self):
        '''
        Metodo lista_zone
        -----------------
        Dati di output
        --------------
        zone: Lista delle zone urbane monitorate.
        '''
        zone = []

        query = "prop(X, type, zona_urbana)"
        for atom in self.prolog.query(query):
            if isinstance(atom["X"], str):
                zone.append(atom["X"])

        return zone

    def lista_stazioni(self):
        '''
        Metodo lista_stazioni
        ----------------------
        Dati di output
        --------------
        stazioni: Lista di tutte le stazioni di monitoraggio.
        '''
        stazioni = []
        query_stazioni = "prop(N, type, stazione_monitoraggio)"
        for atom in self.prolog.query(query_stazioni):
            stazioni.append(atom["N"])

        return stazioni



