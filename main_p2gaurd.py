import numpy as np
import tensorflow as tf
from web3 import Web3
import shap
import matplotlib.pyplot as plt

# ==========================================
# SETUP & BLOCKCHAIN CONNECTION
# ==========================================
ganache_url = "http://127.0.0.1:6780" 
web3 = Web3(Web3.HTTPProvider(ganache_url))

if web3.is_connected():
    print("SUCCESS: Python is connected to Ganache!")
else:
    print("FAILED: Python still cannot see Ganache. Check the URL/Port.")

contract_address = '0x7E01EeC1A47c69933A9F01A35ba897a6C1ef3F93' 
safe_contract_address = web3.to_checksum_address(contract_address)

contract_abi = [
	{
		"inputs": [{"internalType": "address", "name": "_user", "type": "address"}],
		"name": "grantLicense",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [{"internalType": "address", "name": "", "type": "address"}],
		"name": "hasLicense",
		"outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [{"internalType": "address", "name": "_user", "type": "address"}],
		"name": "verifyLicense",
		"outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
		"stateMutability": "view",
		"type": "function"
	}
] 

# Initialize the contract object globally
contract = web3.eth.contract(address=safe_contract_address, abi=contract_abi)


# ==========================================
# --- LAYER 1: DETECTION ---
# ==========================================
def detect_traffic(model, incoming_traffic):
    print("\n--- SENTINEL LAYER: Analyzing Traffic ---")
    probability = model.predict(incoming_traffic, verbose=0)[0][0]
    is_p2p = probability > 0.3 # 30% confidence threshold
    print(f"P2P Traffic Probability: {probability:.2%}")
    return is_p2p


# ==========================================
# --- LAYER 2: VERIFICATION ---
# ==========================================
def verify_license(user_address, contract_instance): 
    print("\n--- LEDGER LAYER: Checking Blockchain Registry ---")
    try:
        has_license = contract_instance.functions.verifyLicense(user_address).call()

        if has_license:
            print("STATUS: Access Granted. Valid cryptographic license found.")
            return True
        else:
            print("STATUS: Access Denied. No valid license on the blockchain.")
            return False
    except Exception as e:
        print(f"Blockchain Error: {e}")
        return False


# ==========================================
# --- LAYER 3: GOVERNANCE (XAI) ---
# ==========================================
def generate_audit_log(cnn_model, simulated_traffic):
    print("\n--- CONTROLLER LAYER: Generating XAI Audit Log ---")
    print("Generating rich global justification chart (this may take a few seconds)...")
    
    # 1. Wrapper function for Keras
    def predict_wrapper(data):
        data_reshaped = data.reshape(-1, 20, 1)
        return cnn_model.predict(data_reshaped, verbose=0).flatten()

    # 2. Background data for the Explainer baseline
    background_data = np.random.rand(50, 20)
    explainer = shap.KernelExplainer(predict_wrapper, background_data)

    # 3. THE FIX: Generate a large batch of flows (300) for the dense Beeswarm plot
    # We include the specific user's blocked traffic as the first row, plus 299 random flows
    test_batch = np.vstack([
        simulated_traffic.reshape(1, 20),
        np.random.rand(299, 20)
    ])

    # 4. Calculate SHAP values for the entire batch
    shap_values = explainer.shap_values(test_batch)

    # 5. Generate the Plot
    feature_names = [f"Packet {i+1} Size" for i in range(20)]
    plt.figure(figsize=(10, 6))

    # Handle output shape depending on the SHAP version
    sv = shap_values[0] if isinstance(shap_values, list) else shap_values

    # Pass the entire test_batch into the summary_plot to get the gradient colors
    shap.summary_plot(sv, test_batch, feature_names=feature_names, show=False)

    plt.title("XAI Audit: Global Feature Importance for P2P Classification", fontsize=14, pad=15)
    plt.tight_layout()
    
    # Optional: Save the figure 
    plt.savefig('dense_shap_audit.png', dpi=300, bbox_inches='tight')
    plt.show()


# ==========================================
# --- MAIN EXECUTION ---
# ==========================================
if __name__ == "__main__":
    print("Loading P2Guard CNN Model...")
    try:
        cnn_model = tf.keras.models.load_model('p2guard_cnn_model.h5')
    except:
        print("Error: Run train_cnn.py first! Could not find p2guard_cnn_model.h5")
        exit()

    # Simulate an incoming user flow (20 packets)
    simulated_user_traffic = np.random.rand(1, 20, 1)
    
    # Simulate a user's crypto wallet address
    simulated_user_wallet = "0x14420f537057606f97AF35714bF2b7a8060C1F1b"
    safe_user_wallet = web3.to_checksum_address(simulated_user_wallet)

    # Run the Pipeline
    if detect_traffic(cnn_model, simulated_user_traffic):
        print("ALERT: High-probability P2P stream detected.")
        
        # Pass the safe_user_wallet and the contract object here
        if verify_license(safe_user_wallet, contract):
            print("ACTION: Access Granted. Valid blockchain license found.")
        else:
            print("ACTION: ACCESS BLOCKED. No valid license found.")
            generate_audit_log(cnn_model, simulated_user_traffic)
    else:
        print("ACTION: Traffic is normal. No action taken.")