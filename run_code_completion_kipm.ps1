$pathPrefix = "C:/Users/oligo/OneDrive/Bachelor Arbeit/repos"

# Path to the Python script
$scriptPath = "./CodeCompletion.py"

# Pfad zur JSON-Datei
$jsonFilePath = "C:\Users\oligo\IdeaProjects\CCA GPT\problemSets\contextualProblems.json"

# JSON-Daten aus der Datei lesen
$jsonContent = Get-Content -Path $jsonFilePath -Raw | ConvertFrom-Json

# Iteration über jedes Element im Array
foreach ($item in $jsonContent) {
    $args = @(
        $scriptPath
        $pathPrefix + $item.repo_path
        $pathPrefix + $item.current_file
        $item.cursor_position
        "REDACTED"
        "jaccard"
        "20"
        "60"
        "8000"
        "0.2"
        "0.2"
        "gpt-3.5-turbo-0125"
        $item.solution
    )
    python @args
}

