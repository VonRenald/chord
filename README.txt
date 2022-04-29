# Chord
 TP M1 SECIL SD

 v1: le port unique est de 8001
    python3 chord_v1.0.py
 
 v2: les noeud sont en gestion des clés entre lui et le prochain noeud
    python3 chord_v2.4.py <port> #premier noeud
    python3 chord_v2.4.py <port> <ip connection> <port connexion> #rajouter un noeud
    python3 chord_v2.4.py <port> <identifiant> <ip connection> <port connexion> #rajouter un noeud en choisissant son identifiant de connexion

 v3: les noeud sont en gestion des clés entre lui et son precedant 
    python3 chord_v3.4.py <port> #premier noeud
    python3 chord_v3.4.py <port> <ip connection> <port connexion> #rajouter un noeud
    python3 chord_v3.4.py <port> <identifiant> <ip connection> <port connexion> #rajouter un noeud en choisissant son identifiant de connexion
