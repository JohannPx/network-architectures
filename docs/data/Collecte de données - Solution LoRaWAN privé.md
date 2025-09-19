# Collecte de données - Solution LoRaWAN privé

## Architecture

```mermaid
flowchart LR

    subgraph site [🏭 Site industriel]
        
        subgraph gw [📡 Gateway]
            gwWan[🔌 WAN ou 📡 MODEM]
        end
        sensor1([📟 Capteur 1]) == 🔒 LoRa ==> gw
        sensor2([📟 Capteur 2]) == 🔒 LoRa ==> gw
    end

    gwWan == 🔒 HTTPS ==> myportal3e((☁️ MyPortal3E))

    linkStyle 0 stroke:blue,stroke-width:3px,stroke-dasharray: 5 5 ,color:blue;
    linkStyle 1 stroke:blue,stroke-width:3px,stroke-dasharray: 5 5 ,color:blue;
    linkStyle 2 stroke:orange,stroke-width:3px,color:orange;
```

## Description
Cette architecture met en œuvre une solution de collecte de données sans fil LoRaWAN adaptée aux environnements industriels.  
Les capteurs, généralement alimentés par batterie, transmettent leurs mesures en utilisant le protocole radio LoRa vers une Gateway LoRaWAN privée fournie dans le cadre de la solution.  

La Gateway agit comme point de collecte local et relaie les données de manière sécurisée vers notre plateforme digitale MyPortal3E :  
- Les capteurs rejoignent le réseau via la procédure sécurisée Join-OTA (Over The Air Activation), garantissant l’authenticité et la confidentialité des échanges radio.  
- La Gateway transmet ensuite les données en HTTPS chiffré vers MyPortal3E, soit :  
  - via un accès Internet mobile (réseau Orange en Europe étendue),  
  - soit via un réseau client, avec des flux sortants strictement maîtrisés.  

Pour des raisons de cybersécurité, la configuration de la Gateway est durcie :  
- usage d’un compte local unique et protégé,  
- réduction de la surface d’attaque par la désactivation des services non utilisés,  
- limitation stricte de la connectivité (flux sortants uniquement vers les services autorisés).  

Cette solution est autonome et non intrusive vis-à-vis du SI ou du réseau client, tout en assurant une collecte sécurisée de bout en bout, depuis le capteur jusqu’à la plateforme MyPortal3E.  

## Avantages clés
- Autonomie énergétique : capteurs sur batterie, faible consommation.  
- Connectivité sans fil longue portée : protocole LoRa adapté aux environnements industriels.  
- Non intrusif : pas d’impact sur le SI ou le réseau client.  
- Sécurité renforcée : Join-OTA, chiffrement HTTPS, durcissement de la Gateway.  
- Flexibilité de déploiement : transmission via Internet mobile (Europe étendue) ou réseau client.  
- Simplicité de mise en œuvre : installation rapide, sans câblage supplémentaire.  
