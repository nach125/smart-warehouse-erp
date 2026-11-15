$Port = 8080
$Root = "C:\Users\Nachiket\Downloads\ecomm\SmartWarehouseERP"

$Listener = New-Object System.Net.HttpListener
$Listener.Prefixes.Add("http://localhost:$Port/")

try {
    $Listener.Start()
    Write-Host "Smart Warehouse ERP Server running at http://localhost:$Port/"

    while ($Listener.IsListening) {
        $Context = $Listener.GetContext()
        $Request = $Context.Request
        $Response = $Context.Response

        $UrlPath = $Request.Url.LocalPath
        if ($UrlPath -eq "/" -or [string]::IsNullOrWhiteSpace($UrlPath)) {
            $UrlPath = "/index.html"
        }

        $RelativePath = $UrlPath.TrimStart("/").Replace("/", "\")
        $FilePath = Join-Path $Root $RelativePath

        if (Test-Path $FilePath -PathType Leaf) {
            $Ext = [System.IO.Path]::GetExtension($FilePath).ToLower()
            $ContentType = "application/octet-stream"
            if ($Ext -eq ".html" -or $Ext -eq ".htm") { $ContentType = "text/html; charset=utf-8" }
            elseif ($Ext -eq ".css") { $ContentType = "text/css; charset=utf-8" }
            elseif ($Ext -eq ".js") { $ContentType = "application/javascript; charset=utf-8" }
            elseif ($Ext -eq ".json") { $ContentType = "application/json; charset=utf-8" }
            elseif ($Ext -eq ".svg") { $ContentType = "image/svg+xml" }
            elseif ($Ext -eq ".sql") { $ContentType = "text/plain; charset=utf-8" }
            elseif ($Ext -eq ".md") { $ContentType = "text/markdown; charset=utf-8" }

            $Response.ContentType = $ContentType
            $Bytes = [System.IO.File]::ReadAllBytes($FilePath)
            $Response.ContentLength64 = $Bytes.Length
            $Response.OutputStream.Write($Bytes, 0, $Bytes.Length)
        } else {
            $Response.StatusCode = 404
            $NotFoundMsg = [System.Text.Encoding]::UTF8.GetBytes("404 Not Found")
            $Response.ContentLength64 = $NotFoundMsg.Length
            $Response.OutputStream.Write($NotFoundMsg, 0, $NotFoundMsg.Length)
        }
        $Response.OutputStream.Close()
    }
}
catch {
    Write-Host "Server Error: $_"
}
finally {
    if ($Listener.IsListening) { $Listener.Stop() }
    $Listener.Close()
}
