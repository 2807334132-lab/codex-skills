param(
    [Parameter(Mandatory = $true)]
    [string]$InputPptx,

    [Parameter(Mandatory = $true)]
    [string]$OutputDir,

    [int]$Width = 1600,
    [int]$Height = 900
)

$resolvedInput = (Resolve-Path -LiteralPath $InputPptx).Path
$resolvedOutput = [System.IO.Path]::GetFullPath($OutputDir)
[System.IO.Directory]::CreateDirectory($resolvedOutput) | Out-Null

$powerPoint = $null
$presentation = $null

try {
    $powerPoint = New-Object -ComObject PowerPoint.Application
    $presentation = $powerPoint.Presentations.Open($resolvedInput, $true, $true, $false)
    $presentation.Export($resolvedOutput, "PNG", $Width, $Height)
}
finally {
    if ($presentation -ne $null) {
        $presentation.Close()
        [System.Runtime.InteropServices.Marshal]::ReleaseComObject($presentation) | Out-Null
    }
    if ($powerPoint -ne $null) {
        $powerPoint.Quit()
        [System.Runtime.InteropServices.Marshal]::ReleaseComObject($powerPoint) | Out-Null
    }
    [GC]::Collect()
    [GC]::WaitForPendingFinalizers()
}

$count = (Get-ChildItem -LiteralPath $resolvedOutput -File -Filter *.PNG).Count
if ($count -lt 1) {
    throw "PowerPoint exported no PNG slides."
}

Write-Output "Exported $count slides to $resolvedOutput"
