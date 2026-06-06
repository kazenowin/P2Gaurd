import React, { useState } from 'react';

function App() {
  // --- PASTE YOUR GANACHE ADDRESSES HERE ---
  const WALLET_UNLICENSED = "0x14420f537057606f97AF35714bF2b7a8060C1F1b"; 
  const WALLET_LICENSED = "0x1467B20D296b00519628343E6F333E5710504724";   

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const runSimulation = async (scenario) => {
    setLoading(true);
    setResult(null);

    let payload = { wallet_address: "", packet_sizes: [] };

    if (scenario === 1) {
      payload.wallet_address = WALLET_UNLICENSED;
      
      // OPTIMIZED DEMO DATA: Realistic HTTP Web Browsing Signature
      // Simulates a standard burst: [Tiny Request, Server ACK, Big HTML, Med Images, Idle...]
      // Guarantees deterministic, self-contained demonstration.
      payload.packet_sizes = [0.0133, 0.967, 0.9817, 0.1004, 0.9143, 0.0635, 0.9814, 0.6485, 0.993, 0.9843, 0.3809, 0.9835, 0.2783, 0.0244, 0.0213, 0.1549, 0.1287, 0.4814, 0.8165, 0.7095];
    } else if (scenario === 2) {
      payload.wallet_address = WALLET_LICENSED;
      payload.packet_sizes = [0.9, 0.95, 0.85, 1.0, 0.9, 0.95, 0.88, 0.92, 0.9, 0.99, 1.0, 0.95, 0.9, 0.85, 0.9, 1.0, 0.95, 0.9, 0.85, 0.9];
    } else if (scenario === 3) {
      payload.wallet_address = WALLET_UNLICENSED;
      payload.packet_sizes = [0.9, 0.95, 0.85, 1.0, 0.9, 0.95, 0.88, 0.92, 0.9, 0.99, 1.0, 0.95, 0.9, 0.85, 0.9, 1.0, 0.95, 0.9, 0.85, 0.9];
    }

    try {
      const response = await fetch("http://127.0.0.1:8000/api/evaluate-traffic", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      
      const data = await response.json();
      setResult(data);
    } catch (error) {
      setResult({ status: "error", message: "Failed to connect to Python backend." });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen p-8 flex flex-col items-center">
      <header className="mb-12 text-center">
        <h1 className="text-4xl font-extrabold text-blue-500 tracking-wider">P2GUARD SENTINEL</h1>
        <p className="text-slate-400 mt-2">Decentralized Anti-Piracy Framework</p>
      </header>

      <div className="w-full max-w-6xl grid grid-cols-1 md:grid-cols-2 gap-8">
        
        <div className="bg-slate-800 p-6 rounded-xl border border-slate-700 shadow-lg h-fit">
          <h2 className="text-xl font-bold mb-6 text-slate-200 border-b border-slate-600 pb-2">Simulation Controls</h2>
          <div className="space-y-4">
            <button onClick={() => runSimulation(1)} className="w-full bg-slate-700 hover:bg-blue-600 text-white font-semibold py-3 px-4 rounded transition-colors">
              1. Simulate Normal Web Traffic
            </button>
            <button onClick={() => runSimulation(2)} className="w-full bg-slate-700 hover:bg-emerald-600 text-white font-semibold py-3 px-4 rounded transition-colors">
              2. Simulate Authorized P2P (Licensed)
            </button>
            <button onClick={() => runSimulation(3)} className="w-full bg-slate-700 hover:bg-red-600 text-white font-semibold py-3 px-4 rounded transition-colors">
              3. Simulate Piracy (Unauthorized)
            </button>
          </div>
        </div>

        <div className="bg-slate-900 p-6 rounded-xl border border-slate-700 shadow-inner flex flex-col min-h-[400px]">
          <h2 className="text-xl font-bold mb-6 text-slate-200 border-b border-slate-600 pb-2">System Telemetry</h2>
          
          <div className="flex-grow flex flex-col justify-center items-center">
            {loading ? (
              <div className="text-blue-400 animate-pulse text-lg">Analyzing network tensor & Generating XAI Audit...</div>
            ) : result ? (
              <div className="w-full space-y-4">
                
                <div className={`p-4 rounded-lg border text-center ${result.action === 'block' ? 'bg-red-900/30 border-red-500/50 text-red-400' : 'bg-emerald-900/30 border-emerald-500/50 text-emerald-400'}`}>
                  <h3 className="text-2xl font-black uppercase tracking-widest">{result.action}</h3>
                </div>

                <div className="bg-slate-800 p-4 rounded text-sm font-mono text-slate-300">
                  <p><span className="text-blue-400">P2P Probability:</span> {result.probability ? (result.probability * 100).toFixed(2) + '%' : 'N/A'}</p>
                  <p className="mt-2"><span className="text-blue-400">System Message:</span> {result.message}</p>
                </div>

                {/* FLAW 2 FIX: The XAI Audit Image Renderer */}
                {result.shap_image && (
                  <div className="mt-6 border-t border-slate-600 pt-4 animate-fade-in">
                    <h3 className="text-lg font-bold text-slate-300 mb-4">XAI Audit Log Generated</h3>
                    <div className="bg-white p-2 rounded-lg">
                      <img 
                        src={`data:image/png;base64,${result.shap_image}`} 
                        alt="SHAP Beeswarm Plot" 
                        className="w-full h-auto rounded"
                      />
                    </div>
                  </div>
                )}

              </div>
            ) : (
              <div className="text-slate-500 text-center">
                <p>System idle.</p>
                <p className="text-sm">Awaiting traffic simulation...</p>
              </div>
            )}
          </div>
        </div>

      </div>
    </div>
  );
}

export default App;