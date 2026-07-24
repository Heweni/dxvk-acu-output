from pathlib import Path


def insert_after_line(path: str, needle: str, new_lines: list[str]) -> None:
    p = Path(path)
    lines = p.read_text(encoding="utf-8").splitlines()
    matches = [i for i, line in enumerate(lines) if needle in line]
    if len(matches) != 1:
        context = "\n".join(line for line in lines if needle.split("(")[0] in line)
        raise SystemExit(
            f"Expected one line containing {needle!r} in {path}, found {len(matches)}.\n"
            f"Related lines:\n{context}"
        )
    i = matches[0]
    lines[i + 1:i + 1] = new_lines
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")


def replace_line_with_block(path: str, required_parts: tuple[str, ...], block: list[str]) -> None:
    p = Path(path)
    lines = p.read_text(encoding="utf-8").splitlines()
    matches = [
        i for i, line in enumerate(lines)
        if all(part in line for part in required_parts)
    ]
    if len(matches) != 1:
        related = "\n".join(line for line in lines if "enumMonitors" in line)
        raise SystemExit(
            f"Expected one matching line in {path}, found {len(matches)}.\n"
            f"enumMonitors lines:\n{related}"
        )
    i = matches[0]
    indent = lines[i][:len(lines[i]) - len(lines[i].lstrip())]
    rendered = [indent + line if line else "" for line in block]
    lines[i:i + 1] = rendered
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")


insert_after_line(
    "src/dxgi/dxgi_options.h",
    "uint32_t forceRefreshRate;",
    [
        "",
        "    /// Move the selected physical DXGI output to output index 0.",
        "    /// A negative value keeps the normal enumeration order.",
        "    int32_t outputIndex;",
    ],
)

# Match only the stable option name, not spacing or the exact getOption syntax.
insert_after_line(
    "src/dxgi/dxgi_options.cpp",
    '"dxgi.forceRefreshRate"',
    ['    this->outputIndex = config.getOption("dxgi.outputIndex", -1);'],
)

replace_line_with_block(
    "src/dxgi/dxgi_adapter.cpp",
    ("HMONITOR monitor", "wsi::enumMonitors", "Output"),
    [
        "UINT physicalOutput = Output;",
        "",
        "const DxgiOptions* options = m_factory->GetOptions();",
        "if (options->outputIndex >= 0) {",
        "  const UINT selectedOutput = UINT(options->outputIndex);",
        "",
        "  if (Output == 0)",
        "    physicalOutput = selectedOutput;",
        "  else if (Output <= selectedOutput)",
        "    physicalOutput = Output - 1;",
        "}",
        "",
        "HMONITOR monitor = wsi::enumMonitors(",
        "  luidPointers.data(), luidPointers.size(), physicalOutput);",
        "",
        "if (monitor != nullptr && options->outputIndex >= 0 && Output == 0) {",
        "  Logger::info(str::format(",
        '    "DXGI: Forcing physical output ", physicalOutput,',
        '    " to IDXGI output 0"));',
        "}",
    ],
)

print("DXVK output-selector source edits applied successfully.")
