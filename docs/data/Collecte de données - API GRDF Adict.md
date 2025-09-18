# Collecte de données - API GRDF ADICT (Accès aux Données Individuelles des Clients par des Tiers)

## Architecture

```mermaid
flowchart LR
    datalink((☁️ Datalink)) == 🔒 HTTPS ==> grdf((🌐 API GRDF
    ADICT))
    datalink((☁️ Datalink)) == 🔒 HTTPS ==> myportal3e((☁️ MyPortal3E))

    linkStyle 0 stroke:orange,stroke-width:3px,color:orange;
    linkStyle 1 stroke:orange,stroke-width:3px,color:orange;
```

## Description