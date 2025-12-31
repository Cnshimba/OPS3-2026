# Fix common encoding/render issues in Slides files
$root = Get-Location
Get-ChildItem -Path $root -Recurse -Include *_Slides.html -File | ForEach-Object {
    $path = $_.FullName
    $text = Get-Content -Raw -LiteralPath $path
    $new = $text -replace '\? Back to Course Index','← Back to Course Index'
    $new = [regex]::Replace($new,'\\uFFFD','—')
    $new = [regex]::Replace($new,'\uFFFD','—')
    # Common mojibake sequences -> proper characters
    $new = $new -replace 'â€”','—'
    $new = $new -replace 'â€“','–'
    $new = $new -replace 'â€™','’'
    $new = $new -replace 'â€œ','“'
    $new = $new -replace 'â€�','”'
    $new = $new -replace 'â€¦','...'
    $new = $new -replace 'â€¢','•'
    $new = $new -replace '�','—'
    if ($new -ne $text) {
        Copy-Item -LiteralPath $path -Destination ($path + '.encbak') -Force
        Set-Content -LiteralPath $path -Value $new
        Write-Host "Fixed encoding in: $path"
    } else {
        Write-Host "No fixes needed: $path"
    }
}
Write-Host "Done."