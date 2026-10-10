# Energy Network Simulation

This Java console application simulates a simplified energy grid. Users can add producers, consumers, and batteries; mark components as operational or faulty; advance the simulation in ticks; and inspect the grid status and event history. The simulator balances production and demand, uses batteries when needed, prioritizes consumers, and detects blackouts.

## Application structure

- `ComponentaRetea` is the base class for network components.
- `ProducatorEnergie` has three variants: `PanouSolar`, `TurbinaEoliana`, and `ReactorNuclear`.
- `ConsumatorEnergie` has three variants: `SistemSuportViata`, `LaboratorStiintific`, and `SistemIluminat`.
- `Baterie` stores and releases energy to help stabilize the grid.
- `GridController` manages components, consumer priority, production and demand, battery charging and discharging, blackouts, and event history.
- `App` reads commands, validates arguments, and prints responses.

## Commands

Enter one command per line. The application uses numeric command IDs:

| ID | Action | Format |
| --- | --- | --- |
| `0` | Add a producer | `0 <solar\|turbina\|reactor> <id> <power>` |
| `1` | Add a consumer | `1 <suport_viata\|laborator\|iluminat> <id> <demand>` |
| `2` | Add a battery | `2 <id> <capacity>` |
| `3` | Advance one simulation tick | `3 <sun_factor> <wind_factor>` |
| `4` | Change operational status | `4 <id> <true\|false>` |
| `5` | Show grid status | `5` |
| `6` | Show event history | `6` |
| `7` | Exit | `7` |

The application's command responses are in Romanian. Their spacing, capitalization, and numeric formatting follow the assignment's expected output.

## Run

The source files declare the `Tema1` package. With a JDK installed, open PowerShell in this folder and run:

```powershell
javac -d out (Get-ChildItem *.java).FullName
java -cp out Tema1.App
```

Then type commands into the terminal, ending with `7`.

## Potential behavior improvements

These are ideas noted during development; they are not current features.

1. **Validate sun and wind factors.** The application currently accepts any numeric production factor. Restricting factors to the range `0`–`1`, either by clamping or by reporting an error, would make the simulation more realistic.
2. **Limit unusually high consumer demand.** A consumer can be added with a very large demand, such as a laboratory requiring 500,000 MW. A reasonable limit or warning could help prevent accidental blackouts.
3. **Handle IDs without case sensitivity.** The current code treats `b1` and `B1` as different IDs. Normalizing IDs when storing them could prevent confusion.

## Potential code improvements

1. **Centralize error messages.** Messages currently appear in several methods. A single `Messages` class would make exact wording easier to maintain.
2. **Separate presentation from application logic.** `App` could only read commands, `GridController` could return data objects, and another class could format responses. This would make the code easier to extend and test.
3. **Use command handlers.** The switch in `App` contains a branch for each command from `0` to `7`. A `Command` interface with a class for each action would make future commands easier to add.
