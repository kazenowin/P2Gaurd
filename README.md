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

