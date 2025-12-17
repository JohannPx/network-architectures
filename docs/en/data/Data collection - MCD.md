# Data collection - MCD (MyClaugerDetect)

## Architecture - Single network segment

```mermaid
flowchart BT

    subgraph site [🏭 Industrial site]
        subgraph automation [🖲️ Automation]
            plc([📟 PLC])
        end

        vlan(Dedicated VLAN)

        subgraph mcd [🖴 MCD]
            mcdLan[🔌 LAN]
        end
    end

    myportal3e((☁️ MyPortal3E))

    vlan == 🔒 MQTTS ==> datalink((☁️ Datalink)) == 🔒 HTTPS ==> myportal3e((☁️ MyPortal3E))
    automation === vlan
    vlan === mcdLan

    linkStyle 0 stroke:orange,stroke-width:3px,color:orange;
    linkStyle 1 stroke:orange,stroke-width:3px,color:orange;
    linkStyle 3 stroke:orange,stroke-width:3px,color:orange;
```

## Architecture - 2 network segments

```mermaid
flowchart BT

    mcdWan == 🔒 MQTTS ==> datalink((☁️ Datalink)) == 🔒 HTTPS ==> myportal3e((☁️ MyPortal3E))

    subgraph site [🏭 Customer site]
        subgraph mcd [🖴 MCD]
            mcdLan[🔌 LAN]
            mcdWan[🔌 WAN or 📡 MODEM]
        end
        vlan(Dedicated VLAN)
        subgraph automation [🖲️ Automation]
            plc([📟 PLC])
        end
    end

    automation === vlan
    vlan === mcdLan

    linkStyle 0 stroke:orange,stroke-width:3px,color:orange;
    linkStyle 1 stroke:orange,stroke-width:3px,color:orange;
```

## Description
The **MyClaugerDetect (MCD)** solution is based on installing an **industrial Linux PC**, equipped with **containerized applications** for collecting and locally enriching data from automation networks.

The MCD queries equipment via **field protocols** (PLC, HMI, sensors), processes and structures the data, then transmits it **securely and encrypted** using the **MQTTS** protocol to our **Datalink data management platform**.
Datalink then handles transformation, governance, and flow monitoring before delivering the data via **encrypted HTTPS** to our **MyPortal3E** digital platform.

Key features:
- No VPN function: the MCD is limited to local data collection and processing.
- Architecture possible in **single network segment** (dedicated LAN) or in **2 segments** (LAN + WAN/modem) to ensure segmentation and enhance security.
- Application containers enable **flexibility and scalability** in integrating new features or connectors.
- The entire solution is integrated within our **ISO 27001 certified ISMS** perimeter, aligned with **IEC 62443** and **NIS 2** frameworks.

This architecture guarantees an **end-to-end secure collection chain**, from the field to the MyPortal3E portal, with strict flow control and clearly established governance responsibilities.
