# Smart Warehouse & Order Fulfillment ERP - Native Localhost Server
$Port = 8080
$Root = "C:\Users\Nachiket\Downloads\ecomm\SmartWarehouseERP"

$Listener = New-Object System.Net.HttpListener
$Listener.Prefixes.Add("http://localhost:$Port/")
$Listener.Prefixes.Add("http://127.0.0.1:$Port/")

try {
    $Listener.Start()
    Write-Host "=========================================================="
    Write-Host "Smart Warehouse ERP Server running at http://localhost:$Port/"
    Write-Host "Serving files from: $Root"
    Write-Host "Press Ctrl+C or kill process to terminate server."
    Write-Host "=========================================================="

    while ($Listener.IsListening) {
        $Context = $Listener.GetContext()
        $Request = $Context.Request
        $Response = $Context.Response

        $UrlPath = $Request.Url.LocalPath
        if ($UrlPath -eq "/" -or $UrlPath -eq "") {
            $UrlPath = "/index.html"
        }

        # Security check - keep within root
        $RelativePath = $UrlPath.TrimStart("/").Replace("/", "\")
        $FilePath = Join-Path $Root $RelativePath

        if (Test-Path $FilePath -PathType Leaf) {
            $Ext = [System.IO.Path]::GetExtension($FilePath).ToLower()
            $ContentType = switch ($Ext) {
                ".html" { "text/html; charset=utf-8" }
                ".htm"  { "text/html; charset=utf-8" }
                ".css"  { "text/css; charset=utf-8" }
                ".js"   { "application/javascript; charset=utf-8" }
                ".json" { "application/json; charset=utf-8" }
                ".png"  { "image/png" }
                ".jpg"  { "image/jpeg" }
                ".jpeg" { "image/jpeg" }
                ".svg"  { "image/svg+xml" }
                ".sql"  { "text/plain; charset=utf-8" }
                ".md"   { "text/markdown; charset=utf-8" }
                default { "application/octet-stream" }
            }

            $Response.ContentType = $ContentType
            $Bytes = [System.IO.File]::ReadAllBytes($FilePath)
            $Response.ContentLength64 = $Bytes.Length
            $Response.OutputStream.Write($Bytes, 0, $Bytes.Length)
        } else {
            $Response.StatusCode = 404
            $NotFoundMsg = [System.Text.Encoding]::UTF8.GetBytes("404 - File Not Found in SmartWarehouseERP: $UrlPath")
            $Response.ContentLength64 = $NotFoundMsg.Length
            $Response.OutputStream.Write($NotFoundMsg, 0, $NotFoundMsg.Length)
        }

        $Response.OutputStream.Close()
    }
}
catch {
    Write-Host "Error in server: $_"
}
finally {
    if ($Listener.IsListening) {
        $Listener.Stop()
    }
    $Listener.Close()
}
