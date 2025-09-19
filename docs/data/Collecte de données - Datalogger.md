# Collecte de données - Datalogger

## Architecture - 1 seul segment réseau

```mermaid
flowchart BT

    subgraph site [🏭 Site client]
        subgraph automation [🖲️ Automatisme]
            plc([📟 API])
        end

        vlan(VLAN dédié)
        
        subgraph ewon [🖴 Datalogger]
            ewonLan[🔌 LAN]
        end
    end

    myportal3e((☁️ MyPortal3E))

    vlan == 🔒 HTTPS ==> myportal3e
    automation === vlan
    vlan === ewon
    
    linkStyle 0 stroke:orange,stroke-width:3px,color:orange;
    linkStyle 2 stroke:orange,stroke-width:3px,color:orange;
```

## Architecture - 2 segments réseau

```mermaid
flowchart BT

    subgraph site [🏭 Site industriel]
        subgraph automation [🖲️ Automatisme]
            plc([📟 API])
        end

        vlan(LAN autonome ou VLAN dédié)
        
        subgraph ewon [🖴 Datalogger]
            ewonLan[🔌 LAN]
            ewonWan[🔌 WAN ou 📡 MODEM]
        end
    end

    myportal3e((☁️ MyPortal3E))

    ewonWan == 🔒 HTTPS ==> myportal3e
    automation === vlan
    vlan === ewonLan
    
    linkStyle 0 stroke:orange,stroke-width:3px,color:orange;
```
## Description
La solution de collecte de données repose sur l’installation d’un **datalogger** industriel chez nos clients.  
Ce datalogger interroge directement les équipements de la zone automatisme via les **protocoles de terrain** (Modbus/TCP, S7, etc.), stocke temporairement les données localement, puis les transmet en **HTTPS chiffré** vers notre plateforme digitale **MyPortal3E**.  

Le datalogger est basé sur le produit **HMS Ewon Flexy**, configuré spécifiquement pour la collecte de données :  
- Dans une architecture **à une seule interface LAN**, le datalogger est relié uniquement au réseau automatisme et pousse les données vers Internet via un VLAN ou un proxy existant.  
- Dans une architecture **à deux interfaces (LAN + WAN)**, le datalogger assure la **segmentation entre réseau industriel et réseau externe**. Dans ce cas, l’interface WAN peut être connectée soit au réseau IT client, soit à un modem 4G, et la fonction VPN peut être activée si nécessaire.  
- Dans le cadre de la collecte de données, le datalogger peut être déployé **sans fonction de routage et sans VPN**, afin de limiter la surface d’exposition et de répondre à des besoins de simplicité.  

Conformément à notre **politique de sécurité**, la configuration du datalogger est **endurcie** :  
- désactivation des services non utilisés,  
- séparation stricte LAN/WAN lorsque applicable,  
- protection des flux sortants (*outbound only*),  
- mise à jour régulière des firmwares et gestion proactive des vulnérabilités,  
- authentification et gestion des comptes selon le principe du moindre privilège,  
- intégration dans notre SMSI certifié ISO 27001, alignée sur IEC 62443 et NIS 2.  

Ainsi, la collecte est **sécurisée, gouvernée et maîtrisée** : seules les données contractuellement définies avec le client sont transmises, via un canal chiffré TLS, vers notre infrastructure MyPortal3E hébergée de manière conforme à notre SMSI.  
