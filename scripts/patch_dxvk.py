from pathlib import Path
import re


def edit_once(path: str, pattern: str, replacement: str, flags: int = 0) -> None:
    file_path = Path(path)
    text = file_path.read_text(encoding="utf-8")
    updated, count = re.subn(pattern, replacement, text, count=1, flags=flags)
    if count != 1:
        raise SystemExit(f"Expected exactly one regex match in {path}, found {count}")
    file_path.write_text(updated, encoding="utf-8")


# Add the configuration field directly after forceRefreshRate, tolerating
# whitespace/alignment differences in the tagged source.
edit_once(
    "src/dxgi/dxgi_options.h",
    r"(?m)^(\s*uint32_t\s+forceRefreshRate\s*;\s*)$",
    r"\1\n\n    /// Move the selected physical DXGI output to output index 0.\n"
    r"    /// A negative value keeps the normal enumeration order.\n"
    r"    int32_t outputIndex;",
)

# Insert config parsing after the existing force-refresh-rate option.
edit_once(
    "src/dxgi/dxgi_options.cpp",
    r'(?m)^(\s*this->forceRefreshRate\s*=\s*config\.getOption\("dxgi\.forceRefreshRate",\s*0u\);\s*)$',
    r'\1\n    this->outputIndex = config.getOption("dxgi.outputIndex", -1);',
)

# Replace only the monitor enumeration statement. Keeping the surrounding
# source untouched makes this resilient to formatting changes.
edit_once(
    "src/dxgi/dxgi_adapter.cpp",
    r"(?m)^(\s*)HMONITOR\s+monitor\s*=\s*wsi::enumMonitors\(luidPointers\.data\(\),\s*luidPointers\.size\(\),\s*Output\);\s*$",
    r'''\1UINT physicalOutput = Output;

\1const DxgiOptions* options = m_factory->GetOptions();
\1if (options->outputIndex >= 0) {
\1  const UINT selectedOutput = UINT(options->outputIndex);

\1  if (Output == 0)
\1    physicalOutput = selectedOutput;
\1  else if (Output <= selectedOutput)
\1    physicalOutput = Output - 1;
\1}

\1HMONITOR monitor = wsi::enumMonitors(
\1  luidPointers.data(), luidPointers.size(), physicalOutput);

\1if (monitor != nullptr && options->outputIndex >= 0 && Output == 0) {
\1  Logger::info(str::format(
\1    "DXGI: Forcing physical output ", physicalOutput,
\1    " to IDXGI output 0"));
\1}''',
)

print("DXVK output-selector source edits applied successfully.")
