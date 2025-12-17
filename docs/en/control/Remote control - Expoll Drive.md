# Remote control - Expoll Drive

## Architecture - Single network segment

```mermaid
flowchart BT

    expoll((☁️ Expoll)) == 🔒 HTTPS ==> datalink((☁️ Datalink))
    vlan == 🔒 MQTTS ==> datalink

    subgraph site [🏭 Industrial site]
        subgraph mcd [🖴 MCD]
            mcdLan[🔌 LAN]
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
    linkStyle 3 stroke:orange,stroke-width:3px,color:orange;
```

## Architecture - 2 network segments

```mermaid
flowchart BT
    expoll((☁️ expoll)) == 🔒 HTTPS ==> datalink((☁️ Datalink))
    mcdWan == 🔒 MQTTS ==>   datalink

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
The **Expoll Drive** solution enables **remote control** of an **MCD (MyClaugerDetect)** device installed at our customers' industrial sites, from the **Expoll** application integrated into our **MyPortal3E** digital portal.

Operation relies on a secure and reliable chain:
- The user interacts with the **Expoll** application from MyPortal3E.
- Requests are transmitted via **encrypted HTTPS** to our **Datalink data management platform**.
- Datalink acts as an **intermediate link**:
  - the **Datalink API** exposes a specific resource corresponding to the device,
  - the **MCD** subscribes (subscription to a *topic*) to this resource,
  - commands are thus relayed in a controlled manner to the MCD.
- The **MCD**, via its containerized applications, locally executes the requested actions (collection, processing, or control).

### Security and reliability
- **End-to-end encryption**: HTTPS between Expoll and Datalink, MQTTS between Datalink and MCD.
- **Authentication and authorizations** managed via the Datalink API.
- **No direct MCD exposure**: flows are outbound only from the customer site to Datalink, limiting the attack surface.
- **Resilience and monitoring** integrated into Datalink to ensure service reliability.

This architecture combines the **flexibility of remote control** with the **security of a controlled chain**, fully integrated within our ISMS perimeter.
