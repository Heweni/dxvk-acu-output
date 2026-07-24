# AC Unity DXVK 3.0.2 output-selector builder

This repository contains a small source patch and a manually triggered GitHub Actions workflow. GitHub builds an experimental 64-bit DXVK package containing `d3d11.dll` and `dxgi.dll`.

The patch adds this custom `dxvk.conf` option:

```ini
dxgi.outputIndex = 1
```

It moves the selected physical output to `IDXGIOutput 0`, for games such as Assassin's Creed Unity that appear to select output zero regardless of the Windows primary-display setting.

## Build it on GitHub

1. Create a new **private** or public GitHub repository.
2. Extract this ZIP on your PC.
3. Upload **all extracted contents**, including the hidden `.github` folder, to the repository root.
4. Commit the files.
5. Open the repository's **Actions** tab.
6. Select **Build patched DXVK 3.0.2**.
7. Click **Run workflow**, then confirm **Run workflow**.
8. Wait for the `build-x64` job to finish with a green check mark.
9. Open the completed workflow run.
10. Under **Artifacts**, download `acu-dxvk-3.0.2-output-selector-x64`.

The downloaded artifact contains:

```text
x64/d3d11.dll
x64/dxgi.dll
dxvk.conf
TESTING.txt
SHA256SUMS.txt
```

## Test in AC Unity

Follow `TESTING.txt`. Back up the existing DLLs before copying anything beside `ACU.exe`.

Start with:

```ini
dxgi.outputIndex = 1
```

A successful patched run should add this to `ACU_dxgi.log`:

```text
DXGI: Forcing physical output 1 to IDXGI output 0
```

If index 1 does not select the 1440p monitor, test index 0. Windows “Display 1” does not necessarily equal DXGI output index 0.

## What the workflow does

The workflow clones the official DXVK `v3.0.2` tag and its submodules, verifies and applies `patches/dxvk-3.0.2-output-selector.patch`, builds DXVK with the same Arch MinGW GitHub Action used by upstream DXVK workflows, and uploads only the needed x64 DLLs plus the configuration and checksums.

## Trust and limitations

- This patch is experimental and unofficial.
- The DLLs are built by GitHub Actions in your own repository; this ZIP contains no executables.
- The patch and resulting binaries have not been tested on your machine yet.
- Use only with AC Unity; avoid anti-cheat-protected games.
