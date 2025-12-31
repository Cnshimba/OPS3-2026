# Replace all occurrences of Course_Index.html (any case) with index.html in .html files
$root = Get-Location
Get-ChildItem -Path $root -Recurse -Include *.html -File | ForEach-Object {
    $path = $_.FullName
    $text = Get-Content -Raw -LiteralPath $path
    $new = $text -replace '(?i)course_index\.html','index.html'
    if ($new -ne $text) { Set-Content -LiteralPath $path -Value $new; Write-Host "Updated $path" }
}
Write-Host "Replacement complete."