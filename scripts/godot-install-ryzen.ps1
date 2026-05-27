# One-shot Godot 4.6.2-stable + Web export templates installer (Ryzen VGit).
# Eduardo authorized 2026-05-19. Run via Scheduled Task (robust detached).
$ErrorActionPreference = 'Stop'
$log = "$env:USERPROFILE\Desktop\.godot-install.log"
function Lg($m) { ((Get-Date -Format HH:mm:ss) + ' ' + $m) | Out-File -Append -Encoding ascii $log }
try {
  Lg 'START'
  $lad = "$env:LOCALAPPDATA\Godot"
  $tpl = "$env:APPDATA\Godot\export_templates\4.6.2.stable"
  $dl  = "$env:TEMP\gdl"
  New-Item -ItemType Directory -Force -Path $lad, $tpl, $dl | Out-Null
  $edUrl  = 'https://github.com/godotengine/godot/releases/download/4.6.2-stable/Godot_v4.6.2-stable_win64.exe.zip'
  $tplUrl = 'https://github.com/godotengine/godot/releases/download/4.6.2-stable/Godot_v4.6.2-stable_export_templates.tpz'
  Lg 'dl editor ~80MB'
  Invoke-WebRequest -UseBasicParsing -Uri $edUrl -OutFile "$dl\ed.zip"
  Expand-Archive -Path "$dl\ed.zip" -DestinationPath "$dl\ed" -Force
  $exe = Get-ChildItem "$dl\ed" -Filter 'Godot_v4.6.2-stable_win64_console.exe' -Recurse | Select-Object -First 1
  if (-not $exe) { $exe = Get-ChildItem "$dl\ed" -Filter 'Godot_v4.6.2-stable_win64.exe' -Recurse | Select-Object -First 1 }
  Copy-Item $exe.FullName (Join-Path $lad $exe.Name) -Force
  Lg ('editor ok -> ' + (Join-Path $lad $exe.Name))
  Lg 'dl templates ~1.25GB slow'
  Invoke-WebRequest -UseBasicParsing -Uri $tplUrl -OutFile "$dl\t.tpz"
  Copy-Item "$dl\t.tpz" "$dl\t.zip" -Force
  Expand-Archive -Path "$dl\t.zip" -DestinationPath "$dl\tx" -Force
  $tdir = Get-ChildItem "$dl\tx" -Directory -Filter 'templates' -Recurse | Select-Object -First 1
  Copy-Item (Join-Path $tdir.FullName '*') $tpl -Recurse -Force
  Lg 'templates extracted'
  $e = Test-Path (Join-Path $lad $exe.Name)
  $w = (Get-ChildItem $tpl -Filter 'web*.zip' -ErrorAction SilentlyContinue | Measure-Object).Count
  $tot = (Get-ChildItem $tpl -ErrorAction SilentlyContinue | Measure-Object).Count
  Lg ("VERIFY exe=$e webTemplates=$w totalTemplateFiles=$tot")
  Remove-Item "$dl\ed.zip","$dl\t.tpz","$dl\t.zip" -Force -ErrorAction SilentlyContinue
  if ($e -and $w -ge 1) { Lg 'DONE OK' } else { Lg 'DONE FAIL missing exe or web template' }
} catch {
  Lg ('ERROR ' + $_.Exception.Message)
  Lg 'DONE FAIL'
}
