# Analyse des trois APK de référence pour NYO12

Analyse de structure ZIP, bibliothèques ELF AArch64, dépendances natives, assets et code source DroidPlay disponible dans le dépôt. Les APK ne contiennent pas nécessairement leurs sources originales complètes.

## DroidPlay-0.6.0-arm64-v8a.apk

- Contient `libnxloader.so`, `libdmhost_0100000011D90000.so`, `libadrenotools.so`, `libhook_impl.so`, `libmain_hook.so` et `assets/selftest/*`.
- Le Title ID `0100000011D90000` correspond au profil Pokémon Brilliant Diamond 1.3.0 dans `dm/games/0100000011D90000/README.md`.
- Il s'agit donc d'un launcher avec un host de jeu déjà compilé, pas d'un émulateur universel vide.
- Le paquet contient les éléments nécessaires pour reconstruire une APK de launcher avec le Java NYO12 modifié, sans recompiler le host natif.

## BOTWRecompAndroid-0.3.1-beta.apk

- Environ 86 MiB sur disque, 257 MiB décompressés.
- Contient `libmain.so`, `libzig.so` (environ 164 MiB décompressés), SDL3, FFmpeg, `libshaderc_shared.so`, Python 3.14, Capstone et Unicorn.
- Toutes les bibliothèques observées sont AArch64.
- Architecture dédiée à cette recompilation/port Android de BOTW. Elle n'emploie pas le couple `libnxloader.so` + `libdmhost_<TITLE_ID>.so` de DroidPlay.
- Conclusion : utile comme référence d'intégration native, rendu SDL/Vulkan et packaging de gros assets ; ce n'est pas un module de moteur Switch que l'on peut ajouter directement à NYO12.

## MKart8Port-v0.3.2-Xclipse.apk

- Environ 70 MiB sur disque.
- Contient notamment `libdmhost.so`, `libshader_recompiler_android.so`, `librecompiler_android_c.so`, `libporter_native_jni.so`, `libporter_python.so`, Python 3.14 et `libadrenotools.so` avec ses hooks.
- Embarque `assets/vulkan.radeon.so` et `assets/libvulkan_freedreno.so` comme assets, pas comme bibliothèques Android ordinaires dans `lib/arm64-v8a/`.
- Le premier est un ELF AArch64 dont le SONAME est `libvulkan_radeon.so`; ses chaînes contiennent des marqueurs RADV et `[XCLIPSE]`, dont un message d'override GBCFG. C'est un indice fort d'un build Mesa RADV modifié pour la famille Xclipse.
- Le second identifie clairement Freedreno et des appareils Adreno ; il ne cible pas le Xclipse.
- `libdmhost.so` utilise Vulkan système et expose des chaînes relatives au chargement d'un pilote personnalisé via adrenotools. Son architecture globale reste spécifique à cette application/ce port.
- Conclusion : c'est la meilleure référence pour étudier un pilote RADV Xclipse empaqueté dans une app Android. Mais l'APK ne prouve pas que ce binaire précis est compatible avec le Xclipse 540 de la Tab S10 FE. Il faut vérifier son GPU cible, ses dépendances, son ABI et le résultat de `vkEnumeratePhysicalDevices` sur la tablette avant de l'intégrer.

## Décisions pour NYO12

1. Garder DroidPlay Core comme base du launcher et de son interface NVN/Vulkan.
2. Étudier le chargement RADV Xclipse de MKart8Port comme piste expérimentale, sans embarquer aveuglément le pilote ni le présenter comme compatible 540.
3. Réutiliser BOTW Recomp uniquement comme référence de packaging/UX native, pas comme moteur Switch multi-jeux.
4. Ne pas fusionner les bibliothèques natives de ces APK sans leurs interfaces et licences : leurs loaders, symboles JNI, formats de données et cycles de vie ne sont pas interchangeables.
