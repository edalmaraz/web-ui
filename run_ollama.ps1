# Set environment variables for optimal performance
$env:CUDA_VISIBLE_DEVICES = "0"
$env:OMP_NUM_THREADS = "16"
$env:MKL_NUM_THREADS = "16"

# Kill any existing Ollama processes
taskkill /F /IM ollama.exe 2>$null

# Start Ollama with optimized configuration
$ollamaPath = "C:\Program Files\Ollama\ollama.exe"
Start-Process -FilePath $ollamaPath -ArgumentList "serve" -NoNewWindow

# Wait for Ollama to start
Start-Sleep -Seconds 5

# Pull and run the model with optimized settings
ollama pull deepseek-r1:70b
ollama run deepseek-r1:70b --verbose `
    --gpu-layers 68 `
    --ctx 8192 `
    --batch 8 `
    --threads 16 `
    --f16-kv `
    --rope-scaling "dynamic" `
    --rope-factor 2.0
