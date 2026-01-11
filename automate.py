import copy as cp


class automate:
    """
    classe de manipulation des automates
    l'alphabet est l'ensemble des caractères alphabétiques minuscules et "E" pour epsilon, 
    et "O" pour l'automate vide
    """
    
    def __init__(self, expr="O"):
        """
        construit un automate élémentaire pour une expression régulière expr 
            réduite à un caractère de l'alphabet, ou automate vide si "O"
        identifiant des états = entier de 0 à n-1 pour automate à n états
        état initial = état 0
        """
        
        # alphabet
        self.alphabet = list("abc")
        # l'expression doit contenir un et un seul caractère de l'alphabet
        if expr not in (self.alphabet + ["O", "E"]):
            raise ValueError("l'expression doit contenir un et un seul\
                           caractère de l'alphabet " + str(self.alphabet))
        # nombre d'états
        if expr == "O":
            # langage vide
            self.n = 1
        elif expr == "E":
            self.n = 1
        else:
            self.n = 2
        # états finals: liste d'états (entiers de 0 à n-1)
        if expr == "O":
            self.final = []
        elif expr == "E":
            self.final = [0]
        else:
            self.final = [1]
        # transitions: dico indicé par (état, caractère) qui donne la liste des états d'arrivée
        self.transition =  {} if (expr in ["O", "E"]) else {(0,expr): [1]}
        # nom de l'automate: obtenu par application des règles de construction
        self.name = "" if expr == "O" else "(" + expr + ")" 
        
    def __str__(self):
        """affichage de l'automate par fonction print"""
        res = "Automate " + self.name + "\n"
        res += "Nombre d'états " + str(self.n) + "\n"
        res += "Etats finals " + str(self.final) + "\n"
        res += "Transitions:\n"
        for k,v in self.transition.items():    
            res += str(k) + ": " + str(v) + "\n"
        res += "*********************************"
        return res
    
    def ajoute_transition(self, q0, a, qlist):
        """ ajoute la liste de transitions (q0, a, q1) pour tout q1 
            dans qlist à l'automate
            qlist est une liste d'états
        """
        if not isinstance(qlist, list):
            raise TypeError("Erreur de type: ajoute_transition requiert une liste à ajouter")
        if (q0, a) in self.transition:
            self.transition[(q0, a)] = self.transition[(q0, a)] + qlist
        else:
            self.transition.update({(q0, a): qlist})
    
    
def concatenation(a1, a2): 
    """Retourne l'automate qui reconnaît la concaténation des 
    langages reconnus par les automates a1 et a2"""

    a1 = cp.deepcopy(a1) #on copie l'automate pour éviter les effets de bord
    a2 = cp.deepcopy(a2)
    a = automate()
    a.name = a1.name + " " + a2.name 
    a.n = a1.n + a2.n #on définit le nombre d'états de l'automate concaténé
    a.final = [q + a1.n for q in a2.final] #on définit les états finaux comme étant les états finaux de a2 avec un décalage de numérotation

    for trans in a1.transition:
        a.transition[trans] = list(a1.transition[trans])#on ajoute les transitions de a1

    for trans in a2.transition :
        q, lettre = trans
        a.transition[(q+a1.n, lettre)] = [d+ a1.n for d in a2.transition[trans]]#on ajote les transitions de a2 avec un décalage de numérotation pour ne pas superposer les numéros 

    for etat_final in a1.final : 
        a.ajoute_transition(etat_final, 'E', [a1.n])#on créer des nouvelles transitions depuis les etats finaux de a1 jusqu'à l'etat initial de a2

    return a


def union(a1, a2):
    """Retourne l'automate qui reconnaît l'union des 
    langages reconnus par les automates a1 et a2""" 
    a1 = cp.deepcopy(a1)#on copie l'automate pour éviter les effets de bords
    a2 = cp.deepcopy(a2)
    a = automate()
    a.name = a1.name + " " + a2.name
    a.n = 1 + a1.n + a2.n #on rajoute un etat initial 1 pour l'union
    a.final = [q+1 for q in  a1.final] + [q+1+ a1.n for q in a2.final] #les etats finaux de a sont ceux de a1 et a2 mais avec un décalage de numérotation car on a rajouter un état

    for trans in a1.transition : 
        q, lettre = trans 
        a.transition[(q+1, lettre)] = [d+1 for d in a1.transition[trans]]#on rajoute les transition de a1 dans a mais avec un décalage pour cause de décalage de numérotation
    
    for trans in a2.transition : 
        q, lettre = trans 
        a.transition[(q+1+a1.n, lettre)] = [d+1+a1.n for d in a2.transition[trans]]

    a.ajoute_transition(0, 'E', [1, 1+a1.n])#on créer les transitions du nouvel état initial de a aux étst initiaux de a1 et a2

    return a


def etoile(a):
    """Retourne l'automate qui reconnaît l'étoile de Kleene du 
    langage reconnu par l'automate a""" 
    # Inspiration autre fonction du code, on évite les effets de bord ?
    a = cp.deepcopy(a)
    for etat in a.final :
        a.ajoute_transition(etat,'E',[0])

    return a


def acces_epsilon(a):
    """ retourne la liste pour chaque état des états accessibles par epsilon
        transitions pour l'automate a
        res[i] est la liste des états accessible pour l'état i
    """
    # on initialise la liste résultat qui contient au moins l'état i pour chaque état i
    res = [[i] for i in range(a.n)]
    for i in range(a.n):
        candidats = list(range(i)) + list(range(i+1, a.n))
        new = [i]
        while True:
            # liste des epsilon voisins des états ajoutés en dernier:
            voisins_epsilon = []
            for e in new:
                if (e, "E") in a.transition.keys():
                    voisins_epsilon += [j for j in a.transition[(e, "E")]]
            # on calcule la liste des nouveaux états:
            new = list(set(voisins_epsilon) & set(candidats))
            # si la nouvelle liste est vide on arrête:
            if new == []:
                break
            # sinon on retire les nouveaux états ajoutés aux états candidats
            candidats = list(set(candidats) - set(new))
            res[i] += new 
    return res


def supression_epsilon_transitions(a):
    """ retourne l'automate équivalent sans epsilon transitions
    """
    # on copie pour éviter les effets de bord     
    a = cp.deepcopy(a)
    res = automate()
    res.name = a.name
    res.n = a.n
    res.final = a.final
    # pour chaque état on calcule les états auxquels il accède
    # par epsilon transitions.
    acces = acces_epsilon(a)
    # on retire toutes les epsilon transitions
    res.transition = {c: j for c, j in a.transition.items() if c[1] != "E"}
    for i in range(a.n):
        # on ajoute i dans les états finals si accès à un état final:
        if (set(acces[i]) & set(a.final)):
            if i not in res.final:
                res.final.append(i)
        # on ajoute les nouvelles transitions en parcourant toutes les transitions
        for c, v in a.transition.items():
            if c[1] != "E" and c[0] in acces[i]:
                res.ajoute_transition(i, c[1], v)
    return res
        
        
def determinisation(a):
    """ retourne l'automate équivalent déterministe
        la construction garantit que tous les états sont accessibles
        automate d'entrée sans epsilon-transitions
    """        
    det_a = automate() # On cree l'automate deterministe
    liste_ensemble = [[0]]
    num_etat = 0
    if 0 in a.final :
        det_a.final = [0]
    
    while num_etat < len(liste_ensemble) :
        for lettre in 'abc':
            etats_decouverts = []
            for q in liste_ensemble[num_etat] :
                if (q,lettre) in a.transition.keys() :
                    etats_decouverts += a.transition[(q,lettre)]
            etats_decouverts = sorted(list(set(etats_decouverts))) # Pour éviter les doublons, et pour tout avoir toujours dans le même prdre
            if etats_decouverts : # Verifications qu'elle est pas libre 
                if not etats_decouverts in liste_ensemble : # On verifie qu'elle est pas vide
                    liste_ensemble.append(etats_decouverts)
                    if any([x in a.final for x in etats_decouverts]) : # Liste par comprehension pour gerer avec le mot clé any si un etat decouvert est dans les etats finaux de a
                        det_a.final.append(liste_ensemble.index(etats_decouverts))
                det_a.ajoute_transition(num_etat,lettre,[liste_ensemble.index(etats_decouverts),])
        num_etat += 1
    
    det_a.n = num_etat
    return det_a
    
    
def completion(a):
    """ retourne l'automate a complété
        l'automate en entrée doit être déterministe
    """
    a = cp.deepcopy(a)#on copie l'automate pour éviter les effets de bord
    etat_poub = a.n #on stock le numéro du nouvel état 
    a.n+= 1 #on incrémente 1 aux états car on rajoute l'état poubelle 

    for q in range(a.n) :
        for lettre in a.alphabet : 
            if (q, lettre) not in a.transition :
                a.transition[(q, lettre)] = [etat_poub]#on définit les transitions allant jusqu'à l'état poubelle

    return a


def minimisation(a):
    """ retourne l'automate minimum
        a doit être déterministe complet
        algo par raffinement de partition (algo de Moore)
    """
    # on copie pour éviter les effets de bord     
    a = cp.deepcopy(a)
    res = automate()
    res.name = a.name
    
    # Étape 1 : partition initiale = finaux / non finaux
    part = [set(a.final), set(range(a.n)) - set(a.final)]
    # on retire les ensembles vides
    part = [e for e in part if e != set()]  
    
    # Étape 2 : raffinement jusqu’à stabilité
    modif = True
    while modif:
        modif = False
        new_part = []
        for e in part:
            # sous-ensembles à essayer de séparer
            classes = {}
            for q in e:
                # signature = tuple des indices des blocs atteints pour chaque lettre
                signature = []
                for c in a.alphabet:
                    for i, e2 in enumerate(part):
                        if a.transition[(q, c)][0] in e2:
                            signature.append(i)
                # on ajoute l'état q à la clef signature calculée
                classes.setdefault(tuple(signature), set()).add(q)
            if len(classes) > 1:
                # s'il y a >2 signatures différentes on a séparé des états dans e
                modif = True
                new_part.extend(classes.values())
            else:
                new_part.append(e)
        part = new_part    
     
    # Étape 3 : on construit le nouvel automate minimal
    mapping = {}
    # on associe à chaque état q le nouvel état i
    # obtenu comme étant l'indice du sous-ensemble de part
    for i, e in enumerate(part):
        for q in e:
            mapping[q] = i

    res.n = len(part)
    res.final = list({mapping[q] for q in a.final if q in mapping})
    for i, e in enumerate(part):
        # on récupère un élément de e:
        representant = next(iter(e))
        for c in a.alphabet:
            q = a.transition[(representant, c)][0]
            res.transition[(i, c)] = [mapping[q]]
    return res
    

def tout_faire(a):
    a1 = supression_epsilon_transitions(a)
    a2 = determinisation(a1)
    a3 = completion(a2)
    a4 = minimisation(a3)
    return a4


def egal(a1, a2):
    """ retourne True si a1 et a2 sont isomorphes
        a1 et a2 doivent être minimaux
    """

    if a1.n != a2.n :
        return False
    if sorted(a1.final) != sorted(a2.final) :
        return False
    else :
        for trans in a1.transition.keys() :
            if trans not in a2.transition.keys():
                return False
            else :
                if sorted(a1.transition[trans]) != sorted(a2.transition[trans]) :
                    return False
        for trans2 in a2.transition.keys() :
            if trans2 not in a1.transition.keys():
                return False
            else :
                if sorted(a1.transition[trans]) != sorted(a2.transition[trans]) :
                    return False
                
    return True



# TESTS

def test_concatenation():
    """test de la fonction concaténatinon de 2 automates"""
    a1 = automate("a")
    a2 = automate("b")
    a = concatenation(a1, a2)

    assert a.n == 4 #on vérifier que le nombre d'états est 4
    assert a.final == [3] #on vérifie que l'état final est 3 
    assert(1, "E") in a.transition #on vérifier que la transition espilon existe
    assert a.transition[(1, "E")] == [2]#on vérifie que la transition epsilon va bien vers 2 
    print("test 1 réussi a.b")

    a3 = automate("c")
    a = concatenation(a1,a3)
    
    assert a.n == 4
    assert a.final == [3]
    assert(1, "E") in a.transition
    assert a.transition[(1, "E")] == [2]
    print("test 2 reussi")

def test_union():
    """test de la fonction union sur 2 automates"""
    a1 = automate("a")
    a2 = automate("b")
    a = union(a1, a2)

    assert a.n == 5 #on verifie que le nombre d'états est de 5
    assert sorted(a.final) == [2,4] #on vérifie les états finaux sont 2 et 4
    assert (0,"E") in a.transition #on vérifie que la transition epsilon depuis 0 existe
    assert len(a.transition[(0,"E")]) == 2 #on vérifie qu'il y a 2 transitions epsilon depuis 0
    assert 1 in a.transition[(0,"E")] #on vérifie que la transition allant de 0 à 1 existe
    assert 3 in a.transition[(0, "E")]#on vérifie que la transition allant de 0 à 3 existe 
    print("test 1 reussi")

    a3 = automate("c")
    a = union(a2,a3)

    assert a.n == 5
    assert sorted(a.final) == [2,4]
    assert (0, "E") in a.transition
    assert len(a.transition[(0, "E")]) == 2
    assert 1 in a.transition[(0, "E")]
    assert 3 in a.transition[(0, "E")]
    print("test 2 reussis ")

def test_completion():
    """test de la fonction completion d'un automate"""

    a1 = automate("a")
    a = completion(a1)

    assert a.n == 3 #on vérifie le nombre d'états est 3
    assert a.final == [1]  #on vérifie que l'éat final est 1

    for q in range(a.n):
        for lettre in ["a", "b", "c"]:
            assert(q, lettre) in a.transition#on vérifie qu'il y a bien toute les transitions
    print("test 1 reussi")

    a2 = automate("b")
    a = completion(a2)

    assert a.n == 3
    assert a.final == [1]

    for q in range(a.n):
        for lettre in ["a", "b", "c"]:
            assert(q, lettre) in a.transition
    print("test 2 reussis")




