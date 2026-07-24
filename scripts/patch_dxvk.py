from pathlib import Path


def replace_once(path: str, old: str, new: str) -> None:
    file_path = Path(path)
    text = file_path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"Expected exactly one match in {path}, found {count}")
    file_path.write_text(text.replace(old, new, 1), encoding="utf-8")


replace_once(
    "src/dxgi/dxgi_options.h",
    "    /// Forced refresh rate, disable other modes\n"
    "    uint32_t forceRefreshRate;\n",
    "    /// Forced refresh rate, disable other modes\n"
    "    uint32_t forceRefreshRate;\n\n"
    "    /// Move the selected physical DXGI output to output index 0.\n"
    "    /// A negative value keeps the normal enumeration order.\n"
    "    int32_t outputIndex;\n",
)

replace_once(
    "src/dxgi/dxgi_options.cpp",
    '    this->forceRefreshRate = config.getOption("dxgi.forceRefreshRate", 0u);\n',
    '    this->forceRefreshRate = config.getOption("dxgi.forceRefreshRate", 0u);\n'
    '    this->outputIndex      = config.getOption("dxgi.outputIndex", -1);\n',
)

replace_once(
    "src/dxgi/dxgi_adapter.cpp",
    "    for (const auto& luid : adapterLUIDs)\n"
    "      luidPointers.push_back(&luid);\n\n"
    "    HMONITOR monitor = wsi::enumMonitors(luidPointers.data(), luidPointers.size(), Output);\n",
    "    UINT physicalOutput = Output;\n\n"
    "    const DxgiOptions* options = m_factory->GetOptions();\n"
    "    if (options->outputIndex >= 0) {\n"
    "      const UINT selectedOutput = UINT(options->outputIndex);\n\n"
    "      if (Output == 0)\n"
    "        physicalOutput = selectedOutput;\n"
    "      else if (Output <= selectedOutput)\n"
    "        physicalOutput = Output - 1;\n"
    "    }\n\n"
    "    for (const auto& luid : adapterLUIDs)\n"
    "      luidPointers.push_back(&luid);\n\n"
    "    HMONITOR monitor = wsi::enumMonitors(\n"
    "      luidPointers.data(), luidPointers.size(), physicalOutput);\n\n"
    "    if (monitor != nullptr && options->outputIndex >= 0 && Output == 0) {\n"
    "      Logger::info(str::format(\n"
    '        "DXGI: Forcing physical output ", physicalOutput,\n'
    '        " to IDXGI output 0"));\n'
    "    }\n",
)

print("DXVK output-selector source edits applied successfully.")
