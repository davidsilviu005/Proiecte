# Energy Network Simulation

This Java console application simulates an energy grid with producers, consumers, and batteries. It calculates production and demand over simulation ticks, handles component faults and blackouts, and keeps an event history.

## Main components

- `ComponentaRetea` is the base class for network components.
- `ProducatorEnergie` has solar panel, wind turbine, and nuclear reactor variants.
- `ConsumatorEnergie` has life support, laboratory, and lighting variants.
- `Baterie` stores and releases energy.
- `GridController` coordinates the grid and simulation state.
- `App` reads commands from standard input and prints the results.

Commands `0`–`6` add components, advance the simulation, change fault status, or display grid information; command `7` exits. The command responses in the program are in Romanian.

The accompanying `README_tema1poo.docx` contains a fuller explanation of the design and possible improvements.
