# Accès distant - Solution VPN client

## Architecture

```mermaid
flowchart TB

    remote([💻 PC distant])

    internet((🌐 Internet))

    subgraph site [🏭 Site client]
        fw(🛡️ Pare-feu 🧱)
        vlan@{ shape: das, label: "VLAN dédié" }
        jumpServer([🖥️ Poste
        de rebond])
        subgraph automation [🖲️ Automatisme]
            direction RL
            plc([📟 API])
            hmi([🎛️ IHM])
            gtc([💻 GTC])
        end
    end

    remote e2@== 🔒 VPN ==> internet
    e2@{ animation: fast }

    internet e1@== 🔒 VPN ==> fw
    e1@{ animation: fast }

    fw e3@=== vlan
    e3@{ animation: fast }

    fw e5@==> jumpServer
    e5@{ animation: fast }

    jumpServer === automation

    vlan e4@==> automation
    e4@{ animation: fast }

    linkStyle 0 stroke:orange,stroke-width:3px,color:orange;
    linkStyle 1 stroke:orange,stroke-width:3px,color:orange;
    linkStyle 2 stroke:orange,stroke-width:3px,color:orange;
    linkStyle 3 stroke:orange,stroke-width:3px,color:orange;
    linkStyle 5 stroke:orange,stroke-width:3px,color:orange;
```

### Légende
- 💻 = PC distant (technicien)  
- 🌐 = Internet  
- 🏭 = Site client  
- 🛡️🧱 = Pare-feu (filtrage, terminaison VPN)  
- 🖥️ = Serveur/poste de rebond (jump server / bastion)  
- 🖲️ = Zone Automatisme  
- 📟 = Automate (API/PLC)  
- 🎛️ = IHM  
- 💻 = GTC (supervision locale)  
- 🔒 = VPN chiffré  
- VLAN dédié = Segment réseau isolé pour la télémaintenance  


## Description
Cette architecture illustre l’accès distant par **solution VPN client** :  
- Le **poste distant** (PC 💻) de l’intervenant établit un tunnel **VPN chiffré** vers le **pare-feu du site client**.  
- Le **pare-feu** contrôle et limite les flux entrants.  
- L’accès au réseau automatisme se fait ensuite :  
  - soit via un **VLAN dédié**, l’intervenant utilise directement son poste avec le logiciel d’ingénierie pour **modifier les programmes automates** et peut accéder aux serveurs **VNC**, **RDP** et **Web** disponibles sur ce VLAN (automates 📟, IHM 🎛️, supervision locale 💻 GTC),  
  - soit via un **poste de rebond** 🖥️, auquel il se connecte à distance : dans ce cas, l’intervenant est limité aux **outils installés et mis à disposition** sur ce poste.  
- Cette segmentation réduit la surface d’attaque et permet un **contrôle précis des flux par le pare-feu**.


