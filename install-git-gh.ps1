$ErrorActionPreference = 'Stop'
$root = Join-Path $env:LOCALAPPDATA 'Programs'
$dl   = Join-Path $env:LOCALAPPDATA 'Temp\dsh-installers'
$gitDir = Join-Path $root 'PortableGit'
$ghRoot = Join-Path $root 'gh'

Write-Host "=== 1. extract PortableGit ==="
if (Test-Path (Join-Path $gitDir 'cmd\git.exe')) {
  Write-Host "already extracted: $gitDir"
} else {
  $exe = Join-Path $dl 'PortableGit-2.56.0.2-64-bit.7z.exe'
  if (-not (Test-Path $exe)) { throw "missing installer: $exe" }
  $env:MSYS = 'winsymlinks:nativestrict'
  $proc = Start-Process -FilePath $exe -ArgumentList "-o`"$gitDir`"", '-y' -Wait -PassThru -WindowStyle Hidden
  Write-Host "extractor exit code: $($proc.ExitCode)"
}
Write-Host "git.exe: $(Test-Path (Join-Path $gitDir 'cmd\git.exe'))"

Write-Host "=== 2. extract gh ==="
if (Test-Path (Join-Path $ghRoot 'bin\gh.exe')) {
  Write-Host "already extracted: $ghRoot"
} else {
  $zip = Join-Path $dl 'gh_2.102.0_windows_amd64.zip'
  if (-not (Test-Path $zip)) { throw "missing installer: $zip" }
  New-Item -ItemType Directory -Force -Path $ghRoot | Out-Null
  Expand-Archive -Path $zip -DestinationPath $ghRoot -Force
}
Write-Host "gh.exe: $(Test-Path (Join-Path $ghRoot 'bin\gh.exe'))"

Write-Host "=== 3. add to USER PATH (idempotent) ==="
$want = @((Join-Path $gitDir 'cmd'), (Join-Path $ghRoot 'bin'))
$cur  = [Environment]::GetEnvironmentVariable('Path', 'User')
if ($null -eq $cur) { $cur = '' }
$parts = $cur -split ';' | Where-Object { $_ -ne '' }
foreach ($w in $want) {
  $dup = $parts | Where-Object { $_.TrimEnd('\') -ieq $w.TrimEnd('\') }
  if ($dup) { Write-Host "already in PATH: $w" }
  else { $parts += $w; Write-Host "added to PATH: $w" }
}
$new = ($parts -join ';')
[Environment]::SetEnvironmentVariable('Path', $new, 'User')
Write-Host "user PATH now:"
[Environment]::GetEnvironmentVariable('Path', 'User') -split ';' | ForEach-Object { "   $_" }

Write-Host "=== 4. verify (absolute paths) ==="
& (Join-Path $gitDir 'cmd\git.exe') --version
& (Join-Path $ghRoot 'bin\gh.exe') --version
