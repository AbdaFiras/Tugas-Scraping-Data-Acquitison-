from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

def scrape_maps_v3(url, target_count=1200):
    options = webdriver.ChromeOptions()
    # Menghilangkan deteksi bot agar tidak diblokir Google
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(options=options)
    
    driver.get(url)
    driver.maximize_window()
    print("Sedang memuat halaman... Tunggu 10 detik.")
    time.sleep(10) 

    reviews_data = []
    seen_users = set()

    try:
        # Cari container
        print("Mencari panel ulasan...")
        try:
            
            sample_review = driver.find_element(By.CLASS_NAME, "jftiEf")
            papan_scroll = sample_review.find_element(By.XPATH, "./ancestor::div[contains(@class, 'm686Fd') or @role='main' or @tabindex='-1']")
            print("Panel ulasan ditemukan!")
        except:
            print("Gagal deteksi otomatis. Mencoba teknik paksa...")
            # Jika gagal pakai target div yang paling umum di Maps
            papan_scroll = driver.find_element(By.CSS_SELECTOR, "div[role='main']")

        while len(reviews_data) < target_count:
            # Ambil semua blok ulasan
            elements = driver.find_elements(By.CLASS_NAME, "jftiEf")
            
            for el in elements:
                try:
                    # Ambil Username sebagai ID unik
                    user = el.find_element(By.CLASS_NAME, "d4r55").text
                    if user in seen_users:
                        continue
                    
                    seen_users.add(user)

                    # Klik Lainnya jika teks ulasan panjang
                    try:
                        more_btn = el.find_element(By.CSS_SELECTOR, "button.w8nwRe")
                        driver.execute_script("arguments[0].click();", more_btn)
                    except:
                        pass

                    # Ekstrak Data
                    isi = el.find_element(By.CLASS_NAME, "wiI7pd").text
                    rating = el.find_element(By.CLASS_NAME, "kvMYJc").get_attribute("aria-label")
                    waktu = el.find_element(By.CLASS_NAME, "rsqaWe").text

                    reviews_data.append({
                        "Username": user,
                        "Rating": rating,
                        "Isi Ulasan": isi,
                        "Waktu Ulasan": waktu
                    })

                    if len(reviews_data) >= target_count: break
                except:
                    continue

            print(f"Terkumpul: {len(reviews_data)}/{target_count}")

            papan_scroll.send_keys(Keys.END)
            time.sleep(3) 

    except Exception as e:
        print(f"Berhenti karena: {e}")
    
    finally:
        if reviews_data:
            df = pd.DataFrame(reviews_data)
            df.to_csv("data_maps_final.csv", index=False, encoding='utf-8')
            print(f"Data tersimpan! Total: {len(reviews_data)} ulasan.")
        driver.quit()

url_target = "https://www.google.com/maps/place/Tugu+Jogja/@-7.7829165,110.3622048,17z/data=!4m18!1m9!3m8!1s0x2e7a591a4d553bd5:0xc0f964003add568b!2sTugu+Jogja!8m2!3d-7.7829218!4d110.3670757!9m1!1b1!16s%2Fg%2F122zk22q!3m7!1s0x2e7a591a4d553bd5:0xc0f964003add568b!8m2!3d-7.7829218!4d110.3670757!9m1!1b1!16s%2Fg%2F122zk22q?entry=ttu&g_ep=EgoyMDI2MDMwOC4wIKXMDSoASAFQAw%3D%3D" 
scrape_maps_v3(url_target, target_count=1200)