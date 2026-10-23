"""Génère en/index.html à partir de index.html (français, version de référence).
Chaque texte français est remplacé par sa traduction ; le script signale tout texte resté en français.
python3 tools/make-en.py"""
import re, pathlib

root = pathlib.Path(__file__).resolve().parent.parent
fr = (root / 'index.html').read_text(encoding='utf-8')

T = [
 # <head>
 ('<html lang="fr">', '<html lang="en">'),
 ('<title>SQLVault Gateway · Accès sécurisé aux bases de données bancaires</title>', '<title>SQLVault Gateway · Secure access to banking databases</title>'),
 ("SQLVault Gateway contrôle et trace chaque accès aux bases de données de la banque : données sensibles masquées, double validation des modifications, rapports automatiques et journal d'audit infalsifiable. Oracle, SQL Server, PostgreSQL, MySQL, MariaDB.",
  "SQLVault Gateway controls and records every access to a bank's databases: sensitive data masked, every change approved by a second person, automated reports and a tamper-evident audit log. Oracle, SQL Server, PostgreSQL, MySQL, MariaDB."),
 ('<meta property="og:locale" content="fr_FR">', '<meta property="og:locale" content="en_US">'),
 ('SQLVault Gateway · Qui a consulté les données de vos clients hier ?', 'SQLVault Gateway · Who accessed your customers\' data yesterday?'),
 ("Masquage des données sensibles, validation à quatre yeux, rapports automatiques et journal d'audit infalsifiable, pour toutes les bases de la banque.",
  "Sensitive data masking, four-eyes approval, automated reports and a tamper-evident audit log, for every database in the bank."),
 ("Passerelle d'accès sécurisé aux bases de données bancaires : masquage, double validation, rapports planifiés, journal d'audit chaîné.",
  "Secure access gateway for banking databases: masking, dual approval, scheduled reports, chained audit log."),
 ('"inLanguage":"fr"', '"inLanguage":"en"'),
 # navigation
 ('Aller au contenu', 'Skip to content'), ('SQLVault Gateway, accueil', 'SQLVault Gateway, home'), ('Ouvrir le menu', 'Open menu'),
 ('Navigation principale', 'Main navigation'),
 ('>Principe</a>', '>How it works</a>'), ('>Fonctionnalités</a>', '>Features</a>'), ('>Fonctionnement</a>', '>Request flow</a>'),
 ('>Démo</a>', '>Demo</a>'), ('>Sécurité</a>', '>Security</a>'), ('>Documents</a>', '>Documents</a>'), ('>FAQ</a>', '>FAQ</a>'),
 ('Demander un pilote</a>', 'Request a pilot</a>'),
 # accroche
 ('Accès sécurisé aux bases de données bancaires</p>', 'Secure access to banking databases</p>'),
 ('Qui a consulté les données de vos clients hier&nbsp;?', 'Who accessed your customers’ data yesterday?'),
 ("SQLVault Gateway est le point de passage unique et contrôlé entre vos équipes et les bases de données de la banque. Chacun ne voit que ce dont il a besoin, aucune modification ne part sans double validation, et chaque accès laisse une trace impossible à effacer.",
  "SQLVault Gateway is the single, controlled path between your teams and the bank's databases. Everyone sees only what they need, no change goes through without a second approval, and every access leaves a trace that cannot be erased."),
 ('Demander un pilote de 4 semaines', 'Request a 4-week pilot'), ('Voir la vidéo (1 min 38)', 'Watch the video (1 min 38, in French)'),
 ('Rien à installer sur les postes', 'Nothing to install on workstations'), ('Hébergé dans votre infrastructure', 'Hosted in your own infrastructure'),
 ('Aucune donnée ne quitte la banque', 'No data leaves the bank'),
 ('sqlvault.votre-banque.sn', 'sqlvault.your-bank.com'),
 ('Éditeur SQL de SQLVault Gateway : IBAN et soldes masqués pour une analyste', 'SQLVault Gateway SQL editor: IBAN and balances masked for an analyst'),
 # moteurs
 ('Bases de données compatibles', 'Supported databases'), ("Compatible avec vos bases, telles qu'elles sont", 'Works with your databases as they are'),
 # schéma
 ('Avant / après</p>', 'Before / after</p>'),
 ('Un seul passage contrôlé entre vos équipes et vos bases', 'One controlled path between your teams and your databases'),
 ("<strong>Aujourd'hui</strong><span>Chaque poste se connecte directement à chaque base de production.</span>",
  '<strong>Today</strong><span>Every workstation connects directly to every production database.</span>'),
 ('Six postes de travail reliés directement aux quatre bases de production, par une multitude de connexions croisées',
  'Six workstations connected directly to the four production databases through a tangle of crossing connections'),
 ('Qui a lu quoi ? Qui a modifié quoi ?', 'Who read what? Who changed what?'),
 ('<strong>Avec SQLVault Gateway</strong><span>Toutes les requêtes passent par un point unique qui analyse, masque, fait valider et trace.</span>',
  '<strong>With SQLVault Gateway</strong><span>Every query goes through a single point that analyses, masks, gets approval and records.</span>'),
 ("Six postes de travail reliés à SQLVault Gateway, seul point d'accès aux quatre bases de production",
  'Six workstations connected to SQLVault Gateway, the only access point to the four production databases'),
 ('1 · Analyse<', '1 · Analysis<'), ('2 · Décision<', '2 · Decision<'), ('3 · Masquage<', '3 · Masking<'), ('4 · Traçabilité<', '4 · Audit trail<'),
 # constat
 ('>Le constat</p>', '>The problem</p>'),
 ("Les données des clients sont le premier actif de la banque. Leur accès est souvent le moins contrôlé.",
  "Customer data is a bank's most valuable asset. Access to it is often the least controlled."),
 ('<h3>Des accès directs à la production</h3>', '<h3>Direct access to production</h3>'),
 ("Analystes, développeurs et prestataires se connectent aux bases avec des outils installés sur leur poste. Chacun voit tout, y compris les numéros de compte et de carte.",
  "Analysts, developers and contractors connect to databases with tools installed on their workstations. Everyone sees everything, including account and card numbers."),
 ('<h3>Des modifications sans contrôle</h3>', '<h3>Unchecked changes</h3>'),
 ("Une correction urgente, un oubli de condition, et des milliers de lignes sont modifiées en production, sans que personne ne l'ait validé.",
  "One urgent fix, one missing condition, and thousands of production rows are changed without anyone having approved it."),
 ('<h3>Des preuves difficiles à produire</h3>', '<h3>Evidence that is hard to produce</h3>'),
 ("Lors d'un audit ou d'une inspection, il est long, voire impossible, de dire avec certitude qui a consulté quoi, quand et depuis quel poste.",
  "During an audit or an inspection, it takes a long time, if it is possible at all, to say for certain who accessed what, when and from which workstation."),
 # fonctionnalités
 ('>La solution</p>', '>The solution</p>'), ('Six garanties, dans un seul outil', 'Six guarantees in a single tool'),
 ('<h3>Chacun ne voit que ce dont il a besoin</h3>', '<h3>Everyone sees only what they need</h3>'),
 ("Les informations sensibles (IBAN, cartes, soldes, coordonnées) sont masquées automatiquement selon la fonction de la personne, jusque dans les exports Excel. Neuf modes de masquage, dont le format carte bancaire PCI DSS.",
  "Sensitive data (IBANs, cards, balances, contact details) is masked automatically according to each person's role, including in Excel exports. Nine masking modes, including the PCI DSS card format."),
 ("<h3>Aucune modification sans double validation</h3>", "<h3>No change without a second approval</h3>"),
 ("Toute correction de données devient une demande justifiée, approuvée par une deuxième personne avant d'être exécutée. Personne ne valide sa propre demande.",
  "Every data correction becomes a justified request, approved by a second person before it runs. Nobody approves their own request."),
 ('<h3>Les erreurs graves sont empêchées</h3>', '<h3>Serious mistakes are prevented</h3>'),
 ("Suppression de table, modification sans condition, requêtes multiples, motif d'injection : la requête est bloquée avant d'atteindre la base, avec un motif clair et une alerte de sécurité.",
  "Dropping a table, updating without a condition, stacked queries, injection patterns: the query is blocked before it reaches the database, with a clear reason and a security alert."),
 ('<h3>Des rapports automatiques et sécurisés</h3>', '<h3>Automated, secure reports</h3>'),
 ("Les extractions envoyées à la main sont remplacées par des rapports Excel planifiés, validés par un responsable, toujours masqués, et téléchargeables par les collègues autorisés.",
  "Hand-made extracts are replaced by scheduled Excel reports, approved by a manager, always masked, and downloadable by authorised colleagues."),
 ('<h3>Une trace impossible à effacer</h3>', '<h3>A trace that cannot be erased</h3>'),
 ("Chaque accès est inscrit dans un journal d'audit signé et chaîné : qui, quoi, quand, depuis quel poste, avec quel rôle. Une seule ligne retouchée est détectée.",
  "Every access is written to a signed, chained audit log: who, what, when, from which workstation, with which role. A single altered line is detected."),
 ('<h3>Un vrai éditeur SQL, dans le navigateur</h3>', '<h3>A real SQL editor, in the browser</h3>'),
 ("Autocomplétion, explorateur de tables, plan d'exécution, favoris partagés, exports : vos équipes gardent leur confort de travail, sans client SQL sur les postes.",
  "Autocompletion, table explorer, execution plans, shared favourites, exports: your teams keep a comfortable way of working, with no SQL client on their workstations."),
 # fonctionnement
 ('>Fonctionnement</p>', '>Request flow</p>'),
 ('Chaque requête suit le même parcours, en quelques millisecondes', 'Every query follows the same path, in a few milliseconds'),
 ('<h3>Analyse</h3>', '<h3>Analysis</h3>'),
 ("La requête est lue avant d'atteindre la base. Les opérations interdites sont bloquées.", 'The query is read before it reaches the database. Forbidden operations are blocked.'),
 ('<h3>Décision</h3>', '<h3>Decision</h3>'),
 ("Une lecture s'exécute aussitôt. Une modification part en double validation.", 'A read runs immediately. A change goes to dual approval.'),
 ('<h3>Masquage</h3>', '<h3>Masking</h3>'),
 ('Les colonnes sensibles sont masquées dans le résultat, selon le rôle de la personne.', "Sensitive columns are masked in the result, according to the person's role."),
 ('<h3>Traçabilité</h3>', '<h3>Audit trail</h3>'),
 ("La requête, acceptée ou refusée, est inscrite dans le journal d'audit chaîné.", 'The query, accepted or refused, is written to the chained audit log.'),
 ('Une administration répartie : personne ne détient seul toutes les clés', 'Split administration: no one holds all the keys'),
 ('<strong>Administrateur technique</strong><span>déclare les bases</span>', '<strong>Technical administrator</strong><span>registers the databases</span>'),
 ('<strong>Responsable sécurité</strong><span>décide du masquage</span>', '<strong>Security officer</strong><span>decides on masking</span>'),
 ('<strong>Administrateur des accès</strong><span>gère les comptes</span>', '<strong>Access administrator</strong><span>manages accounts</span>'),
 ('<strong>Super administrateur</strong><span>gère les rôles, validés à quatre yeux</span>', '<strong>Super administrator</strong><span>manages roles, with four-eyes approval</span>'),
 # démo
 ('>Démonstration</p>', '>Demo</p>'), ('SQLVault Gateway en vidéo', 'SQLVault Gateway on video'),
 ("Une présentation d'une minute et demie, tournée sur la Banque Téranga, une banque fictive de démonstration.",
  'A 90-second overview (in French, with subtitles), filmed on Banque Téranga, a fictitious demo bank.'),
 ('Votre navigateur ne lit pas la vidéo.', 'Your browser cannot play this video.'), ('Télécharger la vidéo', 'Download the video'),
 ('Quelques écrans', 'A few screens'),
 ("Examen d'une demande de modification par un valideur", 'A validator reviewing a change request'),
 ('Validation à quatre yeux d\'une modification', 'Four-eyes approval of a change'),
 ('Suppression de table refusée par la politique de sécurité', 'Table drop refused by the security policy'),
 ("Suppression de table refusée avant d'atteindre la base", 'Table drop refused before reaching the database'),
 ("Journal d'audit vu par une auditrice", 'Audit log seen by an auditor'),
 ("Journal d'audit : qui, quoi, quand, depuis quel poste", 'Audit log: who, what, when, from which workstation'),
 ("Vérification d'intégrité du journal d'audit", 'Audit log integrity check'),
 ('Vérification d\'intégrité du journal', 'Audit log integrity check'),
 ("Programmation d'un rapport avec aperçu masqué", 'Scheduling a report with a masked preview'),
 ('Rapport planifié, aperçu déjà masqué', 'Scheduled report, preview already masked'),
 ('Numéros de carte masqués sur SQL Server', 'Card numbers masked on SQL Server'),
 ('Numéros de carte masqués (PCI DSS)', 'Card numbers masked (PCI DSS)'),
 # pour qui
 ('>Pour qui</p>', '>Who it is for</p>'), ('Chacun y trouve son compte', 'Something for everyone'),
 ('<h3>Direction générale</h3>', '<h3>Executive management</h3>'),
 ('Un risque opérationnel et réputationnel maîtrisé, démontrable aux régulateurs et aux auditeurs.',
  'Operational and reputational risk under control, and demonstrably so to regulators and auditors.'),
 ('<h3>DSI</h3>', '<h3>IT department</h3>'),
 ("Un seul chemin d'accès aux bases, sans client SQL à maintenir sur les postes, déployé en conteneur Docker.",
  'One access path to the databases, no SQL client to maintain on workstations, deployed as a Docker container.'),
 ('<h3>RSSI et conformité</h3>', '<h3>CISO and compliance</h3>'),
 ('Masquage piloté par la sécurité, alertes en temps réel, revue des habilitations exportable en Excel.',
  'Masking controlled by security, real-time alerts, access reviews exportable to Excel.'),
 ('<h3>Équipes métier et audit</h3>', '<h3>Business and audit teams</h3>'),
 ('Des données utiles, des rapports qui arrivent seuls, et un historique complet consultable en quelques clics.',
  'Useful data, reports that arrive on their own, and a complete history a few clicks away.'),
 # sécurité
 ('>Sécurité et déploiement</p>', '>Security and deployment</p>'), ("Conçu pour l'environnement bancaire", 'Built for banking environments'),
 ("SQLVault Gateway s'installe sur un serveur de la banque. Les postes y accèdent en HTTPS, depuis un simple navigateur. Les bases ne sont plus ouvertes qu'au serveur SQLVault Gateway, avec des comptes techniques à droits limités.",
  "SQLVault Gateway is installed on a server inside the bank. Workstations reach it over HTTPS from a web browser. The databases are opened only to the SQLVault Gateway server, through technical accounts with limited rights."),
 ('Lire la note de déploiement DSI / RSSI →', 'Read the IT / CISO deployment note (French) →'),
 ('<b>Hébergement chez vous</b>, dans votre réseau : aucune donnée ne quitte la banque.', '<b>Hosted on your premises</b>, in your network: no data leaves the bank.'),
 ('<b>Mots de passe des bases chiffrés</b> (AES-256) et jamais réaffichés.', '<b>Database passwords encrypted</b> (AES-256) and never displayed again.'),
 ("<b>Comptes activés par l'utilisateur lui-même</b> : l'administrateur ne connaît aucun mot de passe.", '<b>Accounts activated by the users themselves</b>: administrators never know a password.'),
 ("<b>Journal d'audit signé et chaîné</b>, vérifiable à tout moment, propriété de la banque.", '<b>Signed, chained audit log</b>, verifiable at any time, owned by the bank.'),
 ('<b>Moteur écrit en Go</b>, livré dans une image Docker légère, en lecture seule et sans privilèges.', '<b>Engine written in Go</b>, shipped as a lightweight, read-only, unprivileged Docker image.'),
 ('<b>Rôles et droits personnalisables</b>, avec refus des droits incompatibles et validation à quatre yeux.', '<b>Customisable roles and permissions</b>, with incompatible rights refused and four-eyes approval.'),
 # pilote
 ('>Pilote</p>', '>Pilot</p>'), ('Quatre semaines pour décider, sur vos propres critères', 'Four weeks to decide, on your own criteria'),
 ('Une équipe de la banque utilise SQLVault Gateway sur une base de recette. Aucune donnée de production, aucun outil actuel coupé.',
  'A team from the bank uses SQLVault Gateway on a test database. No production data, and no current tool is switched off.'),
 ('<span>Semaine 1</span><h3>Installation</h3>', '<span>Week 1</span><h3>Installation</h3>'),
 ('Serveur, bases de recette, rôles, règles de masquage validées par le RSSI.', 'Server, test databases, roles, masking rules approved by the CISO.'),
 ('<span>Semaine 2</span><h3>Formation</h3>', '<span>Week 2</span><h3>Training</h3>'),
 ('Utilisateurs et administrateurs formés, premiers accès, premières demandes.', 'Users and administrators trained, first logins, first requests.'),
 ('<span>Semaine 3</span><h3>Usage réel</h3>', '<span>Week 3</span><h3>Real use</h3>'),
 ("Les équipes travaillent dans l'outil ; le RSSI déroule son scénario de test.", 'Teams work in the tool; the CISO runs their test scenario.'),
 ('<span>Semaine 4</span><h3>Bilan</h3>', '<span>Week 4</span><h3>Review</h3>'),
 ('Critères mesurés, restauration testée, recommandation remise. La banque décide.', 'Criteria measured, restore tested, recommendation delivered. The bank decides.'),
 # documents
 ('Tout savoir avant de nous rencontrer', 'Everything you need before we meet'),
 ('<strong>Fiche produit</strong><small>2 pages · l\'essentiel en un coup d\'œil</small>', '<strong>Product sheet</strong><small>2 pages, in French · the essentials at a glance</small>'),
 ('<strong>Note de déploiement DSI / RSSI</strong><small>7 pages · comptes, réseau, postes, audit</small>', '<strong>IT / CISO deployment note</strong><small>7 pages, in French · accounts, network, workstations, audit</small>'),
 ('Demande%20du%20guide%20utilisateur%20SQLVault%20Gateway', 'SQLVault%20Gateway%20user%20guide%20request'),
 ('<span class="pdf">Sur demande</span><strong>Guide utilisateur</strong><small>34 pages · chaque écran, illustré · envoyé aux établissements intéressés</small>',
  '<span class="pdf">On request</span><strong>User guide</strong><small>34 pages, in French · every screen, illustrated · sent to interested institutions</small>'),
 ('Demande%20du%20document%20technique%20SQLVault%20Gateway', 'SQLVault%20Gateway%20technical%20document%20request'),
 ('<strong>Document technique de référence</strong><small>Sur demande, sous accord de confidentialité</small>',
  '<strong>Technical reference</strong><small>On request, under a non-disclosure agreement</small>'),
 # FAQ
 ('>Questions fréquentes</p>', '>Frequently asked questions</p>'), ('Vos questions, nos réponses', 'Your questions, answered'),
 ('Faut-il installer quelque chose sur les postes de travail ?', 'Do we need to install anything on workstations?'),
 ("Non. Un navigateur récent suffit. SQLVault Gateway est installé sur un serveur de la banque et s'utilise en HTTPS.",
  'No. A recent browser is enough. SQLVault Gateway is installed on a server inside the bank and used over HTTPS.'),
 ('Nos données sortent-elles de la banque ?', 'Does our data leave the bank?'),
 ("Non. L'outil est hébergé dans votre infrastructure, et DEF TECH n'a pas besoin d'accéder à vos données, y compris pendant le pilote.",
  'No. The tool is hosted in your infrastructure, and DEF TECH does not need access to your data, including during the pilot.'),
 ('Quelles bases de données sont prises en charge ?', 'Which databases are supported?'),
 ('Oracle, SQL Server, PostgreSQL, MySQL et MariaDB, avec ou sans chiffrement TLS. Le même écran et les mêmes règles servent pour toutes.',
  'Oracle, SQL Server, PostgreSQL, MySQL and MariaDB, with or without TLS encryption. The same screen and the same rules apply to all of them.'),
 ("Est-ce que l'outil ralentit les requêtes ?", 'Does the tool slow queries down?'),
 ("L'analyse et le masquage ajoutent quelques millisecondes. Les grands résultats sont lus en flux, et l'export complet est produit côté serveur.",
  'Analysis and masking add a few milliseconds. Large results are streamed, and full exports are produced on the server.'),
 ('Que se passe-t-il pour les administrateurs de bases (DBA) ?', 'What about database administrators (DBAs)?'),
 ("Les évolutions de structure et l'accès d'urgence passent par des circuits dédiés et tracés (bastion, coffre-fort à mots de passe). La note DSI / RSSI décrit le dispositif complet.",
  'Schema changes and emergency access go through dedicated, recorded channels (bastion host, password vault). The IT / CISO note describes the full set-up.'),
 ('Comment se déroule un pilote ?', 'How does a pilot work?'),
 ('Quatre semaines sur une base de recette, avec 5 à 10 utilisateurs et des critères de réussite fixés dès le premier jour avec votre DSI et votre RSSI.',
  'Four weeks on a test database, with 5 to 10 users and success criteria agreed on day one with your IT department and your CISO.'),
 # contact
 ('Parlons de vos accès aux données', "Let's talk about access to your data"),
 ('Démonstration en ligne de 30 minutes ou pilote de 4 semaines sur votre propre environnement : écrivez-nous, nous vous répondons rapidement.',
  'A 30-minute online demo or a 4-week pilot in your own environment: write to us and we will get back to you quickly.'),
 ('Demande%20de%20d%C3%A9monstration%20SQLVault%20Gateway', 'SQLVault%20Gateway%20demo%20request'),
 ('Demander une démonstration', 'Request a demo'),
 ("L'équipe SQLVault Gateway · DEF TECH 2.0 · Sénégal", 'The SQLVault Gateway team · DEF TECH 2.0 · Senegal'),
 # pied de page
 ('Haut de page ↑', 'Back to top ↑'),
 ("© 2026 DEF TECH 2.0. Tous droits réservés. SQLVault Gateway, ses textes, captures, vidéos et documents ne peuvent être reproduits sans autorisation écrite. Les captures et la vidéo utilisent des données fictives (Banque Téranga). Oracle, MySQL, SQL Server, PostgreSQL et MariaDB sont des marques de leurs propriétaires respectifs ; logos : projet Devicon, licence MIT.",
  "© 2026 DEF TECH 2.0. All rights reserved. SQLVault Gateway and its text, screenshots, videos and documents may not be reproduced without written permission. Screenshots and video use fictitious data (Banque Téranga). Oracle, MySQL, SQL Server, PostgreSQL and MariaDB are trademarks of their respective owners; logos: Devicon project, MIT licence."),
 ('Agrandissement de la capture', 'Enlarged screenshot'), ('aria-label="Fermer"', 'aria-label="Close"'),
]

en = fr
for a, b in T:
    if a not in en:
        print('ABSENT :', a[:70])
    en = en.replace(a, b)
# chemins relatifs depuis /en/
en = re.sub(r'(src|href|poster|data-full)="(assets/|favicon\.ico)', r'\1="../\2', en)
en = en.replace('href="https://sqlvaultgateway.github.io/" ', 'href="https://sqlvaultgateway.github.io/en/" ')
en = en.replace('<link rel="canonical" href="https://sqlvaultgateway.github.io/">', '<link rel="canonical" href="https://sqlvaultgateway.github.io/en/">')
en = en.replace('<meta property="og:url" content="https://sqlvaultgateway.github.io/">', '<meta property="og:url" content="https://sqlvaultgateway.github.io/en/">')
en = en.replace('"url":"https://sqlvaultgateway.github.io/"', '"url":"https://sqlvaultgateway.github.io/en/"')
# sélecteur de langue
en = en.replace('<a class="lang" href="../en/" hreflang="en" lang="en">EN</a>', '<a class="lang" href="../" hreflang="fr" lang="fr">FR</a>')
en = en.replace('<a class="lang" href="en/" hreflang="en" lang="en">EN</a>', '<a class="lang" href="../" hreflang="fr" lang="fr">FR</a>')

# contrôle : texte français restant (hors noms propres et extraits techniques)
body = re.sub(r'<script.*?</script>|<svg.*?</svg>|<style.*?</style>', '', en, flags=re.S)
txt = re.sub(r'<[^>]+>', '\n', body)
left = [l.strip() for l in txt.split('\n') if re.search(r"[éèàùâêîôûç]|\b(les|des|une|pour|vos|nous)\b", l) and 'Téranga' not in l]
for l in left: print('FR RESTANT :', l[:90])
(root / 'en').mkdir(exist_ok=True)
(root / 'en' / 'index.html').write_text(en, encoding='utf-8')
print('en/index.html écrit,', len(T), 'traductions')
