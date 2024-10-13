import time
from flask import Flask,request,g,render_template,redirect,url_for,session
import uiautomator2
from uiautomator2 import Direction
from ppadb.client import Client as AdbClient
from bin.lib.lib_adb import LibAdb
from threading import Thread
import subprocess
app = Flask(__name__)
data_adb = []
def loop_check_adb():
    global data_adb
    while True:
        try:
            main_adb = LibAdb()
            data_adb = main_adb.list_adb()
            time.sleep(1)
        except:
            pass

Thread(target=loop_check_adb).start()
def run_adb_command(cmd):
    """Run an ADB shell command and print the output."""
    result = subprocess.run(f"adb shell {cmd}", shell=True, capture_output=True, text=True)
    print(result.stdout)
    print(result.stderr)

# package = "com.kasikorn.retail.mbanking.wap"
# name_adb = "WWTWDQ4XX48XIBTO"
# url = ""
# adb = uiautomator2.connect(name_adb)
# adb.open_url(url)
#http://192.168.0.63:56485?device=WWTWDQ4XX48XIBTO&token=KMBCYB000000000CBDCC53FC8E84BFF82D0A21FFFCC529A
#https://kpaymentgateway-services.kasikornbank.com/KPGW-Redirect-Webapi/Appswitch/KMBCYB000000000CBDCC53FC8E84BFF82D0A21FFFCC529A
@app.route("/devices",methods=["GET"])
def get_devices_all():
    main_adb = LibAdb()
    data_adb = main_adb.list_adb()
    return  data_adb


@app.route("/",methods=["GET", "POST"])
def index():
    global data_adb
    try:
        start_time = time.time()
        time_out = 60
        data = request.args
        device = data["device"]
        token = data["token"]
        link = f"https://kpaymentgateway-services.kasikornbank.com/KPGW-Redirect-Webapi/Appswitch/{token}"
        pin = "112233"
        if device not in data_adb:
            return {"status":False,"msg":"check name device"}
        package = "com.kasikorn.retail.mbanking.wap"
        adb = uiautomator2.connect(device)
        print(adb.info)
        if adb.info['currentPackageName'] == "com.android.systemui":
            adb.screen_on()
            adb.swipe_ext(Direction.FORWARD)
            # run_adb_command("input keyevent KEYCODE_WAKEUP")  # Turn on the screen
            # run_adb_command("input swipe 300 1000 300 500")  # Swipe up (for swipe unlock)
        adb.app_stop(package)
        adb.open_url(link)
        while True:
            if time.time() - start_time >= time_out:
                adb.app_stop(package)
                return {"status":False,"msg":"time_out"}

            try:
                adb(text="ขออภัย").get_text(timeout=0.1)
                adb.app_stop(package)
                return {"status":False,"msg":"check token"}
            except:
                pass
            try:
                check_pin = adb(text="กรุณาใส่รหัสผ่าน").get_text(timeout=0.1)
                print(check_pin)
                break
            except:
                pass
        time.sleep(1)
        for p in pin:
                    adb(resourceId=f"com.kasikorn.retail.mbanking.wap:id/linear_layout_button_activity_{p}").click()
                    time.sleep(0.5)
        data_json = {}
        while True:
            if time.time() - start_time >= time_out:
                adb.app_stop(package)
                return {"status":False,"msg":"time_out"}
            try:
                adb(text="ยืนยันรายการ").get_text(timeout=0.1)
                data_info = adb(className="android.widget.TextView")
                print(data_info.count)
                data_json = {
                    "from":data_info[-5].get_text(),
                    "to":data_info[-4].get_text(),
                    "amount":data_info[-3].get_text(),
                    "fee":data_info[-2].get_text(),
                    "number":data_info[-1].get_text(),
                }
                break
            except:
                pass

        while True:
            if time.time() - start_time >= time_out:
                adb.app_stop(package)
                return {"status":False,"msg":"time_out"}
            try:
                adb(text="ยืนยัน").click(timeout=0.5)
            except:
                pass
            try:
                adb(text="ดำเนินการเสร็จสิ้น").get_text(timeout=0.1)
                adb.app_stop(package)
                return {"status":True,"msg":data_json}
            except:
                pass
    except Exception as e:
        return {"status":False,"msg":f"error : {e}"}







if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=56485)

# {'errorCode': '00', 'qrBase64': 'data:image/png;base64,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', 'tokenId': 'KMBCYB0000000001F8AC5280A2D44C2BE4F7F8F100DB6A8', 'link': 'https://kplus.kasikornbank.com/authenwithkplus/?tokenId=KMBCYB0000000001F8AC5280A2D44C2BE4F7F8F100DB6A8&nextAction=authenwithkplus', 'expQr': '6', 'transType': 'FTOT', 'transferType': 'Online', 'bulk': 'N', 'fromAccountNo': '1178114472', 'fromAccountNoMasking': 'xxx-x-x1447-x', 'fromAccountName': 'นาย สรศักดิ์ ธุระหาย', 'beneficiaryNo': '1761711527', 'beneficiaryNoMasking': '176-1-71152-7', 'beneficiaryName': 'MRS. NOUTHIP VONGVANE', 'amount': '3', 'feeAmount': '0', 'totalAmount': '3', 'transStatus': 'S', 'effectiveDate': '2024-07-26 15:20:18.178', 'lang': 'th', 'memo': '', 'memoTypeId': '12', 'notiEmailNote': '', 'errorMsg': 'Success', 'reqRefNo': 'TRBS240726964088208', 'scheduleFlag': 'N', 'rqUID': '069_20240726_8FE3D9FE3CAB4183B9732524E98B74EA', 'attachFileName': '', 'smsLang': 'th', 'createDate': '2024-07-26 15:20:18.178', 'beneficiaryNoMaskingSms': 'xxx-x-x1152-x', 'bankCode': '004'}
# https://kpaymentgateway-services.kasikornbank.com/KPGW-Redirect-Webapi/Appswitch/KMBCYB0000000001F8AC5280A2D44C2BE4F7F8F100DB6A8
