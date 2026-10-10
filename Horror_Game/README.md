# RGD Horror Story

**A 3D horror project built in Unity by a team of five.** Explore, collect clues and supplies, manage your flashlight, and protect your sanity in an atmosphere designed around suspense.

> [!NOTE]
> This project is in development. The `SampleScene` configured in Build Settings is currently a basic scene. The gameplay systems are present in the project's code and assets, but this repository does not yet include a finished playable level.

## About the project

RGD Horror Story combines first-person exploration with survival and investigation mechanics. The player can interact with nearby objects, collect clues, batteries, pills, and keys, and use these resources to progress. Darkness affects sanity, while the flashlight has a limited battery.

### Implemented systems

- **Exploration and interaction:** raycast-based interaction with objects and doors.
- **Inventory:** tracks collected batteries, pills, and keys.
- **Flashlight and sanity:** battery drain, recharging, and visual effects as sanity decreases.
- **Clues:** collection and display in a dedicated menu.
- **Doors and keys:** doors can require a specific key.
- **Save and load:** player position, resources, clues, keys, and progress through certain audio events are stored locally in JSON.
- **Interface:** start, pause, save/load, and audio settings menus.

## Technologies

- **Unity:** `6000.3.19f1`
- **Language:** C#
- **Rendering:** Universal Render Pipeline (URP)
- **Relevant packages:** Input System, AI Navigation, TextMesh Pro, and Unity UI

## Open the project

1. Clone the repository using the URL under GitHub's **Code** button, or download its ZIP archive.
2. Open **Unity Hub** and choose **Add project from disk**.
3. Select the `Horror_Game` folder and open it with **Unity 6000.3.19f1**.
4. Wait for assets and packages to import. The scene included in Build Settings is `Assets/Scenes/SampleScene.unity`.

> To obtain a playable level, the mechanics in `Assets/Scripts/` must be configured in a gameplay scene. The included scene is not a final version.

## Controls defined in the scripts

| Action | Key |
| --- | --- |
| Move | `W` `A` `S` `D` |
| Look around | Mouse |
| Interact | `E` |
| Toggle flashlight | `F` |
| Replace flashlight battery | `R` |
| Use a pill | `Q` |
| View inventory | `Tab` |
| Open clues menu | `C` |
| Pause menu | `M` |
| Save/load menu | `Esc` |

Control availability depends on how the scene and its components are configured.

## Project structure

```text
Assets/
├── Scenes/              # Unity scenes
├── Scripts/             # Gameplay systems and interface
├── UI/                  # Interface elements
├── TexturesRGD/         # Project textures
└── ...                  # Other imported assets and packages
Packages/                # Unity dependencies
ProjectSettings/          # Project configuration
```

## Team

- David Silviu
- Argatu Ioan-Dinu
- Dumitrescu Vlad-Ionu
- Nicolae Theodor
- Ghiduc Alexandru

## External assets

This repository includes imported third-party assets. Their respective creators retain the rights to them; check each package's documentation and license before redistribution.