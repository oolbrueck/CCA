# run_code_completion.ps1

# Definieren Sie hier Ihre Parameterwerte
$PathToRepo = "path\to\repo"
$CurrentFile = "path\to\current\file.py"
$CursorPosition = 10
$OpenAIKey = "your_openai_key"
$CompareMethod = "jaccard"

# Path to the Python executable
$pythonExe = "python"  # Passen Sie diesen Pfad an, falls Python nicht in Ihrem PATH ist

# Path to the Python script
$scriptPath = "path\to\your\script.py"  # Passen Sie diesen Pfad an

# Build the argument list
$args = @(
    $scriptPath,
    $PathToRepo,
    $CurrentFile,
    $CursorPosition,
    $OpenAIKey,
    $CompareMethod
)

# Execute the Python script with arguments
& $pythonExe @args
