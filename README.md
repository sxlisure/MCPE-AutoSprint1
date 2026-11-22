# MCPE 1.1.5 AutoSprint — PC-only app controls

## Cloud build (no Python needed on your PC)
1. Create a GitHub repository: https://github.com/new
2. Upload all files in this folder, preserving `.github/workflows/build.yml`.
3. Open **Actions**, enable workflows if prompted, then run **Build MCPE AutoSprint EXE**.
   A push to the `main` branch also starts a build.
4. Open the completed run and download artifact `MCPE-AutoSprint-Windows-x64`.
5. Extract the artifact ZIP to get `MCPE_AutoSprint.exe`.

## Usage
- Connect your controller before launching the helper.
- Launch the helper and click **ВКЛЮЧИТЬ AUTOSPRINT** with the mouse.
- Move the left stick forward to activate sprint input.
- Click the button again to turn it off.
- Close the app to stop and release the Ctrl key.

## Controller input behavior
The program reads only the left stick's vertical axis. It does not read or bind any
gamepad buttons, including A/B/X/Y, bumpers, triggers, D-pad, or L3/R3. Those controls
remain available to Minecraft. The app window is controlled with the PC mouse.

## Compatibility limitation
The helper sends the Windows Left Ctrl key while AutoSprint is enabled and the left
stick is pushed forward. This is an input helper, not a Minecraft mod. Whether MCPE
1.1.5 on the user's Windows build accepts Ctrl as sprint while a gamepad is active
must be tested in-game. Some versions may use a different sprint input or ignore
keyboard modifiers during controller play.
