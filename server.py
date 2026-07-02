from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Sunucuda biriken mesajları tutmak için geçici bir veri tabanı (List)
mesaj_veritabani = []

@app.route('/api/sms/gonder', methods=['POST'])
def sms_gonder_api():
    data = request.json
    
    # Termux'tan gelen verileri ayıklıyoruz
    hedef_numara = data.get('hedef')
    gonderen_numara = data.get('gonderen', '+111 222 999') # Tanımladığın sahte numara
    mesaj_icerigi = data.get('mesaj')
    
    if not hedef_numara or not mesaj_icerigi:
        return jsonify({"durum": "hata", "mesaj": "Eksik parametre gönderildi!"}), 400
        
    # --- GERÇEK DÜNYA BAĞLANTISI ---
    # Eğer gerçek SMS göndermek istersen, resmi firmanın kodunu TAM BURAYA ekliyorsun.
    # Şimdilik sistem mimarisinin çalışması için loglama yapıyoruz:
    log_verisi = {
        "zaman": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "gonderen": gonderen_numara,
        "alici": hedef_numara,
        "mesaj": mesaj_icerigi,
        "durum": "Iletildi (Gateway Mode)"
    }
    mesaj_veritabani.append(log_verisi)
    
    # Termux'a başarı raporu dönüyoruz
    print(f"\n[SUNUCU LOG] {gonderen_numara} -> {hedef_numara} numarasına mesaj bıraktı: '{mesaj_icerigi}'")
    
    return jsonify({
        "durum": "basarili",
        "mesaj": f"{hedef_numara} hattına mesaj başarıyla teslim edildi.",
        "detay": log_verisi
    }), 200

@app.route('/api/sms/raporlar', methods=['GET'])
def raporlari_listele():
    # Sunucuda biriken tüm transferleri görmek için API ucu
    return jsonify({"toplam_gonderilen": len(mesaj_veritabani), "veriler": mesaj_veritabani}), 200

if __name__ == '__main__':
    # Sunucuyu dış dünyaya açmak için host='0.0.0.0' yapıyoruz
    app.run(host='0.0.0.0', port=5000, debug=True)
