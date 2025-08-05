<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Http\JsonResponse;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Facades\Storage;

class SignLanguageController extends Controller
{
    // Data akurasi per huruf dari model Anda
    private $accuracyData = [
        'A' => 100.00, 'B' => 100.00, 'C' => 100.00, 'D' => 100.00,
        'E' => 100.00, 'F' => 100.00, 'G' => 100.00, 'H' => 100.00,
        'I' => 100.00, 'J' => 100.00, 'K' => 95.65, 'L' => 100.00,
        'M' => 100.00, 'N' => 100.00, 'O' => 95.24, 'P' => 100.00,
        'Q' => 100.00, 'R' => 100.00, 'S' => 100.00, 'T' => 95.65,
        'U' => 95.24, 'V' => 95.00, 'W' => 100.00, 'X' => 96.00,
        'Y' => 100.00, 'Z' => 100.00
    ];

    public function predict(Request $request): JsonResponse
    {
        try {
            // Set longer execution time
            set_time_limit(120); // 2 minutes
            ini_set('max_execution_time', 120);
            
            // Enhanced logging untuk debugging
            Log::info('🔍 Prediction request received', [
                'has_image' => $request->has('image'),
                'image_length' => $request->has('image') ? strlen($request->input('image')) : 0,
                'user_agent' => $request->userAgent(),
                'ip' => $request->ip()
            ]);

            $request->validate([
                'image' => 'required|string' // base64 image
            ]);
    
            // Enhanced base64 image processing
            $imageData = $request->input('image');
            
            // Remove various possible base64 prefixes
            $prefixes = [
                'data:image/jpeg;base64,',
                'data:image/jpg;base64,',
                'data:image/png;base64,',
                'data:image/webp;base64,'
            ];
            
            foreach ($prefixes as $prefix) {
                if (strpos($imageData, $prefix) === 0) {
                    $imageData = substr($imageData, strlen($prefix));
                    break;
                }
            }
            
            $imageData = str_replace([' ', '\n', '\r', '\t'], '', $imageData);
            $decodedImage = base64_decode($imageData);
    
            if (!$decodedImage || strlen($decodedImage) < 1000) {
                Log::error('❌ Failed to decode base64 image or image too small', [
                    'decoded_size' => $decodedImage ? strlen($decodedImage) : 0
                ]);
                return response()->json([
                    'success' => false,
                    'message' => 'Invalid or corrupted image data'
                ]);
            }

            // Create unique temporary file to avoid conflicts
            $tempFileName = 'temp_image_' . uniqid() . '_' . time() . '.jpg';
            $tempPath = storage_path('app/' . $tempFileName);
            
            // Ensure storage directory exists
            $storageDir = dirname($tempPath);
            if (!is_dir($storageDir)) {
                mkdir($storageDir, 0755, true);
            }
            
            $bytesWritten = file_put_contents($tempPath, $decodedImage);
            
            if (!$bytesWritten) {
                Log::error('❌ Failed to save temporary image', [
                    'temp_path' => $tempPath,
                    'storage_writable' => is_writable($storageDir)
                ]);
                return response()->json([
                    'success' => false,
                    'message' => 'Failed to save image to storage'
                ]);
            }
            
            Log::info('💾 Image saved successfully', [
                'temp_path' => $tempPath,
                'file_size' => filesize($tempPath)
            ]);
    
            // Enhanced Python script execution
            $pythonScript = base_path('python/predict_sign.py');
            $modelPath = base_path('python/model.p');
            
            // Comprehensive file existence checks
            if (!file_exists($pythonScript)) {
                Log::error('❌ Python script not found', ['path' => $pythonScript]);
                $this->cleanupTempFile($tempPath);
                return response()->json([
                    'success' => false,
                    'message' => 'Python script not found: ' . $pythonScript
                ]);
            }
            
            if (!file_exists($modelPath)) {
                Log::error('❌ Model file not found', ['path' => $modelPath]);
                $this->cleanupTempFile($tempPath);
                return response()->json([
                    'success' => false,
                    'message' => 'Model file not found: ' . $modelPath
                ]);
            }
            
            // Enhanced command execution with better error handling
            $pythonExecutable = $this->findPythonExecutable();
            $command = sprintf('"%s" "%s" "%s" "%s"', $pythonExecutable, $pythonScript, $tempPath, $modelPath);
            
            Log::info('🐍 Executing Python command', ['command' => $command]);
            
            // Execute with timeout and comprehensive error capture
            $descriptorspec = [
                0 => ["pipe", "r"],  // stdin
                1 => ["pipe", "w"],  // stdout
                2 => ["pipe", "w"]   // stderr
            ];
            
            // Execute with longer timeout
            $process = proc_open($command, $descriptorspec, $pipes);
            
            if (is_resource($process)) {
                // Set longer timeout for process
                $timeout = 90; // 90 seconds
                $start_time = time();
                
                do {
                    $status = proc_get_status($process);
                    if (!$status['running']) {
                        break;
                    }
                    usleep(100000); // 0.1 second
                } while ((time() - $start_time) < $timeout);
                
                // Close stdin
                fclose($pipes[0]);
                
                // Read stdout and stderr
                $output = stream_get_contents($pipes[1]);
                $error_output = stream_get_contents($pipes[2]);
                
                fclose($pipes[1]);
                fclose($pipes[2]);
                
                $return_value = proc_close($process);
                
                Log::info('🔄 Python execution completed', [
                    'return_code' => $return_value,
                    'output_length' => strlen($output),
                    'error_output' => $error_output
                ]);
            } else {
                Log::error('❌ Failed to start Python process');
                $this->cleanupTempFile($tempPath);
                return response()->json([
                    'success' => false,
                    'message' => 'Failed to execute Python script'
                ]);
            }
            
            // Clean up temp file immediately after processing
            $this->cleanupTempFile($tempPath);
    
            if (empty($output)) {
                Log::error('❌ No output from Python script', [
                    'error_output' => $error_output,
                    'return_code' => $return_value ?? 'unknown'
                ]);
                return response()->json([
                    'success' => false,
                    'message' => 'No output from Python script. Error: ' . $error_output
                ]);
            }
            
            // Enhanced JSON extraction
            $outputLines = explode("\n", trim($output));
            $jsonLine = '';
            
            // Look for JSON line (starts with {)
            foreach (array_reverse($outputLines) as $line) {
                $line = trim($line);
                if (strpos($line, '{') === 0 && strpos($line, '}') !== false) {
                    $jsonLine = $line;
                    break;
                }
            }
            
            if (empty($jsonLine)) {
                Log::error('❌ No valid JSON found in output', [
                    'raw_output' => $output,
                    'output_lines' => $outputLines
                ]);
                return response()->json([
                    'success' => false,
                    'message' => 'No valid JSON response from Python script'
                ]);
            }
            
            $result = json_decode($jsonLine, true);
            
            if (json_last_error() !== JSON_ERROR_NONE) {
                Log::error('❌ JSON decode error', [
                    'error' => json_last_error_msg(),
                    'json_line' => $jsonLine
                ]);
                return response()->json([
                    'success' => false,
                    'message' => 'Invalid JSON response: ' . json_last_error_msg()
                ]);
            }
            
            // Enhanced result processing
            if ($result && !isset($result['error']) && isset($result['prediction']) && !empty($result['prediction'])) {
                $prediction = strtoupper(trim($result['prediction']));
                $confidence = floatval($result['confidence'] ?? 0);
                
                Log::info('✅ Successful prediction', [
                    'prediction' => $prediction,
                    'confidence' => $confidence
                ]);
                
                return response()->json([
                    'success' => true,
                    'prediction' => $prediction,
                    'confidence' => round($confidence, 2),
                    'accuracy' => $this->accuracyData[$prediction] ?? 95.0
                ]);
            } else {
                $errorMsg = $result['error'] ?? 'Unknown prediction error';
                Log::warning('⚠️ Python script returned error', [
                    'error' => $errorMsg,
                    'full_result' => $result
                ]);
                
                return response()->json([
                    'success' => false,
                    'message' => $errorMsg
                ]);
            }
    
        } catch (\Exception $e) {
            Log::error('💥 Sign language prediction exception', [
                'message' => $e->getMessage(),
                'file' => $e->getFile(),
                'line' => $e->getLine(),
                'trace' => $e->getTraceAsString()
            ]);
            
            return response()->json([
                'success' => false,
                'message' => 'Prediction failed: ' . $e->getMessage()
            ], 500);
        }
    }
    
    private function findPythonExecutable(): string
    {
        // Try different Python executable names
        $pythonCommands = ['python', 'python3', 'py'];
        
        foreach ($pythonCommands as $cmd) {
            $output = shell_exec("where $cmd 2>nul");
            if (!empty($output)) {
                return trim($cmd);
            }
        }
        
        return 'python'; // Default fallback
    }
    
    private function cleanupTempFile(string $path): void
    {
        if (file_exists($path)) {
            unlink($path);
            Log::info('🗑️ Cleaned up temporary file', ['path' => $path]);
        }
    }

    public function getAccuracyData(): JsonResponse
    {
        return response()->json([
            'success' => true,
            'data' => $this->accuracyData
        ]);
    }
}