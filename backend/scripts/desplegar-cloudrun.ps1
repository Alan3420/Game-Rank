# Despliega el backend en Google Cloud Run.
# Uso (desde backend/):  powershell -ExecutionPolicy Bypass -File scripts\desplegar-cloudrun.ps1
#
# Lee DB_URI, SECRET_KEY y RAWG_API_KEY de app/.env y las pasa a Cloud Run en
# un archivo temporal que se borra al terminar: los secretos nunca se suben
# al repositorio. La region europe-west4 (Paises Bajos) esta junto a la base
# de Aiven (Amsterdam).
param(
    [string]$Servicio = "game-rank-api",
    [string]$Region = "europe-west4",
    [string]$OrigenFrontend = "https://game-rank-2h1.pages.dev",
    [string]$MostrarDocs = "true"
)

$ErrorActionPreference = "Stop"
$raiz = Split-Path -Parent $PSScriptRoot
$rutaEnv = Join-Path $raiz "app\.env"

if (-not (Get-Command gcloud -ErrorAction SilentlyContinue)) {
    throw "No se encuentra gcloud. Instala Google Cloud SDK y ejecuta 'gcloud auth login'."
}
if (-not (Test-Path $rutaEnv)) {
    throw "No existe $rutaEnv"
}

# lee KEY=VALOR del .env (ignora comentarios y lineas vacias)
$valores = @{}
foreach ($linea in Get-Content $rutaEnv) {
    $l = $linea.Trim()
    if ($l -eq "" -or $l.StartsWith("#") -or -not $l.Contains("=")) { continue }
    $i = $l.IndexOf("=")
    $valores[$l.Substring(0, $i).Trim()] = $l.Substring($i + 1).Trim().Trim('"').Trim("'")
}

foreach ($obligatoria in @("DB_URI", "SECRET_KEY", "RAWG_API_KEY")) {
    if (-not $valores.ContainsKey($obligatoria) -or $valores[$obligatoria] -eq "") {
        throw "Falta $obligatoria en app/.env"
    }
}

# archivo temporal de variables (YAML con comillas simples escapadas)
function Comillas([string]$v) { "'" + $v.Replace("'", "''") + "'" }
$temporal = Join-Path $env:TEMP ("cloudrun-env-" + [guid]::NewGuid().ToString() + ".yaml")
@(
    "DB_URI: " + (Comillas $valores["DB_URI"])
    "SECRET_KEY: " + (Comillas $valores["SECRET_KEY"])
    "RAWG_API_KEY: " + (Comillas $valores["RAWG_API_KEY"])
    "FRONTEND_ORIGIN: " + (Comillas $OrigenFrontend)
    "MOSTRAR_DOCS: " + (Comillas $MostrarDocs)
    "WEB_CONCURRENCY: '2'"
) | Set-Content -Path $temporal -Encoding utf8

try {
    Write-Host "Activando las APIs necesarias (solo tarda la primera vez)..."
    gcloud services enable run.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com
    if ($LASTEXITCODE -ne 0) { throw "No se pudieron activar las APIs" }

    Write-Host "Desplegando $Servicio en $Region..."
    gcloud run deploy $Servicio `
        --source $raiz `
        --region $Region `
        --allow-unauthenticated `
        --env-vars-file $temporal `
        --memory 512Mi `
        --cpu 1 `
        --min-instances 0 `
        --max-instances 2 `
        --cpu-boost `
        --port 8080 `
        --quiet
    if ($LASTEXITCODE -ne 0) { throw "El despliegue ha fallado (mira el mensaje de gcloud arriba)" }
}
finally {
    Remove-Item $temporal -Force -ErrorAction SilentlyContinue
}

$url = gcloud run services describe $Servicio --region $Region --format "value(status.url)"
Write-Host ""
Write-Host "Backend publicado en: $url"
Write-Host "Ponla en frontend/.env.production como VITE_API_URL=$url"
