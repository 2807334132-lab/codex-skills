param(
    [Parameter(Mandatory = $true)]
    [string]$InputPath,

    [int]$LongEdge,
    [int]$Width,
    [int]$Height,

    [string]$OutputPath,
    [switch]$Overwrite
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

if (-not (Test-Path -LiteralPath $InputPath)) {
    throw "Input file does not exist: $InputPath"
}

$modeCount = @($LongEdge, $Width, $Height | Where-Object { $_ -gt 0 }).Count
if ($modeCount -ne 1) {
    throw "Specify exactly one positive resize target: -LongEdge, -Width, or -Height."
}

Add-Type -AssemblyName System.Drawing

$source = [System.Drawing.Image]::FromFile($InputPath)
try {
    $srcW = $source.Width
    $srcH = $source.Height

    if ($LongEdge -gt 0) {
        if ($srcW -ge $srcH) {
            $newW = $LongEdge
            $newH = [int][Math]::Round($srcH * ($LongEdge / $srcW))
        } else {
            $newH = $LongEdge
            $newW = [int][Math]::Round($srcW * ($LongEdge / $srcH))
        }
        $suffix = "_${LongEdge}px"
    } elseif ($Width -gt 0) {
        $newW = $Width
        $newH = [int][Math]::Round($srcH * ($Width / $srcW))
        $suffix = "_w${Width}"
    } else {
        $newH = $Height
        $newW = [int][Math]::Round($srcW * ($Height / $srcH))
        $suffix = "_h${Height}"
    }

    if ($newW -lt 1 -or $newH -lt 1) {
        throw "Computed output dimensions are invalid: ${newW}x${newH}"
    }

    if ([string]::IsNullOrWhiteSpace($OutputPath)) {
        $dir = Split-Path -LiteralPath $InputPath -Parent
        $name = [System.IO.Path]::GetFileNameWithoutExtension($InputPath)
        $ext = [System.IO.Path]::GetExtension($InputPath)
        $OutputPath = Join-Path $dir "$name$suffix$ext"
    }

    if ((Test-Path -LiteralPath $OutputPath) -and -not $Overwrite) {
        throw "Output file already exists: $OutputPath. Use -Overwrite or choose another -OutputPath."
    }

    $bitmap = New-Object System.Drawing.Bitmap($newW, $newH)
    try {
        $bitmap.SetResolution($source.HorizontalResolution, $source.VerticalResolution)
        $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
        try {
            $graphics.CompositingQuality = [System.Drawing.Drawing2D.CompositingQuality]::HighQuality
            $graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
            $graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::HighQuality
            $graphics.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
            $graphics.DrawImage($source, 0, 0, $newW, $newH)
        } finally {
            $graphics.Dispose()
        }

        $extension = [System.IO.Path]::GetExtension($OutputPath).ToLowerInvariant()
        switch ($extension) {
            '.jpg' { $format = [System.Drawing.Imaging.ImageFormat]::Jpeg }
            '.jpeg' { $format = [System.Drawing.Imaging.ImageFormat]::Jpeg }
            '.bmp' { $format = [System.Drawing.Imaging.ImageFormat]::Bmp }
            '.gif' { $format = [System.Drawing.Imaging.ImageFormat]::Gif }
            default { $format = [System.Drawing.Imaging.ImageFormat]::Png }
        }

        $bitmap.Save($OutputPath, $format)
    } finally {
        $bitmap.Dispose()
    }
} finally {
    $source.Dispose()
}

$check = [System.Drawing.Image]::FromFile($OutputPath)
try {
    [PSCustomObject]@{
        OutputPath = $OutputPath
        Width = $check.Width
        Height = $check.Height
    } | Format-List
} finally {
    $check.Dispose()
}
