# NYO12 Ultimate — Android Switch launcher

## Direction produit
Une seule application Android ARM64, inspirée de l'ergonomie SteamOS et des panneaux de réglages GameHub. Le moteur DroidPlay Core reste le moteur d'exécution ; NYO12 construit autour de lui une interface, une bibliothèque et des outils système cohérents.

## Identité visuelle
- Fond bleu-noir profond, surfaces anthracite bleutées.
- Accent bleu électrique, états positifs vert menthe.
- Typographie claire, grands visuels de jeux, navigation pensée pour écran tactile et manette.
- Interface paysage en priorité, adaptée tablette.

## Architecture cible
1. **Accueil / bibliothèque** : jeux détectés localement, jaquettes, recherche, filtres, état de compatibilité.
2. **Fiche de jeu** : lancer, reprendre, sauvegardes, paramètres individuels et profil graphique.
3. **Import local** : sélecteur Android (SAF), espace temporaire, validation et préparation des dumps personnels. Le pipeline actuel `scripts/build_android_from_nsp.py` est un outil de préparation orienté ordinateur ; il doit être porté et ses dépendances auditées avant de promettre un import NSP/XCI autonome.
4. **Centre de performances** : FPS/frametime quand exposés par le moteur, journal, profil énergie et résolution.
5. **Graphismes** : options réellement prises en charge par le moteur et le pilote Vulkan détecté.
6. **Pilotes** : détection du GPU et du pilote système ; ne jamais proposer Turnip comme solution universelle. Xclipse 540 doit être testé avec son pilote Vulkan Samsung.
7. **Amélioration d'image** : commencer par les options de résolution/rendu déjà présentes. L'upscaling spatial et l'interpolation d'images sont des modules expérimentaux distincts ; pas de promesse d'équivalence avec Lossless Scaling.

## Contraintes techniques connues
- Cible Android `arm64-v8a`, backend Vulkan.
- Le dépôt utilise un assembleur APK maison (`dm/android/tools/build_apk.py`) et CMake/NDK, pas un projet Gradle standard.
- Un hôte natif `libdmhost_<TITLE_ID>.so` est actuellement empaqueté par jeu. La bibliothèque ne peut donc pas lancer automatiquement tout jeu sans profil/hôte compatible.
- Le chargeur Android est `dm/android/java/org/nxnative/android/Launcher.java`. Le premier changement de cette branche renomme et recolore son écran d'accueil sans toucher au moteur natif.
- Les fichiers de jeu et clés doivent provenir des sauvegardes personnelles de l'utilisateur ; aucun jeu ni clé n'est fourni par NYO12.

## Étapes
- [x] Poser le nom NYO12 Ultimate et la palette de base dans le launcher Android.
- [x] Mettre à jour le nom affiché de l'application Android.
- [x] Documenter l'architecture et les limites réelles du port Android.
- [ ] Construire et tester l'APK de base sur Android 16 / Xclipse 540.
- [ ] Refaire l'accueil en bibliothèque SteamOS (navigation, recherche, tuiles, états).
- [ ] Ajouter l'import SAF et établir une vraie chaîne de préparation on-device.
- [ ] Ajouter les diagnostics Vulkan et les profils graphiques vérifiés.
- [ ] Évaluer séparément upscaling et interpolation sur l'Exynos 1580.

## Build
Le build natif reste piloté par `dm/android/CMakeLists.txt`, `dm/android/tools/build_apk.py` et les scripts de préparation. Il faut un Android SDK/NDK et au moins un profil de jeu/hôte valide. Une APK générique complète ne peut pas être produite honnêtement sans ces entrées.

## Références APK inspectées
- `APK_REFERENCE_ANALYSIS_FR.md` décrit BOTW Recomp, MKart8Port Xclipse et le paquet DroidPlay fourni.
- `BUILD_APK_GITHUB_FR.md` décrit la première compilation du launcher sur GitHub Actions, sans ordinateur local.
- Le premier build de packaging réutilise le host Pokémon Brilliant Diamond déjà présent dans le DroidPlay APK fourni ; il ne prétend pas ajouter BOTW ou Mario Kart comme jeux compatibles.
