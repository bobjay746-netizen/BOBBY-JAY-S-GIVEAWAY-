from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
  <title>Bobby Jay Giveaway</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    body { font-family: Arial, sans-serif; background:#ffffff; margin:0; padding:0; color:#111; }
    .header { padding:12px; display:flex; align-items:center; border-bottom:1px solid #eee; }
    .header img { width:45px; height:45px; border-radius:50%; margin-right:10px; }
    .header h3 { margin:0; font-weight:bold; font-size:16px; }

    .balance-box { background:#0a8f3d; color:white; padding:18px; border-radius:14px; margin:12px; }
    .balance-top { display:flex; justify-content:space-between; align-items:center; font-size:14px; font-weight:bold; }
    .balance-amt { font-size:28px; font-weight:bold; margin-top:6px; }
    .balance-history { font-size:14px; margin-top:8px; font-weight:bold; }
    .balance-btn { margin-top:8px; padding:10px; background:white; color:#0a8f3d; font-weight:bold; border:none; border-radius:8px; width:100%; cursor:pointer; }

    .eye { cursor:pointer; margin-left:8px; font-size:18px; }

    .grid { display:grid; grid-template-columns: repeat(3, 1fr); gap:10px; margin:15px; }
    .btn { background:#f2fef6; padding:18px 8px; border-radius:12px; text-align:center; cursor:pointer; font-size:14px; font-weight:bold; }
    .btn:hover { background:#d6f5df; }

    #popup { display:none; position:fixed; top:50%; left:50%; transform:translate(-50%,-50%);
             background:white; border:2px solid green; padding:25px; font-size:22px; font-weight:bold;
             border-radius:12px; text-align:center; width:70%; max-width:300px; }

    .navbar { position:fixed; bottom:0; left:0; right:0; display:flex; background:#fff; border-top:1px solid #ccc; }
    .navbar div { flex:1; text-align:center; padding:10px 0; font-weight:bold; font-size:13px; cursor:pointer; }

    /* form modal */
    #formModal { display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.5); }
    #formBox { background:white; padding:18px; width:85%; max-width:360px; margin:90px auto; border-radius:12px; }
    #formBox h3 { margin-top:0; font-weight:bold; font-size:16px; text-align:center; }
    input { width:95%; padding:10px; margin:6px 0; border:1px solid #ccc; border-radius:6px; font-size:14px; }
    button { background:#0a8f3d; color:white; padding:10px; border:none; border-radius:6px; cursor:pointer; font-weight:bold; width:48%; }
    .btn-row { display:flex; justify-content:space-between; margin-top:10px; }
    .cancel { background:#777; }
  </style>
  <script>
    let balanceVisible = true;
    let balance = 100000;

    function toggleBalance(){
      let bal = document.getElementById("balance");
      let eye = document.getElementById("eyeIcon");
      if(balanceVisible){
        bal.innerText = "*****";
        eye.innerText = "🙈";
      } else {
        bal.innerText = "₦" + balance.toLocaleString();
        eye.innerText = "👁️";
      }
      balanceVisible = !balanceVisible;
    }

    function doAction(name){
      if (name=="To OPay" || name=="To Bank" || name=="Withdraw"){
        document.getElementById("formModal").style.display="block";
        document.getElementById("formAction").value=name;
      } else {
        fetch("/action/"+name).then(r=>r.json()).then(data=>{
          showPopup(data.message, data.success);
        });
      }
    }
    function closeForm(){ document.getElementById("formModal").style.display="none"; }
    function submitForm(){
      let name = document.getElementById("fname").value;
      let acc = document.getElementById("facc").value;
      let bank = document.getElementById("fbank").value;
      let amt = parseInt(document.getElementById("famt").value);
      let action = document.getElementById("formAction").value;

      if(isNaN(amt) || amt <= 0){
        alert("Please enter a valid amount");
        return;
      }
      if(amt > balance){
        alert("Insufficient Balance!");
        return;
      }

      balance -= amt;
      document.getElementById("balance").innerText = "₦" + balance.toLocaleString();
      document.getElementById("history").innerText = "₦" + amt.toLocaleString() + " Sent";

      closeForm();
      showPopup("Sent Successfully ✅", true);
    }

    function showPopup(msg, success=false){
      let popup = document.getElementById("popup");
      popup.innerText = msg;
      popup.style.color = success ? "green" : "black";
      popup.style.display = "block";
      setTimeout(()=>popup.style.display="none", 2500);
    }
  </script>
</head>
<body>
  <div class="header">
    <img src="https://via.placeholder.com/40" alt="Profile">
    <h3>Hi, welcome to Bobby Jay Giveaway 🎉</h3>
  </div>

  <div class="balance-box">
    <div class="balance-top">
      <span>Available Balance <span id="eyeIcon" class="eye" onclick="toggleBalance()">👁️</span></span>
      <span>Transaction History</span>
    </div>
    <div class="balance-amt" id="balance">₦100,000</div>
    <div class="balance-history" id="history"></div>
    <button class="balance-btn">+ Add Money</button>
  </div>

  <div class="grid">
    <div class="btn" onclick="doAction('To OPay')">To OPay</div>
    <div class="btn" onclick="doAction('To Bank')">To Bank</div>
    <div class="btn" onclick="doAction('Withdraw')">Withdraw</div>
    <div class="btn" onclick="doAction('Airtime')">Airtime</div>
    <div class="btn" onclick="doAction('Data')">Data</div>
    <div class="btn" onclick="doAction('Betting')">Betting</div>
    <div class="btn" onclick="doAction('TV')">TV</div>
    <div class="btn" onclick="doAction('Safebox')">Safebox</div>
    <div class="btn" onclick="doAction('Check-In')">Check-In</div>
    <div class="btn" onclick="doAction('Refer & Earn')">Refer & Earn</div>
    <div class="btn" onclick="doAction('More')">More</div>
  </div>

  <div id="popup"></div>

  <div class="navbar">
    <div onclick="showPopup('Home Page (Demo)')">Home</div>
    <div onclick="showPopup('Rewards Page (Demo)')">Rewards</div>
    <div onclick="showPopup('Finance Page (Demo)')">Finance</div>
    <div onclick="showPopup('Cards Page (Demo)')">Cards</div>
    <div onclick="showPopup('Profile Page (Demo)')">Me</div>
  </div>

  <!-- form modal -->
  <div id="formModal">
    <div id="formBox">
      <h3>Enter Transfer Details</h3>
      <input id="fname" placeholder="Your Name" required>
      <input id="facc" placeholder="Account Number" required>
      <input id="fbank" placeholder="Bank Name" required>
      <input id="famt" placeholder="Amount" type="number" required>
      <input type="hidden" id="formAction">
      <div class="btn-row">
        <button onclick="submitForm()">Send</button>
        <button class="cancel" onclick="closeForm()">Cancel</button>
      </div>
    </div>
  </div>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/action/<name>")
def action(name):
    return jsonify({"message": f"{name} service in progress", "success": False})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)