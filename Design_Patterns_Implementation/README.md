-> The system manages:
  - servers, including status, location, and owner;
  - resource groups associated with a server and identified by IP;
  - members within groups;
  - alerts associated with a server, including type, severity, and message.

-> Main classes:
  - Main chooses the workflow from PathTypes and runs the corresponding process.
  - CommandFileReader reads a file, parses its header and lines, and produces CommandRow objects.
  - CommandRow represents one command and its key-value parameters.
  - Database stores servers, groups, and alerts in memory.
  - ServerCommandProcessor handles server commands.
  - GroupCommandProcessor handles groups and members.
  - EventCommandProcessor handles events and alerts.

Collections used:
  - Map provides fast lookup by IP for servers and groups.
  - Set stores alerts.
  - List stores the alert observers.

Design patterns implemented:
1) Singleton
  - Database exposes one instance through getInstance().

2) Factory
  - UserFactory creates a User, Admin, or Operator from the available input fields.

3) Builder
  - Server.Builder constructs a server with optional fields without a long constructor.

4) Observer
  - Server is the subject and notifies AlertListener objects.
  - ResourceGroup is a listener and receives alerts through onAlert().