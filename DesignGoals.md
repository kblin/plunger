# plunger design goals #

plunger was designed to support a [wide variety of formats](SupportedFormats.md). In order to allow adding new formats easily, plunger uses a plugin architecture with a really loose coupling between plunger and it's plugins.

plunger currently has a text-based interface, but the core logic doesn't depend on the interface. It should be possible to write a GUI for plunger without (m)any changes to the core files.