# Clickjacking Demo using Flask, ngrok, and SecurityHeaders

## Overview

This project demonstrates a **clickjacking-style UI redressing vulnerability** in a fake banking withdrawal flow.

The application includes:

* a **bank dashboard**
* a **vulnerable withdraw page** where a misleading click triggers a hidden sensitive action
* a **protected withdraw page** with anti-clickjacking headers
* support for exposing the local app publicly with **ngrok**
* validation of missing/present headers using **SecurityHeaders**

## Demo Goal

The goal of this project is to show:

1. how a sensitive action can be triggered through deceptive UI interaction
2. how missing anti-framing protections make a page susceptible to clickjacking
3. how to verify the vulnerability using a real security analysis tool
4. how to prevent the issue using HTTP response headers

## Tech Stack

* Python
* Flask
* HTML/CSS
* ngrok
* SecurityHeaders

## Project Structure

```text
.
├── app.py
├── templates/
│   ├── bank.html
│   ├── withdraw.html
│   └── withdraw_protected.html
└── README.md
```

## Routes

### `/bank`

Displays the fake banking dashboard.

Features:

* account name
* current balance
* navigation to withdraw pages
* transaction history
* reset button for demo reuse

### `/withdraw`

Vulnerable withdrawal page.

Behavior:

* user sees a visible button labeled **Check Offer & Continue**
* clicking it actually submits a hidden **Withdraw All** action
* this simulates a deceptive UI flow that causes an unintended sensitive operation

### `/withdraw-protected`

Protected withdrawal page.

This version adds:

* `X-Frame-Options: DENY`
* `Content-Security-Policy: frame-ancestors 'none';`

These headers prevent framing and help defend against clickjacking.

### `/process-withdraw`

Processes withdrawal requests.

Supports:

* custom amount withdrawal
* full balance withdrawal

### `/reset`

Resets the demo state:

* balance back to initial value
* transaction log cleared

## How the Vulnerability Works

On the vulnerable withdraw page, the user believes they are clicking a harmless UI control to check an offer.

However, the application is intentionally designed so that the click is registered on a hidden sensitive action instead.

Effect:

* the full balance is withdrawn
* the dashboard reflects the balance as `₹0`
* the transaction history records the action

This demonstrates the core security idea:

> user intention does not match the actual action performed

## How the Protection Works

The protected route adds anti-clickjacking headers:

```http
X-Frame-Options: DENY
Content-Security-Policy: frame-ancestors 'none';
```

These instruct the browser not to allow the page to be embedded in a frame, which is a standard clickjacking defense.

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Sailendra211/secure_coding_roleplau.git
cd secure_coding_roleplau
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
```

#### On Windows

```bash
venv\Scripts\activate
```

#### On Linux / macOS

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install flask
```

## How to Run the Application

Start the Flask app:

```bash
python app.py
```

The application will run locally at:

```text
http://127.0.0.1:5000
```

## Local Demo Flow

### Vulnerable Flow

1. Open `http://127.0.0.1:5000/bank`
2. Click **Withdraw**
3. On the vulnerable page, click **Check Offer & Continue**
4. You will be redirected back to the dashboard
5. The balance will become `₹0`
6. The transaction table will show a full withdrawal entry

### Protected Flow

1. Reset the demo using the **Reset Demo** button
2. Open **Protected Withdraw**
3. Observe that this route includes anti-clickjacking headers
4. Use SecurityHeaders to verify the protections are present

## What ngrok Does in This Project

`ngrok` is used to expose the locally running Flask application to the internet through a temporary public URL.

Why this is needed:

* local addresses such as `localhost` or `127.0.0.1` cannot be scanned by external web tools
* SecurityHeaders requires a public URL to inspect the application

### Concept

```text
localhost:5000  ->  ngrok  ->  public HTTPS URL
```

## How to Use ngrok

### 1. Make sure the Flask app is already running

```bash
python app.py
```

### 2. Start ngrok in a separate terminal

```bash
ngrok http 5000
```

If ngrok is not added to PATH on Windows, run it using the full path or from the folder containing `ngrok.exe`.

Example in PowerShell:

```powershell
& "C:\path\to\ngrok.exe" http 5000
```

### 3. Copy the forwarding URL

ngrok will display something like:

```text
Forwarding  https://your-subdomain.ngrok-free.app  ->  http://localhost:5000
```

This public URL is what you use in the browser and in SecurityHeaders.

### 4. Open the public routes

Examples:

* `https://your-subdomain.ngrok-free.app/bank`
* `https://your-subdomain.ngrok-free.app/withdraw`
* `https://your-subdomain.ngrok-free.app/withdraw-protected`

## What SecurityHeaders Does in This Project

SecurityHeaders is the **main security analysis tool** used in this project.

It checks the HTTP response headers of the page and reports whether important security protections are present or missing.

For clickjacking, the most relevant headers are:

* `X-Frame-Options`
* `Content-Security-Policy` with `frame-ancestors`

### Role distinction

* **ngrok** exposes the app publicly
* **SecurityHeaders** analyzes the app's headers

## How to Use SecurityHeaders

### 1. Start the Flask app

```bash
python app.py
```

### 2. Start ngrok

```bash
ngrok http 5000
```

### 3. Copy the public HTTPS URL from ngrok

Example:

```text
https://your-subdomain.ngrok-free.app
```

### 4. Open SecurityHeaders in the browser

Use the SecurityHeaders website and scan the following URLs:

#### Vulnerable page

```text
https://your-subdomain.ngrok-free.app/withdraw
```

#### Protected page

```text
https://your-subdomain.ngrok-free.app/withdraw-protected
```

## Expected SecurityHeaders Results

### Vulnerable `/withdraw`

Expected findings:

* missing `X-Frame-Options`
* missing `Content-Security-Policy` with `frame-ancestors`

Interpretation:

* the page lacks standard anti-clickjacking protections
* the route is susceptible to framing-based abuse

### Protected `/withdraw-protected`

Expected findings:

* `X-Frame-Options: DENY`
* `Content-Security-Policy: frame-ancestors 'none';`

Interpretation:

* the page has anti-framing protections
* the browser should block embedding attempts

## Important Note About ngrok Web Interface

ngrok also provides a local inspection interface, usually at:

```text
http://127.0.0.1:4040
```

This interface is useful for:

* viewing captured requests
* inspecting responses
* replaying traffic

However:

* `127.0.0.1:4040` is **not** the public URL to scan with SecurityHeaders
* you must use the **Forwarding** HTTPS URL shown in the ngrok terminal

## Suggested Presentation Flow

1. Run the Flask application locally
2. Open `/bank`
3. Navigate to `/withdraw`
4. Click **Check Offer & Continue**
5. Show that the full balance is withdrawn unexpectedly
6. Explain that this demonstrates deceptive triggering of a sensitive action
7. Start ngrok and copy the public URL
8. Scan `/withdraw` using SecurityHeaders
9. Show that clickjacking-related protection headers are missing
10. Scan `/withdraw-protected`
11. Show that the anti-clickjacking headers are present
12. Explain that adding these headers mitigates framing-based clickjacking

## Key Security Concept

This project demonstrates two related ideas:

* **UI redressing / deceptive interaction** in the vulnerable withdrawal flow
* **anti-clickjacking protection** through browser-enforced response headers

## Sample Viva Explanation

> This project demonstrates a vulnerable banking withdrawal flow in Flask where a misleading interface triggers a sensitive action. The local application is exposed publicly using ngrok so that external analysis tools can access it. SecurityHeaders is then used to inspect the application's HTTP response headers and confirm that the vulnerable route lacks anti-clickjacking protections, while the protected route includes X-Frame-Options and Content-Security-Policy to mitigate the issue.

## Resetting the Demo

To reset the application state:

* open the dashboard
* click **Reset Demo**

This restores:

* original balance
* empty transaction history

## Future Improvements

Possible extensions:

* persistent logging using a database
* a dedicated framed test page for strict iframe-based clickjacking demonstration
* browser devtools header inspection screenshots
* additional CSP rules
* audit logging for suspicious actions

## Author

Sailendra Kolluru
