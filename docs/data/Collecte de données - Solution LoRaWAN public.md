# Collecte de données - Solution LoRaWAN public

## Architecture

```mermaid
flowchart LR

    sensor1== 🔒 LoRa ==> gw((📡 Gateway
    publique))
    sensor2== 🔒 LoRa ==> gw

    subgraph site [🏭 Site industriel]
        sensor1([📟 Capteur 1]) 
        sensor2([📟 Capteur 2])
    end

    gw == 🔒 HTTPS ==> Datalink((☁️ Datalink))
    Datalink == 🔒 HTTPS ==> myportal3e((☁️ MyPortal3E))

    linkStyle 0 stroke:blue,stroke-width:3px,stroke-dasharray: 5 5 ,color:blue;
    linkStyle 1 stroke:blue,stroke-width:3px,stroke-dasharray: 5 5 ,color:blue;
    linkStyle 2 stroke:orange,stroke-width:3px,color:orange;
    linkStyle 3 stroke:orange,stroke-width:3px,color:orange;
```

## Description