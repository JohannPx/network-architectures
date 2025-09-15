# Accès distant - Logiciel prise de main à distance (PMAD)

## Architecture

```mermaid
flowchart BT

    remote([💻 PC distant])

    pmad((☁️ AnyDesk,
    TeamViewer,
    ...))

    subgraph site [🏭 Site client]
        fw(🛡️ Pare-feu 🧱)
        jumpAera@{ shape: das, label: "Zone de rebond" }
        vlanAutomation@{ shape: das, label: "VLAN dédié" }
        jumpServer([🖥️ Poste de rebond
        ou
        GTC])
        subgraph automation [🖲️ Automatisme]
            direction RL
            plc([📟 API])
            hmi([🎛️ IHM])
        end
    end

    remote e2@== 🔒 ==> pmad
    e2@{ animation: fast }

    fw e1@== 🔒 ==> pmad
    e1@{ animation: fast }

    jumpAera e3@ == 🔒 === fw
    e3@{ animation: fast }

    jumpServer e4@ == 🔒 === jumpAera
    e4@{ animation: fast }

    vlanAutomation === fw

    automation === vlanAutomation

    jumpServer --- jumpAera

    jumpAera --- fw

    linkStyle 0 stroke:orange,stroke-width:3px,color:orange;
    linkStyle 1 stroke:orange,stroke-width:3px,color:orange;
    linkStyle 2 stroke:orange,stroke-width:3px,color:orange;
    linkStyle 3 stroke:orange,stroke-width:3px,color:orange;
    linkStyle 4 stroke:blue,stroke-width:2px;
    linkStyle 5 stroke:blue,stroke-width:2px;
    linkStyle 6 stroke:blue,stroke-width:2px;
    linkStyle 7 stroke:blue,stroke-width:2px;

```

### Légende
- 💻 = PC distant (intervenant)  
- ☁️ = Service PMAD cloud (AnyDesk / TeamViewer)  
- 🏭 = Site client  
- 🛡️🧱 = Pare-feu (filtrage, sorties contrôlées)  
- 🖥️ = Poste de rebond (ou GTC utilisée comme point d’appui)  
- 🖲️ = Zone Automatisme  
- 📟 = Automate (API/PLC)  
- 🎛️ = IHM  
- 🔒 = Lien chiffré (PMAD / VPN / TLS)  
- **Zone de rebond** = Zone sécurisée dédiée aux accès distants et au poste de rebond  
- **VLAN Automatisme** = Segment de la zone Automatisme (équipements industriels)  
- **Couleurs de liens (ex.)** : **orange** = liaisons PMAD via Internet ; **bleu** = liaisons internes site (Zone de rebond ↔ VLAN Automatisme)  

## Description
Cette architecture met en œuvre une **prise en main à distance (PMAD)** via un service cloud (ex. **AnyDesk / TeamViewer**) :  
- Le **poste distant** établit une session **PMAD chiffrée** vers le **service cloud** (courtier d’accès).  
- Le **site client** initie lui aussi une connexion **sortante chiffrée** depuis le **pare-feu** vers le **service PMAD** ; aucun flux entrant non sollicité n’est requis.  
- Le **poste de rebond** 🖥️ (ou la **GTC** si elle sert de point d’appui) réside dans une **Zone de rebond dédiée aux accès distants**. Une fois la session établie par le courtier, l’intervenant agit **depuis ce poste de rebond** avec les **outils installés** (ex. client VNC, RDP, navigateur Web, logiciels d’ingénierie).  
- Les **équipements d’automatisme** (API/PLC, IHM) sont isolés dans un **VLAN Automatisme** distinct ; les flux depuis la **Zone de rebond** vers ce **VLAN Automatisme** sont **strictement filtrés** au pare-feu (liste blanche par protocole/port/IP).  
- Recommandations sécurité : **MFA** sur les comptes PMAD, **restriction par domaine/IP** vers le cloud PMAD, **journalisation** des sessions, comptes nominatifs sur le poste de rebond, et **politique « deny all »** par défaut avec ouvertures minimales côté site.  
