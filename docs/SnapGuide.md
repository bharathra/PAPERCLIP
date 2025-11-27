# Snap Creation and Publishing Guide

## 1. Building the Snap
To build the snap package, run the following command in the root of the project:
```bash
snapcraft
```
This will generate a `.snap` file (e.g., `paperclip_1.0.0_amd64.snap`).

## 2. Publishing to the Snap Store

### Prerequisites
- A Ubuntu One account.
- `snapcraft` installed.

### Steps

#### 1. Create a Developer Account
Create an account at [dashboard.snapcraft.io](https://dashboard.snapcraft.io/).

#### 2. Register Your App Name
Register the name defined in `snapcraft.yaml`:
```bash
snapcraft register paperclip
```

#### 3. Login
Authenticate your local tool:
```bash
snapcraft login
```

#### 4. Upload
Push your built `.snap` file to the store (stable channel):
```bash
snapcraft upload --release=stable paperclip_1.0.0_amd64.snap
```

#### 5. Manage
Visit [dashboard.snapcraft.io](https://dashboard.snapcraft.io/) to manage metadata and releases.
