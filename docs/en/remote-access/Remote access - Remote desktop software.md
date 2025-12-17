# Remote access - Remote Desktop Software (PMAD)

## Architecture

```mermaid
flowchart LR

    remote([💻 Remote PC])

    pmad((☁️ AnyDesk,
    TeamViewer,
    ...))

    subgraph site [🏭 Industrial site]
        fw[🛡️ Firewall 🧱]
        jumpAera(Jump zone)
        vlanAutomation(Dedicated VLAN)
        jumpServer([🖥️ Jump server
        or
        BMS])
        subgraph automation [🖲️ Automation]
            direction RL
            plc([📟 PLC])
            hmi([🎛️ HMI])
        end
    end

    remote == 🔒 ==> pmad
    fw == 🔒 ==> pmad
    jumpAera == 🔒 === fw
    jumpServer == 🔒 === jumpAera
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

## Description
This architecture implements **remote desktop access (PMAD)** via a cloud service (e.g., **AnyDesk / TeamViewer**):
- The **remote workstation** establishes an **encrypted PMAD session** to the **cloud service** (access broker).
- The **customer site** also initiates an **encrypted outbound connection** from the **firewall** to the **PMAD service**; no unsolicited incoming flow is required.
- The **jump server** (or the **BMS** if used as an access point) resides in a **dedicated Jump zone for remote access**. Once the session is established by the broker, the technician operates **from this jump server** with the **installed tools** (e.g., VNC client, RDP, web browser, engineering software).
- The **automation equipment** (PLC, HMI) is isolated in a separate **Automation VLAN**; flows from the **Jump zone** to this **Automation VLAN** are **strictly filtered** at the firewall (whitelist by protocol/port/IP).
- Security recommendations: **MFA** on PMAD accounts, **domain/IP restriction** to the PMAD cloud, **session logging**, named accounts on the jump server, and **"deny all" policy** by default with minimal openings on the site side.
