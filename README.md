# P2Guard Sentinel 🛡️
**Decentralized Anti-Piracy & AI-Driven Network Traffic Analysis Framework**

## 📖 Overview
P2Guard is a full-stack proof-of-concept framework designed to detect unauthorized peer-to-peer (P2P) network traffic and verify digital licenses via blockchain. By combining deep learning for packet analysis with Ethereum smart contracts for zero-trust license verification, P2Guard offers a modernized approach to decentralized digital rights management.

## 🏗️ System Architecture
The framework is divided into three distinct operational layers:

1. **The Sentinel Layer (Machine Learning)**
   - Ingests network traffic arrays (packet sizes) representing temporal web flows.
   - Utilizes a Convolutional Neural Network (CNN) trained on network signatures to predict the probability of P2P activity.
2. **The Ledger Layer (Web3/Blockchain)**
   - If P2P traffic is detected, the system queries an Ethereum Smart Contract (`LicenseCheck`).
   - Validates the user's cryptographic wallet address to see if they hold a legitimate license for the content.
3. **The Controller Layer (Explainable AI & UI)**
   - Acts as the command center, returning a definitive **ALLOW** or **BLOCK** action.
   - Integrates the **SHAP (SHapley Additive exPlanations)** library to instantly generate an Explainable AI (XAI) beeswarm plot, visually auditing exactly which network packets triggered the CNN's decision.

```text
[ React.js Frontend ] 
        │ (JSON Traffic Payloads)
        ▼
[ FastAPI Backend ] ──► [ CNN Model (.h5) ] ──► (Traffic > 40% P2P?)
        │                                              │
        │                                              ▼ (Yes)
        │                               [ Web3.js / Smart Contract ]
        │                                              │
        ▼                                              ▼
[ SHAP XAI Generator ] ◄── (Action: Block) ◄── (Unlicensed Wallet)
        │
        ▼ (Base64 Image)
[ React Dashboard: Render Telemetry & XAI Audit ]

Setup for the Ledger Layer
### 1. Blockchain & Wallet Setup (Ganache)
Because this framework relies on smart contracts to verify licenses, you must run a local Ethereum blockchain to test the UI.

**A. Start Your Local Blockchain**
1. Download and install [Ganache](https://trufflesuite.com/ganache/).
2. Click **Quickstart** to launch a local testnet. 
3. Ensure your Ganache RPC Server is running on `http://127.0.0.1:7545` (this is the default).

**B. Deploy the Smart Contract**
1. Open [Remix IDE](https://remix.ethereum.org/) in your browser.
2. Compile the `LicenseCheck.sol` contract provided in this repository.
3. In Remix's "Deploy & Run Transactions" tab, change the Environment to **Dev - Ganache Provider** and connect to your `7545` port.
4. Deploy the contract.
5. **Action Required:** Copy the newly deployed Contract Address and paste it into `app.py` on **Line 34**:
   `contract_address = web3.to_checksum_address('0xYOUR_CONTRACT_ADDRESS')`

**C. Configure Frontend Wallets**
To test the "Licensed" vs "Unlicensed" simulation buttons, you need to provide the frontend with two distinct wallet addresses from your Ganache instance.
1. Open Ganache and look at the list of available accounts.
2. **Action Required:** Open `p2guard-dashboard/src/App.jsx` and locate lines 5 and 6 at the top of the file.
3. Copy **Address 1** from Ganache and paste it as the `WALLET_UNLICENSED` variable.
4. Copy **Address 2** from Ganache and paste it as the `WALLET_LICENSED` variable.
5. *(Optional for Full Simulation)*: Using Remix, interact with your deployed smart contract to manually grant a license to Address 2 so the backend successfully validates it during Scenario 2.
