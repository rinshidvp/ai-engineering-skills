<#
.SYNOPSIS
  Install this repo's skills and agents into the global folders of Claude Code,
  opencode and Google Antigravity.

.DESCRIPTION
  Skills are host-neutral: every folder in skills/ (including _shared/, which
  holds the per-host tool/model mapping) is linked into every host. Folders in
  skills-only/<host>/ go to that host only.

  Agents differ per host (tool names, model names, permission fields), so each
  agent lives in agents/<name>/ as body.md (shared prompt) plus one
  <host>.yaml frontmatter file per host. This script GENERATES
  <host-agents-folder>/<name>.md = frontmatter + body. Generated files are
  copies, so re-run this script after editing an agent.

  Skill links use junctions (no admin needed). If linking fails, it falls back
  to a copy, and edits then need a re-run to propagate.

.PARAMETER Only
  Install to a single host: claude, opencode or antigravity.

.EXAMPLE
  .\install.ps1
  .\install.ps1 -Only claude
#>

param(
    [ValidateSet("claude", "opencode", "antigravity")]
    [string]$Only
)

$ErrorActionPreference = "Stop"

$skillsSrc     = Join-Path $PSScriptRoot "skills"
$hostSkillsSrc = Join-Path $PSScriptRoot "skills-only"
$agentsSrc     = Join-Path $PSScriptRoot "agents"
$home_         = $env:USERPROFILE

# Each install target: Host = adapter key (selects skills-only/<host> and agents/<name>/<host>.yaml)
$targets = @(
    @{ Host = "claude";      Label = "Claude Code";     Skills = "$home_\.claude\skills";                  Agents = "$home_\.claude\agents" }
    @{ Host = "opencode";    Label = "opencode";        Skills = "$home_\.config\opencode\skills";         Agents = "$home_\.config\opencode\agents" }
    @{ Host = "antigravity"; Label = "Antigravity";     Skills = "$home_\.gemini\config\skills";           Agents = "$home_\.gemini\config\agents" }
    @{ Host = "antigravity"; Label = "Antigravity CLI"; Skills = "$home_\.gemini\antigravity-cli\skills";  Agents = "$home_\.gemini\antigravity-cli\agents" }
)
if ($Only) { $targets = $targets | Where-Object { $_.Host -eq $Only } }

function Remove-Existing($Path) {
    if (-not (Test-Path -LiteralPath $Path)) {
        # Test-Path is false for a dangling link; remove it anyway.
        $item = Get-Item -LiteralPath $Path -Force -ErrorAction SilentlyContinue
        if ($item) { $item.Delete() }
        return
    }
    $item = Get-Item -LiteralPath $Path -Force
    if ($item.LinkType) { $item.Delete() }   # remove the link, never its target
    else { Remove-Item -LiteralPath $Path -Recurse -Force }
}

function Install-SkillFolders($SrcDir, $TargetRoot, $Label) {
    if (-not (Test-Path $SrcDir)) { return }
    New-Item -ItemType Directory -Force -Path $TargetRoot | Out-Null
    foreach ($item in Get-ChildItem $SrcDir -Directory) {
        $dest = Join-Path $TargetRoot $item.Name
        Remove-Existing $dest
        try {
            New-Item -ItemType Junction -Path $dest -Target $item.FullName -ErrorAction Stop | Out-Null
            Write-Host "LINK   $Label skill: $($item.Name)"
        } catch {
            Copy-Item -LiteralPath $item.FullName -Destination $dest -Recurse -Force
            Write-Host "COPY   $Label skill: $($item.Name)  (link unavailable, copied)"
        }
    }
}

$utf8NoBom = New-Object System.Text.UTF8Encoding($false)   # a BOM before '---' breaks frontmatter parsing

function Install-Agents($HostKey, $TargetRoot, $Label) {
    if (-not (Test-Path $agentsSrc)) { return }
    New-Item -ItemType Directory -Force -Path $TargetRoot | Out-Null
    foreach ($agentDir in Get-ChildItem $agentsSrc -Directory) {
        $bodyPath = Join-Path $agentDir.FullName "body.md"
        $yamlPath = Join-Path $agentDir.FullName "$HostKey.yaml"
        if (-not (Test-Path $bodyPath)) { continue }
        if (-not (Test-Path $yamlPath)) {
            Write-Host "SKIP   $Label agent: $($agentDir.Name)  (no $HostKey.yaml)"
            continue
        }
        $frontmatter = [System.IO.File]::ReadAllText($yamlPath).TrimEnd()
        $body        = [System.IO.File]::ReadAllText($bodyPath)
        $dest        = Join-Path $TargetRoot "$($agentDir.Name).md"
        Remove-Existing $dest
        [System.IO.File]::WriteAllText($dest, "---`n$frontmatter`n---`n`n$body", $utf8NoBom)
        Write-Host "GEN    $Label agent: $($agentDir.Name)"
    }
}

foreach ($t in $targets) {
    Install-SkillFolders $skillsSrc $t.Skills $t.Label
    Install-SkillFolders (Join-Path $hostSkillsSrc $t.Host) $t.Skills $t.Label
    Install-Agents $t.Host $t.Agents $t.Label
}

Write-Host ""
Write-Host "Done. Re-run after editing an agent (agents are generated copies; skills are live links)."
Write-Host "Verify: Claude Code -> new session, check skills + /agents; opencode -> 'what skills are available?'; Antigravity CLI -> /skills and /agents"
