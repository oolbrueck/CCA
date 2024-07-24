

# Path to the Python executable
$pythonExe = "python"  # Passen Sie diesen Pfad an, falls Python nicht in Ihrem PATH ist

# Path to the Python script
$scriptPath = "./CodeCompletion.py"

# Pfad zur JSON-Datei
$jsonFilePath = "C:\Users\oligo\IdeaProjects\CCA GPT\problemSets\leetCodeProblems.json"

# JSON-Daten aus der Datei lesen
$jsonContent = Get-Content -Path $jsonFilePath -Raw | ConvertFrom-Json

# Iteration über jedes Element im Array
foreach ($item in $jsonContent) {
$args = @(
    $PathToRepo = $item.repo_path
    $CurrentFile = $item.current_file
    $CursorPosition = $item.cursor_position
    $OpenAIKey = "your_openai_key"
    $CompareMethod = "jaccard"
    $DomainWindowSize = 20
    $CoDomainWindowSize = 60
    $ContextTokenLimit = 100
    $IntersectionThreshold = 0.2
    $ValueThreshold = 0.2
    $Model = "gpt-3.5-turbo-0125"
    $OriginalCode = $item.solution
    )
    & $pythonExe @args
}

