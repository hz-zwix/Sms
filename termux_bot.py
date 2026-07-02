import requests
import os
import sys

# UYARI: Eğer sunucuyu kendi bilgisayarında çalıştırıyorsan
# Bilgisayarının yerel IP adresini (örn: http://11.22.33.44:5000) buraya yazmalısın.
API_URL = "http://localhost:5000/api/sms"

def temizle():
    os.system('clear')

def banner():
    print("""
    \033[36m==================================================
    * CRIMSON SMS GATEWAY CONTROL PANEL        *
    * [ Termux v1.0 ]                  *
    ==================================================\033[0m
    """)

def sms_gonder_arayuz():
    temizle()
    banner()
    print("\033[33m[+] Yurt İçi / Yurt Dışı Canlı SMS Gönderimi\033[0m\n")
    
    hedef = input("-> Hedef Telefon Numarası (Örn: +905xxx): ")
    gonderen = "+111 222 999" # İstediğin o özel numara
    mesaj = input("-> Gönderilecek Mesaj Metni: ")
    
    if not hedef or not mesaj:
        print("\n\033[31m[X] Hata: Numara veya mesaj alanı boş bırakılamaz!\033[0m")
        input("\nDevam etmek için ENTER...")
        return

    # Veriyi paketliyoruz (JSON verisi)
    payload = {
        "hedef": hedef,
        "gonderen": gonderen,
        "mesaj": mesaj
    }
    
    print("\n\033[34m[*] Veri paketleniyor ve API Sunucusuna aktarılıyor...\033[0m")
    
    try:
        # Sunucuya POST isteği atıyoruz
        response = requests.post(f"{API_URL}/gonder", json=payload, timeout=7)
        
        if response.status_code == 200:
            sonuc = response.json()
            print(f"\n\033[32m[✓] DURUM: {sonuc['mesaj']}\033[0m")
            print(f"       Zaman stampası: {sonuc['detay']['zaman']}")
            print(f"       Kullanılan Hat: {sonuc['detay']['gonderen']}")
        else:
            print(f"\n\033[31m[X] Sunucu Hatası: {response.status_code}\033[0m")
            
    except requests.exceptions.ConnectionError:
        print("\n\033[31m[X] Hata: Sunucu aktif değil veya URL yanlış!\033[0m")
        print("    Lütfen server.py kodunun açık olduğundan emin olun.")

    input("\nAna menüye dönmek için ENTER'a basın...")

def ana_menu():
    while True:
        temizle()
        banner()
        print(" 1 - Canlı SMS Gönder (Özel İçerikli)")
        print(" 2 - Sunucu Loglarını/Raporlarını Çek")
        print(" 3 - Çıkış Yap\n")
        
        secim = input("Seçiminiz (1/2/3): ")
        
        if secim == "1":
            sms_gonder_arayuz()
        elif secim == "2":
            temizle()
            banner()
            print("\033[34m[*] Sunucudan veri tabanı kayıtları isteniyor...\033[0m\n")
            try:
                res = requests.get(f"{API_URL}/raporlar")
                veriler = res.json()
                print(f"Toplam Başarılı Trafik: {veriler['toplam_gonderilen']}\n")
                for log in veriler['veriler']:
                    print(f"[{log['zaman']}] {log['gonderen']} -> {log['alici']}: {log['mesaj']}")
            except:
                print("[X] Sunucuya bağlanılamadı.")
            input("\nDevam etmek için ENTER...")
        elif secim == "3":
            print("\n[*] Oturum kapatıldı.")
            sys.exit()
        else:
            print("\n[!] Geçersiz hamle.")
            os.system('sleep 1')

if __name__ == "__main__":
    ana_menu()
