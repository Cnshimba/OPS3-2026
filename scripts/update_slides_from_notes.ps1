# Backup slides and replace article content with student notes article content
$root = Get-Location
$slides = Get-ChildItem -Path $root -Recurse -Include *_Slides.html -File
foreach ($s in $slides) {
    $notesPath = Join-Path $s.DirectoryName ($s.Name -replace '_Slides.html','_Student_Notes.html')
    if (Test-Path $notesPath) {
        $slidesPath = $s.FullName
        $notesText = Get-Content -Raw -LiteralPath $notesPath
        $notesMatch = [regex]::Match($notesText, '(?s)<article\b[^>]*>(.*?)</article>')
        if ($notesMatch.Success) {
            $inner = $notesMatch.Groups[1].Value
            $slidesText = Get-Content -Raw -LiteralPath $slidesPath
            $pattern = '(?s)(<article\b[^>]*>).*?(</article>)'
            $replacement = '$1' + $inner + '$2'
            $newSlides = [regex]::Replace($slidesText, $pattern, $replacement)
            if ($newSlides -ne $slidesText) {
                Copy-Item -LiteralPath $slidesPath -Destination ($slidesPath + '.bak') -Force
                Set-Content -LiteralPath $slidesPath -Value $newSlides
                Write-Host "Updated: $slidesPath (backup created)"
            } else {
                Write-Host "No changes needed: $slidesPath"
            }
        } else {
            Write-Host "No <article> found in notes: $notesPath"
        }
    } else {
        Write-Host "No matching notes file for: $($s.Name)"
    }
}
Write-Host "Done."