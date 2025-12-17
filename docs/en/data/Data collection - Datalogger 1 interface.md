# Data collection - Datalogger 1 interface

## Architecture

```mermaid
flowchart BT

    subgraph site [🏭 Customer site]
        subgraph automation [🖲️ Automation]
            plc([📟 PLC])
        end

        vlan(Dedicated VLAN)

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

## Description
The data collection solution is based on installing an industrial **datalogger** at our customers' sites.
This datalogger directly queries equipment in the automation zone via **field protocols** (Modbus/TCP, S7, etc.), temporarily stores data locally, then transmits it via **encrypted HTTPS** to our **MyPortal3E** digital platform.

The datalogger is based on the **HMS Ewon Flexy** product, specifically configured for data collection:
- The datalogger is connected only to the automation network and pushes data to the Internet via an existing VLAN or proxy.
- For data collection purposes, the datalogger can be deployed **without routing function and without VPN**, to limit the exposure surface and meet simplicity requirements.

In accordance with our **security policy**, the datalogger configuration is **hardened**:
- disabling unused services,
- outbound-only flow protection,
- integration into our ISO 27001 certified ISMS, aligned with IEC 62443 and NIS 2.

Thus, collection is **secure, governed, and controlled**: only data contractually defined with the customer is transmitted, via a TLS encrypted channel, to our MyPortal3E infrastructure hosted in compliance with our ISMS.
