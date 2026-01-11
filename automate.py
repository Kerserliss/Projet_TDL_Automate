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

    a1 = cp.deepcopy(a1)
    a2 = cp.deepcopy(a2)
    a = automate()
    a.name = a1.name + " " + a2.name 
    a.n = a1.n + a2.n
    a.final = [q + a1.n for q in a2.final]

    for trans in a1.transition:
        a.transition[trans] = list(a1.transition[trans])

    for trans in a2.transition :
        q, lettre = trans
        a.transition[(q+a1.n, lettre)] = [d+ a1.n for d in a2.transition[trans]]

    for etat_final in a1.final : 
        a.ajoute_transition(etat_final, 'E', [a1.n])

    return a


def union(a1, a2):
    """Retourne l'automate qui reconnaît l'union des 
    langages reconnus par les automates a1 et a2""" 
    a1 = cp.deepcopy(a1)
    a2 = cp.deepcopy(a2)
    a = automate()
    a.name = a1.name + " " + a2.name
    a.n = 1 + a1.n + a2.n
    a.final = [q+1 for q in  a1.final] + [q+1+ a1.n for q in a2.final]

    for trans in a1.transition : 
        q, lettre = trans 
        a.transition[(q+1, lettre)] = [d+1 for d in a1.transition[trans]]
    
    for trans in a2.transition : 
        q, lettre = trans 
        a.transition[(q+1+a1.n, lettre)] = [d+1+a1.n for d in a2.transition[trans]]
    a.ajoute_transition(0, 'E', [1, 1+a1.n])

    return a


def etoile(a):
    """Retourne l'automate qui reconnaît l'étoile de Kleene du 
    langage reconnu par l'automate a""" 
    # Inspiration autre fonction du code, on évite les effets de bord ?
    a = cp.deepcopy(a)
    for etat in a.final :
        a.ajoute_transition(etat,'E',[0])
    a.final = sorted(a.final + [0])

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
    a = cp.deepcopy(a)
    etat_poub = a.n
    a.n+= 1

    for q in range(a.n) :
        for lettre in a.alphabet : 
            if (q, lettre) not in a.transition :
                a.transition[(q, lettre)] = [etat_poub]

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

#test concatenation 

a1 = automate("a")
a2 = automate("b")
a3 = automate("c")
a_concat = concatenation(a1,a2)
a_concat1 = concatenation(a1, a3)
a_concat2 = concatenation(a2, a3)
print(a_concat)
print(a_concat1)
print(a_concat2)

#test union 
a_union = union(a1,a2)
a_union1 = union(a1,a3)
a_union2 = union(a2,a3)
print(a_union)

#test complementation
a_complet = completion(a1)
a_complet1 = completion(a2)
a_complet2 = completion(a3)
print(a_complet)
print(a_complet1)
print(a_complet2)

def test_etoile():
    """
    TEST N°1
    On teste l'étoile de Kleene de l'automate reconnaissant a
    """
    a1 = automate("a")
    a = etoile(a1)
    # Assert permet de lever une assertion error si jamais ce qu'il evalue est faux, cela permet de tester les fonctions 
    
    assert a.n == a1.n # Vérifie que c'est le même nombre d'état, on en rajoute pas 
    assert a.final == [0,1] # On vérifie que c'est bien le même état final ainsi que l'état 0
    assert (1, "E") in a.transition # On verifie que la transition de etat final epsilon existe
    assert a.transition[(1, "E")] == [0] # On vérifie que la transition renvoie bien vers l'état epsilon. 

    """
    TEST N°2
    On teste l'étoile de Kleene de l'automate reconnaissant aa
    """

    # Ici on reprends la même idée de ce qui a été écrit au dessus, mais on crée notre automate de base nous même
    a1 = automate("a")
    a1.n = 3
    a1.final = [2] 
    a1.transition = {(0, "a"): [1], (1, "a"): [2]}
    a = etoile(a1)

    # Même commentaire
    assert a.n == 3
    assert a.final == [0,2]
    assert (2, "E") in a.transition
    assert a.transition[(2, "E")] == [0]


def test_determinisation():
    """
    TEST N°1
    On teste la determination d'un automate non deterministe ab+a
    """
    a = automate("a")
    a.ajoute_transition(0,"a",[1]) # Premier cas a
    a.ajoute_transition(0,"a",[2]) # Deuxième cas : a pour ensuite b
    a.ajoute_transition(2,"b",[3]) # 2 vers 3 avec b
    a.final = [1,3]
    a.n = 4
    a = determinisation(a)
    assert a.n == 3 # L'etat 1 et 2 sont regroupés ensemble donc on perd un état
    assert a.final == [1, 2] # 1 et 2 parce qu'on a le cas juste a et le cas ab
    assert (0, "a") in a.transition 
    assert a.transition[(0, "a")] == [1]
    assert a.transition[(1, "b")] == [2]

    """
    TEST N°2
    On teste la déterminisation d'un automate déterministe par exemple juste b.
    """
    a = automate("b")
    a = determinisation(a)
    assert a.n == 2 # On change pas de nombre d'etat
    assert a.final == [1] # On change pas l'état final
    assert (0, "b") in a.transition # On a bien l'unique transition b
    assert a.transition[(0, "b")] == [1] # Qui mène bien vers 1

def test_egal():
    """
    TEST N°1 
    On test l'égalité entre deux automates qui sont simplement a et a
    """
    # Creation des deux automates
    a1 = automate("a") 
    a2 = automate("a")

    # On fait tout comme on le ferait
    a1 = tout_faire(a1)
    a2 = tout_faire(a2)
    # On verifie l'egalité dans les deux sens
    assert egal(a1, a2)
    assert egal(a2, a1)

    """
    TEST N°2
    On test l'égalité entre deux automates différents comme acb et bc
    """

    a1 = automate("a")
    a2 = automate("b")

    #Definition du premier automate
    a1.n = 4
    a1.final = [3]
    a1.ajoute_transition(0, "a", [1])
    a1.ajoute_transition(1, "b", [2])
    a1.ajoute_transition(2, "c", [3])

    #Definition du deuxième automate

    a2.n = 3
    a2.final = [2]
    a1.ajoute_transition(0, "b", [1])
    a1.ajoute_transition(1, "c", [2])

    # On fait tout comme indiqué
    a1 = tout_faire(a1)
    a2 = tout_faire(a2)

    #On fait notre égalité
    assert not egal(a1, a2)
    assert not egal(a2, a1)

if __name__ == "__main__":
    test_etoile()
    test_egal()
    test_determinisation()

