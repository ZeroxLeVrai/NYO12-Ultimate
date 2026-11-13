# Construire NYO12 Ultimate en APK depuis Android (GitHub Actions)

Cette première chaîne produit une APK installable à partir du code Java NYO12 et des bibliothèques ARM64 déjà compilées présentes dans `build-inputs/DroidPlay-0.6.0-arm64-v8a.apk`.

## Une seule préparation

1. Garde le dépôt **privé** sur GitHub.
2. Envoie le contenu de cette archive dans ton dépôt en conservant les dossiers.
3. Vérifie que `build-inputs/DroidPlay-0.6.0-arm64-v8a.apk` est bien présent.
4. Ouvre l'onglet **Actions** du dépôt.
5. Choisis **Build NYO12 Ultimate APK** puis **Run workflow**.
6. Quand le travail est terminé, ouvre son exécution et télécharge l'artefact `NYO12-Ultimate-v0.1.0-arm64`.
7. Décompresse l'artefact si nécessaire, puis installe l'APK sur la tablette.

## Ce que cette première APK contient réellement

- Le launcher Java compilé depuis le code NYO12.
- Le chargeur Android natif et les bibliothèques de hooks reprises du paquet de base.
- Le host précompilé `libdmhost_0100000011D90000.so`, associé au profil Pokémon Brilliant Diamond 1.3.0.

Ce build ne recompile pas le moteur C/C++ et ne transforme pas BOTW Recomp ou MKart8Port en plugins. Il sert à valider le nouveau launcher et la chaîne de packaging. L'ajout de nouveaux hosts demande une compilation native et un profil compatible pour chaque jeu.

## Installation et signature

L'APK est signée avec une clé de test générée dans le runner GitHub. Son identifiant Android est `org.nyo12.ultimate`, différent de celui de DroidPlay : les deux applications peuvent donc coexister. Les données privées de DroidPlay ne sont pas automatiquement partagées avec NYO12.

Ne publie pas le dépôt si tu y ajoutes des données de jeux, clés ou sauvegardes personnelles.

## Conserver la signature pour les prochaines versions

Au premier lancement du workflow, GitHub crée une clé de signature de test et fournit un second artefact `NYO12-signing-key-backup`. Télécharge-le, ouvre `NYO12_KEYSTORE_BASE64.txt` et copie son contenu complet. Dans le dépôt privé : **Settings → Secrets and variables → Actions → New repository secret**. Nom : `NYO12_KEYSTORE_BASE64`. Valeur : le texte Base64 copié.

Les prochains builds réutiliseront cette même clé. Ne la publie pas et ne la perds pas : Android refuse une mise à jour signée avec une clé différente.
