# Network Architectures (Mermaid)

Ce dépôt contient des **schémas d’architectures réseaux OT/IT** écrits en **Markdown + Mermaid**, puis exportés automatiquement en **PNG** et **PDF**.

---

## Pourquoi utiliser GitHub ?
Nous utilisons GitHub comme **bibliothèque centralisée de schémas** et outil de collaboration :
- Historique complet des modifications (qui / quand / quoi).
- Travail à plusieurs sans écraser le travail des autres (pull requests).
- Génération **automatique** des PNG et PDF lors des builds.
- Partage simple : les fichiers finaux sont disponibles dans la **Release “latest”**.

---

## Pourquoi Markdown + Mermaid ?
Les fichiers `.md` contiennent le **code Mermaid** qui décrit les diagrammes.  
Avantages :
- **Édition simple** : on modifie du texte, pas un dessin binaire.
- **Automatisation** : export en PNG/PDF sans retouche manuelle.
- **Interopérabilité** : une IA peut **lire et raisonner** sur ces descriptions textuelles.
- **Pérennité** : le format texte reste lisible et diffable.

Exemple minimal Mermaid :

~~~mermaid
graph TD
  A[Poste utilisateur] -->|VPN| B[Firewall]
  B --> C[Automate/PLC]
~~~

---

## Objectif du dépôt
Conserver nos **architectures “standard” / “de base”** (Remote Access, Data, etc.) pour servir de **socle réutilisable** et accélérer la déclinaison **pour les projets clients**.  
Les documents intègrent des **rappels de sécurité** inspirés de **IEC 62443** (zones & conduites) et **NIS 2** (cybersécurité OT/IT).

---

## Organisation
- `docs/remote-access` : variantes d’accès distant (Ewon, VPN client, PMAD, …)
- `docs/data` : variantes de collecte / transfert de données (Ewon datalogger, myClaugerDetect, SCADA, …)

Pour chaque `.md`, la CI publie :
- un **PNG** (aperçu visuel),
- un **PDF** (document prêt à partager).

---

## Comment consulter / utiliser
- Ouvrez les `.md` directement sur GitHub, dans **VS Code** (extension *Mermaid*), ou via **Mermaid Live Editor** : https://mermaid.live
- Récupérez les **PDF et PNG générés** dans la **dernière Release** : **[Releases › Latest](../../releases/latest)**.
- Pour une version figée (ex. livraison client), créez un **tag** `vX.Y.Z` ; une Release versionnée sera publiée automatiquement avec les mêmes assets.

---

## Notes sécurité dans les PDF
Les PDF rappellent des principes de base (exemples) :
- **Segmentation** par zones / conduites (IEC 62443) et filtrage inter-zones (pare-feu).
- **Accès distant** : authentification forte, principe du moindre privilège, journalisation.
- **Collecte de données** : flux sortants maîtrisés, chiffrement en transit, réduction de surface d’attaque.
Ces schémas sont des **modèles génériques** : ils doivent être **revus et adaptés** à chaque contexte client.

---

## Contribution
- Proposez vos changements via **pull request** (PR).
- Privilégiez un **schéma par fichier `.md`**.
- Ajoutez un court **contexte** en tête de fichier (objectif, périmètre, dépendances).

---

## Licence
MIT (sauf mention contraire).
