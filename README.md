<div align="center">

<br/>

```
██████╗ ██████╗  ██████╗ ██╗   ██╗ █████╗ ██████╗ ██████╗
██╔══██╗╚════██╗██╔════╝ ██║   ██║██╔══██╗██╔══██╗██╔══██╗
██████╔╝ █████╔╝██║  ███╗██║   ██║███████║██████╔╝██║  ██║
██╔═══╝ ██╔═══╝ ██║   ██║██║   ██║██╔══██║██╔══██╗██║  ██║
██║     ███████╗╚██████╔╝╚██████╔╝██║  ██║██║  ██║██████╔╝
╚═╝     ╚══════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝
                                          S E N T I N E L
```

### Decentralized Anti-Piracy & AI-Driven Network Traffic Analysis

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![React](https://img.shields.io/badge/React-Vite-61DAFB?style=flat-square&logo=react&logoColor=black)](https://reactjs.org)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-CNN-FF6F00?style=flat-square&logo=tensorflow&logoColor=white)](https://tensorflow.org)
[![Ethereum](https://img.shields.io/badge/Ethereum-Smart_Contracts-627EEA?style=flat-square&logo=ethereum&logoColor=white)](https://ethereum.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

<br/>

> **P2Guard** is a full-stack proof-of-concept that fuses deep learning packet analysis with on-chain license verification — giving you a zero-trust, explainable, and decentralized approach to digital rights management.

<br/>

</div>

---

## ✦ What Is P2Guard?

P2Guard Sentinel monitors network traffic in real time, uses a **Convolutional Neural Network** to identify unauthorized P2P activity, and immediately cross-references an **Ethereum smart contract** to validate whether the user holds a legitimate digital license. Every decision is fully auditable through **SHAP-powered Explainable AI**, so you always know *exactly* why a connection was allowed or blocked.

No black boxes. No centralized trust. Just transparent, automated enforcement.

---

## 🏗️ System Architecture

P2Guard is organized into three distinct operational layers:

```
┌─────────────────────────────────────────────────────────────────┐
│                      React.js Frontend                          │
│              (Dashboard · Telemetry · XAI Audit)                │
└────────────────────────┬────────────────────────────────────────┘
                         │  JSON Traffic Payloads
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FastAPI Backend                             │
└───────┬─────────────────────────────────────────────────────────┘
        │
        ▼
┌───────────────────────┐         P2P Probability > 40%?
│  🧠 SENTINEL LAYER    │ ──────────────────────────────────────┐
│  CNN Model (.h5)      │                                        │
│  Packet Analysis      │                                        ▼
└───────────────────────┘              ┌─────────────────────────────┐
                                       │  ⛓️  LEDGER LAYER            │
                                       │  Web3.py · Smart Contract    │
                                       │  Wallet License Validation   │
                                       └──────────────┬──────────────┘
                                                       │
                                                       ▼
┌───────────────────────────────────────────────────────────────┐
│  🎛️  CONTROLLER LAYER                                          │
│  SHAP XAI Generator → Base64 Plot → Action: ALLOW / BLOCK     │
└───────────────────────────────────────────────────────────────┘
```

| Layer | Role | Key Technology |
|---|---|---|
| 🧠 **Sentinel** | Classifies traffic as P2P or benign | TensorFlow CNN |
| ⛓️ **Ledger** | Verifies on-chain license ownership | Web3.py · Solidity |
| 🎛️ **Controller** | Delivers the final verdict + XAI audit | SHAP · FastAPI |

---

## 💻 Tech Stack

<table>
<tr>
<td><b>Frontend</b></td>
<td>React · Vite · Tailwind CSS v4</td>
</tr>
<tr>
<td><b>Backend</b></td>
<td>Python · FastAPI · Uvicorn</td>
</tr>
<tr>
<td><b>Machine Learning</b></td>
<td>TensorFlow / Keras (CNN) · NumPy</td>
</tr>
<tr>
<td><b>Explainable AI</b></td>
<td>SHAP · Matplotlib</td>
</tr>
<tr>
<td><b>Blockchain</b></td>
<td>Web3.py · Solidity · Ganache (Local Testnet)</td>
</tr>
</table>

---

## 🚀 Local Development Setup

### Prerequisites

Before you begin, ensure you have the following installed:

- [Node.js & npm](https://nodejs.org/)
- [Python 3.9+](https://python.org/)
- [Ganache (Truffle Suite)](https://trufflesuite.com/ganache/)

---

### Step 1 — Blockchain & Wallet Setup (Ganache)

P2Guard relies on a live smart contract for license verification. You need a local Ethereum testnet running before the backend can function.

#### A. Start Your Local Blockchain

1. Launch **Ganache** and click **Quickstart** to spin up a local testnet.
2. Confirm the RPC server is running at `http://127.0.0.1:7545` (the default port).

#### B. Deploy the Smart Contract

1. Open [Remix IDE](https://remix.ethereum.org/) in your browser.
2. Load and compile the `LicenseCheck.sol` contract from this repository.
3. In the **Deploy & Run Transactions** tab, set the Environment to **Dev - Ganache Provider** and point it to port `7545`.
4. Deploy the contract.

> **⚠️ Action Required:** Copy the deployed **Contract Address** and paste it into `app.py` at **line 34**:
> ```python
> contract_address = web3.to_checksum_address('0xYOUR_CONTRACT_ADDRESS')
> ```

#### C. Configure Frontend Wallet Addresses

To simulate the *Licensed* vs *Unlicensed* scenarios, you need to wire up two Ganache wallet addresses.

1. Open Ganache and note your available accounts.
2. Open `p2guard-dashboard/src/App.jsx` and find **lines 5–6** at the top of the file.
3. Set the variables as follows:

```js
// App.jsx — lines 5–6
const WALLET_UNLICENSED = "0xADDRESS_1_FROM_GANACHE";
const WALLET_LICENSED   = "0xADDRESS_2_FROM_GANACHE";
```

> **📝 Note:** Using Remix, manually call the smart contract to **grant a license** to Address 2 so that Scenario 2 (Licensed user) validates successfully on the backend.

---

### Step 2 — Backend (FastAPI & Machine Learning)

Navigate to the project root and install Python dependencies:

```bash
pip install -r requirements.txt
```

> No `requirements.txt`? Run this instead:
> ```bash
> pip install fastapi uvicorn tensorflow web3 shap matplotlib pydantic numpy
> ```

Start the backend server:

```bash
uvicorn app:app --reload
```

The API will be live at `http://127.0.0.1:8000`.

---

### Step 3 — Frontend (React / Vite)

Open a new terminal, navigate to the frontend directory, and start the dev server:

```bash
cd p2guard-dashboard
npm install
npm run dev
```

Visit **[http://localhost:5173](http://localhost:5173)** to interact with the P2Guard Sentinel dashboard.

---

## 🧪 Running a Simulation

Once all three services are running, you can test both enforcement scenarios from the dashboard:

| Scenario | Wallet | CNN Result | Contract Check | Final Action |
|---|---|---|---|---|
| **Normal Traffic** | — | Benign | Skipped | ✅ `ALLOW` |
| **Unlicensed P2P** | Address 1 | P2P Detected | No license found | 🚫 `BLOCK` |
| **Licensed P2P** | Address 2 | P2P Detected | License verified | ✅ `ALLOW` |

After each simulation, the dashboard renders a **SHAP beeswarm plot** — a visual XAI audit showing exactly which packet features drove the CNN's prediction.

---

## 🧠 A Note on Demonstration Data

For reproducibility and ease of setup, the **Normal Web Traffic** simulation uses a predefined heuristic array extracted from the safest baseline index of the model's test dataset. This ensures deterministic UI behavior for reviewers without requiring the full raw network dataset to be cloned locally.

---

## 📁 Project Structure

```
p2guard-sentinel/
├── app.py                    # FastAPI backend · CNN inference · Web3 integration
├── model.h5                  # Pre-trained CNN model
├── LicenseCheck.sol          # Solidity smart contract
├── requirements.txt          # Python dependencies
└── p2guard-dashboard/
    ├── src/
    │   ├── App.jsx           # Root component · wallet config (lines 5–6)
    │   └── ...
    ├── package.json
    └── vite.config.js
```

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to open a [GitHub Issue](../../issues) or submit a pull request.

---

<div align="center">

Built as a proof-of-concept exploring the intersection of **deep learning**, **blockchain**, and **explainable AI** for next-generation digital rights management.

<br/>

*P2Guard Sentinel — See everything. Trust nothing. Explain it all.*

</div>
