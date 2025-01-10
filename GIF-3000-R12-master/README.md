# Assembleur pour le jeu d'instructions R12

Exécutez simplement `./cr12.py prog.r12` pour compiler le fichier `prog.r12` contenant des instructions R12.

Par défaut, les instructions codées en binaire seront affichées à la console. Pour les sauvegarder dans un fichier,
redirigez simplement la console vers le fichier:

  > ./cr12.py prog.r12 > prog.bin

Le compilateur supporte les formats d'instruction suivants:
1. `op rd, rs1, rs2`
2. `op rd, rs1`
3. `op rd, rs1, imm4`
4. `op rs, imm6`

où `rd`, `rs1` et `rs2` sont l'un ou l'autre des quatre registres d'**architecture** R0, R1, R2 ou R3,
et où `imm4` et `imm6` sont des valeurs entières (constantes) de quatre (4) ou six (6) bits.
Notez que chaque instruction doit se trouver sur une ligne distincte, et que les lignes blanches
sont permises. Il n'y a pour l'instant **aucun** support pour définir des étiquettes de branchement.

Ce logiciel vous est offert gracieusement, mais sans aucune garantie de bon fonctionnement.
