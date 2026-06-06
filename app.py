from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
import tensorflow as tf
from web3 import Web3
import shap
import matplotlib
import matplotlib.pyplot as plt
import io
import base64

# Force Matplotlib to run in background (Server Mode)
matplotlib.use('Agg')

app = FastAPI(title="P2Guard API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TrafficPayload(BaseModel):
    wallet_address: str
    packet_sizes: list[float]

try:
    cnn_model = tf.keras.models.load_model('p2guard_cnn_model.h5', compile=False)
    
    web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:6780")) # Ensure your port is correct!
    
    # !!! PASTE YOUR REMIX CONTRACT ADDRESS HERE !!!
    contract_address = web3.to_checksum_address('0x5c4A58ee01eeBb1afA01B59154cC170F614AC343')
    
    contract_abi = [{
        "inputs": [{"internalType": "address", "name": "_user", "type": "address"}],
        "name": "verifyLicense",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function"
    }]
    contract = web3.eth.contract(address=contract_address, abi=contract_abi)
    
except Exception as e:
    print(f"Startup Error: {e}")

@app.post("/api/evaluate-traffic")
async def evaluate_traffic(payload: TrafficPayload):
    try:
        traffic_tensor = np.array(payload.packet_sizes).reshape(1, 20, 1)
        
        # --- SENTINEL LAYER ---
        probability = float(cnn_model.predict(traffic_tensor, verbose=0)[0][0])
        is_p2p = probability > 0.4
        
        if not is_p2p:
            return {
                "status": "success",
                "probability": probability,
                "action": "allow",
                "message": "Traffic is normal."
            }

        # --- LEDGER LAYER ---
        safe_wallet = web3.to_checksum_address(payload.wallet_address)
        has_license = contract.functions.verifyLicense(safe_wallet).call()

        if has_license:
            return {
                "status": "success",
                "probability": probability,
                "action": "allow",
                "message": "P2P detected, but valid blockchain license found."
            }
        
        # --- CONTROLLER LAYER (Generate SHAP Graph) ---
        def predict_wrapper(data):
            data_reshaped = data.reshape(-1, 20, 1)
            return cnn_model.predict(data_reshaped, verbose=0).flatten()

        # OPTIMIZATION 1: Reduce background data to 10 samples
        background_data = np.random.rand(10, 20)
        explainer = shap.KernelExplainer(predict_wrapper, background_data)
        
        # OPTIMIZATION 2: Reduce batch from 300 to 100 
        test_batch = np.vstack([
            np.array(payload.packet_sizes).reshape(1, 20),
            np.random.rand(99, 20)
        ])
        
        # OPTIMIZATION 3: Restrict 'nsamples' to stop the math from spiraling
        shap_values = explainer.shap_values(test_batch, nsamples=50)
        sv = shap_values[0] if isinstance(shap_values, list) else shap_values
        
        plt.figure(figsize=(10, 6))
        feature_names = [f"Packet {i+1} Size" for i in range(20)]
        shap.summary_plot(sv, test_batch, feature_names=feature_names, show=False)
        plt.title("XAI Audit: Feature Importance for Piracy Classification", fontsize=14, pad=15)
        plt.tight_layout()
        
        # Save image to a memory buffer instead of the hard drive
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
        buf.seek(0)
        
        # Convert the image buffer into a Base64 string
        image_base64 = base64.b64encode(buf.read()).decode('utf-8')
        plt.close() # Free memory!

        return {
            "status": "blocked",
            "probability": probability,
            "action": "block",
            "message": "Piracy detected. No valid license on the blockchain.",
            "shap_image": image_base64
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))